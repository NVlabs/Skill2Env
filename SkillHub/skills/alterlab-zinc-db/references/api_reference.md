# ZINC Database API Reference

## Overview

Complete technical reference for programmatic access to the ZINC database, covering API endpoints, query syntax, parameters, response formats, and advanced usage patterns for ZINC22, ZINC20, and legacy versions.

> **Request model (read first).** CartBlanche22 searches are submitted as **form
> fields** — either `curl -F field=value` (multipart) or a form-encoded POST (what
> `scripts/query_zinc.py` sends). The legacy "colon URL" form
> (`/substances.txt:zinc_id=...`) is not supported by the current service. Every
> search is **asynchronous**: the endpoint returns a JSON task handle
> (`{"task": "<uuid>"}`) and the rows are assembled server-side for the web UI. For
> large programmatic retrieval, use the bulk file repository (below) rather than
> scraping task results.

## Base URLs

### ZINC22 (Current)
- **CartBlanche22 API**: `https://cartblanche22.docking.org/`
- **File Repository**: `https://files.docking.org/zinc22/`
- **Main Website**: `https://zinc.docking.org/`

### ZINC20 (Maintained)
- **API**: `https://zinc20.docking.org/`
- **File Repository**: `https://files.docking.org/zinc20/`

### Documentation
- **Wiki**: `https://wiki.docking.org/`
- **GitHub**: `https://github.com/docking-org/`

## API Endpoints

### 1. Substance Retrieval by ZINC ID

Retrieve compound information using ZINC identifiers.

**Endpoint**: `/substances.txt`

**Parameters** (form fields):
- `zinc_ids` (required): Comma-separated list of ZINC IDs, or `@file` (one per line).
  Note the field is **plural** — `zinc_id` returns HTTP 400.
- `output_fields` (optional): Comma-separated field names (default: all fields)

**Examples**:

Multiple compounds (inline):
```bash
curl -X GET "https://cartblanche22.docking.org/substances.txt" \
  -F zinc_ids="ZINC000019632618,ZINC000000000001" \
  -F output_fields="zinc_id,smiles,catalogs"
```

Batch retrieval from a file:
```bash
# zinc_ids.txt: one ZINC ID per line
curl -X GET "https://cartblanche22.docking.org/substances.txt" \
  -F zinc_ids=@zinc_ids.txt \
  -F output_fields="zinc_id,smiles,tranche"
```

**Response** (JSON task handle):
```json
{"task": "0bf64e3e-ac00-4123-9270-7bfd3572117c"}
```
The result rows (TSV-style columns: `zinc_id`, `smiles`, `catalogs`, …) are then
materialized in the web UI task view.

### 2. Structure Search by SMILES

Search for compounds by chemical structure with optional similarity thresholds.

**Endpoint**: `/smiles.txt`

**Parameters** (form fields):
- `smiles` (required): Query SMILES string (inline, or `@file` for a batch of queries)
- `dist` (optional): Tanimoto distance threshold (default: 0 = exact)
- `adist` (optional): Anonymous (graph-topology) distance for broader searches (default: 0)
- `output_fields` (optional): Comma-separated field names

**Examples**:

Exact structure match (dist/adist default to 0):
```bash
curl -X GET "https://cartblanche22.docking.org/smiles.txt" \
  -F smiles="c1ccccc1" -F output_fields="zinc_id,smiles"
```

Similarity search (Tanimoto distance = 3):
```bash
curl -X GET "https://cartblanche22.docking.org/smiles.txt" \
  -F smiles="CC(C)Cc1ccc(cc1)C(C)C(=O)O" -F dist=3 \
  -F output_fields="zinc_id,smiles,catalogs"
```

Broad similarity search (both metrics):
```bash
curl -X GET "https://cartblanche22.docking.org/smiles.txt" \
  -F smiles="c1ccccc1" -F dist=5 -F adist=5 \
  -F output_fields="zinc_id,smiles,tranche"
```

Because SMILES is sent as a form-field value rather than embedded in the URL, no
URL-encoding of special characters (`(`, `=`, `#`) is needed.

**Distance Parameters Interpretation**:
- `dist=0`: Exact match
- `dist=1-3`: Close analogs (high similarity)
- `dist=4-6`: Moderate analogs
- `dist=7-10`: Diverse chemical space

