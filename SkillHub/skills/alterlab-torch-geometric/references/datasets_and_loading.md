# Working with Datasets

Loading built-in datasets, creating custom in-memory datasets, and loading graphs from CSV.
For the full dataset catalog, see `references/datasets_reference.md`.

## Loading Built-in Datasets

PyG provides extensive benchmark datasets:

```python
# Citation networks (node classification)
from torch_geometric.datasets import Planetoid
dataset = Planetoid(root='/tmp/Cora', name='Cora')  # or 'CiteSeer', 'PubMed'

# Graph classification
from torch_geometric.datasets import TUDataset
dataset = TUDataset(root='/tmp/ENZYMES', name='ENZYMES')

# Molecular datasets
from torch_geometric.datasets import QM9
dataset = QM9(root='/tmp/QM9')

# Large-scale datasets
from torch_geometric.datasets import Reddit
dataset = Reddit(root='/tmp/Reddit')
```

Check `references/datasets_reference.md` for a comprehensive list.

## Creating Custom Datasets

For datasets that fit in memory, inherit from `InMemoryDataset`:

```python
from torch_geometric.data import InMemoryDataset, Data
import torch

class MyOwnDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super().__init__(root, transform, pre_transform)
        self.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return ['my_data.csv']  # Files needed in raw_dir

    @property
    def processed_file_names(self):
        return ['data.pt']  # Files in processed_dir

    def download(self):
        # Download raw data to self.raw_dir
        pass

    def process(self):
        # Read data, create Data objects
        data_list = []

        # Example: Create a simple graph
        edge_index = torch.tensor([[0, 1], [1, 0]], dtype=torch.long)
        x = torch.randn(2, 16)
        y = torch.tensor([0], dtype=torch.long)

        data = Data(x=x, edge_index=edge_index, y=y)
        data_list.append(data)

        # Apply pre_filter and pre_transform
        if self.pre_filter is not None:
            data_list = [d for d in data_list if self.pre_filter(d)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(d) for d in data_list]

        # Save processed data
        self.save(data_list, self.processed_paths[0])
```

For large datasets that don't fit in memory, inherit from `Dataset` and implement `len()` and `get(idx)`.

## Loading Graphs from CSV

```python
import pandas as pd
import torch
from torch_geometric.data import HeteroData

# Load nodes
nodes_df = pd.read_csv('nodes.csv')
x = torch.tensor(nodes_df[['feat1', 'feat2']].values, dtype=torch.float)

# Load edges
edges_df = pd.read_csv('edges.csv')
edge_index = torch.tensor([edges_df['source'].values,
                           edges_df['target'].values], dtype=torch.long)

data = Data(x=x, edge_index=edge_index)
```
