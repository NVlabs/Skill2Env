# Building Graph Neural Networks

Message-passing paradigm, pre-built layers (GCN, GAT, GraphSAGE), and custom `MessagePassing` layers.
For the full layer catalog, see `references/layers_reference.md`.

## Message Passing Paradigm

GNNs in PyG follow a neighborhood aggregation scheme:
1. Transform node features
2. Propagate messages along edges
3. Aggregate messages from neighbors
4. Update node representations

## Using Pre-Built Layers

PyG provides 40+ convolutional layers. Common ones:

**GCNConv** (Graph Convolutional Network):
```python
from torch_geometric.nn import GCNConv
import torch.nn.functional as F

class GCN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 16)
        self.conv2 = GCNConv(16, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

**GATConv** (Graph Attention Network):
```python
from torch_geometric.nn import GATConv

class GAT(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GATConv(num_features, 8, heads=8, dropout=0.6)
        self.conv2 = GATConv(8 * 8, num_classes, heads=1, concat=False, dropout=0.6)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.dropout(x, p=0.6, training=self.training)
        x = F.elu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

**GraphSAGE**:
```python
from torch_geometric.nn import SAGEConv

class GraphSAGE(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = SAGEConv(num_features, 64)
        self.conv2 = SAGEConv(64, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)
```

## Custom Message Passing Layers

For custom layers, inherit from `MessagePassing`:

```python
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

class CustomConv(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super().__init__(aggr='add')  # "add", "mean", or "max"
        self.lin = torch.nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_index):
        # Add self-loops to adjacency matrix
        edge_index, _ = add_self_loops(edge_index, num_nodes=x.size(0))

        # Transform node features
        x = self.lin(x)

        # Compute normalization
        row, col = edge_index
        deg = degree(col, x.size(0), dtype=x.dtype)
        deg_inv_sqrt = deg.pow(-0.5)
        norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]

        # Propagate messages
        return self.propagate(edge_index, x=x, norm=norm)

    def message(self, x_j, norm):
        # x_j: features of source nodes
        return norm.view(-1, 1) * x_j
```

Key methods:
- **`forward()`**: Main entry point
- **`message()`**: Constructs messages from source to target nodes
- **`aggregate()`**: Aggregates messages (usually don't override—set `aggr` parameter)
- **`update()`**: Updates node embeddings after aggregation

**Variable naming convention**: Appending `_i` or `_j` to tensor names automatically maps them to target or source nodes.

## Layer Capabilities

When choosing layers, consider these capabilities:
- **SparseTensor**: Supports efficient sparse matrix operations
- **edge_weight**: Handles one-dimensional edge weights
- **edge_attr**: Processes multi-dimensional edge features
- **Bipartite**: Works with bipartite graphs (different source/target dimensions)
- **Lazy**: Enables initialization without specifying input dimensions

See the GNN cheatsheet at `references/layers_reference.md`.
