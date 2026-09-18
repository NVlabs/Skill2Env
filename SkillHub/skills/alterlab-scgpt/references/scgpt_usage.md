# scGPT — Usage Reference

Deeper detail for `alterlab-scgpt`. Verify the API, checkpoints, and pin against the upstream
`bowang-lab/scGPT` README (`TODO(verify)`) — the package API has evolved.

## Install

Install the `scgpt` package into a CUDA-enabled environment (PyTorch + flash-attn on some
setups). Download a pretrained checkpoint (whole-human / organ-specific) per the repo. A GPU
is strongly recommended.

## Typical tasks

- **Zero-shot annotation** — embed a query dataset with a pretrained checkpoint and transfer
  labels from a reference. Fast, no training.
- **Fine-tuned annotation** — fine-tune on a labeled reference for a specific tissue for higher
  accuracy (GPU-heavy — dispatch via `alterlab-remote-compute`).
- **Embeddings** — export cell/gene embeddings for clustering, UMAP, or gene-network analysis.
- **Integration** — use the model representation to integrate batches/donors.

Confirm the exact function/class names (embedding, annotation, fine-tune entry points) against
your installed version.

## scverse integration

Inputs and outputs are AnnData (`.h5ad`). Keep the object well-formed with `alterlab-anndata`,
and feed scGPT embeddings into a Scanpy neighbors/UMAP/Leiden workflow (`alterlab-scanpy`) for
downstream steps.

## Choosing the single-cell skill

| Goal | Skill |
|------|-------|
| Pretrained foundation-model annotation/embeddings | `alterlab-scgpt` |
| Probabilistic latent model (scVI/scANVI), integration, DE | `alterlab-scvi-tools` |
| Standard pipeline: QC, clustering, UMAP, marker DE | `alterlab-scanpy` |
| `.h5ad` data structure I/O and wrangling | `alterlab-anndata` |
| RNA velocity | `alterlab-scvelo` |
