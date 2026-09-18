---
name: alterlab-qiime2-amplicon
description: 'Runs 16S/ITS amplicon (microbiome) analysis with the QIIME 2 amplicon distribution (2026.1; renamed to "qiime2" in 2026.4) in the correct order: manifest import, cutadapt trim-paired primer removal BEFORE dada2 denoise-paired (trunc-len chosen from the demux quality .qzv), feature-classifier classify-sklearn against a version-matched SILVA 138 or Greengenes2 classifier, and diversity core-metrics-phylogenetic — teaching the .qza/.qzv artifact-and-provenance model and the 2026.1 feature-table summarize change (the former summarize_plus). Use when the request mentions QIIME2, QIIME 2, qiime, 16S, 18S, ITS, amplicon, microbiome, ASV, DADA2 denoising, feature table, taxonomic classification, or core-metrics diversity. For downstream alpha/beta diversity, PCoA, and PERMANOVA on the exported feature table prefer alterlab-scikit-bio; this is conda-only (no pip install). Part of the AlterLab Academic Skills suite.'
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*) Bash(qiime:*) Bash(conda:*)
compatibility: "Requires the QIIME 2 amplicon conda environment (cannot be pip-installed); commands are run via the `qiime` CLI. Pretrained classifiers and reference data are downloaded from the QIIME 2 Library. The helper scripts in scripts/ are stdlib-only and run under `uv run python` without a QIIME 2 env."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# QIIME 2 Amplicon — 16S/ITS Microbiome Pipeline (FASTQ → Feature Table → Taxonomy → Diversity)

The command-line, workflow-runner entry point for marker-gene (amplicon) microbiome
analysis. Given raw demultiplexed paired-end reads, it walks the **canonical QIIME 2
order** — import → primer trim → denoise → classify → diversity — and teaches the two
things people get wrong most: **trimming primers BEFORE DADA2**, and the **.qza/.qzv
provenance model**. It is the raw-data-to-result pipeline that hands a feature table off
to in-memory analysis skills (see routing below).

Pinned to **QIIME 2 2026.1** (the `amplicon` distribution). Forward-compat note: the
distribution is **renamed `qiime2` in 2026.4** — the env name and channel URL change, the
plugin commands below do not.

## When to Use This Skill

Use this skill when the request involves running an amplicon / microbiome pipeline from
sequencing reads:

- "Run a QIIME 2 16S pipeline on my paired-end reads."
- "I have ITS amplicon FASTQs — denoise with DADA2 and assign taxonomy."
- "Build a feature table / ASV table and classify against SILVA."
- "Pick truncation lengths from my quality plot and run core-metrics diversity."
- "How do I trim primers before DADA2 in QIIME 2?"
- "What's the right order of QIIME 2 commands?"

### Does NOT Trigger — route these elsewhere

| The request is really about… | Route to |
|------------------------------|----------|
| Alpha/beta diversity, UniFrac, **PCoA ordination, PERMANOVA** on an already-exported feature/distance table (in-memory, Python) | `alterlab-scikit-bio` |
| Building / manipulating a phylogenetic tree, tree visualization, or comparative phylogenetics outside QIIME 2 | `alterlab-phylogenetics` / `alterlab-etetoolkit` |
| **Shotgun metagenomics** taxonomic profiling, MAG assembly, functional genes (not marker-gene amplicons) | not in this skill — amplicon only; flag the gap |
| **RNA-seq** transcript quantification (salmon/kallisto), differential expression | `alterlab-rnaseq-quant` → `alterlab-pydeseq2` |
| **Variant calling** FASTQ → VCF (germline/somatic) | `alterlab-nf-core-sarek` |
| Protein/nucleotide **sequence similarity search** (BLAST+/DIAMOND) | `alterlab-blast` |
| **Spatial** transcriptomics neighborhood/enrichment analysis | `alterlab-squidpy-spatial` |
| Quick one-off gene/sequence/database lookups | `alterlab-gget` |
| Reading/writing BAM/SAM/VCF, alignment file surgery | `alterlab-pysam` |

This skill is **amplicon (marker-gene) only**. If the data is shotgun metagenomic,
single-cell, or anything other than 16S/18S/ITS marker-gene sequencing, say so and stop.

## The Artifact Model (.qza / .qzv) — read this first

Everything in QIIME 2 is a **typed, zipped artifact** that records its own provenance:

- **`.qza`** — a QIIME 2 **Artifact**: data (a feature table, sequences, a classifier)
  plus an embedded **semantic type** (e.g. `SampleData[PairedEndSequencesWithQuality]`,
  `FeatureTable[Frequency]`) and a full **provenance graph** of every action that
  produced it.
