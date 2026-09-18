# Reading Modern Platforms with spatialdata-io

Squidpy 1.8 requires `spatialdata>=0.7.1` and accepts `SpatialData` objects, which
is the recommended representation for single-cell-resolution platforms (Xenium,
Visium HD) that carry images, shapes, and points alongside the expression table.
Squidpy's own `sq.read` module covers `visium`, `vizgen`, and `nanostring` only —
**there is no `sq.read.xenium`** — so Xenium and Visium HD come in through
`spatialdata-io`. Reader names below are verified against the spatialdata-io stable
API.

## Readers

```python
from spatialdata_io import xenium, visium, visium_hd, merscope

sdata = xenium("path/to/xenium_outs/")        # 10x Genomics Xenium
sdata = visium("path/to/visium_outs/")        # 10x Genomics Visium (spatialdata form)
sdata = visium_hd("path/to/visium_hd_outs/")  # 10x Genomics Visium HD
sdata = merscope("path/to/merscope/")         # Vizgen MERSCOPE
```

Each returns a `SpatialData` object — a container of elements: `images`, `labels`
(segmentation masks), `shapes` (cell/nucleus boundaries), `points` (transcript
locations), and `tables` (the AnnData expression table(s)).

## Getting the AnnData table squidpy operates on

Squidpy graph functions run on the expression `table` (an AnnData) inside the
`SpatialData` object. Access it via the `tables` mapping:

```python
adata = sdata.tables["table"]            # the AnnData squidpy analyses use
# ... run scanpy QC/clustering (alterlab-scanpy) to populate adata.obs["leiden"] ...
import squidpy as sq
sq.gr.spatial_neighbors(adata, coord_type="generic", delaunay=True)  # Xenium = single cell
sq.gr.nhood_enrichment(adata, cluster_key="leiden")
```

The exact key under `tables` depends on the reader/dataset; inspect `sdata.tables`
(a dict-like mapping) to find it. Spatial coordinates live in `adata.obsm["spatial"]`,
which `spatial_neighbors` reads by default (`spatial_key="spatial"`).

## When to stay in AnnData vs. SpatialData

- **Visium (legacy spot data):** `sq.read.visium(...)` returns a plain AnnData that
  already has `adata.uns["spatial"]` and `adata.obsm["spatial"]`; you can skip
  SpatialData entirely. Use `coord_type="grid"`.
- **Xenium / Visium HD / large MERSCOPE:** prefer `spatialdata-io` + `SpatialData`
  so images, segmentation shapes, and transcript points stay aligned; extract the
  `table` for squidpy graph statistics. Use `coord_type="generic"` (Xenium/MERSCOPE)
  or `"grid"` (Visium HD bins) per `platform_routing.md`.

## Hand-offs

- Non-spatial QC, normalization, PCA/UMAP, Leiden clustering, marker genes on the
  extracted `table` → `alterlab-scanpy`.
- Spot deconvolution for Visium (destVI / Tangram) → `alterlab-scvi-tools`
  (`references/models-spatial.md`).
- Pure `.h5ad` AnnData construction/slicing with no spatial analysis →
  `alterlab-anndata`.
