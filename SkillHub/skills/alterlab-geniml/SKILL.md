---
name: alterlab-geniml
description: Machine learning on genomic interval data (BED files) with the geniml Python package — region embeddings (Region2Vec), joint region+metadata embeddings (BEDspace/StarSpace), single-cell ATAC-seq embeddings (scEmbed), consensus peak sets / universes (build-universe), tokenization, BEDshift randomization, and BBClient/BEDbase caching. Use when training or using region/cell embeddings, clustering scATAC-seq, building a tokenization universe from BED collections, or any ML/feature-learning task over genomic regions. NOT for plain interval arithmetic (overlap/intersect/merge counts) — that is gtars, not geniml. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(uv:*) Bash(python:*) Bash(geniml:*)
compatibility: No API key required. Runs locally via `uv run python` / the `geniml` CLI; requires the geniml Python package (verified against geniml 0.8.4). Tokenization and universe building also need the external `bedtools` and `uniwig` binaries; BEDspace needs StarSpace.
metadata:
    skill-author: AlterLab
    version: "1.1.0"
---

# Geniml: Genomic Interval Machine Learning

## Overview

Geniml is a Python package for building machine learning models on genomic interval data from BED files. It provides unsupervised methods for learning embeddings of genomic regions, single cells, and metadata labels, enabling similarity searches, clustering, and downstream ML tasks.

## Installation

Verified against **geniml 0.8.4**. Install with uv (prefer `uv run --with` for one-off runs so nothing leaks into the project env):

```bash
uv pip install 'geniml[ml]'        # [ml] pulls torch/gensim; needed for region2vec/scembed
```

scEmbed and scATAC-seq examples also need scanpy: `uv pip install scanpy`. Universe building (`build-universe`) and hard tokenization shell out to external binaries — `uniwig` (coverage tracks) and `bedtools` — so install those separately.

Development version: `uv pip install git+https://github.com/databio/geniml.git`

### Import paths (IMPORTANT — verified gotcha)

geniml's subpackage `__init__.py` files do **not** re-export their internals, so the obvious short imports fail with `ImportError`. Import from the concrete module instead:

| Want | Wrong (fails) | Correct (verified) |
|------|---------------|--------------------|
| Hard tokenization | `from geniml.tokenization import hard_tokenization` | `from geniml.tokenization.main import hard_tokenization_main` |
| Region2Vec (legacy fn) | `from geniml.region2vec import region2vec` | `from geniml.region2vec.main_legacy import region2vec` |
| Region2Vec (model class) | — | `from geniml.region2vec.main import Region2VecExModel` |
| scEmbed | `from geniml.scembed import ScEmbed` | `from geniml.scembed.main import ScEmbed` |
| Token dataset | `from geniml.io import tokenize_cells` (does not exist) | `from geniml.region2vec.utils import Region2VecDataset` |
| Tokenizer | — | `from gtars.tokenizers import Tokenizer` |

Tokenizing cells is handled internally by `ScEmbed` via a `gtars` `Tokenizer`; there is no `geniml.io.tokenize_cells` function.

## Core Capabilities

Geniml provides five primary capabilities, each detailed in dedicated reference files:

### 1. Region2Vec: Genomic Region Embeddings

Train unsupervised embeddings of genomic regions using word2vec-style learning.

**Use for:** Dimensionality reduction of BED files, region similarity analysis, feature vectors for downstream ML.

**Workflow:**
1. Tokenize BED files using a universe reference
2. Train Region2Vec model on tokens
3. Generate embeddings for regions

**Reference:** See `references/region2vec.md` for detailed workflow, parameters, and examples.

### 2. BEDspace: Joint Region and Metadata Embeddings

Train shared embeddings for region sets and metadata labels using StarSpace.

**Use for:** Metadata-aware searches, cross-modal queries (region→label or label→region), joint analysis of genomic content and experimental conditions.

**Workflow:**
1. Preprocess regions and metadata
2. Train BEDspace model
3. Compute distances
4. Query across regions and labels

**Reference:** See `references/bedspace.md` for detailed workflow, search types, and examples.

### 3. scEmbed: Single-Cell Chromatin Accessibility Embeddings

Train Region2Vec models on single-cell ATAC-seq data for cell-level embeddings.

**Use for:** scATAC-seq clustering, cell-type annotation, dimensionality reduction of single cells, integration with scanpy workflows.

