# RCSB PDB API Reference

This document provides detailed information about the RCSB Protein Data Bank APIs, including advanced usage patterns, data schemas, and best practices.

## API Overview

RCSB PDB provides multiple programmatic interfaces:

1. **Data API** - Retrieve PDB data when you have an identifier
2. **Search API** - Find identifiers matching specific search criteria
3. **ModelServer API** - Access macromolecular model subsets
4. **VolumeServer API** - Retrieve volumetric data subsets
5. **Sequence Coordinates API** - Obtain alignments between structural and sequence databases
6. **Alignment API** - Perform structure alignment computations

## Data API

### Core Data Objects

The Data API organizes information hierarchically:

- **core_entry**: PDB entries or Computed Structure Models (CSM IDs start with AF_ or MA_)
- **core_polymer_entity**: Protein, DNA, and RNA entities
- **core_nonpolymer_entity**: Ligands, cofactors, ions
- **core_branched_entity**: Oligosaccharides
- **core_assembly**: Biological assemblies
- **core_polymer_entity_instance**: Individual chains
- **core_chem_comp**: Chemical components

### REST API Endpoints

Base URL: `https://data.rcsb.org/rest/v1/`

**Entry Data:**
```
GET https://data.rcsb.org/rest/v1/core/entry/{entry_id}
```

**Polymer Entity:**
```
GET https://data.rcsb.org/rest/v1/core/polymer_entity/{entry_id}_{entity_id}
```

**Assembly:**
```
GET https://data.rcsb.org/rest/v1/core/assembly/{entry_id}/{assembly_id}
```

**Examples:**
```bash
# Get entry data for hemoglobin
curl https://data.rcsb.org/rest/v1/core/entry/4HHB

# Get first polymer entity
curl https://data.rcsb.org/rest/v1/core/polymer_entity/4HHB_1

# Get biological assembly 1
curl https://data.rcsb.org/rest/v1/core/assembly/4HHB/1
```

### GraphQL API

Endpoint: `https://data.rcsb.org/graphql`

The GraphQL API enables flexible data retrieval, allowing you to grab any piece of data from any level of the hierarchy in a single query.

**Example Query:**
```graphql
{
  entry(entry_id: "4HHB") {
    struct {
      title
    }
    exptl {
      method
    }
    rcsb_entry_info {
      resolution_combined
      deposited_atom_count
      polymer_entity_count
    }
    rcsb_accession_info {
      deposit_date
      initial_release_date
    }
  }
}
```

**Python Example:**
```python
import requests

query = """
{
  polymer_entity(entity_id: "4HHB_1") {
    rcsb_polymer_entity {
      pdbx_description
      formula_weight
    }
    entity_poly {
      pdbx_seq_one_letter_code
      pdbx_strand_id
    }
    rcsb_entity_source_organism {
      ncbi_taxonomy_id
      scientific_name
    }
  }
}
"""

response = requests.post(
    "https://data.rcsb.org/graphql",
    json={"query": query}
)
data = response.json()
```

### Common Data Fields

**Entry Level:**
- `struct.title` - Structure title/description
- `exptl[].method` - Experimental method (X-RAY DIFFRACTION, NMR, ELECTRON MICROSCOPY, etc.)
- `rcsb_entry_info.resolution_combined` - Resolution in Ångströms
- `rcsb_entry_info.deposited_atom_count` - Total number of atoms
- `rcsb_accession_info.deposit_date` - Deposition date
- `rcsb_accession_info.initial_release_date` - Release date

**Polymer Entity Level:**
- `entity_poly.pdbx_seq_one_letter_code` - Primary sequence
- `rcsb_polymer_entity.formula_weight` - Molecular weight
- `rcsb_entity_source_organism.scientific_name` - Source organism
- `rcsb_entity_source_organism.ncbi_taxonomy_id` - NCBI taxonomy ID

**Assembly Level:**
- `rcsb_assembly_info.polymer_entity_count` - Number of polymer entities
- `rcsb_assembly_info.assembly_id` - Assembly identifier

