---
name: alterlab-borzoi
description: Predict genome-wide functional genomics tracks from DNA sequence with Borzoi (Linder 2025) — a sequence-to-function model outputting RNA-seq, CAGE, ATAC, and ChIP coverage across long context, used to score non-coding and regulatory variant effects. Use when predicting functional tracks from a DNA sequence, scoring a non-coding/regulatory variant's effect on expression or chromatin, or doing in-silico mutagenesis of a locus. To LOOK UP a variant's population frequency prefer alterlab-gnomad; for its clinical significance prefer alterlab-clinvar; for protein-structure effects prefer alterlab-alphafold; for single-cell foundation models prefer alterlab-scgpt. Part of the AlterLab Academic Skills suite.
license: Apache-2.0
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs Borzoi (`calico/borzoi`; install per repo — TODO(verify) exact pin) under `uv run python`. Model weights download once and cache; a CUDA GPU is recommended (the model takes long DNA context and is heavy on CPU). Inputs are DNA sequences (FASTA / genome coordinates + a reference); outputs are multi-track coverage arrays. Dispatch large scans via alterlab-remote-compute."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Borzoi (sequence → function)

## Overview

**Borzoi** (Linder et al. 2025; `calico/borzoi`) is a **sequence-to-function** deep-learning
model: given a DNA sequence over a long genomic context, it predicts **genome-wide functional
tracks** — RNA-seq, CAGE, ATAC-seq, and ChIP coverage across many assays/tissues. Its headline
use is **non-coding variant effect scoring**: run the reference and alternate alleles through
the model and compare predicted tracks to estimate a regulatory variant's impact on expression
or chromatin.

It **predicts** function from sequence; it does not *look up* known variants. For a variant's
population frequency use `alterlab-gnomad`; for clinical significance use `alterlab-clinvar`.

## When to Use This Skill

Use this skill when the user wants to:
- Predict **functional tracks** (RNA-seq/CAGE/ATAC/ChIP) from a DNA sequence or locus.
- Score a **non-coding / regulatory variant's** predicted effect (ref vs. alt).
- Run **in-silico mutagenesis** to find driver bases in a regulatory element.
- Prioritize candidate regulatory variants by predicted functional impact.

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Look up a variant's **population frequency** | `alterlab-gnomad` |
| Look up a variant's **clinical significance** | `alterlab-clinvar` |
| Predict a **protein-structure** / coding effect | `alterlab-alphafold` |
| Single-cell foundation-model tasks | `alterlab-scgpt` |
| Standard variant calling from reads | `alterlab-nf-core-sarek` (or the relevant pipeline skill) |

## Core Capabilities

### 1. Track prediction from sequence

```python
# calico/borzoi — API sketch; TODO(verify) against installed borzoi
# 1) extract the reference sequence window around a locus
# 2) run the model to get multi-track predicted coverage
# (see references/borzoi_usage.md for the exact model-loading + predict calls)
```

Provide a genome window (coordinates + reference, or a FASTA); the model returns predicted
coverage across its output tracks.

### 2. Non-coding variant effect scoring

The core workflow: build the **reference** and **alternate** sequences for a variant, predict
tracks for each, and quantify the difference (e.g. SAD/SED-style scores) to estimate the
variant's regulatory effect. Prioritize candidates by the magnitude of predicted change.

### 3. In-silico mutagenesis

Systematically mutate bases across a regulatory element and read the predicted-track deltas to
localize functionally important positions (motif/driver discovery).

### 4. GPU and dispatch

Borzoi takes long context and is GPU-heavy; genome-wide or many-variant scans should be
dispatched via `alterlab-remote-compute` (submit → poll → harvest).

## Resources

- `references/borzoi_usage.md` — install/pinning, sequence extraction, predict calls,
  ref/alt variant scoring, in-silico mutagenesis, and Enformer lineage. Loaded on demand.

Part of the AlterLab Academic Skills suite.
