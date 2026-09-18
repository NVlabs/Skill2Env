# Zarr Python Quick Reference

This reference provides a concise overview of commonly used Zarr functions, parameters, and patterns for quick lookup during development.

## Array Creation Functions

> **Zarr v3 note:** the high-level creation functions take `compressors=` / `filters=`
> (not the v2 `compressor=`). Passing `compressor=` to a `zarr_format=3` array raises a
> `ValueError`. `compressors=None` disables compression; omitting it defaults to Zstandard.

### `zarr.zeros()` / `zarr.ones()` / `zarr.empty()`
```python
zarr.zeros(shape, *, chunks=None, dtype='f8', store=None, compressors='auto',
           fill_value=0, order='C', filters=None)
```
Create arrays filled with zeros, ones, or empty (uninitialized) values. These thin wrappers
forward their keyword arguments to `create_array`.

**Key parameters:**
- `shape`: Tuple defining array dimensions (e.g., `(1000, 1000)`)
- `chunks`: Tuple defining chunk dimensions (e.g., `(100, 100)`), `'auto'`, or `None`
- `dtype`: NumPy data type (e.g., `'f4'`, `'i8'`, `'bool'`)
- `store`: Storage location (string path, Store object, or mapping; `None` for in-memory)
- `compressors`: codec, list of codecs, `'auto'` (Zstandard default), or `None` to disable

### `zarr.create_array()`
```python
zarr.create_array(store, *, shape, dtype='f8', chunks='auto', shards=None,
                  compressors='auto', filters=None, fill_value=0, order='C',
                  zarr_format=3, overwrite=False)
```
Create a new array with explicit control over all parameters. Use `shards=` (Zarr v3) for
sharded storage.

### `zarr.array()`
```python
zarr.array(data, *, chunks='auto', dtype=None, compressors='auto', store=None)
```
Create array from existing data (NumPy array, list, etc.).

**Example:**
```python
import numpy as np
data = np.random.random((1000, 1000))
z = zarr.array(data, chunks=(100, 100), store='data.zarr')
```

### `zarr.open_array()` / `zarr.open()`
```python
zarr.open_array(store, *, mode='a', shape=None, chunks='auto', dtype=None,
                compressors='auto', fill_value=0)
```
Open existing array or create new one.

**Mode options:**
- `'r'`: Read-only
- `'r+'`: Read-write, file must exist
- `'a'`: Read-write, create if doesn't exist (default)
- `'w'`: Create new, overwrite if exists
- `'w-'`: Create new, fail if exists

## Storage Classes

### LocalStore (Default)
```python
from zarr.storage import LocalStore

store = LocalStore('path/to/data.zarr')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
```

### MemoryStore
```python
from zarr.storage import MemoryStore

store = MemoryStore()  # Data only in memory
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
```

### ZipStore
```python
from zarr.storage import ZipStore

# Write
store = ZipStore('data.zip', mode='w')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
z[:] = data
store.close()  # MUST close

# Read
store = ZipStore('data.zip', mode='r')
z = zarr.open_array(store=store)
data = z[:]
store.close()
```

### Cloud Storage (S3/GCS)
```python
from zarr.storage import FsspecStore

# S3 (needs s3fs)
store = FsspecStore.from_url("s3://bucket/path/data.zarr",
                             storage_options={"anon": False})

# GCS (needs gcsfs)
store = FsspecStore.from_url("gs://bucket/path/data.zarr",
                             storage_options={"project": "my-project"})
```

## Compression Codecs

Pass codecs through the `compressors=` keyword on `create_array` (not `codecs=`).

### Blosc Codec
```python
from zarr.codecs import BloscCodec, BloscShuffle

codec = BloscCodec(
    cname='zstd',                  # 'blosclz', 'lz4', 'lz4hc', 'zlib', 'zstd'
    clevel=5,                      # Compression level: 0-9
    shuffle=BloscShuffle.shuffle,  # .noshuffle / .shuffle / .bitshuffle (strings also accepted)
)

z = zarr.create_array(store='data.zarr', shape=(1000, 1000), chunks=(100, 100),
                      dtype='f4', compressors=codec)
```

