---
name: alterlab-rnaseq-quant
description: Quantifies bulk RNA-seq transcript abundance with salmon (v1.11.4 selective alignment) and kallisto (v0.52.0, kb-python workflow), builds a decoy-aware gentrome index, runs quant with --validateMappings --gcBias -l A, then imports estimates via tximport/tximeta with a tx2gene map and hands differential expression to alterlab-pydeseq2. Warns that salmon's index format changed to SSHash (rebuild pre-v1.11.2 indices) and that 'salmon alevin' was REMOVED (single-cell now uses piscem + alevin-fry). Use when quantifying RNA-seq transcript abundance, running salmon or kallisto, building a decoy-aware index, or wiring tximport to DESeq2; for differential expression use alterlab-pydeseq2, for FASTQ-to-VCF variant calling use alterlab-nf-core-sarek. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*) Bash(salmon:*) Bash(kallisto:*) Bash(kb:*)
compatibility: "Requires the salmon and/or kallisto CLI on PATH (conda/bioconda or a container). salmon v1.11.4 and kallisto v0.52.0 are the versions this skill targets; the tximport/tx2gene helper runs under `uv run python` with pure stdlib (no pandas needed). No API key or account required; all work is local."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    last_updated: "2026-06-06"
    depends_on: "alterlab-pydeseq2 (downstream differential expression)"
---

# RNA-seq Quantification — salmon & kallisto Transcript Abundance

The command-line quantification entry point for bulk RNA-seq: take raw FASTQ
reads plus a reference transcriptome and produce transcript-level abundance
estimates (counts + TPM) with **salmon** (selective alignment) or **kallisto**
(pseudoalignment via kb-python), then aggregate to the gene level with
`tximport`/`tximeta` and hand off to `alterlab-pydeseq2` for differential
expression. It is the raw-data-to-count-matrix pipeline that the repo's Python
analysis skills assume already ran.

## Quick Start

```
Quantify these RNA-seq FASTQs with salmon and a decoy-aware index
Build a salmon gentrome index from this transcriptome + genome
Run kallisto / kb count on my paired-end reads
Turn my salmon quant.sf files into a gene-level count matrix for DESeq2
```

→ Build a **decoy-aware** index once, run `salmon quant` (or `kb count`) per
sample, then run `scripts/build_tx2gene.py` + `scripts/import_quant.py` to make
the `tximport` gene matrix and route it to `alterlab-pydeseq2`.

---

## When to Use This Skill

Use this skill when the request is about **getting from FASTQ to transcript or
gene abundance** with a lightweight quantifier:

- "Quantify my RNA-seq with salmon / kallisto."
- "Build a decoy-aware salmon index (gentrome + decoys.txt)."
- "Run selective alignment with `--validateMappings --gcBias`."
- "I have `quant.sf` files — make me a gene-level count matrix for DESeq2."
- "Set up `tximport` / `tximeta` with a tx2gene map."
- "Use kb-python / `kb count` to pseudoalign these reads."

### Does NOT Trigger — route these to the right sibling

| The request is really about… | Route to |
|------------------------------|----------|
| Differential expression on a **count matrix** (DESeq2 Wald tests, FDR, volcano) | `alterlab-pydeseq2` |
| **Single-cell** RNA-seq quantification (was `salmon alevin`) | piscem + alevin-fry — see [references/single_cell_alevin.md](references/single_cell_alevin.md); downstream → `alterlab-scanpy` / `alterlab-scvi-tools` |
| **FASTQ-to-VCF** germline/somatic variant calling | `alterlab-nf-core-sarek` |
| **16S/ITS amplicon** (microbiome) FASTQ-to-feature-table | `alterlab-qiime2-amplicon` |
| **Spatial** transcriptomics (Visium/Xenium) neighborhood analysis | `alterlab-squidpy-spatial` |
| Loading/manipulating the resulting matrix as an **AnnData** object | `alterlab-anndata` |
| BLAST/DIAMOND **sequence similarity search** | `alterlab-blast` |
| Quick gene/transcript **ID lookups & reference fetch** (Ensembl/RefSeq) | `alterlab-gget` |
| Aligned **BAM** manipulation, coverage, read counting from alignments | `alterlab-pysam` |

This skill stops at the **count/abundance matrix**. It does not call DEGs, does
not handle single-cell barcodes, and does not align to a genome for variant
calling.

---

## Two Critical Correctness Traps (read before quantifying)

These are the two failures most outdated RNA-seq instructions get wrong as of
salmon **v1.11.4** (released 2026-03-11). Both are confirmed in the upstream
release notes (see [references/tool_versions.md](references/tool_versions.md)).

