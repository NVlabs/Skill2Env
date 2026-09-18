# tximport / tximeta handoff to pydeseq2

## What tximport does

salmon `quant.sf` and kallisto `abundance.tsv/.h5` are **transcript-level**.
DESeq2/PyDESeq2 work at the **gene level**. `tximport` summarizes transcript
estimates to genes using a transcript→gene map (`tx2gene`) and, importantly,
generates an **average-transcript-length offset** so the model accounts for
changes in transcript usage between samples.

The recommended import for DESeq2 uses
`countsFromAbundance = "lengthScaledTPM"` (or `"scaledTPM"`), which produces
length-scaled, library-size-scaled counts that correct for between-sample
differences in average transcript length, suitable to feed directly into the
differential-expression model. (GC/sequence-bias correction is a separate step
done earlier by salmon's `--gcBias`/`--seqBias`, not by tximport.)

## tx2gene map

A two-column table mapping `transcript_id` → `gene_id`. Build it from the same
GTF/GFF3 annotation used to make the transcriptome FASTA. `scripts/build_tx2gene.py`
parses `transcript_id` and `gene_id` attributes from a GTF and writes a TSV.

```bash
uv run python scripts/build_tx2gene.py annotation.gtf --out tx2gene.tsv
```

Caveat: transcript IDs in the `quant.sf`/`abundance.tsv` `Name`/`target_id`
column must match the IDs in `tx2gene` (watch for version suffixes like
`ENST00000456328.2` vs `ENST00000456328` — strip with `--strip-version` if your
annotation and reference disagree).

## Python aggregation helper

`scripts/import_quant.py` reproduces the tximport `lengthScaledTPM` computation
in pure stdlib (no pandas) so the workflow can stay in `uv`:

```bash
uv run python scripts/import_quant.py \
  --quants quants \
  --tx2gene tx2gene.tsv \
  --out-counts gene_counts.tsv \
  --out-tpm gene_tpm.tsv
```

It reads every `<sample>/quant.sf` (auto-detects kallisto `abundance.tsv` too)
and applies tximport's `makeCountsFromAbundance(..., "lengthScaledTPM")` at the
transcript level before summarizing to genes:

1. `newCounts[tx, s] = TPM[tx, s] * mean_over_samples(effLength[tx, :])`
2. rescale each sample column so its total equals that sample's original
   mapped-read count: `* (sum NumReads[:, s] / sum newCounts[:, s])`
3. sum the scaled transcript counts per gene and round to integers.

The result is length-corrected and library-size-scaled (per-sample column totals
equal the salmon/kallisto library size) — **not** a plain sum of raw `NumReads`.
The gene × TPM matrix is the per-gene sum of transcript TPMs. The only
differences from Bioconductor `tximport` are integer rounding and the lack of
`tximeta` provenance metadata; for exact parity or provenance use the R path
below.

## When to use the R path instead

Prefer the Bioconductor `tximport` + `tximeta` packages when you need:

- Full **`tximeta` provenance** — `linkedTxome` records the exact transcriptome
  checksum, source, and release, attaching it to the imported object.
- The officially validated `dtuScaledTPM` mode for differential transcript usage,
  or exact parity with a published DESeq2/tximport pipeline.

In R the flow is `tximport(files, type="salmon", tx2gene=..., countsFromAbundance="lengthScaledTPM")`
→ `DESeqDataSetFromTximport(...)`. The Python helper here is a convenience that
covers the common count-matrix case.

## Handoff

The resulting `gene_counts.tsv` (gene × sample integer matrix) plus a sample
metadata sheet (sample → condition) are exactly the inputs **`alterlab-pydeseq2`**
expects. This skill stops here; pydeseq2 owns normalization, dispersion, Wald
tests, FDR, and plots.