**Blosc compressor characteristics:**
- `'lz4'`: Fastest compression, lower ratio
- `'zstd'`: Balanced, good ratio and speed
- `'zlib'`: Good compatibility, moderate performance
- `'lz4hc'`: Better ratio than lz4, slower
- `'blosclz'`: Blosc's own default codec

### Other Codecs
```python
from zarr.codecs import GzipCodec, ZstdCodec

# Zstandard compression — the default when compressors is unspecified
ZstdCodec(level=3)  # Level typically 1-22

# Gzip compression (maximum compatibility / high ratio, slower)
GzipCodec(level=6)  # Level 0-9

# No compression: pass compressors=None to create_array (do not pass an empty codec)
```

## Array Indexing and Selection

### Basic Indexing (NumPy-style)
```python
z = zarr.zeros((1000, 1000), chunks=(100, 100))

# Read
row = z[0, :]           # Single row
col = z[:, 0]           # Single column
block = z[10:20, 50:60] # Slice
element = z[5, 10]      # Single element

# Write
z[0, :] = 42
z[10:20, 50:60] = np.random.random((10, 10))
```

### Advanced Indexing
```python
# Coordinate indexing (point selection)
z.vindex[[0, 5, 10], [2, 8, 15]]  # Specific coordinates

# Orthogonal indexing (outer product)
z.oindex[0:10, [5, 10, 15]]  # Rows 0-9, columns 5, 10, 15

# Block/chunk indexing
z.blocks[0, 0]  # First chunk
z.blocks[0:2, 0:2]  # First four chunks
```

## Groups and Hierarchies

### Creating Groups
```python
# Create root group
root = zarr.group(store='data.zarr')

# Create nested groups
grp1 = root.create_group('group1')
grp2 = grp1.create_group('subgroup')

# Create arrays in groups
arr = grp1.create_array(name='data', shape=(1000, 1000),
                        chunks=(100, 100), dtype='f4')

# Access by path
arr2 = root['group1/data']
```

### Group Methods
```python
root = zarr.group('data.zarr')

# Create arrays / subgroups
dataset = root.create_array(name='data', shape=(1000, 1000), chunks=(100, 100), dtype='f4')
subgrp = root.require_group('subgroup')  # get-or-create

# Visualize structure
print(root.tree())

# List contents
print(list(root.keys()))
print(list(root.groups()))
print(list(root.arrays()))
```

> Zarr v3 removed the h5py-style `create_dataset` / `require_dataset` methods; use
> `create_array`.

## Array Attributes and Metadata

### Working with Attributes
```python
z = zarr.zeros((1000, 1000), chunks=(100, 100))

# Set attributes
z.attrs['units'] = 'meters'
z.attrs['description'] = 'Temperature data'
z.attrs['created'] = '2024-01-15'
z.attrs['version'] = 1.2
z.attrs['tags'] = ['climate', 'temperature']

# Read attributes
print(z.attrs['units'])
print(dict(z.attrs))  # All attributes as dict

# Update/delete
z.attrs['version'] = 2.0
del z.attrs['tags']
```

**Note:** Attributes must be JSON-serializable.

## Array Properties and Methods

### Properties
```python
z = zarr.zeros((1000, 1000), chunks=(100, 100), dtype='f4')

z.shape            # (1000, 1000)
z.chunks           # (100, 100)
z.dtype            # dtype('float32')
z.size             # 1000000
z.nbytes           # 4000000 (uncompressed size in bytes)
z.nbytes_stored()  # method() in v3 — actual compressed size on disk
z.nchunks          # 100 (number of chunks)
z.cdata_shape      # Shape in terms of chunks: (10, 10)
```

