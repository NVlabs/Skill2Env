---
name: alterlab-nf-core-sarek
description: "Runs FASTQ-to-VCF germline and somatic variant calling via the Nextflow nf-core/sarek pipeline pinned to -r 3.8.1 — builds the samplesheet.csv (patient, sex, status, sample, lane, fastq_1, fastq_2), runs bwa-mem/bwa-mem2/dragmap alignment plus GATK4 MarkDuplicates and BQSR against the GATK GRCh38 resource bundle (dbSNP, Mills/1000G indels), and selects callers — explicitly correcting that sarek defaults to Strelka when --tools is unset (pass haplotypecaller for GATK best practice or deepvariant for CNN accuracy), with a non-Nextflow manual GATK4 fallback. Use when the user wants a variant-calling pipeline, FASTQ to VCF, germline or somatic SNV/indel calling, nf-core/sarek, GATK best-practices alignment-to-VCF, or BQSR/HaplotypeCaller/Mutect2/DeepVariant; annotate hits with alterlab-clinvar/alterlab-gnomad/alterlab-cosmic, parse VCFs with alterlab-pysam, store at scale with alterlab-tiledbvcf. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*) Bash(nextflow:*)
compatibility: "Requires Nextflow plus a container engine (Docker/Singularity/Apptainer) or conda; the pipeline pulls nf-core/sarek 3.8.1 and reference bundles over the network on first run. The manual GATK4 fallback needs bwa-mem2 + samtools + gatk4 (bioconda) and runs offline once references are local. No API key. Indexing, BQSR and variant calling are long, compute-heavy jobs — good candidates to run locally rather than through repeated API calls."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    last_updated: "2026-06-06"
---

# nf-core/sarek — FASTQ-to-VCF Variant Calling

