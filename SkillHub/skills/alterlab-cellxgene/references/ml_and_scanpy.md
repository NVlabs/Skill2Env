# Machine Learning, Scanpy, and Multi-Dataset Integration

Code patterns for training PyTorch models on Census data, integrating with scanpy, and combining multiple datasets/tissues.

## Machine Learning with PyTorch

The PyTorch integration now lives in the standalone **`tiledbsoma_ml`** package
(`pip install tiledbsoma-ml`), NOT in `cellxgene_census.experimental.ml` — that
prototype API has been superseded. Build an `ExperimentDataset` from an
`axis_query`, then wrap it with `experiment_dataloader`:

```python
import torch
import tiledbsoma as soma
from tiledbsoma_ml import ExperimentDataset, experiment_dataloader

with cellxgene_census.open_soma(census_version="2023-07-25") as census:
    experiment = census["census_data"]["homo_sapiens"]
    with experiment.axis_query(
        measurement_name="RNA",
        obs_query=soma.AxisQuery(
            value_filter="tissue_general == 'liver' and is_primary_data == True"
        ),
    ) as query:
        dataset = ExperimentDataset(
            query,
            layer_name="raw",
            obs_column_names=["cell_type"],
            batch_size=128,
            shuffle=True,
            seed=42,
        )
        dataloader = experiment_dataloader(dataset)

        # Each batch is a (X, obs) tuple: X is a NumPy array, obs a pandas DataFrame.
        for epoch in range(num_epochs):
            for X_batch, obs_batch in dataloader:
                X = torch.from_numpy(X_batch).float()
                labels = label_encoder.transform(obs_batch["cell_type"])

                outputs = model(X)
                loss = criterion(outputs, torch.from_numpy(labels))

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
```

**Train/test splitting** — call `random_split` on the dataset (positional
fractions, not `split=[...]`), then wrap each split:
```python
train_dataset, test_dataset = dataset.random_split(0.8, 0.2, seed=42)
train_loader = experiment_dataloader(train_dataset)
test_loader = experiment_dataloader(test_dataset)
```

## Integration with Scanpy

Seamlessly integrate Census data with scanpy workflows:

```python
import scanpy as sc

# Load data from Census
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="cell_type == 'neuron' and tissue_general == 'cortex' and is_primary_data == True",
)

# Standard scanpy workflow
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

# Dimensionality reduction
sc.pp.pca(adata, n_comps=50)
sc.pp.neighbors(adata)
sc.tl.umap(adata)

# Visualization
sc.pl.umap(adata, color=["cell_type", "tissue", "disease"])
```

## Multi-Dataset Integration

Prefer a single query with an `in` filter (Strategy 2) — it pulls a consistent
gene set in one pass. Only query separately and concatenate when you need to tag
or transform each slice differently:

```python
import anndata as ad

# Strategy 1: Query multiple tissues separately, then concatenate
tissues = ["lung", "liver", "kidney"]
adatas = []
for tissue in tissues:
    a = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter=f"tissue_general == '{tissue}' and is_primary_data == True",
    )
    adatas.append(a)

# Use anndata.concat (adata.concatenate() is deprecated). Inner join keeps
# only genes shared across all slices.
combined = ad.concat(adatas, join="inner", label="tissue", keys=tissues)

# Strategy 2 (preferred): one query, multiple tissues
adata = cellxgene_census.get_anndata(
    census=census,
    organism="Homo sapiens",
    obs_value_filter="tissue_general in ['lung', 'liver', 'kidney'] and is_primary_data == True",
)
```

## Worked Use Cases

### Use Case 1: Explore Cell Types in a Tissue
```python
with cellxgene_census.open_soma() as census:
    cells = cellxgene_census.get_obs(
        census, "homo_sapiens",
        value_filter="tissue_general == 'lung' and is_primary_data == True",
        column_names=["cell_type"]
    )
    print(cells["cell_type"].value_counts())
```

### Use Case 2: Query Marker Gene Expression
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        var_value_filter="feature_name in ['CD4', 'CD8A', 'CD19']",
        obs_value_filter="cell_type in ['T cell', 'B cell'] and is_primary_data == True",
    )
```

### Use Case 3: Train Cell Type Classifier
```python
import tiledbsoma as soma
from tiledbsoma_ml import ExperimentDataset, experiment_dataloader

with cellxgene_census.open_soma(census_version="2023-07-25") as census:
    experiment = census["census_data"]["homo_sapiens"]
    with experiment.axis_query(
        measurement_name="RNA",
        obs_query=soma.AxisQuery(
            value_filter="tissue_general == 'blood' and is_primary_data == True"
        ),
    ) as query:
        dataset = ExperimentDataset(
            query, layer_name="raw", obs_column_names=["cell_type"],
            batch_size=128, shuffle=True, seed=42,
        )
        dataloader = experiment_dataloader(dataset)
        for X_batch, obs_batch in dataloader:
            ...  # Training logic
```

### Use Case 4: Cross-Tissue Analysis
```python
with cellxgene_census.open_soma() as census:
    adata = cellxgene_census.get_anndata(
        census=census,
        organism="Homo sapiens",
        obs_value_filter="cell_type == 'macrophage' and tissue_general in ['lung', 'liver', 'brain'] and is_primary_data == True",
    )

    # Analyze macrophage differences across tissues
    sc.tl.rank_genes_groups(adata, groupby="tissue_general")
```
