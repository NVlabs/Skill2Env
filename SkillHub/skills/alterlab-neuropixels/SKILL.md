---
name: alterlab-neuropixels
description: Analyze Neuropixels 1.0/2.0 extracellular electrophysiology with SpikeInterface — load SpikeGLX/Open Ephys recordings, preprocess and motion-correct, run Kilosort4 spike sorting, compute quality metrics, apply Allen/IBL curation, and do AI-assisted visual inspection. Use when working with neural recordings, spike sorting, or extracellular electrophysiology, or when the user mentions Neuropixels, SpikeGLX, Open Ephys, Kilosort, quality metrics, or unit curation. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with the skill's Python package installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Neuropixels Data Analysis

## Overview

Comprehensive toolkit for analyzing Neuropixels high-density neural recordings using current best practices from SpikeInterface, Allen Institute, and International Brain Laboratory (IBL). Supports the full workflow from raw data to publication-ready curated units.

## When to Use This Skill

This skill should be used when:
- Working with Neuropixels recordings (.ap.bin, .lf.bin, .meta files)
- Loading data from SpikeGLX, Open Ephys, or NWB formats
- Preprocessing neural recordings (filtering, CAR, bad channel detection)
- Detecting and correcting motion/drift in recordings
- Running spike sorting (Kilosort4, SpykingCircus2, Mountainsort5)
- Computing quality metrics (SNR, ISI violations, presence ratio)
- Curating units using Allen/IBL criteria
- Creating visualizations of neural data
- Exporting results to Phy or NWB

## Supported Hardware & Formats

| Probe | Electrodes | Channels | Notes |
|-------|-----------|----------|-------|
| Neuropixels 1.0 | 960 | 384 | Requires phase_shift correction |
| Neuropixels 2.0 (single) | 1280 | 384 | Denser geometry |
| Neuropixels 2.0 (4-shank) | 5120 | 384 | Multi-region recording |

| Format | Extension | Reader |
|--------|-----------|--------|
| SpikeGLX | `.ap.bin`, `.lf.bin`, `.meta` | `si.read_spikeglx()` |
| Open Ephys | `.continuous`, `.oebin` | `si.read_openephys()` |
| NWB | `.nwb` | `si.read_nwb()` |

## Quick Start

### Basic Import and Setup

```python
import spikeinterface.full as si

# Bundled helper functions live in scripts/neuropixels_pipeline.py
from scripts.neuropixels_pipeline import (
    load_recording, preprocess, check_drift, correct_motion,
    run_spike_sorting, postprocess, curate_units, export_results, run_pipeline,
)

# Configure parallel processing
job_kwargs = dict(n_jobs=-1, chunk_duration='1s', progress_bar=True)
```

### Loading Data

```python
# SpikeGLX (most common)
recording = si.read_spikeglx('/path/to/data', stream_id='imec0.ap')

# Open Ephys (common for many labs)
recording = si.read_openephys('/path/to/Record_Node_101/')

# Check available streams
streams, ids = si.get_neo_streams('spikeglx', '/path/to/data')
print(streams)  # ['imec0.ap', 'imec0.lf', 'nidq']

# For testing with subset of data
recording = recording.frame_slice(0, int(60 * recording.get_sampling_frequency()))
```

### Complete Pipeline (One Command)

```python
# Run full analysis pipeline (writes all outputs under output_path/)
from scripts.neuropixels_pipeline import run_pipeline

run_pipeline(
    data_path='/path/to/data',
    output_path='output/',
    sorter='kilosort4',
    stream_name='imec0.ap',
    apply_motion_correction=True,
    curation_method='allen',
)

# Results are written to disk:
#   output/sorting_output/    spike sorter output
#   output/analyzer/          SortingAnalyzer (waveforms, metrics)
#   output/quality_metrics.csv
#   output/curation_labels.json
```

Or run it from the command line:

```bash
python scripts/neuropixels_pipeline.py /path/to/data output/ --sorter kilosort4 --curation allen
```

## Standard Analysis Workflow

### 1. Preprocessing

```python
# Recommended preprocessing chain
rec = si.highpass_filter(recording, freq_min=400)
rec = si.phase_shift(rec)  # Required for Neuropixels 1.0
bad_ids, _ = si.detect_bad_channels(rec)
rec = rec.remove_channels(bad_ids)
rec = si.common_reference(rec, operator='median')

# Or use the bundled wrapper (returns the preprocessed recording + bad channel ids)
from scripts.neuropixels_pipeline import preprocess
rec, bad_channels = preprocess(recording)
```

### 2. Check and Correct Drift

