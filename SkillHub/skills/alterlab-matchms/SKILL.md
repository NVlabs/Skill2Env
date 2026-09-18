---
name: alterlab-matchms
description: Computes mass-spectral similarity and identifies compounds for metabolomics with matchms — comparing mass spectra, scoring similarity (cosine, modified cosine), and searching spectral libraries to annotate unknowns. Use when matching MS/MS spectra, identifying metabolites, or library searching; for full LC-MS/MS proteomics pipelines use pyopenms. Part of the AlterLab Academic Skills suite.
license: Apache-2.0
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with the skill's Python package installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Matchms

## Overview

Matchms is an open-source Python library for mass spectrometry data processing and analysis. Import spectra from various formats, standardize metadata, filter peaks, calculate spectral similarities, and build reproducible analytical workflows.

## Core Capabilities

### 1. Importing and Exporting Mass Spectrometry Data

Load spectra from multiple file formats and export processed data:

```python
from matchms.importing import load_from_mgf, load_from_mzml, load_from_msp, load_from_json
from matchms.exporting import save_as_mgf, save_as_msp, save_as_json

# Import spectra
spectra = list(load_from_mgf("spectra.mgf"))
spectra = list(load_from_mzml("data.mzML"))
spectra = list(load_from_msp("library.msp"))

# Export processed spectra
save_as_mgf(spectra, "output.mgf")
save_as_json(spectra, "output.json")
```

**Supported formats:**
- mzML and mzXML (raw mass spectrometry formats)
- MGF (Mascot Generic Format)
- MSP (spectral library format)
- JSON (GNPS-compatible)
- metabolomics-USI references
- Pickle (Python serialization)

For detailed importing/exporting documentation, consult `references/importing_exporting.md`.

### 2. Spectrum Filtering and Processing

Apply comprehensive filters to standardize metadata and refine peak data:

```python
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, require_minimum_number_of_peaks

# Apply default metadata harmonization filters
spectrum = default_filters(spectrum)

# Normalize peak intensities
spectrum = normalize_intensities(spectrum)

# Filter peaks by relative intensity
spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01, intensity_to=1.0)

# Require minimum peaks
spectrum = require_minimum_number_of_peaks(spectrum, n_required=5)
```

**Filter categories:**
- **Metadata processing**: Harmonize compound names, derive chemical structures, standardize adducts, correct charges
- **Peak filtering**: Normalize intensities, select by m/z or intensity, remove precursor peaks
- **Quality control**: Require minimum peaks, validate precursor m/z, ensure metadata completeness
- **Chemical annotation**: Add fingerprints, derive InChI/SMILES, repair structural mismatches

Matchms provides 40+ filters. For the complete filter reference, consult `references/filtering.md`.

### 3. Calculating Spectral Similarities

Compare spectra using various similarity metrics:

```python
from matchms import calculate_scores
from matchms.similarity import CosineGreedy, ModifiedCosineGreedy, CosineHungarian

# Calculate cosine similarity (fast, greedy algorithm)
scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=CosineGreedy())

# Calculate modified cosine (accounts for precursor m/z differences)
scores = calculate_scores(references=library_spectra,
                         queries=query_spectra,
                         similarity_function=ModifiedCosineGreedy(tolerance=0.1))

# Get best matches. The cosine functions return a structured score
# (score + matched-peak count), so to SORT you must name the field to
# sort by — `sort=True` alone raises IndexError. The field is
# "<FunctionName>_score", e.g. "ModifiedCosineGreedy_score" / "CosineGreedy_score".
best_matches = scores.scores_by_query(query_spectra[0],
                                      name="ModifiedCosineGreedy_score",
                                      sort=True)[:10]
```

**Available similarity functions:**
- **CosineGreedy/CosineHungarian**: Peak-based cosine similarity with different matching algorithms
- **ModifiedCosineGreedy** (also `ModifiedCosineHungarian`): cosine similarity accounting for precursor mass differences. Note the rename — the class is no longer called `ModifiedCosine`.
- **NeutralLossesCosine**: Similarity based on neutral loss patterns
- **FingerprintSimilarity**: Molecular structure similarity using fingerprints
- **MetadataMatch**: Compare user-defined metadata fields
- **PrecursorMzMatch/ParentMassMatch**: Simple mass-based filtering

For detailed similarity function documentation, consult `references/similarity.md`.

### 4. Building Processing Pipelines

Create reproducible, multi-step analysis workflows:

```python
from matchms import SpectrumProcessor
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity, remove_peaks_around_precursor_mz

# Define a processing pipeline. Each step is a callable, a registered filter
# name (str), or a ("filter_name", {kwargs}) tuple (introspectable via
# processor.processing_steps). NOTE: default_filters is a composite, so pass it
# as the callable — the string "default_filters" is not a registered name.
processor = SpectrumProcessor([
    default_filters,
    "normalize_intensities",
    ("select_by_relative_intensity", {"intensity_from": 0.01}),
    ("remove_peaks_around_precursor_mz", {"mz_tolerance": 17}),
])

# A SpectrumProcessor is NOT callable. Use .process_spectrum() for one
# spectrum, or .process_spectra() for a list (returns a (spectra, report)
# tuple — unpack it, don't treat the result as the spectra list).
processed_spectra, report = processor.process_spectra(spectra)
# single spectrum: processed = processor.process_spectrum(spectrum)
```

### 5. Working with Spectrum Objects

The core `Spectrum` class contains mass spectral data:

```python
from matchms import Spectrum
import numpy as np

# Create a spectrum
mz = np.array([100.0, 150.0, 200.0, 250.0])
intensities = np.array([0.1, 0.5, 0.9, 0.3])
metadata = {"precursor_mz": 250.5, "ionmode": "positive"}

spectrum = Spectrum(mz=mz, intensities=intensities, metadata=metadata)

# Access spectrum properties
print(spectrum.peaks.mz)           # m/z values
print(spectrum.peaks.intensities)  # Intensity values
print(spectrum.get("precursor_mz")) # Metadata field

# Visualize spectra
spectrum.plot()
spectrum.plot_against(reference_spectrum)
```

### 6. Metadata Management

Standardize and harmonize spectrum metadata:

```python
# Metadata is automatically harmonized
spectrum.set("Precursor_mz", 250.5)  # Gets harmonized to lowercase key
print(spectrum.get("precursor_mz"))   # Returns 250.5

# Derive chemical information
from matchms.filtering import derive_inchi_from_smiles, derive_inchikey_from_inchi
from matchms.filtering import add_fingerprint

spectrum = derive_inchi_from_smiles(spectrum)
spectrum = derive_inchikey_from_inchi(spectrum)
# fingerprint_type must be one of: "daylight", "morgan1", "morgan2", "morgan3"
# (the digit is the Morgan radius). Plain "morgan" is NOT valid.
spectrum = add_fingerprint(spectrum, fingerprint_type="morgan2", nbits=2048)
```

## Common Workflows

For typical mass spectrometry analysis workflows, including:
- Loading and preprocessing spectral libraries
- Matching unknown spectra against reference libraries
- Quality filtering and data cleaning
- Large-scale similarity comparisons
- Network-based spectral clustering

Consult `references/workflows.md` for detailed examples.

## Installation

```bash
uv pip install matchms
```

Molecular-structure processing (SMILES/InChI/fingerprints) needs rdkit, which
ships in the base matchms install on current versions — there is no separate
`[chemistry]` extra. If `import rdkit` fails, `uv pip install rdkit` explicitly.

API notes below were verified against **matchms 0.33.x**.

## Version gotchas (verified, matchms 0.33.x)

These trip people up and the code examples here account for them:

- **`SpectrumProcessor` instances are not callable.** Use
  `processor.process_spectrum(spectrum)` for one spectrum or
  `processor.process_spectra(spectra)` for a list — the latter returns a
  `(processed_spectra, report)` tuple, not a bare list.
- **`scores_by_query(query, sort=True)` raises `IndexError`** for cosine-family
  scores. You must pass `name="<FunctionName>_score"` (e.g.
  `"CosineGreedy_score"`) so the structured score knows which field to sort on.
- **`scores.scores[i, j]` is a structured element**, not a float — it carries
  both `..._score` and `..._matches` fields. For plain float matrices use
  `scores.to_array("CosineGreedy_score")`; there is no `to_dataframe`/`to_list`.
- **`add_fingerprint(fingerprint_type=...)`** accepts only `"daylight"`,
  `"morgan1"`, `"morgan2"`, `"morgan3"` (no `"morgan"`, no `radius=` argument).

## Reference Documentation

Detailed reference documentation is available in the `references/` directory:
- `filtering.md` - Complete filter function reference with descriptions
- `similarity.md` - All similarity metrics and when to use them
- `importing_exporting.md` - File format details and I/O operations
- `workflows.md` - Common analysis patterns and examples

Load these references as needed for detailed information about specific matchms capabilities.

