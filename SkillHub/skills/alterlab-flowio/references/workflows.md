# FlowIO Core Workflows

Detailed code for the four primary FlowIO operations: reading/parsing, metadata
extraction, creating files, and exporting/modifying. See `api_reference.md` for
the full class/function signatures.

## Reading and Parsing FCS Files

The `FlowData` class is the primary interface for reading FCS files.

**Standard reading:**

```python
from flowio import FlowData

# Basic reading
flow = FlowData('sample.fcs')

# Access attributes
version = flow.version              # '3.0', '3.1', etc.
event_count = flow.event_count      # Number of events
channel_count = flow.channel_count  # Number of channels
pnn_labels = flow.pnn_labels        # Short channel names
pns_labels = flow.pns_labels        # Descriptive stain names

# Get event data
events = flow.as_array()            # Preprocessed (gain, log scaling applied)
raw_events = flow.as_array(preprocess=False)  # Raw data
```

**Memory-efficient metadata reading** (no event data):

```python
# Only parse TEXT segment, skip DATA and ANALYSIS
flow = FlowData('sample.fcs', only_text=True)

# Access metadata
metadata = flow.text  # Dictionary of TEXT segment keywords
print(metadata.get('$DATE'))  # Acquisition date
print(metadata.get('$CYT'))   # Instrument name
```

**Handling problematic files** (offset discrepancies or errors):

```python
# Ignore offset discrepancies between HEADER and TEXT sections
flow = FlowData('problematic.fcs', ignore_offset_discrepancy=True)

# Use HEADER offsets instead of TEXT offsets
flow = FlowData('problematic.fcs', use_header_offsets=True)

# Ignore offset errors entirely
flow = FlowData('problematic.fcs', ignore_offset_error=True)
```

**Excluding null channels:**

```python
# Exclude specific channels during parsing
flow = FlowData('sample.fcs', null_channel_list=['Time', 'Null'])
```

## Extracting Metadata and Channel Information

FCS files contain rich metadata in the TEXT segment.

**Common metadata keywords:**

```python
flow = FlowData('sample.fcs')

# File-level metadata
text_dict = flow.text
acquisition_date = text_dict.get('$DATE', 'Unknown')
instrument = text_dict.get('$CYT', 'Unknown')
data_type = flow.data_type  # 'I', 'F', 'D', 'A'

# Channel metadata
for i in range(flow.channel_count):
    pnn = flow.pnn_labels[i]      # Short name (e.g., 'FSC-A')
    pns = flow.pns_labels[i]      # Descriptive name (e.g., 'Forward Scatter')
    pnr = flow.pnr_values[i]      # Range/max value
    print(f"Channel {i}: {pnn} ({pns}), Range: {pnr}")
```

**Channel type identification** (FlowIO auto-categorizes channels):

```python
# Get indices by channel type
scatter_idx = flow.scatter_indices    # [0, 1] for FSC, SSC
fluoro_idx = flow.fluoro_indices      # [2, 3, 4] for FL channels
time_idx = flow.time_index            # Index of time channel (or None)

# Access specific channel types
events = flow.as_array()
scatter_data = events[:, scatter_idx]
fluorescence_data = events[:, fluoro_idx]
```

**ANALYSIS segment** (if present, processed results):

```python
if flow.analysis:
    analysis_keywords = flow.analysis  # Dictionary of ANALYSIS keywords
    print(analysis_keywords)
```

## Creating New FCS Files

Generate FCS files from NumPy arrays or other data sources.

**Basic creation:**

> **`create_fcs` call contract (two easy mistakes):**
> 1. First arg is a **writable binary file handle** (`open(path, 'wb')`), not a
>    path string — it calls `file_handle.seek(0)`.
> 2. `event_data` must be a **flattened 1-D** sequence (channel-interleaved); pass
>    `array.flatten()`, not the 2-D `(events, channels)` matrix.
> 3. The metadata keyword is `metadata_dict=` (not `metadata=`, which belongs to
>    `write_fcs`).

