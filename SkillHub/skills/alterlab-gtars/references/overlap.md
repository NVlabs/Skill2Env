# Overlap Detection and IGD

Two ways to detect overlaps in gtars:

1. **`RegionSet` overlap methods (Python)** — best for one or a few region-set
   comparisons in an analysis pipeline.
2. **IGD indexing (CLI)** — best when you query one large reference database many
   times. IGD (Integrated Genome Database) is a Rust data structure; in v0.8 it is
   exposed through the **CLI only** (`gtars igd ...`), not a `gtars.igd` Python module.

## Python: RegionSet overlaps

```python
from gtars.models import RegionSet

set_a = RegionSet("regions_a.bed")
set_b = RegionSet("regions_b.bed")

# Per-region results, aligned to set_a's order
set_a.any_overlaps(set_b)     # [True, False, ...]
set_a.count_overlaps(set_b)   # [1, 0, ...]
set_a.find_overlaps(set_b)    # [[idx into b, ...], [], ...]

# Keep regions of A that overlap B (returns a RegionSet)
overlapping_a = set_a.subset_by_overlaps(set_b)

# Regions of A with NO overlap in B
non_overlapping_a = set_a.setdiff(set_b)
```

### Similarity

```python
set_a.jaccard(set_b)             # Jaccard index
set_a.overlap_coefficient(set_b) # overlap coefficient
```

## CLI: IGD index

IGD subcommands (require the `igd` feature). The two operations are `create` and
`search` — confirm exact flags for your version with `--help`, as they vary.

```bash
# Build an IGD database (typically from a directory of BED files)
gtars igd create --help

# Search the database with query regions
gtars igd search --help
```

## CLI: overlaprs

The `overlaprs` subcommand (requires the `overlaprs` feature) does pairwise BED
overlap from the command line:

```bash
gtars overlaprs --help
```

## Performance characteristics

- IGD trades a one-time index build for fast repeated queries — index once,
  search many times.
- `RegionSet` overlap methods sort internally; pre-sorting and `reduce()`-merging
  inputs reduces redundant work for large sets.

## Use cases

### Regulatory element analysis

```python
from gtars.models import RegionSet

tfbs = RegionSet("chip_seq_peaks.bed")
promoters = RegionSet("promoters.bed")

overlapping_tfbs = tfbs.subset_by_overlaps(promoters)
print(f"Found {len(overlapping_tfbs)} TFBS in promoters")
```

### Variant annotation

```python
variants = RegionSet("variants.bed")
cds = RegionSet("coding_sequences.bed")

coding_variants = variants.subset_by_overlaps(cds)
```

### Sample similarity

```python
sample1 = RegionSet("sample1_peaks.bed")
sample2 = RegionSet("sample2_peaks.bed")

print(sample1.jaccard(sample2))   # how similar the two peak sets are
```
