# Importing data & the manifest format

Everything entering QIIME 2 must be **imported into a typed `.qza`** first. For
demultiplexed reads, a **manifest** gives you explicit control over the sample-ID →
FASTQ-path mapping (preferred over directory-format guessing).

## Paired-end manifest (recommended)

Semantic type: `SampleData[PairedEndSequencesWithQuality]`.
Input format: `PairedEndFastqManifestPhred33V2` (verified present in `q2-types`,
`q2_types/per_sample_sequences/_formats.py`).

The V2 manifest is a **TSV** with a header and one row per sample:

```
sample-id	forward-absolute-filepath	reverse-absolute-filepath
sample1	/abs/path/sample1_R1.fastq.gz	/abs/path/sample1_R2.fastq.gz
sample2	/abs/path/sample2_R1.fastq.gz	/abs/path/sample2_R2.fastq.gz
```

- Paths must be **absolute**.
- `Phred33V2` means Phred+33 quality encoding (modern Illumina). A `Phred64` variant
  exists for legacy data; do not mix.

```bash
qiime tools import \
  --type 'SampleData[PairedEndSequencesWithQuality]' \
  --input-format PairedEndFastqManifestPhred33V2 \
  --input-path manifest.tsv \
  --output-path demux.qza
```

## Single-end manifest

Format `SingleEndFastqManifestPhred33V2` (also in `q2-types`), one path column
(`absolute-filepath`), type `SampleData[SequencesWithQuality]`.

## EMP-style (multiplexed, barcodes still attached)

If reads are **not yet demultiplexed** (EMP protocol), import as
`EMPPairedEndSequences` / `EMPSingleEndSequences` and demultiplex with `qiime demux`
(e.g. `qiime demux emp-single`) using a barcodes column in the metadata. The Moving
Pictures tutorial uses `EMPSingleEndSequences` + `qiime tools import` then
`qiime demux summarize`.

## After import — always summarize

```bash
qiime demux summarize --i-data demux.qza --o-visualization demux.qzv
```

`demux.qzv` gives you the **interactive quality plot** that drives DADA2 truncation
length choices. Read it before denoising.

## ITS-specific note

For fungal ITS amplicons, the amplicon length is **variable**, so aggressive fixed
truncation in DADA2 can discard real reads. Many ITS workflows trim primers with cutadapt
and then run DADA2 with `--p-trunc-len 0` (no truncation), relying on quality trimming
only. Pair with the UNITE classifier (see `classifiers.md`).

## Sources

- `q2-types` `dev` branch, `q2_types/per_sample_sequences/_formats.py` and `__init__.py`
  (manifest format class names confirmed).
- QIIME 2 Moving Pictures tutorial (EMP import + `demux summarize` commands).
