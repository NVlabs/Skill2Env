---
name: alterlab-torch-geometric
description: Graph Neural Networks with PyTorch Geometric (PyG) — node and graph classification, link prediction, GCN, GAT, and GraphSAGE layers, heterogeneous graphs, and molecular property prediction. Use when building or training GNNs for geometric deep learning on graph-structured data. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: No API key required. Runs locally via `uv run python`; requires the torch and torch-geometric Python packages (GPU optional).
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# PyTorch Geometric (PyG)

## Overview

PyTorch Geometric is a library built on PyTorch for developing and training Graph Neural Networks (GNNs). Apply this skill for deep learning on graphs and irregular structures, including mini-batch processing, multi-GPU training, and geometric deep learning applications.

## When to Use This Skill

This skill should be used when working with:
- **Graph-based machine learning**: Node classification, graph classification, link prediction
- **Molecular property prediction**: Drug discovery, chemical property prediction
- **Social network analysis**: Community detection, influence prediction
- **Citation networks**: Paper classification, recommendation systems
- **3D geometric data**: Point clouds, meshes, molecular structures
- **Heterogeneous graphs**: Multi-type nodes and edges (e.g., knowledge graphs)
- **Large-scale graph learning**: Neighbor sampling, distributed training

## Quick Start

```bash
uv pip install torch_geometric
```

Graphs are `torch_geometric.data.Data` objects: `x` (node features `[N, F]`), `edge_index`
(connectivity in COO `[2, E]`), optional `edge_attr`, `y`, `pos`, and any custom attribute
(`train_mask`, etc.). `DataLoader` batches multiple graphs into one block-diagonal graph
(no padding); a `batch` vector maps nodes back to their source graph.

Full install/sparse-deps, basic graph creation, benchmark loading, edge-index format, and
mini-batching details: `references/getting_started.md`.

## Core Workflow

1. **Load or build data** — benchmark datasets, custom `InMemoryDataset`, or from CSV
   (`references/datasets_and_loading.md`; full catalog in `references/datasets_reference.md`).
2. **Define a GNN** — stack pre-built conv layers (GCNConv, GATConv, SAGEConv) or subclass
   `MessagePassing` for custom layers (`references/building_gnns.md`; full layer list in
   `references/layers_reference.md`).
3. **Train** — node classification (single graph, train/test masks), graph classification
   (`DataLoader` + global pooling), or large-scale via `NeighborLoader` neighbor sampling
   (`references/training_workflows.md`).
4. **Go advanced if needed** — `HeteroData`/`to_hetero` for heterogeneous graphs, transforms,
   `GNNExplainer` explainability, hierarchical pooling, GPU, save/load
   (`references/advanced_features.md`; transforms catalog in `references/transforms_reference.md`).

## Building GNNs (at a glance)

GNNs follow neighborhood aggregation: transform node features → propagate messages along edges →
aggregate from neighbors → update representations. PyG ships 40+ conv layers. When choosing one,
check its capabilities: SparseTensor support, `edge_weight`, `edge_attr`, bipartite, and lazy
(`-1` channel) initialization. Code for GCN/GAT/GraphSAGE and custom `MessagePassing` layers
(including the `_i`/`_j` target/source naming convention) is in `references/building_gnns.md`.

## Resources

### Bundled References

This skill includes detailed reference documentation:

- **`references/getting_started.md`**: Install, basic graph creation, `Data` structure, edge-index format, mini-batching
- **`references/building_gnns.md`**: Message passing, GCN/GAT/GraphSAGE code, custom `MessagePassing` layers, layer capabilities
- **`references/datasets_and_loading.md`**: Built-in datasets, custom `InMemoryDataset`, loading graphs from CSV
- **`references/training_workflows.md`**: Node classification, graph classification, large-scale neighbor sampling
- **`references/advanced_features.md`**: Heterogeneous graphs, transforms, explainability, pooling, GPU, save/load
- **`references/layers_reference.md`**: Complete listing of all 40+ GNN layers with descriptions and capabilities
- **`references/datasets_reference.md`**: Comprehensive dataset catalog organized by category
- **`references/transforms_reference.md`**: All available transforms and their use cases

### Scripts

Utility scripts are provided in `scripts/`:

- **`scripts/visualize_graph.py`**: Visualize graph structure using networkx and matplotlib
- **`scripts/create_gnn_template.py`**: Generate boilerplate code for common GNN architectures
- **`scripts/benchmark_model.py`**: Benchmark model performance on standard datasets

Execute scripts directly or read them for implementation patterns.

### Official Resources

- **Documentation**: https://pytorch-geometric.readthedocs.io/
- **GitHub**: https://github.com/pyg-team/pytorch_geometric
- **Tutorials**: https://pytorch-geometric.readthedocs.io/en/latest/get_started/introduction.html
- **Examples**: https://github.com/pyg-team/pytorch_geometric/tree/master/examples