### 3. Supplier Code Search

Query compounds by vendor catalog numbers.

**Endpoint**: `/catitems.txt`

**Parameters** (form fields):
- `supplier_codes` (required): Supplier catalog code(s) — inline, or `@file`
- `output_fields` (optional): Comma-separated field names

**Example**:
```bash
curl -X GET "https://cartblanche22.docking.org/catitems.txt" \
  -F supplier_codes="SUPPLIER-12345" \
  -F output_fields="zinc_id,smiles,supplier_code,catalogs"
```

### 4. Random Compound Sampling

Generate random compound sets with optional filtering by chemical properties.

**Endpoint**: `/substance/random.txt`

**Parameters** (form fields):
- `count` (optional): Number of compounds to retrieve (default: 100, max: depends on server)
- `subset` (optional): Filter by predefined subset (e.g., 'lead-like', 'drug-like', 'fragment')
- `output_fields` (optional): Comma-separated field names

**Examples**:

Random 100 compounds (default):
```bash
curl "https://cartblanche22.docking.org/substance/random.txt" -F count=100
```

Random lead-like molecules:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt" \
  -F count=1000 -F subset="lead-like" -F output_fields="zinc_id,smiles,tranche"
```

Random fragments:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt" \
  -F count=500 -F subset="fragment" -F output_fields="zinc_id,smiles,tranche"
```

**Subset Definitions**:
- `fragment`: MW < 250, suitable for fragment-based drug discovery
- `lead-like`: MW 250-350, LogP ≤ 3.5, rotatable bonds ≤ 7
- `drug-like`: MW 350-500, follows Lipinski's Rule of Five
- `lugs`: Large, unusually good subset (highly curated)

## Output Fields

### Available Fields

Customize API responses using the `output_fields` parameter:

| Field | Description | Example |
|-------|-------------|---------|
| `zinc_id` | ZINC identifier | ZINC000000000001 |
| `smiles` | Canonical SMILES string | CC(C)O |
| `sub_id` | Internal substance ID | 123456 |
| `supplier_code` | Vendor catalog number | AB-1234567 |
| `catalogs` | List of suppliers | [emolecules, mcule, mcule-ultimate] |
| `tranche` | Encoded molecular properties | H02P025M300-0 |
| `mwt` | Molecular weight | 325.45 |
| `logp` | LogP (partition coefficient) | 2.5 |
| `hba` | H-bond acceptors | 4 |
| `hbd` | H-bond donors | 2 |
| `rotatable_bonds` | Rotatable bonds count | 5 |

**Note**: Not all fields are available for all endpoints. Field availability depends on the database version and endpoint.

### Default Fields

If `output_fields` is not specified, endpoints return all available fields in TSV format.

### Custom Field Selection

Request specific fields only:
```bash
curl -X GET "https://cartblanche22.docking.org/substances.txt" \
  -F zinc_ids="ZINC000019632618" -F output_fields="zinc_id,smiles"
```

Request multiple fields:
```bash
curl -X GET "https://cartblanche22.docking.org/substances.txt" \
  -F zinc_ids="ZINC000019632618" -F output_fields="zinc_id,smiles,tranche,catalogs"
```

## Tranche System

ZINC organizes compounds into tranches based on molecular properties for efficient filtering and organization.

### Tranche Code Format

**Pattern**: `H##P###M###-phase`

| Component | Description | Range |
|-----------|-------------|-------|
| H## | Hydrogen bond donors | 00-99 |
| P### | LogP × 10 | 000-999 (e.g., P035 = LogP 3.5) |
| M### | Molecular weight | 000-999 Da |
| phase | Reactivity classification | 0-9 |

### Examples

| Tranche Code | Interpretation |
|--------------|----------------|
| `H00P010M250-0` | 0 H-donors, LogP=1.0, MW=250 Da, phase 0 |
| `H05P035M400-0` | 5 H-donors, LogP=3.5, MW=400 Da, phase 0 |
| `H02P-005M180-0` | 2 H-donors, LogP=-0.5, MW=180 Da, phase 0 |

### Reactivity Phases

| Phase | Description |
|-------|-------------|
| 0 | Unreactive (preferred for screening) |
| 1-9 | Increasing reactivity (PAINS, reactive groups) |

