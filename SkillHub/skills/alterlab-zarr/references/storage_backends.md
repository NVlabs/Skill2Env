# Zarr Storage Backends

Zarr supports multiple storage backends through a flexible storage interface.

## Local Filesystem (Default)

```python
from zarr.storage import LocalStore

# Explicit store creation
store = LocalStore('data/my_array.zarr')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))

# Or use string path (creates LocalStore automatically)
z = zarr.open_array('data/my_array.zarr', mode='w', shape=(1000, 1000),
                    chunks=(100, 100))
```

## In-Memory Storage

```python
from zarr.storage import MemoryStore

# Create in-memory store
store = MemoryStore()
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))

# Data exists only in memory, not persisted
```

## ZIP File Storage

```python
from zarr.storage import ZipStore

# Write to ZIP file
store = ZipStore('data.zip', mode='w')
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000), chunks=(100, 100))
z[:] = np.random.random((1000, 1000))
store.close()  # IMPORTANT: Must close ZipStore

# Read from ZIP file
store = ZipStore('data.zip', mode='r')
z = zarr.open_array(store=store)
data = z[:]
store.close()
```

## Cloud Storage (S3, GCS)

Zarr v3 ships a native `FsspecStore` — the idiomatic way to target object stores. Install the
matching fsspec backend (`s3fs` for S3, `gcsfs` for GCS).

```python
import zarr
from zarr.storage import FsspecStore

# S3 via URL (credentials picked up from the fsspec backend / env)
store = FsspecStore.from_url(
    "s3://my-bucket/path/to/array.zarr",
    storage_options={"anon": False},   # forwarded to s3fs
)
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000),
                    chunks=(100, 100), dtype='f4')
z[:] = data

# Google Cloud Storage — same pattern with a gs:// URL
store = FsspecStore.from_url(
    "gs://my-bucket/path/to/array.zarr",
    storage_options={"project": "my-project"},
)
z = zarr.open_array(store=store, mode='w', shape=(1000, 1000),
                    chunks=(100, 100), dtype='f4')

# A bare s3:// / gs:// path string also works directly:
z = zarr.open_array("s3://my-bucket/path/to/array.zarr", mode='r')
```

A plain fsspec mapping (`s3fs.S3Map(root=..., s3=...)`) is still accepted as a store, but
`FsspecStore.from_url` is preferred in v3.

**Cloud Storage Best Practices**:
- Consolidate metadata to cut round-trips: `zarr.consolidate_metadata(store)`, then read with `zarr.open_consolidated(store)`
- Align chunk sizes with cloud object sizing (roughly 5-100 MB per chunk)
- Use Dask (`da.to_zarr`) for parallel, chunk-aligned writes at scale
- Consider sharding (`shards=`) to reduce the number of stored objects
