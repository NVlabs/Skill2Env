# Decoy-aware salmon index (gentrome)

## Why decoys

Selective alignment scores how well a read maps to the transcriptome. Some reads
actually originate from intronic / intergenic genomic sequence and would
otherwise be force-assigned to a transcript. Including the **genome as a decoy**
lets salmon recognize "this read aligns better to the genome than to any
transcript" and decline the spurious transcript assignment. This is the
recommended construction for accurate bulk quantification.

## Construction

A **gentrome** is the transcripts FASTA concatenated with the genome FASTA. The
`decoys.txt` file lists the genome sequence (chromosome/scaffold) names so salmon
knows which gentrome entries are decoys.

```bash
# decoys = the genome's sequence names (strip '>' and any description after a space)
grep "^>" genome.fa | sed 's/^>//; s/ .*//' > decoys.txt

# gentrome: transcripts FIRST, then genome (order matters — decoys go last)
cat transcripts.fa genome.fa > gentrome.fa

salmon index -t gentrome.fa -d decoys.txt -i salmon_index -k 31 -p 8
```

### Gotchas

- **Order matters.** Transcripts must come before the genome in the gentrome;
  `decoys.txt` names must match the genome FASTA headers exactly.
- **Header trimming.** Many genome FASTAs have headers like
  `>1 dna:chromosome ...`; the `sed 's/ .*//'` keeps only `1`. salmon matches on
  the first whitespace-delimited token, so trim consistently.
- **Rebuild for v1.11.4.** The SSHash index format means any pre-v1.11.2 index is
  invalid — rebuild (see ../references/tool_versions.md).
- Use a transcriptome FASTA and genome from the **same assembly/annotation
  release** (e.g. matching Ensembl/GENCODE versions). Fetch references with
  `alterlab-gget` if needed.

## Helper

`scripts/make_decoys.py` automates the two derived files and adds a guard: it
extracts genome names into `decoys.txt`, concatenates the gentrome in the correct
order, and warns if the transcript and genome FASTAs look swapped or empty. It
shells out nothing — pure stdlib file IO — so it runs in a bare `uv` env.

```bash
uv run python scripts/make_decoys.py \
  --transcripts transcripts.fa \
  --genome genome.fa \
  --out-gentrome gentrome.fa \
  --out-decoys decoys.txt
```

Then run `salmon index -t gentrome.fa -d decoys.txt -i salmon_index`.
