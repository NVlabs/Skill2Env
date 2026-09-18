---
name: alterlab-pdb
description: Access the RCSB Protein Data Bank (PDB) for EXPERIMENTALLY determined 3D structures (X-ray, cryo-EM, NMR) of proteins and nucleic acids — searching by text, sequence, or structure similarity and downloading coordinates in PDB/mmCIF format with metadata. Use when retrieving a structure by PDB ID, running sequence or structure similarity searches, or obtaining experimental coordinates for structural biology and drug discovery; for AI-PREDICTED structures of proteins lacking experimental data prefer alterlab-alphafold-db, and for protein sequences, annotations, or accession ID mapping prefer alterlab-uniprot instead. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read WebFetch Bash(curl:*) Bash(python:*)
compatibility: Keyless RCSB PDB REST API (no authentication required)
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# PDB Database

## Overview

RCSB PDB is the worldwide repository for 3D structural data of biological macromolecules. Search for structures, retrieve coordinates and metadata, perform sequence and structure similarity searches across 200,000+ experimentally determined structures and computed models.

## Scripts

`scripts/query_pdb.py` — RCSB Search + Data + file APIs (stdlib only, JSON to stdout):

```bash
python scripts/query_pdb.py search hemoglobin --rows 25     # full-text search (entry IDs)
python scripts/query_pdb.py entry 4HHB                      # entry metadata
python scripts/query_pdb.py download 4HHB --format cif      # download coordinates
```

## When to Use This Skill

This skill should be used when:
- Searching for protein or nucleic acid 3D structures by text, sequence, or structural similarity
- Downloading coordinate files in PDB, mmCIF, or BinaryCIF formats
- Retrieving structural metadata, experimental methods, or quality metrics
- Performing batch operations across multiple structures
- Integrating PDB data into computational workflows for drug discovery, protein engineering, or structural biology research

## Core Capabilities

### 1. Searching for Structures

Find PDB entries using various search criteria:

**Text Search:** Search by protein name, keywords, or descriptions
```python
from rcsbapi.search import TextQuery
query = TextQuery("hemoglobin")
results = list(query())
print(f"Found {len(results)} structures")
```

**Attribute Search:** Query specific properties (organism, resolution, method, etc.)
```python
from rcsbapi.search import AttributeQuery
from rcsbapi.search import search_attributes as attrs

# Find human protein structures (idiomatic form — recommended)
query = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"
results = list(query())

# OR explicit AttributeQuery with a dotted-path STRING (not the Attr object):
query = AttributeQuery(
    attribute="rcsb_entity_source_organism.scientific_name",
    operator="exact_match",
    value="Homo sapiens",
)
results = list(query())
```

**Sequence Similarity:** Find structures similar to a given sequence
```python
from rcsbapi.search import SeqSimilarityQuery

query = SeqSimilarityQuery(
    value="MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQGVDDAFYTLVREIRKHKEKMSKDGKKKKKKSKTKCVIM",
    evalue_cutoff=0.1,
    identity_cutoff=0.9,
    sequence_type="protein"
)
results = list(query())
```

**Structure Similarity:** Find structures with similar 3D geometry
```python
from rcsbapi.search import StructSimilarityQuery

query = StructSimilarityQuery(
    structure_search_type="entry",
    entry_id="4HHB"  # Hemoglobin
)
results = list(query())
```

**Combining Queries:** Use logical operators to build complex searches
```python
from rcsbapi.search import search_attributes as attrs

# High-resolution human proteins
query1 = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"
query2 = attrs.rcsb_entry_info.resolution_combined < 2.0
combined_query = query1 & query2  # AND operation
results = list(combined_query())
```

### 2. Retrieving Structure Data

Access detailed information about specific PDB entries:

**Basic Entry Information:**
```python
from rcsbapi.data import DataQuery

# Get entry-level data
query = DataQuery(
    input_type="entries",
    input_ids=["4HHB"],
    return_data_list=["struct.title", "exptl.method"],
)
data = query.exec()  # synchronous; returns a dict
entry = data["data"]["entries"][0]
print(entry["struct"]["title"])
print(entry["exptl"][0]["method"])
```

**Polymer Entity Information:**
```python
from rcsbapi.data import DataQuery

# Get protein/nucleic acid information
query = DataQuery(
    input_type="polymer_entities",
    input_ids=["4HHB_1"],
    return_data_list=["entity_poly.pdbx_seq_one_letter_code"],
)
data = query.exec()
entity = data["data"]["polymer_entities"][0]
print(entity["entity_poly"]["pdbx_seq_one_letter_code"])
```

**Building Queries (GraphQL under the hood):**
```python
from rcsbapi.data import DataQuery

# DataQuery builds the GraphQL query for you from input_type/input_ids/return_data_list;
# there is no separate fetch(query_type="graphql", ...) entry point.
query = DataQuery(
    input_type="entries",
    input_ids=["4HHB"],
    return_data_list=[
        "struct.title",
        "exptl.method",
        "rcsb_entry_info.resolution_combined",
        "rcsb_entry_info.deposited_atom_count",
    ],
)
# Inspect the auto-generated GraphQL / open it in the editor:
print(query.get_editor_link())
data = query.exec()
```

### 3. Downloading Structure Files

Retrieve coordinate files in various formats:

**Download Methods:**
- **PDB format** (legacy text format): `https://files.rcsb.org/download/{PDB_ID}.pdb`
- **mmCIF format** (modern standard): `https://files.rcsb.org/download/{PDB_ID}.cif`
- **BinaryCIF** (compressed binary): Use ModelServer API for efficient access
- **Biological assembly**: `https://files.rcsb.org/download/{PDB_ID}.pdb1` (for assembly 1)

