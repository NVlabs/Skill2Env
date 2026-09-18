# Zarr Array Operations

Creating, opening, reading/writing, resizing arrays, and attributes/metadata.

## Creating Arrays

Zarr provides multiple convenience functions for array creation:

```python
# Create empty array
z = zarr.zeros(shape=(10000, 10000), chunks=(1000, 1000), dtype='f4',
               store='data.zarr')

# Create filled arrays
z = zarr.ones((5000, 5000), chunks=(500, 500))
z = zarr.full((1000, 1000), fill_value=42, chunks=(100, 100))

# Create from existing data
data = np.arange(10000).reshape(100, 100)
z = zarr.array(data, chunks=(10, 10), store='data.zarr')

# Create like another array
z2 = zarr.zeros_like(z)  # Matches shape, chunks, dtype of z
```

## Opening Existing Arrays

```python
# Open array (read/write mode by default)
z = zarr.open_array('data.zarr', mode='r+')

# Read-only mode
z = zarr.open_array('data.zarr', mode='r')

# The open() function auto-detects arrays vs groups
z = zarr.open('data.zarr')  # Returns Array or Group
```

## Reading and Writing Data

Zarr arrays support NumPy-like indexing:

```python
# Write entire array
z[:] = 42

# Write slices
z[0, :] = np.arange(100)
z[10:20, 50:60] = np.random.random((10, 10))

# Read data (returns NumPy array)
data = z[0:100, 0:100]
row = z[5, :]

# Advanced indexing
z.vindex[[0, 5, 10], [2, 8, 15]]  # Coordinate indexing
z.oindex[0:10, [5, 10, 15]]       # Orthogonal indexing
z.blocks[0, 0]                     # Block/chunk indexing
```

## Resizing and Appending

```python
# Resize array — pass the new shape as a single tuple (v3)
z.resize((15000, 15000))  # Expands or shrinks dimensions

# Append data along an axis
z.append(np.random.random((1000, 10000)), axis=0)  # Adds rows
```

## Attributes and Metadata

Attach custom metadata to arrays and groups using attributes:

```python
# Add attributes to array
z = zarr.zeros((1000, 1000), chunks=(100, 100))
z.attrs['description'] = 'Temperature data in Kelvin'
z.attrs['units'] = 'K'
z.attrs['created'] = '2024-01-15'
z.attrs['processing_version'] = 2.1

# Attributes are stored as JSON
print(z.attrs['units'])  # Output: K

# Add attributes to groups
root = zarr.group('data.zarr')
root.attrs['project'] = 'Climate Analysis'
root.attrs['institution'] = 'Research Institute'

# Attributes persist with the array/group
z2 = zarr.open('data.zarr')
print(z2.attrs['description'])
```

**Important**: Attributes must be JSON-serializable (strings, numbers, lists, dicts, booleans, null).

## Groups and Hierarchies

Groups organize multiple arrays hierarchically, similar to directories or HDF5 groups.

### Creating and Using Groups

```python
# Create root group
root = zarr.group(store='data/hierarchy.zarr')

# Create sub-groups
temperature = root.create_group('temperature')
precipitation = root.create_group('precipitation')

# Create arrays within groups
temp_array = temperature.create_array(
    name='t2m',
    shape=(365, 720, 1440),
    chunks=(1, 720, 1440),
    dtype='f4'
)

precip_array = precipitation.create_array(
    name='prcp',
    shape=(365, 720, 1440),
    chunks=(1, 720, 1440),
    dtype='f4'
)

# Access using paths
array = root['temperature/t2m']

# Visualize hierarchy
print(root.tree())
# Output:
# /
#  ├── temperature
#  │   └── t2m (365, 720, 1440) f4
#  └── precipitation
#      └── prcp (365, 720, 1440) f4
```

### Creating arrays inside groups

Create arrays with the group's `create_array`, and use `require_group` to get-or-create a
subgroup (handy when migrating HDF5 hierarchies):

```python
root = zarr.group('data.zarr')
dataset = root.create_array(name='my_data', shape=(1000, 1000), chunks=(100, 100),
                            dtype='f4')

# require_group returns the subgroup, creating it only if absent
grp = root.require_group('subgroup')
arr = grp.create_array(name='array', shape=(500, 500), chunks=(50, 50), dtype='i4')
```

> Zarr v3 dropped the h5py-style `create_dataset` / `require_dataset` group methods — use
> `create_array` (and `require_group` for groups).

## Consolidated Metadata

For hierarchical stores with many arrays, consolidate metadata into a single file to reduce I/O operations:

```python
import zarr

# After creating arrays/groups
root = zarr.group('data.zarr')
# ... create multiple arrays/groups ...

# Consolidate metadata
zarr.consolidate_metadata('data.zarr')

# Open with consolidated metadata (faster, especially on cloud storage)
root = zarr.open_consolidated('data.zarr')
```

**Benefits**:
- Reduces metadata read operations from N (one per array) to 1
- Critical for cloud storage (reduces latency)
- Speeds up `tree()` operations and group traversal

**Cautions**:
- Metadata can become stale if arrays update without re-consolidation
- Not suitable for frequently-updated datasets
- Multi-writer scenarios may have inconsistent reads
