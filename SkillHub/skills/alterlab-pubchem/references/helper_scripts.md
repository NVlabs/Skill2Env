# PubChem — Helper Scripts Reference

This skill ships two helper scripts under `scripts/`. Function inventories below.

## scripts/compound_search.py

Utility functions for searching and retrieving compound information:

- `search_by_name(name, max_results=10)`: Search compounds by name
- `search_by_smiles(smiles)`: Search by SMILES string
- `get_compound_by_cid(cid)`: Retrieve compound by CID
- `get_compound_properties(identifier, namespace, properties)`: Get specific properties
- `similarity_search(smiles, threshold, max_records)`: Perform similarity search
- `substructure_search(smiles, max_records)`: Perform substructure search
- `get_synonyms(identifier, namespace)`: Get all synonyms
- `batch_search(identifiers, namespace, properties)`: Batch search multiple compounds
- `download_structure(identifier, namespace, format, filename)`: Download structures
- `print_compound_info(compound)`: Print formatted compound information

```python
from scripts.compound_search import search_by_name, get_compound_properties

# Search for a compound
compounds = search_by_name('ibuprofen')

# Get specific properties
props = get_compound_properties('aspirin', 'name', ['MolecularWeight', 'XLogP'])
```

## scripts/bioactivity_query.py

Functions for retrieving biological activity data:

- `get_bioassay_summary(cid)`: Get bioassay summary for compound
- `get_compound_bioactivities(cid, activity_outcome)`: Get filtered bioactivities
- `get_assay_description(aid)`: Get detailed assay information
- `get_assay_targets(aid)`: Get biological targets for assay
- `search_assays_by_target(target_name, max_results)`: Find assays by target
- `get_active_compounds_in_assay(aid, max_results)`: Get active compounds
- `get_compound_annotations(cid, section)`: Get PUG-View annotations
- `summarize_bioactivities(cid)`: Generate bioactivity summary statistics
- `find_compounds_by_bioactivity(target, threshold, max_compounds)`: Find compounds by target

```python
from scripts.bioactivity_query import get_bioassay_summary, summarize_bioactivities

# Get bioactivity summary
summary = summarize_bioactivities(2244)  # Aspirin
print(f"Total assays: {summary['total_assays']}")
print(f"Active: {summary['active']}, Inactive: {summary['inactive']}")
```