- **`.qzv`** — a **Visualization**: a human-viewable report (quality plots, summaries,
  diversity emperor plots). Drag it into **https://view.qiime2.org** (offline, in-browser)
  or run `qiime tools view file.qzv`.
- Provenance is the reproducibility win: any `.qza/.qzv` carries the exact commands,
  parameters, and plugin versions that made it. Keep artifacts, not just exports.

Treat semantic types as the contract: an action only accepts artifacts of the type it
declares, which is why import (step 1) matters so much.

## The Canonical Order (do not reorder)

```
manifest import → cutadapt trim-paired (primers) → dada2 denoise-paired
   → feature-table summarize → feature-classifier classify-sklearn
   → phylogeny → diversity core-metrics-phylogenetic
```

**Primer trimming comes BEFORE DADA2.** DADA2 models per-base error rates; leftover
primer/adapter bases corrupt that error model and inflate spurious ASVs. Trim with
`cutadapt trim-paired` first, then denoise. (If your reads are already primer-free —
e.g. EMP-style — you can skip cutadapt, but verify, don't assume.)

### 0. Install / activate the environment (conda only — no pip)

QIIME 2 **cannot be pip-installed**; it ships as a conda environment. For 2026.1
(verified env files live in `qiime2/distributions`):

```bash
# macOS (Apple Silicon / Intel) — 2026.1 amplicon distribution
conda env create \
  --name qiime2-amplicon-2026.1 \
  --file https://raw.githubusercontent.com/qiime2/distributions/dev/2026.1/amplicon/released/qiime2-amplicon-macos-latest-conda.yml
# Linux: swap the filename for qiime2-amplicon-ubuntu-latest-conda.yml
conda activate qiime2-amplicon-2026.1
qiime info   # confirm version + installed plugins
```

For **2026.4**, the official command uses the renamed distribution
(`--name rachis-qiime2-2026.4`, file `rachis-qiime2-*-conda.yml`); see the QIIME 2
Library quickstart. Full install detail and the env-file matrix:
[`references/installation.md`](references/installation.md).

> Bulk DADA2 denoising and classifier training are CPU/RAM heavy. On Cem's M4 Max these
> run fine locally — keep them off the API and run them in a `conda activate`d shell.

### 1. Import demultiplexed paired-end reads (manifest)

Use a **manifest** (a TSV mapping sample IDs → absolute FASTQ paths) so you control
exactly which files map to which sample. Format: `PairedEndFastqManifestPhred33V2`
(verified in `q2-types`).

```bash
qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-format PairedEndFastqManifestPhred33V2 \
  --input-path manifest.tsv \
  --output-path demux.qza

qiime demux summarize \
  --i-data demux.qza \
  --o-visualization demux.qzv     # ← READ THIS to choose trunc-len
```

Manifest schema, single-end and EMP variants, and ITS notes:
[`references/import_and_manifest.md`](references/import_and_manifest.md).
Generate a manifest from a folder of FASTQs with
[`scripts/make_manifest.py`](scripts/make_manifest.py).

### 2. Trim primers with cutadapt (BEFORE DADA2)

```bash
qiime cutadapt trim-paired \
  --i-demultiplexed-sequences demux.qza \
  --p-front-f GTGYCAGCMGCCGCGGTAA \   # forward primer (example: 515F)
  --p-front-r GGACTACNVGGGTWTCTAAT \  # reverse primer (example: 806R)
  --p-discard-untrimmed \
  --o-trimmed-sequences demux-trimmed.qza
qiime demux summarize --i-data demux-trimmed.qza --o-visualization demux-trimmed.qzv
```

`--p-discard-untrimmed` drops reads where the primer was not found (usually what you
want for targeted amplicons). Action and flag names verified from the `q2-cutadapt`
source. Primer choice by region (515F/806R, ITS1F/ITS2, etc.):
[`references/pipeline_steps.md`](references/pipeline_steps.md).

### 3. Denoise with DADA2 → ASVs + feature table

Open `demux-trimmed.qzv`, read the **interactive quality plot**, and pick truncation
lengths where median quality drops (forward and reverse independently). Truncated read
length must still leave enough overlap to merge pairs.

```bash
qiime dada2 denoise-paired \
  --i-demultiplexed-seqs demux-trimmed.qza \
  --p-trunc-len-f 0 --p-trunc-len-r 0 \   # ← set from the quality .qzv (0 = no truncation)
  --p-trim-left-f 0 --p-trim-left-r 0 \
  --o-representative-sequences rep-seqs.qza \
  --o-table table.qza \
  --o-denoising-stats denoising-stats.qza
qiime metadata tabulate \
  --m-input-file denoising-stats.qza --o-visualization denoising-stats.qzv
```

Always inspect `denoising-stats.qzv`: low merge or chimera-survival rates usually mean
trunc-len was too aggressive (no overlap) or primers were not trimmed.

### 4. Summarize the feature table — note the 2026.1 change

```bash
qiime feature-table summarize \
  --i-table table.qza \
  --m-sample-metadata-file sample-metadata.tsv \
  --o-summary table.qzv
```

**2026.1 breaking change (verified in the release notes):** the old `summarize`
visualizer was renamed `_summarize`, and the former **`summarize_plus` pipeline is now
`summarize`** — so today's `feature-table summarize` *is* the enhanced summary (it also
emits feature/sample frequency artifacts). Older tutorials calling `summarize_plus` must
switch to `summarize`. Details: [`references/version_notes.md`](references/version_notes.md).

