---
name: alterlab-pubchem
description: Query PubChem via the PUG-REST API and PubChemPy across 110M+ compounds, searching by name, CID, or SMILES and retrieving molecular properties, bioactivity, and similarity/substructure matches. Use when looking up a chemical compound, converting names/SMILES to CIDs, fetching physicochemical properties, or running cheminformatics structure searches. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: Keyless PubChem PUG-REST API; PubChemPy optional for Python (no authentication required)
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# PubChem Database

## Overview

PubChem is the world's largest freely available chemical database with 110M+ compounds and
270M+ bioactivities. Query chemical structures by name, CID, or SMILES, retrieve molecular
properties, perform similarity and substructure searches, and access bioactivity data using
the PUG-REST API and PubChemPy.

## When to Use This Skill

This skill should be used when:
- Searching for chemical compounds by name, structure (SMILES/InChI), or molecular formula
- Retrieving molecular properties (MW, LogP, TPSA, hydrogen bonding descriptors)
- Performing similarity searches to find structurally related compounds
- Conducting substructure searches for specific chemical motifs
- Accessing bioactivity data from screening assays
- Converting between chemical identifier formats (CID, SMILES, InChI)
- Batch processing multiple compounds for drug-likeness screening or property analysis

## Core Capabilities

PubChem access is organized into nine capability areas. Copy-ready snippets for each live in
`references/capabilities.md`.

1. **Chemical structure search** — by name, CID, SMILES, InChI, or molecular formula.
2. **Property retrieval** — single, specific-list, or batch molecular properties.
3. **Similarity search** — Tanimoto similarity with threshold/MaxRecords.
4. **Substructure search** — find compounds containing a structural motif.
5. **Format conversion** — CID/SMILES/InChI/InChIKey and structure-file download.
6. **Structure visualization** — 2D PNG images via PubChemPy or direct URL.
7. **Synonym retrieval** — all known names for a compound.
8. **Bioactivity data access** — assay summaries via PUG-REST and helper script.
9. **Comprehensive annotations** — full PUG-View records (properties, drug info, safety, toxicity).

## Core Workflow

The canonical entry point resolves an identifier to a compound, then reads properties:

```python
import pubchempy as pcp

compound = pcp.get_compounds('aspirin', 'name')[0]
print(compound.cid, compound.molecular_formula, compound.molecular_weight)
print(compound.smiles, compound.xlogp, compound.tpsa)
```

Prefer CIDs for repeated queries (more efficient than names/structures). Similarity and
substructure searches run asynchronously and may take 15-30 seconds; PubChemPy polls
automatically. See `references/best_practices.md` for rate limits and error handling.

## Installation Requirements

```bash
uv pip install 'pubchempy>=1.0.5'  # Python-based access (1.0.5 = current SMILES property names)
uv pip install requests            # direct API / bioactivity queries
uv pip install pandas              # optional, for data analysis
```

**SMILES property naming (PubChem changed this in 2025):** the PUG-REST `CanonicalSMILES`
and `IsomericSMILES` properties are deprecated. Use `SMILES` (full SMILES with
stereo/isotope info, replaces `IsomericSMILES`) and `ConnectivitySMILES` (connectivity-only,
replaces `CanonicalSMILES`). In PubChemPy 1.0.5 the matching Compound attributes are
`compound.smiles` and `compound.connectivity_smiles` (the old `canonical_smiles` /
`isomeric_smiles` attributes still resolve but are deprecated).

## Helper Scripts

This skill ships two Python helper scripts under `scripts/`:

- `scripts/compound_search.py` — search, property retrieval, similarity/substructure search,
  synonyms, batch search, and structure download.
- `scripts/bioactivity_query.py` — bioassay summaries, target identification, target-based
  compound search, and PUG-View annotations.

Full function inventories and usage are in `references/helper_scripts.md`.

## Reference Index

- **`references/api_reference.md`** — Complete PUG-REST endpoint docs, full molecular property
  list, asynchronous request handling, PubChemPy API, PUG-View API, and official doc links.
- **`references/capabilities.md`** — Copy-ready code for all nine capability areas.
- **`references/workflows.md`** — Five end-to-end workflows (identifier conversion, drug-likeness
  screening, similar-candidate search, batch property comparison, substructure virtual screening).
- **`references/helper_scripts.md`** — Function inventory and usage for the two helper scripts.
- **`references/best_practices.md`** — Rate limits, best practices, error handling, troubleshooting,
  and additional resources.
