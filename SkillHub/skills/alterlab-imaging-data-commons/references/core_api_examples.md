# IDC Core API — Worked Examples

**Tested with:** idc-index 0.12.3 (IDC data version v24)

Copy-paste recipes for the essential `idc-index` capabilities. The main SKILL.md
summarizes each capability and routes here for runnable code. For specialized
topics (clinical data, cloud storage, DICOMweb, BigQuery, digital pathology,
CLI, SQL patterns, index tables, use cases) load the dedicated guide named in
the SKILL.md Quick Navigation table.

All examples assume:

```python
from idc_index import IDCClient
client = IDCClient()
```

## 1. Data Discovery and Exploration

Discover what imaging collections and data are available in IDC:

```python
# Get summary statistics from primary index
query = """
SELECT
  collection_id,
  COUNT(DISTINCT PatientID) as patients,
  COUNT(DISTINCT SeriesInstanceUID) as series,
  SUM(series_size_MB) as size_mb
FROM index
GROUP BY collection_id
ORDER BY patients DESC
"""
collections_summary = client.sql_query(query)

# For richer collection metadata, use collections_index
client.fetch_index("collections_index")
collections_info = client.sql_query("""
    SELECT collection_id, CancerTypes, TumorLocations, Species, Subjects, SupportingData
    FROM collections_index
""")

# For analysis results (annotations, segmentations), use analysis_results_index
client.fetch_index("analysis_results_index")
analysis_info = client.sql_query("""
    SELECT analysis_result_id, analysis_result_title, Subjects, Collections, Modalities
    FROM analysis_results_index
""")
```

**`collections_index`** provides curated metadata per collection: cancer types, tumor locations, species, subject counts, and supporting data types — without needing to aggregate from the primary index.

**`analysis_results_index`** lists derived datasets (AI segmentations, expert annotations, radiomics features) with their source collections and modalities.

## 2. Querying Metadata with SQL

Query the IDC mini-index using SQL to find specific datasets.

**First, explore available values for filter columns:**
```python
# Check what Modality values exist
modalities = client.sql_query("""
    SELECT DISTINCT Modality, COUNT(*) as series_count
    FROM index
    GROUP BY Modality
    ORDER BY series_count DESC
""")
print(modalities)

# Check what BodyPartExamined values exist for MR modality
body_parts = client.sql_query("""
    SELECT DISTINCT BodyPartExamined, COUNT(*) as series_count
    FROM index
    WHERE Modality = 'MR' AND BodyPartExamined IS NOT NULL
    GROUP BY BodyPartExamined
    ORDER BY series_count DESC
    LIMIT 20
""")
print(body_parts)
```

**Then query with validated filter values:**
```python
# Find breast MRI scans (use actual values from exploration above)
results = client.sql_query("""
    SELECT
      collection_id,
      PatientID,
      SeriesInstanceUID,
      Modality,
      SeriesDescription,
      license_short_name
    FROM index
    WHERE Modality = 'MR'
      AND BodyPartExamined = 'BREAST'
    LIMIT 20
""")

# Access results as pandas DataFrame
for idx, row in results.iterrows():
    print(f"Patient: {row['PatientID']}, Series: {row['SeriesInstanceUID']}")
```

**To filter by cancer type, join with `collections_index`:**
```python
client.fetch_index("collections_index")
results = client.sql_query("""
    SELECT i.collection_id, i.PatientID, i.SeriesInstanceUID, i.Modality
    FROM index i
    JOIN collections_index c ON i.collection_id = c.collection_id
    WHERE c.CancerTypes LIKE '%Breast%'
      AND i.Modality = 'MR'
    LIMIT 20
""")
```

**Available metadata fields** (use `client.indices_overview` for complete list):
- Identifiers: collection_id, PatientID, StudyInstanceUID, SeriesInstanceUID
- Imaging: Modality, BodyPartExamined, Manufacturer, ManufacturerModelName
- Clinical: PatientAge, PatientSex, StudyDate
- Descriptions: StudyDescription, SeriesDescription
- Licensing: license_short_name

