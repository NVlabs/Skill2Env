# Single-cell RNA-seq: `salmon alevin` is removed

## The change

As of salmon **v1.11.x**, **`salmon alevin` has been removed** (upstream release
notes; see ../references/tool_versions.md). Single-cell / droplet RNA-seq
quantification is no longer a salmon subcommand. Any instruction that writes
`salmon alevin ...` is outdated and will fail.

## The replacement: piscem + alevin-fry

COMBINE-lab directs former alevin users to the **piscem + alevin-fry** pipeline,
which the release notes describe as offering improved memory efficiency and
throughput and being actively maintained:

- **piscem** — the indexing + mapping tool: https://github.com/COMBINE-lab/piscem
- **alevin-fry** — single-cell quantification (collation, barcode/UMI
  resolution, count-matrix generation): https://github.com/COMBINE-lab/alevin-fry

The typical flow is: build a piscem index of the (spliced+intron, if RNA
velocity is desired) reference, map the single-cell reads to produce a RAD file,
then run alevin-fry `generate-permit-list` → `collate` → `quant` to produce the
cell × gene count matrix.

## Routing

This skill (`alterlab-rnaseq-quant`) covers **bulk** RNA-seq only. For
single-cell:

1. Quantify with piscem + alevin-fry (their docs are the source of truth for the
   exact subcommand syntax — verify before running, as the CLI evolves).
2. Take the resulting count matrix downstream to:
   - `alterlab-scanpy` — single-cell analysis (QC, clustering, UMAP).
   - `alterlab-scvi-tools` — probabilistic single-cell models.
   - `alterlab-anndata` — to load/manipulate the matrix as an AnnData object.

Do not attempt to force single-cell barcoded data through the bulk salmon/kallisto
path; the barcode/UMI structure requires the alevin-fry tooling.
