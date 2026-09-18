# Input/Output Operations

AnnData provides comprehensive I/O functionality for reading and writing data in various formats.

> **Namespaces (anndata >= 0.11):** all format readers/writers live in the
> `anndata.io` module — use `ad.io.read_csv`, `ad.io.read_mtx`, `ad.io.read_loom`,
> `ad.io.read_elem`, etc. The old top-level `ad.read_csv`-style names still work
> but warn. **Exceptions that stay top-level without a warning:** `ad.read_h5ad`,
> `ad.read_zarr`, `adata.write_h5ad`, `adata.write_zarr`.

## Native Formats

### H5AD (HDF5-based)
The recommended native format for AnnData objects, providing efficient storage and fast access.

#### Writing H5AD files
```python
import anndata as ad

# Write to file
adata.write_h5ad('data.h5ad')

# Write with compression
adata.write_h5ad('data.h5ad', compression='gzip')

# Write with specific compression level (0-9, higher = more compression)
adata.write_h5ad('data.h5ad', compression='gzip', compression_opts=9)
```

#### Reading H5AD files
```python
# Read entire file into memory
adata = ad.read_h5ad('data.h5ad')

# Read in backed mode (lazy loading for large files)
adata = ad.read_h5ad('data.h5ad', backed='r')  # Read-only
adata = ad.read_h5ad('data.h5ad', backed='r+')  # Read-write

# Backed mode enables working with datasets larger than RAM
# Only accessed data is loaded into memory
```

#### Backed mode operations
```python
# Open in backed mode
adata = ad.read_h5ad('large_dataset.h5ad', backed='r')

# Access metadata without loading X into memory
print(adata.obs.head())
print(adata.var.head())

# Subset operations create views
subset = adata[:100, :500]  # View, no data loaded

# Load specific data into memory
X_subset = subset.X[:]  # Now loads this subset

# Convert entire backed object to memory
adata_memory = adata.to_memory()
```

### Zarr
Hierarchical array storage format, optimized for cloud storage and parallel I/O.

#### Writing Zarr
```python
# Write to Zarr store
adata.write_zarr('data.zarr')

# Write with specific chunks (important for performance)
adata.write_zarr('data.zarr', chunks=(100, 100))
```

#### Reading Zarr
```python
# Read Zarr store
adata = ad.read_zarr('data.zarr')
```

#### Remote Zarr access
```python
import fsspec

# Access Zarr from S3
store = fsspec.get_mapper('s3://bucket-name/data.zarr')
adata = ad.read_zarr(store)

# Access Zarr from URL
store = fsspec.get_mapper('https://example.com/data.zarr')
adata = ad.read_zarr(store)
```

## Alternative Input Formats

### CSV/TSV
```python
# Read CSV (genes as columns, cells as rows)
adata = ad.io.read_csv('data.csv')

# Read with custom delimiter
adata = ad.io.read_csv('data.tsv', delimiter='\t')

# Specify that first column is row names
adata = ad.io.read_csv('data.csv', first_column_names=True)
```

### Excel
```python
# Read Excel file
adata = ad.io.read_excel('data.xlsx')

# Read specific sheet
adata = ad.io.read_excel('data.xlsx', sheet='Sheet1')
```

### Matrix Market (MTX)
Common format for sparse matrices in genomics. `.mtx` stores variables x
observations; `read_mtx` does NOT transpose for you, so verify orientation.

```python
# Read MTX (just the matrix)
adata = ad.io.read_mtx('matrix.mtx')

# MTX often has genes as rows — transpose so cells are observations
adata = adata.T
```

### 10X Genomics formats
The 10x readers (`read_10x_h5`, `read_10x_mtx`) live in **scanpy**, not anndata. They return a standard AnnData object.
```python
import scanpy as sc

# Read 10X h5 format
adata = sc.read_10x_h5('filtered_feature_bc_matrix.h5')

# Read 10X MTX directory
adata = sc.read_10x_mtx('filtered_feature_bc_matrix/')

# Specify genome if multiple present
adata = sc.read_10x_h5('data.h5', genome='GRCh38')
```

### Loom
```python
# Read Loom file
adata = ad.io.read_loom('data.loom')

# Read with specific observation and variable annotations
adata = ad.io.read_loom(
    'data.loom',
    obs_names='CellID',
    var_names='Gene'
)
```

### Text files
```python
# Read generic text file
adata = ad.io.read_text('data.txt', delimiter='\t')

# Read with custom parameters
adata = ad.io.read_text(
    'data.txt',
    delimiter=',',
    first_column_names=True,
    dtype='float32'
)
```

### UMI tools
```python
# Read UMI tools format
adata = ad.io.read_umi_tools('counts.tsv')
```

### HDF5 (generic)
```python
# Read from HDF5 file (not h5ad format)
adata = ad.io.read_hdf('data.h5', key='dataset')
```

## Alternative Output Formats

### CSV
```python
# Write to CSV files (creates multiple files)
adata.write_csvs('output_dir/')

# This creates:
# - output_dir/X.csv (expression matrix)
# - output_dir/obs.csv (observation annotations)
# - output_dir/var.csv (variable annotations)
# - output_dir/uns.csv (unstructured annotations, if possible)

# Skip certain components
adata.write_csvs('output_dir/', skip_data=True)  # Skip X matrix
```

### Loom
```python
# Write to Loom format
adata.write_loom('output.loom')
```

## Reading/Writing Specific Elements

For fine-grained control, read or write individual elements (an obs DataFrame, a
sparse matrix, a layer) without constructing a full AnnData. The element API
takes an **open** h5py/zarr group and an in-group path — not a filesystem path
string. Lives under `ad.io`.

