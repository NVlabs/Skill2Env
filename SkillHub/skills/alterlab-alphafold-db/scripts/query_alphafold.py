#!/usr/bin/env python3
"""Query the AlphaFold DB public REST API (no API key required).

Endpoints (https://alphafold.ebi.ac.uk/api/):
  - prediction/{uniprot}   -> prediction metadata (entryId, file URLs, sequence)

The prediction metadata carries the exact, version-stamped file URLs
(cifUrl / pdbUrl / bcifUrl / plddtDocUrl / paeDocUrl). This script reads those
URLs from the response rather than hand-building a `_v{N}` suffix, so it keeps
working as the DB version advances (currently v6; old `_v4` file URLs now 404).

Smoke test:
    uv run python query_alphafold.py prediction P00520
    uv run python query_alphafold.py confidence P00520 --summary
    uv run python query_alphafold.py download P00520 --fmt cif -o ./structures
"""
import argparse
import json
import sys

import requests

API = "https://alphafold.ebi.ac.uk/api"

# Map a coordinate format to the metadata key that holds its URL.
_MODEL_URL_KEY = {"cif": "cifUrl", "pdb": "pdbUrl", "bcif": "bcifUrl"}


def get_prediction(uniprot: str) -> list:
    """Return AlphaFold prediction metadata records for a UniProt accession."""
    r = requests.get(f"{API}/prediction/{uniprot}", timeout=30)
    r.raise_for_status()
    return r.json()


def _first_record(uniprot: str) -> dict:
    preds = get_prediction(uniprot)
    if not preds:
        sys.exit(f"No AlphaFold prediction for {uniprot}")
    return preds[0]


def get_confidence(uniprot: str) -> dict:
    """Fetch the per-residue confidence (pLDDT) JSON for a UniProt accession."""
    rec = _first_record(uniprot)
    url = rec["plddtDocUrl"]
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()


def download(uniprot: str, fmt: str, outdir: str) -> str:
    """Download a structure file (cif/pdb/bcif) and return the saved path."""
    import os

    rec = _first_record(uniprot)
    url = rec[_MODEL_URL_KEY[fmt]]
    os.makedirs(outdir, exist_ok=True)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    path = os.path.join(outdir, url.rsplit("/", 1)[-1])
    with open(path, "wb") as fh:
        fh.write(r.content)
    return path


def main() -> None:
    p = argparse.ArgumentParser(description="Query AlphaFold DB (no key required).")
    p.add_argument("action", choices=["prediction", "confidence", "download"])
    p.add_argument("uniprot", help="UniProt accession, e.g. P00520")
    p.add_argument("--fmt", default="cif", choices=["cif", "pdb", "bcif"])
    p.add_argument("-o", "--outdir", default="./structures")
    p.add_argument("--summary", action="store_true",
                   help="For confidence: print mean pLDDT + length instead of raw JSON")
    args = p.parse_args()

    if args.action == "prediction":
        print(json.dumps(get_prediction(args.uniprot), indent=2))
    elif args.action == "confidence":
        conf = get_confidence(args.uniprot)
        if args.summary:
            scores = conf.get("confidenceScore", [])
            mean = sum(scores) / len(scores) if scores else 0.0
            print(json.dumps({"length": len(scores), "mean_plddt": round(mean, 2)}, indent=2))
        else:
            print(json.dumps(conf, indent=2))
    else:
        print(download(args.uniprot, args.fmt, args.outdir))


if __name__ == "__main__":
    main()
