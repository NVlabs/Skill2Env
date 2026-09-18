#!/usr/bin/env python3
"""
RCSB PDB query tool.

Access the RCSB Protein Data Bank via its public REST APIs: full-text search
(Search API), entry metadata (Data API), and coordinate file download. Uses
only the Python standard library (no rcsb-api package required).

Search API: https://search.rcsb.org/rcsbsearch/v2/query
Data API:   https://data.rcsb.org/rest/v1/core/entry/{id}
Files:      https://files.rcsb.org/download/{id}.{fmt}
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
DATA_URL = "https://data.rcsb.org/rest/v1/core/entry"
FILES_URL = "https://files.rcsb.org/download"
USER_AGENT = "AlterLab-Academic-Skills/1.0 (RCSB PDB query tool)"


def _get_json(url):
    req = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search(text, rows=25):
    """Full-text search for PDB entries; returns matching identifiers."""
    payload = {
        "query": {
            "type": "terminal",
            "service": "full_text",
            "parameters": {"value": text},
        },
        "return_type": "entry",
        "request_options": {"paginate": {"start": 0, "rows": rows}},
    }
    url = f"{SEARCH_URL}?json={urllib.parse.quote(json.dumps(payload))}"
    return _get_json(url)


def entry(pdb_id):
    """Entry-level metadata for a PDB ID, e.g. 4HHB."""
    return _get_json(f"{DATA_URL}/{pdb_id.upper()}")


def download(pdb_id, fmt="cif", output=None):
    """Download a coordinate file (cif or pdb)."""
    pdb_id = pdb_id.upper()
    url = f"{FILES_URL}/{pdb_id}.{fmt}"
    out_path = output or f"{pdb_id}.{fmt}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    with open(out_path, "wb") as handle:
        handle.write(data)
    return {"pdb_id": pdb_id, "format": fmt, "bytes": len(data), "path": out_path}


def main():
    parser = argparse.ArgumentParser(description="Query the RCSB Protein Data Bank REST APIs")
    sub = parser.add_subparsers(dest="command", required=True)

    p_s = sub.add_parser("search", help="Full-text search for entries")
    p_s.add_argument("text", help="Search text, e.g. hemoglobin")
    p_s.add_argument("--rows", type=int, default=25, help="Max results")

    p_e = sub.add_parser("entry", help="Entry metadata by PDB ID")
    p_e.add_argument("pdb_id", help="4-character PDB ID, e.g. 4HHB")

    p_d = sub.add_parser("download", help="Download a coordinate file")
    p_d.add_argument("pdb_id", help="4-character PDB ID, e.g. 4HHB")
    p_d.add_argument("--format", default="cif", choices=["cif", "pdb"], help="File format")
    p_d.add_argument("--output", help="Output path (default <ID>.<fmt>)")

    args = parser.parse_args()
    try:
        if args.command == "search":
            result = search(args.text, args.rows)
        elif args.command == "entry":
            result = entry(args.pdb_id)
        elif args.command == "download":
            result = download(args.pdb_id, args.format, args.output)
    except urllib.error.HTTPError as exc:
        print(f"HTTP error {exc.code}: {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Connection error: {exc.reason}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
