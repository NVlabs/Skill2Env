# Multimodal and Multi-omics Integration Models

This document covers models for joint analysis of multiple data modalities in scvi-tools.

## totalVI (Total Variational Inference)

**Purpose**: Joint analysis of CITE-seq data (simultaneous RNA and protein measurements from same cells).

**Key Features**:
- Jointly models gene expression and protein abundance
- Learns shared low-dimensional representations
- Enables protein imputation from RNA data
- Performs differential expression for both modalities
- Handles batch effects in both RNA and protein layers

**When to Use**:
- Analyzing CITE-seq or REAP-seq data
- Joint RNA + surface protein measurements
- Imputing missing proteins
- Integrating protein and RNA information
- Multi-batch CITE-seq integration

**Data Requirements**:
- AnnData with gene expression in `.X` or a layer
- Protein measurements in `.obsm["protein_expression"]`
- Same cells measured for both modalities

**Basic Usage**:
```python
import scvi

# Setup data - specify both RNA and protein layers
scvi.model.TOTALVI.setup_anndata(
    adata,
    layer="counts",  # RNA counts
    protein_expression_obsm_key="protein_expression",  # Protein counts
    batch_key="batch"
)

# Train model
model = scvi.model.TOTALVI(adata)
model.train()

# Get joint latent representation
latent = model.get_latent_representation()

# get_normalized_expression returns a (rna, protein) TUPLE for totalVI
rna_normalized, protein_normalized = model.get_normalized_expression(n_samples=25)

# Differential expression returns ONE DataFrame covering both modalities:
# genes and proteins both appear as rows (split by name afterwards).
de = model.differential_expression(groupby="cell_type", group1="T cells", group2="B cells")
is_protein = de.index.isin(adata.uns["protein_names"])
rna_de, protein_de = de[~is_protein], de[is_protein]
```

**Key Parameters**:
- `n_latent`: Latent space dimensionality (default: 20)
- `n_layers_encoder`: Number of encoder layers (default: 1)
- `n_layers_decoder`: Number of decoder layers (default: 1)
- `protein_dispersion`: Protein dispersion handling ("protein" or "protein-batch")
- `empirical_protein_background_prior`: Use empirical background for proteins

**Advanced Features**:

**Protein Imputation / Denoising**:
```python
# Foreground (real signal) vs ambient background for proteins
protein_foreground = model.get_protein_foreground_probability(n_samples=25)

# Denoised values for both modalities come back as a (rna, protein) tuple
denoised_rna, denoised_protein = model.get_normalized_expression(n_samples=25)
```

**Best Practices**:
1. Use empirical protein background prior for datasets with ambient protein
2. Consider protein-specific dispersion for heterogeneous protein data
3. Use joint latent space for clustering (better than RNA alone)
4. Validate protein imputation with known markers
5. Check protein QC metrics before training

## MultiVI (Multi-modal Variational Inference)

**Purpose**: Integration of paired and unpaired multi-omic data (e.g., RNA + ATAC, paired and unpaired cells).

**Key Features**:
- Handles paired data (same cells) and unpaired data (different cells)
- Integrates multiple modalities: RNA, ATAC, proteins, etc.
- Missing modality imputation
- Learns shared representations across modalities
- Flexible integration strategy

**When to Use**:
- 10x Multiome data (paired RNA + ATAC)
- Integrating separate RNA-seq and ATAC-seq experiments
- Some cells with both modalities, some with only one
- Cross-modality imputation tasks

**Data Requirements**:
- A `MuData` object with one modality per `.mod` entry (e.g. `mdata.mod["rna"]`,
  `mdata.mod["atac"]`, optionally `mdata.mod["protein"]`).
- Handles fully paired (10x Multiome), partially paired, and fully unpaired
  cells. For unpaired/mixed data, concatenate paired cells first, then RNA-only,
  then ATAC-only cells — MultiVI infers which modalities each cell has from the
  per-modality observations.

**Basic Usage** (current MuData API):
```python
import scvi
from mudata import MuData

# mdata.mod["rna"] = RNA AnnData (raw counts), mdata.mod["atac"] = ATAC AnnData
scvi.model.MULTIVI.setup_mudata(
    mdata,
    batch_key="batch",
    modalities={"rna_layer": "rna", "atac_layer": "atac"},
)

model = scvi.model.MULTIVI(
    mdata,
    n_genes=mdata.mod["rna"].n_vars,
    n_regions=mdata.mod["atac"].n_vars,
)
model.train()

# Joint latent representation
latent = model.get_latent_representation()

# Modality-specific outputs (and cross-modality imputation: predict the
# missing modality for cells that only measured the other one)
rna_normalized = model.get_normalized_expression()
atac_normalized = model.get_accessibility_estimates()
```

> Older code uses a single concatenated AnnData built with
> `scvi.data.organize_multiome_anndatas(...)` plus `MULTIVI.setup_anndata`.
> New work should prefer the `MuData` + `setup_mudata` path shown above.

**Key Parameters**:
- `n_genes`: Number of gene features (`mdata.mod["rna"].n_vars`)
- `n_regions`: Number of accessibility regions (`mdata.mod["atac"].n_vars`)
- `n_latent`: Latent dimensionality (default: 20)

## MrVI (Multi-resolution Variational Inference)

**Purpose**: Multi-sample analysis accounting for sample-specific and shared variation.