**Note:** Cancer type is in `collections_index.CancerTypes`, not in the primary `index` table.

## 3. Downloading DICOM Files

Download imaging data efficiently from IDC's cloud storage:

**Download entire collection:**
```python
# Download small collection (RIDER Pilot ~1GB)
client.download_from_selection(
    collection_id="rider_pilot",
    downloadDir="./data/rider"
)
```

**Download specific series:**
```python
# First, query for series UIDs
series_df = client.sql_query("""
    SELECT SeriesInstanceUID
    FROM index
    WHERE Modality = 'CT'
      AND BodyPartExamined = 'CHEST'
      AND collection_id = 'nlst'
    LIMIT 5
""")

# Download only those series
client.download_from_selection(
    seriesInstanceUID=list(series_df['SeriesInstanceUID'].values),
    downloadDir="./data/lung_ct"
)
```

**Custom directory structure:**

Default `dirTemplate`: `%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`

```python
# Simplified hierarchy (omit StudyInstanceUID level)
client.download_from_selection(
    collection_id="tcga_luad",
    downloadDir="./data",
    dirTemplate="%collection_id/%PatientID/%Modality"
)
# Results in: ./data/tcga_luad/TCGA-05-4244/CT/

# Flat structure (all files in one directory)
client.download_from_selection(
    seriesInstanceUID=list(series_df['SeriesInstanceUID'].values),
    downloadDir="./data/flat",
    dirTemplate=""
)
# Results in: ./data/flat/*.dcm
```

**Downloaded file names:**

Individual DICOM files are named using their CRDC instance UUID: `<crdc_instance_uuid>.dcm` (e.g., `0d73f84e-70ae-4eeb-96a0-1c613b5d9229.dcm`). This UUID-based naming:
- Enables version tracking (UUIDs change when file content changes)
- Matches cloud storage organization (`s3://idc-open-data/<crdc_series_uuid>/<crdc_instance_uuid>.dcm`)
- Differs from DICOM UIDs (SOPInstanceUID) which are preserved inside the file metadata

To identify files, use the `crdc_instance_uuid` column in queries or read DICOM metadata (SOPInstanceUID) from the files.

### Command-Line Download

The `idc download` command provides command-line access to download functionality without writing Python code. Available after installing `idc-index`.

**Auto-detects input type:** manifest file path, or identifiers (collection_id, PatientID, StudyInstanceUID, SeriesInstanceUID, crdc_series_uuid).

```bash
# Download entire collection
idc download rider_pilot --download-dir ./data

# Download specific series by UID
idc download "1.3.6.1.4.1.9328.50.1.69736" --download-dir ./data

# Download multiple items (comma-separated)
idc download "tcga_luad,tcga_lusc" --download-dir ./data

# Download from manifest file (auto-detected)
idc download manifest.txt --download-dir ./data
```

**Options:**

| Option | Description |
|--------|-------------|
| `--download-dir` | Output directory (default: current directory) |
| `--dir-template` | Directory hierarchy template (default: `%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`) |
| `--log-level` | Verbosity: debug, info, warning, error, critical |

**Manifest files:**

Manifest files contain S3 URLs (one per line) and can be:
- Exported from the IDC Portal after cohort selection
- Shared by collaborators for reproducible data access
- Generated programmatically from query results

Format (one S3 URL per line):
```
s3://idc-open-data/cb09464a-c5cc-4428-9339-d7fa87cfe837/*
s3://idc-open-data/88f3990d-bdef-49cd-9b2b-4787767240f2/*
```

**Example: Generate manifest from Python query:**

```python
# Query for series URLs
results = client.sql_query("""
    SELECT series_aws_url
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
""")

# Save as manifest file
with open('ct_manifest.txt', 'w') as f:
    for url in results['series_aws_url']:
        f.write(url + '\n')
```

Then download:
```bash
idc download ct_manifest.txt --download-dir ./ct_data
```

