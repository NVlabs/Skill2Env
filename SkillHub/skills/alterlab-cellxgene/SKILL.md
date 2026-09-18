---
name: alterlab-cellxgene
description: Query the CZ CELLxGENE Census (61M+ cells) programmatically via cellxgene-census and TileDB-SOMA, slicing expression by tissue, disease, or cell type and returning AnnData. Use when pulling reference single-cell RNA-seq data from the largest curated public atlas, running population-scale queries, or benchmarking your data against a reference — for analyzing your own dataset use scanpy or scvi-tools. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with the skill's Python package installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# CZ CELLxGENE Census

## Overview

The CZ CELLxGENE Census provides programmatic, versioned access to standardized single-cell genomics data from CZ CELLxGENE Discover. It contains **61+ million cells** (human and mouse) with standardized metadata (cell types, tissues, diseases, donors), raw gene expression matrices, pre-calculated embeddings, and integration with PyTorch, scanpy, and other analysis tools.

## When to Use This Skill

Use this skill when:
- Querying single-cell expression data by cell type, tissue, or disease
- Exploring available single-cell datasets and metadata
- Training machine learning models on single-cell data
- Performing large-scale cross-dataset analyses
- Integrating Census data with scanpy or other analysis frameworks
- Computing statistics across millions of cells
- Accessing pre-calculated embeddings or model predictions

For analyzing **your own** dataset (not the reference atlas), use scanpy or scvi-tools instead.

## Installation

```bash
uv pip install cellxgene-census
# For PyTorch ML workflows (loaders moved out of cellxgene-census):
uv pip install tiledbsoma-ml
```

## Core Workflow

1. **Open the Census** with a context manager; pin `census_version` for reproducibility.
2. **Explore metadata first** (`get_obs` / datasets summary) to understand what's available — always filter `is_primary_data == True` to avoid duplicate cells.
3. **Estimate query size** before loading expression. < 100k cells → `get_anndata()` (in-memory); larger → `axis_query()` out-of-core iteration.
4. **Query expression** with `obs_value_filter` (cells) and `var_value_filter` (genes); select only the `obs_column_names` you need.
5. **Downstream**: hand the returned AnnData to scanpy, or stream batches into a PyTorch dataloader for ML.

Minimal skeleton:
```python
import cellxgene_census

with cellxgene_census.open_soma(census_version="2023-07-25") as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="cell_type == 'B cell' and tissue_general == 'lung' and is_primary_data == True",
    )
```

## Routing Guidance

- **Small/medium query (fits in RAM)** → `get_anndata()`. See `references/querying_expression.md`.
- **Query exceeds RAM** → `axis_query()` with chunked iteration and incremental stats. See `references/querying_expression.md`.
- **Training ML models** → `tiledbsoma_ml` PyTorch dataloader / `ExperimentDataset`. See `references/ml_and_scanpy.md`.
- **Standard scanpy analysis / multi-tissue integration** → see `references/ml_and_scanpy.md`.
- **Need full schema, all metadata fields, or filter-syntax details** → `references/census_schema.md`.

## Reference Index

- **`references/querying_expression.md`** — Opening the Census, exploring metadata, small/medium `get_anndata()` queries, and large out-of-core `axis_query()` processing with incremental statistics.
- **`references/ml_and_scanpy.md`** — `tiledbsoma_ml` PyTorch dataloader / `ExperimentDataset` train-test splits, scanpy integration, multi-dataset/tissue integration (`anndata.concat`), and four worked use cases.
- **`references/best_practices_and_troubleshooting.md`** — Primary-data filtering, version pinning, query-size estimation, `tissue_general` vs `tissue`, presence matrices, the full obs/var metadata field list, and a troubleshooting guide.
- **`references/census_schema.md`** — Census data structure, all metadata fields, value-filter syntax/operators, SOMA object types, and data inclusion criteria.
- **`references/common_patterns.md`** — Extras beyond the core recipes: incremental (Welford) variance out-of-core, ontology-term filtering, batch-processing sweeps, and a common-pitfalls list.
