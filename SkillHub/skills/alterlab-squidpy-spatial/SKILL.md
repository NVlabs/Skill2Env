---
name: alterlab-squidpy-spatial
description: "Analyzes spatial transcriptomics with squidpy (1.8.x) on AnnData and SpatialData objects, routing platforms correctly: Visium spots use spatial_neighbors(coord_type='grid') and pair with deconvolution, while Xenium/MERFISH single-cell data use coord_type='generic'/Delaunay neighbors and spatialdata-io readers (xenium, visium_hd, merscope). Runs sq.gr.spatial_neighbors, nhood_enrichment, co_occurrence, spatial_autocorr (Moran's I for spatially variable genes), ripley, and ligrec. Use when the user wants spatial transcriptomics, squidpy, Visium/Xenium/MERFISH analysis, neighborhood enrichment, co-occurrence, or spatially variable genes; QC/clustering uses alterlab-scanpy and spot deconvolution (destVI/Tangram) uses alterlab-scvi-tools. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with squidpy (1.8.x, needs spatialdata>=0.7.1, scanpy>=1.9.3, anndata>=0.9, Python>=3.11) installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Squidpy: Spatial Transcriptomics

Squidpy is the scverse toolkit for spatially-resolved omics, built on AnnData and
SpatialData. It answers questions a non-spatial scRNA-seq pipeline cannot: *which
cell types sit next to which* (neighborhood enrichment), *how cell-type pairs
co-occur across distance* (co-occurrence), *which genes vary across tissue space*
(Moran's I / spatially variable genes), and *what ligand-receptor signalling is
plausible* (ligrec). This skill does the spatial analysis; it hands non-spatial
QC/clustering to `alterlab-scanpy` and spot deconvolution to `alterlab-scvi-tools`.

## When to Use This Skill

Use when the request involves:
- Spatial transcriptomics / spatially-resolved omics on **Visium, Visium HD, Xenium,
  MERFISH/MERSCOPE, or CosMx** data.
- Building a **spatial neighbor graph** and running **neighborhood enrichment**,
  **co-occurrence**, **interaction matrix**, **Ripley's statistics**, or
  **centrality scores**.
- Finding **spatially variable genes** via Moran's I (`spatial_autocorr`) or Sepal.
- **Ligand-receptor** analysis in a spatial context (`ligrec`).
- Reading platform output into AnnData/SpatialData and choosing the right
  `coord_type` for the platform.

### Does NOT Trigger

| Request | Route to |
|---------|----------|
| Non-spatial scRNA-seq QC, normalization, PCA/UMAP, Leiden clustering, marker genes | `alterlab-scanpy` |
| Spot **deconvolution** / mapping cell types to Visium spots (destVI, Tangram), probabilistic batch correction/integration | `alterlab-scvi-tools` (see its `references/models-spatial.md`) |
| Building/slicing/concatenating `.h5ad` AnnData objects, layer & obsm wrangling (no spatial analysis) | `alterlab-anndata` |
| RNA-velocity / trajectory dynamics | `alterlab-scvelo` |
| Bulk RNA-seq **differential expression** from a count matrix | `alterlab-pydeseq2` |
| Raw FASTQ → expression matrix (read alignment/quantification) | `alterlab-rnaseq-quant` |
| Diversity / ecology statistics on a feature table | `alterlab-scikit-bio` |

If the user wants the *whole* pipeline ("cluster my Xenium data, then find which
cell types are neighbors"), run the scanpy clustering step under `alterlab-scanpy`
first, then return here for the spatial graph and enrichment.

## The One Decision That Matters: Platform → coord_type

Squidpy's spatial graph depends on the measurement geometry. Getting `coord_type`
wrong silently produces a meaningless graph. (All parameter behavior below is from
the squidpy 1.8 `sq.gr.spatial_neighbors` API.)

| Platform | Resolution | Builder | Pair with |
|----------|-----------|---------|-----------|
| **Visium** | spot (multi-cell, hex grid) | `coord_type="grid"`, `n_neighs=6`, `n_rings=1..2` | deconvolution → `alterlab-scvi-tools` |
| **Visium HD** | 2/8/16 µm bins (square grid) | `coord_type="grid"` (square lattice) | binning choice up front |
| **Xenium / MERFISH / CosMx** | single cell | `coord_type="generic"`, `delaunay=True` (or `n_neighs=k`) | direct cell-type analysis |

- `coord_type=None` auto-picks `"grid"` only when `spatial` is in `adata.uns` with
  `n_neighs=6` (the Visium signature); otherwise it falls back to `"generic"`. **Set
  `coord_type` explicitly** rather than relying on auto-detection.
- `delaunay=True` is only used when `coord_type="generic"`; it builds the graph from
  a Delaunay triangulation instead of k-nearest spots. `n_rings` is only used for
  `coord_type="grid"`.

## Loading Data (pick the reader for the platform)

```python
import squidpy as sq
import scanpy as sc

# Visium (legacy spot data) — squidpy's own reader, returns AnnData
adata = sq.read.visium("path/to/visium_outs/")

# Vizgen MERSCOPE / Nanostring CosMx via squidpy readers
adata = sq.read.vizgen("path/to/merscope/", counts_file="cell_by_gene.csv",
                       meta_file="cell_metadata.csv")
adata = sq.read.nanostring("path/to/cosmx/", counts_file="exprMat_file.csv",
                           meta_file="metadata_file.csv", fov_file="fov_positions.csv")
```

For **Xenium and Visium HD**, use the **`spatialdata-io`** readers (squidpy has no
`sq.read.xenium`) and operate on a `SpatialData` object:

```python
from spatialdata_io import xenium, visium_hd, merscope
sdata = xenium("path/to/xenium_outs/")        # 10x Xenium
sdata = visium_hd("path/to/visium_hd_outs/")  # 10x Visium HD
sdata = merscope("path/to/merscope/")         # Vizgen MERSCOPE
```

`spatialdata-io` reader names are verified against the spatialdata-io stable API.
Squidpy 1.8 accepts SpatialData objects directly; see
`references/spatialdata_io.md` for the SpatialData ↔ AnnData (table) flow.

## Standard Spatial Workflow

QC, normalization, HVGs, PCA, neighbors, Leiden, and `sc.tl.umap` are **scanpy**
steps — run them via `alterlab-scanpy`. Once you have clusters / cell-type labels,
do the spatial part here.

```python
import squidpy as sq

# 1. Build the spatial neighbor graph (choose coord_type per the table above)
sq.gr.spatial_neighbors(adata, coord_type="generic", delaunay=True)   # Xenium/MERFISH
# sq.gr.spatial_neighbors(adata, coord_type="grid", n_neighs=6)       # Visium

# 2. Neighborhood enrichment: which cluster pairs are spatially adjacent?
sq.gr.nhood_enrichment(adata, cluster_key="leiden")
sq.pl.nhood_enrichment(adata, cluster_key="leiden")

# 3. Co-occurrence across distance
sq.gr.co_occurrence(adata, cluster_key="leiden")
sq.pl.co_occurrence(adata, cluster_key="leiden", clusters="0")

# 4. Spatially variable genes via Moran's I
sq.gr.spatial_autocorr(adata, mode="moran")
svgs = adata.uns["moranI"].head(20)   # ranked by Moran's I

# 5. Ligand-receptor interaction (Omnipath-backed)
sq.gr.ligrec(adata, cluster_key="leiden")
```

Other graph statistics: `sq.gr.interaction_matrix`, `sq.gr.centrality_scores`,
`sq.gr.ripley` (clustering/dispersion vs. CSR), and `sq.gr.sepal` (an alternative
spatially-variable-gene test). Visualize tissue with `sq.pl.spatial_scatter`
(spot/point) or `sq.pl.spatial_segment` (segmented cells). For image features on
H&E/IF, the `sq.im` module (`process`, `segment`, `calculate_image_features`)
operates on an `ImageContainer`.

**Helper script** — build the graph and run the core statistics in one call:

```bash
uv run python skills/bioinformatics/alterlab-squidpy-spatial/scripts/spatial_neighborhood.py \
    clustered.h5ad --platform xenium --cluster-key leiden --out spatial_report.json
```

See `scripts/spatial_neighborhood.py --help`. It chooses `coord_type` from
`--platform`, runs `spatial_neighbors`, `nhood_enrichment`, `co_occurrence`, and
`spatial_autocorr`, and writes a JSON summary (top spatially variable genes + the
enrichment z-score matrix) plus the updated `.h5ad`.

## Deeper References

- `references/platform_routing.md` — full platform→`coord_type` decision table, the
  `n_neighs`/`n_rings`/`delaunay` parameter semantics, and per-platform gotchas.
- `references/analysis_recipes.md` — copy-paste recipes for each `sq.gr` / `sq.pl`
  function with the parameters that matter and how to read the outputs.
- `references/spatialdata_io.md` — reading Xenium / Visium HD / MERSCOPE into
  SpatialData and getting the AnnData `table` squidpy operates on.

## Self-Check Before Reporting

- Did you set `coord_type` to match the platform (grid for Visium, generic for
  single-cell)? A wrong graph invalidates every downstream statistic.
- Did clustering/QC run under `alterlab-scanpy` (this skill assumes labels exist)?
- For Visium spot data, did you flag that **deconvolution** (`alterlab-scvi-tools`)
  is needed before cell-type-level claims — spots are multi-cell?
- Are `nhood_enrichment` z-scores reported with the permutation context, not as raw
  counts?

Part of the AlterLab Academic Skills suite.