```python
from scripts.neuropixels_pipeline import check_drift, correct_motion

# Check for drift (always do this!) — detects/localizes peaks and saves
# a drift plot to <output_folder>/drift_check.png, returns a dict with
# 'drift_estimate' (μm range).
drift_info = check_drift(rec, output_folder='output/')

# Apply correction if needed
if drift_info['drift_estimate'] > 20:  # microns
    rec = correct_motion(rec, output_folder='output/', preset='nonrigid_fast_and_accurate')
```

### 3. Spike Sorting

```python
# Kilosort4 (recommended, requires GPU)
sorting = si.run_sorter('kilosort4', rec, folder='ks4_output')

# CPU alternatives
sorting = si.run_sorter('tridesclous2', rec, folder='tdc2_output')
sorting = si.run_sorter('spykingcircus2', rec, folder='sc2_output')
sorting = si.run_sorter('mountainsort5', rec, folder='ms5_output')

# Check available sorters
print(si.installed_sorters())
```

### 4. Postprocessing

```python
# Create analyzer and compute all extensions
analyzer = si.create_sorting_analyzer(sorting, rec, sparse=True)

analyzer.compute('random_spikes', max_spikes_per_unit=500)
analyzer.compute('waveforms', ms_before=1.0, ms_after=2.0)
analyzer.compute('templates', operators=['average', 'std'])
analyzer.compute('spike_amplitudes')
analyzer.compute('correlograms', window_ms=50.0, bin_ms=1.0)
analyzer.compute('unit_locations', method='monopolar_triangulation')
analyzer.compute('quality_metrics')

metrics = analyzer.get_extension('quality_metrics').get_data()
```

### 5. Curation

```python
# Allen Institute criteria (conservative)
good_units = metrics.query("""
    presence_ratio > 0.9 and
    isi_violations_ratio < 0.5 and
    amplitude_cutoff < 0.1
""").index.tolist()

# Or use automated curation (returns {unit_id: 'good'|'mua'|'noise'})
from scripts.neuropixels_pipeline import curate_units
labels = curate_units(metrics, method='allen')  # 'allen', 'ibl', 'strict'
```

### 6. AI-Assisted Curation (For Uncertain Units)

When using this skill with Claude Code, Claude can directly analyze waveform plots and provide expert curation decisions. The recommended workflow is to render per-unit summary plots with SpikeInterface and let Claude inspect them:

```python
import spikeinterface.widgets as sw
import matplotlib.pyplot as plt

# Find borderline units worth a visual look
uncertain = metrics.query('snr > 3 and snr < 8').index.tolist()

# Render a summary figure per uncertain unit (waveform + correlogram + amplitudes)
for unit_id in uncertain:
    sw.plot_unit_summary(analyzer, unit_id=unit_id)
    plt.savefig(f'ai_curation/unit_{unit_id}_summary.png', dpi=150, bbox_inches='tight')
    plt.close()
```

**Claude Code Integration**: When running within Claude Code, ask Claude to examine the saved waveform/correlogram plots directly - no API setup required.

### 7. Generate Analysis Report

```python
# The bundled run_pipeline writes a machine-readable summary.json
# (sampling rate, duration, channel count, unit counts) into output_path/.
import json
with open('output/summary.json') as f:
    summary = json.load(f)
print(summary)

# For a browsable HTML report of waveforms/metrics, use SpikeInterface's exporter:
si.export_report(analyzer, output_folder='output/report/')
# Open output/report/index.html for figures and the per-unit table
```

### 8. Export Results

```python
# Export to Phy for manual review
si.export_to_phy(analyzer, output_folder='phy_export/',
                 compute_pc_features=True, compute_amplitudes=True)

# Export to NWB (via NeuroConv — SpikeInterface has no native NWB exporter)
# pip install neuroconv
from neuroconv.tools.spikeinterface import write_sorting, write_recording
write_recording(recording=rec, nwbfile_path='output.nwb', overwrite=True)
write_sorting(sorting=sorting, nwbfile_path='output.nwb')

# Save quality metrics
metrics.to_csv('quality_metrics.csv')
```

## Common Pitfalls and Best Practices

1. **Always check drift** before spike sorting - drift > 10μm significantly impacts quality
2. **Use phase_shift** for Neuropixels 1.0 probes (not needed for 2.0)
3. **Save preprocessed data** to avoid recomputing - use `rec.save(folder='preprocessed/')`
4. **Use GPU** for Kilosort4 - it's 10-50x faster than CPU alternatives
5. **Review uncertain units manually** - automated curation is a starting point
6. **Combine metrics with AI** - use metrics for clear cases, AI for borderline units
7. **Document your thresholds** - different analyses may need different criteria
8. **Export to Phy** for critical experiments - human oversight is valuable

## Key Parameters to Adjust

