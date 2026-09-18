# FlowIO Error Handling and Troubleshooting

Exception handling patterns, best practices, FCS file structure notes, and a
troubleshooting table.

## Error Handling

Handle common FlowIO exceptions appropriately:

```python
from flowio import (
    FlowData,
    FCSParsingError,
    DataOffsetDiscrepancyError,
    MultipleDataSetsError
)

try:
    flow = FlowData('sample.fcs')
    events = flow.as_array()

except FCSParsingError as e:
    print(f"Failed to parse FCS file: {e}")
    # Try with relaxed parsing
    flow = FlowData('sample.fcs', ignore_offset_error=True)

except DataOffsetDiscrepancyError as e:
    print(f"Offset discrepancy detected: {e}")
    # Use ignore_offset_discrepancy parameter
    flow = FlowData('sample.fcs', ignore_offset_discrepancy=True)

except MultipleDataSetsError as e:
    print(f"Multiple datasets detected: {e}")
    # Use read_multiple_data_sets instead
    from flowio import read_multiple_data_sets
    datasets = read_multiple_data_sets('sample.fcs')

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Memory efficiency:** Use `only_text=True` when event data is not needed.
2. **Error handling:** Wrap file operations in try-except blocks for robust code.
3. **Multi-dataset detection:** Check for `MultipleDataSetsError` and use the
   appropriate function.
4. **Preprocessing control:** Explicitly set the `preprocess` parameter based on
   analysis needs.
5. **Offset issues:** If parsing fails, try `ignore_offset_discrepancy=True`.
6. **Channel validation:** Verify channel counts and names match expectations
   before processing.
7. **Metadata preservation:** When modifying files, preserve original TEXT
   segment keywords.

## FCS File Structure

FCS files consist of four segments:

1. **HEADER:** FCS version and byte offsets for other segments
2. **TEXT:** Key-value metadata pairs (delimiter-separated)
3. **DATA:** Raw event data (binary/float/ASCII format)
4. **ANALYSIS** (optional): Results from data processing

Access these segments via `FlowData` attributes:

- `flow.header` — HEADER segment
- `flow.text` — TEXT segment keywords
- `flow.events` — DATA segment (as bytes)
- `flow.analysis` — ANALYSIS segment keywords (if present)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Offset discrepancy error" | Use `ignore_offset_discrepancy=True` parameter |
| "Multiple datasets error" | Use `read_multiple_data_sets()` instead of the `FlowData` constructor |
| Out of memory with large files | Use `only_text=True` for metadata-only operations, or process events in chunks |
| Unexpected channel counts | Check for null channels; use `null_channel_list` to exclude them |
| Cannot modify event data in place | FlowIO doesn't support direct modification; extract data, modify, then use `create_fcs()` to save (see below for its call contract) |
| `create_fcs` → `AttributeError: 'str' object has no attribute 'seek'` | First arg must be a writable binary file handle (`open(path, 'wb')`), not a path string |
| `create_fcs` → `ValueError: Number of data points is not a multiple of the number of channels` | `event_data` must be a flattened 1-D array; pass `array.flatten()`, not the 2-D `(events, channels)` matrix |
| `create_fcs` → `TypeError: unexpected keyword argument 'metadata'` | Use `metadata_dict=` for `create_fcs` (only `write_fcs` uses `metadata=`) |

## Integration Notes

- **NumPy arrays:** All event data is returned as NumPy ndarrays with shape
  `(events, channels)`.
- **Pandas DataFrames:** Convert easily with
  `pd.DataFrame(flow.as_array(), columns=flow.pnn_labels)`.
- **FlowKit integration:** For advanced analysis (compensation, gating, FlowJo
  support), use FlowKit, which builds on FlowIO's parsing capabilities.
- **Web applications:** FlowIO's minimal dependencies make it ideal for web
  backend services processing FCS uploads.
