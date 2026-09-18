#!/usr/bin/env python3
"""
HMDB metabolite query tool.

HMDB has no public REST API; the canonical programmatic route is fetching the
per-metabolite XML record served at https://www.hmdb.ca/metabolites/<ID>.xml .
This tool retrieves that XML for an HMDB accession and extracts core fields
(name, formula, weight, SMILES, InChI, cross-references). Standard library only.

Record URL: https://www.hmdb.ca/metabolites/HMDB0000001.xml
Downloads:  https://www.hmdb.ca/downloads  (bulk XML/SDF/CSV)
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

BASE_URL = "https://www.hmdb.ca/metabolites"
USER_AGENT = "AlterLab-Academic-Skills/1.0 (HMDB metabolite query tool)"

# Simple, well-known top-level fields in the HMDB metabolite XML schema.
FIELDS = [
    "accession", "name", "chemical_formula", "average_molecular_weight",
    "monisotopic_molecular_weight",  # HMDB's actual (misspelled) XML tag
    "iupac_name", "smiles", "inchi",
    "inchikey", "cas_registry_number", "kegg_id", "pubchem_compound_id",
    "chebi_id", "status", "description",
]


def normalize_id(metabolite_id):
    """Zero-pad a bare HMDB number to the canonical 7-digit accession."""
    m = re.fullmatch(r"(?:HMDB)?0*(\d+)", metabolite_id.strip(), re.IGNORECASE)
    if not m:
        return metabolite_id
    return f"HMDB{int(m.group(1)):07d}"


def fetch_metabolite(metabolite_id):
    """Fetch and parse the HMDB XML record for an accession."""
    accession = normalize_id(metabolite_id)
    url = f"{BASE_URL}/{accession}.xml"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        root = ET.fromstring(resp.read())

    # HMDB XML is not namespaced; tags compared by local name for safety.
    def local(tag):
        return tag.split("}", 1)[-1]

    record = {f: None for f in FIELDS}
    for child in root:
        name = local(child.tag)
        if name in record and child.text and child.text.strip():
            record[name] = child.text.strip()
    return record


def main():
    parser = argparse.ArgumentParser(description="Fetch an HMDB metabolite record by accession")
    parser.add_argument(
        "hmdb_id",
        help="HMDB accession or bare number, e.g. HMDB0000001 or 1",
    )
    args = parser.parse_args()

    try:
        result = fetch_metabolite(args.hmdb_id)
    except urllib.error.HTTPError as exc:
        print(f"HTTP error {exc.code}: {exc.reason}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Connection error: {exc.reason}", file=sys.stderr)
        return 1
    except ET.ParseError as exc:
        print(f"XML parse error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
