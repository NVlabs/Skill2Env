# Matchms Importing and Exporting Reference

This document details all file format support in matchms for loading and saving mass spectrometry data.

## Importing Spectra

Matchms provides dedicated functions for loading spectra from various file formats. All import functions return generators for memory-efficient processing of large files.

### Common Import Pattern

```python
from matchms.importing import load_from_mgf

# Load spectra (returns generator)
spectra_generator = load_from_mgf("spectra.mgf")

# Convert to list for processing
spectra = list(spectra_generator)
```

## Supported Import Formats

### MGF (Mascot Generic Format)

**Function**: `load_from_mgf(filename, metadata_harmonization=True)`

**Description**: Loads spectra from MGF files, a common format for mass spectrometry data exchange.

**Parameters**:
- `filename` (str): Path to MGF file
- `metadata_harmonization` (bool, default=True): Apply automatic metadata key harmonization

**Example**:
```python
from matchms.importing import load_from_mgf

# Load with metadata harmonization
spectra = list(load_from_mgf("data.mgf"))

# Load without harmonization
spectra = list(load_from_mgf("data.mgf", metadata_harmonization=False))
```

**MGF Format**: Text-based format with BEGIN IONS/END IONS blocks containing metadata and peak lists.

---

### MSP (NIST Mass Spectral Library Format)

**Function**: `load_from_msp(filename, metadata_harmonization=True)`

**Description**: Loads spectra from MSP files, commonly used for spectral libraries.

**Parameters**:
- `filename` (str): Path to MSP file
- `metadata_harmonization` (bool, default=True): Apply automatic metadata harmonization

**Example**:
```python
from matchms.importing import load_from_msp

spectra = list(load_from_msp("library.msp"))
```

**MSP Format**: Text-based format with Name/MW/Comment fields followed by peak lists.

---

### mzML (Mass Spectrometry Markup Language)

**Function**: `load_from_mzml(filename, ms_level=2, metadata_harmonization=True)`

**Description**: Loads spectra from mzML files, the standard XML-based format for raw mass spectrometry data.

**Parameters**:
- `filename` (str): Path to mzML file
- `ms_level` (int, default=2): MS level to extract (1 for MS1, 2 for MS2/tandem)
- `metadata_harmonization` (bool, default=True): Apply automatic metadata harmonization

**Example**:
```python
from matchms.importing import load_from_mzml

# Load MS2 spectra (default)
ms2_spectra = list(load_from_mzml("data.mzML"))

# Load MS1 spectra
ms1_spectra = list(load_from_mzml("data.mzML", ms_level=1))
```

**mzML Format**: XML-based standard format containing raw instrument data and rich metadata.

---

### mzXML

**Function**: `load_from_mzxml(filename, ms_level=2, metadata_harmonization=True)`

**Description**: Loads spectra from mzXML files, an earlier XML-based format for mass spectrometry data.

**Parameters**:
- `filename` (str): Path to mzXML file
- `ms_level` (int, default=2): MS level to extract
- `metadata_harmonization` (bool, default=True): Apply automatic metadata harmonization

**Example**:
```python
from matchms.importing import load_from_mzxml

spectra = list(load_from_mzxml("data.mzXML"))
```

**mzXML Format**: XML-based format, predecessor to mzML.

---

### JSON (GNPS Format)

**Function**: `load_from_json(filename, metadata_harmonization=True)`

**Description**: Loads spectra from JSON files, particularly GNPS-compatible JSON format.

**Parameters**:
- `filename` (str): Path to JSON file
- `metadata_harmonization` (bool, default=True): Apply automatic metadata harmonization

**Example**:
```python
from matchms.importing import load_from_json

spectra = list(load_from_json("spectra.json"))
```

**JSON Format**: Structured JSON with spectrum metadata and peak arrays.

---

### Pickle (Python Serialization)

**Function**: `load_from_pickle(filename, metadata_harmonization)`

**Description**: Loads previously saved matchms Spectrum objects from pickle files. Fast loading of preprocessed spectra.

**Parameters**:
- `filename` (str): Path to pickle file
- `metadata_harmonization` (bool): Whether to re-harmonize metadata keys on load. This argument is **required** (no default).

