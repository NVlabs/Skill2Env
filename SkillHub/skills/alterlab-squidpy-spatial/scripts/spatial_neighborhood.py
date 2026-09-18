#!/usr/bin/env python3
"""
Spatial neighborhood analysis for squidpy (1.8.x).

Given a clustered AnnData (.h5ad) that already carries a categorical cluster /
cell-type column in ``adata.obs`` (produce it upstream with alterlab-scanpy), this
script:

  1. builds the spatial neighbor graph with the *correct* ``coord_type`` for the
     platform (the one decision that invalidates everything downstream if wrong),
  2. runs ``sq.gr.nhood_enrichment`` (permutation z-scores per cluster pair),
  3. runs ``sq.gr.co_occurrence`` (adjacency vs. radial distance),
  4. runs ``sq.gr.spatial_autocorr`` (Moran's I -> spatially variable genes),

then writes a compact JSON summary and (optionally) the updated .h5ad.

Platform -> coord_type (squidpy 1.8 sq.gr.spatial_neighbors semantics):
  visium / visium_hd        -> coord_type="grid"     (n_neighs / n_rings)
  xenium / merfish / cosmx  -> coord_type="generic"  (delaunay=True)

This runs locally and sends no data anywhere. squidpy + scanpy must be installed
(``uv run --with squidpy python ...`` or a project env). For large single-cell
panels this is a good candidate to run on local compute rather than burning API
calls.

Usage:
    uv run python spatial_neighborhood.py clustered.h5ad \
        --platform xenium --cluster-key leiden --out spatial_report.json
"""
from __future__ import annotations

import argparse
import json
import sys

# Platform -> (coord_type, kwargs for sq.gr.spatial_neighbors)
GRID_PLATFORMS = {"visium", "visium_hd"}
GENERIC_PLATFORMS = {"xenium", "merfish", "merscope", "cosmx"}


def graph_kwargs(platform: str, n_neighs: int, n_rings: int):
    """Return the spatial_neighbors kwargs for the platform."""
    platform = platform.lower()
    if platform in GRID_PLATFORMS:
        return {"coord_type": "grid", "n_neighs": n_neighs, "n_rings": n_rings}
    if platform in GENERIC_PLATFORMS:
        # Delaunay adapts to local density without a fixed k -> preferred single-cell.
        return {"coord_type": "generic", "delaunay": True}
    raise ValueError(
        f"unknown platform {platform!r}; "
        f"expected one of {sorted(GRID_PLATFORMS | GENERIC_PLATFORMS)}"
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Build a squidpy spatial graph and run core neighborhood statistics."
    )
    p.add_argument("h5ad", help="Path to a clustered AnnData .h5ad (labels in obs).")
    p.add_argument(
        "--platform",
        required=True,
        help="visium | visium_hd | xenium | merfish | merscope | cosmx",
    )
    p.add_argument(
        "--cluster-key",
        default="leiden",
        help="Categorical obs column with cluster / cell-type labels (default: leiden).",
    )
    p.add_argument("--n-neighs", type=int, default=6, help="grid n_neighs (default: 6).")
    p.add_argument("--n-rings", type=int, default=1, help="grid n_rings (default: 1).")
    p.add_argument(
        "--moran-top", type=int, default=20, help="How many top SVGs to report (default: 20)."
    )
    p.add_argument("--out", default=None, help="Write JSON summary here (default: stdout).")
    p.add_argument(
        "--write-h5ad", default=None, help="Optionally write the updated AnnData here."
    )
    args = p.parse_args(argv)

    try:
        import scanpy as sc
        import squidpy as sq
    except ImportError as exc:  # pragma: no cover - dependency guard
        print(
            f"ERROR: this script needs scanpy + squidpy installed ({exc}). "
            "Try: uv run --with squidpy python " + __file__,
            file=sys.stderr,
        )
        return 2

    try:
        kwargs = graph_kwargs(args.platform, args.n_neighs, args.n_rings)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    adata = sc.read_h5ad(args.h5ad)

    if args.cluster_key not in adata.obs:
        print(
            f"ERROR: cluster key {args.cluster_key!r} not found in adata.obs "
            f"(have: {list(adata.obs.columns)}). Cluster upstream with alterlab-scanpy.",
            file=sys.stderr,
        )
        return 2

    # 1. spatial graph (the consequential choice)
    sq.gr.spatial_neighbors(adata, **kwargs)

    # 2. neighborhood enrichment (permutation z-scores)
    sq.gr.nhood_enrichment(adata, cluster_key=args.cluster_key)
    nhood = adata.uns.get(f"{args.cluster_key}_nhood_enrichment", {})
    zscore = nhood.get("zscore")
    categories = list(adata.obs[args.cluster_key].cat.categories) if hasattr(
        adata.obs[args.cluster_key], "cat"
    ) else sorted(set(map(str, adata.obs[args.cluster_key])))

    # 3. co-occurrence across distance
    sq.gr.co_occurrence(adata, cluster_key=args.cluster_key)

    # 4. spatially variable genes via Moran's I
    sq.gr.spatial_autocorr(adata, mode="moran")
    moran = adata.uns.get("moranI")
    top_svgs = []
    if moran is not None:
        moran_sorted = moran.sort_values("I", ascending=False).head(args.moran_top)
        for gene, row in moran_sorted.iterrows():
            entry = {"gene": str(gene), "morans_I": float(row["I"])}
            if "pval_norm" in moran_sorted.columns:
                entry["pval_norm"] = float(row["pval_norm"])
            if "pval_norm_fdr_bh" in moran_sorted.columns:
                entry["fdr_bh"] = float(row["pval_norm_fdr_bh"])
            top_svgs.append(entry)

    report = {
        "tool": "alterlab-squidpy-spatial/spatial_neighborhood.py",
        "version": "1.0.0",
        "input": args.h5ad,
        "platform": args.platform.lower(),
        "spatial_neighbors_kwargs": kwargs,
        "cluster_key": args.cluster_key,
        "n_obs": int(adata.n_obs),
        "n_vars": int(adata.n_vars),
        "clusters": categories,
        "nhood_enrichment_zscore": (
            zscore.tolist() if zscore is not None else None
        ),
        "top_spatially_variable_genes": top_svgs,
        "notes": (
            "z-scores are permutation-test based: positive = spatial attraction, "
            "negative = avoidance. For Visium spot data, deconvolve "
            "(alterlab-scvi-tools) before cell-type-level claims."
        ),
    }

    if args.write_h5ad:
        adata.write(args.write_h5ad)
        report["written_h5ad"] = args.write_h5ad

    payload = json.dumps(report, indent=2)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(payload)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
