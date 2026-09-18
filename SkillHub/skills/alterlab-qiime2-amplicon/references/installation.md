# Installation — QIIME 2 amplicon distribution (conda only)

QIIME 2 is distributed as a **conda environment**, not a PyPI package. There is no
`pip install qiime2` for the full distribution; the plugin ecosystem, native binaries
(MAFFT, FastTree, DADA2's R/C++ stack, cutadapt) and the framework are resolved by conda.

## 2026.1 (the `amplicon` distribution)

Verified environment files in the `qiime2/distributions` repo at
`2026.1/amplicon/released/`:

- `qiime2-amplicon-macos-latest-conda.yml`
- `qiime2-amplicon-ubuntu-latest-conda.yml`

These resolve from the channels `conda-forge`, `bioconda`, and
`https://packages.qiime2.org/qiime2/2026.1/amplicon/released`.

```bash
# macOS
conda env create \
  --name qiime2-amplicon-2026.1 \
  --file https://raw.githubusercontent.com/qiime2/distributions/dev/2026.1/amplicon/released/qiime2-amplicon-macos-latest-conda.yml

# Linux
conda env create \
  --name qiime2-amplicon-2026.1 \
  --file https://raw.githubusercontent.com/qiime2/distributions/dev/2026.1/amplicon/released/qiime2-amplicon-ubuntu-latest-conda.yml

conda activate qiime2-amplicon-2026.1
qiime info        # prints version + every installed plugin
```

`mamba` is a faster drop-in for the solve if available (`mamba env create ...`).

## 2026.4 — distribution renamed to `qiime2`

Per the 2026.1 release announcement, the **`amplicon` distribution is renamed `qiime2`
in 2026.4** (it is the historical package collection users associate with the `qiime2`
namespace). The QIIME 2 Library quickstart shows the 2026.4 install using the renamed
files, e.g.:

```bash
conda env create \
  --name rachis-qiime2-2026.4 \
  --file https://raw.githubusercontent.com/qiime2/distributions/refs/heads/dev/2026.4/qiime2/released/rachis-qiime2-linux-64-conda.yml
```

Also in the 2026.1 notes: the underlying **framework was renamed from `qiime2` to
`rachis`** and published to PyPI. The plugin **commands** in this skill
(`qiime tools import`, `qiime cutadapt trim-paired`, `qiime dada2 denoise-paired`,
`qiime feature-classifier classify-sklearn`, `qiime diversity core-metrics-phylogenetic`)
are unchanged by the rename — only the env name, channel path, and file names move.

Always confirm the exact current command from the official source rather than hardcoding:
- Quickstart: https://library.qiime2.org/quickstart/amplicon
- 2026.1 announcement: https://qiime2.org/news/qiime-2-2026-1-is-now-available-33935/

## Viewing artifacts

- In-browser, offline: https://view.qiime2.org (nothing is uploaded; it runs locally).
- CLI: `qiime tools view file.qzv`.

## Sources

- `qiime2/distributions` repo, `dev` branch, `2026.1/amplicon/released/` (env files
  confirmed to exist and resolve over HTTPS).
- QIIME 2 2026.1 release announcement (distribution rename to `qiime2` in 2026.4;
  framework renamed to `rachis` on PyPI).
- QIIME 2 Library amplicon quickstart (2026.4 `rachis-qiime2-*` install command).