**Example**:
```python
from matchms.importing import load_from_pickle

spectra = list(load_from_pickle("processed_spectra.pkl", metadata_harmonization=False))
```

**Use case**: Saving and loading preprocessed spectra for faster subsequent analyses.

**Note**: There is no `matchms.exporting.save_as_pickle`. Pickle files are written with Python's own `pickle.dump(spectra, file)` (see the Pickle Export section).

---

### USI (Universal Spectrum Identifier)

**Function**: `load_from_usi(usi)`

**Description**: Loads a single spectrum from a metabolomics USI reference.

**Parameters**:
- `usi` (str): Universal Spectrum Identifier string

**Example**:
```python
from matchms.importing import load_from_usi

usi = "mzspec:GNPS:TASK-...:spectrum..."
spectrum = load_from_usi(usi)
```

**USI Format**: Standardized identifier for accessing spectra from online repositories.

---

## Exporting Spectra

Matchms provides functions to save processed spectra to various formats for sharing and archival.

> Heads up — the append/mode argument differs per function and is **not** `write_mode`: it is `file_mode` for MGF, `mode` for MSP, and JSON has no mode argument at all. For MGF/MSP the default is `"a"` (append), so writing repeatedly to the same path concatenates — delete the file first or pass `"w"` to overwrite.

### MGF Export

**Function**: `save_as_mgf(spectra, filename, file_mode="a")`

**Description**: Saves spectra to MGF format.

**Parameters**:
- `spectra` (list): List of Spectrum objects to save
- `filename` (str): Output file path
- `file_mode` (str, default="a"): `"a"` to append, `"w"` to overwrite

**Example**:
```python
from matchms.exporting import save_as_mgf

save_as_mgf(processed_spectra, "output.mgf", file_mode="w")  # overwrite
```

---

### MSP Export

**Function**: `save_as_msp(spectra, filename, mode="a")`

**Description**: Saves spectra to MSP format.

**Parameters**:
- `spectra` (list): List of Spectrum objects to save
- `filename` (str): Output file path (must end in `.msp`)
- `mode` (str, default="a"): `"a"` to append, `"w"` to overwrite

**Example**:
```python
from matchms.exporting import save_as_msp

save_as_msp(library_spectra, "library.msp", mode="w")
```

---

### JSON Export

**Function**: `save_as_json(spectra, filename, export_style="matchms")`

**Description**: Saves spectra to JSON format. Always overwrites (`filename` is opened in `"w"` mode); there is no append option.

**Parameters**:
- `spectra` (list): List of Spectrum objects to save
- `filename` (str): Output file path
- `export_style` (str, default="matchms"): metadata key style — e.g. `"matchms"` or `"gnps"`

**Example**:
```python
from matchms.exporting import save_as_json

save_as_json(spectra, "spectra.json")
```

---

### Pickle Export

**There is no `save_as_pickle` in matchms.** Write pickle files with Python's standard `pickle` module; read them back with `matchms.importing.load_from_pickle`.

**Description**: Saves spectra as a Python pickle file. Preserves all Spectrum attributes and is fastest for loading.

**Example**:
```python
import pickle

with open("processed.pkl", "wb") as f:
    pickle.dump(processed_spectra, f)

# Reload:
from matchms.importing import load_from_pickle
spectra = list(load_from_pickle("processed.pkl", metadata_harmonization=False))
```

> For the supported text/standard formats use the dedicated `save_as_mgf` / `save_as_msp` / `save_as_json` functions (or the generic `save_spectra(spectra, "out.mgf")`, which dispatches by file extension and does NOT accept `.pkl`).

**Advantages**:
- Fast save and load
- Preserves exact Spectrum state
- No format conversion overhead

**Disadvantages**:
- Not human-readable
- Python-specific (not portable to other languages)
- Pickle format may not be compatible across Python versions

---

## Complete Import/Export Workflow

### Preprocessing and Saving Pipeline