## Search API

### Query Types

The Search API supports seven primary query types:

1. **TextQuery** - Full-text search
2. **AttributeQuery** - Property-based search
3. **SeqSimilarityQuery** - Sequence similarity search
4. **SeqMotifQuery** - Motif pattern search
5. **StructSimilarityQuery** - 3D structure similarity
6. **StructMotifQuery** - Structural motif search
7. **ChemSimilarityQuery** - Chemical similarity search

### AttributeQuery Operators

Available operators for AttributeQuery:

- `exact_match` - Exact string match
- `contains_words` - Contains all words
- `contains_phrase` - Contains exact phrase
- `equals` - Numerical equality
- `greater` - Greater than (numerical)
- `greater_or_equal` - Greater than or equal
- `less` - Less than (numerical)
- `less_or_equal` - Less than or equal
- `range` - Numerical range (closed interval)
- `exists` - Field has a value
- `in` - Value in list

### Common Searchable Attributes

There are two equivalent ways to build an `AttributeQuery`. The idiomatic form
uses the tab-completable `search_attributes` object with Python comparison
operators; the explicit form passes a dotted-path **string** to `AttributeQuery`.
Note: `AttributeQuery(attribute=...)` takes a string path, not an `Attr` object.

**Resolution and Quality:**
```python
from rcsbapi.search import AttributeQuery, search_attributes as attrs

# Idiomatic form
query = attrs.rcsb_entry_info.resolution_combined < 2.0

# Explicit form (equivalent)
query = AttributeQuery(
    attribute="rcsb_entry_info.resolution_combined",
    operator="less",
    value=2.0,
)
```

**Experimental Method:**
```python
from rcsbapi.search import AttributeQuery

query = AttributeQuery(
    attribute="exptl.method",
    operator="exact_match",
    value="X-RAY DIFFRACTION",
)
```

**Organism:**
```python
from rcsbapi.search import search_attributes as attrs

query = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"
```

**Molecular Weight:**
```python
from rcsbapi.search import AttributeQuery

query = AttributeQuery(
    attribute="rcsb_polymer_entity.formula_weight",
    operator="range",
    value=(10000, 50000),  # 10-50 kDa
)
```

**Release Date:**
```python
from rcsbapi.search import AttributeQuery

# Structures released in 2024
query = AttributeQuery(
    attribute="rcsb_accession_info.initial_release_date",
    operator="range",
    value=("2024-01-01", "2024-12-31"),
)
```

### Sequence Similarity Search

Search for structures with similar sequences using MMseqs2:

```python
from rcsbapi.search import SeqSimilarityQuery

# Basic sequence search
query = SeqSimilarityQuery(
    value="MTEYKLVVVGAGGVGKSALTIQLIQNHFVDEYDPTIEDSYRKQVVIDGETCLLDILDTAGQEEYSAMRDQYMRTGEGFLCVFAINNTKSFEDIHHYREQIKRVKDSEDVPMVLVGNKCDLPSRTVDTKQAQDLARSYGIPFIETSAKTRQGVDDAFYTLVREIRKHKEKMSKDGKKKKKKSKTKCVIM",
    evalue_cutoff=0.1,
    identity_cutoff=0.9,
)

# With sequence type specified
query = SeqSimilarityQuery(
    value="ACGTACGTACGT",
    evalue_cutoff=1e-5,
    identity_cutoff=0.8,
    sequence_type="dna",  # or "rna" or "protein"
)
```

### Structure Similarity Search

Find structures with similar 3D geometry using BioZernike:

```python
from rcsbapi.search import StructSimilarityQuery

# Search by entry
query = StructSimilarityQuery(
    structure_search_type="entry",
    entry_id="4HHB"
)

# Search by chain
query = StructSimilarityQuery(
    structure_search_type="chain",
    entry_id="4HHB",
    chain_id="A"
)

# Search by assembly
query = StructSimilarityQuery(
    structure_search_type="assembly",
    entry_id="4HHB",
    assembly_id="1"
)
```

