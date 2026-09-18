#!/usr/bin/env python3
"""
Metabolomics Workbench query tool.

Query the NIH Metabolomics Workbench REST API: standardize names via RefMet,
fetch study summaries/data, look up compounds, or run m/z searches.
Standard library only.

API base: https://www.metabolomicsworkbench.org/rest
Docs:     https://www.metabolomicsworkbench.org/tools/mw_rest.php
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://www.metabolomicsworkbench.org/rest"
USER_AGENT = "AlterLab-Academic-Skills/1.0 (Metabolomics Workbench query tool)"


def _get(path):
    """GET a pre-built REST path and return parsed JSON (or raw text)."""
    url = f"{BASE_URL}/{path.lstrip('/')}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read().decode("utf-8")
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"raw": body}


def refmet(name):
    """Standardize a metabolite name via RefMet."""
    return _get(f"refmet/match/{urllib.parse.quote(name)}/name/json")


def study(study_id, output="summary"):
    """Study metadata (summary) or data for a study ID, e.g. ST000001."""
    return _get(f"study/study_id/{study_id}/{output}/json")


def compound(regno):
    """Compound record by Metabolomics Workbench registry number."""
    return _get(f"compound/regno/{regno}/all/json")


def moverz(mz, adduct="M+H", tolerance=0.5, database="MB"):
    """m/z search across a database with an ion adduct and tolerance."""
    return _get(f"moverz/{database}/{mz}/{urllib.parse.quote(adduct)}/{tolerance}/json")


def main():
    parser = argparse.ArgumentParser(description="Query the NIH Metabolomics Workbench REST API")
    sub = parser.add_subparsers(dest="command", required=True)

    p_r = sub.add_parser("refmet", help="Standardize a metabolite name via RefMet")
    p_r.add_argument("name", help="Metabolite name, e.g. citrate")

    p_s = sub.add_parser("study", help="Study summary or data by ID")
    p_s.add_argument("study_id", help="Study ID, e.g. ST000001")
    p_s.add_argument("--output", default="summary", help="summary | data | factors")

    p_c = sub.add_parser("compound", help="Compound record by registry number")
    p_c.add_argument("regno", help="Registry number, e.g. 11")

    p_m = sub.add_parser("moverz", help="m/z search")
    p_m.add_argument("mz", help="m/z value, e.g. 635.52")
    p_m.add_argument("--adduct", default="M+H", help="Ion adduct (default M+H)")
    p_m.add_argument("--tolerance", default=0.5, help="Mass tolerance in Da")
    p_m.add_argument("--database", default="MB", help="MB | LIPIDS | REFMET")

    args = parser.parse_args()
    try:
        if args.command == "refmet":
            result = refmet(args.name)
        elif args.command == "study":
            result = study(args.study_id, args.output)
        elif args.command == "compound":
            result = compound(args.regno)
        elif args.command == "moverz":
            result = moverz(args.mz, args.adduct, args.tolerance, args.database)
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