```python
import pickle
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf
from matchms.filtering import default_filters, normalize_intensities
from matchms.filtering import select_by_relative_intensity

# Load raw spectra
spectra = list(load_from_mgf("raw_data.mgf"))

# Process spectra (filters can return None for invalid spectra — bail early)
processed = []
for spectrum in spectra:
    spectrum = default_filters(spectrum)
    spectrum = normalize_intensities(spectrum)
    spectrum = select_by_relative_intensity(spectrum, intensity_from=0.01)
    if spectrum is not None:
        processed.append(spectrum)

# Save processed spectra (MGF for sharing)
save_as_mgf(processed, "processed_data.mgf")

# Save as pickle for fast reloading (no save_as_pickle helper — use stdlib pickle)
with open("processed_data.pkl", "wb") as f:
    pickle.dump(processed, f)
```

### Format Conversion

```python
from matchms.importing import load_from_mzml
from matchms.exporting import save_as_mgf, save_as_msp

# Convert mzML to MGF
spectra = list(load_from_mzml("data.mzML", ms_level=2))
save_as_mgf(spectra, "data.mgf")

# Convert to MSP library format
save_as_msp(spectra, "data.msp")
```

### Loading from Multiple Files

```python
from matchms.importing import load_from_mgf
import glob

# Load all MGF files in directory
all_spectra = []
for mgf_file in glob.glob("data/*.mgf"):
    spectra = list(load_from_mgf(mgf_file))
    all_spectra.extend(spectra)

print(f"Loaded {len(all_spectra)} spectra from multiple files")
```

### Memory-Efficient Processing

```python
from matchms.importing import load_from_mgf
from matchms.exporting import save_as_mgf
from matchms.filtering import default_filters, normalize_intensities

# Process large file without loading all into memory
import os

def process_spectrum(spectrum):
    spectrum = default_filters(spectrum)
    spectrum = normalize_intensities(spectrum)
    return spectrum

# Stream processing. save_as_mgf takes a FILENAME (not an open handle) and
# defaults to file_mode="a" (append), so each call appends one spectrum. Start
# from a clean file so a previous run's output is not concatenated.
out_path = "output.mgf"
if os.path.exists(out_path):
    os.remove(out_path)

for spectrum in load_from_mgf("large_file.mgf"):
    processed = process_spectrum(spectrum)
    if processed is not None:
        save_as_mgf([processed], out_path, file_mode="a")
```

## Format Selection Guidelines

**MGF**:
- ✓ Widely supported
- ✓ Human-readable
- ✓ Good for data sharing
- ✓ Moderate file size
- Best for: Data exchange, GNPS uploads, publication data

**MSP**:
- ✓ Spectral library standard
- ✓ Human-readable
- ✓ Good metadata support
- Best for: Reference libraries, NIST format compatibility

**JSON**:
- ✓ Structured format
- ✓ GNPS compatible
- ✓ Easy to parse programmatically
- Best for: Web applications, GNPS integration, structured data

**Pickle**:
- ✓ Fastest save/load
- ✓ Preserves exact state
- ✗ Not portable to other languages
- ✗ Not human-readable
- Best for: Intermediate processing, Python-only workflows

**mzML/mzXML**:
- ✓ Raw instrument data
- ✓ Rich metadata
- ✓ Industry standard
- ✗ Large file size
- ✗ Slower to parse
- Best for: Raw data archival, multi-level MS data

## Metadata Harmonization

The `metadata_harmonization` parameter (available in most import functions) automatically standardizes metadata keys:

```python
# Without harmonization
spectrum = load_from_mgf("data.mgf", metadata_harmonization=False)
# May have: "PRECURSOR_MZ", "Precursor_mz", "precursormz"

# With harmonization (default)
spectrum = load_from_mgf("data.mgf", metadata_harmonization=True)
# Standardized to: "precursor_mz"
```

**Recommended**: Keep harmonization enabled (default) for consistent metadata access across different data sources.

## File Format Specifications

For detailed format specifications:
- **MGF**: http://www.matrixscience.com/help/data_file_help.html
- **MSP**: https://chemdata.nist.gov/mass-spc/ms-search/
- **mzML**: http://www.psidev.info/mzML
- **GNPS JSON**: https://gnps.ucsd.edu/

## Further Reading

For complete API documentation:
https://matchms.readthedocs.io/en/latest/api/matchms.importing.html
https://matchms.readthedocs.io/en/latest/api/matchms.exporting.html
