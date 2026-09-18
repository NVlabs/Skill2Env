# Manual GATK4 fallback (no Nextflow)

Use this when the user cannot run Nextflow + a container engine. It reproduces
the **same GATK best-practices preprocessing chain** that sarek automates, using
the GATK4 CLI directly. It is more error-prone and you must manage references
yourself — prefer the pipeline when available.

Sources: GATK Best Practices "Data pre-processing for variant discovery"
(https://gatk.broadinstitute.org/hc/en-us/articles/360035535912) and the
germline short-variant discovery best-practice (HaplotypeCaller in GVCF mode →
GenotypeGVCFs). The known-sites resources match those the sarek 3.8.1 GATK genome
key uses (dbSNP + Mills/1000G gold-standard indels).

## Tools needed (bioconda)

`bwa-mem2`, `samtools`, `gatk4`. Install in an isolated env (e.g. conda/mamba);
these run offline once the reference and known-sites are local.

## Reference inputs

- `ref.fasta` — GRCh38 reference (with `.fai` and `.dict`).
- `dbsnp.vcf.gz` — dbSNP known sites.
- `mills_1000G.indels.vcf.gz` — Mills and 1000G gold-standard indels.

All three are in the Broad GATK resource bundle for hg38
(`genomics-public-data/resources/broad/hg38/v0/`).

## Germline single-sample chain

```bash
# 0. Index the reference for bwa-mem2 (once)
bwa-mem2 index ref.fasta

# 1. Align (set a read group; required downstream)
bwa-mem2 mem -t 8 -R '@RG\tID:L001\tSM:NORMAL_01\tPL:ILLUMINA\tLB:lib1' \
    ref.fasta R1.fastq.gz R2.fastq.gz \
  | samtools sort -@ 8 -o aligned.bam -
samtools index aligned.bam

# 2. Mark duplicates
gatk MarkDuplicates -I aligned.bam -O markdup.bam -M markdup.metrics.txt
samtools index markdup.bam

# 3. BQSR — build the recalibration table from known sites
gatk BaseRecalibrator \
    -I markdup.bam -R ref.fasta \
    --known-sites dbsnp.vcf.gz \
    --known-sites mills_1000G.indels.vcf.gz \
    -O recal.table

# 4. BQSR — apply it
gatk ApplyBQSR -I markdup.bam -R ref.fasta --bqsr-recal-file recal.table -O recal.bam
samtools index recal.bam

# 5. Call per-sample variants in GVCF mode
gatk HaplotypeCaller -I recal.bam -R ref.fasta -ERC GVCF -O sample.g.vcf.gz

# 6. Genotype to a final VCF (single-sample shortcut)
gatk GenotypeGVCFs -R ref.fasta -V sample.g.vcf.gz -O sample.vcf.gz
```

## Joint genotyping (cohort)

Produce one `*.g.vcf.gz` per sample (steps 1–5), then combine and joint-genotype:

```bash
gatk CombineGVCFs -R ref.fasta -V a.g.vcf.gz -V b.g.vcf.gz -O cohort.g.vcf.gz
gatk GenotypeGVCFs -R ref.fasta -V cohort.g.vcf.gz -O cohort.vcf.gz
```

(For large cohorts the best-practice path uses `GenomicsDBImport` instead of
`CombineGVCFs`; consult the GATK docs.)

## WES

Restrict every region-aware step with `-L targets.bed` (the capture-kit BED) —
the manual analogue of sarek's `--intervals`.

## After the VCF

Hand off exactly as with the pipeline: `alterlab-pysam` (parse/filter),
`alterlab-tiledbvcf` (store/query), `alterlab-clinvar` / `alterlab-gnomad` /
`alterlab-cosmic` (annotate).

> Caveat: command flags can change between GATK4 minor versions. Verify against
> `gatk <Tool> --help` for the installed version before running on real data.
