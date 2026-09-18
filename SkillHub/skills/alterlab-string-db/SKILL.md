---
name: alterlab-string-db
description: Query the STRING API for protein-protein interactions (59M proteins, 20B interactions across 5000+ species), building interaction networks, discovering functional partners, and running GO/KEGG/Pfam enrichment on protein lists. Use when constructing a protein-protein interaction network, expanding from seed proteins to functional partners, or running PPI-based enrichment for systems biology; for curated metabolic pathway maps and reactions prefer alterlab-kegg, and for protein sequences, annotations, or accession ID mapping prefer alterlab-uniprot instead. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: Keyless STRING REST API (no authentication required)
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# STRING Database

## Overview

STRING is a comprehensive database of known and predicted protein-protein
interactions covering 59M proteins and 20B+ interactions across 5000+ organisms.
Query interaction networks, perform functional enrichment, and discover partners
via the REST API for systems biology and pathway analysis.

## When to Use This Skill

Use this skill when:

- Retrieving protein-protein interaction networks for single or multiple proteins
- Performing functional enrichment (GO, KEGG, Pfam) on protein lists
- Discovering interaction partners and expanding protein networks
- Testing if proteins form significantly enriched functional modules
- Generating network visualizations with evidence-based coloring
- Analyzing homology and protein family relationships
- Conducting cross-species protein interaction comparisons
- Identifying hub proteins and network connectivity patterns

## What This Skill Provides

1. Python helper functions (`scripts/string_api.py`) for all STRING REST API
   operations.
2. Comprehensive reference documentation (`references/string_reference.md`) with
   detailed endpoint and parameter specifications.

When a user requests STRING data, determine which operation is needed and use
the appropriate function from `scripts/string_api.py`.

## Core Workflow

1. **Map identifiers first** — `string_map_ids()` converts gene/protein names to
   STRING IDs (format `9606.ENSP00000269305`); always do this for speed and
   accuracy.
2. **Retrieve the network or partners** — `string_network()` for tabular
   interaction data, `string_interaction_partners()` to expand from seeds,
   `string_network_image()` for a PNG figure.
3. **Test and interpret** — `string_ppi_enrichment()` checks whether the network
   has more edges than chance; `string_enrichment()` runs GO/KEGG/Pfam enrichment
   (FDR < 0.05 = significant).
4. **Compare / extend** — `string_homology()` for family/paralog analysis;
   repeat with other `species` for cross-species comparison.
5. **Record version** — `string_version()` for reproducibility.

The eight helper operations and five composed analysis workflows are documented
in the references below.

## Key Parameters

- **`required_score`** (confidence, 0-1000): 150 = low/exploratory, 400 =
  medium/default, 700 = high/conservative, 900 = highest/very stringent. Lower =
  higher recall (more false positives); higher = higher precision.
- **`network_type`**: `'functional'` (all evidence, default — pathway/systems
  biology) or `'physical'` (direct binding only — complexes, structural work).
- **`species`**: NCBI taxon ID (9606 human, 10090 mouse, 7227 fly, 4932 yeast,
  6239 C. elegans, 7955 zebrafish, …). Required for networks > 10 proteins. Full
  list: https://string-db.org/cgi/input?input_page_active_form=organisms

## API Best Practices

1. Always map identifiers first with `string_map_ids()`.
2. Prefer STRING IDs (`9606.ENSP00000269305`) over gene names.
3. Specify `species` for networks > 10 proteins.
4. Respect rate limits — wait ~1 second between API calls.
5. Pin a version for reproducibility — set `STRING_BASE_URL` to a stable
   subdomain (e.g. `https://version-12-0.string-db.org/api`) before running the
   helpers; see `string_reference.md`.
6. Handle errors gracefully — check for an `"Error:"` prefix in returned strings.
7. Match the confidence threshold to your analysis goals.

## Routing Guidance

- **Need the exact code for one operation (ID mapping, network, image, partners,
  functional enrichment, PPI enrichment, homology, version)?** Read
  `references/operations.md`.
- **Running an end-to-end analysis (protein-list, single-protein, pathway-centric,
  cross-species, or network expansion)?** Read `references/analysis-workflows.md`.
- **Need endpoint specs, output formats (TSV/JSON/XML/PSI-MI), evidence-channel
  details, advanced features, error handling, or tool integration (Cytoscape, R,
  Python)?** Read `references/string_reference.md`.

## References

- `references/operations.md` — The eight `scripts/string_api.py` operations with
  usage, parameters, output columns, and interpretation guidance.
- `references/analysis-workflows.md` — Five composed workflows: protein-list
  analysis, single-protein investigation, pathway-centric analysis, cross-species
  comparison, and network expansion/discovery.
- `references/string_reference.md` — Complete API endpoint specifications, all
  output formats, evidence channels and confidence-score details, advanced
  features (bulk upload, values/ranks enrichment), error handling, tool
  integration, and data license/citation.

## Troubleshooting (Quick)

- **No proteins found** — verify `species` matches identifiers; map first; check
  for typos.
- **Empty network** — lower `required_score`; confirm the proteins interact;
  verify species.
- **Timeout / slow** — reduce input size; use STRING IDs; batch large queries.
- **"Species required" error** — add `species` for networks > 10 proteins.
- **Unexpected results** — check `string_version()`; verify `network_type`;
  review the confidence threshold.

See `references/string_reference.md` for the full troubleshooting section.

## Additional Resources

- Web app (proteome upload, complete network + function prediction):
  https://string-db.org
- Bulk downloads (interactions, annotations, pathway mappings):
  https://string-db.org/cgi/download

## Data License and Citation

STRING data is freely available under **Creative Commons BY 4.0** (free for
academic and commercial use, attribution required). When publishing, cite the
most recent STRING publication: https://string-db.org/cgi/about