### Preprocessing
- `freq_min`: Highpass cutoff (300-400 Hz typical)
- `detect_threshold`: Bad channel detection sensitivity

### Motion Correction
- `preset`: 'kilosort_like' (fast) or 'nonrigid_accurate' (better for severe drift)

### Spike Sorting (Kilosort4)
- `batch_size`: Samples per batch (30000 default)
- `nblocks`: Number of drift blocks (increase for long recordings)
- `Th_learned`: Detection threshold (lower = more spikes)

### Quality Metrics
- `snr_threshold`: Signal-to-noise cutoff (3-5 typical)
- `isi_violations_ratio`: Refractory violations (0.01-0.5)
- `presence_ratio`: Recording coverage (0.5-0.95)

## Bundled Resources

### scripts/preprocess_recording.py
Automated preprocessing script:
```bash
python scripts/preprocess_recording.py /path/to/data --output preprocessed/
```

### scripts/run_sorting.py
Run spike sorting:
```bash
python scripts/run_sorting.py preprocessed/ --sorter kilosort4 --output sorting/
```

### scripts/compute_metrics.py
Compute quality metrics and apply curation:
```bash
python scripts/compute_metrics.py sorting/ preprocessed/ --output metrics/ --curation allen
```

### scripts/export_to_phy.py
Export to Phy for manual curation:
```bash
python scripts/export_to_phy.py metrics/analyzer --output phy_export/
```

### assets/analysis_template.py
Complete analysis template. Copy and customize:
```bash
cp assets/analysis_template.py my_analysis.py
# Edit parameters and run
python my_analysis.py
```

### references/standard_workflow.md
Detailed step-by-step workflow with explanations for each stage.

### references/api_reference.md
Quick function reference organized by module.

### references/plotting_guide.md
Comprehensive visualization guide for publication-quality figures.

## Detailed Reference Guides

| Topic | Reference |
|-------|-----------|
| Full workflow | [references/standard_workflow.md](references/standard_workflow.md) |
| API reference | [references/api_reference.md](references/api_reference.md) |
| Plotting guide | [references/plotting_guide.md](references/plotting_guide.md) |
| Preprocessing | [references/PREPROCESSING.md](references/PREPROCESSING.md) |
| Spike sorting | [references/SPIKE_SORTING.md](references/SPIKE_SORTING.md) |
| Motion correction | [references/MOTION_CORRECTION.md](references/MOTION_CORRECTION.md) |
| Quality metrics | [references/QUALITY_METRICS.md](references/QUALITY_METRICS.md) |
| Automated curation | [references/AUTOMATED_CURATION.md](references/AUTOMATED_CURATION.md) |
| AI-assisted curation | [references/AI_CURATION.md](references/AI_CURATION.md) |
| Waveform analysis | [references/ANALYSIS.md](references/ANALYSIS.md) |

## Installation

```bash
# Core packages
pip install spikeinterface[full] probeinterface neo

# Spike sorters
pip install kilosort          # Kilosort4 (GPU required)
pip install spykingcircus     # SpykingCircus2 (CPU)
pip install mountainsort5     # Mountainsort5 (CPU)

# Our toolkit ships as local scripts (scripts/) — no pip install needed;
# run them directly or import from scripts.neuropixels_pipeline

# Optional: AI curation
pip install anthropic

# Optional: IBL tools
pip install ibl-neuropixel ibllib
```

## Project Structure

```
project/
├── raw_data/
│   └── recording_g0/
│       └── recording_g0_imec0/
│           ├── recording_g0_t0.imec0.ap.bin
│           └── recording_g0_t0.imec0.ap.meta
├── preprocessed/           # Saved preprocessed recording
├── motion/                 # Motion estimation results
├── sorting_output/         # Spike sorter output
├── analyzer/               # SortingAnalyzer (waveforms, metrics)
├── phy_export/             # For manual curation
├── ai_curation/            # AI analysis reports
└── results/
    ├── quality_metrics.csv
    ├── curation_labels.json
    └── output.nwb
```

## Additional Resources

- **SpikeInterface Docs**: https://spikeinterface.readthedocs.io/
- **Neuropixels Tutorial**: https://spikeinterface.readthedocs.io/en/stable/how_to/analyze_neuropixels.html
- **Kilosort4 GitHub**: https://github.com/MouseLand/Kilosort
- **IBL Neuropixel Tools**: https://github.com/int-brain-lab/ibl-neuropixel
- **Allen Institute ecephys**: https://github.com/AllenInstitute/ecephys_spike_sorting
- **Bombcell (Automated QC)**: https://github.com/Julie-Fabre/bombcell
- **SpikeAgent (AI Curation)**: https://github.com/SpikeAgent/SpikeAgent

