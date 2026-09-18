#!/usr/bin/env python3
"""Confirm a bioRxiv/medRxiv preprint DOI and surface any published-article link.

Queries the keyless bioRxiv/medRxiv content API (api.biorxiv.org) to (1) confirm
a preprint DOI resolves and report its versions, and (2) check the `/pubs/`
preprint-to-publication mapping so a posted preprint can be linked to its version
of record. No API key is required.

Endpoints (verified on api.biorxiv.org):
  /details/{server}/{doi}/na/json   -> manuscript details + versions
  /pubs/{server}/{interval}/{cursor} -> preprint->published-article mappings

`server` is `biorxiv` or `medrxiv`. Degrades gracefully offline.

Auto-selects an HTTP backend: uses `requests` if installed, else stdlib urllib.

    uv run python scripts/preprint_link_check.py --server biorxiv --doi 10.1101/2020.01.01.000000
    uv run python scripts/preprint_link_check.py --server medrxiv --doi 10.1101/2021.05.05.21256000
"""
from __future__ import annotations

import argparse
import json
import sys

API_BASE = "https://api.biorxiv.org"
USER_AGENT = "alterlab-preprint-deposition/1.0 (+https://github.com/AlterLab-IEU)"


class NetworkUnavailable(RuntimeError):
    pass


def _fetch(url: str, timeout: float) -> dict:
    try:
        try:
            import requests  # type: ignore

            resp = requests.get(url, timeout=timeout,
                                headers={"User-Agent": USER_AGENT})
            resp.raise_for_status()
            return resp.json()
        except ImportError:
            import urllib.request

            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310
                return json.loads(r.read().decode("utf-8", errors="replace"))
    except Exception as exc:  # noqa: BLE001
        raise NetworkUnavailable(str(exc)) from exc


def check(server: str, doi: str, timeout: float) -> dict:
    server = server.lower()
    if server not in ("biorxiv", "medrxiv"):
        return {"status": "error",
                "reason": "server must be 'biorxiv' or 'medrxiv'"}

    details_url = f"{API_BASE}/details/{server}/{doi}/na/json"
    pubs_url = f"{API_BASE}/pubs/{server}/{doi}/na/json"

    out = {
        "tool": "alterlab-preprint-deposition/preprint_link_check.py",
        "version": "1.0.0",
        "server": server,
        "doi": doi,
    }

    try:
        details = _fetch(details_url, timeout)
    except NetworkUnavailable as exc:
        out.update(status="unverified",
                   manual_instructions=(
                       f"Could not reach api.biorxiv.org ({exc}). Confirm the "
                       f"DOI manually at https://doi.org/{doi}."))
        return out

    collection = details.get("collection") or []
    if not collection:
        out.update(status="not_found",
                   detail=details.get("messages"),
                   manual_instructions=(
                       "No record matched this DOI on the content API; check "
                       "the DOI and server."))
        return out

    versions = sorted({str(c.get("version")) for c in collection
                       if c.get("version") is not None})
    latest = collection[-1]
    out.update(
        status="found",
        title=latest.get("title"),
        versions=versions,
        latest_version=latest.get("version"),
        posted_date=latest.get("date"),
        category=latest.get("category"),
    )

    # Published-article link (best-effort; absence != not published).
    try:
        pubs = _fetch(pubs_url, timeout)
        pub_coll = pubs.get("collection") or []
        if pub_coll:
            link = pub_coll[0]
            out["published_link"] = {
                "published_doi": link.get("published_doi"),
                "published_journal": link.get("published_journal"),
                "published_date": link.get("published_date"),
            }
        else:
            out["published_link"] = None
            out["published_link_note"] = (
                "No preprint->published link detected yet; this does not mean "
                "the paper is unpublished. Add the link manually on publication.")
    except NetworkUnavailable:
        out["published_link"] = None
        out["published_link_note"] = "pubs endpoint unreachable this run."

    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--server", required=True, choices=["biorxiv", "medrxiv"])
    p.add_argument("--doi", required=True, help="Preprint DOI, e.g. 10.1101/...")
    p.add_argument("--timeout", type=float, default=20.0)
    args = p.parse_args(argv)

    report = check(args.server, args.doi, args.timeout)
    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
