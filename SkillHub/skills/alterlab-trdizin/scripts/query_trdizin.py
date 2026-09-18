#!/usr/bin/env python3
"""query_trdizin.py — Search TR Dizin (TÜBİTAK ULAKBİM national citation index).

Wraps the confirmed, unauthenticated TR Dizin search API at
``https://search.trdizin.gov.tr/api/defaultSearch/{type}/`` where ``type`` is one
of ``publication | journal | author | institution``. The API returns a raw
Elasticsearch response (``hits.hits[]._source`` + faceted ``aggregations``); this
script parses ``_source`` into clean records and surfaces the aggregations as
facets.

Verified live (HTTP 200, real Elasticsearch JSON) on 2026-06-06 via curl.

Design constraints (mirror skills/core/alterlab-citation-verifier):
- NO API key. NO required third-party deps: uses ``requests`` if importable, else
  falls back to the stdlib (``urllib``). A polite User-Agent carries a mailto.
- The server returns ~10 hits per page and IGNORES a client ``limit`` param, so
  paging is done with ``page`` and ``--limit`` is applied client-side by walking
  pages and slicing. This is an observed server behaviour, not a guess.
- Network failure is reported, never silently swallowed into an empty success.

Usage:
  uv run python query_trdizin.py publication "machine learning" [--order ORDER]
                                 [--limit N] [--mailto you@example.com]
                                 [--facets] [--json] [--out report.json]
  uv run python query_trdizin.py journal "Bilig" --json

Valid --order (verified against the SPA): relevance-DESC (default),
publicationYear-ASC, publicationYear-DESC, title-ASC, title-DESC,
orderCitationCount-ASC, orderCitationCount-DESC.

Exit codes: 0 = ran; 2 = bad usage; 3 = network unavailable.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from typing import Any

API_BASE = "https://search.trdizin.gov.tr/api/defaultSearch"
TYPES = ("publication", "journal", "author", "institution")
ORDERS = (
    "relevance-DESC",
    "publicationYear-ASC",
    "publicationYear-DESC",
    "title-ASC",
    "title-DESC",
    "orderCitationCount-ASC",
    "orderCitationCount-DESC",
)
PAGE_SIZE = 10  # server-side page size; the server ignores a client limit param
DEFAULT_MAILTO = "alterlab.ieu@gmail.com"
USER_AGENT = (
    "alterlab-trdizin/1.0.1 (https://github.com/AlterLab-IEU/"
    "AlterLab-Academic-Skills; mailto:{mailto})"
)
HTTP_TIMEOUT = 25


class NetworkUnavailable(RuntimeError):
    """Raised when the TR Dizin API cannot be reached."""


def _http_get(url: str, mailto: str) -> dict[str, Any]:
    headers = {"User-Agent": USER_AGENT.format(mailto=mailto), "Accept": "application/json"}
    try:
        import requests  # type: ignore

        resp = requests.get(url, headers=headers, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except ImportError:
        pass
    except Exception as exc:  # requests present but call failed
        raise NetworkUnavailable(str(exc)) from exc

    import urllib.error
    import urllib.request

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as fh:
            return json.loads(fh.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError) as exc:
        raise NetworkUnavailable(str(exc)) from exc


def _build_url(rtype: str, q: str, order: str, page: int) -> str:
    params = urllib.parse.urlencode({"q": q, "order": order, "page": page})
    return f"{API_BASE}/{rtype}/?{params}"


def _total(raw: dict[str, Any]) -> int:
    total = raw.get("hits", {}).get("total")
    if isinstance(total, dict):
        return int(total.get("value", 0))
    if isinstance(total, int):
        return total
    return 0


def search(rtype: str, q: str, order: str, limit: int, mailto: str) -> dict[str, Any]:
    """Walk pages until ``limit`` records are collected (or results run out)."""
    if rtype not in TYPES:
        raise ValueError(f"type must be one of {TYPES}, got {rtype!r}")
    if order not in ORDERS:
        raise ValueError(f"order must be one of {ORDERS}, got {order!r}")

    collected: list[dict[str, Any]] = []
    total = 0
    aggregations: dict[str, Any] = {}
    page = 1
    while len(collected) < limit:
        raw = _http_get(_build_url(rtype, q, order, page), mailto)
        if page == 1:
            total = _total(raw)
            aggregations = raw.get("aggregations", {}) or {}
        hits = raw.get("hits", {}).get("hits", []) or []
        if not hits:
            break
        for hit in hits:
            collected.append(hit.get("_source", {}))
        if len(hits) < PAGE_SIZE:  # last page
            break
        page += 1

    records = [_clean(rtype, src) for src in collected[:limit]]
    return {
        "tool": "alterlab-trdizin/query_trdizin.py",
        "type": rtype,
        "query": q,
        "order": order,
        "total": total,
        "returned": len(records),
        "records": records,
        "facets": _facets(aggregations),
    }


def _clean(rtype: str, s: dict[str, Any]) -> dict[str, Any]:
    if rtype == "publication":
        return {
            "id": s.get("id"),
            "title": s.get("orderTitle") or _title(s),
            "authors": [a.get("inPublicationName") for a in s.get("authors", []) if isinstance(a, dict)],
            "journal": (s.get("journal") or {}).get("name"),
            "issn": (s.get("journal") or {}).get("issn"),
            "year": s.get("publicationYear"),
            "doi": s.get("doi") or None,
            "accessType": s.get("accessType"),
            "pdf": s.get("pdf"),
            "docType": s.get("docType"),
            "citationCount": s.get("orderCitationCount"),
        }
    if rtype == "journal":
        return journal_status(s)
    if rtype == "author":
        # Live API: author _source has name=null/title=null; the populated
        # name lives in fullName / orderTitle (firstName + lastName).
        return {
            "id": s.get("id"),
            "name": s.get("fullName") or s.get("orderTitle") or s.get("name") or _title(s),
            "orcid": s.get("orcid") or None,
            "hindex": s.get("hindex"),
            "publicationCount": s.get("orderPublicationCount"),
            "citationCount": s.get("orderCitationCount"),
        }
    # institution
    return {"id": s.get("id"), "name": s.get("name") or _title(s)}


def _title(s: dict[str, Any]) -> Any:
    t = s.get("title")
    if isinstance(t, list):
        return t[0] if t else None
    return t


def journal_status(s: dict[str, Any]) -> dict[str, Any]:
    """Derive a TR Dizin indexing verdict from a journal ``_source`` record.

    Status signals (verified field names on the live API):
      isActive      bool   — record flag; NOT reliable on its own (see below)
      journalYear[] list   — per-year index entries; each has .year and .databases
      lastYearList         — last indexed year(s) (often null while active)
      rejectYearList       — [{id, year}] for years the journal was rejected
                             (null if never rejected)

    CRITICAL — isActive is not trustworthy alone. A journal can keep
    isActive=true while its coverage stopped years ago and recent years sit in
    rejectYearList. Verified live: "Eğitim Bilim Toplum" (ISSN 1303-9202) is
    isActive=true with journalYear coverage ending 2019 and rejectYearList
    2020–2025 — it is NOT currently indexed. So we evaluate rejectYearList vs
    the latest coverage year BEFORE declaring "currently indexed": if the most
    recent reject year is newer than the last covered year, the journal is no
    longer indexed regardless of isActive.

    NOTE: firstIndexDate / indexDate on this endpoint are populated at query time
    (they equal "today"), so they are NOT a reliable index-history signal and are
    deliberately excluded from the verdict. journalYear is the authoritative
    coverage signal.
    """
    years = sorted(
        {int(y["year"]) for y in s.get("journalYear", []) if isinstance(y, dict) and y.get("year")},
        reverse=True,
    )
    reject = s.get("rejectYearList")
    is_active = bool(s.get("isActive"))
    databases = sorted({db for y in s.get("journalYear", []) if isinstance(y, dict) for db in (y.get("databases") or [])})

    # rejectYearList entries are {id, year} dicts on the live API; collect the
    # rejected years so we can compare them against the coverage window.
    reject_years = sorted(
        {int(r["year"]) for r in reject if isinstance(r, dict) and r.get("year")}
        if isinstance(reject, list)
        else set()
    )
    latest_year = years[0] if years else None
    latest_reject = reject_years[-1] if reject_years else None

    # CRITICAL: isActive alone is unreliable. A journal can carry isActive=true
    # while coverage stopped years ago and recent years are in rejectYearList
    # (e.g. "Eğitim Bilim Toplum", ISSN 1303-9202: active, coverage→2019,
    # rejected 2020–2025). Reject years more recent than the last coverage year
    # mean it is NO LONGER indexed — never report "currently indexed" then.
    rejected_after_coverage = latest_reject is not None and (
        latest_year is None or latest_reject > latest_year
    )

    if rejected_after_coverage:
        cov = f"coverage ended {latest_year}; " if latest_year else ""
        verdict = (
            f"No longer indexed in TR Dizin — rejected after coverage "
            f"({cov}rejected years {reject_years})"
        )
    elif is_active and years:
        verdict = f"Currently indexed in TR Dizin (active; coverage years {years[-1]}–{years[0]})"
    elif reject_years:
        verdict = f"Rejected / not indexed (rejected years {reject_years})"
    elif not is_active:
        verdict = "Not currently active in TR Dizin"
    else:
        verdict = "Status indeterminate from record — inspect raw fields"

    return {
        "id": s.get("id"),
        "title": _title(s),
        "issn": s.get("issn") or None,
        "eissn": s.get("eissn") or None,
        "isActive": is_active,
        "coverageYears": years,
        "lastYearList": s.get("lastYearList"),
        "rejectYearList": reject,
        "databases": databases,
        "webAddress": s.get("webAddress"),
        "verdict": verdict,
    }


def _facets(aggs: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, agg in aggs.items():
        if not isinstance(agg, dict):
            continue
        buckets = agg.get("buckets")
        if isinstance(buckets, list):
            out[name] = [{"key": b.get("key"), "count": b.get("doc_count")} for b in buckets[:25]]
    return out


def _render(report: dict[str, Any]) -> str:
    lines = [
        f"TR Dizin · {report['type']} · q={report['query']!r} · order={report['order']}",
        f"total matches: {report['total']} · showing {report['returned']}",
        "",
    ]
    for r in report["records"]:
        if report["type"] == "journal":
            lines.append(f"- {r['title']}  [ISSN {r['issn'] or '-'} / eISSN {r['eissn'] or '-'}]")
            lines.append(f"    {r['verdict']}")
        elif report["type"] == "publication":
            doi = f" doi:{r['doi']}" if r["doi"] else ""
            lines.append(f"- ({r['year']}) {r['title']} — {r['journal']}{doi} [{r['accessType']}]")
        else:
            lines.append(f"- {r['name']} (id {r['id']})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Search TR Dizin (TÜBİTAK ULAKBİM national index).")
    p.add_argument("type", choices=TYPES)
    p.add_argument("query")
    p.add_argument("--order", default="relevance-DESC", choices=ORDERS)
    p.add_argument("--limit", type=int, default=10, help="max records to collect (paged client-side)")
    p.add_argument("--mailto", default=DEFAULT_MAILTO)
    p.add_argument("--facets", action="store_true", help="print faceted aggregations too")
    p.add_argument("--json", action="store_true", help="emit raw JSON report")
    p.add_argument("--out", help="write JSON report to this path")
    args = p.parse_args(argv)

    if args.limit < 1:
        print("--limit must be >= 1", file=sys.stderr)
        return 2

    try:
        report = search(args.type, args.query, args.order, args.limit, args.mailto)
    except NetworkUnavailable as exc:
        print(f"NETWORK UNAVAILABLE: could not reach TR Dizin API ({exc}).", file=sys.stderr)
        print("Retry with connectivity; the API needs no key.", file=sys.stderr)
        return 3
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not args.facets:
        report = {k: v for k, v in report.items() if k != "facets"}

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
        print(f"wrote {args.out}")
    elif args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(_render(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