### Combining Queries

Use Python bitwise operators to combine queries:

```python
from rcsbapi.search import TextQuery, search_attributes as attrs

# AND operation (&)
query1 = TextQuery("kinase")
query2 = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"
combined = query1 & query2

# OR operation (|)
organism1 = attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens"
organism2 = attrs.rcsb_entity_source_organism.scientific_name == "Mus musculus"
combined = organism1 | organism2

# NOT operation (~)
all_structures = TextQuery("protein")
low_res = attrs.rcsb_entry_info.resolution_combined > 3.0
high_res_only = all_structures & (~low_res)

# Complex combinations
high_res_human_kinases = (
    TextQuery("kinase")
    & (attrs.rcsb_entity_source_organism.scientific_name == "Homo sapiens")
    & (attrs.rcsb_entry_info.resolution_combined < 2.5)
)
```

### Return Types

Control what information is returned. `return_type` is a string keyword argument
(valid values: "entry", "assembly", "polymer_entity", "non_polymer_entity",
"polymer_instance", "mol_definition"; default "entry"). There is no `ReturnType`
enum. To get scores, set `results_verbosity` ("minimal" = scores only,
"verbose" = all metadata, "compact" = IDs only, the default).

```python
from rcsbapi.search import TextQuery

query = TextQuery("hemoglobin")

# Return entry IDs (default)
results = list(query())  # ['4HHB', '1A3N', ...]

# Return entry IDs with scores
results = list(query(results_verbosity="minimal"))
# [{'identifier': '4HHB', 'score': 0.95}, ...]

# Return polymer entities
results = list(query(return_type="polymer_entity"))
# ['4HHB_1', '4HHB_2', ...]
```

## File Download URLs

### Structure Files

**PDB Format (legacy):**
```
https://files.rcsb.org/download/{PDB_ID}.pdb
```

**mmCIF Format (modern standard):**
```
https://files.rcsb.org/download/{PDB_ID}.cif
```

**Structure Factors:**
```
https://files.rcsb.org/download/{PDB_ID}-sf.cif
```

**Biological Assembly:**
```
https://files.rcsb.org/download/{PDB_ID}.pdb1  # Assembly 1
https://files.rcsb.org/download/{PDB_ID}.pdb2  # Assembly 2
```

**FASTA Sequence:**
```
https://www.rcsb.org/fasta/entry/{PDB_ID}
```

### Python Download Helper

```python
import requests

def download_pdb_file(pdb_id, format="pdb", output_dir="."):
    """
    Download PDB structure file.

    Args:
        pdb_id: 4-character PDB ID
        format: 'pdb' or 'cif'
        output_dir: Directory to save file
    """
    base_url = "https://files.rcsb.org/download"
    url = f"{base_url}/{pdb_id}.{format}"

    response = requests.get(url)
    if response.status_code == 200:
        output_path = f"{output_dir}/{pdb_id}.{format}"
        with open(output_path, "w") as f:
            f.write(response.text)
        print(f"Downloaded {pdb_id}.{format}")
        return output_path
    else:
        print(f"Error downloading {pdb_id}: {response.status_code}")
        return None

# Usage
download_pdb_file("4HHB", format="pdb")
download_pdb_file("4HHB", format="cif")
```

## Rate Limiting and Best Practices

### Rate Limits

- The API implements rate limiting to ensure fair usage
- If you exceed the limit, you'll receive a 429 HTTP error code
- Recommended starting point: a few requests per second
- Use exponential backoff to find acceptable request rates

### Exponential Backoff Implementation

```python
import time
import requests

def fetch_with_retry(url, max_retries=5, initial_delay=1):
    """
    Fetch URL with exponential backoff on rate limit errors.

    Args:
        url: URL to fetch
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
    """
    delay = initial_delay

    for attempt in range(max_retries):
        response = requests.get(url)

        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            print(f"Rate limited. Waiting {delay}s before retry...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        else:
            response.raise_for_status()

    raise Exception(f"Failed after {max_retries} retries")
```

