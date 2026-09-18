---
name: alterlab-zinc-db
description: Access the ZINC database of 230M+ commercially available (purchasable) compounds, searching by ZINC ID or SMILES, running similarity searches, and downloading 3D-ready structures. Use when assembling a compound library for virtual screening, finding purchasable analogs, or obtaining docking-ready 3D structures for drug discovery. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: Keyless public ZINC database (no authentication required)
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# ZINC Database

## Overview

ZINC is a freely accessible repository of 230M+ purchasable compounds maintained by UCSF. Search by ZINC ID or SMILES, perform similarity searches, download 3D-ready structures for docking, discover analogs for virtual screening and drug discovery.

## Scripts

`scripts/query_zinc.py` — query the ZINC22 CartBlanche API via form-encoded POST (stdlib only, JSON to stdout):

```bash
python scripts/query_zinc.py id ZINC000019632618          # ZINC-ID lookup
python scripts/query_zinc.py smiles "c1ccccc1" --dist 3   # SMILES similarity search
python scripts/query_zinc.py random --count 100 --subset lead-like   # random sample
```

**Every CartBlanche search is asynchronous.** Each call returns a JSON task handle
(`{"task": "<uuid>"}`); the result rows are assembled server-side and rendered in the
web UI at `https://cartblanche22.docking.org`. There is no plain-text polling endpoint —
the task route serves the single-page app. Use the script to submit searches and obtain
the task id, then open the UI to retrieve/export rows, or use the bulk file repository
(below) for programmatic large-scale retrieval.

## When to Use This Skill

This skill should be used when:

- **Virtual screening**: Finding compounds for molecular docking studies
- **Lead discovery**: Identifying commercially-available compounds for drug development
- **Structure searches**: Performing similarity or analog searches by SMILES
- **Compound retrieval**: Looking up molecules by ZINC IDs or supplier codes
- **Chemical space exploration**: Exploring purchasable chemical diversity
- **Docking studies**: Accessing 3D-ready molecular structures
- **Analog searches**: Finding similar compounds based on structural similarity
- **Supplier queries**: Identifying compounds from specific chemical vendors
- **Random sampling**: Obtaining random compound sets for screening

## Database Versions

ZINC has evolved through multiple versions:

- **ZINC22** (Current): Largest version with 230+ million purchasable compounds and multi-billion scale make-on-demand compounds
- **ZINC20**: Still maintained, focused on lead-like and drug-like compounds
- **ZINC15**: Predecessor version, legacy but still documented

This skill primarily focuses on ZINC22, the most current and comprehensive version.

## Access Methods

### Web Interface

Primary access point: https://zinc.docking.org/
Interactive searching: https://cartblanche22.docking.org/

### API Access

All ZINC22 searches can be performed programmatically via the CartBlanche22 API:

**Base URL**: `https://cartblanche22.docking.org/`

Searches are submitted as **form-encoded POST** requests (the `scripts/query_zinc.py`
helper does this) or as `curl -F` form-field uploads. Endpoints accept either an inline
value or an `@file` upload, and **every search returns a JSON task handle**
(`{"task": "<uuid>"}`) — results are then rendered in the web UI. Pass the desired
columns via the `output_fields` form field.

> The older "colon URL" form (`/substances.txt:zinc_id=...`) does **not** work against
> the current CartBlanche22 service; use form fields as shown below.

## Core Capabilities

### 1. Search by ZINC ID

Retrieve specific compounds using their ZINC identifiers.

**Web interface**: https://cartblanche22.docking.org/search/zincid

**API endpoint** (form field is `zinc_ids`, plural — the singular `zinc_id` returns HTTP 400):
```bash
# Inline list of IDs
curl -X GET "https://cartblanche22.docking.org/substances.txt" \
  -F zinc_ids="ZINC000019632618,ZINC000000000001" \
  -F output_fields="zinc_id,smiles,catalogs"

# Or upload a file of IDs (one per line)
curl -X GET "https://cartblanche22.docking.org/substances.txt" \
  -F zinc_ids=@zinc_ids.txt \
  -F output_fields="zinc_id,smiles,tranche"
```

