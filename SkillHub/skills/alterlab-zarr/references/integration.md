# Zarr Integration: NumPy, Dask, Xarray, and Parallel Computing

## NumPy Integration

Zarr arrays implement the NumPy array interface:

```python
import numpy as np
import zarr

z = zarr.zeros((1000, 1000), chunks=(100, 100))

# Use NumPy functions directly
result = np.sum(z, axis=0)  # NumPy operates on Zarr array
mean = np.mean(z[:100, :100])

# Convert to NumPy array
numpy_array = z[:]  # Loads entire array into memory
```

## Dask Integration

Dask provides lazy, parallel computation on Zarr arrays:

```python
import dask.array as da
import zarr

# Create large Zarr array
z = zarr.open('data.zarr', mode='w', shape=(100000, 100000),
              chunks=(1000, 1000), dtype='f4')

# Load as Dask array (lazy, no data loaded)
dask_array = da.from_zarr('data.zarr')

# Perform computations (parallel, out-of-core)
result = dask_array.mean(axis=0).compute()  # Parallel computation

# Write Dask array to Zarr
large_array = da.random.random((100000, 100000), chunks=(1000, 1000))
da.to_zarr(large_array, 'output.zarr')
```

**Benefits**:
- Process datasets larger than memory
- Automatic parallel computation across chunks
- Efficient I/O with chunked storage

## Xarray Integration

Xarray provides labeled, multidimensional arrays with Zarr backend:

```python
import xarray as xr
import zarr

# Open Zarr store as Xarray Dataset (lazy loading)
ds = xr.open_zarr('data.zarr')

# Dataset includes coordinates and metadata
print(ds)

# Access variables
temperature = ds['temperature']

# Perform labeled operations
subset = ds.sel(time='2024-01', lat=slice(30, 60))

# Write Xarray Dataset to Zarr
ds.to_zarr('output.zarr')

# Create from scratch with coordinates
ds = xr.Dataset(
    {
        'temperature': (['time', 'lat', 'lon'], data),
        'precipitation': (['time', 'lat', 'lon'], data2)
    },
    coords={
        'time': pd.date_range('2024-01-01', periods=365),
        'lat': np.arange(-90, 91, 1),
        'lon': np.arange(-180, 180, 1)
    }
)
ds.to_zarr('climate_data.zarr')
```

**Benefits**:
- Named dimensions and coordinates
- Label-based indexing and selection
- Integration with pandas for time series
- NetCDF-like interface familiar to climate/geospatial scientists

## Parallel Computing and Concurrency

Zarr v3 removed the explicit `synchronizer` objects (`ThreadSynchronizer` /
`ProcessSynchronizer`) and the `synchronizer=` argument that existed in Zarr v2. The v3 model
is simpler:

- **Concurrent reads** are always safe and need no coordination.
- **Within one process**, reads and writes are thread-safe.
- **Across processes**, concurrent writes are safe *only when each process writes to a disjoint
  set of chunks* (and the store backend supports atomic per-key writes). Overlapping writes to
  the *same* chunk from multiple processes still require external coordination — design the
  workload so writers own non-overlapping chunk-aligned regions instead.

```python
import zarr

# Tune Zarr's internal I/O concurrency (defaults: async.concurrency=10).
# Lower these when pairing with Dask so dask_threads * async.concurrency
# doesn't overwhelm the storage backend.
zarr.config.set({
    "async.concurrency": 4,
    "threading.max_workers": 4,
})

# Multiple workers writing to chunk-aligned, non-overlapping regions is safe
# without any synchronizer:
z = zarr.open_array('data.zarr', mode='r+')   # chunks e.g. (1000, 1000)
# worker A: z[0:1000, :] = block_a
# worker B: z[1000:2000, :] = block_b
```

For distributed/out-of-core writes, prefer Dask's `da.to_zarr`, which schedules
non-overlapping chunk writes for you.