### Methods
```python
# Information
print(z.info)             # Summary (shape, chunks, dtype, codecs)
print(z.info_complete())  # Adds on-disk size / compression ratio (reads store)

# Resizing — pass the new shape as a single tuple (v3)
z.resize((1500, 1500))  # Change dimensions

# Appending
z.append(new_data, axis=0)  # Add data along axis
```

## Chunking Guidelines

### Chunk Size Calculation
```python
# For float32 (4 bytes per element):
# 1 MB = 262,144 elements
# 10 MB = 2,621,440 elements

# Examples for 1 MB chunks:
(512, 512)      # For 2D: 512 × 512 × 4 = 1,048,576 bytes
(128, 128, 128) # For 3D: 128 × 128 × 128 × 4 = 8,388,608 bytes ≈ 8 MB
(64, 256, 256)  # For 3D: 64 × 256 × 256 × 4 = 16,777,216 bytes ≈ 16 MB
```

### Chunking Strategies by Access Pattern

**Time series (sequential access along first dimension):**
```python
chunks=(1, 720, 1440)  # One time step per chunk
```

**Row-wise access:**
```python
chunks=(10, 10000)  # Small rows, span columns
```

**Column-wise access:**
```python
chunks=(10000, 10)  # Span rows, small columns
```

**Random access:**
```python
chunks=(500, 500)  # Balanced square chunks
```

**3D volumetric data:**
```python
chunks=(64, 64, 64)  # Cubic chunks for isotropic access
```

## Integration APIs

### NumPy Integration
```python
import numpy as np

z = zarr.zeros((1000, 1000), chunks=(100, 100))

# Use NumPy functions
result = np.sum(z, axis=0)
mean = np.mean(z)
std = np.std(z)

# Convert to NumPy
arr = z[:]  # Loads entire array into memory
```

### Dask Integration
```python
import dask.array as da

# Load Zarr as Dask array
dask_array = da.from_zarr('data.zarr')

# Compute operations in parallel
result = dask_array.mean(axis=0).compute()

# Write Dask array to Zarr
large_array = da.random.random((100000, 100000), chunks=(1000, 1000))
da.to_zarr(large_array, 'output.zarr')
```

### Xarray Integration
```python
import xarray as xr

# Open Zarr as Xarray Dataset
ds = xr.open_zarr('data.zarr')

# Write Xarray to Zarr
ds.to_zarr('output.zarr')

# Create with coordinates
ds = xr.Dataset(
    {'temperature': (['time', 'lat', 'lon'], data)},
    coords={
        'time': pd.date_range('2024-01-01', periods=365),
        'lat': np.arange(-90, 91, 1),
        'lon': np.arange(-180, 180, 1)
    }
)
ds.to_zarr('climate.zarr')
```

## Parallel Computing

Zarr v3 has **no** `synchronizer` objects or `synchronizer=` argument (removed from v2).
Coordinate concurrent writers by region instead, and tune I/O concurrency via config.

```python
import zarr

# Tune internal concurrency (default async.concurrency=10)
zarr.config.set({"async.concurrency": 4, "threading.max_workers": 4})

# Safe concurrent writes: each writer owns a disjoint, chunk-aligned region
z = zarr.open_array('data.zarr', mode='r+')
# worker A: z[0:1000, :] = ... ; worker B: z[1000:2000, :] = ...
```

**Rules of thumb:**
- Reads are always safe (no coordination)
- Within a process, reads and writes are thread-safe
- Across processes, only writes to disjoint chunks are safe; overlapping writes to the same
  chunk need external coordination — restructure so writers don't share chunks

## Metadata Consolidation

```python
# Consolidate metadata (after creating all arrays/groups)
zarr.consolidate_metadata('data.zarr')

# Open with consolidated metadata (faster, especially on cloud)
root = zarr.open_consolidated('data.zarr')
```

**Benefits:**
- Reduces I/O from N operations to 1
- Critical for cloud storage (reduces latency)
- Speeds up hierarchy traversal