### Batch Processing Best Practices

1. **Use Search API first** to get the list of IDs, then fetch data
2. **Fetch in one DataQuery** — `input_ids` accepts many IDs at once, so prefer a
   single query (optionally with `batch_size`) over a per-ID loop
3. **Cache results** to avoid redundant queries
4. **Add delays** only if you fall back to many separate raw HTTP requests

`DataQuery` retrieves all requested IDs in one call. For very large ID lists pass
`batch_size` to `exec()` so the client chunks the GraphQL request for you:

```python
from rcsbapi.search import TextQuery
from rcsbapi.data import DataQuery

def batch_fetch_structures(query, fields=None):
    """Fetch entry data for every PDB ID matching a search query."""
    pdb_ids = list(query())
    print(f"Found {len(pdb_ids)} structures")

    data_query = DataQuery(
        input_type="entries",
        input_ids=pdb_ids,
        return_data_list=fields or ["rcsb_id", "struct.title", "exptl.method"],
    )
    # batch_size chunks large ID lists into multiple requests automatically
    response = data_query.exec(batch_size=200)
    return {e["rcsb_id"]: e for e in response["data"]["entries"]}

results = batch_fetch_structures(TextQuery("hemoglobin"))
```

## Advanced Use Cases

### Finding Drug-Target Complexes

```python
from rcsbapi.search import AttributeQuery

# Find structures containing a specific ligand (3-letter chemical component ID)
query = AttributeQuery(
    attribute="rcsb_nonpolymer_entity_instance_container_identifiers.comp_id",
    operator="exact_match",
    value="ATP",  # or other ligand code
)

results = list(query())
print(f"Found {len(results)} structures with ATP")
```

### Filtering by Resolution and R-factor

```python
from rcsbapi.search import search_attributes as attrs

# High-quality X-ray structures
resolution_query = attrs.rcsb_entry_info.resolution_combined < 2.0
rfactor_query = attrs.refine.ls_R_factor_R_free < 0.25

high_quality = resolution_query & rfactor_query
results = list(high_quality())
```

### Finding Recent Structures

```python
import datetime
from rcsbapi.search import AttributeQuery

# Structures released in the last month
one_month_ago = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
today = datetime.date.today().isoformat()

query = AttributeQuery(
    attribute="rcsb_accession_info.initial_release_date",
    operator="range",
    value=(one_month_ago, today),
)

recent_structures = list(query())
```

## Troubleshooting

### Common Errors

**404 Not Found:**
- PDB ID doesn't exist or is obsolete
- Check if ID is correct (case-sensitive)
- Verify entry hasn't been superseded

**429 Too Many Requests:**
- Rate limit exceeded
- Implement exponential backoff
- Reduce request frequency

**500 Internal Server Error:**
- Temporary server issue
- Retry after short delay
- Check RCSB PDB status page

**Empty Results:**
- Query too restrictive
- Check attribute names and operators
- Verify data exists for searched field

### Debugging Tips

```python
# Enable verbose output for searches
from rcsbapi.search import TextQuery

query = TextQuery("hemoglobin")
print(query.to_dict())  # See query structure

# Check query JSON
import json
print(json.dumps(query.to_dict(), indent=2))

# Test with curl
import subprocess
result = subprocess.run(
    ["curl", "https://data.rcsb.org/rest/v1/core/entry/4HHB"],
    capture_output=True,
    text=True
)
print(result.stdout)
```

## Additional Resources

- **API Documentation:** https://www.rcsb.org/docs/programmatic-access/web-apis-overview
- **Data API Redoc:** https://data.rcsb.org/redoc/index.html
- **GraphQL Schema:** https://data.rcsb.org/graphql
- **Python Package Docs:** https://rcsbapi.readthedocs.io/
- **GitHub Issues:** https://github.com/rcsb/py-rcsb-api/issues
- **Community Forum:** https://www.rcsb.org/help
