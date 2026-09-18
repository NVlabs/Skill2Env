#!/usr/bin/env python3
"""Query the ENA (European Nucleotide Archive) Portal API (no API key required).

Base: https://www.ebi.ac.uk/ena/portal/api
  GET /search       result, query (ENA query syntax), fields, format, limit
  GET /filereport   accession, result=read_run -> FASTQ FTP URLs + md5

Query syntax: tax_eq(9606), tax_tree(562), study_accession="PRJNA123456", AND/OR.

Smoke test:
    uv run python query_ena.py search --result read_run \\
        --query 'study_accession="PRJEB1787"' \\
        --fields run_accession,fastq_ftp --limit 5
    uv run python query_ena.py filereport ERR164407
"""
import argparse
import json

import requests

BASE = "https://www.ebi.ac.uk/ena/portal/api"


def search(result: str, query: str, fields: str | None = None,
           fmt: str = "json", limit: int = 100) -> object:
    """Advanced search across an ENA result type. Returns parsed JSON or raw text."""
    params = {"result": result, "query": query, "format": fmt, "limit": limit}
    if fields:
        params["fields"] = fields
    r = requests.get(f"{BASE}/search", params=params, timeout=120)
    r.raise_for_status()
    return r.json() if fmt == "json" else r.text


def filereport(accession: str, result: str = "read_run",
               fields: str = "run_accession,fastq_ftp,fastq_md5,fastq_bytes") -> list:
    """Get file (FASTQ) URLs and checksums for a run or analysis accession."""
    params = {"accession": accession, "result": result, "format": "json", "fields": fields}
    r = requests.get(f"{BASE}/filereport", params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def main() -> None:
    p = argparse.ArgumentParser(description="Query ENA Portal API (no key required).")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("search")
    ps.add_argument("--result", required=True, help="e.g. sample, study, read_run, assembly")
    ps.add_argument("--query", required=True, help="ENA query, e.g. tax_eq(9606)")
    ps.add_argument("--fields", default=None)
    ps.add_argument("--format", dest="fmt", default="json", choices=["json", "tsv", "xml"])
    ps.add_argument("--limit", type=int, default=100)

    pf = sub.add_parser("filereport")
    pf.add_argument("accession")
    pf.add_argument("--result", default="read_run", choices=["read_run", "analysis"])
    pf.add_argument("--fields", default="run_accession,fastq_ftp,fastq_md5,fastq_bytes")

    args = p.parse_args()
    if args.cmd == "search":
        out = search(args.result, args.query, args.fields, args.fmt, args.limit)
        print(json.dumps(out, indent=2) if args.fmt == "json" else out)
    else:
        print(json.dumps(filereport(args.accession, args.result, args.fields), indent=2))


if __name__ == "__main__":
    main()
