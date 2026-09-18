---
name: alterlab-flowio
description: Parse and write FCS (Flow Cytometry Standard) files v2.0-3.1 with FlowIO — extract event data as NumPy arrays, read $-keyword metadata and channel/parameter definitions, and convert events to CSV or pandas DataFrame. Use when loading raw .fcs flow-cytometry files, inspecting channels and metadata, or preprocessing cytometry data for downstream gating and analysis. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with the skill's Python package installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# FlowIO: Flow Cytometry Standard File Handler

## Overview

FlowIO is a lightweight Python library for reading and writing Flow Cytometry
Standard (FCS) files. Parse FCS metadata, extract event data, and create new FCS
files with minimal dependencies. Supports FCS versions 2.0, 3.0, and 3.1 —
ideal for backend services, data pipelines, and basic cytometry file operations.

## When to Use This Skill

Use this skill when:

- FCS files require parsing or metadata extraction
- Flow cytometry data needs conversion to NumPy arrays
- Event data requires export to FCS format
- Multi-dataset FCS files need separation
- Channel information (scatter, fluorescence, time) must be extracted
- Cytometry files need validation or inspection
- Pre-processing is needed before advanced analysis

**Related tool:** For advanced analysis (compensation, gating, FlowJo/GatingML
support), recommend the **FlowKit** library as a companion to FlowIO.

## Installation

```bash
uv pip install flowio
```

Requires Python 3.9 or later.

## Quick Start

```python
from flowio import FlowData

# Read FCS file and inspect
flow = FlowData('experiment.fcs')
print(f"FCS Version: {flow.version}")
print(f"Events: {flow.event_count}")
print(f"Channels: {flow.pnn_labels}")

# Get event data as NumPy array, shape (events, channels)
events = flow.as_array()
```

```python
import numpy as np
from flowio import create_fcs

# Write a new FCS file from a NumPy array.
# Gotcha: create_fcs takes a WRITABLE BINARY FILE HANDLE (not a path) and a
# FLATTENED 1-D event array — pass data.flatten(), not the 2-D matrix.
data = np.array([[100, 200, 50], [150, 180, 60]], dtype='float32')  # 2 events, 3 channels
with open('output.fcs', 'wb') as fh:
    create_fcs(fh, data.flatten(), ['FSC-A', 'SSC-A', 'FL1-A'])
```

## Core Workflow

1. **Read** — Construct a `FlowData('file.fcs')` instance. Use `only_text=True`
   for metadata-only (memory-efficient) reads; pass offset/null-channel flags
   for problematic files.
2. **Inspect** — Read `flow.version`, `flow.event_count`, `flow.pnn_labels`,
   `flow.pns_labels`, channel-type indices, and the `flow.text` metadata dict.
3. **Extract** — Get a NumPy array via `flow.as_array()` (preprocessed) or
   `flow.as_array(preprocess=False)` (raw). Slice by channel type as needed.
4. **Transform / export** — Convert to a pandas DataFrame or CSV; or write a new
   FCS file with `flow.write_fcs(path, ...)` (takes a path) or `create_fcs(fh,
   data.flatten(), ...)` (takes a binary file handle + flattened events). Output
   is always FCS 3.1, single-precision float.
5. **Multi-dataset** — If a file holds multiple datasets, use
   `read_multiple_data_sets()` instead of the constructor.

## Routing Guidance

- **Need exact signatures, attributes, exceptions, or FCS keyword definitions?**
  Read `references/api_reference.md`.
- **Doing one of the core operations (read/parse, metadata, create, export,
  multi-dataset, preprocessing)?** Read `references/workflows.md` for full code.
- **Need a task recipe (inspect a file, batch a directory, FCS→CSV, filter
  events, extract channels)?** Read `references/recipes.md`.
- **Hitting an error, or want best practices / file-structure / troubleshooting?**
  Read `references/error-handling-and-troubleshooting.md`.

## References

- `references/api_reference.md` — Complete `FlowData` class, utility functions
  (`read_multiple_data_sets`, `create_fcs`), exception classes, FCS file
  structure, common TEXT-segment keywords, channel types, and example workflows.
- `references/workflows.md` — Full code for the core operations: reading/parsing,
  metadata & channel extraction, creating files, exporting/modifying,
  multi-dataset handling, and data preprocessing.
- `references/recipes.md` — Worked examples: inspecting contents, batch
  processing a directory, FCS→CSV conversion, event filtering & re-export, and
  channel extraction with statistics.
- `references/error-handling-and-troubleshooting.md` — Exception-handling
  patterns, best practices, FCS file-structure notes, a troubleshooting table,
  and integration notes (NumPy, pandas, FlowKit, web apps).

## Summary

FlowIO provides essential FCS file handling for flow cytometry workflows — use
it for parsing, metadata extraction, and file creation. For simple file
operations and data extraction, FlowIO alone is sufficient; for complex analysis
(compensation, gating), integrate with FlowKit or other specialized tools.