**Key Features**:
- Simultaneously analyzes multiple samples/conditions
- Decomposes variation into:
  - Shared variation (common across samples)
  - Sample-specific variation
- Enables sample-level comparisons
- Identifies sample-specific cell states

**When to Use**:
- Comparing multiple biological samples or conditions
- Identifying sample-specific vs. shared cell states
- Disease vs. healthy sample comparisons
- Understanding inter-sample heterogeneity
- Multi-donor studies

**Basic Usage** (note: MrVI lives in `scvi.external`, not `scvi.model`):
```python
from scvi.external import MRVI

MRVI.setup_anndata(
    adata,
    layer="counts",
    batch_key="batch",
    sample_key="sample",  # Critical: defines biological samples
)

model = MRVI(adata, n_latent=10, n_latent_sample=5)
model.train()

# u = sample-invariant latent; z = sample-aware ("local") latent
u_latent = model.get_latent_representation(give_z=False)  # sample-corrected
z_latent = model.get_latent_representation(give_z=True)   # sample-aware

# Per-cell, per-sample representation and pairwise sample distances
local_repr = model.get_local_sample_representation()
sample_distances = model.get_local_sample_distances()
```

**Key Parameters**:
- `n_latent`: Dimensionality of the (shared) `z` latent space
- `n_latent_sample`: Dimensionality of the sample-specific latent space
- `sample_key`: Column defining biological samples

**Analysis Workflow**:
```python
# 1. Cluster on the sample-invariant u space
adata.obsm["X_mrvi_u"] = model.get_latent_representation(give_z=False)
sc.pp.neighbors(adata, use_rep="X_mrvi_u")
sc.tl.umap(adata)
sc.tl.leiden(adata, key_added="shared_clusters")

# 2. Per-cell sample distance matrices (how samples differ at each cell state)
distances = model.get_local_sample_distances()

# 3. MrVI's differential analyses are driven by SAMPLE-LEVEL covariates
#    (e.g. condition/donor), not a cell-level group1/group2 comparison like
#    scVI. Use model.differential_abundance(...) and
#    model.differential_expression(...) with the sample covariate(s) of
#    interest — check the current API for the exact keyword.
```

**Use Cases**:
- **Multi-donor studies**: Separate donor effects from cell type variation
- **Disease studies**: Identify disease-specific vs. shared biology
- **Time series**: Separate temporal from stable variation
- **Batch + biology**: Disentangle technical and biological variation

## totalVI vs. MultiVI vs. MrVI: When to Use Which?

### totalVI
**Use for**: CITE-seq (RNA + protein, same cells)
- Paired measurements
- Single modality type per feature
- Focus: protein imputation, joint analysis

### MultiVI
**Use for**: Multiple modalities (RNA + ATAC, etc.)
- Paired, unpaired, or mixed
- Different feature types
- Focus: cross-modality integration and imputation

### MrVI
**Use for**: Multi-sample RNA-seq
- Single modality (RNA)
- Multiple biological samples
- Focus: sample-level variation decomposition

## Integration Best Practices

### For CITE-seq (totalVI)
1. **Quality control proteins**: Remove low-quality antibodies
2. **Background subtraction**: Use empirical background prior
3. **Joint clustering**: Use joint latent space, not RNA alone
4. **Validation**: Check known markers in both modalities

### For Multiome/Multi-modal (MultiVI)
1. **Feature filtering**: Filter genes and peaks independently
2. **Balance modalities**: Ensure reasonable representation of each
3. **Modality weights**: Consider if one modality dominates
4. **Imputation validation**: Validate imputed values carefully

### For Multi-sample (MrVI)
1. **Sample definition**: Carefully define biological samples
2. **Sample size**: Need sufficient cells per sample
3. **Covariate handling**: Properly account for batch vs. sample
4. **Interpretation**: Distinguish technical from biological variation

## Complete Example: CITE-seq Analysis with totalVI

```python
import scvi
import scanpy as sc

# 1. Load CITE-seq data
adata = sc.read_h5ad("cite_seq.h5ad")

# 2. QC and filtering
sc.pp.filter_genes(adata, min_cells=3)
sc.pp.highly_variable_genes(adata, n_top_genes=4000)

# Protein QC
protein_counts = adata.obsm["protein_expression"]
# Remove low-quality proteins

# 3. Setup totalVI
# protein_names_uns_key registers the protein names so DE rows are labelled
# (and adata.uns["protein_names"] is available to split RNA vs protein results).
scvi.model.TOTALVI.setup_anndata(
    adata,
    layer="counts",
    protein_expression_obsm_key="protein_expression",
    protein_names_uns_key="protein_names",
    batch_key="batch"
)

# 4. Train
model = scvi.model.TOTALVI(adata, n_latent=20)
model.train(max_epochs=400)

# 5. Extract joint representation
latent = model.get_latent_representation()
adata.obsm["X_totalVI"] = latent

# 6. Clustering on joint space
sc.pp.neighbors(adata, use_rep="X_totalVI")
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5)

# 7. Differential expression — one DataFrame covers genes AND proteins
de = model.differential_expression(groupby="leiden", group1="0", group2="1")
is_protein = de.index.isin(adata.uns["protein_names"])
rna_de, protein_de = de[~is_protein], de[is_protein]

# 8. Save model
model.save("totalvi_model")
```
