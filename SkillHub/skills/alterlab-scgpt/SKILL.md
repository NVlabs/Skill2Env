---
name: alterlab-scgpt
description: Apply the scGPT single-cell foundation model (Cui 2024) to annotate and embed cells — zero-shot and fine-tuned cell-type annotation, gene/cell embeddings, batch integration, and gene-regulatory / perturbation inference from AnnData. Use when annotating cell types with a pretrained foundation model, generating scGPT embeddings, integrating batches with a transformer, or running zero-shot single-cell inference on an h5ad. For probabilistic latent models (scVI/scANVI) prefer alterlab-scvi-tools; for the standard QC→cluster→UMAP→DE pipeline prefer alterlab-scanpy; for the AnnData data structure itself prefer alterlab-anndata; for protein language models prefer alterlab-esm. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs the scGPT model (`bowang-lab/scGPT`; install `scgpt` — TODO(verify) exact pin) under `uv run python`. Pretrained checkpoints download once and cache (GB-scale); a CUDA GPU is strongly recommended (CPU is impractical for large datasets). Input/output is AnnData (`.h5ad`) in the scverse ecosystem. Dispatch heavy fine-tuning via alterlab-remote-compute."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# scGPT (single-cell foundation model)

## Overview

**scGPT** (Cui et al., *Nature Methods* 2024; `bowang-lab/scGPT`) is a transformer **foundation
model** pretrained on tens of millions of cells. It provides **zero-shot** and fine-tuned
**cell-type annotation**, **gene and cell embeddings**, **batch integration**, and
gene-regulatory / perturbation inference — all operating on **AnnData** (`.h5ad`) objects.

Its niche vs. the existing single-cell skills: scGPT is the *pretrained-transformer* route.
For probabilistic latent-variable models use `alterlab-scvi-tools`; for the conventional
Scanpy analysis pipeline use `alterlab-scanpy`; scGPT complements both.

## When to Use This Skill

Use this skill when the user wants to:
- **Annotate cell types** with a pretrained foundation model (zero-shot or fine-tuned).
- Generate **scGPT embeddings** for cells or genes.
- **Integrate batches** using the transformer's representation.
- Run **zero-shot** inference / transfer to a new dataset without training from scratch.

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Probabilistic integration / latent model (scVI, scANVI) | `alterlab-scvi-tools` |
| Standard QC → cluster → UMAP → differential expression | `alterlab-scanpy` |
| Read/write/wrangle the `.h5ad` data structure itself | `alterlab-anndata` |
| RNA velocity | `alterlab-scvelo` |
| Protein (not single-cell) language models | `alterlab-esm` |

## Core Capabilities

### 1. Zero-shot cell embedding & annotation

```python
# bowang-lab/scGPT — API sketch; TODO(verify) against installed scgpt
import scanpy as sc
adata = sc.read_h5ad("cells.h5ad")
# Load a pretrained scGPT checkpoint, embed cells, map to reference cell types.
# (see references/scgpt_usage.md for the exact embed/annotate calls)
```

Zero-shot mode maps a new dataset onto scGPT's learned space without training — fast triage
of cell identities. Fine-tuning on labeled reference data improves accuracy on a specific
tissue.

### 2. Embeddings for downstream analysis

Produce cell embeddings (for clustering/visualization) or gene embeddings (for
gene-network/similarity analysis). Feed embeddings back into a Scanpy neighbors/UMAP workflow.

### 3. Batch integration

Use the model representation to integrate across batches/donors, comparable in role to
scVI-based integration but from the pretrained-transformer paradigm.

### 4. GPU and dispatch

scGPT needs a GPU for realistic dataset sizes; fine-tuning is heavy. Dispatch fine-tuning /
large inference via `alterlab-remote-compute` (submit → poll → harvest). Keep the AnnData I/O
consistent with `alterlab-anndata`.

## Resources

- `references/scgpt_usage.md` — install/pinning, checkpoints, embed/annotate/fine-tune calls,
  scverse integration, and paradigm comparison. Loaded on demand.

Part of the AlterLab Academic Skills suite.