```python
import numpy as np
from flowio import create_fcs

# Create event data (rows=events, columns=channels)
events = (np.random.rand(10000, 5) * 1000).astype('float32')

# Define channel names
channel_names = ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'Time']

# Create FCS file
with open('output.fcs', 'wb') as fh:
    create_fcs(fh, events.flatten(), channel_names)
```

**With descriptive channel names:**

```python
# Add optional descriptive names (PnS)
channel_names = ['FSC-A', 'SSC-A', 'FL1-A', 'FL2-A', 'Time']
descriptive_names = ['Forward Scatter', 'Side Scatter', 'FITC', 'PE', 'Time']

with open('output.fcs', 'wb') as fh:
    create_fcs(fh,
               events.flatten(),
               channel_names,
               opt_channel_names=descriptive_names)
```

**With custom metadata:**

```python
# Add TEXT segment metadata
metadata = {
    '$SRC': 'Python script',
    '$DATE': '19-OCT-2025',
    '$CYT': 'Synthetic Instrument',
    '$INST': 'Laboratory A'
}

with open('output.fcs', 'wb') as fh:
    create_fcs(fh,
               events.flatten(),
               channel_names,
               opt_channel_names=descriptive_names,
               metadata_dict=metadata)
```

**Note:** FlowIO exports as FCS 3.1 with single-precision floating-point data.

## Exporting Modified Data

**Approach 1 — `write_fcs()` method:**

```python
from flowio import FlowData

# Read original file
flow = FlowData('original.fcs')

# Write with updated metadata
flow.write_fcs('modified.fcs', metadata={'$SRC': 'Modified data'})
```

**Approach 2 — extract, modify, and recreate** (for modifying event data):

```python
from flowio import FlowData, create_fcs

# Read and extract data
flow = FlowData('original.fcs')
events = flow.as_array(preprocess=False)

# Modify event data
events[:, 0] = events[:, 0] * 1.5  # Scale first channel

# Create new FCS file with modified data (handle + flattened + metadata_dict=)
with open('modified.fcs', 'wb') as fh:
    create_fcs(fh,
               events.flatten(),
               flow.pnn_labels,
               opt_channel_names=flow.pns_labels,
               metadata_dict=flow.text)
```

## Handling Multi-Dataset FCS Files

Some FCS files contain multiple datasets in a single file.

**Detecting multi-dataset files:**

```python
from flowio import FlowData, MultipleDataSetsError

try:
    flow = FlowData('sample.fcs')
except MultipleDataSetsError:
    print("File contains multiple datasets")
    # Use read_multiple_data_sets() instead
```

**Reading all datasets:**

```python
from flowio import read_multiple_data_sets

# Read all datasets from file
datasets = read_multiple_data_sets('multi_dataset.fcs')

print(f"Found {len(datasets)} datasets")

# Process each dataset
for i, dataset in enumerate(datasets):
    print(f"\nDataset {i}:")
    print(f"  Events: {dataset.event_count}")
    print(f"  Channels: {dataset.pnn_labels}")

    # Get event data for this dataset
    events = dataset.as_array()
    print(f"  Shape: {events.shape}")
    print(f"  Mean values: {events.mean(axis=0)}")
```

**Reading a specific dataset:**

```python
from flowio import FlowData

# Read first dataset (nextdata_offset=0)
first_dataset = FlowData('multi.fcs', nextdata_offset=0)

# Read second dataset using NEXTDATA offset from first
next_offset = int(first_dataset.text['$NEXTDATA'])
if next_offset > 0:
    second_dataset = FlowData('multi.fcs', nextdata_offset=next_offset)
```

## Data Preprocessing

FlowIO applies standard FCS preprocessing transformations when `preprocess=True`:

1. **Gain scaling:** Multiply values by PnG (gain) keyword
2. **Logarithmic transformation:** Apply PnE exponential transformation if present
   - Formula: `value = a * 10^(b * raw_value)` where PnE = "a,b"
3. **Time scaling:** Convert time values to appropriate units

```python
# Preprocessed data (default)
preprocessed = flow.as_array(preprocess=True)

# Raw data (no transformations)
raw = flow.as_array(preprocess=False)
```