## 4. Visualizing IDC Images

View DICOM data in browser without downloading:

```python
import webbrowser

# First query to get valid UIDs
results = client.sql_query("""
    SELECT SeriesInstanceUID, StudyInstanceUID
    FROM index
    WHERE collection_id = 'rider_pilot' AND Modality = 'CT'
    LIMIT 1
""")

# View single series
viewer_url = client.get_viewer_URL(seriesInstanceUID=results.iloc[0]['SeriesInstanceUID'])
webbrowser.open(viewer_url)

# View all series in a study (useful for multi-series exams like MRI protocols)
viewer_url = client.get_viewer_URL(studyInstanceUID=results.iloc[0]['StudyInstanceUID'])
webbrowser.open(viewer_url)
```

The method automatically selects OHIF v3 for radiology or SLIM for slide microscopy. Viewing by study is useful when a DICOM Study contains multiple Series (e.g., T1, T2, DWI sequences from a single MRI session).

## 5. Understanding and Checking Licenses

Check data licensing before use (critical for commercial applications):

```python
# Check licenses for all collections
query = """
SELECT DISTINCT
  collection_id,
  license_short_name,
  COUNT(DISTINCT SeriesInstanceUID) as series_count
FROM index
GROUP BY collection_id, license_short_name
ORDER BY collection_id
"""

licenses = client.sql_query(query)
print(licenses)
```

**License types in IDC:**
- **CC BY 4.0** / **CC BY 3.0** (~97% of data) - Allows commercial use with attribution
- **CC BY-NC 4.0** / **CC BY-NC 3.0** (~3% of data) - Non-commercial use only
- **Custom licenses** (rare) - Some collections have specific terms (e.g., NLM Terms and Conditions)

**Important:** Always check the license before using IDC data in publications or commercial applications. Each DICOM file is tagged with its specific license in metadata.

### Generating Citations for Attribution

The `source_DOI` column contains DOIs linking to publications describing how the data was generated. To satisfy attribution requirements, use `citations_from_selection()` to generate properly formatted citations:

```python
# Get citations for a collection (APA format by default)
citations = client.citations_from_selection(collection_id="rider_pilot")
for citation in citations:
    print(citation)

# Get citations for specific series
results = client.sql_query("""
    SELECT SeriesInstanceUID FROM index
    WHERE collection_id = 'tcga_luad' LIMIT 5
""")
citations = client.citations_from_selection(
    seriesInstanceUID=list(results['SeriesInstanceUID'].values)
)

# Alternative format: BibTeX (for LaTeX documents)
bibtex_citations = client.citations_from_selection(
    collection_id="tcga_luad",
    citation_format=IDCClient.CITATION_FORMAT_BIBTEX
)
```

**Parameters:**
- `collection_id`: Filter by collection(s)
- `patientId`: Filter by patient ID(s)
- `studyInstanceUID`: Filter by study UID(s)
- `seriesInstanceUID`: Filter by series UID(s)
- `citation_format`: Use `IDCClient.CITATION_FORMAT_*` constants:
  - `CITATION_FORMAT_APA` (default) - APA style
  - `CITATION_FORMAT_BIBTEX` - BibTeX for LaTeX
  - `CITATION_FORMAT_JSON` - CSL JSON
  - `CITATION_FORMAT_TURTLE` - RDF Turtle

**Best practice:** When publishing results using IDC data, include the generated citations to properly attribute the data sources and satisfy license requirements.

## 6. Batch Processing and Filtering

Process large datasets efficiently with filtering:

```python
import pandas as pd

# Find chest CT scans from GE scanners
query = """
SELECT
  SeriesInstanceUID,
  PatientID,
  collection_id,
  ManufacturerModelName
FROM index
WHERE Modality = 'CT'
  AND BodyPartExamined = 'CHEST'
  AND Manufacturer = 'GE MEDICAL SYSTEMS'
  AND license_short_name = 'CC BY 4.0'
LIMIT 100
"""

results = client.sql_query(query)

# Save manifest for later
results.to_csv('lung_ct_manifest.csv', index=False)

# Download in batches to avoid timeout
batch_size = 10
for i in range(0, len(results), batch_size):
    batch = results.iloc[i:i+batch_size]
    client.download_from_selection(
        seriesInstanceUID=list(batch['SeriesInstanceUID'].values),
        downloadDir=f"./data/batch_{i//batch_size}"
    )
```

