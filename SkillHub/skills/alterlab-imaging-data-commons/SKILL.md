---
name: alterlab-imaging-data-commons
description: Query and download public cancer imaging data from the NCI Imaging Data Commons (IDC) using the idc-index Python package, filtering by metadata, visualizing in-browser, and checking licenses, with no authentication required. Use when obtaining large-scale radiology (CT, MR, PET) or digital pathology DICOM datasets for AI/ML training or cancer imaging research. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: Requires the idc-index Python package (pinned to 0.12.3, IDC data release v24); keyless IDC data access (no authentication required)
metadata:
    version: "1.5.1"
    skill-author: AlterLab
    skill-source: https://github.com/ImagingDataCommons/idc-claude-skill
---

# Imaging Data Commons

## Overview

Use the `idc-index` Python package to query and download public cancer imaging data from the National Cancer Institute Imaging Data Commons (IDC). No authentication required for data access.

**Current IDC Data Version: v24** (always verify with `IDCClient().get_idc_version()`)

**Primary tool:** `idc-index` ([GitHub](https://github.com/imagingdatacommons/idc-index))

**CRITICAL - Check package version and upgrade if needed (run this FIRST):**

```python
from importlib.metadata import version as _v
from packaging.version import Version

REQUIRED_VERSION = "0.12.3"  # Must match metadata.idc-index in this file
installed = _v("idc-index")

# Compare as versions, not strings ("0.9.0" < "0.11.0" is False as a string).
if Version(installed) < Version(REQUIRED_VERSION):
    print(f"idc-index {installed} is older than {REQUIRED_VERSION}; upgrade with:")
    print("    pip install --upgrade idc-index   # or: uv pip install --upgrade idc-index")
    print("Then restart Python to load the new version.")
else:
    print(f"idc-index {installed} meets requirement ({REQUIRED_VERSION})")
```

**Verify IDC data version and check current data scale:**

```python
from idc_index import IDCClient
client = IDCClient()

# Verify IDC data version (should be "v24")
print(f"IDC data version: {client.get_idc_version()}")

# Get collection count and total series
stats = client.sql_query("""
    SELECT
        COUNT(DISTINCT collection_id) as collections,
        COUNT(DISTINCT analysis_result_id) as analysis_results,
        COUNT(DISTINCT PatientID) as patients,
        COUNT(DISTINCT StudyInstanceUID) as studies,
        COUNT(DISTINCT SeriesInstanceUID) as series,
        SUM(instanceCount) as instances,
        SUM(series_size_MB)/1000000 as size_TB
    FROM index
""")
print(stats)
```

**Core workflow:**
1. Query metadata → `client.sql_query()`
2. Download DICOM files → `client.download_from_selection()`
3. Visualize in browser → `client.get_viewer_URL(seriesInstanceUID=...)`

## Scripts

`scripts/query_imaging_data_commons.py` — CLI wrapper over the `idc-index` package (JSON to stdout; `pip install --upgrade idc-index`):

```bash
python scripts/query_imaging_data_commons.py version                 # IDC data version
python scripts/query_imaging_data_commons.py collections --limit 50   # collections + counts
python scripts/query_imaging_data_commons.py sql "SELECT * FROM index LIMIT 5"   # raw SQL
```

## When to Use This Skill

- Finding publicly available radiology (CT, MR, PET) or pathology (slide microscopy) images
- Selecting image subsets by cancer type, modality, anatomical site, or other metadata
- Downloading DICOM data from IDC
- Checking data licenses before use in research or commercial applications
- Visualizing medical images in a browser without local DICOM viewer software

## Quick Navigation

**Core Sections (inline):**
- IDC Data Model - Collection and analysis result hierarchy
- Index Tables - Available tables and joining patterns
- Installation - Package setup and version verification
- Core Capabilities - Essential API patterns (query, download, visualize, license, citations, batch)
- Best Practices - Usage guidelines
- Troubleshooting - Common issues and solutions

**Reference Guides (load on demand):**

| Guide | When to Load |
|-------|--------------|
| `core_api_examples.md` | Runnable code for Core Capabilities §1-§9 (discovery, SQL, download, visualize, license, batch, BigQuery, pipelines) |
| `index_tables_guide.md` | Complex JOINs, schema discovery, DataFrame access |
| `use_cases.md` | End-to-end workflow examples (training datasets, batch downloads) |
| `sql_patterns.md` | Quick SQL patterns for filter discovery, annotations, size estimation |
| `clinical_data_guide.md` | Clinical/tabular data, imaging+clinical joins, value mapping |
| `cloud_storage_guide.md` | Direct S3/GCS access, versioning, UUID mapping |
| `dicomweb_guide.md` | DICOMweb endpoints, PACS integration |
| `digital_pathology_guide.md` | Slide microscopy (SM), annotations (ANN), pathology workflows |
| `bigquery_guide.md` | Full DICOM metadata, private elements (requires GCP) |
| `cli_guide.md` | Command-line tools (`idc download`, manifest files) |

## IDC Data Model

IDC adds two grouping levels above the standard DICOM hierarchy (Patient → Study → Series → Instance):

- **collection_id**: Groups patients by disease, modality, or research focus (e.g., `tcga_luad`, `nlst`). A patient belongs to exactly one collection.
- **analysis_result_id**: Identifies derived objects (segmentations, annotations, radiomics features) across one or more original collections.

Use `collection_id` to find original imaging data, may include annotations deposited along with the images; use `analysis_result_id` to find AI-generated or expert annotations.

**Key identifiers for queries:**
| Identifier | Scope | Use for |
|------------|-------|---------|
| `collection_id` | Dataset grouping | Filtering by project/study |
| `PatientID` | Patient | Grouping images by patient |
| `StudyInstanceUID` | DICOM study | Grouping of related series, visualization |
| `SeriesInstanceUID` | DICOM series | Grouping of related series, visualization |

## Index Tables

The `idc-index` package provides multiple metadata index tables, accessible via SQL or as pandas DataFrames.

**Complete index table documentation:** Use https://idc-index.readthedocs.io/en/latest/indices_reference.html for quick check of available tables and columns without executing any code.

**Important:** Use `client.indices_overview` to get current table descriptions and column schemas. This is the authoritative source for available columns and their types — always query it when writing SQL or exploring data structure.

### Available Tables

| Table | Row Granularity | Loaded | Description |
|-------|-----------------|--------|-------------|
| `index` | 1 row = 1 DICOM series | Auto | Primary metadata for all current IDC data |
| `prior_versions_index` | 1 row = 1 DICOM series | Auto | Series from previous IDC releases; for downloading deprecated data |
| `collections_index` | 1 row = 1 collection | fetch_index() | Collection-level metadata and descriptions |
| `analysis_results_index` | 1 row = 1 analysis result collection | fetch_index() | Metadata about derived datasets (annotations, segmentations) |
| `clinical_index` | 1 row = 1 clinical data column | fetch_index() | Dictionary mapping clinical table columns to collections |
| `sm_index` | 1 row = 1 slide microscopy series | fetch_index() | Slide Microscopy (pathology) series metadata |
| `sm_instance_index` | 1 row = 1 slide microscopy instance | fetch_index() | Instance-level (SOPInstanceUID) metadata for slide microscopy |
| `seg_index` | 1 row = 1 DICOM Segmentation series | fetch_index() | Segmentation metadata: algorithm, segment count, reference to source image series |
| `ann_index` | 1 row = 1 DICOM ANN series | fetch_index() | Microscopy Bulk Simple Annotations series metadata; references annotated image series |
| `ann_group_index` | 1 row = 1 annotation group | fetch_index() | Detailed annotation group metadata: graphic type, annotation count, property codes, algorithm |
| `contrast_index` | 1 row = 1 series with contrast info | fetch_index() | Contrast agent metadata: agent name, ingredient, administration route (CT, MR, PT, XA, RF) |

**Auto** = loaded automatically when `IDCClient()` is instantiated
**fetch_index()** = requires `client.fetch_index("table_name")` to load

### Joining Tables

**Key columns are not explicitly labeled, the following is a subset that can be used in joins.**

| Join Column | Tables | Use Case |
|-------------|--------|----------|
| `collection_id` | index, prior_versions_index, collections_index, clinical_index | Link series to collection metadata or clinical data |
| `SeriesInstanceUID` | index, prior_versions_index, sm_index, sm_instance_index | Link series across tables; connect to slide microscopy details |
| `StudyInstanceUID` | index, prior_versions_index | Link studies across current and historical data |
| `PatientID` | index, prior_versions_index | Link patients across current and historical data |
| `analysis_result_id` | index, analysis_results_index | Link series to analysis result metadata (annotations, segmentations) |
| `source_DOI` | index, analysis_results_index | Link by publication DOI |
| `crdc_series_uuid` | index, prior_versions_index | Link by CRDC unique identifier |
| `Modality` | index, prior_versions_index | Filter by imaging modality |
| `SeriesInstanceUID` | index, seg_index, ann_index, ann_group_index, contrast_index | Link segmentation/annotation/contrast series to its index metadata |
| `segmented_SeriesInstanceUID` | seg_index → index | Link segmentation to its source image series (join seg_index.segmented_SeriesInstanceUID = index.SeriesInstanceUID) |
| `referenced_SeriesInstanceUID` | ann_index → index | Link annotation to its source image series (join ann_index.referenced_SeriesInstanceUID = index.SeriesInstanceUID) |

**Note:** `Subjects`, `Updated`, and `Description` appear in multiple tables but have different meanings (counts vs identifiers, different update contexts).

For detailed join examples, schema discovery patterns, key columns reference, and DataFrame access, see `references/index_tables_guide.md`.

### Clinical Data Access

```python
# Fetch clinical index (also downloads clinical data tables)
client.fetch_index("clinical_index")

# Query clinical index to find available tables and their columns
tables = client.sql_query("SELECT DISTINCT table_name, column_label FROM clinical_index")

# Load a specific clinical table as DataFrame
clinical_df = client.get_clinical_table("table_name")
```

See `references/clinical_data_guide.md` for detailed workflows including value mapping patterns and joining clinical data with imaging.

## Data Access Options

| Method | Auth Required | Best For |
|--------|---------------|----------|
| `idc-index` | No | Key queries and downloads (recommended) |
| IDC Portal | No | Interactive exploration, manual selection, browser-based download |
| BigQuery | Yes (GCP account) | Complex queries, full DICOM metadata |
| DICOMweb proxy | No | Tool integration via DICOMweb API |
| Cloud storage (S3/GCS) | No | Direct file access, bulk downloads, custom pipelines |

**Cloud storage organization**

IDC maintains all DICOM files in public cloud storage buckets mirrored between AWS S3 and Google Cloud Storage. Files are organized by CRDC UUIDs (not DICOM UIDs) to support versioning.

| Bucket (AWS / GCS) | License | Content |
|--------------------|---------|---------|
| `idc-open-data` / `idc-open-data` | No commercial restriction | >90% of IDC data |
| `idc-open-data-two` / `idc-open-idc1` | No commercial restriction | Collections with potential head scans |
| `idc-open-data-cr` / `idc-open-cr` | Commercial use restricted (CC BY-NC) | ~4% of data |

Files are stored as `<crdc_series_uuid>/<crdc_instance_uuid>.dcm`. Access is free (no egress fees) via AWS CLI, gsutil, or s5cmd with anonymous access. Use `series_aws_url` column from the index for S3 URLs; GCS uses the same path structure.

See `references/cloud_storage_guide.md` for bucket details, access commands, UUID mapping, and versioning.

**DICOMweb access**

IDC data is available via DICOMweb interface (Google Cloud Healthcare API implementation) for integration with PACS systems and DICOMweb-compatible tools.

| Endpoint | Auth | Use Case |
|----------|------|----------|
| Public proxy | No | Testing, moderate queries, daily quota |
| Google Healthcare | Yes (GCP) | Production use, higher quotas |

See `references/dicomweb_guide.md` for endpoint URLs, code examples, supported operations, and implementation details.

## Installation and Setup

**Required (for basic access):**
```bash
pip install --upgrade idc-index
```

**Important:** New IDC data release will always trigger a new version of `idc-index`. Always use `--upgrade` flag while installing, unless an older version is needed for reproducibility.

**IMPORTANT:** IDC data version v24 is current. Always verify your version:
```python
print(client.get_idc_version())  # Should return "v24"
```
If you see an older version, upgrade with: `pip install --upgrade idc-index`

**Tested with:** idc-index 0.12.3 (IDC data version v24)

**Optional (for data analysis):**
```bash
pip install pandas numpy pydicom
```

## Core Capabilities

Runnable Python/SQL/CLI recipes for every capability below live in
`references/core_api_examples.md` (numbered §1-§9 matching the headings here).
Load that file when you need copy-paste code; the summaries here give the
routing and the key decisions. All examples assume
`from idc_index import IDCClient; client = IDCClient()`.

### 1. Data Discovery and Exploration

Find available collections and derived datasets:
- Aggregate the primary `index` (patients/series/size per `collection_id`).
- `collections_index` (after `fetch_index`) gives curated per-collection metadata
  (CancerTypes, TumorLocations, Species, Subjects) without aggregating.
- `analysis_results_index` lists derived datasets (AI segmentations, expert
  annotations, radiomics) with source collections and modalities.

Recipes in `core_api_examples.md` §1.

### 2. Querying Metadata with SQL

Two-step pattern: **explore filter values first** (`SELECT DISTINCT Modality …`,
`BodyPartExamined …`), then query with validated values. Access results as a
pandas DataFrame. To filter by cancer type, JOIN `index` with `collections_index`
(cancer type lives in `collections_index.CancerTypes`, not the primary `index`).
Use `client.indices_overview` for the full column list. Recipes in
`core_api_examples.md` §2.

### 3. Downloading DICOM Files

`client.download_from_selection(...)` by `collection_id` or `seriesInstanceUID`,
with `downloadDir` and an optional `dirTemplate` (default
`%collection_id/%PatientID/%StudyInstanceUID/%Modality_%SeriesInstanceUID`; `""`
for a flat layout). Files are named by CRDC instance UUID (`<uuid>.dcm`), not
DICOM UID. The `idc download` CLI mirrors this and auto-detects identifiers vs
manifest files. Recipes, CLI options, and manifest format in
`core_api_examples.md` §3; deeper CLI detail in `references/cli_guide.md`.

### 4. Visualizing IDC Images

`client.get_viewer_URL(seriesInstanceUID=...)` (or `studyInstanceUID=...` for
multi-series exams) returns a browser URL — no download needed. The method picks
OHIF v3 for radiology or SLIM for slide microscopy automatically. Recipe in
`core_api_examples.md` §4.

### 5. Understanding and Checking Licenses

Query `license_short_name` before any use. **CC BY 4.0/3.0** (~97%) allows
commercial use with attribution; **CC BY-NC 4.0/3.0** (~3%) is non-commercial
only; rare custom licenses exist. For attribution, `citations_from_selection()`
generates formatted citations from `source_DOI` (APA default; also BibTeX, JSON,
Turtle via `IDCClient.CITATION_FORMAT_*`). Recipes in `core_api_examples.md` §5.

### 6. Batch Processing and Filtering

Query with filters → save a manifest CSV → download in batches (e.g. 10 series at
a time) to avoid timeouts. Recipe in `core_api_examples.md` §6.

### 7. Advanced Queries with BigQuery

Use BigQuery only when you need full DICOM metadata, complex JOINs, or private
DICOM elements (`OtherElements`). **First check** whether a specialized index
(`seg_index`, `ann_index`/`ann_group_index`, `sm_index`, `collections_index`)
already has the field — local `sql_query` is free and needs no GCP account.
Dataset `bigquery-public-data.idc_current.*`, main table `dicom_all`. See
`references/bigquery_guide.md`; quick reference in `core_api_examples.md` §7.

### 8. Tool Selection Guide

| Task | Tool | Reference |
|------|------|-----------|
| Programmatic queries & downloads | `idc-index` | This document |
| Interactive exploration | IDC Portal | https://portal.imaging.datacommons.cancer.gov/ |
| Complex metadata queries | BigQuery | `references/bigquery_guide.md` |
| 3D visualization & analysis | SlicerIDCBrowser | https://github.com/ImagingDataCommons/SlicerIDCBrowser |

**Default choice:** Use `idc-index` for most tasks (no auth, easy API, batch downloads).

### 9. Integration with Analysis Pipelines

After download, read DICOM with `pydicom`, build 3D volumes by sorting on
`ImagePositionPatient[2]` and stacking `pixel_array`, or read a series with
`SimpleITK.ImageSeriesReader` for processing and NIfTI export. Recipes in
`core_api_examples.md` §9.

## Common Use Cases

See `references/use_cases.md` for complete end-to-end workflow examples including:
- Building deep learning training datasets from lung CT scans
- Comparing image quality across scanner manufacturers
- Previewing data in browser before downloading
- License-aware batch downloads for commercial use

## Best Practices

- **Verify IDC version before generating responses** - Always call `client.get_idc_version()` at the start of a session to confirm you're using the expected data version (currently v24). If using an older version, recommend `pip install --upgrade idc-index`
- **Check licenses before use** - Always query the `license_short_name` field and respect licensing terms (CC BY vs CC BY-NC)
- **Generate citations for attribution** - Use `citations_from_selection()` to get properly formatted citations from `source_DOI` values; include these in publications
- **Start with small queries** - Use `LIMIT` clause when exploring to avoid long downloads and understand data structure
- **Use mini-index for simple queries** - Only use BigQuery when you need comprehensive metadata or complex JOINs
- **Organize downloads with dirTemplate** - Use meaningful directory structures like `%collection_id/%PatientID/%Modality`
- **Cache query results** - Save DataFrames to CSV files to avoid re-querying and ensure reproducibility
- **Estimate size first** - Check collection size before downloading - some collection sizes are in terabytes!
- **Save manifests** - Always save query results with Series UIDs for reproducibility and data provenance
- **Read documentation** - IDC data structure and metadata fields are documented at https://learn.canceridc.dev/
- **Use IDC forum** - Search for questons/answers and ask your questions to the IDC maintainers and users at https://discourse.canceridc.dev/

## Troubleshooting

**Issue: `ModuleNotFoundError: No module named 'idc_index'`**
- **Cause:** idc-index package not installed
- **Solution:** Install with `pip install --upgrade idc-index`

**Issue: Download fails with connection timeout**
- **Cause:** Network instability or large download size
- **Solution:**
  - Download smaller batches (e.g., 10-20 series at a time)
  - Check network connection
  - Use `dirTemplate` to organize downloads by batch
  - Implement retry logic with delays

**Issue: `BigQuery quota exceeded` or billing errors**
- **Cause:** BigQuery requires billing-enabled GCP project
- **Solution:** Use idc-index mini-index for simple queries (no billing required), or see `references/bigquery_guide.md` for cost optimization tips

**Issue: Series UID not found or no data returned**
- **Cause:** Typo in UID, data not in current IDC version, or wrong field name
- **Solution:**
  - Check if data is in current IDC version (some old data may be deprecated)
  - Use `LIMIT 5` to test query first
  - Check field names against metadata schema documentation

**Issue: Downloaded DICOM files won't open**
- **Cause:** Corrupted download or incompatible viewer
- **Solution:**
  - Check DICOM object type (Modality and SOPClassUID attributes) - some object types require specialized tools
  - Verify file integrity (check file sizes)
  - Use pydicom to validate: `pydicom.dcmread(file, force=True)`
  - Try different DICOM viewer (3D Slicer, Horos, RadiAnt, QuPath)
  - Re-download the series

## Common SQL Query Patterns

See `references/sql_patterns.md` for quick-reference SQL patterns including:
- Filter value discovery (modalities, body parts, manufacturers)
- Annotation and segmentation queries (including seg_index, ann_index joins)
- Slide microscopy queries (sm_index patterns)
- Download size estimation
- Clinical data linking

For segmentation and annotation details, also see `references/digital_pathology_guide.md`.

## Related Skills

The following skills complement IDC workflows for downstream analysis and visualization:

### DICOM Processing
- **pydicom** - Read, write, and manipulate downloaded DICOM files. Use for extracting pixel data, reading metadata, anonymization, and format conversion. Essential for working with IDC radiology data (CT, MR, PET).

### Pathology and Slide Microscopy
See `references/digital_pathology_guide.md` for DICOM-compatible tools (highdicom, wsidicom, TIA-Toolbox, Slim viewer).

### Metadata Visualization
- **matplotlib** - Low-level plotting for full customization. Use for creating static figures summarizing IDC query results (bar charts of modalities, histograms of series counts, etc.).
- **seaborn** - Statistical visualization with pandas integration. Use for quick exploration of IDC metadata distributions, relationships between variables, and categorical comparisons with attractive defaults.
- **plotly** - Interactive visualization. Use when you need hover info, zoom, and pan for exploring IDC metadata, or for creating web-embeddable dashboards of collection statistics.

### Data Exploration
- **exploratory-data-analysis** - Comprehensive EDA on scientific data files. Use after downloading IDC data to understand file structure, quality, and characteristics before analysis.

## Resources

### Schema Reference (Primary Source)

**Always use `client.indices_overview` for current column schemas.** This ensures accuracy with the installed idc-index version:

```python
# Get all column names and types for any table
schema = client.indices_overview["index"]["schema"]
columns = [(c['name'], c['type'], c.get('description', '')) for c in schema['columns']]
```

### Reference Documentation

See the Quick Navigation section at the top for the full list of reference guides with decision triggers.

- **[indices_reference](https://idc-index.readthedocs.io/en/latest/indices_reference.html)** - External documentation for index tables (may be ahead of the installed version)

### External Links

- **IDC Portal**: https://portal.imaging.datacommons.cancer.gov/explore/
- **Documentation**: https://learn.canceridc.dev/
- **Tutorials**: https://github.com/ImagingDataCommons/IDC-Tutorials
- **User Forum**: https://discourse.canceridc.dev/
- **idc-index GitHub**: https://github.com/ImagingDataCommons/idc-index
- **Citation**: Fedorov, A., et al. "National Cancer Institute Imaging Data Commons: Toward Transparency, Reproducibility, and Scalability in Imaging Artificial Intelligence." RadioGraphics 43.12 (2023). https://doi.org/10.1148/rg.230180

### Skill Updates

This skill version is available in skill metadata. To check for updates:
- Visit the [releases page](https://github.com/ImagingDataCommons/idc-claude-skill/releases)
- Watch the repository on GitHub (Watch → Custom → Releases)