1. **The salmon index format changed to SSHash.** salmon switched from the
   colored compacted de Bruijn graph index to a new SSHash-based k-mer index.
   The release notes state **all previously built indices must be rebuilt**
   before using v1.11.2+. If you reuse a pre-v1.11.2 index you will get an error
   or silently wrong results — **always rebuild the index** with the same salmon
   version you quantify with.

2. **`salmon alevin` was REMOVED.** Single-cell quantification is no longer part
   of salmon. The release notes direct former `alevin` users to the
   **piscem + alevin-fry** pipeline. Do **not** write `salmon alevin` commands.
   If the user has single-cell / droplet data, route per the table above and see
   [references/single_cell_alevin.md](references/single_cell_alevin.md).

---

## Pipeline (salmon, the default path)

### 1. Build a decoy-aware gentrome index (once per reference)

A **decoy-aware** index lets salmon distinguish reads that align better to the
genome than the transcriptome, reducing spurious assignments. You build a
"gentrome" = transcripts FASTA **concatenated with the genome FASTA**, plus a
`decoys.txt` listing the genome sequence names as decoys.

```bash
# 1. decoys.txt = the genome's sequence (chromosome) names, one per line
grep "^>" genome.fa | sed 's/^>//; s/ .*//' > decoys.txt

# 2. gentrome = transcripts FIRST, then genome (order matters)
cat transcripts.fa genome.fa > gentrome.fa

# 3. build the index (rebuild for v1.11.4 — see trap #1)
salmon index \
  -t gentrome.fa \
  -d decoys.txt \
  -i salmon_index \
  -k 31 \
  -p 8
```

- `-k 31` is the default k-mer; lower it only for very short reads.
- The helper `scripts/make_decoys.py` writes `decoys.txt` and `gentrome.fa` for
  you and refuses to proceed if the genome names are absent from the transcript
  FASTA (a common silent mistake). See [references/decoy_index.md](references/decoy_index.md).

### 2. Quantify each sample

```bash
salmon quant \
  -i salmon_index \
  -l A \
  -1 sampleA_R1.fastq.gz -2 sampleA_R2.fastq.gz \
  --validateMappings \
  --gcBias \
  -p 8 \
  -o quants/sampleA
```

- **`-l A`** — auto-detect library type (strandedness). Let salmon infer it
  unless you have a documented protocol; verify the inferred type in
  `lib_format_counts.json`.
- **`--validateMappings`** — enables selective alignment (the accurate default
  mode; scores mappings rather than trusting raw pseudo-mappings).
- **`--gcBias`** — corrects fragment-level GC bias; recommended for DE and cheap
  to enable. Add `--seqBias` for 5'/3' sequence-specific bias if needed.
- For single-end reads, pass `-r reads.fastq.gz` instead of `-1/-2`.

Each sample produces `quants/<sample>/quant.sf` (transcript-level estimates) and
`quants/<sample>/lib_format_counts.json` (the inferred library type). See
[references/salmon_quant.md](references/salmon_quant.md) for the full flag map
and per-sample QC checks.

### 3. Aggregate to gene level with tximport

Build a transcript→gene map (`tx2gene`) from your annotation, then summarize the
per-sample `quant.sf` files into a gene-level matrix that `pydeseq2` consumes.

```bash
# tx2gene from a GTF/GFF3 (transcript_id -> gene_id)
uv run python scripts/build_tx2gene.py annotation.gtf --out tx2gene.tsv

# import + summarize to gene level (tximport "lengthScaledTPM" counts)
uv run python scripts/import_quant.py \
  --quants quants \
  --tx2gene tx2gene.tsv \
  --out-counts gene_counts.tsv \
  --out-tpm gene_tpm.tsv
```

`import_quant.py` produces an integer-rounded gene × sample count matrix plus a
gene × sample TPM matrix, the inputs `alterlab-pydeseq2` expects. It implements
tximport's `makeCountsFromAbundance(..., "lengthScaledTPM")` at the transcript
level (scale each transcript's TPM by its sample-averaged effective length, then
rescale each sample column back to its mapped-read library size) and sums to
genes — so the counts are length-corrected and library-size-scaled, **not** raw
summed `NumReads`. The canonical R route is the `tximport` / `tximeta`
Bioconductor packages with `countsFromAbundance = "lengthScaledTPM"`; the Python
helper here reproduces that computation so you can stay in `uv` (differing only
in integer rounding and the absence of `tximeta` provenance). See
[references/tximport_handoff.md](references/tximport_handoff.md) for the exact
semantics, the `tximeta` linkedTxome metadata option, and when to prefer the R
path.

