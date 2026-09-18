# AlphaFold Database API Reference

This document provides comprehensive technical documentation for programmatic access to the AlphaFold Protein Structure Database.

## Table of Contents

1. [REST API Endpoints](#rest-api-endpoints)
2. [File Access Patterns](#file-access-patterns)
3. [Data Schemas](#data-schemas)
4. [Google Cloud Access](#google-cloud-access)
5. [BigQuery Schema](#bigquery-schema)
6. [Best Practices](#best-practices)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)

---

## REST API Endpoints

### Base URL

```
https://alphafold.ebi.ac.uk/api/
```

### 1. Get Prediction by UniProt Accession

**Endpoint:** `/prediction/{uniprot_id}`

**Method:** GET

**Description:** Retrieve AlphaFold prediction metadata for a given UniProt accession.

**Parameters:**
- `uniprot_id` (required): UniProt accession (e.g., "P00520")

**Example Request:**
```bash
curl https://alphafold.ebi.ac.uk/api/prediction/P00520
```

**Example Response:**
```json
[
  {
    "entryId": "AF-P00520-F1",
    "gene": "ABL1",
    "uniprotAccession": "P00520",
    "uniprotId": "ABL1_HUMAN",
    "uniprotDescription": "Tyrosine-protein kinase ABL1",
    "taxId": 9606,
    "organismScientificName": "Homo sapiens",
    "uniprotStart": 1,
    "uniprotEnd": 1130,
    "uniprotSequence": "MLEICLKLVGCKSKKGLSSSSSCYLEEALQRPVASDFEPQGLSEAARWNSKENLLAGPSENDPNLFVALYDFVASGDNTLSITKGEKLRVLGYNHNGEWCEAQTKNGQGWVPSNYITPVNSLEKHSWYHGPVSRNAAEYLLSSGINGSFLVRESESSPGQRSISLRYEGRVYHYRINTASDGKLYVSSESRFNTLAELVHHHSTVADGLITTLHYPAPKRNKPTVYGVSPNYDKWEMERTDITMKHKLGGGQYGEVYEGVWKKYSLTVAVKTLKEDTMEVEEFLKEAAVMKEIKHPNLVQLLGVCTREPPFYIITEFMTYGNLLDYLRECNRQEVNAVVLLYMATQISSAMEYLEKKNFIHRDLAARNCLVGENHLVKVADFGLSRLMTGDTYTAHAGAKFPIKWTAPESLAYNKFSIKSDVWAFGVLLWEIATYGMSPYPGIDLSQVYELLEKDYRMERPEGCPEKVYELMRACWQWNPSDRPSFAEIHQAFETMFQESSISDEVEKELGKQGVRGAVSTLLQAPELPTKTRTSRRAAEHRDTTDVPEMPHSKGQGESDPLDHEPAVSPLLPRKERGPPEGGLNEDERLLPKDKKTNLFSALIKKKKKTAPTPPKRSSSFREMDGQPERRGAGEEEGRDISNGALAFTPLDTADPAKSPKPSNGAGVPNGALRESGGSGFRSPHLWKKSSTLTSSRLATGEEEGGGSSSKRFLRSCSASCVPHGAKDTEWRSVTLPRDLQSTGRQFDSSTFGGHKSEKPALPRKRAGENRSDQVTRGTVTPPPRLVKKNEEAADEVFKDIMESSPGSSPPNLTPKPLRRQVTVAPASGLPHKEEAGKGSALGTPAAAEPVTPTSKAGSGAPGGTSKGPAEESRVRRHKHSSESPGRDKGKLSRLKPAPPPPPAASAGKAGGKPSQSPSQEAAGEAVLGAKTKATSLVDAVNSDAAKPSQPGEGLKKPVLPATPKPQSAKPSGTPISPAPVPSTLPSASSALAGDQPSSTAFIPLISTRVSLRKTRQPPERIASGAITKGVVLDSTEALCLAISRNSEQMASHSAVLEAGKNLYTFCVSYVDSIQQMRNKFAFREAINKLENNLRELQICPATAGSGPAATQDFSKLLSSVKEISDIVQR",
    "modelCreatedDate": "2021-07-01",
    "latestVersion": 6,
    "allVersions": [1, 2, 3, 4, 5, 6],
    "cifUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v6.cif",
    "bcifUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v6.bcif",
    "pdbUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v6.pdb",
    "plddtDocUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-confidence_v6.json",
    "paeImageUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-predicted_aligned_error_v6.png",
    "paeDocUrl": "https://alphafold.ebi.ac.uk/files/AF-P00520-F1-predicted_aligned_error_v6.json"
  }
]
```

> **Always read the file URLs from this response** rather than hand-building a
> `_v{N}` suffix: the version moves (now v6) and old `_v4` file URLs return 404.

**Response Fields** (selected — the live response includes more):
- `entryId`: AlphaFold internal identifier (format: AF-{uniprot}-F{fragment})
- `gene`: Gene symbol
- `uniprotAccession`: UniProt accession
- `uniprotId`: UniProt entry name
- `uniprotDescription`: Protein description
- `taxId`: NCBI taxonomy identifier
- `organismScientificName`: Species scientific name
- `uniprotStart/uniprotEnd`: Residue range covered
- `uniprotSequence`: Full protein sequence
- `modelCreatedDate`: Initial prediction date
- `latestVersion`: Current model version number
- `allVersions`: List of available versions
- `cifUrl/bcifUrl/pdbUrl`: Structure file download URLs
- `plddtDocUrl`: Per-residue confidence (pLDDT) JSON URL
- `paeImageUrl`: PAE visualization image URL
- `paeDocUrl`: PAE data JSON URL

### 2. 3D-Beacons Integration

AlphaFold is integrated into the 3D-Beacons network for federated structure access.

**Endpoint:** `https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{uniprot_id}.json`

**Example:**
```python
import requests

uniprot_id = "P00520"
url = f"https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{uniprot_id}.json"
response = requests.get(url)
data = response.json()

# Filter for AlphaFold structures
alphafold_structures = [
    s for s in data['structures']
    if s['provider'] == 'AlphaFold DB'
]
```

---

## File Access Patterns

### Direct File Downloads

All AlphaFold files are accessible via direct URLs without authentication.

**URL Pattern:**
```
https://alphafold.ebi.ac.uk/files/{alphafold_id}-{file_type}_{version}.{extension}
```

**Components:**
- `{alphafold_id}`: Entry identifier (e.g., "AF-P00520-F1")
- `{file_type}`: Type of file (see below)
- `{version}`: Database version (currently "v6"). **Prefer the exact URLs from the
  `/prediction/{uniprot}` response over hand-building this** — old `_v4` URLs 404.
- `{extension}`: File format extension

### Available File Types

#### 1. Model Coordinates

**mmCIF Format (Recommended):**
```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v6.cif
```
- Standard crystallographic format
- Contains full metadata
- Supports large structures
- File size: Variable (100KB - 10MB typical)

**Binary CIF Format:**
```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v6.bcif
```
- Compressed binary version of mmCIF
- Smaller file size (~70% reduction)
- Faster parsing
- Requires specialized parser

**PDB Format (Legacy):**
```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-model_v6.pdb
```
- Traditional PDB text format
- Limited to 99,999 atoms
- Widely supported by older tools
- File size: Similar to mmCIF

#### 2. Confidence Metrics

**Per-Residue Confidence (JSON):**
```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-confidence_v6.json
```

**Structure:**
```json
{
  "residueNumber": [1, 2, 3, ...],
  "confidenceScore": [87.5, 91.2, 93.8, ...],
  "confidenceCategory": ["high", "very_high", "very_high", ...]
}
```

**Fields:**
- `residueNumber`: 1-based residue index, one per residue
- `confidenceScore`: Array of pLDDT values (0-100) for each residue
- `confidenceCategory`: Categorical classification (very_low, low, high, very_high)

#### 3. Predicted Aligned Error (JSON)

```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-predicted_aligned_error_v6.json
```

**Structure:** a single-element JSON array wrapping one object:
```json
[
  {
    "predicted_aligned_error": [[0, 2.3, 4.5, ...], [2.3, 0, 3.1, ...], ...],
    "max_predicted_aligned_error": 31.75
  }
]
```

**Fields:**
- `predicted_aligned_error`: N×N matrix of PAE values in Ångströms
- `max_predicted_aligned_error`: Maximum PAE value in the matrix

> The response is wrapped in a one-element array, so index `[0]` before the key:
> `pae[0]['predicted_aligned_error']`.

#### 4. PAE Visualization (PNG)

```
https://alphafold.ebi.ac.uk/files/AF-P00520-F1-predicted_aligned_error_v6.png
```
- Pre-rendered PAE heatmap
- Useful for quick visual assessment
- Resolution: Variable based on protein size

### Batch Download Strategy

For downloading multiple files efficiently, use concurrent downloads with proper error handling and rate limiting to respect server resources.

---

## Data Schemas

### Coordinate File (mmCIF) Schema

AlphaFold mmCIF files contain:

**Key Data Categories:**
- `_entry`: Entry-level metadata
- `_struct`: Structure title and description
- `_entity`: Molecular entity information
- `_atom_site`: Atomic coordinates and properties
- `_pdbx_struct_assembly`: Biological assembly info

**Important Fields in `_atom_site`:**
- `group_PDB`: "ATOM" for all records
- `id`: Atom serial number
- `label_atom_id`: Atom name (e.g., "CA", "N", "C")
- `label_comp_id`: Residue name (e.g., "ALA", "GLY")
- `label_seq_id`: Residue sequence number
- `Cartn_x/y/z`: Cartesian coordinates (Ångströms)
- `B_iso_or_equiv`: B-factor (contains pLDDT score)

**pLDDT in B-factor Column:**
AlphaFold stores per-residue confidence (pLDDT) in the B-factor field. This allows standard structure viewers to color by confidence automatically.

### Confidence JSON Schema

```json
{
  "residueNumber": [1, 2, 3, ...],   // 1-based residue index, one per residue
  "confidenceScore": [
    87.5,   // Residue 1 pLDDT
    91.2,   // Residue 2 pLDDT
    93.8    // Residue 3 pLDDT
    // ... one value per residue
  ],
  "confidenceCategory": [
    "high",      // Residue 1 category
    "very_high", // Residue 2 category
    "very_high"  // Residue 3 category
    // ... one category per residue
  ]
}
```

**Confidence Categories:**
- `very_high`: pLDDT > 90
- `high`: 70 < pLDDT ≤ 90
- `low`: 50 < pLDDT ≤ 70
- `very_low`: pLDDT ≤ 50

### PAE JSON Schema

```json
[
  {
    "predicted_aligned_error": [
      [0.0, 2.3, 4.5, ...],     // PAE from residue 1 to all residues
      [2.3, 0.0, 3.1, ...],     // PAE from residue 2 to all residues
      [4.5, 3.1, 0.0, ...]      // PAE from residue 3 to all residues
      // ... N×N matrix for N residues
    ],
    "max_predicted_aligned_error": 31.75
  }
]
```

**Interpretation** (with `pae = pae[0]['predicted_aligned_error']`):
- `pae[i][j]`: Expected position error (Ångströms) of residue j if the predicted and true structures were aligned on residue i
- Lower values indicate more confident relative positioning
- Diagonal is always 0 (residue aligned to itself)
- Matrix is not symmetric: pae[i][j] ≠ pae[j][i]

---

## Google Cloud Access

AlphaFold DB is hosted on Google Cloud Platform for bulk access.

> **Note:** The bulk GCS bucket and BigQuery dataset are versioned independently
> of the REST API and currently lag at **v4** (bucket `...-alphafold-v4`, proteome
> archives `..._v4.tar`). The per-protein REST API serves **v6**. Use the v4 paths
> below for bulk access; do not "upgrade" them to v6.

### Cloud Storage Bucket

**Bucket:** `gs://public-datasets-deepmind-alphafold-v4`

**Directory Structure:**
```
gs://public-datasets-deepmind-alphafold-v4/
├── accession_ids.csv              # Index of all entries (13.5 GB)
├── sequences.fasta                # All protein sequences (16.5 GB)
└── proteomes/                     # Grouped by species (1M+ archives)
```

### Installing gsutil

```bash
# Using pip
pip install gsutil
```

Or install the Google Cloud SDK (which bundles `gsutil`) by following the
official instructions at https://cloud.google.com/sdk/docs/install. Prefer a
package manager or the versioned installer archive, for example:

```bash
# macOS (Homebrew)
brew install --cask google-cloud-sdk

# Debian/Ubuntu (APT repository) — see the install page for the full steps
sudo apt-get install google-cloud-cli
```

> **Caution:** Avoid `curl https://sdk.cloud.google.com | bash` — piping a
> remote script straight into a shell executes unreviewed code. Download the
> installer or use a package manager so you can verify what runs.

### Downloading Proteomes

**By Taxonomy ID:**

```bash
# Download all archives for a species
TAX_ID=9606  # Human
gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-${TAX_ID}-*_v4.tar .
```

---

## BigQuery Schema

AlphaFold metadata is available in BigQuery for SQL-based queries.

**Dataset:** `bigquery-public-data.deepmind_alphafold`
**Table:** `metadata`

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `entryId` | STRING | AlphaFold entry ID |
| `uniprotAccession` | STRING | UniProt accession |
| `gene` | STRING | Gene symbol |
| `organismScientificName` | STRING | Species scientific name |
| `taxId` | INTEGER | NCBI taxonomy ID |
| `globalMetricValue` | FLOAT | Overall quality metric |
| `fractionPlddtVeryHigh` | FLOAT | Fraction with pLDDT ≥ 90 |
| `isReviewed` | BOOLEAN | Swiss-Prot reviewed status |
| `sequenceLength` | INTEGER | Protein sequence length |

### Example Query

```sql
SELECT
  entryId,
  uniprotAccession,
  gene,
  fractionPlddtVeryHigh
FROM `bigquery-public-data.deepmind_alphafold.metadata`
WHERE
  taxId = 9606  -- Homo sapiens
  AND fractionPlddtVeryHigh > 0.8
  AND isReviewed = TRUE
ORDER BY fractionPlddtVeryHigh DESC
LIMIT 100;
```

---

## Best Practices

### 1. Caching Strategy

Always cache downloaded files locally to avoid repeated downloads.

### 2. Error Handling

Implement robust error handling for API requests with retry logic for transient failures.

### 3. Bulk Processing

For processing many proteins, use concurrent downloads with appropriate rate limiting.

### 4. Version Management

Read file URLs from the `/prediction` response rather than hardcoding a version
suffix. The REST API currently serves **v6**; the bulk GCS/BigQuery datasets lag
at **v4**. Track which version a result came from in your code.

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response normally |
| 404 | Not Found | No AlphaFold prediction for this UniProt ID |
| 429 | Too Many Requests | Implement rate limiting and retry with backoff |
| 500 | Server Error | Retry with exponential backoff |
| 503 | Service Unavailable | Wait and retry later |

---

## Rate Limiting

### Recommendations

- Limit to **10 concurrent requests** maximum
- Add **100-200ms delay** between sequential requests
- Use Google Cloud for bulk downloads instead of REST API
- Cache all downloaded data locally

---

## Additional Resources

- **AlphaFold GitHub:** https://github.com/google-deepmind/alphafold
- **Google Cloud Documentation:** https://console.cloud.google.com/marketplace/product/bigquery-public-data/deepmind-alphafold
- **3D-Beacons Documentation:** https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/docs
- **Biopython Tutorial:** https://biopython.org/docs/latest/api/Bio.PDB.alphafold_db.html

## Version History

The `/prediction` response reports `latestVersion` and `allVersions`; treat those
as the source of truth rather than this list.

- **v1** (2021): Initial release with ~350K structures
- **v2** (2022): Expanded to 200M+ structures
- **v3** (2023): Updated models and expanded coverage
- **v4** (2024): Improved confidence metrics; still the version served by the bulk
  GCS bucket and BigQuery dataset
- **v5–v6**: Later model updates served by the REST API (`latestVersion` is 6 as
  observed); bulk datasets had not been re-cut to these at time of writing

## Citation

When using AlphaFold DB in publications, cite:

1. Jumper, J. et al. Highly accurate protein structure prediction with AlphaFold. Nature 596, 583–589 (2021).
2. Varadi, M. et al. AlphaFold Protein Structure Database in 2024: providing structure coverage for over 214 million protein sequences. Nucleic Acids Res. 52, D368–D375 (2024).
