# PubChem — Common Workflows

End-to-end recipes. See `capabilities.md` for per-capability snippets and `helper_scripts.md`
for the helper-script function inventory.

## Workflow 1: Chemical Identifier Conversion Pipeline

Convert between different chemical identifiers:

```python
import pubchempy as pcp

# Start with any identifier type
compound = pcp.get_compounds('caffeine', 'name')[0]

# Extract all identifier formats
identifiers = {
    'CID': compound.cid,
    'Name': compound.iupac_name,
    'SMILES': compound.smiles,  # was canonical_smiles (deprecated in 2025)
    'InChI': compound.inchi,
    'InChIKey': compound.inchikey,
    'Formula': compound.molecular_formula
}
```

## Workflow 2: Drug-Like Property Screening

Screen compounds using Lipinski's Rule of Five:

```python
import pubchempy as pcp

def check_drug_likeness(compound_name):
    compound = pcp.get_compounds(compound_name, 'name')[0]

    # Lipinski's Rule of Five
    rules = {
        'MW <= 500': compound.molecular_weight <= 500,
        'LogP <= 5': compound.xlogp <= 5 if compound.xlogp else None,
        'HBD <= 5': compound.h_bond_donor_count <= 5,
        'HBA <= 10': compound.h_bond_acceptor_count <= 10
    }

    violations = sum(1 for v in rules.values() if v is False)
    return rules, violations

rules, violations = check_drug_likeness('aspirin')
print(f"Lipinski violations: {violations}")
```

## Workflow 3: Finding Similar Drug Candidates

Identify structurally similar compounds to a known drug:

```python
import pubchempy as pcp

# Start with known drug
reference_drug = pcp.get_compounds('imatinib', 'name')[0]
reference_smiles = reference_drug.smiles

# Find similar compounds
similar = pcp.get_compounds(
    reference_smiles,
    'smiles',
    searchtype='similarity',
    Threshold=85,
    MaxRecords=20
)

# Filter by drug-like properties
candidates = []
for comp in similar:
    if comp.molecular_weight and 200 <= comp.molecular_weight <= 600:
        if comp.xlogp and -1 <= comp.xlogp <= 5:
            candidates.append(comp)

print(f"Found {len(candidates)} drug-like candidates")
```

## Workflow 4: Batch Compound Property Comparison

Compare properties across multiple compounds:

```python
import pubchempy as pcp
import pandas as pd

compound_list = ['aspirin', 'ibuprofen', 'naproxen', 'celecoxib']

properties_list = []
for name in compound_list:
    try:
        compound = pcp.get_compounds(name, 'name')[0]
        properties_list.append({
            'Name': name,
            'CID': compound.cid,
            'Formula': compound.molecular_formula,
            'MW': compound.molecular_weight,
            'LogP': compound.xlogp,
            'TPSA': compound.tpsa,
            'HBD': compound.h_bond_donor_count,
            'HBA': compound.h_bond_acceptor_count
        })
    except Exception as e:
        print(f"Error processing {name}: {e}")

df = pd.DataFrame(properties_list)
print(df.to_string(index=False))
```

## Workflow 5: Substructure-Based Virtual Screening

Screen for compounds containing specific pharmacophores:

```python
import pubchempy as pcp

# Define pharmacophore (e.g., sulfonamide group)
pharmacophore_smiles = 'S(=O)(=O)N'

# Search for compounds containing this substructure
hits = pcp.get_compounds(
    pharmacophore_smiles,
    'smiles',
    searchtype='substructure',
    MaxRecords=100
)

# Further filter by properties
filtered_hits = [
    comp for comp in hits
    if comp.molecular_weight and comp.molecular_weight < 500
]

print(f"Found {len(filtered_hits)} compounds with desired substructure")
```
