# FlowIO Common Recipes

Worked examples for frequent FCS tasks: inspecting contents, batch processing,
CSV export, event filtering, and channel extraction.

## Inspecting FCS File Contents

Quick exploration of FCS file structure:

```python
from flowio import FlowData

flow = FlowData('unknown.fcs')

print("=" * 50)
print(f"File: {flow.name}")
print(f"Version: {flow.version}")
print(f"Size: {flow.file_size:,} bytes")
print("=" * 50)

print(f"\nEvents: {flow.event_count:,}")
print(f"Channels: {flow.channel_count}")

print("\nChannel Information:")
for i, (pnn, pns) in enumerate(zip(flow.pnn_labels, flow.pns_labels)):
    ch_type = "scatter" if i in flow.scatter_indices else \
              "fluoro" if i in flow.fluoro_indices else \
              "time" if i == flow.time_index else "other"
    print(f"  [{i}] {pnn:10s} | {pns:30s} | {ch_type}")

print("\nKey Metadata:")
for key in ['$DATE', '$BTIM', '$ETIM', '$CYT', '$INST', '$SRC']:
    value = flow.text.get(key, 'N/A')
    print(f"  {key:15s}: {value}")
```

## Batch Processing Multiple Files

Process a directory of FCS files (metadata-only, memory efficient):

```python
from pathlib import Path
from flowio import FlowData
import pandas as pd

# Find all FCS files
fcs_files = list(Path('data/').glob('*.fcs'))

# Extract summary information
summaries = []
for fcs_path in fcs_files:
    try:
        flow = FlowData(str(fcs_path), only_text=True)
        summaries.append({
            'filename': fcs_path.name,
            'version': flow.version,
            'events': flow.event_count,
            'channels': flow.channel_count,
            'date': flow.text.get('$DATE', 'N/A')
        })
    except Exception as e:
        print(f"Error processing {fcs_path.name}: {e}")

# Create summary DataFrame
df = pd.DataFrame(summaries)
print(df)
```

## Converting FCS to CSV

Export event data to CSV format:

```python
from flowio import FlowData
import pandas as pd

# Read FCS file
flow = FlowData('sample.fcs')

# Convert to DataFrame
df = pd.DataFrame(
    flow.as_array(),
    columns=flow.pnn_labels
)

# Add metadata as attributes
df.attrs['fcs_version'] = flow.version
df.attrs['instrument'] = flow.text.get('$CYT', 'Unknown')

# Export to CSV
df.to_csv('output.csv', index=False)
print(f"Exported {len(df)} events to CSV")
```

## Filtering Events and Re-exporting

Apply filters and save filtered data:

```python
from flowio import FlowData, create_fcs
import numpy as np

# Read original file
flow = FlowData('sample.fcs')
events = flow.as_array(preprocess=False)

# Apply filtering (example: threshold on first channel)
fsc_idx = 0
threshold = 500
mask = events[:, fsc_idx] > threshold
filtered_events = events[mask]

print(f"Original events: {len(events)}")
print(f"Filtered events: {len(filtered_events)}")

# Create new FCS file with filtered data.
# create_fcs wants a binary file handle + a FLATTENED 1-D event array, and the
# metadata keyword is metadata_dict= (not metadata=).
with open('filtered.fcs', 'wb') as fh:
    create_fcs(fh,
               filtered_events.flatten(),
               flow.pnn_labels,
               opt_channel_names=flow.pns_labels,
               metadata_dict={**flow.text, '$SRC': 'Filtered data'})
```

## Extracting Specific Channels

Extract and process specific channels:

```python
from flowio import FlowData
import numpy as np

flow = FlowData('sample.fcs')
events = flow.as_array()

# Extract fluorescence channels only
fluoro_indices = flow.fluoro_indices
fluoro_data = events[:, fluoro_indices]
fluoro_names = [flow.pnn_labels[i] for i in fluoro_indices]

print(f"Fluorescence channels: {fluoro_names}")
print(f"Shape: {fluoro_data.shape}")

# Calculate statistics per channel
for i, name in enumerate(fluoro_names):
    channel_data = fluoro_data[:, i]
    print(f"\n{name}:")
    print(f"  Mean: {channel_data.mean():.2f}")
    print(f"  Median: {np.median(channel_data):.2f}")
    print(f"  Std Dev: {channel_data.std():.2f}")
```
