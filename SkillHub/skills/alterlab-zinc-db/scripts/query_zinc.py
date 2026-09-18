#!/usr/bin/env python3
"""
ZINC22 query tool.

Query the ZINC22 CartBlanche API for purchasable compounds. CartBlanche accepts
form-encoded POST submissions and dispatches every search (ID lookup, SMILES,
random sample) asynchronously: each call returns a JSON task handle
({"task": "<uuid>"}). The result rows are assembled server-side and shown in the
web UI at https://cartblanche22.docking.org (the task-retrieval route serves the
single-page app, so there is no plain-text polling endpoint to scrape).
Standard library only.

API base: https://cartblanche22.docking.org
Docs:     https://wiki.docking.org/index.php/Zinc22:Searching
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://cartblanche22.docking.org"
USER_AGENT = "AlterLab-Academic-Skills/1.0 (ZINC22 query tool)"


def _post(path, fields):
    """POST form-encoded fields to a CartBlanche endpoint; return raw text."""
    data = urllib.parse.urlencode(fields).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/{path.lstrip('/')}",
        data=data,
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read().decode("utf-8")


def _parse(text):
    """Return JSON if the body is JSON (async task), else parse TSV rows."""
    stripped = text.strip()
    if stripped.startswith("{") or stripped.startswith("["):
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return []
    header = lines[0].split("\t")
    return [dict(zip(header, ln.split("\t"))) for ln in lines[1:]]


def by_id(zinc_ids, output_fields="zinc_id,smiles,catalogs"):
    """Submit a ZINC-ID lookup; returns a JSON task handle.

    The form field is ``zinc_ids`` (plural); the singular ``zinc_id`` is
    rejected with HTTP 400.
    """
    return _parse(_post("substances.txt", {
        "zinc_ids": ",".join(zinc_ids),
        "output_fields": output_fields,
    }))


def by_smiles(smiles, dist=0, output_fields="zinc_id,smiles,tranche"):
    """Submit a SMILES (similarity) search; returns a JSON task handle."""
    return _parse(_post("smiles.txt", {
        "smiles": smiles,
        "dist": dist,
        "output_fields": output_fields,
    }))


def random(count=100, subset=None, output_fields="zinc_id,smiles,tranche"):
    """Submit a random-sample request; returns a JSON task handle."""
    fields = {"count": count, "output_fields": output_fields}
    if subset:
        fields["subset"] = subset
    return _parse(_post("substance/random.txt", fields))


def main():
    parser = argparse.ArgumentParser(description="Query the ZINC22 CartBlanche API")
    sub = parser.add_subparsers(dest="command", required=True)

    p_i = sub.add_parser("id", help="Look up ZINC IDs (async task handle)")
    p_i.add_argument("zinc_ids", nargs="+", help="One or more ZINC IDs")
    p_i.add_argument("--fields", default="zinc_id,smiles,catalogs", help="Output fields")

    p_s = sub.add_parser("smiles", help="Search by SMILES (async task handle)")
    p_s.add_argument("smiles", help="Query SMILES, e.g. c1ccccc1")
    p_s.add_argument("--dist", type=int, default=0, help="Tanimoto distance (0 = exact)")
    p_s.add_argument("--fields", default="zinc_id,smiles,tranche", help="Output fields")

    p_r = sub.add_parser("random", help="Random compound sample (async task handle)")
    p_r.add_argument("--count", type=int, default=100, help="Number of compounds")
    p_r.add_argument("--subset", help="lead-like | drug-like | fragment")
    p_r.add_argument("--fields", default="zinc_id,smiles,tranche", help="Output fields")

    args = parser.parse_args()
    try:
        if args.command == "id":
            result = by_id(args.zinc_ids, args.fields)
        elif args.command == "smiles":
            result = by_smiles(args.smiles, args.dist, args.fields)
        elif args.command == "random":
            result = random(args.count, args.subset, args.fields)
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
