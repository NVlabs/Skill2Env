# AlphaFold DB — Worked Code Examples

Copy-paste Python recipes for the common AlphaFold DB tasks. For REST endpoint
specs, file schemas, GCP dataset layout, rate limiting, and error handling, see
`api_reference.md`.

## 1. Searching and Retrieving Predictions

### Using Biopython (Recommended)

The Biopython library provides the simplest interface for retrieving AlphaFold structures:

```python
from Bio.PDB import alphafold_db

# Get all predictions for a UniProt accession
predictions = list(alphafold_db.get_predictions("P00520"))

# Download structure file (mmCIF format)
for prediction in predictions:
    cif_file = alphafold_db.download_cif_for(prediction, directory="./structures")
    print(f"Downloaded: {cif_file}")

# Get Structure objects directly
from Bio.PDB import MMCIFParser
structures = list(alphafold_db.get_structural_models_for("P00520"))
```

### Direct API Access

Query predictions using REST endpoints:

```python
import requests

# Get prediction metadata for a UniProt accession
uniprot_id = "P00520"
api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
response = requests.get(api_url)
prediction_data = response.json()

# Extract AlphaFold ID
alphafold_id = prediction_data[0]['entryId']
print(f"AlphaFold ID: {alphafold_id}")
```

### Using UniProt to Find Accessions

Search UniProt to find protein accessions first:

```python
import requests, time

def get_uniprot_ids(query, from_db='PDB', to_db='UniProtKB'):
    """Map IDs to UniProt accessions via the current REST API.

    from_db/to_db must be current DB names, e.g. 'PDB', 'Gene_Name',
    'UniProtKB_AC-ID', 'UniProtKB'.
    Valid values: https://rest.uniprot.org/configure/idmapping/fields
    """
    base = 'https://rest.uniprot.org'
    # 1) submit job
    r = requests.post(f'{base}/idmapping/run',
                      data={'from': from_db, 'to': to_db, 'ids': query})
    r.raise_for_status()
    job_id = r.json()['jobId']
    # 2) poll status
    while True:
        s = requests.get(f'{base}/idmapping/status/{job_id}').json()
        if s.get('jobStatus') in (None, 'FINISHED') or 'results' in s:
            break
        if s.get('jobStatus') in ('ERROR',):
            raise RuntimeError(s)
        time.sleep(1)
    # 3) fetch results
    res = requests.get(f'{base}/idmapping/results/{job_id}').json()
    return [m['to'] for m in res.get('results', [])]

# Example: Find UniProt accessions for a gene name
protein_ids = get_uniprot_ids("HBB", from_db="Gene_Name", to_db="UniProtKB")
```

## 2. Downloading Structure Files

AlphaFold provides multiple file formats for each prediction. **Read the file
URLs from the prediction metadata rather than hand-building a `_v{N}` suffix** —
the DB version advances (currently v6) and old hardcoded `_v4` URLs now 404. The
prediction record carries the exact, version-stamped URLs:

- `cifUrl` / `pdbUrl` / `bcifUrl` — model coordinates (mmCIF / PDB / binary CIF)
- `plddtDocUrl` — per-residue pLDDT confidence JSON (0-100)
- `paeDocUrl` — Predicted Aligned Error JSON

```python
import requests

# Resolve the current file URLs from the prediction metadata.
rec = requests.get("https://alphafold.ebi.ac.uk/api/prediction/P00520").json()[0]
alphafold_id = rec["entryId"]  # e.g. "AF-P00520-F1"

# Model coordinates (mmCIF) — write bytes, never decode/re-encode text.
r = requests.get(rec["cifUrl"])
with open(f"{alphafold_id}.cif", "wb") as f:
    f.write(r.content)

# Confidence scores (JSON)
confidence_data = requests.get(rec["plddtDocUrl"]).json()

# Predicted Aligned Error (JSON)
pae_data = requests.get(rec["paeDocUrl"]).json()
```

**PDB Format (Alternative):**