### 5. Assign taxonomy — VERSION-MATCHED classifier

```bash
qiime feature-classifier classify-sklearn \
  --i-classifier silva-138-99-nb-classifier.qza \   # MUST match your QIIME 2 version
  --i-reads rep-seqs.qza \
  --o-classification taxonomy.qza
qiime metadata tabulate --m-input-file taxonomy.qza --o-visualization taxonomy.qzv
```

A pretrained naive-Bayes classifier is **pickled scikit-learn** — it only loads under the
QIIME 2 release it was trained on. Download the classifier built for **your** version
from the QIIME 2 Library (SILVA 138 for 16S/18S, Greengenes2 for 16S, UNITE for ITS).
Version-match traps and the train-your-own path:
[`references/classifiers.md`](references/classifiers.md).

### 6. Phylogeny + core diversity

```bash
qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences rep-seqs.qza \
  --o-alignment aligned.qza --o-masked-alignment masked.qza \
  --o-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny rooted-tree.qza \
  --i-table table.qza \
  --p-sampling-depth 1103 \           # ← choose from table.qzv rarefaction; see below
  --m-metadata-file sample-metadata.tsv \
  --output-dir core-metrics
```

**Sampling depth** is a rarefaction floor: every sample is subsampled to this many reads,
and samples below it are dropped. Pick it from `table.qzv` to balance depth against sample
retention — never guess. `core-metrics-phylogenetic` produces Faith's PD, Shannon,
observed features, Bray-Curtis / Jaccard / weighted+unweighted UniFrac distance matrices,
and Emperor PCoA `.qzv`s in one shot.

For **stats and ordination off the exported table** (PERMANOVA, custom PCoA, alpha/beta
metrics in Python), export and hand off to **`alterlab-scikit-bio`** — that is the
in-memory companion to this pipeline.

## Export to hand off downstream

```bash
qiime tools export --input-path table.qza --output-path exported/   # → feature-table.biom
qiime tools export --input-path taxonomy.qza --output-path exported/ # → taxonomy.tsv
```

`scripts/check_artifact.py` reads a `.qza/.qzv` (it is just a zip) and prints its semantic
type, UUID, and the provenance action list **without a QIIME 2 install** — handy for
sanity-checking that an artifact is what a downstream step expects.

## Self-Check Before Reporting

- Did primers get trimmed **before** DADA2? If `--p-discard-untrimmed` dropped almost
  everything, the primer sequences are likely wrong.
- Were trunc-lens chosen from the **quality `.qzv`**, and does `denoising-stats.qzv` show
  reasonable merge + non-chimeric retention?
- Is the classifier **version-matched** to the running QIIME 2 release?
- Is `--p-sampling-depth` justified from `table.qzv`, not guessed?
- Did you call `feature-table summarize` (2026.1 = former `summarize_plus`), not a removed
  action name?

## References

- [`references/installation.md`](references/installation.md) — conda env files (2026.1 / 2026.4 rename), `qiime info`, why no pip.
- [`references/import_and_manifest.md`](references/import_and_manifest.md) — manifest formats, single-end/EMP/ITS import.
- [`references/pipeline_steps.md`](references/pipeline_steps.md) — per-step flags, primer sets by region, denoising QC reading.
- [`references/classifiers.md`](references/classifiers.md) — SILVA 138 / Greengenes2 / UNITE, version-matching, train-your-own.
- [`references/version_notes.md`](references/version_notes.md) — 2026.1 release deltas, 2026.4 `qiime2` rename, `summarize` change.

Part of the AlterLab Academic Skills suite.
