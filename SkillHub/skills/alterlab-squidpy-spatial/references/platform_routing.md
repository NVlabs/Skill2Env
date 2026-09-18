# Platform → coord_type Routing

The single most consequential choice in a squidpy analysis is how the spatial
neighbor graph is built, because every downstream statistic (`nhood_enrichment`,
`co_occurrence`, `spatial_autocorr`, `ripley`, `interaction_matrix`,
`centrality_scores`) consumes that graph. The right builder depends on the
measurement geometry of the platform. All parameter semantics below are from the
squidpy 1.8 `sq.gr.spatial_neighbors` API.

## Decision table

| Platform | Spatial unit | Geometry | `coord_type` | Key args | Notes |
|----------|--------------|----------|--------------|----------|-------|
| Visium | spot (10–100s of cells) | hexagonal grid | `"grid"` | `n_neighs=6`, `n_rings=1` (or `2`) | 6 immediate neighbors per spot; raise `n_rings` for wider neighborhoods |
| Visium HD | 2/8/16 µm bin | square grid | `"grid"` | `n_neighs=4` or `6` | square lattice; pick the bin size before graphing |
| Xenium | single cell | irregular points | `"generic"` | `delaunay=True` | Delaunay triangulation gives adjacency without a k cutoff |
| MERFISH / MERSCOPE | single cell | irregular points | `"generic"` | `delaunay=True` or `n_neighs=k` | k-NN (`delaunay=False`) when you want a fixed degree |
| CosMx (Nanostring) | single cell | irregular points | `"generic"` | `delaunay=True` | same as Xenium/MERFISH |

## Parameter semantics (squidpy 1.8 `sq.gr.spatial_neighbors`)

- **`coord_type`** — `"grid"`, `"generic"`, or `None`.
  - `None` auto-selects `"grid"` **only** when `spatial` is present in `adata.uns`
    with `n_neighs == 6` (the Visium signature); otherwise it uses `"generic"`.
  - Do not rely on auto-detection — pass `coord_type` explicitly so the geometry is
    unambiguous and reproducible.
- **`n_neighs`** (default `6`) — for `"grid"`, the number of neighboring tiles; for
  `"generic"`, the number of nearest neighbors, applied only when `delaunay=False`.
- **`n_rings`** (default `1`) — number of rings of neighbors; **only used for
  `coord_type="grid"`**. `n_rings=2` includes second-shell spots.
- **`delaunay`** (default `False`) — build the graph from a Delaunay triangulation;
  **only used for `coord_type="generic"`**. Preferred for single-cell platforms
  because it adapts to local density without a fixed `k`.

## Per-platform gotchas

- **Visium spots are multi-cell.** Any cell-type-level claim from raw Visium needs
  **deconvolution first** (destVI / Tangram via `alterlab-scvi-tools`,
  `references/models-spatial.md`). Squidpy graph statistics on undeconvolved spots
  describe *spot-cluster* adjacency, not single-cell adjacency.
- **Single-cell platforms (Xenium/MERFISH/CosMx)** carry true per-cell coordinates,
  so `nhood_enrichment` and `co_occurrence` are directly interpretable at cell-type
  resolution — no deconvolution step.
- **Visium HD** must have its bin size chosen before analysis; 2 µm bins are near
  single-cell but sparse, 8/16 µm bins trade resolution for counts.
- **Clusters/labels must already exist.** `nhood_enrichment`, `co_occurrence`,
  `interaction_matrix`, `centrality_scores`, and `ligrec` all take a `cluster_key`
  pointing at a categorical `adata.obs` column produced upstream (Leiden via
  `alterlab-scanpy`, or imported cell-type annotations).

## Reading `nhood_enrichment` output

`sq.gr.nhood_enrichment` runs a permutation test and stores a **z-score** matrix in
`adata.uns[f"{cluster_key}_nhood_enrichment"]["zscore"]`. Positive z = the two
clusters are adjacent more often than expected under the permuted null (attraction);
negative z = avoidance. Always report z-scores with that permutation context, never
raw adjacency counts.
