---
name: alterlab-gtars
description: Runs high-performance genomic interval analysis with gtars (databio), a Rust toolkit with Python bindings — the performance-critical backend for the geniml ML library. Use when computing overlaps/jaccard/coverage between BED region sets, indexing intervals with IGD, generating uniwig accumulation/coverage tracks, tokenizing genomic regions for ML, splitting single-cell fragments into pseudobulks, or computing GA4GH refget sequence digests. NOT for training region embeddings (use alterlab-geniml) or non-genomic spatial joins (use alterlab-geopandas). Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read, Write, Edit, Bash
compatibility: No API key required. Python API runs locally via `uv run python` with the `gtars` package (PyPI, v0.8). The CLI is a separate Rust binary (`gtars-cli`, install via cargo).
metadata:
    skill-author: AlterLab
    version: "1.1.0"
---

# Gtars: Genomic Tools and Algorithms in Rust

## Overview

Gtars (from databio, the lab behind `geniml`) is a high-performance Rust toolkit for manipulating, analyzing, and processing genomic interval data. Its primary purpose is to be the performance-critical backend for `geniml`, a Python library for machine learning on genomic intervals. It provides overlap/set operations, IGD overlap indexing, coverage (uniwig) tracks, region tokenization for ML, single-cell fragment pseudobulking, and GA4GH refget sequence-collection management.

Use this skill when working with:
- Genomic interval files (BED) — overlaps, jaccard, set ops, coverage
- IGD indexing for fast overlap queries over large interval databases
- Coverage / accumulation tracks via uniwig
- Genomic ML preprocessing and region tokenization
- Single-cell fragment files (split into pseudobulks by cluster)
- Reference sequence digests and retrieval (refget)

> Version note: examples are verified against the **`gtars` Python package v0.8** (PyPI). The Python API is exposed through submodules — `gtars.models`, `gtars.tokenizers`, `gtars.refget`, `gtars.utils` — NOT as flat top-level functions. There is no `gtars.igd` or `gtars.uniwig` Python submodule; IGD building and uniwig track generation are CLI-only.

## Installation

### Python package

```bash
uv pip install gtars   # or: uv add gtars
```

Import surface (verified, v0.8):

```python
from gtars.models import RegionSet, Region, RegionSetList
from gtars.tokenizers import Tokenizer, tokenize_fragment_file
from gtars import refget          # RefgetStore, digest_fasta, sha512t24u_digest, ...
from gtars import utils           # read/write .gtok token files
```

### CLI (separate Rust binary)

The CLI ships as the `gtars-cli` crate (binary name `gtars`) and is installed with Cargo. Most subcommands are behind feature flags:

```bash
# All commonly used commands
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit genomicdist"

# Or a subset
cargo install gtars-cli --features "uniwig igd"
```

Available CLI subcommands: `igd`, `overlaprs`, `uniwig`, `bbcache`, `pb` (fragment pseudobulking), `scoring`, `genomicdist`, `ranges`, `consensus`, `prep`. Flag sets differ per subcommand and evolve across versions — always confirm with `gtars <command> --help`.

## Core Capabilities

Gtars is organized into specialized modules, each focused on specific genomic analysis tasks:

### 1. Overlap Detection and Set Operations

Detect overlaps and compute set operations / similarity between region sets with `RegionSet` (Python), or index a large interval database with IGD (CLI).

**When to use:**
- Finding overlapping regulatory elements, comparing ChIP-seq peaks
- Variant annotation; identifying shared genomic features
- Jaccard / overlap-coefficient similarity between BED files

**Quick example (Python):**
```python
from gtars.models import RegionSet

peaks = RegionSet("chip_peaks.bed")
promoters = RegionSet("promoters.bed")

# Regions in peaks that overlap a promoter (the real method is subset_by_overlaps)
in_promoters = peaks.subset_by_overlaps(promoters)
in_promoters.to_bed("peaks_in_promoters.bed")

print(peaks.count_overlaps(promoters))  # per-region overlap counts
print(peaks.jaccard(promoters))         # similarity score
```

For querying a large reference database many times, build an IGD index once via the CLI (`gtars igd create ...`) and search it (`gtars igd search ...`). See `references/overlap.md`.

### 2. Coverage / Accumulation Tracks (uniwig, CLI)

Generate coverage / accumulation tracks from a BED or BAM file with the uniwig CLI subcommand.

**When to use:**
- ATAC-seq accessibility profiles, ChIP-seq coverage, RNA-seq read coverage

**Quick example (CLI):**
```bash
# uniwig reads a sorted BED/BAM and writes accumulation tracks.
# Flags differ by version; confirm with `gtars uniwig --help`.
gtars uniwig --file fragments.bed --filetype bed \
             --fileheader coverage --outputtype bw
```

See `references/coverage.md` for verified flags and `RegionSet.coverage()` for an in-memory alternative.

### 3. Genomic Tokenization

Convert genomic regions into discrete tokens for ML (the preprocessing layer `geniml` builds on).

**When to use:**
- Preprocessing peaks/regions into a fixed vocabulary for genomic ML models
- Feeding token IDs to geniml or custom transformer models

