# kallisto & kb-python (pseudoalignment path)

Targets standalone kallisto **v0.52.0** and kb-python (the `kb` CLI). See
../references/tool_versions.md for the version facts.

## Plain kallisto

```bash
# index
kallisto index -i kallisto_index.idx transcripts.fa

# paired-end quant
kallisto quant -i kallisto_index.idx -o quants_kallisto/sampleA \
  sampleA_R1.fastq.gz sampleA_R2.fastq.gz

# single-end (must supply fragment length mean/SD)
kallisto quant -i kallisto_index.idx -o quants_kallisto/sampleA \
  --single -l 200 -s 20 sampleA.fastq.gz
```

Outputs per sample: `abundance.tsv` (`target_id`, `length`, `eff_length`,
`est_counts`, `tpm`), `abundance.h5`, and `run_info.json`. Feed `abundance.h5`
(or `abundance.tsv`) to `tximport` with `type="kallisto"`.

## kb-python (`kb`) — wraps kallisto | bustools

```bash
# build references (index + t2g) from a GENOME FASTA + GTF
# positional order: <GENOME_FASTA> <GTF> (genome first, annotation second)
kb ref -i index.idx -g t2g.txt -f1 cdna.fa genome.fa annotation.gtf

# bulk quantification
kb count -i index.idx -g t2g.txt -x bulk -o quants_kb/sampleA \
  sampleA_R1.fastq.gz sampleA_R2.fastq.gz
```

- `kb ref` extracts the cDNA from the genome+GTF, builds the kallisto index, and
  writes the transcript-to-gene map (`t2g.txt`) in one step.
- `-f1 cdna.fa` is the **output** cDNA FASTA that `kb ref` writes (not an input
  transcriptome). The two trailing positionals are the genome FASTA **then** the
  GTF — genome first, in that order.
- `-x` is the technology string; `bulk` for bulk RNA-seq.
- kb-python emits tidy count outputs and a run log.

## Long reads (lr-kallisto)

kb-python exposes **lr-kallisto** through the `--long` flag and supports k-mer
sizes greater than 31, for long-read cDNA (ONT/PacBio). kb-python v0.29.1
introduced this option. Use it instead of the short-read defaults for long-read
libraries; consult `kb count --help` in your installed version for the exact
`--long` usage and the recommended `-k`.

## Notes

- kallisto/kb does **not** use the salmon gentrome/decoy construction — that is
  salmon-specific. A plain transcriptome index is correct here.
- The bundled kallisto inside a given kb-python build may lag the standalone
  kallisto release; check your install.
- Downstream, kallisto output aggregates to gene level via `tximport`
  identically to salmon — see ../references/tximport_handoff.md — then hand the
  gene matrix to `alterlab-pydeseq2`.
