#!/usr/bin/env python3
"""
NCI Imaging Data Commons (IDC) query tool.

IDC's public programmatic interface is the `idc-index` Python package, which
ships a local mini-index queryable with SQL (no auth, no network for queries).
This tool wraps that package: run arbitrary SQL, list collections, or report
the IDC data version. Install with: pip install --upgrade idc-index

Package: https://github.com/ImagingDataCommons/idc-index
Docs:    https://idc-index.readthedocs.io/
"""

import argparse
import json
import sys


def _client():
    """Instantiate an IDCClient, with a helpful error if idc-index is absent."""
    try:
        from idc_index import IDCClient
    except ImportError:
        sys.stderr.write(
            "idc-index is not installed. Install it with:\n"
            "    pip install --upgrade idc-index\n"
        )
        raise SystemExit(2)
    return IDCClient()


def cmd_version(_args):
    client = _client()
    return {"idc_data_version": client.get_idc_version()}


def cmd_collections(args):
    client = _client()
    df = client.sql_query(
        "SELECT collection_id, "
        "COUNT(DISTINCT PatientID) AS patients, "
        "COUNT(DISTINCT SeriesInstanceUID) AS series "
        "FROM index GROUP BY collection_id "
        "ORDER BY patients DESC "
        f"LIMIT {int(args.limit)}"
    )
    return df.to_dict(orient="records")


def cmd_sql(args):
    client = _client()
    df = client.sql_query(args.query)
    return df.to_dict(orient="records")


def main():
    parser = argparse.ArgumentParser(description="Query the NCI Imaging Data Commons via idc-index")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="Report the IDC data version")

    p_c = sub.add_parser("collections", help="List collections with patient/series counts")
    p_c.add_argument("--limit", type=int, default=50, help="Max collections to list")

    p_s = sub.add_parser("sql", help="Run a SQL query against the IDC mini-index")
    p_s.add_argument("query", help="SQL string, e.g. \"SELECT * FROM index LIMIT 5\"")

    args = parser.parse_args()
    handlers = {"version": cmd_version, "collections": cmd_collections, "sql": cmd_sql}
    result = handlers[args.command](args)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
