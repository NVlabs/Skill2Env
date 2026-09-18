---
name: alterlab-pydeseq2
description: Run differential gene expression analysis on bulk RNA-seq count matrices with PyDESeq2, the Python port of DESeq2 — size-factor normalization, dispersion estimation, Wald tests, FDR (Benjamini-Hochberg) correction, and volcano/MA plots. Use when identifying differentially expressed genes between conditions from raw bulk RNA-seq counts. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with the skill's Python package installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# PyDESeq2

## Overview

PyDESeq2 is a Python implementation of DESeq2 for differential expression analysis with bulk RNA-seq data. It supports complete workflows from data loading through result interpretation, including single-factor and multi-factor designs, Wald tests with multiple-testing correction, optional apeGLM shrinkage, and integration with pandas and AnnData.

## When to Use This Skill

Use this skill when:
- Analyzing bulk RNA-seq count data for differential expression
- Comparing gene expression between experimental conditions (e.g., treated vs control)
- Performing multi-factor designs accounting for batch effects or covariates
- Converting R-based DESeq2 workflows to Python
- Integrating differential expression analysis into Python-based pipelines
- Users mention "DESeq2", "differential expression", "RNA-seq analysis", or "PyDESeq2"

## Installation and Requirements

```bash
uv pip install "pydeseq2>=0.5,<0.6"
```

**System requirements (pydeseq2 0.5.x):** Python ≥3.11; numpy ≥2.0, pandas ≥2.2, scipy ≥1.12, scikit-learn ≥1.4, anndata ≥0.11, formulaic ≥1.0.2 (parses the `~` design formula), matplotlib ≥3.9. These are pulled in automatically as dependencies.

**API note (0.4+):** parallelism is configured through an `inference` object, not a bare `n_cpus=` kwarg:

```python
from pydeseq2.default_inference import DefaultInference
inference = DefaultInference(n_cpus=8)
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition", inference=inference)
ds = DeseqStats(dds, contrast=["condition", "treated", "control"], inference=inference)
```

## Core Workflow

1. **Prepare data** — load counts as **samples × genes** (transpose with `.T` if loaded genes × samples); filter low-count genes (e.g., total reads < 10); drop samples with missing metadata.
2. **Specify the design** — Wilkinson formula (`"~condition"`, `"~batch + condition"`); put adjustment variables before the variable of interest.
3. **Fit** — `DeseqDataSet(...).deseq2()` runs the full pipeline (size factors → dispersions → LFCs → Cook's outliers).
4. **Test** — `DeseqStats(dds, contrast=[var, test, ref]).summary()`; read `results_df`.
5. **(Optional) shrink** — `ds.lfc_shrink()` for visualization/ranking only; p-values stay unshrunken.
6. **Interpret/export** — filter on `padj < 0.05`, plot volcano/MA, save CSV/pickle.

Minimal skeleton:
```python
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
significant = ds.results_df[ds.results_df.padj < 0.05]
```

## Command-Line Script

This skill includes a complete standalone script for standard analyses:

```bash
python scripts/run_deseq2_analysis.py \
  --counts counts.csv \
  --metadata metadata.csv \
  --design "~batch + condition" \
  --contrast condition treated control \
  --output results/ \
  --min-counts 10 --alpha 0.05 --n-cpus 4 --plots
```

It handles data loading/validation, gene+sample filtering, the full DESeq2 pipeline, statistical testing with customizable parameters, result export (CSV, pickle), and optional volcano/MA plots. Refer users to `scripts/run_deseq2_analysis.py` for batch-processing multiple datasets.

## Routing Guidance

- **Running a standard analysis (load → fit → test → export), or any specific design (two-group, multi-comparison, batch, covariate)** → `references/pipeline_steps.md`.
- **Interpreting results, ranking genes, plotting volcano/MA, or quality metrics** → `references/interpretation_and_plots.md`.
- **Hitting an error** (index mismatch, all-zero counts, "not full rank", no significant genes) → Troubleshooting in `references/interpretation_and_plots.md`.
- **Need exact class/method parameters or object attributes** → `references/api_reference.md`.
- **Complex experimental designs or in-depth workflow** → `references/workflow_guide.md`.

## Key Reminders

1. **Data orientation matters:** counts usually load genes × samples but need samples × genes — transpose with `.T` if needed.
2. **Sample filtering:** remove samples with missing metadata before analysis.
3. **Gene filtering:** drop low-count genes (e.g., < 10 total reads) to improve power.
4. **Design formula order:** adjustment variables before the variable of interest (`"~batch + condition"`).
5. **LFC shrinkage timing:** shrink after testing, for visualization/ranking only — p-values stay unshrunken.
6. **Significance:** use `padj < 0.05` (Benjamini-Hochberg FDR), not raw p-values.
7. **Contrast format:** `[variable, test_level, reference_level]`.
8. **Save intermediates:** pickle the DeseqDataSet to avoid re-running the expensive fit.

## Reference Index

- **`references/pipeline_steps.md`** — Quick-start, the six pipeline steps with full code (data prep, design, fitting, testing, shrinkage, export), and four common experimental designs.
- **`references/interpretation_and_plots.md`** — Filtering/ranking significant genes, quality metrics, volcano and MA plots, and a troubleshooting guide.
- **`references/api_reference.md`** — Complete PyDESeq2 class/method/parameter and data-structure documentation.
- **`references/workflow_guide.md`** — In-depth complete workflows, data-loading patterns, multi-factor designs, and best practices.

## Additional Resources

- **Official Documentation:** https://pydeseq2.readthedocs.io
- **GitHub Repository:** https://github.com/owkin/PyDESeq2
- **Publication:** Muzellec et al. (2023) Bioinformatics, DOI: 10.1093/bioinformatics/btad547
- **Original DESeq2 (R):** Love et al. (2014) Genome Biology, DOI: 10.1186/s13059-014-0550-8
