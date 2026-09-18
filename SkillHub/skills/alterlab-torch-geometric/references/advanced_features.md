# Advanced PyG Features

Heterogeneous graphs, transforms, explainability, and hierarchical pooling.
For the full transforms catalog, see `references/transforms_reference.md`.

## Heterogeneous Graphs

For graphs with multiple node and edge types, use `HeteroData`:

```python
from torch_geometric.data import HeteroData

data = HeteroData()

# Add node features for different types
data['paper'].x = torch.randn(100, 128)  # 100 papers with 128 features
data['author'].x = torch.randn(200, 64)  # 200 authors with 64 features

# Add edges for different types (source_type, edge_type, target_type)
data['author', 'writes', 'paper'].edge_index = torch.randint(0, 200, (2, 500))
data['paper', 'cites', 'paper'].edge_index = torch.randint(0, 100, (2, 300))

print(data)
```

Convert homogeneous models to heterogeneous:

```python
from torch_geometric.nn import to_hetero

# Define homogeneous model
model = GNN(...)

# Convert to heterogeneous
model = to_hetero(model, data.metadata(), aggr='sum')

# Use as normal
out = model(data.x_dict, data.edge_index_dict)
```

Or use `HeteroConv` for custom edge-type-specific operations:

```python
from torch_geometric.nn import HeteroConv, GCNConv, SAGEConv

class HeteroGNN(torch.nn.Module):
    def __init__(self, metadata):
        super().__init__()
        self.conv1 = HeteroConv({
            ('paper', 'cites', 'paper'): GCNConv(-1, 64),
            ('author', 'writes', 'paper'): SAGEConv((-1, -1), 64),
        }, aggr='sum')

        self.conv2 = HeteroConv({
            ('paper', 'cites', 'paper'): GCNConv(64, 32),
            ('author', 'writes', 'paper'): SAGEConv((64, 64), 32),
        }, aggr='sum')

    def forward(self, x_dict, edge_index_dict):
        x_dict = self.conv1(x_dict, edge_index_dict)
        x_dict = {key: F.relu(x) for key, x in x_dict.items()}
        x_dict = self.conv2(x_dict, edge_index_dict)
        return x_dict
```

## Transforms

Apply transforms to modify graph structure or features:

```python
from torch_geometric.transforms import NormalizeFeatures, AddSelfLoops, Compose

# Single transform
transform = NormalizeFeatures()
dataset = Planetoid(root='/tmp/Cora', name='Cora', transform=transform)

# Compose multiple transforms
transform = Compose([
    AddSelfLoops(),
    NormalizeFeatures(),
])
dataset = Planetoid(root='/tmp/Cora', name='Cora', transform=transform)
```

Common transforms:
- **Structure**: `ToUndirected`, `AddSelfLoops`, `RemoveSelfLoops`, `KNNGraph`, `RadiusGraph`
- **Features**: `NormalizeFeatures`, `NormalizeScale`, `Center`
- **Sampling**: `RandomNodeSplit`, `RandomLinkSplit`
- **Positional Encoding**: `AddLaplacianEigenvectorPE`, `AddRandomWalkPE`

See `references/transforms_reference.md` for the full list.

## Model Explainability

PyG provides explainability tools to understand model predictions:

```python
from torch_geometric.explain import Explainer, GNNExplainer

# Create explainer
explainer = Explainer(
    model=model,
    algorithm=GNNExplainer(epochs=200),
    explanation_type='model',  # or 'phenomenon'
    node_mask_type='attributes',
    edge_mask_type='object',
    model_config=dict(
        mode='multiclass_classification',
        task_level='node',
        return_type='log_probs',
    ),
)

# Generate explanation for a specific node
node_idx = 10
explanation = explainer(data.x, data.edge_index, index=node_idx)

# Visualize
print(f'Node {node_idx} explanation:')
print(f'Important edges: {explanation.edge_mask.topk(5).indices}')
print(f'Important features: {explanation.node_mask[node_idx].topk(5).indices}')
```

## Pooling Operations

For hierarchical graph representations:

```python
from torch_geometric.nn import TopKPooling, global_mean_pool

class HierarchicalGNN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 64)
        self.pool1 = TopKPooling(64, ratio=0.8)
        self.conv2 = GCNConv(64, 64)
        self.pool2 = TopKPooling(64, ratio=0.8)
        self.lin = torch.nn.Linear(64, num_classes)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        x = F.relu(self.conv1(x, edge_index))
        x, edge_index, _, batch, _, _ = self.pool1(x, edge_index, None, batch)

        x = F.relu(self.conv2(x, edge_index))
        x, edge_index, _, batch, _, _ = self.pool2(x, edge_index, None, batch)

        x = global_mean_pool(x, batch)
        x = self.lin(x)
        return F.log_softmax(x, dim=1)
```

## Common Patterns and Best Practices

### Check Graph Properties

```python
# Undirected check
from torch_geometric.utils import is_undirected
print(f"Is undirected: {is_undirected(data.edge_index)}")

# Contains self-loops
from torch_geometric.utils import contains_self_loops
print(f"Has self-loops: {contains_self_loops(data.edge_index)}")

# Connected components — PyG has no utils.connected_components; convert to
# networkx, or use the LargestConnectedComponents transform (see transforms ref).
import networkx as nx
from torch_geometric.utils import to_networkx
G = to_networkx(data, to_undirected=True)
print(f"Connected components: {nx.number_connected_components(G)}")
```

### GPU Training

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
data = data.to(device)

# For DataLoader
for batch in loader:
    batch = batch.to(device)
    # Train...
```

### Save and Load Models

```python
# Save
torch.save(model.state_dict(), 'model.pth')

# Load
model = GCN(num_features, num_classes)
model.load_state_dict(torch.load('model.pth'))
model.eval()
```