### Parsing Tranches in Python

```python
import re

def parse_tranche(tranche_str):
    """
    Parse ZINC tranche code.

    Args:
        tranche_str: Tranche code (e.g., "H05P035M400-0")

    Returns:
        dict with h_donors, logp, mw, phase
    """
    pattern = r'H(\d+)P(-?\d+)M(\d+)-(\d+)'
    match = re.match(pattern, tranche_str)

    if not match:
        return None

    return {
        'h_donors': int(match.group(1)),
        'logp': int(match.group(2)) / 10.0,
        'mw': int(match.group(3)),
        'phase': int(match.group(4))
    }

# Example usage
tranche = "H05P035M400-0"
props = parse_tranche(tranche)
print(props)  # {'h_donors': 5, 'logp': 3.5, 'mw': 400, 'phase': 0}
```

### Filtering by Tranches

Download specific tranches from file repositories:
```bash
# Download all compounds in a specific tranche
wget https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz
```

## File Repository Access

### Directory Structure

ZINC22 3D structures are organized hierarchically by H-bond donors:

```
https://files.docking.org/zinc22/
├── H00/
│   ├── H00P010M200-0.db2.gz
│   ├── H00P020M250-0.db2.gz
│   └── ...
├── H01/
├── H02/
└── ...
```

### File Formats

| Extension | Format | Description |
|-----------|--------|-------------|
| `.db2.gz` | DOCK database | Compressed multi-conformer DB for DOCK |
| `.mol2.gz` | MOL2 | Multi-molecule format with 3D coordinates |
| `.sdf.gz` | SDF | Structure-Data File format |
| `.smi` | SMILES | Plain text SMILES with ZINC IDs |

### Downloading 3D Structures

**Single tranche**:
```bash
wget https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz
```

**Multiple tranches** (parallel download with aria2c):
```bash
# Create URL list
cat > tranche_urls.txt <<EOF
https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz
https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz
https://files.docking.org/zinc22/H05/H05P040M400-0.db2.gz
EOF

# Download in parallel
aria2c -i tranche_urls.txt -x 8 -j 4
```

**Recursive download** (use with caution - large data):
```bash
wget -r -np -nH --cut-dirs=1 -A "*.db2.gz" \
  https://files.docking.org/zinc22/H05/
```

### Extracting Structures

```bash
# Decompress
gunzip H05P035M400-0.db2.gz

# Convert to other formats using OpenBabel
obabel H05P035M400-0.db2 -O output.sdf
obabel H05P035M400-0.db2 -O output.mol2
```

## Advanced Query Patterns

### Combining Multiple Search Criteria

**Python wrapper for complex queries** (form-encoded POST, stdlib only):

```python
import json
import urllib.parse
import urllib.request

BASE = "https://cartblanche22.docking.org"

def _post(path, fields):
    data = urllib.parse.urlencode(fields).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/{path}", data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))

def advanced_zinc_search(smiles=None, zinc_ids=None, dist=0,
                         subset=None, count=None, output_fields=None):
    """
    Submit a ZINC22 search. Returns the JSON task handle ({"task": "<uuid>"});
    retrieve the rows from the web UI task view.

    Exactly one of smiles / zinc_ids / count must be given.
    """
    fields_str = ",".join(output_fields or ["zinc_id", "smiles", "tranche", "catalogs"])

    if smiles:
        return _post("smiles.txt",
                     {"smiles": smiles, "dist": dist, "output_fields": fields_str})
    if zinc_ids:
        return _post("substances.txt",
                     {"zinc_ids": ",".join(zinc_ids), "output_fields": fields_str})
    if count:
        body = {"count": count, "output_fields": fields_str}
        if subset:
            body["subset"] = subset
        return _post("substance/random.txt", body)
    raise ValueError("Must specify smiles, zinc_ids, or count")
```

**Usage examples**:

```python
# Find similar compounds (submits the search, returns a task handle)
task = advanced_zinc_search(
    smiles="CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    dist=3,
    output_fields=["zinc_id", "smiles", "catalogs"],
)

# Batch retrieval
task = advanced_zinc_search(zinc_ids=["ZINC000019632618", "ZINC000000000001"])

# Random drug-like set
task = advanced_zinc_search(
    count=1000, subset="drug-like",
    output_fields=["zinc_id", "smiles", "tranche"],
)
```

