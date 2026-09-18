# STRING Core Operations

Eight helper-function operations from `scripts/string_api.py`. For the
underlying REST endpoints, output formats, and full parameter specs, see
`string_reference.md`.

## 1. Identifier Mapping (`string_map_ids`)

Convert gene names, protein names, and external IDs to STRING identifiers.

**When to use**: Starting any STRING analysis, validating protein names, finding
canonical identifiers.

```python
from scripts.string_api import string_map_ids

# Map single protein
result = string_map_ids('TP53', species=9606)

# Map multiple proteins
result = string_map_ids(['TP53', 'BRCA1', 'EGFR', 'MDM2'], species=9606)

# Map with multiple matches per query
result = string_map_ids('p53', species=9606, limit=5)
```

**Parameters**:
- `species`: NCBI taxon ID (9606 = human, 10090 = mouse, 7227 = fly)
- `limit`: Number of matches per identifier (default: 1)
- `echo_query`: Include query term in output (default: 1)

**Best practice**: Always map identifiers first for faster subsequent queries.

## 2. Network Retrieval (`string_network`)

Get protein-protein interaction network data in tabular format.

**When to use**: Building interaction networks, analyzing connectivity,
retrieving interaction evidence.

```python
from scripts.string_api import string_network

# Get network for single protein
network = string_network('9606.ENSP00000269305', species=9606)

# Get network with multiple proteins
proteins = ['9606.ENSP00000269305', '9606.ENSP00000275493']
network = string_network(proteins, required_score=700)

# Expand network with additional interactors
network = string_network('TP53', species=9606, add_nodes=10, required_score=400)

# Physical interactions only
network = string_network('TP53', species=9606, network_type='physical')
```

**Parameters**:
- `required_score`: Confidence threshold (0-1000)
  - 150: low confidence (exploratory)
  - 400: medium confidence (default, standard analysis)
  - 700: high confidence (conservative)
  - 900: highest confidence (very stringent)
- `network_type`: `'functional'` (all evidence, default) or `'physical'`
  (direct binding only)
- `add_nodes`: Add N most connected proteins (0-10)

**Output columns**: Interaction pairs, confidence scores, and individual
evidence scores (neighborhood, fusion, coexpression, experimental, database,
text-mining).

## 3. Network Visualization (`string_network_image`)

Generate network visualization as a PNG image.

**When to use**: Creating figures, visual exploration, presentations.

```python
from scripts.string_api import string_network_image

# Get network image
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1']
img_data = string_network_image(proteins, species=9606, required_score=700)

# Save image
with open('network.png', 'wb') as f:
    f.write(img_data)

# Evidence-colored network
img = string_network_image(proteins, species=9606, network_flavor='evidence')

# Confidence-based visualization
img = string_network_image(proteins, species=9606, network_flavor='confidence')

# Actions network (activation/inhibition)
img = string_network_image(proteins, species=9606, network_flavor='actions')
```

**Network flavors**:
- `'evidence'`: Colored lines show evidence types (default)
- `'confidence'`: Line thickness represents confidence
- `'actions'`: Shows activating/inhibiting relationships

## 4. Interaction Partners (`string_interaction_partners`)

Find all proteins that interact with given protein(s).

**When to use**: Discovering novel interactions, finding hub proteins, expanding
networks.

```python
from scripts.string_api import string_interaction_partners

# Get top 10 interactors of TP53
partners = string_interaction_partners('TP53', species=9606, limit=10)

# Get high-confidence interactors
partners = string_interaction_partners('TP53', species=9606,
                                      limit=20, required_score=700)

# Find interactors for multiple proteins
partners = string_interaction_partners(['TP53', 'MDM2'],
                                      species=9606, limit=15)
```

**Parameters**:
- `limit`: Maximum number of partners to return (default: 10)
- `required_score`: Confidence threshold (0-1000)

**Use cases**: hub protein identification, network expansion from seed proteins,
discovering indirect connections.

## 5. Functional Enrichment (`string_enrichment`)

Perform enrichment analysis across Gene Ontology, KEGG pathways, Pfam domains,
and more.

**When to use**: Interpreting protein lists, pathway analysis, functional
characterization, understanding biological processes.

```python
from scripts.string_api import string_enrichment

# Enrichment for a protein list
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1', 'ATR', 'TP73']
enrichment = string_enrichment(proteins, species=9606)

# Parse results to find significant terms
import pandas as pd
import io
df = pd.read_csv(io.StringIO(enrichment), sep='\t')
significant = df[df['fdr'] < 0.05]
```

**Enrichment categories**: Gene Ontology (Biological Process, Molecular
Function, Cellular Component), KEGG Pathways, Pfam, InterPro, SMART, UniProt
Keywords.

**Output columns**:
- `category`: Annotation database (e.g., "KEGG Pathways", "GO Biological Process")
- `term`: Term identifier
- `description`: Human-readable term description
- `number_of_genes`: Input proteins with this annotation
- `p_value`: Uncorrected enrichment p-value
- `fdr`: False discovery rate (corrected p-value)

**Statistical method**: Fisher's exact test with Benjamini-Hochberg FDR
correction. **Interpretation**: FDR < 0.05 indicates significant enrichment.

## 6. PPI Enrichment (`string_ppi_enrichment`)

Test if a protein network has significantly more interactions than expected by
chance.

**When to use**: Validating if proteins form a functional module, testing
network connectivity.

```python
from scripts.string_api import string_ppi_enrichment
import json

# Test network connectivity
proteins = ['TP53', 'MDM2', 'ATM', 'CHEK2', 'BRCA1']
result = string_ppi_enrichment(proteins, species=9606, required_score=400)

# Parse JSON result
data = json.loads(result)
print(f"Observed edges: {data['number_of_edges']}")
print(f"Expected edges: {data['expected_number_of_edges']}")
print(f"P-value: {data['p_value']}")
```

**Output fields**: `number_of_nodes`, `number_of_edges`,
`expected_number_of_edges`, `p_value`.

**Interpretation**:
- p-value < 0.05: Network significantly enriched (proteins likely form a module)
- p-value ≥ 0.05: No significant enrichment (proteins may be unrelated)

## 7. Homology Scores (`string_homology`)

Retrieve protein similarity and homology information.

**When to use**: Identifying protein families, paralog analysis, cross-species
comparisons.

```python
from scripts.string_api import string_homology

# Get homology between proteins
proteins = ['TP53', 'TP63', 'TP73']  # p53 family
homology = string_homology(proteins, species=9606)
```

**Use cases**: protein family identification, paralog discovery, evolutionary
analysis.

## 8. Version Information (`string_version`)

Get the current STRING database version.

**When to use**: Ensuring reproducibility, documenting methods.

```python
from scripts.string_api import string_version

version = string_version()
print(f"STRING version: {version}")
```
