---
name: alterlab-primekg
description: Queries the Precision Medicine Knowledge Graph (PrimeKG) for multiscale biomedical relationships across genes, drugs, diseases, phenotypes, pathways, and biological processes. Use when exploring drug-disease or gene-disease links, building disease-centric knowledge subgraphs, or sourcing relations for drug repurposing and precision-medicine analyses. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs under `uv run python` with pandas installed and the PrimeKG `kg.csv` available locally (set `PRIMEKG_DATA_PATH`); no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# PrimeKG Knowledge Graph Skill

## Overview

PrimeKG (Chandak, Huang & Zitnik, *Scientific Data* 2023; mims-harvard/PrimeKG) is a precision medicine knowledge graph integrating 20 primary resources. It contains 129,375 nodes and 4,050,249 edges across 30 edge types and 10 node types, including drug-target, disease-gene, and disease-phenotype associations.

**Key capabilities:**
- Search for nodes (genes, proteins, drugs, diseases, phenotypes)
- Retrieve direct neighbors (associated entities and clinical evidence)
- Analyze local disease context (related genes, drugs, phenotypes)
- Identify drug-disease paths (potential repurposing opportunities)

**Data access:** Programmatic access via `scripts/query_primekg.py`. Point the loader at the `kg.csv` released on Harvard Dataverse via the `PRIMEKG_DATA_PATH` environment variable (it defaults to `../data/kg.csv` relative to the script). All functions operate on the `x_*`/`y_*`/`relation`/`display_relation` columns of `kg.csv`.

## When to Use This Skill

This skill should be used when:

- **Knowledge-based drug discovery:** Identifying targets and mechanisms for diseases.
- **Drug repurposing:** Finding existing drugs that might have evidence for new indications.
- **Phenotype analysis:** Understanding how symptoms/phenotypes relate to diseases and genes.
- **Multiscale biology:** Bridging the gap between molecular targets (genes) and clinical outcomes (diseases).
- **Network pharmacology:** Investigating the broader network effects of drug-target interactions.

## Core Workflow

Run under `uv run python` from the skill directory (so `scripts/` is importable),
or add the `scripts/` dir to `sys.path`. Set `PRIMEKG_DATA_PATH` to your `kg.csv`.

### 1. Search for Entities

Find identifiers for genes, drugs, or diseases. Pass `node_type` using PrimeKG's
exact type strings (see node types below) — e.g. `"gene/protein"`, not `"gene"`.

```python
from scripts.query_primekg import search_nodes

# Search for Alzheimer's disease nodes
results = search_nodes("Alzheimer", node_type="disease")
# Returns: [{"id": <MONDO id>, "type": "disease", "name": "...",
#            "source": "MONDO" | "MONDO_grouped"}, ...]
# Disease ids are MONDO ids; PrimeKG groups diseases, so one name can map to
# several MONDO ids. Use the returned id with get_neighbors.
```

### 2. Get Neighbors (Direct Associations)

Retrieve all connected nodes and relationship types.

```python
from scripts.query_primekg import get_neighbors

# Get all neighbors of a specific disease ID (the MONDO id from search_nodes)
neighbors = get_neighbors(disease_id, relation_type="disease_protein")
# Returns: List of neighbors like
#   {"neighbor_name": "APOE", "neighbor_type": "gene/protein",
#    "relation": "disease_protein", "display_relation": "associated with", ...}
```

### 3. Analyze Disease Context

A high-level function to summarize associations for a disease.

```python
from scripts.query_primekg import get_disease_context

# Comprehensive summary for a disease
context = get_disease_context("Alzheimer")
# Access: context['associated_genes'], context['associated_drugs'],
#         context['phenotypes'], context['related_diseases']
```

### 4. Trace Drug-Disease Paths (Repurposing)

Find depth-2 paths (drug -> shared gene/protein target -> disease) as graph-based
repurposing evidence.

```python
from scripts.query_primekg import find_paths

# drug_id and disease_id come from search_nodes
paths = find_paths(drug_id, disease_id, max_depth=2)
# Each path is a list of edge dicts; a drug -> gene/protein -> disease path is a
# candidate new-indication hypothesis. For deeper traversal, load kg.csv into networkx.
```

## Node and Relation Types in PrimeKG

These are the exact strings used in `kg.csv` — match them verbatim when filtering.

**Node types** (`x_type`/`y_type`, 10 total): `gene/protein`, `drug`, `disease`,
`effect/phenotype`, `biological_process`, `molecular_function`, `cellular_component`,
`pathway`, `anatomy`, `exposure`. Note: genes use `gene/protein` (not `gene`) and
phenotypes use `effect/phenotype` (not `phenotype`).

**Key relations** (`relation`, 30 total). Edges are undirected; check both endpoints.
- `protein_protein`: physical PPIs
- `drug_protein`: drug target/mechanism associations
- `disease_protein`: disease-gene/protein associations (there is no `disease_gene`)
- `indication`, `contraindication`, `off-label use`: the three drug-disease relations
  (there is no single `drug_disease`)
- `disease_phenotype_positive` / `disease_phenotype_negative`: phenotype present/absent
- `bioprocess_protein`, `pathway_protein`, `molfunc_protein`, `cellcomp_protein`: GO /
  pathway annotations
- `anatomy_protein_present` / `anatomy_protein_absent`, `exposure_*`: anatomy/exposure links

## Best Practices

1. **Use specific IDs:** When using `get_neighbors`, ensure you have the correct ID from `search_nodes` (disease IDs are MONDO ids).
2. **Context first:** Use `get_disease_context` for a broad overview before diving into specific genes or drugs.
3. **Filter relationships:** Use the `relation_type` filter in `get_neighbors` to focus on specific evidence (e.g., only `drug_protein`, or `indication` for treatment links). Use exact relation strings from the list above.
4. **Mind disease grouping:** PrimeKG collapses ~22k MONDO concepts into ~17k grouped disease nodes, so one disease name may resolve to multiple MONDO ids that share a `node_index`.

## Resources

### Scripts
- `scripts/query_primekg.py`: Core functions — `search_nodes`, `get_neighbors`, `find_paths`, `get_disease_context`.

### Data Path
- Data: `kg.csv` (set `PRIMEKG_DATA_PATH`; default `../data/kg.csv`), from Harvard Dataverse (mims-harvard/PrimeKG).
- 129,375 nodes, 4,050,249 edges; 10 node types, 30 edge types.
- Loaded with pandas (`pd.read_csv`, `low_memory=True`). kg.csv is ~3 GB+ uncompressed — each function reloads it; for repeated queries, cache the DataFrame or use a real graph store.