### Property-Based Filtering

Filter compounds by molecular properties using tranche data:

```python
def filter_by_properties(df, mw_range=None, logp_range=None,
                        max_hbd=None, phase=0):
    """
    Filter DataFrame by molecular properties.

    Args:
        df: DataFrame with 'tranche' column
        mw_range: Tuple (min_mw, max_mw)
        logp_range: Tuple (min_logp, max_logp)
        max_hbd: Maximum H-bond donors
        phase: Reactivity phase (0 = unreactive)

    Returns:
        Filtered DataFrame
    """
    # Parse tranches
    df['tranche_props'] = df['tranche'].apply(parse_tranche)
    df['mw'] = df['tranche_props'].apply(lambda x: x['mw'] if x else None)
    df['logp'] = df['tranche_props'].apply(lambda x: x['logp'] if x else None)
    df['hbd'] = df['tranche_props'].apply(lambda x: x['h_donors'] if x else None)
    df['phase'] = df['tranche_props'].apply(lambda x: x['phase'] if x else None)

    # Apply filters
    mask = pd.Series([True] * len(df))

    if mw_range:
        mask &= (df['mw'] >= mw_range[0]) & (df['mw'] <= mw_range[1])

    if logp_range:
        mask &= (df['logp'] >= logp_range[0]) & (df['logp'] <= logp_range[1])

    if max_hbd is not None:
        mask &= df['hbd'] <= max_hbd

    if phase is not None:
        mask &= df['phase'] == phase

    return df[mask]

# Example: filter exported result rows by molecular properties.
# `df` is a DataFrame with a 'tranche' column (exported from the UI task view,
# or read from the bulk file repository) — advanced_zinc_search only returns the
# task handle, so the rows are fetched separately.
filtered = filter_by_properties(
    df,
    mw_range=(300, 450),
    logp_range=(1.0, 4.0),
    max_hbd=3,
    phase=0
)
```

## Rate Limiting and Best Practices

### Rate Limiting

ZINC does not publish explicit rate limits, but users should:

- **Avoid rapid-fire requests**: Space out queries by at least 1 second
- **Use batch operations**: Query multiple ZINC IDs in single request
- **Cache results**: Store frequently accessed data locally
- **Off-peak usage**: Perform large downloads during off-peak hours (UTC nights/weekends)

### Etiquette

```python
import time

def polite_zinc_query(query_func, *args, delay=1.0, **kwargs):
    """Wrapper to add delay between queries."""
    result = query_func(*args, **kwargs)
    time.sleep(delay)
    return result
```

### Error Handling

```python
def robust_zinc_query(url, max_retries=3, timeout=30):
    """
    Query ZINC with retry logic.

    Args:
        url: Full ZINC API URL
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds

    Returns:
        Query results or None on failure
    """
    import subprocess
    import time

    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['curl', '-s', '--max-time', str(timeout), url],
                capture_output=True,
                text=True,
                check=True
            )

            # Check for empty or error responses
            if not result.stdout or 'error' in result.stdout.lower():
                raise ValueError("Invalid response")

            return result.stdout

        except (subprocess.CalledProcessError, ValueError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts")
                return None
```

## Integration with Molecular Docking

### Preparing DOCK6 Libraries

```bash
# 1. Download tranche files
wget https://files.docking.org/zinc22/H05/H05P035M400-0.db2.gz

# 2. Decompress
gunzip H05P035M400-0.db2.gz

# 3. Use directly with DOCK6
dock6 -i dock.in -o dock.out -l H05P035M400-0.db2
```

### AutoDock Vina Integration

```bash
# 1. Download MOL2 format
wget https://files.docking.org/zinc22/H05/H05P035M400-0.mol2.gz
gunzip H05P035M400-0.mol2.gz

# 2. Convert to PDBQT using prepare_ligand script
prepare_ligand4.py -l H05P035M400-0.mol2 -o ligands.pdbqt -A hydrogens

# 3. Run Vina
vina --receptor protein.pdbqt --ligand ligands.pdbqt \
     --center_x 25.0 --center_y 25.0 --center_z 25.0 \
     --size_x 20.0 --size_y 20.0 --size_z 20.0
```

