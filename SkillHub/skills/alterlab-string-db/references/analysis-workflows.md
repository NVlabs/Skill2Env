# STRING Analysis Workflows

Five end-to-end workflows combining the helper functions in
`scripts/string_api.py`. See `operations.md` for individual function details.

## Workflow 1: Protein List Analysis (Standard Workflow)

**Use case**: Analyze a list of proteins from an experiment (e.g., differential
expression, proteomics).

```python
from scripts.string_api import (string_map_ids, string_network,
                                string_enrichment, string_ppi_enrichment,
                                string_network_image)

# Step 1: Map gene names to STRING IDs
gene_list = ['TP53', 'BRCA1', 'ATM', 'CHEK2', 'MDM2', 'ATR', 'BRCA2']
mapping = string_map_ids(gene_list, species=9606)

# Step 2: Get interaction network
network = string_network(gene_list, species=9606, required_score=400)

# Step 3: Test if network is enriched
ppi_result = string_ppi_enrichment(gene_list, species=9606)

# Step 4: Perform functional enrichment
enrichment = string_enrichment(gene_list, species=9606)

# Step 5: Generate network visualization
img = string_network_image(gene_list, species=9606,
                          network_flavor='evidence', required_score=400)
with open('protein_network.png', 'wb') as f:
    f.write(img)

# Step 6: Parse and interpret results
```

## Workflow 2: Single Protein Investigation

**Use case**: Deep dive into one protein's interactions and partners.

```python
from scripts.string_api import (string_map_ids, string_interaction_partners,
                                string_network_image)

# Step 1: Map protein name
protein = 'TP53'
mapping = string_map_ids(protein, species=9606)

# Step 2: Get all interaction partners
partners = string_interaction_partners(protein, species=9606,
                                      limit=20, required_score=700)

# Step 3: Visualize expanded network
img = string_network_image(protein, species=9606, add_nodes=15,
                          network_flavor='confidence', required_score=700)
with open('tp53_network.png', 'wb') as f:
    f.write(img)
```

## Workflow 3: Pathway-Centric Analysis

**Use case**: Identify and visualize proteins in a specific biological pathway.

```python
from scripts.string_api import string_enrichment, string_network

# Step 1: Start with known pathway proteins
dna_repair_proteins = ['TP53', 'ATM', 'ATR', 'CHEK1', 'CHEK2',
                       'BRCA1', 'BRCA2', 'RAD51', 'XRCC1']

# Step 2: Get network
network = string_network(dna_repair_proteins, species=9606,
                        required_score=700, add_nodes=5)

# Step 3: Enrichment to confirm pathway annotation
enrichment = string_enrichment(dna_repair_proteins, species=9606)

# Step 4: Parse enrichment for DNA repair pathways
import pandas as pd
import io
df = pd.read_csv(io.StringIO(enrichment), sep='\t')
dna_repair = df[df['description'].str.contains('DNA repair', case=False)]
```

## Workflow 4: Cross-Species Analysis

**Use case**: Compare protein interactions across different organisms.

```python
from scripts.string_api import string_network

# Human network
human_network = string_network('TP53', species=9606, required_score=700)

# Mouse network
mouse_network = string_network('Trp53', species=10090, required_score=700)

# Yeast network (if ortholog exists)
yeast_network = string_network('gene_name', species=4932, required_score=700)
```

## Workflow 5: Network Expansion and Discovery

**Use case**: Start with seed proteins and discover connected functional modules.

```python
from scripts.string_api import (string_interaction_partners, string_network,
                                string_enrichment)

# Step 1: Start with seed protein(s)
seed_proteins = ['TP53']

# Step 2: Get first-degree interactors
partners = string_interaction_partners(seed_proteins, species=9606,
                                      limit=30, required_score=700)

# Step 3: Parse partners to get protein list
import pandas as pd
import io
df = pd.read_csv(io.StringIO(partners), sep='\t')
all_proteins = list(set(df['preferredName_A'].tolist() +
                       df['preferredName_B'].tolist()))

# Step 4: Perform enrichment on expanded network
enrichment = string_enrichment(all_proteins[:50], species=9606)

# Step 5: Filter for interesting functional modules
enrichment_df = pd.read_csv(io.StringIO(enrichment), sep='\t')
modules = enrichment_df[enrichment_df['fdr'] < 0.001]
```
