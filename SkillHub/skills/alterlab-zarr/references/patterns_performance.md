# Zarr Patterns, Performance, and Troubleshooting

## Performance Optimization Checklist

1. **Chunk Size**: Aim for 1-10 MB per chunk
   ```python
   # For float32: 1MB = 262,144 elements
   chunks = (512, 512)  # 512×512×4 bytes = ~1MB
   ```

2. **Chunk Shape**: Align with access patterns
   ```python
   # Row-wise access → chunk spans columns: (small, large)
   # Column-wise access → chunk spans rows: (large, small)
   # Random access → balanced: (medium, medium)
   ```

3. **Compression**: Choose based on workload
   ```python
   # Interactive/fast: BloscCodec(cname='lz4')
   # Balanced: BloscCodec(cname='zstd', clevel=5)
   # Maximum compression: GzipCodec(level=9)
   ```

4. **Storage Backend**: Match to environment
   ```python
   # Local: LocalStore (default)
   # Cloud: FsspecStore.from_url("s3://...") with consolidated metadata
   # Temporary: MemoryStore
   ```

5. **Sharding**: Use for large-scale datasets
   ```python
   # When you have millions of small chunks
   shards=(10*chunk_size, 10*chunk_size)
   ```

6. **Parallel I/O**: Use Dask for large operations
   ```python
   import dask.array as da
   dask_array = da.from_zarr('data.zarr')
   result = dask_array.compute(scheduler='threads', num_workers=8)
   ```

## Profiling and Debugging

```python
# Print detailed array information
print(z.info)

# Output includes:
# - Type, shape, chunks, dtype
# - Compression codec and level
# - Storage size (compressed vs uncompressed)
# - Storage location

# Check storage size (nbytes_stored() is a method in v3)
stored = z.nbytes_stored()
print(f"Compressed size: {stored / 1e6:.2f} MB")
print(f"Uncompressed size: {z.nbytes / 1e6:.2f} MB")
print(f"Compression ratio: {z.nbytes / stored:.2f}x")
```

## Common Patterns

### Pattern: Time Series Data

```python
# Store time series with time as first dimension
# This allows efficient appending of new time steps
z = zarr.open('timeseries.zarr', mode='a',
              shape=(0, 720, 1440),  # Start with 0 time steps
              chunks=(1, 720, 1440),  # One time step per chunk
              dtype='f4')

# Append new time steps
new_data = np.random.random((1, 720, 1440))
z.append(new_data, axis=0)
```

### Pattern: Large Matrix Operations

```python
import dask.array as da

# Create large matrix in Zarr
z = zarr.open('matrix.zarr', mode='w',
              shape=(100000, 100000),
              chunks=(1000, 1000),
              dtype='f8')

# Use Dask for parallel computation
dask_z = da.from_zarr('matrix.zarr')
result = (dask_z @ dask_z.T).compute()  # Parallel matrix multiply
```

### Pattern: Cloud-Native Workflow

```python
import zarr
from zarr.storage import FsspecStore

# Write to S3 (needs s3fs)
store = FsspecStore.from_url("s3://my-bucket/data.zarr")

# Create array with appropriate chunking for cloud
z = zarr.open_array(store=store, mode='w',
                    shape=(10000, 10000),
                    chunks=(500, 500),  # ~1MB chunks
                    dtype='f4')
z[:] = data

# Consolidate metadata for faster reads
zarr.consolidate_metadata(store)

# Read from S3 (anywhere, anytime)
store_read = FsspecStore.from_url("s3://my-bucket/data.zarr")
root = zarr.open_consolidated(store_read)
subset = root[0:100, 0:100]
```

### Pattern: Format Conversion

```python
# HDF5 to Zarr
import h5py
import zarr

with h5py.File('data.h5', 'r') as h5:
    dataset = h5['dataset_name']
    z = zarr.array(dataset[:],
                   chunks=(1000, 1000),
                   store='data.zarr')

# NumPy to Zarr
import numpy as np
data = np.load('data.npy')
z = zarr.array(data, chunks='auto', store='data.zarr')

# Zarr to NetCDF (via Xarray)
import xarray as xr
ds = xr.open_zarr('data.zarr')
ds.to_netcdf('data.nc')
```

## Common Issues and Solutions

### Issue: Slow Performance

**Diagnosis**: Check chunk size and alignment
```python
print(z.chunks)  # Are chunks appropriate size?
print(z.info)    # Check compression ratio
```

**Solutions**:
- Increase chunk size to 1-10 MB
- Align chunks with access pattern
- Try different compression codecs
- Use Dask for parallel operations

### Issue: High Memory Usage

**Cause**: Loading entire array or large chunks into memory

**Solutions**:
```python
# Don't load entire array
# Bad: data = z[:]
# Good: Process in chunks
for i in range(0, z.shape[0], 1000):
    chunk = z[i:i+1000, :]
    process(chunk)

# Or use Dask for automatic chunking
import dask.array as da
dask_z = da.from_zarr('data.zarr')
result = dask_z.mean().compute()  # Processes in chunks
```

### Issue: Cloud Storage Latency

**Solutions**:
```python
# 1. Consolidate metadata
zarr.consolidate_metadata(store)
z = zarr.open_consolidated(store)

# 2. Use appropriate chunk sizes (5-100 MB for cloud)
chunks = (2000, 2000)  # Larger chunks for cloud

# 3. Enable sharding
shards = (10000, 10000)  # Groups many chunks
```

### Issue: Concurrent Write Conflicts

Zarr v3 has no `synchronizer` object (that was a Zarr v2 feature). Make concurrent writers
safe by giving each one a disjoint, chunk-aligned region so no two writers touch the same chunk:

```python
import zarr

z = zarr.open_array('data.zarr', mode='r+')  # chunks e.g. (1000, 1000)
# worker A writes z[0:1000, :]; worker B writes z[1000:2000, :] — no overlap, no coordination

# For distributed writes, let Dask schedule non-overlapping chunk writes:
import dask.array as da
da.to_zarr(dask_array, 'data.zarr')
```
