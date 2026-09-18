# Training Workflows

Complete training loops for node classification, graph classification, and large-scale
neighbor sampling.

## Node Classification (Single Graph)

```python
import torch
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid

# Load dataset
dataset = Planetoid(root='/tmp/Cora', name='Cora')
data = dataset[0]

# Create model
model = GCN(dataset.num_features, dataset.num_classes)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# Training
model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')

# Evaluation
model.eval()
pred = model(data).argmax(dim=1)
correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
acc = int(correct) / int(data.test_mask.sum())
print(f'Test Accuracy: {acc:.4f}')
```

## Graph Classification (Multiple Graphs)

```python
from torch_geometric.datasets import TUDataset
from torch_geometric.loader import DataLoader
from torch_geometric.nn import global_mean_pool

class GraphClassifier(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GCNConv(num_features, 64)
        self.conv2 = GCNConv(64, 64)
        self.lin = torch.nn.Linear(64, num_classes)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch

        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)

        # Global pooling (aggregate node features to graph-level)
        x = global_mean_pool(x, batch)

        x = self.lin(x)
        return F.log_softmax(x, dim=1)

# Load dataset
dataset = TUDataset(root='/tmp/ENZYMES', name='ENZYMES')
loader = DataLoader(dataset, batch_size=32, shuffle=True)

model = GraphClassifier(dataset.num_features, dataset.num_classes)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training
model.train()
for epoch in range(100):
    total_loss = 0
    for batch in loader:
        optimizer.zero_grad()
        out = model(batch)
        loss = F.nll_loss(out, batch.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {total_loss / len(loader):.4f}')
```

## Large-Scale Graphs with Neighbor Sampling

For large graphs, use `NeighborLoader` to sample subgraphs:

```python
from torch_geometric.loader import NeighborLoader

# Create a neighbor sampler
train_loader = NeighborLoader(
    data,
    num_neighbors=[25, 10],  # Sample 25 neighbors for 1st hop, 10 for 2nd hop
    batch_size=128,
    input_nodes=data.train_mask,
)

# Training
model.train()
for batch in train_loader:
    optimizer.zero_grad()
    out = model(batch)
    # Only compute loss on seed nodes (first batch_size nodes)
    loss = F.nll_loss(out[:batch.batch_size], batch.y[:batch.batch_size])
    loss.backward()
    optimizer.step()
```

**Important**:
- Output subgraphs are directed
- Node indices are relabeled (0 to batch.num_nodes - 1)
- Only use seed node predictions for loss computation
- Sampling beyond 2-3 hops is generally not feasible