### 4. Hand off to differential expression

Pass `gene_counts.tsv` (+ a sample/condition sheet) to **`alterlab-pydeseq2`**.
This skill does not call DEGs — that is pydeseq2's job (size-factor
normalization, dispersion, Wald tests, BH-FDR, volcano/MA plots).

---

## Pipeline (kallisto, the pseudoalignment path)

`kallisto` (standalone **v0.52.0**) and the **kb-python** wrapper (`kb`) give a
faster pseudoalignment route. kb-python drives `kallisto | bustools` and writes
tidy outputs.

```bash
# build a kallisto index from the transcriptome
kallisto index -i kallisto_index.idx transcripts.fa

# quantify a paired-end sample
kallisto quant -i kallisto_index.idx -o quants_kallisto/sampleA \
  sampleA_R1.fastq.gz sampleA_R2.fastq.gz

# OR the kb-python workflow (bulk)
# -f1 is the cDNA FASTA kb WRITES; trailing positionals are genome FASTA THEN GTF
kb ref -i index.idx -g t2g.txt -f1 cdna.fa genome.fa annotation.gtf
kb count -i index.idx -g t2g.txt -x bulk -o quants_kb/sampleA \
  sampleA_R1.fastq.gz sampleA_R2.fastq.gz
```

- kallisto outputs `abundance.tsv` / `abundance.h5`; feed these to `tximport`
  (`type="kallisto"`) the same way as salmon's `quant.sf`.
- **Long reads:** kb-python exposes **lr-kallisto** via the `--long` flag (and
  `k>31` k-mers) — use it for ONT/PacBio cDNA. See
  [references/kallisto_kb.md](references/kallisto_kb.md).
- kallisto does not use the decoy/gentrome construction; that is salmon-specific.

---

## Turnkey alternative — nf-core/rnaseq

For an end-to-end, provenance-tracked pipeline (trimming → alignment →
quantification → QC), **nf-core/rnaseq v3.26.0** runs `--aligner star_salmon` by
default: STAR maps to the genome, projects onto the transcriptome, and Salmon
does the quantification. Reach for it when the user wants a reproducible
Nextflow pipeline rather than hand-run commands; this skill covers the
direct-salmon/kallisto path and the tximport handoff. See
[references/tool_versions.md](references/tool_versions.md).

---

## Offload note

Indexing and per-sample quantification are CPU/IO-heavy but fully offline. On a
local workstation these are good candidates to run directly (e.g. overnight)
rather than streaming large FASTQs through an API session. Build the index once;
quantify samples in a loop.

---

## Self-Check Before Reporting

- Did you **rebuild** the salmon index with the v1.11.4 you quantified with
  (SSHash format — trap #1)? Never reuse a pre-v1.11.2 index.
- Is the index **decoy-aware** (gentrome + `decoys.txt`) for salmon? Confirm the
  genome names made it into `decoys.txt`.
- Did you let `-l A` infer strandedness, and did you sanity-check the inferred
  type in `lib_format_counts.json`?
- Is the data actually **single-cell**? If so you must NOT use this path —
  `salmon alevin` is gone; route to piscem + alevin-fry (trap #2).
- Did you stop at the **count matrix** and hand DE off to `alterlab-pydeseq2`
  rather than calling DEGs here?

---

## References

- [references/tool_versions.md](references/tool_versions.md) — pinned versions
  (salmon v1.11.4, kallisto v0.52.0, kb-python, nf-core/rnaseq v3.26.0) and the
  upstream release-note facts (SSHash index change, alevin removal).
- [references/decoy_index.md](references/decoy_index.md) — decoy-aware gentrome
  index construction, gotchas, and the `make_decoys.py` helper.
- [references/salmon_quant.md](references/salmon_quant.md) — `salmon quant` flag
  map, library-type inference, and per-sample QC.
- [references/kallisto_kb.md](references/kallisto_kb.md) — kallisto / kb-python
  workflow, `--long` (lr-kallisto), and output handling.
- [references/tximport_handoff.md](references/tximport_handoff.md) — tximport /
  tximeta aggregation, tx2gene, `countsFromAbundance`, and the pydeseq2 handoff.
- [references/single_cell_alevin.md](references/single_cell_alevin.md) — why
  `salmon alevin` is removed and the piscem + alevin-fry replacement.

Part of the AlterLab Academic Skills suite.
