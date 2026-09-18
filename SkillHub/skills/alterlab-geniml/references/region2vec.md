# Region2Vec: Genomic Region Embeddings

## Overview

Region2Vec generates unsupervised embeddings of genomic regions and region sets from BED files. It maps genomic regions to a vocabulary, creates sentences through concatenation, and applies word2vec training to learn meaningful representations.

## When to Use

Use Region2Vec when working with:
- BED file collections requiring dimensionality reduction
- Genomic region similarity analysis
- Downstream ML tasks requiring region feature vectors
- Comparative analysis across multiple genomic datasets

## Workflow

### Step 1: Prepare Data

Gather BED files in a source folder. Optionally specify a file list (default uses all files in the directory). Prepare a universe file as the reference vocabulary for tokenization.

### Step 2: Tokenization

Run hard tokenization to convert genomic regions into tokens. The function is `hard_tokenization_main` (the short `hard_tokenization` alias is commented out in the package and does not import). It shells out to the `bedtools` binary, which must be on PATH:

```python
from geniml.tokenization.main import hard_tokenization_main

src_folder = '/path/to/raw/bed/files'
dst_folder = '/path/to/tokenized_files'
universe_file = '/path/to/universe_file.bed'

hard_tokenization_main(src_folder, dst_folder, universe_file, fraction=1e-9)
```

The `fraction` parameter (default 1e-9) is the **minimum overlap fraction** required to assign a region to a universe token — it is NOT a p-value.

### Step 3: Train Region2Vec Model

Execute Region2Vec training on the tokenized files. Import the legacy training function from its concrete module:

```python
from geniml.region2vec.main_legacy import region2vec

region2vec(
    token_folder=dst_folder,
    save_dir='./region2vec_model',
    num_shufflings=1000,      # also the number of training epochs
    embedding_dim=100,
    context_win_size=5,       # half-window size
    init_lr=0.025,
    neg_samples=5,
    train_alg='cbow',         # or 'skip-gram'
)
```

For the newer object-oriented API, use `Region2VecExModel` from `geniml.region2vec.main` (`.train(dataset, ...)`, `.encode(...)`, `.export(...)`), mirroring the scEmbed pattern.

## Key Parameters (legacy `region2vec` function)

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `init_lr` | Initial learning rate | 0.01 - 0.05 |
| `context_win_size` | Context half-window | 3 - 10 |
| `num_shufflings` | Shuffling iterations / epochs | 500 - 2000 |
| `embedding_dim` | Output embedding dimension | 50 - 300 |
| `neg_samples` | Negative samples | 5 - 20 |
| `train_alg` | `cbow` or `skip-gram` | — |

## CLI Usage

The CLI exposes the context window as `--context-len` (half-window). There is no `--window-size` flag.

```bash
geniml region2vec --token-folder /path/to/tokens \
  --save-dir ./region2vec_model \
  --num-shuffle 1000 \
  --embed-dim 100 \
  --context-len 5 \
  --neg-samples 5 \
  --init-lr 0.025
```

## Best Practices

- **Parameter tuning**: Tune `init_lr`, `context_win_size`, `num_shufflings`, and `embedding_dim` for your dataset
- **Universe file**: Use a comprehensive universe file that covers all regions of interest in your analysis
- **Validation**: Always validate tokenization output before proceeding to training
- **Resources**: Training can be computationally intensive; monitor memory usage with large datasets

## Output

The trained model saves embeddings that can be used for:
- Similarity searches across genomic regions
- Clustering region sets
- Feature vectors for downstream ML tasks
- Visualization via dimensionality reduction (t-SNE, UMAP)
