---
name: alterlab-alphafold-db
description: Access the AlphaFold DB of 200M+ AI-PREDICTED protein structures — retrieve models by UniProt accession, download PDB/mmCIF files, and analyze prediction confidence metrics (pLDDT, PAE). Use when a UniProt ID needs a computationally predicted 3D structure or when no experimental structure exists, for homology modeling, protein engineering, or structure-based drug discovery; for EXPERIMENTALLY determined structures (X-ray, cryo-EM, NMR) prefer alterlab-pdb, and for protein sequences, annotations, or accession ID mapping prefer alterlab-uniprot instead. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: Keyless AlphaFold DB (EBI) REST API; optional Google Cloud/BigQuery for bulk proteome downloads
metadata:
    skill-author: AlterLab
    version: "1.1.0"
---

# AlphaFold Database

## Overview

AlphaFold DB is a public repository of AI-predicted 3D protein structures for over 200 million proteins, maintained by DeepMind and EMBL-EBI. Access structure predictions with confidence metrics, download coordinate files, retrieve bulk datasets, and integrate predictions into computational workflows.

## When to Use This Skill

This skill should be used when working with AI-predicted protein structures in scenarios such as:

- Retrieving protein structure predictions by UniProt ID or protein name
- Downloading PDB/mmCIF coordinate files for structural analysis
- Analyzing prediction confidence metrics (pLDDT, PAE) to assess reliability
- Accessing bulk proteome datasets via Google Cloud Platform
- Comparing predicted structures with experimental data
- Performing structure-based drug discovery or protein engineering
- Building structural models for proteins lacking experimental structures
- Integrating AlphaFold predictions into computational pipelines

## Core Capabilities

Worked, copy-paste Python recipes for every capability below live in
`references/code_examples.md`. Load it when you need runnable code; the summaries
here give the routing and the key decisions.

### 1. Searching and Retrieving Predictions

Three entry points, in order of preference:

- **Biopython** (recommended): `Bio.PDB.alphafold_db.get_predictions(accession)`,
  `download_cif_for(...)`, `get_structural_models_for(...)` — simplest path.
- **Direct REST**: `GET https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}`;
  the AlphaFold ID is `response[0]['entryId']`.
