# PubChem — Capabilities & Code Examples

Copy-ready snippets for each PubChem capability area. For full PUG-REST endpoints and the
complete property list, see `api_reference.md`. For end-to-end recipes, see `workflows.md`.

## 1. Chemical Structure Search

Search for compounds using multiple identifier types.

**By Chemical Name**:
```python
import pubchempy as pcp
compounds = pcp.get_compounds('aspirin', 'name')
compound = compounds[0]
```

**By CID (Compound ID)**:
```python
compound = pcp.Compound.from_cid(2244)  # Aspirin
```

**By SMILES**:
```python
compound = pcp.get_compounds('CC(=O)OC1=CC=CC=C1C(=O)O', 'smiles')[0]
```

**By InChI**:
```python
compound = pcp.get_compounds('InChI=1S/C9H8O4/...', 'inchi')[0]
```

**By Molecular Formula**:
```python
compounds = pcp.get_compounds('C9H8O4', 'formula')
# Returns all compounds matching this formula
```

## 2. Property Retrieval

**Using PubChemPy (Recommended)**:
```python
import pubchempy as pcp

# Get compound object with all properties
compound = pcp.get_compounds('caffeine', 'name')[0]

# Access individual properties
molecular_formula = compound.molecular_formula
molecular_weight = compound.molecular_weight
iupac_name = compound.iupac_name
smiles = compound.smiles  # full SMILES (was canonical_smiles, now deprecated)
inchi = compound.inchi
xlogp = compound.xlogp  # Partition coefficient
tpsa = compound.tpsa    # Topological polar surface area
```

**Get Specific Properties**:
```python
properties = pcp.get_properties(
    ['MolecularFormula', 'MolecularWeight', 'SMILES', 'XLogP'],
    'aspirin',
    'name'
)
# Returns list of dictionaries
```

**Batch Property Retrieval**:
```python
import pandas as pd

compound_names = ['aspirin', 'ibuprofen', 'paracetamol']
all_properties = []

for name in compound_names:
    props = pcp.get_properties(
        ['MolecularFormula', 'MolecularWeight', 'XLogP'],
        name,
        'name'
    )
    all_properties.extend(props)

df = pd.DataFrame(all_properties)
```

**Available Properties**: MolecularFormula, MolecularWeight, SMILES, ConnectivitySMILES,
InChI, InChIKey, IUPACName, XLogP, TPSA, HBondDonorCount, HBondAcceptorCount,
RotatableBondCount, Complexity, Charge, and many more (see `api_reference.md` for the
complete list). Note: `CanonicalSMILES`/`IsomericSMILES` were deprecated in 2025 in favor of
`ConnectivitySMILES`/`SMILES`.

## 3. Similarity Search

Find structurally similar compounds using Tanimoto similarity:

```python
import pubchempy as pcp

# Start with a query compound
query_compound = pcp.get_compounds('gefitinib', 'name')[0]
query_smiles = query_compound.smiles

# Perform similarity search
similar_compounds = pcp.get_compounds(
    query_smiles,
    'smiles',
    searchtype='similarity',
    Threshold=85,  # Similarity threshold (0-100)
    MaxRecords=50
)

# Process results
for compound in similar_compounds[:10]:
    print(f"CID {compound.cid}: {compound.iupac_name}")
    print(f"  MW: {compound.molecular_weight}")
```

**Note**: Similarity searches are asynchronous for large queries and may take 15-30 seconds
to complete. PubChemPy handles the asynchronous pattern automatically.

## 4. Substructure Search

Find compounds containing a specific structural motif:

```python
import pubchempy as pcp

# Search for compounds containing pyridine ring
pyridine_smiles = 'c1ccncc1'

matches = pcp.get_compounds(
    pyridine_smiles,
    'smiles',
    searchtype='substructure',
    MaxRecords=100
)

print(f"Found {len(matches)} compounds containing pyridine")
```

**Common Substructures**:
- Benzene ring: `c1ccccc1`
- Pyridine: `c1ccncc1`
- Phenol: `c1ccc(O)cc1`
- Carboxylic acid: `C(=O)O`

## 5. Format Conversion

Convert between different chemical structure formats:

```python
import pubchempy as pcp

compound = pcp.get_compounds('aspirin', 'name')[0]

# Convert to different formats
smiles = compound.smiles
inchi = compound.inchi
inchikey = compound.inchikey
cid = compound.cid

# Download structure files
pcp.download('SDF', 'aspirin', 'name', 'aspirin.sdf', overwrite=True)
pcp.download('JSON', '2244', 'cid', 'aspirin.json', overwrite=True)
```

## 6. Structure Visualization

Generate 2D structure images:

```python
import pubchempy as pcp

# Download compound structure as PNG
pcp.download('PNG', 'caffeine', 'name', 'caffeine.png', overwrite=True)

# Using direct URL (via requests)
import requests

cid = 2244  # Aspirin
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/PNG?image_size=large"
response = requests.get(url)

with open('structure.png', 'wb') as f:
    f.write(response.content)
```

## 7. Synonym Retrieval

Get all known names and synonyms for a compound:

```python
import pubchempy as pcp

synonyms_data = pcp.get_synonyms('aspirin', 'name')

if synonyms_data:
    cid = synonyms_data[0]['CID']
    synonyms = synonyms_data[0]['Synonym']

    print(f"CID {cid} has {len(synonyms)} synonyms:")
    for syn in synonyms[:10]:  # First 10
        print(f"  - {syn}")
```

## 8. Bioactivity Data Access

Retrieve biological activity data from assays:

```python
import requests
import json

# Get bioassay summary for a compound
cid = 2244  # Aspirin
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/assaysummary/JSON"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    # Process bioassay information
    table = data.get('Table', {})
    rows = table.get('Row', [])
    print(f"Found {len(rows)} bioassay records")
```

**For more complex bioactivity queries**, use the `scripts/bioactivity_query.py` helper
script which provides bioassay summaries with activity-outcome filtering, assay target
identification, search for compounds by biological target, and active-compound lists.

## 9. Comprehensive Compound Annotations

Access detailed compound information through PUG-View:

```python
import requests

cid = 2244
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"

response = requests.get(url)
if response.status_code == 200:
    annotations = response.json()
    # Contains extensive data including:
    # - Chemical and Physical Properties
    # - Drug and Medication Information
    # - Pharmacology and Biochemistry
    # - Safety and Hazards
    # - Toxicity
    # - Literature references
    # - Patents
```

**Get Specific Section**:
```python
# Get only drug information
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON?heading=Drug and Medication Information"
```
