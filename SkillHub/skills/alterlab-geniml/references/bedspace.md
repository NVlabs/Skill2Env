# BEDspace: Joint Region and Metadata Embeddings

## Overview

BEDspace applies the StarSpace model to genomic data, enabling simultaneous training of numerical embeddings for both region sets and their metadata labels in a shared low-dimensional space. This allows for rich queries across regions and metadata.

## When to Use

Use BEDspace when working with:
- Region sets with associated metadata (cell types, tissues, conditions)
- Search tasks requiring metadata-aware similarity
- Cross-modal queries (e.g., "find regions similar to label X")
- Joint analysis of genomic content and experimental conditions

## Workflow

BEDspace consists of four sequential operations:

### 1. Preprocess

Format genomic intervals and metadata for StarSpace training:

```bash
geniml bedspace preprocess \
  --input /path/to/regions/ \
  --metadata labels.csv \
  --universe universe.bed \
  --labels "cell_type,tissue" \
  --output preprocessed.txt
```

**Required files:**
- **Input folder**: Directory containing BED files
- **Metadata CSV**: Must include `file_name` column matching BED filenames, plus metadata columns
- **Universe file**: Reference BED file for tokenization
- **Labels**: Comma-separated list of metadata columns to use

The preprocessing step adds `__label__` prefixes to metadata and converts regions to StarSpace-compatible format.

### 2. Train

Execute StarSpace model on preprocessed data:

The StarSpace path flag is `-s` / `--path-to-starsapce` (the geniml CLI literally misspells "starspace" as "starsapce"). Verified flags: `-s`, `-i/--input`, `-n/--epochs`, `-d/--dim`, `-l/--lr`, `-o/--output`.

```bash
geniml bedspace train \
  -s /path/to/starspace \
  --input preprocessed.txt \
  --output model/ \
  --dim 100 \
  --epochs 50 \
  --lr 0.05
```

**Key training parameters:**
- `--dim`: Embedding dimension (typical: 50-200)
- `--epochs`: Training epochs (typical: 20-100)
- `--lr`: Learning rate (typical: 0.01-0.1)

### 3. Distances

Compute distances between region sets and labels. This command takes the trained model (`-i`), the StarSpace path (`-s`), train/test metadata (`--metadata-train` / `--metadata-test`), the universe, the data files (`-f`), and the label string (`-l`):

```bash
geniml bedspace distances \
  -i model/ \
  -s /path/to/starspace \
  --metadata-train train.csv \
  --metadata-test test.csv \
  -u universe.bed \
  -f regions/ \
  -l "cell_type" \
  -o distances/
```

This step creates the distance data needed for similarity searches.

### 4. Search

Retrieve similar items across three scenarios. **The query is a positional argument (last), not a `-q` flag.** `-t` is the search type, `-d` the distances file, `-n` the number of results.

**Region-to-Label (r2l)**: query region set → similar metadata labels
```bash
geniml bedspace search -t r2l -d distances.pkl -n 10 query_regions.bed
```

**Label-to-Region (l2r)**: query metadata label → similar region sets
```bash
geniml bedspace search -t l2r -d distances.pkl -n 10 "T_cell"
```

**Region-to-Region (r2r)**: query region set → similar region sets
```bash
geniml bedspace search -t r2r -d distances.pkl -n 10 query_regions.bed
```

## API note

BEDspace is driven entirely through the `geniml bedspace` CLI (it orchestrates the external StarSpace binary). There is no public `BEDSpaceModel` Python class to import; script the workflow via `subprocess` if needed.

## Best Practices

- **Metadata structure**: Ensure metadata CSV includes `file_name` column that exactly matches BED filenames (without path)
- **Label selection**: Choose informative metadata columns that capture biological variation of interest
- **Universe consistency**: Use the same universe file across preprocessing, distances, and any subsequent analyses
- **Validation**: Preprocess and check output format before investing in training
- **StarSpace installation**: Install StarSpace separately as it's an external dependency

## Output Interpretation

Search results return items ranked by similarity in the joint embedding space:
- **r2l**: Identifies metadata labels characterizing your query regions
- **l2r**: Finds region sets matching your metadata criteria
- **r2r**: Discovers region sets with similar genomic content

## Requirements

BEDspace requires StarSpace to be installed separately. Download from: https://github.com/facebookresearch/StarSpace