Both return a task handle; open the printed UI task URL to view rows.

**Response fields**: `zinc_id`, `smiles`, `sub_id`, `supplier_code`, `catalogs`, `tranche` (includes H-count, LogP, MW, phase)

### 2. Search by SMILES

Find compounds by chemical structure using SMILES notation, with optional distance parameters for analog searching.

**Web interface**: https://cartblanche22.docking.org/search/smiles

**API endpoint**:
```bash
curl -X GET "https://cartblanche22.docking.org/smiles.txt" \
  -F smiles="c1ccccc1" -F dist=3 -F adist=3 \
  -F output_fields="zinc_id,smiles,tranche"
```

**Parameters** (each passed as a `-F` form field):
- `smiles`: Query SMILES string (inline, or `@file` for a batch of queries)
- `dist`: Tanimoto distance threshold (default: 0 for exact match)
- `adist`: Anonymous (graph-topology) distance for broader searches (default: 0)
- `output_fields`: Comma-separated list of desired output fields

**Example - Exact match** (dist/adist default to 0):
```bash
curl -X GET "https://cartblanche22.docking.org/smiles.txt" -F smiles="c1ccccc1"
```

### 3. Search by Supplier Codes

Query compounds from specific chemical suppliers or retrieve all molecules from particular catalogs.

**Web interface**: https://cartblanche22.docking.org/search/catitems

**API endpoint** (form field is `supplier_codes`):
```bash
curl -X GET "https://cartblanche22.docking.org/catitems.txt" \
  -F supplier_codes="SUPPLIER-CODE-123" \
  -F output_fields="zinc_id,smiles,supplier_code,catalogs"
```

**Use cases**:
- Verify compound availability from specific vendors
- Retrieve all compounds from a catalog
- Cross-reference supplier codes with ZINC IDs

### 4. Random Compound Sampling

Generate random compound sets for screening or benchmarking purposes.

**Web interface**: https://cartblanche22.docking.org/search/random

**API endpoint**:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt" -F count=100
```

**Parameters** (each passed as a `-F` form field):
- `count`: Number of random compounds to retrieve (default: 100)
- `subset`: Filter by subset (e.g., 'lead-like', 'drug-like', 'fragment')
- `output_fields`: Customize returned data fields

**Example - Random lead-like molecules**:
```bash
curl "https://cartblanche22.docking.org/substance/random.txt" \
  -F count=1000 -F subset="lead-like" -F output_fields="zinc_id,smiles,tranche"