## 7. Advanced Queries with BigQuery

For queries requiring full DICOM metadata, complex JOINs, clinical data tables, or private DICOM elements, use Google BigQuery. Requires GCP account with billing enabled.

**Quick reference:**
- Dataset: `bigquery-public-data.idc_current.*`
- Main table: `dicom_all` (combined metadata)
- Full metadata: `dicom_metadata` (all DICOM tags)
- Private elements: `OtherElements` column (vendor-specific tags like diffusion b-values)

See `bigquery_guide.md` for setup, table schemas, query patterns, private element access, and cost optimization.

**Before using BigQuery**, always check if a specialized index table already has the metadata you need:
1. Use `client.indices_overview` or the [idc-index indices reference](https://idc-index.readthedocs.io/en/latest/indices_reference.html) to discover all available tables and their columns
2. Fetch the relevant index: `client.fetch_index("table_name")`
3. Query locally with `client.sql_query()` (free, no GCP account needed)

Common specialized indices: `seg_index` (segmentations), `ann_index` / `ann_group_index` (microscopy annotations), `sm_index` (slide microscopy), `collections_index` (collection metadata). Only use BigQuery if you need private DICOM elements or attributes not in any index.

## 8. Tool Selection Guide

| Task | Tool | Reference |
|------|------|-----------|
| Programmatic queries & downloads | `idc-index` | Main SKILL.md |
| Interactive exploration | IDC Portal | https://portal.imaging.datacommons.cancer.gov/ |
| Complex metadata queries | BigQuery | `bigquery_guide.md` |
| 3D visualization & analysis | SlicerIDCBrowser | https://github.com/ImagingDataCommons/SlicerIDCBrowser |

**Default choice:** Use `idc-index` for most tasks (no auth, easy API, batch downloads).

## 9. Integration with Analysis Pipelines

Integrate IDC data into imaging analysis workflows:

**Read downloaded DICOM files:**
```python
import pydicom
import os

# Read DICOM files from downloaded series
series_dir = "./data/rider/rider_pilot/RIDER-1007893286/CT_1.3.6.1..."

dicom_files = [os.path.join(series_dir, f) for f in os.listdir(series_dir)
               if f.endswith('.dcm')]

# Load first image
ds = pydicom.dcmread(dicom_files[0])
print(f"Patient ID: {ds.PatientID}")
print(f"Modality: {ds.Modality}")
print(f"Image shape: {ds.pixel_array.shape}")
```

**Build 3D volume from CT series:**
```python
import pydicom
import numpy as np
from pathlib import Path

def load_ct_series(series_path):
    """Load CT series as 3D numpy array"""
    files = sorted(Path(series_path).glob('*.dcm'))
    slices = [pydicom.dcmread(str(f)) for f in files]

    # Sort by slice location
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))

    # Stack into 3D array
    volume = np.stack([s.pixel_array for s in slices])

    return volume, slices[0]  # Return volume and first slice for metadata

volume, metadata = load_ct_series("./data/lung_ct/series_dir")
print(f"Volume shape: {volume.shape}")  # (z, y, x)
```

**Integrate with SimpleITK:**
```python
import SimpleITK as sitk
from pathlib import Path

# Read DICOM series
series_path = "./data/ct_series"
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(series_path)
reader.SetFileNames(dicom_names)
image = reader.Execute()

# Apply processing
smoothed = sitk.CurvatureFlow(image1=image, timeStep=0.125, numberOfIterations=5)

# Save as NIfTI
sitk.WriteImage(smoothed, "processed_volume.nii.gz")
```
