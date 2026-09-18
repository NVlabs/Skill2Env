---
name: alterlab-anndata
description: Build, slice, concatenate, read, and write AnnData annotated data matrices (obs, var, X, layers, obsm, uns) — the scverse data STRUCTURE, not an analysis pipeline. Use when creating or wrangling .h5ad/zarr files, managing cell and gene annotations, concatenating batches, or handling layers/obsm/backed-mode; for the QC, normalization, clustering, UMAP, and differential-expression analysis pipeline prefer alterlab-scanpy instead, and for RNA velocity from spliced/unspliced layers prefer alterlab-scvelo instead. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs under `uv run python` with `anndata` (>=0.11) installed in the project env; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# AnnData

## Overview

AnnData is a Python package for handling annotated data matrices, storing experimental measurements (X) alongside observation metadata (obs), variable metadata (var), and multi-dimensional annotations (obsm, varm, obsp, varp, uns). Originally designed for single-cell genomics through Scanpy, it now serves as a general-purpose framework for any annotated data requiring efficient storage, manipulation, and analysis.

## When to Use This Skill

Use this skill when:
- Creating, reading, or writing AnnData objects
- Working with h5ad, zarr, or other genomics data formats
- Performing single-cell RNA-seq analysis
- Managing large datasets with sparse matrices or backed mode
- Concatenating multiple datasets or experimental batches
- Subsetting, filtering, or transforming annotated data
- Integrating with scanpy, scvi-tools, or other scverse ecosystem tools

## Installation

```bash
uv pip install anndata          # 0.11+ (the API namespaces below assume >= 0.11)

# Optional extra for Dask-backed lazy reads (ad.experimental.read_lazy)
uv pip install 'anndata[dask]'
```

## Quick Start

### Creating an AnnData object
```python
import anndata as ad
import numpy as np
import pandas as pd

# Minimal creation
X = np.random.rand(100, 2000)  # 100 cells × 2000 genes
adata = ad.AnnData(X)

# With metadata
obs = pd.DataFrame({
    'cell_type': ['T cell', 'B cell'] * 50,
    'sample': ['A', 'B'] * 50
}, index=[f'cell_{i}' for i in range(100)])

var = pd.DataFrame({
    'gene_name': [f'Gene_{i}' for i in range(2000)]
}, index=[f'ENSG{i:05d}' for i in range(2000)])

adata = ad.AnnData(X=X, obs=obs, var=var)
```

### Reading data
```python
import scanpy as sc  # 10x readers live in scanpy, not anndata

# Read h5ad file
adata = ad.read_h5ad('data.h5ad')

# Read with backed mode (for large files)
adata = ad.read_h5ad('large_data.h5ad', backed='r')

# Read other formats (these live under ad.io as of anndata 0.11)
adata = ad.io.read_csv('data.csv')
adata = ad.io.read_loom('data.loom')
adata = sc.read_10x_h5('filtered_feature_bc_matrix.h5')
```

> **API namespaces (anndata >= 0.11)**: all format readers/writers moved to the
> `anndata.io` module (`ad.io.read_csv`, `ad.io.read_mtx`, `ad.io.read_loom`,
> `ad.io.read_elem`, ...). The top-level `ad.read_csv`-style aliases still work
> but emit a `DeprecationWarning`. **Exceptions**: `ad.read_h5ad`, `ad.read_zarr`,
> `adata.write_h5ad`, and `adata.write_zarr` stay top-level with no warning.
>
> **10x readers** (`read_10x_h5`, `read_10x_mtx`) live in **scanpy**
> (`sc.read_10x_h5`), not anndata — this skill defers analysis-specific I/O to scanpy.

### Writing data
```python
# Write h5ad file
adata.write_h5ad('output.h5ad')

# Write with compression
adata.write_h5ad('output.h5ad', compression='gzip')

# Write other formats
adata.write_zarr('output.zarr')
adata.write_csvs('output_dir/')
```

### Basic operations
```python
# Subset by conditions
t_cells = adata[adata.obs['cell_type'] == 'T cell']

# Subset by indices
subset = adata[0:50, 0:100]

# Add metadata
adata.obs['quality_score'] = np.random.rand(adata.n_obs)
adata.var['highly_variable'] = np.random.rand(adata.n_vars) > 0.8

# Access dimensions
print(f"{adata.n_obs} observations × {adata.n_vars} variables")
```

