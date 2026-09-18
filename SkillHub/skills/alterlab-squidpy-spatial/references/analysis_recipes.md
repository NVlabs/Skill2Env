# Squidpy Analysis Recipes

Copy-paste recipes for the core `sq.gr` graph statistics and their `sq.pl`
visualizations, with the parameters that matter and how to read each output. These
assume an AnnData (or SpatialData `table`) with cluster/cell-type labels in
`adata.obs[cluster_key]` and a spatial graph already built (see
`platform_routing.md`). Function names are verified against the squidpy 1.8 API.

## 1. Spatial neighbor graph (prerequisite)

```python
import squidpy as sq

# Single-cell (Xenium / MERFISH / CosMx)
sq.gr.spatial_neighbors(adata, coord_type="generic", delaunay=True)

# Visium spots
sq.gr.spatial_neighbors(adata, coord_type="grid", n_neighs=6, n_rings=1)
```

Writes `adata.obsp["spatial_connectivities"]` and `adata.obsp["spatial_distances"]`,
plus `adata.uns["spatial_neighbors"]`.

## 2. Neighborhood enrichment

```python
sq.gr.nhood_enrichment(adata, cluster_key="leiden")
sq.pl.nhood_enrichment(adata, cluster_key="leiden")
z = adata.uns["leiden_nhood_enrichment"]["zscore"]   # cluster x cluster z-scores
```

Permutation z-score per cluster pair: positive = adjacent more than chance
(attraction), negative = avoidance. Report with the permutation context.

## 3. Co-occurrence across distance

```python
sq.gr.co_occurrence(adata, cluster_key="leiden")
sq.pl.co_occurrence(adata, cluster_key="leiden", clusters="0")
```

Computes the co-occurrence probability ratio of cluster pairs as a function of
radial distance. Use it when you care about *how adjacency decays with distance*,
not just binary neighbor counts. Stored in `adata.uns["leiden_co_occurrence"]`.

## 4. Spatially variable genes — Moran's I

```python
sq.gr.spatial_autocorr(adata, mode="moran")
top = adata.uns["moranI"].sort_values("I", ascending=False).head(20)
```

`mode="moran"` writes the `adata.uns["moranI"]` table (Moran's I, p-value, FDR per
gene); `mode="geary"` writes `gearyC`. High positive Moran's I = strong spatial
autocorrelation = a spatially variable gene. Restrict to highly variable genes
first to cut runtime.

### Alternative: Sepal

```python
sq.gr.sepal(adata, max_neighs=6)   # max_neighs=6 hex (Visium) / 4 square grid
```

`sq.gr.sepal` identifies spatially variable genes via a diffusion-based score; it is
an alternative to Moran's I, useful as a cross-check.

## 5. Ligand-receptor analysis

```python
sq.gr.ligrec(adata, cluster_key="leiden")
sq.pl.ligrec(adata, cluster_key="leiden")
```

Tests ligand-receptor co-expression between cluster pairs using an Omnipath-backed
interaction database (a permutation test in the spirit of CellPhoneDB). Returns
means and p-values per L-R pair per cluster pair.

## 6. Other graph statistics

```python
sq.gr.interaction_matrix(adata, cluster_key="leiden")   # raw inter-cluster edge counts
sq.gr.centrality_scores(adata, cluster_key="leiden")    # degree / closeness / clustering per cluster
sq.gr.ripley(adata, cluster_key="leiden", mode="L")     # Ripley's L vs. complete spatial randomness
```

`ripley` (modes `"F"`, `"G"`, `"L"`) tests whether a cluster is more clustered or
dispersed than complete spatial randomness. `centrality_scores` summarizes each
cluster's position in the spatial graph.

## 7. Visualizing tissue

```python
sq.pl.spatial_scatter(adata, color="leiden")    # spot/point overlay (Visium, points)
sq.pl.spatial_segment(adata, color="leiden", seg_cell_id="cell_id")  # segmented cells (Xenium)
```

## 8. Image features (optional, H&E / IF)

```python
from squidpy.im import ImageContainer
img = ImageContainer("tissue_image.tif")
sq.im.process(img, layer="image", method="smooth")
sq.im.segment(img, layer="image", method="watershed")
sq.im.calculate_image_features(adata, img, features="summary")
```

The `sq.im` module operates on an `ImageContainer` and writes per-observation image
features back into `adata.obs` for joint expression+morphology analysis. Skip this
entirely for pure transcriptomic neighborhood work.
