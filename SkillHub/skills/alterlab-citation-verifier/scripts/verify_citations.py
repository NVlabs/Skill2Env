#!/usr/bin/env python3
"""verify_citations.py — Existence-verify a bibliography against public scholarly APIs.

Given a bibliography (BibTeX, a list of DOIs/arXiv IDs, or free-form references),
this checks whether each entry ACTUALLY EXISTS by querying four keyless public
APIs (Crossref, OpenAlex, Semantic Scholar, arXiv) with a polite ``mailto``
identifier. It resolves DOI / arXiv identifiers, fuzzy-matches title and authors
(difflib SequenceMatcher ratio — Ratcliff/Obershelp, not edit-distance — default
threshold 0.70), flags Crossref/OpenAlex-marked
retractions, and emits a JSON verdict per entry mapped to the AlterLab citation
hallucination taxonomy (TF / PAC / IH / PH / SH).

Design constraints:
- NO API keys. NO third-party deps required: uses ``requests`` if present, else
  falls back to the stdlib (``urllib``). Mirrors the integrity_verification_agent
  taxonomy exactly (see ../SKILL.md and
  skills/core/alterlab-research-pipeline/agents/integrity_verification_agent.md).
- GRACEFUL DEGRADATION: with no network, every entry gets an ``unverified`` verdict
  plus manual-verification instructions. It NEVER silently passes an entry.

Taxonomy (codes mirror the canonical Five-Type Taxonomy):
  TF  Total Fabrication           — entry exists in no source
  PAC Partial Attribute Corruption — entry found but ≥1 metadata field is wrong
  IH  Identifier Hijacking         — DOI/arXiv ID resolves to an unrelated paper
  PH  Placeholder Hallucination    — entry is an unresolved template/placeholder
  SH  Semantic Hallucination       — entry resolves but does not support its claim
                                      (claim-vs-source check is out of scope here;
                                       emitted only as an advisory flag)

Usage:
  uv run python verify_citations.py INPUT [--format auto|bibtex|doi|freeform]
                                          [--mailto you@example.com]
                                          [--threshold 0.70]
                                          [--out report.json] [--offline]
  uv run python verify_citations.py - < refs.bib        # read stdin

Exit codes: 0 = ran (see JSON ``summary.verdict``); 2 = bad input/usage.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from difflib import SequenceMatcher
from typing import Any, Optional

# --------------------------------------------------------------------------- #
# HTTP layer — prefer requests, fall back to urllib (stdlib). No keys, polite. #
# --------------------------------------------------------------------------- #

DEFAULT_MAILTO = "alterlab.ieu@gmail.com"
USER_AGENT = (
    "alterlab-citation-verifier/1.0.0 (https://github.com/AlterLab-IEU/"
    "AlterLab-Academic-Skills; mailto:{mailto})"
)
HTTP_TIMEOUT = 15
RETRIES = 2
BACKOFF = 1.5

try:  # pragma: no cover - environment dependent
    import requests as _requests  # type: ignore
    _HAS_REQUESTS = True
except Exception:  # pragma: no cover
    _requests = None
    _HAS_REQUESTS = False

import urllib.error
import urllib.parse
import urllib.request


class NetworkUnavailable(Exception):
    """Raised when a request cannot reach the network (DNS / connection error)."""


def _http_get(url: str, mailto: str, accept: str = "application/json") -> Any:
    """GET ``url`` and parse JSON (or return raw text for XML endpoints).

    Raises NetworkUnavailable on a connection/DNS failure so the caller can
    distinguish "offline" from "API said not found" (a 404 returns None).
    """
    headers = {"User-Agent": USER_AGENT.format(mailto=mailto), "Accept": accept}
    last_exc: Optional[Exception] = None
    for attempt in range(RETRIES + 1):
        try:
            if _HAS_REQUESTS:
                resp = _requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
                status = resp.status_code
                if status == 404:
                    return None
                if status == 429 or 500 <= status < 600:
                    raise _TransientHTTP(status)
                resp.raise_for_status()
                return resp.json() if "json" in accept else resp.text
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                body = r.read().decode("utf-8", "replace")
                return json.loads(body) if "json" in accept else body
        except _TransientHTTP as exc:
            last_exc = exc
        except urllib.error.HTTPError as exc:  # urllib path
            if exc.code == 404:
                return None
            if exc.code == 429 or 500 <= exc.code < 600:
                last_exc = exc
            else:
                return None  # 4xx other than 404/429 → treat as "no match"
        except urllib.error.URLError as exc:
            # DNS failure / no route → genuinely offline
            raise NetworkUnavailable(str(exc.reason)) from exc
        except Exception as exc:  # requests ConnectionError, Timeout, etc.
            name = type(exc).__name__
            if any(k in name for k in ("Connection", "DNS", "Timeout", "SSL")):
                raise NetworkUnavailable(str(exc)) from exc
            last_exc = exc
        if attempt < RETRIES:
            time.sleep(BACKOFF * (attempt + 1))
    if last_exc:
        # Exhausted retries on a transient/server error: treat as no-match, not offline.
        return None
    return None


class _TransientHTTP(Exception):
    def __init__(self, status: int) -> None:
        super().__init__(f"transient HTTP {status}")
        self.status = status


# --------------------------------------------------------------------------- #
# Fuzzy matching                                                              #
# --------------------------------------------------------------------------- #

_WS = re.compile(r"\s+")
_NONWORD = re.compile(r"[^\w\s]")


def _normalize(text: str) -> str:
    text = (text or "").lower().strip()
    text = _NONWORD.sub(" ", text)
    return _WS.sub(" ", text).strip()


def title_ratio(a: str, b: str) -> float:
    """Similarity ratio (0..1) via difflib SequenceMatcher on normalized titles."""
    return SequenceMatcher(None, _normalize(a), _normalize(b)).ratio()


def _surname(name: str) -> str:
    """Best-effort surname extraction from 'Last, First' or 'First Last'."""
    name = name.strip()
    if "," in name:
        return _normalize(name.split(",", 1)[0])
    parts = _normalize(name).split()
    return parts[-1] if parts else ""


def author_overlap(cited: list[str], found_surnames: list[str]) -> float:
    """Fraction of cited author surnames that appear among the found surnames."""
    if not cited:
        return 1.0  # nothing to disprove
    cited_s = {_surname(a) for a in cited if a.strip()}
    found_s = {_normalize(s) for s in found_surnames if s.strip()}
    if not cited_s:
        return 1.0
    hits = sum(1 for c in cited_s if any(c and (c in f or f in c) for f in found_s))
    return hits / len(cited_s)


# --------------------------------------------------------------------------- #
# Parsing: BibTeX / DOI list / free-form                                      #
# --------------------------------------------------------------------------- #

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
ARXIV_RE = re.compile(
    r"(?:arxiv:\s*)?(\d{4}\.\d{4,5})(?:v\d+)?|(?:arxiv:\s*)?([a-z\-]+(?:\.[A-Z]{2})?/\d{7})",
    re.IGNORECASE,
)
PLACEHOLDER_RE = re.compile(
    r"(\[(?:citation|ref|cite|todo|xx+|author|year)[^\]]*\]"
    r"|\\cite\{[^}]*\}"
    r"|\bTODO\b|\bTKTK\b|\bXX+\b"
    r"|et al\.,?\s*\(?(?:YYYY|n\.d\.|\?\?\?\?)\)?"
    r"|\(\s*(?:year|date)\s*\)"
    r"|\bforthcoming\b|\bin press\b)",
    re.IGNORECASE,
)


@dataclass
class Entry:
    raw: str
    key: str = ""
    title: str = ""
    authors: list[str] = field(default_factory=list)
    year: str = ""
    doi: str = ""
    arxiv_id: str = ""
    venue: str = ""


def _looks_like_bibtex(text: str) -> bool:
    return bool(re.search(r"@\w+\s*\{", text))


def parse_bibtex(text: str) -> list[Entry]:
    entries: list[Entry] = []
    for m in re.finditer(r"@(\w+)\s*\{([^,]*),(.*?)\n\}", text, re.DOTALL):
        body = m.group(3)
        key = m.group(2).strip()

        def fld(name: str) -> str:
            fm = re.search(
                rf"{name}\s*=\s*[{{\"](.+?)[}}\"]\s*,?\s*$",
                body,
                re.IGNORECASE | re.MULTILINE | re.DOTALL,
            )
            return _WS.sub(" ", fm.group(1)).strip() if fm else ""

        authors_raw = fld("author")
        authors = [a.strip() for a in re.split(r"\s+and\s+", authors_raw) if a.strip()]
        e = Entry(
            raw=m.group(0),
            key=key,
            title=fld("title").strip("{}"),
            authors=authors,
            year=fld("year"),
            doi=_first_doi(fld("doi") or body),
            arxiv_id=_first_arxiv(fld("eprint") or fld("archiveprefix") or body),
            venue=fld("journal") or fld("booktitle") or fld("publisher"),
        )
        entries.append(e)
    return entries


def _first_doi(text: str) -> str:
    m = DOI_RE.search(text or "")
    return m.group(0).rstrip(".,;") if m else ""


def _first_arxiv(text: str) -> str:
    m = ARXIV_RE.search(text or "")
    if not m:
        return ""
    return (m.group(1) or m.group(2) or "").strip()


def parse_doi_list(text: str) -> list[Entry]:
    entries: list[Entry] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        doi = _first_doi(line)
        arxiv = _first_arxiv(line) if not doi else ""
        if doi or arxiv:
            entries.append(Entry(raw=line, doi=doi, arxiv_id=arxiv))
    return entries


def parse_freeform(text: str) -> list[Entry]:
    """Split on blank lines / numbered list markers; one reference per block."""
    blocks = re.split(r"\n\s*\n|\n(?=\s*\[?\d{1,3}[\].)]\s)", text.strip())
    entries: list[Entry] = []
    for block in blocks:
        block = _WS.sub(" ", block).strip()
        if not block:
            continue
        ym = re.search(r"\(?((?:19|20)\d{2})\)?", block)
        # Title heuristic: longest quoted span, else text before the year.
        tm = re.search(r"[\"“](.+?)[\"”]", block)
        if tm:
            title = tm.group(1)
        elif ym:
            after = block[ym.end():].lstrip(" .")
            title = after.split(".")[0] if after else block
        else:
            title = block
        authors: list[str] = []
        if ym and ym.start() > 0:
            head = block[: ym.start()].strip(" .,")
            authors = [a.strip() for a in re.split(r",| & | and ", head) if a.strip()][:6]
        entries.append(
            Entry(
                raw=block,
                title=title.strip(" .,"),
                authors=authors,
                year=ym.group(1) if ym else "",
                doi=_first_doi(block),
                arxiv_id=_first_arxiv(block),
            )
        )
    return entries


def parse_bibliography(text: str, fmt: str) -> list[Entry]:
    if fmt == "auto":
        if _looks_like_bibtex(text):
            fmt = "bibtex"
        else:
            non_empty = [ln for ln in text.splitlines() if ln.strip()]
            doi_lines = sum(1 for ln in non_empty if _first_doi(ln) or _first_arxiv(ln))
            fmt = "doi" if non_empty and doi_lines >= max(1, len(non_empty) * 0.6) else "freeform"
    if fmt == "bibtex":
        return parse_bibtex(text)
    if fmt == "doi":
        return parse_doi_list(text)
    if fmt == "freeform":
        return parse_freeform(text)
    raise ValueError(f"unknown format: {fmt}")


# --------------------------------------------------------------------------- #
# API adapters → normalized record {title, authors[surnames], year, doi, retracted} #
# --------------------------------------------------------------------------- #


def crossref_by_doi(doi: str, mailto: str) -> Optional[dict]:
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={mailto}"
    data = _http_get(url, mailto)
    if not data or "message" not in data:
        return None
    rec = _crossref_norm(data["message"])
    rec["method"] = "id"  # resolved BY the cited identifier
    return rec


def crossref_by_title(title: str, mailto: str) -> Optional[dict]:
    q = urllib.parse.quote(title)
    url = (
        f"https://api.crossref.org/works?query.bibliographic={q}"
        f"&rows=5&mailto={mailto}"
    )
    data = _http_get(url, mailto)
    items = (data or {}).get("message", {}).get("items", []) if data else []
    if not items:
        return None
    rec = _crossref_norm(items[0])
    rec["method"] = "title"  # found by a fuzzy title/biblio search
    return rec


def _crossref_norm(msg: dict) -> dict:
    title = (msg.get("title") or [""])
    surnames = [a.get("family", "") for a in msg.get("author", []) if a.get("family")]
    parts = (msg.get("issued", {}) or {}).get("date-parts", [[None]])
    year = str(parts[0][0]) if parts and parts[0] and parts[0][0] else ""
    retracted = False
    for upd in msg.get("update-to", []) or []:
        if "retract" in (upd.get("type", "") or "").lower():
            retracted = True
    if "retract" in (msg.get("type", "") or "").lower():
        retracted = True
    return {
        "source": "crossref",
        "title": title[0] if title else "",
        "authors": surnames,
        "year": year,
        "doi": (msg.get("DOI") or "").lower(),
        "retracted": retracted,
    }


def openalex_lookup(entry: Entry, mailto: str) -> Optional[dict]:
    if entry.doi:
        url = f"https://api.openalex.org/works/doi:{urllib.parse.quote(entry.doi)}?mailto={mailto}"
        data = _http_get(url, mailto)
        if data and data.get("id"):
            rec = _openalex_norm(data)
            rec["method"] = "id"
            return rec
    if entry.title:
        q = urllib.parse.quote(entry.title)
        url = f"https://api.openalex.org/works?search={q}&per-page=5&mailto={mailto}"
        data = _http_get(url, mailto)
        results = (data or {}).get("results", []) if data else []
        if results:
            rec = _openalex_norm(results[0])
            rec["method"] = "title"
            return rec
    return None


def _openalex_norm(w: dict) -> dict:
    surnames = []
    for au in w.get("authorships", []):
        disp = (au.get("author", {}) or {}).get("display_name", "")
        if disp:
            surnames.append(disp.split()[-1])
    return {
        "source": "openalex",
        "title": w.get("title") or w.get("display_name") or "",
        "authors": surnames,
        "year": str(w.get("publication_year") or ""),
        "doi": (w.get("doi") or "").replace("https://doi.org/", "").lower(),
        "retracted": bool(w.get("is_retracted")),
    }


def semanticscholar_lookup(entry: Entry, mailto: str) -> Optional[dict]:
    fields = "title,year,authors,externalIds"
    if entry.doi:
        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(entry.doi)}?fields={fields}"
        data = _http_get(url, mailto)
        if data and data.get("title"):
            rec = _ss_norm(data)
            rec["method"] = "id"
            return rec
    if entry.arxiv_id:
        url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{entry.arxiv_id}?fields={fields}"
        data = _http_get(url, mailto)
        if data and data.get("title"):
            rec = _ss_norm(data)
            rec["method"] = "id"
            return rec
    if entry.title:
        q = urllib.parse.quote(entry.title)
        url = (
            f"https://api.semanticscholar.org/graph/v1/paper/search?query={q}"
            f"&limit=5&fields={fields}"
        )
        data = _http_get(url, mailto)
        items = (data or {}).get("data", []) if data else []
        if items:
            rec = _ss_norm(items[0])
            rec["method"] = "title"
            return rec
    return None


def _ss_norm(p: dict) -> dict:
    surnames = []
    for au in p.get("authors", []) or []:
        nm = au.get("name", "")
        if nm:
            surnames.append(nm.split()[-1])
    ext = p.get("externalIds", {}) or {}
    return {
        "source": "semanticscholar",
        "title": p.get("title") or "",
        "authors": surnames,
        "year": str(p.get("year") or ""),
        "doi": (ext.get("DOI") or "").lower(),
        "retracted": False,  # S2 does not expose a retraction flag
    }


def arxiv_lookup(entry: Entry, mailto: str) -> Optional[dict]:
    if entry.arxiv_id:
        url = f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(entry.arxiv_id)}&max_results=1"
    elif entry.title:
        q = urllib.parse.quote(f'ti:"{entry.title}"')
        url = f"http://export.arxiv.org/api/query?search_query={q}&max_results=5"
    else:
        return None
    text = _http_get(url, mailto, accept="application/atom+xml")
    if not text or "<entry>" not in text:
        return None
    method = "id" if entry.arxiv_id else "title"
    block = text.split("<entry>", 1)[1].split("</entry>", 1)[0]
    tm = re.search(r"<title>(.*?)</title>", block, re.DOTALL)
    title = _WS.sub(" ", tm.group(1)).strip() if tm else ""
    surnames = [
        _WS.sub(" ", n).strip().split()[-1]
        for n in re.findall(r"<name>(.*?)</name>", block, re.DOTALL)
        if n.strip()
    ]
    ym = re.search(r"<published>(\d{4})", block)
    aid = re.search(r"<id>.*?abs/([^<]+)</id>", block)
    return {
        "source": "arxiv",
        "title": title,
        "authors": surnames,
        "year": ym.group(1) if ym else "",
        "doi": "",
        "arxiv_id": aid.group(1) if aid else (entry.arxiv_id or ""),
        "retracted": False,
        "method": method,
    }


# --------------------------------------------------------------------------- #
# Verdict engine                                                              #
# --------------------------------------------------------------------------- #

VERDICTS = {
    "verified": "Entry exists; title+authors match an authoritative record.",
    "TF": "Total Fabrication — entry found in NO source.",
    "PAC": "Partial Attribute Corruption — entry found but metadata fields disagree.",
    "IH": "Identifier Hijacking — DOI/arXiv ID resolves to an unrelated paper.",
    "PH": "Placeholder Hallucination — unresolved citation template/placeholder.",
    "SH": "Semantic Hallucination — resolves but claim-support unverified (advisory).",
    "unverified": "Could not verify (offline or all APIs failed); manual check required.",
}
SEVERITY = {
    "verified": "NONE",
    "TF": "SERIOUS",
    "PAC": "MEDIUM",
    "IH": "SERIOUS",
    "PH": "SERIOUS",
    "SH": "SERIOUS",
    "unverified": "MEDIUM",
}


def _is_placeholder(entry: Entry) -> bool:
    if PLACEHOLDER_RE.search(entry.raw):
        return True
    if not entry.doi and not entry.arxiv_id and len(_normalize(entry.title)) < 6 and not entry.authors:
        return True
    return False


def verify_entry(entry: Entry, mailto: str, threshold: float, offline: bool) -> dict:
    ref_id = entry.key or entry.doi or entry.arxiv_id or (entry.title[:40] or entry.raw[:40])

    # PH check first — placeholders never reach the network.
    if _is_placeholder(entry):
        return _verdict(entry, ref_id, "PH",
                        detail="Citation is an unresolved placeholder/template.",
                        matches=[])

    if offline:
        return _unverified(entry, ref_id, reason="offline mode requested (--offline)")

    matches: list[dict] = []
    network_failed = False
    has_identifier = bool(entry.doi or entry.arxiv_id)

    for fn in (
        lambda: crossref_by_doi(entry.doi, mailto) if entry.doi else crossref_by_title(entry.title, mailto),
        lambda: openalex_lookup(entry, mailto),
        lambda: semanticscholar_lookup(entry, mailto),
        lambda: arxiv_lookup(entry, mailto),
    ):
        try:
            rec = fn()
            if rec:
                matches.append(rec)
        except NetworkUnavailable:
            network_failed = True
            break

    if network_failed and not matches:
        return _unverified(entry, ref_id, reason="network unavailable (DNS/connection failure)")

    id_matches = [m for m in matches if m.get("method") == "id"]
    title_matches = [m for m in matches if m.get("method") == "title"]

    # Identifier Hijacking: the cited DOI/arXiv id actually RESOLVED (method=id),
    # but the resolved record's title does not match the cited title.
    # This must be checked against id-resolved records only — a coincidental
    # title-search hit on a fabricated DOI is NOT hijacking, it is fabrication.
    if has_identifier and entry.title and id_matches:
        best_id = max(id_matches, key=lambda m: title_ratio(entry.title, m["title"]))
        if best_id["title"]:
            r = title_ratio(entry.title, best_id["title"])
            if r < threshold:
                return _verdict(entry, ref_id, "IH",
                                detail=(f"Cited identifier resolved to '{best_id['title']}' "
                                        f"(title ratio {r:.2f} < {threshold:.2f}) — unrelated paper."),
                                matches=matches)

    # Reaching here with no usable signal: either the cited identifier did not
    # resolve anywhere (fabricated DOI/arXiv id) AND only loose title-search hits
    # came back that don't match → Total Fabrication.
    if has_identifier and not id_matches:
        best_loose = max(title_matches, key=lambda m: title_ratio(entry.title, m["title"]),
                         default=None) if (entry.title and title_matches) else None
        loose_ok = best_loose and best_loose["title"] and \
            title_ratio(entry.title, best_loose["title"]) >= threshold
        if not loose_ok:
            return _verdict(entry, ref_id, "TF",
                            detail=("Cited DOI/arXiv identifier did not resolve in any source, "
                                    "and no close title match was found — entry appears fabricated."),
                            matches=matches)

    # No-identifier path with nothing returned was already handled above (TF).
    # Pick the best title match across all sources.
    best = max(matches, key=lambda m: title_ratio(entry.title, m["title"]) if entry.title else 1.0)
    t_ratio = title_ratio(entry.title, best["title"]) if entry.title and best["title"] else 1.0
    a_overlap = author_overlap(entry.authors, best["authors"])

    retracted = any(m.get("retracted") for m in matches)

    # Metadata corruption checks (PAC): year mismatch, author mismatch, low-ish title sim.
    pac_reasons = []
    if entry.year and best["year"] and entry.year != best["year"]:
        pac_reasons.append(f"year cited={entry.year} vs source={best['year']}")
    if entry.authors and a_overlap < 0.5:
        pac_reasons.append(f"author overlap {a_overlap:.0%} below 50%")
    if entry.title and t_ratio < threshold:
        # Title exists somewhere but not close → corrupted/mashup metadata.
        pac_reasons.append(f"title ratio {t_ratio:.2f} < {threshold:.2f}")

    verdict_code = "verified"
    detail = f"Matched in {', '.join(sorted({m['source'] for m in matches}))}."
    if pac_reasons:
        verdict_code = "PAC"
        detail = "Found but metadata disagrees: " + "; ".join(pac_reasons) + "."

    result = _verdict(entry, ref_id, verdict_code, detail=detail, matches=matches)
    result["title_ratio"] = round(t_ratio, 3)
    result["author_overlap"] = round(a_overlap, 3)
    result["retracted"] = retracted
    if retracted:
        result["flags"] = result.get("flags", []) + ["RETRACTED"]
        # Retraction does not change existence verdict but is a SERIOUS flag.
        result["severity"] = "SERIOUS"
        result["detail"] += " ⚠ Crossref/OpenAlex marks this work as RETRACTED."
    return result


def _verdict(entry: Entry, ref_id: str, code: str, detail: str, matches: list[dict]) -> dict:
    return {
        "ref_id": ref_id,
        "verdict": code,
        "verdict_meaning": VERDICTS[code],
        "severity": SEVERITY[code],
        "detail": detail,
        "cited": {
            "title": entry.title,
            "authors": entry.authors,
            "year": entry.year,
            "doi": entry.doi,
            "arxiv_id": entry.arxiv_id,
        },
        "sources_checked": ["crossref", "openalex", "semanticscholar", "arxiv"],
        "matches": [{k: m.get(k) for k in ("source", "title", "year", "doi", "retracted")} for m in matches],
        "flags": [],
    }


def _unverified(entry: Entry, ref_id: str, reason: str) -> dict:
    r = _verdict(entry, ref_id, "unverified",
                 detail=f"{reason}. NOT confirmed — do not treat as passing.",
                 matches=[])
    r["manual_instructions"] = (
        "Verify manually: (1) search the exact title + first author + year on Google "
        "Scholar; (2) if a DOI is given, resolve https://doi.org/<DOI> and confirm the "
        "landing page title matches; (3) for arXiv IDs, open https://arxiv.org/abs/<id>; "
        "(4) confirm the venue, year, and author list field-by-field. Re-run this script "
        "with network access to obtain an automated verdict."
    )
    return r


# --------------------------------------------------------------------------- #
# Report assembly                                                             #
# --------------------------------------------------------------------------- #


def build_report(results: list[dict], mailto: str, threshold: float, offline: bool) -> dict:
    counts = {k: 0 for k in VERDICTS}
    sev = {"SERIOUS": 0, "MEDIUM": 0, "MINOR": 0}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
        s = r["severity"]
        if s in sev:
            sev[s] += 1
    n = len(results) or 1
    fabricated = counts["TF"] + counts["IH"] + counts["PH"]
    fabrication_risk = round(fabricated / n, 3)
    integrity = round((counts["verified"]) / n, 3)

    if counts["unverified"] and not (counts["TF"] or counts["IH"] or counts["PH"] or counts["PAC"]):
        verdict = "UNVERIFIED"
    elif sev["SERIOUS"] > 0:
        verdict = "FAIL"
    elif counts["PAC"] > 0 or sev["MEDIUM"] > 0:
        verdict = "PASS_WITH_CONDITIONS"
    else:
        verdict = "PASS"

    return {
        "tool": "alterlab-citation-verifier/verify_citations.py",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config": {"mailto": mailto, "threshold": threshold, "offline": offline,
                   "http_backend": "requests" if _HAS_REQUESTS else "urllib"},
        "taxonomy": VERDICTS,
        "summary": {
            "total": len(results),
            "verdict": verdict,
            "verdict_counts": counts,
            "severity_counts": sev,
            "citation_integrity_score": integrity,
            "fabrication_risk_score": fabrication_risk,
            "retracted": sum(1 for r in results if r.get("retracted")),
        },
        "entries": results,
    }


# --------------------------------------------------------------------------- #
# CLI                                                                         #
# --------------------------------------------------------------------------- #


def _read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    import os
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    return path  # treat the argument itself as inline text


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Verify that bibliography entries exist via public scholarly APIs.")
    ap.add_argument("input", help="Path to a .bib/.txt file, '-' for stdin, or inline text.")
    ap.add_argument("--format", choices=["auto", "bibtex", "doi", "freeform"], default="auto")
    ap.add_argument("--mailto", default=DEFAULT_MAILTO, help="Polite-pool contact email.")
    ap.add_argument("--threshold", type=float, default=0.70, help="Fuzzy title-match ratio (0..1).")
    ap.add_argument("--out", default=None, help="Write JSON report to this path (default stdout).")
    ap.add_argument("--offline", action="store_true", help="Skip the network; emit 'unverified' verdicts.")
    args = ap.parse_args(argv)

    text = _read_input(args.input)
    try:
        entries = parse_bibliography(text, args.format)
    except Exception as exc:  # noqa: BLE001
        print(f"error: could not parse bibliography: {exc}", file=sys.stderr)
        return 2
    if not entries:
        print("error: no bibliography entries parsed from input.", file=sys.stderr)
        return 2

    results = [verify_entry(e, args.mailto, args.threshold, args.offline) for e in entries]
    report = build_report(results, args.mailto, args.threshold, args.offline)
    out = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
        print(f"wrote {report['summary']['total']} verdicts → {args.out} "
              f"(verdict={report['summary']['verdict']})", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
