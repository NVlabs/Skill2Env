---
name: alterlab-gwas
description: Query the NHGRI-EBI GWAS Catalog REST API for SNP-trait associations, retrieving variants by rs ID, disease/trait, or gene along with p-values and summary statistics. Use when investigating genome-wide association study hits, mapping a SNP or rsID to traits, building polygenic risk scores, or doing genetic epidemiology lookups. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: Keyless NHGRI-EBI GWAS Catalog REST API (no authentication required)
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# GWAS Catalog Database

## Overview

The GWAS Catalog is a curated repository of published genome-wide association studies maintained by NHGRI and EBI. It contains SNP-trait associations from thousands of GWAS publications — genetic variants, associated traits and diseases, p-values, effect sizes, and full summary statistics for many studies.

## Scripts

`scripts/query_gwas.py` — query the GWAS Catalog REST API (stdlib only, JSON to stdout):

```bash
python scripts/query_gwas.py variant rs7903146           # associations for a SNP
python scripts/query_gwas.py trait MONDO_0005148 --size 100  # associations for a trait
python scripts/query_gwas.py study GCST001795            # study metadata
```

## When to Use This Skill

Use this skill for:
- **Genetic variant associations** — SNPs associated with diseases or traits
- **SNP lookups** — information about specific variants (rs IDs)
- **Trait/disease searches** — genetic associations for phenotypes
- **Gene associations** — variants in or near specific genes
- **GWAS summary statistics** — complete genome-wide association data
- **Study metadata** — publication and cohort information
- **Population genetics** — ancestry-specific associations
- **Polygenic risk scores** — variants for risk prediction models
- **Functional genomics** / **systematic reviews** — variant effects, literature synthesis

## Data Model

Four core entities, each with a canonical identifier:
- **Studies** → `GCST` accessions (e.g., GCST001234)
- **Associations** → SNP-trait links with p-values (genome-wide significant: p ≤ 5×10⁻⁸)
- **Variants** → `rs` numbers (e.g., rs7903146)
- **Traits** → trait ontology short-forms (e.g., MONDO_0005148 = type 2 diabetes on the main REST API); genes use HGNC symbols (e.g., TCF7L2)

> **Trait-ID gotcha (verified):** the two APIs disagree on trait IDs. The main REST API has migrated many traits to MONDO / current EFO short-forms, so `efoTraits/MONDO_0005148` works but the legacy `efoTraits/EFO_0001360` now 404s. The Summary Statistics API still uses the legacy ID: `traits/EFO_0001360` works there but `traits/MONDO_0005148` 404s. If a trait path 404s, look up the current short-form with `/efoTraits/search/findByTrait?trait=...` (main API) before assuming the trait is absent.

## APIs

Two free, no-key REST APIs:
- **GWAS Catalog API**: `https://www.ebi.ac.uk/gwas/rest/api` (curated associations, studies, variants, traits)
- **Summary Statistics API**: `https://www.ebi.ac.uk/gwas/summary-statistics/api` (all tested variants, not just significant hits)

Core endpoints: `/studies/{GCST}`, `/efoTraits/{efoID}/associations`, `/singleNucleotidePolymorphisms/{rsID}` and `/{rsID}/associations`. Responses are HAL+JSON with `_embedded` results, `_links` for related resources, and pagination (`page`, `size`).

## Core Workflow

1. **Identify the entity** — get the EFO ID (trait), rs ID (variant), GCST (study), or HGNC symbol (gene). Use the web interface for free-text → EFO mapping.
2. **Query the matching endpoint** — trait/variant/study/region; iterate pages via `page`/`size`.
3. **Filter** — by p-value (≤ 5×10⁻⁸ for genome-wide significance), ancestry, sample size, discovery/replication status.
4. **Extract** — rs IDs, effect alleles/directions, effect sizes (OR or beta), p-values.
5. **Cross-reference** — Ensembl (consequences), gnomAD (frequencies), Open Targets, PGS Catalog.
6. **For genome-wide analyses** — pull full summary statistics via the Summary Statistics API or FTP rather than scraping the association endpoints.

## Routing Guidance

- **Writing API calls / want copy-paste code** (endpoints, the four worked examples, summary-stats access, cross-referencing, full paginated Python helper) → `references/query_examples.md`.
- **Following a multi-step task** (disease-, variant-, gene-centric, systematic review, summary-stats analysis) or **web-interface search syntax** → `references/query_workflows.md`.
- **Need response field names, pagination details, or best-practice / data-quality guidance** → `references/data_fields_and_best_practices.md`.
- **Deep endpoint specs, all query params, error handling, advanced filtering** → `references/api_reference.md`.

## Reference Index

- **`references/query_examples.md`** — REST endpoint code, four canonical query examples (disease, variant, summary stats, chromosomal region), summary-statistics access, cross-referencing, and a complete paginated Python integration returning a DataFrame.
- **`references/query_workflows.md`** — Five step-by-step query workflows (disease, variant, gene, systematic review, summary statistics) plus web-interface search modes.
- **`references/data_fields_and_best_practices.md`** — Association/study response fields, pagination, query and interpretation best practices, rate-limiting ethics, and data-quality considerations.
- **`references/api_reference.md`** — Comprehensive endpoint specifications, query parameters/filters, response formats, error handling, and integration with external databases.

## Citation and Resources

When using GWAS Catalog data, cite:
- Sollis E, et al. (2023) The NHGRI-EBI GWAS Catalog: knowledgebase and deposition resource. Nucleic Acids Research 51:D977-D985. PMID: 36350656. DOI: 10.1093/nar/gkac1010
- Include access date and version when available; cite original studies when discussing specific findings.

- **Website**: https://www.ebi.ac.uk/gwas/
- **Documentation**: https://www.ebi.ac.uk/gwas/docs
- **API docs**: https://www.ebi.ac.uk/gwas/rest/docs/api
- **Summary Statistics API**: https://www.ebi.ac.uk/gwas/summary-statistics/docs/
- **FTP site**: http://ftp.ebi.ac.uk/pub/databases/gwas/
- **Training materials**: https://github.com/EBISPOT/GWAS_Catalog-workshop (Jupyter notebooks, Colab)
- **PGS Catalog** (polygenic scores): https://www.pgscatalog.org/
- **Help and support**: gwas-info@ebi.ac.uk