**Example Download:**
```python
import requests

pdb_id = "4HHB"

# Download PDB format
pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
response = requests.get(pdb_url)
with open(f"{pdb_id}.pdb", "w") as f:
    f.write(response.text)

# Download mmCIF format
cif_url = f"https://files.rcsb.org/download/{pdb_id}.cif"
response = requests.get(cif_url)
with open(f"{pdb_id}.cif", "w") as f:
    f.write(response.text)
```

### 4. Working with Structure Data

Common operations with retrieved structures:

**Parse and Analyze Coordinates:**
Use BioPython or other structural biology libraries to work with downloaded files:
```python
from Bio.PDB import PDBParser

parser = PDBParser()
structure = parser.get_structure("protein", "4HHB.pdb")

# Iterate through atoms
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                print(atom.get_coord())
```

**Extract Metadata:**
```python
from rcsbapi.data import DataQuery

# Get experimental details
query = DataQuery(
    input_type="entries",
    input_ids=["4HHB"],
    return_data_list=[
        "rcsb_entry_info.resolution_combined",
        "exptl.method",
        "rcsb_accession_info.deposit_date",
    ],
)
data = query.exec()["data"]["entries"][0]

resolution = data.get("rcsb_entry_info", {}).get("resolution_combined")
method = data.get("exptl", [{}])[0].get("method")
deposition_date = data.get("rcsb_accession_info", {}).get("deposit_date")

print(f"Resolution: {resolution} Å")
print(f"Method: {method}")
print(f"Deposited: {deposition_date}")
```

### 5. Batch Operations

Process multiple structures efficiently:

```python
from rcsbapi.data import DataQuery

pdb_ids = ["4HHB", "1MBN", "1GZX"]  # Hemoglobin, myoglobin, etc.

# A single DataQuery can fetch all entries at once
query = DataQuery(
    input_type="entries",
    input_ids=pdb_ids,
    return_data_list=[
        "rcsb_id",
        "struct.title",
        "rcsb_entry_info.resolution_combined",
        "rcsb_entity_source_organism.scientific_name",
    ],
)

results = {}
for data in query.exec()["data"]["entries"]:
    pdb_id = data["rcsb_id"]
    results[pdb_id] = {
        "title": data["struct"]["title"],
        "resolution": data.get("rcsb_entry_info", {}).get("resolution_combined"),
        "organism": data.get("rcsb_entity_source_organism", [{}])[0].get("scientific_name")
    }

# Display results
for pdb_id, info in results.items():
    print(f"\n{pdb_id}: {info['title']}")
    print(f"  Resolution: {info['resolution']} Å")
    print(f"  Organism: {info['organism']}")
```

## Python Package Installation

Install the official RCSB PDB Python API client (`rcsb-api`, current major version
1.x; examples here target `>=1.7`):

```bash
uv pip install "rcsb-api>=1.7"
```

The `rcsb-api` package provides unified access to both Search and Data APIs through
the `rcsbapi.search` and `rcsbapi.data` modules. (The older `rcsbsearchapi` package
is superseded by `rcsb-api` and its `import rcsbsearchapi` path is gone — prefer
`rcsb-api` for new code.)

The `scripts/query_pdb.py` helper needs none of this — it hits the public REST APIs
with only the Python standard library.

## Common Use Cases

### Drug Discovery
- Search for structures of drug targets
- Analyze ligand binding sites
- Compare protein-ligand complexes
- Identify similar binding pockets

### Protein Engineering
- Find homologous structures for modeling
- Analyze sequence-structure relationships
- Compare mutant structures
- Study protein stability and dynamics

### Structural Biology Research
- Download structures for computational analysis
- Build structure-based alignments
- Analyze structural features (secondary structure, domains)
- Compare experimental methods and quality metrics

### Education and Visualization
- Retrieve structures for teaching
- Generate molecular visualizations
- Explore structure-function relationships
- Study evolutionary conservation

## Key Concepts

**PDB ID:** Unique 4-character identifier (e.g., "4HHB") for each structure entry. AlphaFold and ModelArchive entries start with "AF_" or "MA_" prefixes.

**mmCIF/PDBx:** Modern file format that uses key-value structure, replacing legacy PDB format for large structures.

**Biological Assembly:** The functional form of a macromolecule, which may contain multiple copies of chains from the asymmetric unit.

**Resolution:** Measure of detail in crystallographic structures (lower values = higher detail). Typical range: 1.5-3.5 Å for high-quality structures.

**Entity:** A unique molecular component in a structure (protein chain, DNA, ligand, etc.).

## Resources

This skill includes reference documentation in the `references/` directory:

### references/api_reference.md
Comprehensive API documentation covering:
- Detailed API endpoint specifications
- Advanced query patterns and examples
- Data schema reference
- Rate limiting and best practices
- Troubleshooting common issues

Use this reference when you need in-depth information about API capabilities, complex query construction, or detailed data schema information.

## Additional Resources

- **RCSB PDB Website:** https://www.rcsb.org
- **PDB-101 Educational Portal:** https://pdb101.rcsb.org
- **API Documentation:** https://www.rcsb.org/docs/programmatic-access/web-apis-overview
- **Python Package Docs:** https://rcsbapi.readthedocs.io/
- **Data API Documentation:** https://data.rcsb.org/
- **GitHub Repository:** https://github.com/rcsb/py-rcsb-api

