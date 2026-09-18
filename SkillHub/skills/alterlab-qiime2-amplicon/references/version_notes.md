# Version notes — QIIME 2 2026.1 and the 2026.4 rename

Pin this skill to **QIIME 2 2026.1** (the `amplicon` distribution). Facts below are from
the official 2026.1 release announcement
(https://qiime2.org/news/qiime-2-2026-1-is-now-available-33935/, announced 2026-01-28).

## Breaking change: `feature-table summarize`

In `q2-feature-table`, **2026.1 swapped two action names**:

- the old `summarize` **visualizer** was renamed **`_summarize`** (now private), and
- the former **`summarize_plus` pipeline** was renamed to **`summarize`**.

Net effect: today, calling `qiime feature-table summarize` runs what used to be
`summarize_plus` — the **enhanced** summary that also produces feature-frequency and
sample-frequency artifacts in addition to the `.qzv`. Consequences for workflows:

- **Older tutorials that call `summarize_plus`** must switch to `summarize`.
- Do **not** call `_summarize` (private/legacy).
- Practically, keep using `qiime feature-table summarize` and read `table.qzv`; that *is*
  the plus behavior now.

## Distribution rename in 2026.4

The 2026.1 notes announce: *"in our next release (2026.4) we will be renaming the amplicon
distribution to qiime2, since this is the historical collection of packages that our user
base is familiar with in the context of the qiime2 namespace."*

Implications:

- The conda **env file name and channel path change** (e.g. `rachis-qiime2-*-conda.yml`
  under a `2026.4/qiime2/released/` path; see `installation.md`).
- The **plugin commands do not change** — `qiime tools import`,
  `qiime cutadapt trim-paired`, `qiime dada2 denoise-paired`,
  `qiime feature-classifier classify-sklearn`,
  `qiime diversity core-metrics-phylogenetic` are all stable across the rename.

## Framework renamed to `rachis`

Also in 2026.1: the underlying QIIME 2 **framework was renamed from `qiime2` to
`rachis`** and is now published on PyPI. This is the framework package, not the user-facing
`qiime` CLI; pipeline command names are unaffected. (This is why the 2026.4 env files are
named `rachis-qiime2-*`.)

## Other plugin updates noted in 2026.1

- `q2-alignment`: added protein-sequence support.
- `q2-boots`: improved memory efficiency in medoid calculations.
- `q2-types`: added formats for genomic data and taxonomy-to-contig mappings.

## How to stay current

When running a different release, **verify command names and install files from the
official sources** rather than trusting this file:

- Release announcement: https://qiime2.org/news/qiime-2-2026-1-is-now-available-33935/
- Amplicon docs: https://amplicon-docs.qiime2.org/
- Library quickstart (install): https://library.qiime2.org/quickstart/amplicon
- In the active env: `qiime info` and `qiime <plugin> <action> --help`.