The workflow-runner entry point for raw-reads-to-variants: drive the
**Nextflow [nf-core/sarek](https://nf-co.re/sarek/3.8.1/) pipeline (pinned `-r 3.8.1`)**
to take germline or somatic short-read FASTQ through alignment, GATK4 duplicate
marking and base-quality recalibration, and SNV/indel calling, then hand the
resulting VCFs to the suite's database and parsing skills for interpretation.

This skill is the **command-line / workflow** counterpart to the suite's
Python-library bioinformatics skills. Use it for the *raw-data-to-VCF* leg;
use the library skills (`alterlab-pysam`, `alterlab-tiledbvcf`) once you hold a VCF.

## When to Use This Skill

Trigger this skill when the user wants to:

- Go from **FASTQ to VCF** — call variants on whole-genome (WGS) or whole-exome
  (WES) short reads.
- Run **germline** SNV/indel calling (one or many normal samples).
- Run **somatic / tumor-normal** calling (matched tumor + normal, or tumor-only).
- Use **nf-core/sarek** specifically, or want a reproducible "GATK
  best-practices alignment-to-VCF" pipeline without hand-writing every step.
- Resume a run from an intermediate **`--step`** (already have BAM/CRAM, only need
  recalibration or variant calling).

### Does NOT Trigger — route adjacent requests here

| The request is really about… | Route to |
|---|---|
| Parsing / filtering / reading an **existing** VCF/BAM in Python (pysam/htslib) | `alterlab-pysam` |
| **Storing / querying** large multi-sample variant stores (TileDB-VCF arrays) | `alterlab-tiledbvcf` |
| Clinical significance of a called variant (pathogenic/benign) | `alterlab-clinvar` |
| Population allele frequencies for a called variant | `alterlab-gnomad` |
| Somatic mutation catalogue / cancer census lookup | `alterlab-cosmic` |
| **RNA-seq** transcript/gene quantification (salmon/kallisto), not DNA variants | `alterlab-rnaseq-quant` |
| 16S/ITS **amplicon / microbiome** FASTQ → feature table | `alterlab-qiime2-amplicon` |
| Sequence **homology / similarity search** (BLAST+, DIAMOND) | `alterlab-blast` |
| Spatial transcriptomics neighborhood/SVG analysis | `alterlab-squidpy-spatial` |
| Differential **expression** stats from counts | `alterlab-pydeseq2` |

If the user has no workflow engine and cannot install Nextflow + containers,
do **not** refuse — fall back to the **manual GATK4 recipe** (below /
`references/manual_gatk4.md`).

## The #1 Correctness Trap: sarek's default caller is Strelka

Per the [3.8.1 usage docs](https://nf-co.re/sarek/3.8.1/docs/usage/), **when
`--tools` is not set, sarek runs preprocessing and then Strelka only.** It does
**not** default to GATK HaplotypeCaller or DeepVariant. Always set `--tools`
explicitly to match the user's intent:

| Intent | Pass |
|---|---|
| GATK4 best-practice germline | `--tools haplotypecaller` |
| Highest germline F1 (CNN) | `--tools deepvariant` |
| Somatic, matched tumor/normal | `--tools mutect2` (often `mutect2,strelka`) |
| Joint germline genotyping across a cohort | `--tools haplotypecaller --joint_germline` |

`--tools` accepts (per the docs' tool matrix): `deepvariant`, `freebayes`,
`haplotypecaller`, `mutect2`, `lofreq`, `mpileup`, `strelka` (and annotation
tools). Caller choice materially changes precision/recall — see
`references/caller_accuracy.md` for the nf-core benchmark (Hanssen et al., 2024).

## Pipeline (how to run it)

### 1. Build the samplesheet

sarek's input is a CSV. Required columns for `--step mapping`:
`patient`, `sample`, `lane`, `fastq_1`, `fastq_2`. Optional: `sex` (XX/XY,
default NA) and `status` (**`0` = normal, `1` = tumor**, default 0) — `status`
is what tells sarek a pair is somatic.

Use the helper to generate a valid sheet from a FASTQ directory (it pairs R1/R2,
fills `lane`, and validates the schema before you burn compute):

```bash
uv run python skills/bioinformatics/alterlab-nf-core-sarek/scripts/make_samplesheet.py \
    --fastq-dir ./fastq --patient PATIENT_01 --sample TUMOR_01 \
    --status 1 --sex XY --out samplesheet.csv
```

Append more rows (e.g. the matched normal with `--status 0 --append`) before
running. See `references/samplesheet_schema.md` for every column, BAM/CRAM
re-entry rows, and a tumor-normal example.

### 2. Run the pipeline (pinned)

```bash
nextflow run nf-core/sarek -r 3.8.1 \
    -profile docker \
    --input samplesheet.csv \
    --outdir ./results \
    --genome GATK.GRCh38 \
    --tools haplotypecaller \
    --aligner bwa-mem2
```

- **Always keep `-r 3.8.1`** — unpinned runs drift to a different pipeline version.
- `-profile` is **mandatory**: `docker`, `singularity`, `apptainer`, or `conda`
  for the local environment (clusters add `test`, institutional configs, etc.).
- `--genome GATK.GRCh38` selects the iGenomes/GATK GRCh38 reference and its
  bundled BQSR known-sites (dbSNP, Mills/1000G indels) automatically.
- `--aligner` options: `bwa-mem` (default), `bwa-mem2`, `dragmap`.
- For **WES**, pass `--intervals targets.bed` with the capture-kit BED (there is
  no `--wes` flag in 3.8.1; restrict to target regions via `--intervals`).
- Resume mid-pipeline with `--step` (`mapping` default, then `markduplicates`,
  `prepare_recalibration`, `recalibrate`, `variant_calling`, `annotate`) and
  Nextflow's `-resume`.

Preprocessing follows GATK best practice: align → **MarkDuplicates** →
**BaseRecalibrator/ApplyBQSR** (BQSR) → variant calling. Details and every flag:
`references/usage_3.8.1.md`.

### 3. Interpret the output VCFs

Per-caller VCFs land under `results/variant_calling/<tool>/`. Then:

- **Parse / filter** with `alterlab-pysam`.
- **Store / query at scale** (multi-sample) with `alterlab-tiledbvcf`.
- **Annotate** clinical significance → `alterlab-clinvar`; population frequency →
  `alterlab-gnomad`; somatic catalogue → `alterlab-cosmic`.

### Fallback: manual GATK4 (no Nextflow)

If the user cannot run Nextflow + containers, run the equivalent GATK4
best-practices chain by hand: `bwa-mem2 mem` → `gatk MarkDuplicates` →
`gatk BaseRecalibrator` + `gatk ApplyBQSR` (with dbSNP + Mills/1000G known
sites) → `gatk HaplotypeCaller -ERC GVCF` → `gatk GenotypeGVCFs`. Full command
sequence and the resource-bundle paths are in `references/manual_gatk4.md`.

## Self-Check Before Reporting

- Is `--tools` set explicitly? Never let a run fall through to the **Strelka**
  default unless the user truly wants Strelka.
- Is the version pinned (`-r 3.8.1`) and a `-profile` chosen?
- For somatic asks, does the samplesheet carry a `status 1` tumor **and** a
  `status 0` normal under the **same `patient`**?
- For WES, was `--intervals` supplied with the capture BED?
- After the run, did you route VCF interpretation to the correct sibling skill
  rather than re-deriving variant meaning here?

## References

- `references/usage_3.8.1.md` — pinned run command, profiles, `--step`/`--aligner`
  options, BQSR preprocessing, sourced from the 3.8.1 usage docs.
- `references/samplesheet_schema.md` — full CSV column spec, BAM/CRAM re-entry,
  tumor-normal worked example.
- `references/caller_accuracy.md` — choosing `--tools`, summarizing the nf-core
  benchmark (Hanssen et al., 2024, NAR Genomics & Bioinformatics).
- `references/manual_gatk4.md` — the non-Nextflow GATK4 best-practices fallback.

Part of the AlterLab Academic Skills suite.
