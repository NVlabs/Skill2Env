# Pinned tool versions & upstream facts

All version-specific claims in this skill trace to the upstream release pages
below. Re-verify against the linked release notes before changing a pin.

## salmon — v1.11.4

- Source: COMBINE-lab/salmon releases — https://github.com/COMBINE-lab/salmon/releases
- Latest release at authoring time: **v1.11.4** (released 2026-03-11).
- **SSHash index format change.** salmon adopted a new SSHash-based k-mer index,
  replacing the prior colored compacted de Bruijn graph index. Upstream release
  notes: *"all users must rebuild their salmon indices before using v1.11.2."*
  → Practical rule: rebuild any index built before v1.11.2 with the same salmon
  version you quantify with.
- **`salmon alevin` removed.** Release notes: *"`salmon alevin` has been
  removed."* Former alevin users are directed to the **piscem + alevin-fry**
  pipeline (https://github.com/COMBINE-lab/piscem,
  https://github.com/COMBINE-lab/alevin-fry).

## kallisto — v0.52.0

- Source: pachterlab/kallisto releases — https://github.com/pachterlab/kallisto/releases
- Latest release at authoring time: **v0.52.0** (released 25 Feb). This release
  restores features (pseudobam, genomebam, fusion) that were missing after the
  index-structure rework; v0.51.1 and v0.51.0 precede it.

## kb-python (the `kb` CLI)

- Source: pachterlab/kb_python releases — https://github.com/pachterlab/kb_python/releases
- Latest release at authoring time: **v0.30.2** (released 19 May).
- **lr-kallisto / `--long`.** kb-python v0.29.1 release notes: *"Added
  lr-kallisto (--long) option, and enabling k>31"* and shipped kallisto/bustools
  binaries with and without long k-mer support. That release upgraded the bundled
  kallisto to **0.51.1** and bustools to **0.44.1**. (The bundled kallisto in a
  given kb-python build may lag the standalone kallisto release above; check
  `kb info` / your install for the exact bundled version.)

## nf-core/rnaseq — v3.26.0 (turnkey alternative)

- Source: nf-core/rnaseq releases — https://github.com/nf-core/rnaseq/releases
- Latest release at authoring time: **v3.26.0** ("Chromium Cuttlefish", released
  7 May).
- **Default route is `--aligner star_salmon`.** From the v3.26.0 usage docs:
  *"By default, the pipeline uses STAR (i.e. `--aligner star_salmon`) to map the
  raw FastQ reads to the reference genome, project the alignments onto the
  transcriptome and to perform the downstream BAM-level quantification with
  Salmon."* (https://nf-co.re/rnaseq/3.26.0/docs/usage)

## tximport / tximeta

- Bioconductor packages used for aggregating transcript-level estimates to the
  gene level (`tximport`) with full transcriptome provenance (`tximeta`,
  `linkedTxome`). They are the canonical R import layer for salmon/kallisto
  output feeding DESeq2. The Python helper in this skill reproduces the
  `countsFromAbundance = "lengthScaledTPM"` computation so the workflow can stay
  in `uv`; use the R packages when you need full `tximeta` metadata.