```

## Common Workflows

### Workflow 1: Preparing a Docking Library

1. **Define search criteria** based on target properties or desired chemical space

2. **Submit the search** with the appropriate method:
   ```bash
   # Example: random drug-like compounds; returns a task handle for the web UI
   python scripts/query_zinc.py random --count 10000 --subset drug-like \
     --fields zinc_id,smiles,tranche
   ```

3. **Retrieve and parse rows** (export from the UI task view, or pull tranche files
   from the bulk repository) into a DataFrame and filter on tranche properties:
   ```python
   import pandas as pd

   df = pd.read_csv('docking_library.tsv', sep='\t')

   # Tranche format: H##P###M###-phase
   # H = H-bond donors, P = LogP*10, M = MW
   ```

4. **Download 3D structures** for docking from the file repository (see below)

### Workflow 2: Finding Analogs of a Hit Compound

1. **Obtain SMILES** of the hit compound:
   ```python
   hit_smiles = "CC(C)Cc1ccc(cc1)C(C)C(=O)O"  # Example: Ibuprofen
   ```

2. **Perform similarity search** with a distance threshold:
   ```bash
   python scripts/query_zinc.py smiles "CC(C)Cc1ccc(cc1)C(C)C(=O)O" \
     --dist 5 --fields zinc_id,smiles,catalogs
   ```

3. **Analyze results** to identify purchasable analogs (after exporting the task rows):
   ```python
   import pandas as pd

   analogs = pd.read_csv('analogs.tsv', sep='\t')
   print(f"Found {len(analogs)} analogs")
   print(analogs[['zinc_id', 'smiles', 'catalogs']].head(10))
   ```

4. **Retrieve 3D structures** for the most promising analogs

### Workflow 3: Batch Compound Retrieval

1. **Compile list of ZINC IDs** from literature, databases, or previous screens:
   ```python
   zinc_ids = [
       "ZINC000000000001",
       "ZINC000000000002",
       "ZINC000000000003"
   ]
   zinc_ids_str = ",".join(zinc_ids)
   ```

2. **Query ZINC22 API** (one batch request, `zinc_ids` plural):
   ```bash
   curl -X GET "https://cartblanche22.docking.org/substances.txt" \
     -F zinc_ids="ZINC000000000001,ZINC000000000002" \
     -F output_fields="zinc_id,smiles,supplier_code,catalogs"
   ```

3. **Process results** for downstream analysis or purchasing

### Workflow 4: Chemical Space Sampling

1. **Select subset parameters** based on screening goals:
   - Fragment: MW < 250, good for fragment-based drug discovery
   - Lead-like: MW 250-350, LogP ≤ 3.5
   - Drug-like: MW 350-500, follows Lipinski's Rule of Five

2. **Generate random sample**:
   ```bash
   python scripts/query_zinc.py random --count 5000 --subset lead-like \
     --fields zinc_id,smiles,tranche
   ```

3. **Analyze chemical diversity** and prepare for virtual screening

## Output Fields

Customize API responses with the `output_fields` parameter:

**Available fields**:
- `zinc_id`: ZINC identifier
- `smiles`: SMILES string representation
- `sub_id`: Internal substance ID
- `supplier_code`: Vendor catalog number
- `catalogs`: List of suppliers offering the compound
- `tranche`: Encoded molecular properties (H-count, LogP, MW, reactivity phase)

**Example**:
```bash
curl -X GET "https://cartblanche22.docking.org/substances.txt" \
  -F zinc_ids="ZINC000000000001" \
  -F output_fields="zinc_id,smiles,catalogs,tranche"
```

## Tranche System

ZINC organizes compounds into "tranches" based on molecular properties:

**Format**: `H##P###M###-phase`

- **H##**: Number of hydrogen bond donors (00-99)
- **P###**: LogP × 10 (e.g., P035 = LogP 3.5)
- **M###**: Molecular weight in Daltons (e.g., M400 = 400 Da)
- **phase**: Reactivity classification

**Example tranche**: `H05P035M400-0`
- 5 H-bond donors
- LogP = 3.5
- MW = 400 Da
- Reactivity phase 0

Use tranche data to filter compounds by drug-likeness criteria.

## Downloading 3D Structures

For molecular docking, 3D structures are available via file repositories:

**File repository**: https://files.docking.org/zinc22/

Structures are organized by tranches and available in multiple formats:
- MOL2: Multi-molecule format with 3D coordinates
- SDF: Structure-data file format
- DB2.GZ: Compressed database format for DOCK

Refer to ZINC documentation at https://wiki.docking.org for downloading protocols and batch access methods.

## Python Integration

### Submitting searches

Use the bundled `scripts/query_zinc.py` (stdlib only) rather than hand-rolling URLs —
it sends the correct form-encoded POST and returns the JSON task handle:

```python
import json, subprocess

def submit(*args):
    """Run query_zinc.py and return the parsed JSON (task handle or rows)."""
    out = subprocess.run(
        ["python", "scripts/query_zinc.py", *args],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)

task = submit("id", "ZINC000019632618", "--fields", "zinc_id,smiles,catalogs")
# -> {"task": "<uuid>"}; open the UI task view to export rows
```

### Parsing tranche codes

Once you have result rows (a `tranche` column, exported from the UI or read from the
file repository), decode each code. The LogP segment can be negative (`P-005`), so the
regex allows a leading sign:

```python
import re

def parse_tranche(tranche_str):
    """Parse a ZINC tranche code, e.g. 'H05P035M400-0'."""
    match = re.match(r"H(\d+)P(-?\d+)M(\d+)-(\d+)", tranche_str)
    if not match:
        return None
    return {
        "h_donors": int(match.group(1)),
        "logp": int(match.group(2)) / 10.0,
        "mw": int(match.group(3)),
        "phase": int(match.group(4)),
    }

# df["tranche_props"] = df["tranche"].apply(parse_tranche)
```

## Best Practices

### Query Optimization

- **Start specific**: Begin with exact searches before expanding to similarity searches
- **Use appropriate distance parameters**: Small dist values (1-3) for close analogs, larger (5-10) for diverse analogs
- **Limit output fields**: Request only necessary fields to reduce data transfer
- **Batch queries**: Combine multiple ZINC IDs in a single API call when possible

### Performance Considerations

- **Rate limiting**: Respect server resources; avoid rapid consecutive requests
- **Caching**: Store frequently accessed compounds locally
- **Parallel downloads**: When downloading 3D structures, use parallel wget or aria2c for file repositories
- **Subset filtering**: Use lead-like, drug-like, or fragment subsets to reduce search space

### Data Quality

- **Verify availability**: Supplier catalogs change; confirm compound availability before large orders
- **Check stereochemistry**: SMILES may not fully specify stereochemistry; verify 3D structures
- **Validate structures**: Use cheminformatics tools (RDKit, OpenBabel) to verify structure validity
- **Cross-reference**: When possible, cross-check with other databases (PubChem, ChEMBL)

## Resources

### references/api_reference.md

Comprehensive documentation including:

- Complete API endpoint reference
- URL syntax and parameter specifications
- Advanced query patterns and examples
- File repository organization and access
- Bulk download methods
- Error handling and troubleshooting
- Integration with molecular docking software

Consult this document for detailed technical information and advanced usage patterns.

## Important Disclaimers

### Data Reliability

ZINC explicitly states: **"We do not guarantee the quality of any molecule for any purpose and take no responsibility for errors arising from the use of this database."**

- Compound availability may change without notice
- Structure representations may contain errors
- Supplier information should be verified independently
- Use appropriate validation before experimental work

### Appropriate Use

- ZINC is intended for academic and research purposes in drug discovery
- Verify licensing terms for commercial use
- Respect intellectual property when working with patented compounds
- Follow your institution's guidelines for compound procurement

## Additional Resources

- **ZINC Website**: https://zinc.docking.org/
- **CartBlanche22 Interface**: https://cartblanche22.docking.org/
- **ZINC Wiki**: https://wiki.docking.org/
- **File Repository**: https://files.docking.org/zinc22/
- **GitHub**: https://github.com/docking-org/
- **Primary Publications**: Tingle et al., *J. Chem. Inf. Model.* 2023 (ZINC22); Irwin et al., *J. Chem. Inf. Model.* 2020 (ZINC20); Sterling & Irwin, *J. Chem. Inf. Model.* 2015 (ZINC15)

## Citations

When using ZINC in publications, cite the appropriate version:

**ZINC22**:
Tingle, B. I.; Tang, K. G.; Castanon, M.; Gutierrez, J. J.; Khurelbaatar, M.; Dandarchuluun, C.; Moroz, Y. S.; Irwin, J. J. "ZINC-22─A Free Multi-Billion-Scale Database of Tangible Compounds for Ligand Discovery." *Journal of Chemical Information and Modeling* 2023, 63(4), 1166–1176. DOI: 10.1021/acs.jcim.2c01253.

**ZINC20**:
Irwin, J. J.; Tang, K. G.; Young, J.; et al. "ZINC20—A Free Ultralarge-Scale Chemical Database for Ligand Discovery." *Journal of Chemical Information and Modeling* 2020, 60(12), 6065–6073. DOI: 10.1021/acs.jcim.0c00675.

**ZINC15**:
Sterling, T.; Irwin, J. J. "ZINC 15 – Ligand Discovery for Everyone." *Journal of Chemical Information and Modeling* 2015, 55, 2324–2337. DOI: 10.1021/acs.jcim.5b00559.

