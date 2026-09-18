# scEmbed: Single-Cell Embedding Generation

## Overview

scEmbed trains Region2Vec models on single-cell ATAC-seq datasets to generate cell embeddings for clustering and analysis. It provides an unsupervised machine learning framework for representing and analyzing scATAC-seq data in low-dimensional space.

## When to Use

Use scEmbed when working with:
- Single-cell ATAC-seq (scATAC-seq) data requiring clustering
- Cell-type annotation tasks
- Dimensionality reduction for single-cell chromatin accessibility
- Integration with scanpy workflows for downstream analysis

## Workflow

### Step 1: Data Preparation

Input data must be in AnnData format with `.var` attributes containing `chr`, `start`, and `end` values for peaks.

**Starting from raw data** (barcodes.txt, peaks.bed, matrix.mtx):

```python
import scanpy as sc
import pandas as pd
import scipy.io
import anndata

# Load data
barcodes = pd.read_csv('barcodes.txt', header=None, names=['barcode'])
peaks = pd.read_csv('peaks.bed', sep='\t', header=None,
                    names=['chr', 'start', 'end'])
matrix = scipy.io.mmread('matrix.mtx').tocsr()

# Create AnnData
adata = anndata.AnnData(X=matrix.T, obs=barcodes, var=peaks)
adata.write('scatac_data.h5ad')
```

### Step 2: Build the model with a universe tokenizer

scEmbed tokenizes against a universe using a `gtars` `Tokenizer`. There is no `geniml.io.tokenize_cells` function — pass the tokenizer (or universe path) directly to `ScEmbed`. Pre-tokenized cells are supplied to training as a `Region2VecDataset` over a parquet of `.gtok` tokens:

```python
from geniml.scembed.main import ScEmbed
from geniml.region2vec.utils import Region2VecDataset
from gtars.tokenizers import Tokenizer

# Bind the model to a universe tokenizer
model = ScEmbed(tokenizer=Tokenizer('universe.bed'))
```

**Why pre-tokenize:** faster iterations, lower memory, and reusable token data across runs.

### Step 3: Model Training

Train on the tokenized dataset. Note the **verified** `train` signature — there is no `batch_size`, `learning_rate`, or `negative_samples` argument; gensim hyper-parameters (including embedding size via `vector_size` and `negative`) are passed through `gensim_params`:

```python
# train(dataset, window_size=5, epochs=10, min_count=10, num_cpus=1,
#       seed=42, save_checkpoint_path=None, gensim_params={}, load_from_checkpoint=None)
dataset = Region2VecDataset('tokenized_cells.parquet', convert_to_str=True)

model.train(
    dataset,
    epochs=100,
    window_size=5,
    min_count=1,
    gensim_params={'vector_size': 100, 'negative': 5},
)

# Save / export the trained model (writes checkpoint.pt, config.yaml, universe.bed)
model.export('scembed_model/')
```

### Step 4: Generate Cell Embeddings

Use the trained model to generate embeddings. `from_pretrained` reads an exported folder; the positional `ScEmbed("<hf-repo>")` form loads a Hugging Face model:

```python
from geniml.scembed.main import ScEmbed

# From a local export folder
model = ScEmbed.from_pretrained('scembed_model/')

# encode(regions, pooling=None) -> np.ndarray; pooling is 'mean' or 'max'
adata.obsm['scembed_X'] = model.encode(adata, pooling='mean')
```

### Step 5: Downstream Analysis

Integrate with scanpy for clustering and visualization:

```python
import scanpy as sc

# Use scEmbed embeddings for neighborhood graph
sc.pp.neighbors(adata, use_rep='scembed_X')

# Cluster cells
sc.tl.leiden(adata, resolution=0.5)

# Compute UMAP for visualization
sc.tl.umap(adata)

# Plot results
sc.pl.umap(adata, color='leiden')
```

## Key Parameters

### Training Parameters

`ScEmbed.train` accepts these directly: `window_size`, `epochs`, `min_count`, `num_cpus`, `seed`. Word2vec hyper-parameters go through `gensim_params` (e.g. `vector_size` for embedding dimension, `negative` for negative samples).

| Parameter | Where | Description | Typical Range |
|-----------|-------|-------------|---------------|
| `epochs` | `train(...)` | Training epochs | 50 - 200 |
| `window_size` | `train(...)` | Context window | 3 - 10 |
| `min_count` | `train(...)` | Min token frequency to keep | 1 - 10 |
| `vector_size` | `gensim_params` | Cell embedding dimension | 50 - 200 |
| `negative` | `gensim_params` | Negative samples | 5 - 20 |

### Tokenization

- **Universe file**: reference BED defining the genomic vocabulary; passed as the `gtars` `Tokenizer` the model is built with.

## Pre-trained Models

Pre-trained region2vec/scEmbed models are published on Hugging Face under the `databio` organization. Pass the repo id positionally to load it from the Hub (this sets `model_path` and marks the model trained):

```python
from geniml.scembed.main import ScEmbed

# Positional arg = Hugging Face repo id (browse the `databio` org for the right one
# for your assembly/reference, e.g. an hg38 ChIP-atlas region2vec model)
model = ScEmbed('databio/r2v-ChIP-atlas-hg38-v2')

embeddings = model.encode(adata, pooling='mean')
```

## Best Practices

- **Data quality**: Use filtered peak-barcode matrices, not raw counts
- **Pre-tokenization**: Always pre-tokenize to improve training efficiency
- **Parameter tuning**: Adjust `embedding_dim` and training epochs based on dataset size
- **Validation**: Use known cell-type markers to validate clustering quality
- **Integration**: Combine with scanpy for comprehensive single-cell analysis
- **Model sharing**: Export trained models to Hugging Face for reproducibility

## Example Dataset

The 10x Genomics PBMC 10k dataset (10,000 peripheral blood mononuclear cells) serves as a standard benchmark:
- Contains diverse immune cell types
- Well-characterized cell populations
- Available from 10x Genomics website

## Cell-Type Annotation

After clustering, annotate cell types by transferring labels in the embedding space — e.g. a standard scikit-learn KNN classifier trained on a reference's `adata.obsm['scembed_X']` and applied to the query's embeddings, or scanpy's `sc.tl.ingest`. (geniml ships annotation helpers under `geniml.scembed.annotation`; check that module's current API before relying on a specific function name.)

## Output

scEmbed produces:
- Low-dimensional cell embeddings (stored in `adata.obsm`)
- Trained model files for reuse
- Compatible format for scanpy downstream analysis
- Optional export to Hugging Face for sharing