**Quick example (Python):**
```python
from gtars.tokenizers import Tokenizer
from gtars.models import Region

tokenizer = Tokenizer.from_bed("universe.bed")   # vocab = the universe BED
tokens = tokenizer.tokenize([Region("chr1", 1000, 2000, None)])  # -> ['chr1:1000-2000']
ids = tokenizer.convert_tokens_to_ids(tokens)                     # -> [<int>]
```

See `references/tokenizers.md`. Note: the class is `Tokenizer` (there is no `TreeTokenizer`).

### 4. Reference Sequence Management (refget)

Compute GA4GH refget digests and manage/retrieve reference sequences.

**When to use:**
- Validating reference genome integrity via sequence digests
- Building a local sequence-collection store and extracting subsequences

**Quick example (Python):**
```python
from gtars import refget

# Digest a FASTA into a GA4GH SequenceCollection (no sequence data loaded)
collection = refget.digest_fasta("hg38.fa")

# Or a one-off sequence digest
d = refget.sha512t24u_digest("ACGTACGT")   # 'GS_...'-style truncated SHA-512/24
```

See `references/refget.md` for `RefgetStore` (load, store, and `get_substring`).

### 5. Fragment Pseudobulking (pb, CLI)

Split a single-cell fragment file into pseudobulks based on a cluster/cell-group mapping.

**When to use:**
- Processing single-cell ATAC-seq; cluster-based fragment aggregation

**Quick example (CLI):**
```bash
# The fragsplit feature exposes the `pb` (pseudobulk) subcommand.
gtars pb --fragments fragments.bed.gz --mapping cluster_mapping.tsv
```

The Python side also offers `gtars.tokenizers.tokenize_fragment_file(...)` for tokenizing fragments directly. See `references/cli.md`.

### 6. Fragment / Region Scoring

Score region/fragment files against reference datasets with the `scoring` CLI subcommand.

**When to use:**
- Evaluating enrichment of regions against a reference universe
- Batch quality-metric computation across samples

```bash
gtars scoring --help   # confirm subcommands and flags for your installed version
```

## Common Workflows

### Workflow 1: Peak Overlap Analysis

Identify peaks overlapping promoters (Python):

```python
from gtars.models import RegionSet

peaks = RegionSet("chip_peaks.bed")
promoters = RegionSet("promoters.bed")

overlapping_peaks = peaks.subset_by_overlaps(promoters)
overlapping_peaks.to_bed("peaks_in_promoters.bed")

# Iterate results (regions expose .chr/.start/.end)
for r in overlapping_peaks:
    print(r.chr, r.start, r.end)
```

### Workflow 2: IGD index + repeated overlap queries (CLI)

Index a large reference database once, then search it many times:

```bash
# Build the IGD database from a directory or list of BED files
gtars igd create --help     # confirm the exact input/output flags for your version

# Search the database with query regions
gtars igd search --help
```

### Workflow 3: ML Preprocessing (tokenization)

Prepare genomic regions for an ML model:

```python
from gtars.tokenizers import Tokenizer
from gtars.models import RegionSet

# Step 1: Build a tokenizer from the universe BED (defines the vocabulary)
tokenizer = Tokenizer.from_bed("universe.bed")

# Step 2: Tokenize a region set (tokenize accepts a RegionSet or a list of Region)
regions = RegionSet("training_peaks.bed")
tokens = tokenizer.tokenize(regions)                      # list of 'chr:start-end' strings
ids = tokenizer.convert_tokens_to_ids(tokens)             # integer IDs for the model

# Step 3: feed `ids` to geniml or a custom model (see alterlab-geniml for training)
```

## Python vs CLI Usage

**Use Python API when:**
- Integrating with analysis pipelines
- Need programmatic control
- Working with NumPy/Pandas
- Building custom workflows

**Use CLI when:**
- Quick one-off analyses
- Shell scripting
- Batch processing files
- Prototyping workflows

## Reference Documentation

- **`references/python-api.md`** — `RegionSet` / `Region` operations, set ops, overlaps, export
- **`references/overlap.md`** — overlap detection and IGD indexing
- **`references/coverage.md`** — uniwig coverage tracks
- **`references/tokenizers.md`** — region tokenization for ML
- **`references/refget.md`** — refget digests and `RefgetStore`
- **`references/cli.md`** — CLI subcommand overview

## Relationship to geniml

gtars is the Rust performance backend for `geniml` (databio's ML-on-genomic-intervals library). Use gtars for the heavy interval ops and tokenization; use `geniml` (skill `alterlab-geniml`) for embedding/model training built on top of those tokens.

## Data Formats

- **BED**: genomic intervals (3-column or extended) — the core input
- **BigWig / WIG**: coverage / accumulation tracks (uniwig output)
- **FASTA**: reference sequences (refget)
- **Fragment files**: single-cell fragments (often `.bed.gz`), with a separate cluster-mapping file for `pb`

## Verifying the API

This package's surface differs between releases and the Python and CLI APIs are NOT mirror images. Before relying on an unfamiliar method or flag, confirm against the installed version:

```bash
uv run python -c "from gtars import models, tokenizers, refget; print(dir(models), dir(tokenizers), dir(refget))"
gtars <command> --help
```

