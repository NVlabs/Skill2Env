# nf-core/sarek 3.8.1 — Samplesheet (`--input`) Schema

Source: https://nf-co.re/sarek/3.8.1/docs/usage/. The input is a comma-separated
CSV with a header row. Columns depend on the `--step` you start from.

## Columns for `--step mapping` (FASTQ entry)

| Column | Required | Meaning |
|---|---|---|
| `patient` | yes | Subject identifier. Tumor and matched normal share the **same** `patient`. |
| `sample` | yes | Biological sample identifier (unique per sample). |
| `lane` | yes (mapping) | Sequencing lane/run identifier; lets sarek track read groups and merge lanes. |
| `fastq_1` | yes | Path to the R1 gzipped FASTQ. |
| `fastq_2` | yes (paired-end) | Path to the R2 gzipped FASTQ. |
| `sex` | optional | `XX` / `XY` (default `NA`). |
| `status` | optional | **`0` = normal, `1` = tumor** (default `0`). Drives somatic pairing. |

### Germline example (single normal sample)

```csv
patient,sex,status,sample,lane,fastq_1,fastq_2
PATIENT_01,XY,0,NORMAL_01,L001,/data/N_R1.fastq.gz,/data/N_R2.fastq.gz
```

### Somatic example (matched tumor + normal, same patient)

```csv
patient,sex,status,sample,lane,fastq_1,fastq_2
PATIENT_01,XY,0,NORMAL_01,L001,/data/N_R1.fastq.gz,/data/N_R2.fastq.gz
PATIENT_01,XY,1,TUMOR_01,L001,/data/T_R1.fastq.gz,/data/T_R2.fastq.gz
```

The tumor row (`status 1`) plus a normal row (`status 0`) under one `patient` is
what makes the run somatic. Run with `--tools mutect2` (or `mutect2,strelka`).
For **tumor-only** somatic calling, include only the `status 1` row.

### Multiple lanes

Repeat the sample with different `lane` values; sarek aligns each lane and merges:

```csv
patient,sex,status,sample,lane,fastq_1,fastq_2
PATIENT_01,XY,0,NORMAL_01,L001,/data/N_L001_R1.fastq.gz,/data/N_L001_R2.fastq.gz
PATIENT_01,XY,0,NORMAL_01,L002,/data/N_L002_R1.fastq.gz,/data/N_L002_R2.fastq.gz
```

## Re-entry rows (resuming with `--step`)

When you already have aligned/recalibrated data, the FASTQ columns are replaced
by alignment columns and you pick the matching `--step`:

- **BAM/CRAM re-entry** (`--step markduplicates` / `prepare_recalibration` /
  `recalibrate` / `variant_calling`): provide `bam`/`bai` or `cram`/`crai`
  (and, for the recalibration steps, the BQSR `table`) instead of
  `fastq_1`/`fastq_2`.
- **VCF re-entry** (`--step annotate`): provide a `vcf` column.

Consult the 3.8.1 usage docs for the exact column set required by each step; the
helper script (`scripts/make_samplesheet.py`) writes the FASTQ-entry sheet for
`--step mapping`, which is the common starting point.

## Common mistakes

- Putting tumor and normal under **different** `patient` IDs → sarek treats them
  as unrelated germline samples and never does somatic calling.
- Omitting `lane` for `--step mapping` (it is required there).
- Leaving `--tools` unset and assuming GATK ran — it ran **Strelka** by default
  (see `caller_accuracy.md`).
