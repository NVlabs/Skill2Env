# Per-step parameters, primers, and QC reading

All action and flag names below are verified from the QIIME 2 plugin sources
(`q2-cutadapt`, `q2-dada2`) and the Moving Pictures tutorial. Do not invent flags —
run `qiime <plugin> <action> --help` in the active env to see the exact signature for
your installed version.

## cutadapt trim-paired

Source-verified parameters (`q2-cutadapt` `dev`, `plugin_setup.py`): `front_f`,
`front_r`, `discard_untrimmed` (CLI: `--p-front-f`, `--p-front-r`,
`--p-discard-untrimmed`). The single-end action is `trim-single` with `--p-front`.

```bash
qiime cutadapt trim-paired \
  --i-demultiplexed-sequences demux.qza \
  --p-front-f <FORWARD_PRIMER> \
  --p-front-r <REVERSE_PRIMER> \
  --p-discard-untrimmed \
  --o-trimmed-sequences demux-trimmed.qza
```

### Common primer pairs (fill in YOUR study's actual primers)

These are widely used reference primers; confirm against your sequencing facility's
protocol before using — primer choice is study-specific.

| Target | Primer | Sequence |
|--------|--------|----------|
| 16S V4 | 515F (Parada) | `GTGYCAGCMGCCGCGGTAA` |
| 16S V4 | 806R (Apprill) | `GGACTACNVGGGTWTCTAAT` |
| 16S V3–V4 | 341F | `CCTACGGGNGGCWGCAG` |
| 16S V3–V4 | 805R | `GACTACHVGGGTATCTAATCC` |
| Fungal ITS | ITS1F | `CTTGGTCATTTAGAGGAAGTAA` |
| Fungal ITS | ITS2 | `GCTGCGTTCTTCATCGATGC` |

`--p-discard-untrimmed` keeps only reads where the primer was found — standard for
targeted amplicons. Without it, untrimmed reads pass through and pollute DADA2.

## dada2 denoise-paired

Source-verified parameters (`q2-dada2` `dev`, `plugin_setup.py`): `trunc_len_f`,
`trunc_len_r`, `trim_left_f`, `trim_left_r` (CLI `--p-trunc-len-f` etc.). The single-end
action `denoise-single` uses `--p-trunc-len` / `--p-trim-left`.

```bash
qiime dada2 denoise-paired \
  --i-demultiplexed-seqs demux-trimmed.qza \
  --p-trunc-len-f <F> --p-trunc-len-r <R> \
  --p-trim-left-f 0 --p-trim-left-r 0 \
  --o-representative-sequences rep-seqs.qza \
  --o-table table.qza \
  --o-denoising-stats denoising-stats.qza
```

### Choosing `--p-trunc-len-f/-r`

1. Open `demux-trimmed.qzv` → "Interactive Quality Plot".
2. Truncate each read where the **median quality** (box plot) drops sharply
   (commonly below ~Q25–Q30). Forward and reverse are chosen independently.
3. **Overlap constraint:** for paired merging, `trunc_len_f + trunc_len_r` must exceed
   the amplicon length by enough for DADA2's minimum overlap (default ~12 nt). Truncate
   too hard and pairs fail to merge.
4. `0` means no truncation (use for ITS / variable-length amplicons).

### Reading `denoising-stats.qzv`

`qiime metadata tabulate --m-input-file denoising-stats.qza --o-visualization
denoising-stats.qzv`. Inspect per-sample columns:

- **input → filtered**: quality filtering loss (usually small).
- **denoised → merged**: a large drop here means insufficient overlap → relax trunc-len.
- **merged → non-chimeric**: a large drop means many chimeras → often a sign primers were
  not removed before denoising.

## feature-table summarize

```bash
qiime feature-table summarize \
  --i-table table.qza \
  --m-sample-metadata-file sample-metadata.tsv \
  --o-summary table.qzv
```

In 2026.1 this is the former `summarize_plus` (see `version_notes.md`). Use `table.qzv`
to pick `--p-sampling-depth` for diversity: the "Interactive Sample Detail" /
frequency-per-sample view shows how many samples you retain at each depth.

## phylogeny + core-metrics-phylogenetic

```bash
qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences rep-seqs.qza \
  --o-alignment aligned.qza --o-masked-alignment masked.qza \
  --o-tree unrooted-tree.qza --o-rooted-tree rooted-tree.qza

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny rooted-tree.qza \
  --i-table table.qza \
  --p-sampling-depth <DEPTH> \
  --m-metadata-file sample-metadata.tsv \
  --output-dir core-metrics
```

`core-metrics-phylogenetic` rarefies to `--p-sampling-depth` and outputs Faith's PD,
observed features, Shannon, Pielou evenness, Bray-Curtis / Jaccard / weighted &
unweighted UniFrac distance matrices, plus Emperor PCoA `.qzv`s.

## Sources

- `q2-cutadapt` `dev` `plugin_setup.py` (trim-paired / trim-single parameter names).
- `q2-dada2` `dev` `plugin_setup.py` (denoise-paired / denoise-single parameter names).
- QIIME 2 Moving Pictures tutorial (`phylogeny align-to-tree-mafft-fasttree`,
  `diversity core-metrics-phylogenetic`, `--p-sampling-depth`).
- Primer sequences are standard published reference primers; verify against your protocol.