```python
# Download as PDB format instead of mmCIF
r = requests.get(rec["pdbUrl"])
with open(f"{alphafold_id}.pdb", "wb") as f:
    f.write(r.content)
```

## 3. Working with Confidence Metrics

AlphaFold predictions include confidence estimates critical for interpretation:

**pLDDT (per-residue confidence):**

```python
import requests

# Resolve the confidence-JSON URL from the prediction metadata (version-stamped).
rec = requests.get("https://alphafold.ebi.ac.uk/api/prediction/P00520").json()[0]
confidence = requests.get(rec["plddtDocUrl"]).json()

# Extract pLDDT scores (keys: residueNumber, confidenceScore, confidenceCategory)
plddt_scores = confidence['confidenceScore']

# Interpret confidence levels
# pLDDT > 90: Very high confidence
# pLDDT 70-90: High confidence
# pLDDT 50-70: Low confidence
# pLDDT < 50: Very low confidence

high_confidence_residues = [i for i, score in enumerate(plddt_scores) if score > 90]
print(f"High confidence residues: {len(high_confidence_residues)}/{len(plddt_scores)}")
```

**PAE (Predicted Aligned Error):**

PAE indicates confidence in relative domain positions:

```python
import numpy as np
import matplotlib.pyplot as plt

# Load PAE matrix (rec from the prediction metadata, as above)
pae = requests.get(rec["paeDocUrl"]).json()

# Visualize PAE matrix.
# The PAE JSON is a single-element array of one object with keys
# 'predicted_aligned_error' (the N×N matrix) and 'max_predicted_aligned_error',
# so index [0] before the key.
pae_matrix = np.array(pae[0]['predicted_aligned_error'])
plt.figure(figsize=(10, 8))
plt.imshow(pae_matrix, cmap='viridis_r', vmin=0, vmax=30)
plt.colorbar(label='PAE (Å)')
plt.title(f'Predicted Aligned Error: {alphafold_id}')
plt.xlabel('Residue')
plt.ylabel('Residue')
plt.savefig(f'{alphafold_id}_pae.png', dpi=300, bbox_inches='tight')

# Low PAE values (<5 Å) indicate confident relative positioning
# High PAE values (>15 Å) suggest uncertain domain arrangements
```

## 4. Bulk Data Access via Google Cloud

For large-scale analyses, use Google Cloud datasets:

**Google Cloud Storage:**

```bash
# Install gsutil
uv pip install gsutil

# List available data
gsutil ls gs://public-datasets-deepmind-alphafold-v4/

# Download entire proteomes (by taxonomy ID)
gsutil -m cp gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-9606-*.tar .

# Download specific files
gsutil cp gs://public-datasets-deepmind-alphafold-v4/accession_ids.csv .
```

**BigQuery Metadata Access:**

```python
from google.cloud import bigquery

# Initialize client
client = bigquery.Client()

# Query metadata
query = """
SELECT
  entryId,
  uniprotAccession,
  organismScientificName,
  globalMetricValue,
  fractionPlddtVeryHigh
FROM `bigquery-public-data.deepmind_alphafold.metadata`
WHERE organismScientificName = 'Homo sapiens'
  AND fractionPlddtVeryHigh > 0.8
LIMIT 100
"""

results = client.query(query).to_dataframe()
print(f"Found {len(results)} high-confidence human proteins")
```

**Download by Species:**