```python
import anndata as ad
import h5py

# Read just observation annotations (pass the open group element)
with h5py.File('data.h5ad', 'r') as f:
    obs = ad.io.read_elem(f['obs'])
    layer = ad.io.read_elem(f['layers/normalized'])

# Write an element into an existing file
with h5py.File('data.h5ad', 'a') as f:
    ad.io.write_elem(f, 'layers/new_layer', adata.X.copy())
```

## Lazy Operations

For very large datasets, open the whole store lazily so array data is backed by
Dask and annotation frames by xarray — nothing is read until accessed. Pass an
open h5py file (you manage its lifetime):

```python
import anndata as ad
import h5py

f = h5py.File('large_data.h5ad', 'r')
adata = ad.experimental.read_lazy(f)

print(type(adata.X))   # dask.array.core.Array
# Compute only the slice you need
subset = adata.X[:100, :100].compute()
```

## Common I/O Patterns

### Convert between formats
```python
# MTX to H5AD
adata = ad.io.read_mtx('matrix.mtx').T
adata.write_h5ad('data.h5ad')

# CSV to H5AD
adata = ad.io.read_csv('data.csv')
adata.write_h5ad('data.h5ad')

# H5AD to Zarr
adata = ad.read_h5ad('data.h5ad')
adata.write_zarr('data.zarr')
```

### Load metadata without data
```python
# Backed mode allows inspecting metadata without loading X
adata = ad.read_h5ad('large_file.h5ad', backed='r')
print(f"Dataset contains {adata.n_obs} observations and {adata.n_vars} variables")
print(adata.obs.columns)
print(adata.var.columns)
# X is not loaded into memory
```

### Append to existing file
```python
# Open in read-write mode
adata = ad.read_h5ad('data.h5ad', backed='r+')

# Modify metadata
adata.obs['new_column'] = values

# Changes are written to disk
```

### Download from URL
```python
import anndata as ad

# Read directly from URL (for h5ad files)
url = 'https://example.com/data.h5ad'
adata = ad.read_h5ad(url, backed='r')  # Streaming access

# For other formats, download first
import urllib.request
urllib.request.urlretrieve(url, 'local_file.h5ad')
adata = ad.read_h5ad('local_file.h5ad')
```

## Performance Tips

### Reading
- Use `backed='r'` for large files you only need to query
- Use `backed='r+'` if you need to modify metadata without loading all data
- H5AD format is generally fastest for random access
- Zarr is better for cloud storage and parallel access
- Consider compression for storage, but note it may slow down reading

### Writing
- Use compression for long-term storage: `compression='gzip'` or `compression='lzf'`
- LZF compression is faster but compresses less than GZIP
- For Zarr, tune chunk sizes based on access patterns:
  - Larger chunks for sequential reads
  - Smaller chunks for random access
- Convert string columns to categorical before writing (smaller files)

### Memory management
```python
# Convert strings to categoricals (reduces file size and memory)
adata.strings_to_categoricals()
adata.write_h5ad('data.h5ad')

# Use sparse matrices for sparse data
from scipy.sparse import csr_matrix
if isinstance(adata.X, np.ndarray):
    density = np.count_nonzero(adata.X) / adata.X.size
    if density < 0.5:  # If more than 50% zeros
        adata.X = csr_matrix(adata.X)
```

## Handling Large Datasets

### Strategy 1: Backed mode
```python
# Work with dataset larger than RAM
adata = ad.read_h5ad('100GB_file.h5ad', backed='r')

# Filter based on metadata (fast, no data loading)
filtered = adata[adata.obs['quality_score'] > 0.8]

# Load filtered subset into memory
adata_memory = filtered.to_memory()
```

### Strategy 2: Chunked processing
```python
# Process data in chunks
adata = ad.read_h5ad('large_file.h5ad', backed='r')

chunk_size = 1000
results = []

for i in range(0, adata.n_obs, chunk_size):
    chunk = adata[i:i+chunk_size, :].to_memory()
    # Process chunk
    result = process(chunk)
    results.append(result)
```

### Strategy 3: Use AnnCollection
A lightweight virtual collection over several AnnData objects that behaves like
one large dataset without concatenating in memory. Pass backed AnnData objects
(read each with `backed='r'`) so X stays on disk until a batch is accessed.
```python
import anndata as ad
from anndata.experimental import AnnCollection

# Open each file backed, then wrap — data is loaded only when a batch is sliced
adatas = [ad.read_h5ad(f'dataset_{i}.h5ad', backed='r') for i in range(10)]
collection = AnnCollection(adatas)

batch = collection[10:20]   # materializes just this slice
print(batch.X.shape)
```

## Common Issues and Solutions

### Issue: Out of memory when reading
**Solution**: Use backed mode or read in chunks
```python
adata = ad.read_h5ad('file.h5ad', backed='r')
```

### Issue: Slow reading from cloud storage
**Solution**: Use Zarr format with appropriate chunking
```python
adata.write_zarr('data.zarr', chunks=(1000, 1000))
```

### Issue: Large file sizes
**Solution**: Use compression and convert to sparse/categorical
```python
adata.strings_to_categoricals()
from scipy.sparse import csr_matrix
adata.X = csr_matrix(adata.X)
adata.write_h5ad('compressed.h5ad', compression='gzip')
```

### Issue: Cannot modify backed object
**Solution**: Either load to memory or open in 'r+' mode
```python
# Option 1: Load to memory
adata = adata.to_memory()

# Option 2: Open in read-write mode
adata = ad.read_h5ad('file.h5ad', backed='r+')
```