## Core Capabilities

### 1. Data Structure

Understand the AnnData object structure including X, obs, var, layers, obsm, varm, obsp, varp, uns, and raw components.

**See**: `references/data_structure.md` for comprehensive information on:
- Core components (X, obs, var, layers, obsm, varm, obsp, varp, uns, raw)
- Creating AnnData objects from various sources
- Accessing and manipulating data components
- Memory-efficient practices

### 2. Input/Output Operations

Read and write data in various formats with support for compression, backed mode, and cloud storage.

**See**: `references/io_operations.md` for details on:
- Native formats (h5ad, zarr)
- Alternative formats (CSV, MTX, Loom, 10X, Excel)
- Backed mode for large datasets
- Remote data access
- Format conversion
- Performance optimization

Common commands:
```python
# Read/write h5ad
adata = ad.read_h5ad('data.h5ad', backed='r')
adata.write_h5ad('output.h5ad', compression='gzip')

# Read 10X data (10x readers live in scanpy, not anndata)
import scanpy as sc
adata = sc.read_10x_h5('filtered_feature_bc_matrix.h5')

# Read MTX format (.mtx is variables x observations; transpose so cells are rows)
adata = ad.io.read_mtx('matrix.mtx').T
```

### 3. Concatenation

Combine multiple AnnData objects along observations or variables with flexible join strategies.

**See**: `references/concatenation.md` for comprehensive coverage of:
- Basic concatenation (axis=0 for observations, axis=1 for variables)
- Join types (inner, outer)
- Merge strategies (same, unique, first, only)
- Tracking data sources with labels
- Lazy concatenation (AnnCollection)
- On-disk concatenation for large datasets

Common commands:
```python
# Concatenate observations (combine samples)
adata = ad.concat(
    [adata1, adata2, adata3],
    axis=0,
    join='inner',
    label='batch',
    keys=['batch1', 'batch2', 'batch3']
)

# Concatenate variables (combine modalities)
adata = ad.concat([adata_rna, adata_protein], axis=1)

# Lazy concatenation
from anndata.experimental import AnnCollection
collection = AnnCollection(
    ['data1.h5ad', 'data2.h5ad'],
    join_obs='outer',
    label='dataset'
)
```

### 4. Data Manipulation

Transform, subset, filter, and reorganize data efficiently.

**See**: `references/manipulation.md` for detailed guidance on:
- Subsetting (by indices, names, boolean masks, metadata conditions)
- Transposition
- Copying (full copies vs views)
- Renaming (observations, variables, categories)
- Type conversions (strings to categoricals, sparse/dense)
- Adding/removing data components
- Reordering
- Quality control filtering

Common commands:
```python
# Subset by metadata
filtered = adata[adata.obs['quality_score'] > 0.8]
hv_genes = adata[:, adata.var['highly_variable']]

# Transpose
adata_T = adata.T

# Copy vs view
view = adata[0:100, :]  # View (lightweight reference)
copy = adata[0:100, :].copy()  # Independent copy

# Convert strings to categoricals
adata.strings_to_categoricals()
```

### 5. Best Practices

Follow recommended patterns for memory efficiency, performance, and reproducibility.

**See**: `references/best_practices.md` for guidelines on:
- Memory management (sparse matrices, categoricals, backed mode)
- Views vs copies
- Data storage optimization
- Performance optimization
- Working with raw data
- Metadata management
- Reproducibility
- Error handling
- Integration with other tools
- Common pitfalls and solutions

Key recommendations:
```python
# Use sparse matrices for sparse data
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)

# Convert strings to categoricals
adata.strings_to_categoricals()

# Use backed mode for large files
adata = ad.read_h5ad('large.h5ad', backed='r')

# Store raw before filtering
adata.raw = adata.copy()
adata = adata[:, adata.var['highly_variable']]
```

## Integration with Scverse Ecosystem

AnnData serves as the foundational data structure for the scverse ecosystem:

### Scanpy (Single-cell analysis)
AnnData is scanpy's native object — once built/loaded, pass it straight in.
Preprocessing, dimensionality reduction, clustering, and plotting
(`sc.pp.normalize_total`, `sc.pp.highly_variable_genes`, `sc.pp.pca`,
`sc.pp.neighbors`, `sc.tl.umap`, `sc.tl.leiden`, `sc.pl.*`) are **scanpy's
job, not anndata's** — defer the analysis workflow there.
```python
import scanpy as sc

sc.pp.filter_cells(adata, min_genes=200)  # scanpy mutates the AnnData in place
# ... continue the analysis pipeline in scanpy
```

### Muon (Multimodal data)
```python
import muon as mu

# Combine RNA and protein data
mdata = mu.MuData({'rna': adata_rna, 'protein': adata_protein})
```

### PyTorch integration
```python
from anndata.experimental import AnnLoader

# Create DataLoader for deep learning (also accepts an AnnCollection)
dataloader = AnnLoader(adata, batch_size=128, shuffle=True)

for batch in dataloader:
    X = batch["X"]      # dict-style access; tensors, not attributes
    labels = batch["obs"]["cell_type"]
    # Train model
```

## Common Workflows

### Single-cell data lifecycle (the anndata-owned parts)
Load, compute simple QC metrics on `obs`/`var`, snapshot `raw`, subset, and write.
The normalize/log1p/HVG/cluster steps belong to scanpy — hand off there.
```python
import anndata as ad
import scanpy as sc

# 1. Load (10x readers live in scanpy)
adata = sc.read_10x_h5('filtered_feature_bc_matrix.h5')

# 2. Quick QC metrics on obs/var, then mask-subset (pure anndata wrangling)
adata.obs['n_genes'] = (adata.X > 0).sum(axis=1)
adata.obs['n_counts'] = adata.X.sum(axis=1)
adata = adata[(adata.obs['n_genes'] > 200) & (adata.obs['n_counts'] < 50000)].copy()

# 3. Snapshot raw before any gene filtering
adata.raw = adata.copy()

# 4. Hand off normalization / HVG / clustering to scanpy, then come back:
#    sc.pp.normalize_total / sc.pp.log1p / sc.pp.highly_variable_genes / ...
adata = adata[:, adata.var['highly_variable']].copy()  # subset is anndata's job

# 5. Save processed data
adata.write_h5ad('processed.h5ad', compression='gzip')
```

### Batch integration (concatenate, then defer correction)
```python
# Load and concatenate batches with source labels — this is anndata's job
adatas = [ad.read_h5ad(p) for p in ['batch1.h5ad', 'batch2.h5ad', 'batch3.h5ad']]
adata = ad.concat(
    adatas,
    label='batch',
    keys=['batch1', 'batch2', 'batch3'],
    join='inner',
)

# Batch correction and downstream analysis (combat / pca / neighbors / umap)
# are scanpy territory — pass `adata` to scanpy from here.
```

### Working with large datasets
```python
# Open in backed mode
adata = ad.read_h5ad('100GB_dataset.h5ad', backed='r')

# Filter based on metadata (no data loading)
high_quality = adata[adata.obs['quality_score'] > 0.8]

# Load filtered subset
adata_subset = high_quality.to_memory()

# Process subset
process(adata_subset)

# Or process in chunks
chunk_size = 1000
for i in range(0, adata.n_obs, chunk_size):
    chunk = adata[i:i+chunk_size, :].to_memory()
    process(chunk)
```

## Troubleshooting

### Out of memory errors
Use backed mode or convert to sparse matrices:
```python
# Backed mode
adata = ad.read_h5ad('file.h5ad', backed='r')

# Sparse matrices
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)
```

### Slow file reading
Use compression and appropriate formats:
```python
# Optimize for storage
adata.strings_to_categoricals()
adata.write_h5ad('file.h5ad', compression='gzip')

# Use Zarr for cloud storage
adata.write_zarr('file.zarr', chunks=(1000, 1000))
```

### Index alignment issues
Always align external data on index:
```python
# Wrong
adata.obs['new_col'] = external_data['values']

# Correct
adata.obs['new_col'] = external_data.set_index('cell_id').loc[adata.obs_names, 'values']
```

## Additional Resources

- **Official documentation**: https://anndata.readthedocs.io/
- **Scanpy tutorials**: https://scanpy.readthedocs.io/
- **Scverse ecosystem**: https://scverse.org/
- **GitHub repository**: https://github.com/scverse/anndata

