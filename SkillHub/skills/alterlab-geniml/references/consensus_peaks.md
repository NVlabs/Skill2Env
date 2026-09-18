# Consensus Peaks: Universe Building

## Overview

Geniml provides tools for building genomic "universes" — standardized reference sets of consensus peaks from collections of BED files. These universes represent genomic regions where analyzed datasets show significant coverage overlap, serving as reference vocabularies for tokenization and analysis.

## When to Use

Use consensus peak creation when:
- Building reference peak sets from multiple experiments
- Creating universe files for Region2Vec or BEDspace tokenization
- Standardizing genomic regions across a collection of datasets
- Defining regions of interest with statistical significance

## Workflow

### Step 1: Combine BED Files

Merge all BED files into a single combined file:

```bash
cat /path/to/bed/files/*.bed > combined_files.bed
```

### Step 2: Generate Coverage Tracks

Create bigWig coverage tracks using uniwig with a smoothing window:

```bash
uniwig -m 25 combined_files.bed chrom.sizes coverage/
```

**Parameters:**
- `-m 25`: Smoothing window size (25bp typical for chromatin accessibility)
- `chrom.sizes`: Chromosome sizes file for your genome
- `coverage/`: Output directory for bigWig files

The smoothing window helps reduce noise and creates more robust peak boundaries.

### Step 3: Build Universe

Use one of four methods to construct the consensus peaks:

## Universe-Building Methods

### 1. Coverage Cutoff (CC)

The simplest approach using a fixed coverage threshold:

The top-level command is `geniml build-universe`, with the method (`cc`/`ccf`/`ml`/`hmm`) as a subcommand. Verified `cc` flags: `--coverage-folder`, `--output-file`, `--coverage-prefix`, `--merge`, `--filter-size`, `--cutoff`.

```bash
geniml build-universe cc \
  --coverage-folder coverage/ \
  --output-file universe_cc.bed \
  --cutoff 5 \
  --merge 100 \
  --filter-size 50
```

**Parameters:**
- `--cutoff`: Coverage threshold (1 = union; file count = intersection)
- `--merge`: Distance for merging adjacent peaks (bp)
- `--filter-size`: Minimum peak size for inclusion (bp)

**Use when:** Simple threshold-based selection is sufficient

### 2. Coverage Cutoff Flexible (CCF)

Adds flexibility around the cutoff for region boundaries and cores:

```bash
geniml build-universe ccf \
  --coverage-folder coverage/ \
  --output-file universe_ccf.bed \
  --merge 100 \
  --filter-size 50
```

**Use when:** Uncertainty in peak boundaries should be captured. Run `geniml build-universe ccf --help` for its exact flags.

### 3. Maximum Likelihood (ML)

Builds probabilistic models accounting for region start/end positions. The ML universe is fit against a likelihood model:

```bash
geniml build-universe ml \
  --coverage-folder coverage/ \
  --output-file universe_ml.bed \
  --model-file model.tar \
  --merge 100 \
  --filter-size 50
```

**Use when:** Statistical modeling of peak locations is important. (Build the likelihood model first via `geniml lh`; see `geniml build-universe ml --help`.)

### 4. Hidden Markov Model (HMM)

Models genomic regions as hidden states with coverage as emissions:

```bash
geniml build-universe hmm \
  --coverage-folder coverage/ \
  --output-file universe_hmm.bed \
  --merge 100 \
  --filter-size 50
```

**Use when:** Complex patterns of genomic states should be captured. Run `geniml build-universe hmm --help` for its exact flags.

## API note

Universe building is driven through the CLI (`geniml build-universe ...`); there is no stable top-level `geniml.universe.build_universe` function to import. Invoke the CLI from Python with `subprocess` if you need to script it.

## Method Comparison

| Method | Complexity | Flexibility | Computational Cost | Best For |
|--------|------------|-------------|-------------------|----------|
| CC | Low | Low | Low | Quick reference sets |
| CCF | Medium | Medium | Medium | Boundary uncertainty |
| ML | High | High | High | Statistical rigor |
| HMM | High | High | Very High | Complex patterns |

## Best Practices

### Choosing a Method

1. **Start with CC**: Quick and interpretable for initial exploration
2. **Use CCF**: When peak boundaries are uncertain or noisy
3. **Apply ML**: For publication-quality statistical analysis
4. **Deploy HMM**: When modeling complex chromatin states

### Parameter Selection

**Coverage cutoff:**
- `cutoff = 1`: Union of all peaks (most permissive)
- `cutoff = n_files`: Intersection (most stringent)
- `cutoff = 0.5 * n_files`: Moderate consensus (typical choice)

**Merge distance:**
- ATAC-seq: 100-200bp
- ChIP-seq (narrow peaks): 50-100bp
- ChIP-seq (broad peaks): 500-1000bp

**Filter size:**
- Minimum 30bp to avoid artifacts
- 50-100bp typical for most assays
- Larger for broad histone marks

### Quality Control

After building, assess universe quality with the `assess-universe` CLI command (it reports fit metrics between the universe and the input coverage/regions):

```bash
geniml assess-universe --help   # inspect available metrics/flags for your version
```

**Key metrics to look at:**
- **Region count**: Should capture major features without excessive fragmentation
- **Size distribution**: Should match expected biology (e.g., ~500bp for ATAC-seq)
- **Input coverage**: Proportion of original peaks represented (typically >80%)

## Output Format

Consensus peaks are saved as BED files with three required columns:

```
chr1    1000    1500
chr1    2000    2800
chr2    500     1000
```

Additional columns may include confidence scores or state annotations depending on the method.

## Common Workflows

### For Region2Vec

1. Build universe using preferred method
2. Use universe as tokenization reference
3. Tokenize BED files
4. Train Region2Vec model

### For BEDspace

1. Build universe from all datasets
2. Use universe in preprocessing step
3. Train BEDspace with metadata
4. Query across regions and labels

### For scEmbed

1. Create universe from bulk or aggregated scATAC-seq
2. Use for cell tokenization
3. Train scEmbed model
4. Generate cell embeddings

## Troubleshooting

**Too few regions:** Lower cutoff threshold or reduce filter size

**Too many regions:** Raise cutoff threshold, increase merge distance, or increase filter size

**Noisy boundaries:** Use CCF or ML methods instead of CC

**Long computation:** Start with CC method for quick results, then refine with ML/HMM if needed