**Cautions:**
- Can become stale if data updates
- Re-consolidate after modifications
- Not for frequently-updated datasets

## Common Patterns

### Time Series with Growing Data
```python
# Start with empty first dimension
z = zarr.open('timeseries.zarr', mode='a',
              shape=(0, 720, 1440),
              chunks=(1, 720, 1440),
              dtype='f4')

# Append new time steps
for new_timestep in data_stream:
    z.append(new_timestep, axis=0)
```

### Processing Large Arrays in Chunks
```python
z = zarr.open('large_data.zarr', mode='r')

# Process without loading entire array
for i in range(0, z.shape[0], 1000):
    chunk = z[i:i+1000, :]
    result = process(chunk)
    save(result)
```

### Format Conversion Pipeline
```python
# HDF5 → Zarr
import h5py
with h5py.File('data.h5', 'r') as h5:
    z = zarr.array(h5['dataset'][:], chunks=(1000, 1000), store='data.zarr')

# Zarr → NumPy file
z = zarr.open('data.zarr', mode='r')
np.save('data.npy', z[:])

# Zarr → NetCDF (via Xarray)
ds = xr.open_zarr('data.zarr')
ds.to_netcdf('data.nc')
```

## Performance Optimization Quick Checklist

1. **Chunk size**: 1-10 MB per chunk
2. **Chunk shape**: Align with access pattern
3. **Compression**:
   - Fast: `BloscCodec(cname='lz4', clevel=1)`
   - Balanced: `BloscCodec(cname='zstd', clevel=5)`
   - Maximum: `GzipCodec(level=9)`
4. **Cloud storage**:
   - Larger chunks (5-100 MB)
   - Consolidate metadata
   - Consider sharding
5. **Parallel I/O**: Use Dask for large operations
6. **Memory**: Process in chunks, don't load entire arrays

## Debugging and Profiling

```python
z = zarr.open('data.zarr', mode='r')

# Detailed information
print(z.info)

# Size statistics (nbytes_stored() is a method in v3)
stored = z.nbytes_stored()
print(f"Uncompressed: {z.nbytes / 1e6:.2f} MB")
print(f"Compressed: {stored / 1e6:.2f} MB")
print(f"Ratio: {z.nbytes / stored:.1f}x")

# Chunk information
print(f"Chunks: {z.chunks}")
print(f"Number of chunks: {z.nchunks}")
print(f"Chunk grid: {z.cdata_shape}")
```

## Common Data Types

```python
# Integers
'i1', 'i2', 'i4', 'i8'  # Signed: 8, 16, 32, 64-bit
'u1', 'u2', 'u4', 'u8'  # Unsigned: 8, 16, 32, 64-bit

# Floats
'f2', 'f4', 'f8'  # 16, 32, 64-bit (half, single, double precision)

# Others
'bool'     # Boolean
'c8', 'c16'  # Complex: 64, 128-bit
'S10'      # Fixed-length string (10 bytes)
'U10'      # Unicode string (10 characters)
```

## Version Compatibility

Zarr-Python version 3.x supports both:
- **Zarr v2 format**: Legacy format, widely compatible
- **Zarr v3 format**: New format with sharding, improved metadata

Check format version:
```python
# Zarr automatically detects format version
z = zarr.open('data.zarr', mode='r')
# Format info available in metadata
```

## Error Handling

```python
from zarr.errors import ArrayNotFoundError  # also: GroupNotFoundError, NodeNotFoundError

try:
    z = zarr.open_array('data.zarr', mode='r')
except FileNotFoundError:
    print("Store path does not exist")
except ArrayNotFoundError:
    print("Store exists but holds no array at this path")
except Exception as e:
    print(f"Unexpected error: {e}")
```

> Zarr v3 renamed the v2 exceptions: there is no `PathNotFoundError` or `ReadOnlyError`. A
> missing store raises `FileNotFoundError`; a missing node raises `ArrayNotFoundError` /
> `GroupNotFoundError`.