> ⚠️ **Security Note**: Always invoke `gsutil` via `subprocess.run()` with a list
> of arguments (never `shell=True` with an interpolated string), and validate the
> taxonomy ID is an integer. Both guard against command injection. See
> [Python subprocess security](https://docs.python.org/3/library/subprocess.html#security-considerations).

```python
import os
import subprocess

def download_proteome(taxonomy_id, output_dir="./proteomes"):
    """Download all AlphaFold predictions for a species (bulk GCS, still v4)."""
    # Validate taxonomy_id is an integer to prevent injection
    if not isinstance(taxonomy_id, int):
        raise ValueError("taxonomy_id must be an integer")

    os.makedirs(output_dir, exist_ok=True)
    pattern = f"gs://public-datasets-deepmind-alphafold-v4/proteomes/proteome-tax_id-{taxonomy_id}-*_v4.tar"
    # List form (no shell=True) prevents command injection.
    subprocess.run(["gsutil", "-m", "cp", pattern, f"{output_dir}/"], check=True)

# Download E. coli proteome (tax ID: 83333)
download_proteome(83333)

# Download human proteome (tax ID: 9606)
download_proteome(9606)
```

## 5. Parsing and Analyzing Structures

Work with downloaded AlphaFold structures using BioPython:

```python
from Bio.PDB import MMCIFParser, PDBIO
import numpy as np

# Parse mmCIF file
parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v6.cif")

# Extract coordinates
coords = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:  # Alpha carbons only
                coords.append(residue['CA'].get_coord())

coords = np.array(coords)
print(f"Structure has {len(coords)} residues")

# Calculate distances
from scipy.spatial.distance import pdist, squareform
distance_matrix = squareform(pdist(coords))

# Identify contacts (< 8 Å)
contacts = np.where((distance_matrix > 0) & (distance_matrix < 8))
print(f"Number of contacts: {len(contacts[0]) // 2}")
```

**Extract B-factors (pLDDT values):**

AlphaFold stores pLDDT scores in the B-factor column:

```python
from Bio.PDB import MMCIFParser

parser = MMCIFParser(QUIET=True)
structure = parser.get_structure("protein", "AF-P00520-F1-model_v6.cif")

# Extract pLDDT from B-factors
plddt_scores = []
for model in structure:
    for chain in model:
        for residue in chain:
            if 'CA' in residue:
                plddt_scores.append(residue['CA'].get_bfactor())

# Identify high-confidence regions
high_conf_regions = [(i, score) for i, score in enumerate(plddt_scores, 1) if score > 90]
print(f"High confidence residues: {len(high_conf_regions)}")
```

## 6. Batch Processing Multiple Proteins

Process multiple predictions efficiently:

```python
import os

import numpy as np
import pandas as pd
import requests

os.makedirs("./batch_structures", exist_ok=True)
uniprot_ids = ["P00520", "P12931", "P04637"]  # Multiple proteins
results = []

for uniprot_id in uniprot_ids:
    try:
        # Get prediction metadata (carries version-stamped file URLs)
        preds = requests.get(
            f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
        ).json()

        if preds:
            rec = preds[0]
            alphafold_id = rec['entryId']

            # Download structure coordinates
            cif = requests.get(rec['cifUrl'])
            with open(f"./batch_structures/{alphafold_id}.cif", "wb") as fh:
                fh.write(cif.content)

            # Get confidence data
            conf_data = requests.get(rec['plddtDocUrl']).json()

            # Calculate statistics
            plddt_scores = conf_data['confidenceScore']
            avg_plddt = np.mean(plddt_scores)
            high_conf_fraction = sum(1 for s in plddt_scores if s > 90) / len(plddt_scores)

            results.append({
                'uniprot_id': uniprot_id,
                'alphafold_id': alphafold_id,
                'avg_plddt': avg_plddt,
                'high_conf_fraction': high_conf_fraction,
                'length': len(plddt_scores)
            })
    except Exception as e:
        print(f"Error processing {uniprot_id}: {e}")

# Create summary DataFrame
df = pd.DataFrame(results)
print(df)
```

## 3D-Beacons API Alternative

AlphaFold can also be accessed via the 3D-Beacons federated API:

```python
import requests

# Query via 3D-Beacons
uniprot_id = "P00520"
url = f"https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/{uniprot_id}.json"
response = requests.get(url)
data = response.json()

# Filter for AlphaFold structures
af_structures = [s for s in data['structures'] if s['provider'] == 'AlphaFold DB']
```
