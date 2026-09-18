# Zarr Chunking, Compression, and Sharding

Chunking is critical for performance. Choose chunk sizes and shapes based on access patterns.

## Chunk Size Guidelines

- **Minimum chunk size**: 1 MB recommended for optimal performance
- **Balance**: Larger chunks = fewer metadata operations; smaller chunks = better parallel access
- **Memory consideration**: Entire chunks must fit in memory during compression

```python
# Configure chunk size (aim for ~1MB per chunk)
# For float32 data: 1MB = 262,144 elements = 512×512 array
z = zarr.zeros(
    shape=(10000, 10000),
    chunks=(512, 512),  # ~1MB chunks
    dtype='f4'
)
```

## Aligning Chunks with Access Patterns

**Critical**: Chunk shape dramatically affects performance based on how data is accessed.

```python
# If accessing rows frequently (first dimension)
z = zarr.zeros((10000, 10000), chunks=(10, 10000))  # Chunk spans columns

# If accessing columns frequently (second dimension)
z = zarr.zeros((10000, 10000), chunks=(10000, 10))  # Chunk spans rows

# For mixed access patterns (balanced approach)
z = zarr.zeros((10000, 10000), chunks=(1000, 1000))  # Square chunks
```

**Performance example**: For a (200, 200, 200) array, reading along the first dimension:
- Using chunks (1, 200, 200): ~107ms
- Using chunks (200, 200, 1): ~1.65ms (65× faster!)

## Sharding for Large-Scale Storage

When arrays have millions of small chunks, use sharding (a Zarr v3 feature) to group chunks
into larger storage objects. `shards` is the storage-object size; `chunks` is the inner,
independently-decodable unit. Each shard dimension must be a whole multiple of the chunk dimension.

```python
import zarr

# Create array with sharding — one storage object per (1000, 1000) shard,
# each containing 10x10 = 100 inner (100, 100) chunks.
z = zarr.create_array(
    store='data.zarr',
    shape=(100000, 100000),
    chunks=(100, 100),    # inner, independently-decodable unit
    shards=(1000, 1000),  # storage object groups 100 chunks per shard
    dtype='f4',
)

# Or let Zarr size the shards automatically:
z_auto = zarr.create_array(
    store='data2.zarr', shape=(100000, 100000),
    chunks=(100, 100), shards="auto", dtype='f4',
)
```

**Benefits**:
- Reduces file system overhead from millions of small files
- Improves cloud storage performance (fewer object requests)
- Prevents filesystem block size waste

**Important**: Entire shards must fit in memory before writing.

## Compression

Zarr applies compression per chunk to reduce storage while maintaining fast access. On
`create_array`, pass codecs via the `compressors=` keyword (a single codec or a list).
The `codecs=` keyword does **not** exist on `create_array` in Zarr v3.

### Configuring Compression

```python
from zarr.codecs import BloscCodec, BloscShuffle, GzipCodec

# Default (no compressors specified): Zstandard (ZstdCodec)
z = zarr.create_array(store='default.zarr', shape=(1000, 1000),
                      chunks=(100, 100), dtype='f4')

# Configure Blosc codec. shuffle accepts the BloscShuffle enum
# (.noshuffle / .shuffle / .bitshuffle); the equivalent strings are also accepted.
z = zarr.create_array(
    store='data.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    compressors=BloscCodec(cname='zstd', clevel=5, shuffle=BloscShuffle.shuffle),
)

# Available Blosc compressors (cname): 'blosclz', 'lz4', 'lz4hc', 'zlib', 'zstd'

# Use Gzip compression
z = zarr.create_array(
    store='gz.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    compressors=GzipCodec(level=6),
)

# Disable compression
z = zarr.create_array(
    store='raw.zarr',
    shape=(1000, 1000),
    chunks=(100, 100),
    dtype='f4',
    compressors=None,  # no compression
)
```

### Compression Performance Tips

- **Zstandard** (default): strong ratio with good speed; the sensible default for scientific data
- **Blosc**: a meta-compressor (wraps zstd/lz4/etc.) with byte-shuffle filters; fast for interactive workloads
- **Gzip**: maximum compatibility / high ratio, slower performance
- **LZ4** (via Blosc `cname='lz4'`): fastest compression, lower ratios
- **Shuffle**: enable the shuffle filter for better compression on numeric data

```python
# Balanced default for numeric scientific data
compressors=BloscCodec(cname='zstd', clevel=5, shuffle=BloscShuffle.shuffle)

# Optimal for speed
compressors=BloscCodec(cname='lz4', clevel=1)

# Optimal for compression ratio
compressors=GzipCodec(level=9)
```