**Workflow:**
1. Prepare AnnData with peak coordinates
2. Pre-tokenize cells
3. Train scEmbed model
4. Generate cell embeddings
5. Cluster and visualize with scanpy

**Reference:** See `references/scembed.md` for detailed workflow, parameters, and examples.

### 4. Consensus Peaks: Universe Building

Build reference peak sets (universes) from BED file collections using multiple statistical methods.

**Use for:** Creating tokenization references, standardizing regions across datasets, defining consensus features with statistical rigor.

**Workflow:**
1. Combine BED files
2. Generate coverage tracks
3. Build universe using CC, CCF, ML, or HMM method

**Methods:**
- **CC (Coverage Cutoff)**: Simple threshold-based
- **CCF (Coverage Cutoff Flexible)**: Confidence intervals for boundaries
- **ML (Maximum Likelihood)**: Probabilistic modeling of positions
- **HMM (Hidden Markov Model)**: Complex state modeling

**Reference:** See `references/consensus_peaks.md` for method comparison, parameters, and examples.

### 5. Utilities: Supporting Tools

Additional tools for caching, randomization, evaluation, and search.

**Available utilities:**
- **BBClient**: BED file caching for repeated access
- **BEDshift**: Randomization preserving genomic context
- **Evaluation**: Metrics for embedding quality (silhouette, Davies-Bouldin, etc.)
- **Tokenization**: Region tokenization utilities (hard, soft, universe-based)
- **Text2BedNN**: Neural search backends for genomic queries

**Reference:** See `references/utilities.md` for detailed usage of each utility.

## Common Workflows

### Basic Region Embedding Pipeline

```python
from geniml.tokenization.main import hard_tokenization_main
from geniml.region2vec.main_legacy import region2vec

# Step 1: Tokenize BED files against a universe.
# `fraction` (default 1e-9) is the minimum overlap fraction for a hit — NOT a p-value.
# Requires the `bedtools` binary on PATH.
hard_tokenization_main(
    src_folder='bed_files/',
    dst_folder='tokens/',
    universe_file='universe.bed',
    fraction=1e-9,
)

# Step 2: Train Region2Vec (word2vec-style over the token "sentences")
region2vec(
    token_folder='tokens/',
    save_dir='model/',
    num_shufflings=1000,   # this is also the number of training epochs
    embedding_dim=100,
    context_win_size=5,    # half-window; CLI flag is --context-len
)
```

### scATAC-seq Analysis Pipeline

```python
import scanpy as sc
from geniml.scembed.main import ScEmbed
from geniml.region2vec.utils import Region2VecDataset
from gtars.tokenizers import Tokenizer

# Step 1: Load AnnData. Peaks must live in adata.var with chr/start/end.
adata = sc.read_h5ad('scatac_data.h5ad')

# Step 2: Build a model bound to a universe tokenizer (gtars).
model = ScEmbed(tokenizer=Tokenizer('universe.bed'))

# Step 3: Train on pre-tokenized cells (a parquet of .gtok tokens).
# Embedding size / negative samples are passed via gensim_params, e.g.
# gensim_params={'vector_size': 100, 'negative': 5}
dataset = Region2VecDataset('tokens.parquet', convert_to_str=True)
model.train(dataset, epochs=100, min_count=1)

# Step 4: Generate cell embeddings and store them.
adata.obsm['scembed_X'] = model.encode(adata, pooling='mean')

# Step 5: Cluster with scanpy
sc.pp.neighbors(adata, use_rep='scembed_X')
sc.tl.leiden(adata)
sc.tl.umap(adata)
```

### Universe Building and Evaluation

```bash
# Generate coverage
cat bed_files/*.bed > combined.bed
uniwig -m 25 combined.bed chrom.sizes coverage/

# Build universe with coverage cutoff (top-level command is `build-universe`)
geniml build-universe cc \
  --coverage-folder coverage/ \
  --output-file universe.bed \
  --cutoff 5 \
  --merge 100 \
  --filter-size 50

# Assess universe quality (command is `assess-universe`)
geniml assess-universe --help   # see flags; varies by metric
```

## CLI Reference

Geniml provides command-line interfaces for major operations:

```bash
# Region2Vec training (--context-len is the half-window; there is no --window-size)
geniml region2vec --token-folder tokens/ --save-dir model/ --num-shuffle 1000 --embed-dim 100

# BEDspace preprocessing
geniml bedspace preprocess --input regions/ --metadata labels.csv --universe universe.bed --output preprocessed/

# BEDspace training (StarSpace must be installed separately)
geniml bedspace train --input preprocessed.txt --output model/ --dim 100

# BEDspace search — the query is POSITIONAL (last arg), not a -q flag
geniml bedspace search -t r2l -d distances.pkl -n 10 query.bed

# Universe building (top-level command is `build-universe`; --output-file, not --output)
geniml build-universe cc --coverage-folder coverage/ --output-file universe.bed --cutoff 5

# BEDshift randomization (-b bedfile, -g refgenie genome OR -l chrom sizes; perturbations
# are rates: -d drop, -a add, -s shift, -c cut, -m merge; -r repeat, -o output)
geniml bedshift -b peaks.bed -g hg38 -s 0.3 -r 100 -o randomized.bed
```

## When to Use Which Tool

| You have / want | Tool |
|-----------------|------|
| Bulk region sets (ChIP/ATAC-seq), unsupervised embeddings, no metadata | **Region2Vec** |
| Region sets **plus** metadata labels; cross-modal label↔region search | **BEDspace** |
| scATAC-seq cells to cluster/annotate (scanpy integration) | **scEmbed** |
| A consensus peak set / tokenization reference from many BEDs | **build-universe** |
| Cache remote BEDs, null models, embedding metrics | **Utilities** (BBClient/BEDshift/eval) |
| Plain interval overlap/intersection/merge **counts**, no ML | **gtars** — not geniml |

## Best Practices

### General Guidelines

- **Universe quality is critical**: Invest time in building comprehensive, well-constructed universes
- **Tokenization validation**: Check coverage (>80% ideal) before training
- **Parameter tuning**: Experiment with embedding dimensions, learning rates, and training epochs
- **Evaluation**: Always validate embeddings with multiple metrics and visualizations
- **Documentation**: Record parameters and random seeds for reproducibility

### Performance Considerations

- **Pre-tokenization**: For scEmbed, always pre-tokenize cells for faster training
- **Memory management**: Large datasets may require batch processing or downsampling
- **Computational resources**: ML/HMM universe methods are computationally intensive
- **Model caching**: Use BBClient to avoid repeated downloads

### Integration Patterns

- **With scanpy**: scEmbed embeddings integrate seamlessly as `adata.obsm` entries
- **With BEDbase**: Use BBClient for accessing remote BED repositories
- **With Hugging Face**: Export trained models for sharing and reproducibility
- **With R**: Use reticulate for R integration (see utilities reference)

## Related Projects

Geniml is part of the BEDbase ecosystem:

- **BEDbase**: Unified platform for genomic regions
- **BEDboss**: Processing pipeline for BED files
- **Gtars**: Genomic tools and utilities
- **BBClient**: Client for BEDbase repositories

## Additional Resources

- **Documentation**: https://docs.bedbase.org/geniml/ (also reachable at https://geniml.databio.org)
- **GitHub**: https://github.com/databio/geniml
- **Pre-trained models**: Available on Hugging Face (databio organization)

## Troubleshooting

**`ImportError` on `from geniml.X import ...`:** the subpackage `__init__` doesn't re-export it — import from the concrete module (see the Import paths table above).

**"Tokenization coverage too low":**
- Check universe quality and completeness
- Loosen the overlap `fraction` (e.g. 1e-6 instead of 1e-9) — note this is an overlap fraction, not a p-value
- Ensure universe matches the genome assembly

**"Training not converging":**
- Adjust learning rate (`init_lr` / gensim params, ~0.01-0.05)
- Increase epochs (`num_shufflings` for region2vec; `epochs` for scEmbed)
- Check data quality and preprocessing

**"Out of memory errors":**
- Pre-tokenize cells so training streams tokens rather than the full matrix
- Process data in chunks or downsample
- Reduce `embedding_dim`

**"StarSpace not found" (BEDspace):**
- Install/build StarSpace separately: https://github.com/facebookresearch/StarSpace
- Point `bedspace train`/`distances` at it with `-s` / `--path-to-starsapce` (note: the geniml CLI flag is literally misspelled "starsapce")

For detailed troubleshooting and method-specific issues, consult the appropriate reference file.

