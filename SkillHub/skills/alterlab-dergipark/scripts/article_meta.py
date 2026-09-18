#!/usr/bin/env python3
"""article_meta.py — Scrape a DergiPark article page and emit BibTeX / RIS locally.

DergiPark article HTML pages are open (no human-verification gate) and expose
Highwire/Google-Scholar ``citation_*`` and ``DC.*`` meta tags. This fetches one
article page, parses those tags into a clean dict, and formats BibTeX or RIS
LOCALLY from the parsed fields — it does NOT depend on any on-site Cite/export
backend (whose URL is unverified).

Verified live (2026-06-06) on /en/pub/mulkiye/article/10:
  citation_title, citation_author (repeated), citation_journal_title,
  citation_issn, citation_publication_date, citation_volume, citation_issue,
  citation_firstpage, citation_lastpage, citation_abstract, citation_language,
  citation_pdf_url, DC.Title, DC.Source, DC.Identifier, DC.Language
  citation_pdf_url is a RELATIVE path of the form /{lang}/download/article-file/{file-id}.
  NOTE: that file-id differs from the article id in the page URL — always take the
  PDF link from citation_pdf_url, never construct it from the article id.

stats_trdizin_citation_count: documented as an in-page signal of TR Dizin
coverage, but NOT present on every article and not observed in this script's
probes — treat it as advisory only and cross-check TR Dizin itself for indexing.

Usage:
  uv run python article_meta.py URL_OR_SLASH_PATH [--format json|bibtex|ris]
  uv run python article_meta.py https://dergipark.org.tr/en/pub/mulkiye/article/10 --format bibtex
  uv run python article_meta.py /en/pub/mulkiye/article/10 --format ris

Design: NO API key. Prefers ``requests`` if installed, else stdlib ``urllib``.
Meta-tag parsing via ``html.parser`` (stdlib). Exit 0 = ran; 1 = fetch error; 2 = usage.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from html.parser import HTMLParser
from typing import Any, Optional

SITE_ROOT = "https://dergipark.org.tr"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "alterlab-dergipark/1.0.0 (+https://github.com/AlterLab-IEU/AlterLab-Academic-Skills)"
)
HTTP_TIMEOUT = 30
RETRIES = 2
BACKOFF = 1.5

try:  # pragma: no cover
    import requests as _requests  # type: ignore

    _HAS_REQUESTS = True
except Exception:  # pragma: no cover
    _requests = None
    _HAS_REQUESTS = False

import urllib.error
import urllib.parse
import urllib.request


class NetworkUnavailable(Exception):
    pass


def _http_get_text(url: str) -> str:
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html"}
    last_exc: Optional[Exception] = None
    for attempt in range(RETRIES + 1):
        try:
            if _HAS_REQUESTS:
                resp = _requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
                if resp.status_code == 200:
                    return resp.text
                last_exc = RuntimeError(f"HTTP {resp.status_code}")
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                    return r.read().decode("utf-8", "replace")
        except (urllib.error.URLError, OSError) as e:
            last_exc = NetworkUnavailable(str(e))
        except Exception as e:  # pragma: no cover
            last_exc = e
        if attempt < RETRIES:
            time.sleep(BACKOFF * (attempt + 1))
    if isinstance(last_exc, NetworkUnavailable):
        raise last_exc
    raise RuntimeError(str(last_exc) if last_exc else "unknown error")


class _MetaParser(HTMLParser):
    """Collect <meta name=... content=...> pairs; allow repeated names (authors)."""

    def __init__(self) -> None:
        super().__init__()
        self.metas: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag != "meta":
            return
        d = {k.lower(): (v or "") for k, v in attrs}
        name = d.get("name") or d.get("property")
        content = d.get("content")
        if name and content is not None:
            self.metas.append((name, content))


def parse_article(html: str) -> dict[str, Any]:
    """Parse citation_* / DC.* meta tags into a structured record."""
    p = _MetaParser()
    p.feed(html)
    single: dict[str, str] = {}
    authors: list[str] = []
    trdizin_count: Optional[str] = None
    for name, content in p.metas:
        if name == "citation_author":
            authors.append(content.strip())
        elif name == "stats_trdizin_citation_count":
            trdizin_count = content.strip()
        else:
            single.setdefault(name, content.strip())

    def g(*keys: str) -> str:
        for k in keys:
            if single.get(k):
                return single[k]
        return ""

    pdf_rel = g("citation_pdf_url")
    pdf_url = urllib.parse.urljoin(SITE_ROOT, pdf_rel) if pdf_rel else ""

    return {
        "title": g("citation_title", "DC.Title"),
        "authors": authors,
        "journal": g("citation_journal_title", "DC.Source"),
        "issn": g("citation_issn"),
        "publisher": g("citation_publisher"),
        "date": g("citation_publication_date", "citation_date"),
        "volume": g("citation_volume"),
        "issue": g("citation_issue"),
        "firstpage": g("citation_firstpage"),
        "lastpage": g("citation_lastpage"),
        "language": g("citation_language", "DC.Language"),
        "abstract": g("citation_abstract"),
        "doi": g("citation_doi"),
        "html_url": g("citation_abstract_html_url", "citation_fulltext_html_url"),
        "pdf_url": pdf_url,
        "stats_trdizin_citation_count": trdizin_count,  # advisory; may be None
    }


def _year(date: str) -> str:
    m = re.search(r"(\d{4})", date or "")
    return m.group(1) if m else ""


def _cite_key(rec: dict[str, Any]) -> str:
    first_author = (rec["authors"][0].split(",")[0] if rec["authors"] else "anon")
    surname = re.sub(r"[^A-Za-z]", "", first_author) or "anon"
    return f"{surname.lower()}{_year(rec['date'])}"


def to_bibtex(rec: dict[str, Any]) -> str:
    pages = ""
    if rec["firstpage"]:
        pages = rec["firstpage"] + (f"--{rec['lastpage']}" if rec["lastpage"] else "")
    authors = " and ".join(rec["authors"])
    fields = [
        ("author", authors),
        ("title", rec["title"]),
        ("journal", rec["journal"]),
        ("year", _year(rec["date"])),
        ("volume", rec["volume"]),
        ("number", rec["issue"]),
        ("pages", pages),
        ("issn", rec["issn"]),
        ("doi", rec["doi"]),
        ("url", rec["html_url"]),
        ("publisher", rec["publisher"]),
    ]
    body = "".join(f"  {k} = {{{v}}},\n" for k, v in fields if v)
    return f"@article{{{_cite_key(rec)},\n{body}}}\n"


def to_ris(rec: dict[str, Any]) -> str:
    lines = ["TY  - JOUR"]
    for a in rec["authors"]:
        lines.append(f"AU  - {a}")
    if rec["title"]:
        lines.append(f"TI  - {rec['title']}")
    if rec["journal"]:
        lines.append(f"JO  - {rec['journal']}")
    if _year(rec["date"]):
        lines.append(f"PY  - {_year(rec['date'])}")
    if rec["volume"]:
        lines.append(f"VL  - {rec['volume']}")
    if rec["issue"]:
        lines.append(f"IS  - {rec['issue']}")
    if rec["firstpage"]:
        lines.append(f"SP  - {rec['firstpage']}")
    if rec["lastpage"]:
        lines.append(f"EP  - {rec['lastpage']}")
    if rec["issn"]:
        lines.append(f"SN  - {rec['issn']}")
    if rec["doi"]:
        lines.append(f"DO  - {rec['doi']}")
    if rec["html_url"]:
        lines.append(f"UR  - {rec['html_url']}")
    if rec["abstract"]:
        lines.append(f"AB  - {rec['abstract']}")
    lines.append("ER  - ")
    return "\n".join(lines) + "\n"


def fetch_article(url_or_path: str) -> dict[str, Any]:
    url = url_or_path if url_or_path.startswith("http") else urllib.parse.urljoin(SITE_ROOT, url_or_path)
    rec = parse_article(_http_get_text(url))
    rec["source_url"] = url
    return rec


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("url", help="full article URL or /en/pub/{slug}/article/{id} path")
    p.add_argument("--format", default="json", choices=["json", "bibtex", "ris"])
    args = p.parse_args(argv)

    try:
        rec = fetch_article(args.url)
    except NetworkUnavailable as e:
        print(json.dumps({"error": "network_unavailable", "detail": str(e)}), file=sys.stderr)
        return 1
    except Exception as e:
        print(json.dumps({"error": "fetch_error", "detail": str(e)}), file=sys.stderr)
        return 1

    if not rec.get("title"):
        print(json.dumps({"error": "no_meta_tags", "detail": "no citation_*/DC.* tags found; page may be gated or moved"}), file=sys.stderr)
        return 1

    if args.format == "bibtex":
        sys.stdout.write(to_bibtex(rec))
    elif args.format == "ris":
        sys.stdout.write(to_ris(rec))
    else:
        print(json.dumps(rec, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