### RDKit Integration

```python
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
import pandas as pd

def process_zinc_results(zinc_df):
    """
    Process ZINC results with RDKit.

    Args:
        zinc_df: DataFrame with SMILES column

    Returns:
        DataFrame with calculated properties
    """
    # Convert SMILES to molecules
    zinc_df['mol'] = zinc_df['smiles'].apply(Chem.MolFromSmiles)

    # Calculate properties
    zinc_df['mw'] = zinc_df['mol'].apply(Descriptors.MolWt)
    zinc_df['logp'] = zinc_df['mol'].apply(Descriptors.MolLogP)
    zinc_df['hbd'] = zinc_df['mol'].apply(Descriptors.NumHDonors)
    zinc_df['hba'] = zinc_df['mol'].apply(Descriptors.NumHAcceptors)
    zinc_df['tpsa'] = zinc_df['mol'].apply(Descriptors.TPSA)
    zinc_df['rotatable'] = zinc_df['mol'].apply(Descriptors.NumRotatableBonds)

    # Generate 3D conformers
    for mol in zinc_df['mol']:
        if mol:
            AllChem.EmbedMolecule(mol, randomSeed=42)
            AllChem.MMFFOptimizeMolecule(mol)

    return zinc_df

# Save to SDF for docking
def save_to_sdf(zinc_df, output_file):
    """Save molecules to SDF file."""
    writer = Chem.SDWriter(output_file)
    for idx, row in zinc_df.iterrows():
        if row['mol']:
            row['mol'].SetProp('ZINC_ID', row['zinc_id'])
            writer.write(row['mol'])
    writer.close()
```

## Troubleshooting

### Common Issues

**Issue**: Empty or no results
- **Solution**: Check SMILES syntax, verify ZINC IDs exist, try broader similarity search

**Issue**: Timeout errors
- **Solution**: Reduce result count, use batch queries, try during off-peak hours

**Issue**: Invalid SMILES encoding
- **Solution**: URL-encode special characters (use `urllib.parse.quote()` in Python)

**Issue**: Tranche files not found
- **Solution**: Verify tranche code format, check file repository structure

### Debug Mode

```python
def debug_zinc_query(url):
    """Print query details for debugging."""
    print(f"Query URL: {url}")

    result = subprocess.run(['curl', '-v', url],
                          capture_output=True, text=True)

    print(f"Status: {result.returncode}")
    print(f"Stderr: {result.stderr}")
    print(f"Stdout length: {len(result.stdout)}")
    print(f"First 500 chars:\n{result.stdout[:500]}")

    return result.stdout
```

## Version Differences

### ZINC22 vs ZINC20 vs ZINC15

| Feature | ZINC22 | ZINC20 | ZINC15 |
|---------|--------|--------|--------|
| Compounds | 230M+ purchasable | Focused on leads | ~750M total |
| API | CartBlanche22 | Similar | REST-like |
| Tranches | Yes | Yes | Yes |
| 3D Structures | Yes | Yes | Yes |
| Status | Current, growing | Maintained | Legacy |

### API Compatibility

Most query patterns work across versions, but URLs differ:
- ZINC22: `cartblanche22.docking.org`
- ZINC20: `zinc20.docking.org`
- ZINC15: `zinc15.docking.org`

## Additional Resources

- **ZINC Wiki**: https://wiki.docking.org/
- **ZINC22 Documentation**: https://wiki.docking.org/index.php/Category:ZINC22
- **ZINC API Guide**: https://wiki.docking.org/index.php/ZINC_api
- **File Access Guide**: https://wiki.docking.org/index.php/ZINC22:Getting_started
- **Publications**:
  - ZINC22: Tingle et al., *J. Chem. Inf. Model.* 2023, 63(4), 1166–1176. DOI: 10.1021/acs.jcim.2c01253
  - ZINC20: Irwin et al., *J. Chem. Inf. Model.* 2020, 60(12), 6065–6073. DOI: 10.1021/acs.jcim.0c00675
  - ZINC15: Sterling & Irwin, *J. Chem. Inf. Model.* 2015, 55, 2324–2337. DOI: 10.1021/acs.jcim.5b00559
- **Support**: Contact via ZINC website or GitHub issues
