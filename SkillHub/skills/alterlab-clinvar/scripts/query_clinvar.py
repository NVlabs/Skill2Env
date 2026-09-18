#!/usr/bin/env python3
"""Query ClinVar via NCBI E-utilities (no API key required; key raises rate limit).

Base: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/  (db=clinvar)
  esearch.fcgi   term -> ClinVar UIDs
  esummary.fcgi  id   -> record summaries (version 2.0 JSON)

Search field tags (verified via einfo; unknown tags silently fall back to
[All Fields] and stop filtering — check 'querytranslation' in the response):
    BRCA1[gene]
    clinsig_pathogenic[Properties]            (also clinsig_likely_pathogenic, clinsig_benign, clinsig_has_conflicts)
    "reviewed by expert panel"[Review status]
    "breast cancer"[Disease/Phenotype]

Smoke test:
    uv run python query_clinvar.py search "BRCA1[gene] AND clinsig_pathogenic[Properties]" --retmax 5
    uv run python query_clinvar.py summary 12345,12346
"""
import argparse
import json
import os

import requests

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
API_KEY = os.environ.get("NCBI_API_KEY")


def _params(extra: dict) -> dict:
    p = {"db": "clinvar", "retmode": "json", **extra}
    if API_KEY:
        p["api_key"] = API_KEY
    return p


def search(term: str, retmax: int = 20) -> dict:
    """Search ClinVar; return the esearch result (Count + IdList)."""
    r = requests.get(f"{BASE}/esearch.fcgi",
                     params=_params({"term": term, "retmax": retmax}), timeout=30)
    r.raise_for_status()
    return r.json().get("esearchresult", {})


def summary(uids: str) -> dict:
    """Fetch ClinVar record summaries for comma-separated UIDs."""
    r = requests.get(f"{BASE}/esummary.fcgi",
                     params=_params({"id": uids, "version": "2.0"}), timeout=30)
    r.raise_for_status()
    return r.json().get("result", {})


def main() -> None:
    p = argparse.ArgumentParser(description="Query ClinVar via NCBI E-utilities.")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("search")
    ps.add_argument("term")
    ps.add_argument("--retmax", type=int, default=20)

    pm = sub.add_parser("summary")
    pm.add_argument("uids", help="comma-separated ClinVar UIDs")

    args = p.parse_args()
    out = search(args.term, args.retmax) if args.cmd == "search" else summary(args.uids)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