- **Find accessions first via UniProt** when you only have a gene name or PDB ID —
  use the UniProt ID-mapping job API (`get_uniprot_ids` helper in
  `code_examples.md` §1; valid db names at
  https://rest.uniprot.org/configure/idmapping/fields).

### 2. Downloading Structure Files

The `/prediction` response carries version-stamped file URLs — **use those, don't
hand-build a `_v{N}` suffix.** The DB version advances (currently v6) and old
`_v4` file URLs now 404:

- `cifUrl` / `pdbUrl` / `bcifUrl` — atomic coordinates (mmCIF / PDB / binary CIF).
- `plddtDocUrl` — per-residue pLDDT scores (0-100).
- `paeDocUrl` — PAE matrix.

Download recipe (resolve URLs from the API, write bytes) in `code_examples.md` §2.

### 3. Working with Confidence Metrics

- **pLDDT**: from `plddtDocUrl`, read `confidence['confidenceScore']` (keys:
  `residueNumber`, `confidenceScore`, `confidenceCategory`); thresholds in
  "Confidence Interpretation Guidelines" below.
- **PAE**: from `paeDocUrl`. The endpoint returns a single-element JSON array of
  one object, so index `[0]` before the key
  (`pae[0]['predicted_aligned_error']`). Visualization recipe in
  `code_examples.md` §3.

### 4. Bulk Data Access via Google Cloud

For proteome-scale work, pull from `gs://public-datasets-deepmind-alphafold-v4/`
with `gsutil`, or query `bigquery-public-data.deepmind_alphafold.metadata` to
filter by organism/confidence. The species-download helper validates the taxonomy
ID and uses list-form `subprocess.run` (never `shell=True`). See
`code_examples.md` §4 and `references/api_reference.md` (Google Cloud / BigQuery).

### 5. Parsing and Analyzing Structures

Parse mmCIF with `Bio.PDB.MMCIFParser`; pLDDT is stored in the B-factor column
(`residue['CA'].get_bfactor()`). Contact-map and B-factor extraction recipes in
`code_examples.md` §5.

### 6. Batch Processing Multiple Proteins

Loop accessions → predictions → confidence stats → summary DataFrame. Full
example in `code_examples.md` §6.

## Installation and Setup

```bash
uv pip install biopython requests          # core: structure access + API
uv pip install numpy matplotlib pandas scipy  # analysis + PAE plots
uv pip install google-cloud-bigquery gsutil   # optional: bulk GCP access
```

**3D-Beacons alternative:** AlphaFold is also reachable via the 3D-Beacons
federated API (`https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{id}.json`),
filtering structures where `provider == 'AlphaFold DB'`. Recipe in
`code_examples.md` (3D-Beacons section).

## Common Use Cases

### Structural Proteomics
- Download complete proteome predictions for analysis
- Identify high-confidence structural regions across proteins
- Compare predicted structures with experimental data
- Build structural models for protein families

### Drug Discovery
- Retrieve target protein structures for docking studies
- Analyze binding site conformations
- Identify druggable pockets in predicted structures
- Compare structures across homologs

### Protein Engineering
- Identify stable/unstable regions using pLDDT
- Design mutations in high-confidence regions
- Analyze domain architectures using PAE
- Model protein variants and mutations

### Evolutionary Studies
- Compare ortholog structures across species
- Analyze conservation of structural features
- Study domain evolution patterns
- Identify functionally important regions

## Key Concepts

**UniProt Accession:** Primary identifier for proteins (e.g., "P00520"). Required for querying AlphaFold DB.

**AlphaFold ID:** Internal identifier format: `AF-[UniProt accession]-F[fragment number]` (e.g., "AF-P00520-F1").

**pLDDT (predicted Local Distance Difference Test):** Per-residue confidence metric (0-100). Higher values indicate more confident predictions.

**PAE (Predicted Aligned Error):** Matrix indicating confidence in relative positions between residue pairs. Low values (<5 Å) suggest confident relative positioning.

**Database Version:** The REST API currently serves v6 (the response reports `latestVersion` / `allVersions`); the bulk GCS/BigQuery datasets lag at v4. File URLs include a version suffix (e.g., `model_v6.cif`) — read them from the prediction response rather than hardcoding the suffix.

**Fragment Number:** Large proteins may be split into fragments. Fragment number appears in AlphaFold ID (e.g., F1, F2).

## Confidence Interpretation Guidelines

**pLDDT Thresholds:**
- **>90**: Very high confidence - suitable for detailed analysis
- **70-90**: High confidence - generally reliable backbone structure
- **50-70**: Low confidence - use with caution, flexible regions
- **<50**: Very low confidence - likely disordered or unreliable

**PAE Guidelines:**
- **<5 Å**: Confident relative positioning of domains
- **5-10 Å**: Moderate confidence in arrangement
- **>15 Å**: Uncertain relative positions, domains may be mobile

## Resources

### references/code_examples.md

Worked, copy-paste Python recipes for every Core Capability: prediction
retrieval (Biopython / REST / UniProt mapping), file downloads, pLDDT + PAE
analysis, GCP/BigQuery bulk access, mmCIF parsing, batch processing, and the
3D-Beacons alternative.

Load this when you need runnable code.

### references/api_reference.md

Comprehensive API documentation covering:
- Complete REST API endpoint specifications
- File format details and data schemas
- Google Cloud dataset structure and access patterns
- Advanced query examples and batch processing strategies
- Rate limiting, caching, and best practices
- Troubleshooting common issues

Consult this reference for detailed API information, bulk download strategies, or when working with large-scale datasets.

## Important Notes

### Data Usage and Attribution

- AlphaFold DB is freely available under CC-BY-4.0 license
- Cite: Jumper et al. (2021) Nature and Varadi et al. (2022) Nucleic Acids Research
- Predictions are computational models, not experimental structures
- Always assess confidence metrics before downstream analysis

### Version Management

- REST API serves v6 (`latestVersion`); bulk GCS/BigQuery datasets lag at v4
- Read file URLs from the `/prediction` response — never hardcode the `_v{N}` suffix
- Old `_v4` file URLs now 404; superseded versions are removed from `/files`
- Track which version a downloaded result came from

### Data Quality Considerations

- High pLDDT doesn't guarantee functional accuracy
- Low confidence regions may be disordered in vivo
- PAE indicates relative domain confidence, not absolute positioning
- Predictions lack ligands, post-translational modifications, and cofactors
- Multi-chain complexes are not predicted (single chains only)

### Performance Tips

- Use Biopython for simple single-protein access
- Use Google Cloud for bulk downloads (much faster than individual files)
- Cache downloaded files locally to avoid repeated downloads
- BigQuery free tier: 1 TB processed data per month
- Consider network bandwidth for large-scale downloads

## Additional Resources

- **AlphaFold DB Website:** https://alphafold.ebi.ac.uk/
- **API Documentation:** https://alphafold.ebi.ac.uk/api-docs
- **Google Cloud Dataset:** https://cloud.google.com/blog/products/ai-machine-learning/alphafold-protein-structure-database
- **3D-Beacons API:** https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/
- **AlphaFold Papers:**
  - Nature (2021): https://doi.org/10.1038/s41586-021-03819-2
  - Nucleic Acids Research (2024): https://doi.org/10.1093/nar/gkad1011
- **Biopython Documentation:** https://biopython.org/docs/dev/api/Bio.PDB.alphafold_db.html
- **GitHub Repository:** https://github.com/google-deepmind/alphafold

## Scripts

`scripts/query_alphafold.py` — runnable helper for the AlphaFold REST API (no key):

```bash
python scripts/query_alphafold.py prediction P00520
python scripts/query_alphafold.py confidence P00520 --summary
python scripts/query_alphafold.py download P00520 --fmt cif -o ./structures
```

