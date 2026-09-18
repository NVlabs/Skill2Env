# Python API Reference

Reference for the `gtars` Python bindings, verified against **v0.8**.

> The public API lives in submodules, not flat on `gtars`:
> `gtars.models` (intervals), `gtars.tokenizers`, `gtars.refget`, `gtars.utils`.
> Method names below were confirmed by introspection on v0.8; confirm against your
> installed version with `dir(...)` if a call is missing.

## Installation

```bash
uv pip install gtars        # or: uv add gtars
```

## RegionSet

`RegionSet` (in `gtars.models`) holds a collection of genomic intervals. Construct it from a path to a BED file, or from parallel vectors / a list of `Region` objects.

```python
from gtars.models import RegionSet, Region

# From a BED file (positional path argument)
regions = RegionSet("regions.bed")

# From parallel vectors (starts/ends are 0-based, half-open)
regions = RegionSet.from_vectors(
    ["chr1", "chr1", "chr2"],
    [1000, 3000, 5000],
    [2000, 4000, 6000],
)

# From a list of Region objects (Region signature: chr, start, end, rest)
regions = RegionSet.from_regions(
    [Region("chr1", 1000, 2000, None), Region("chr2", 5000, 6000, None)]
)

# Length, iteration, identity
n = len(regions)
for r in regions:
    print(r.chr, r.start, r.end, r.rest)

print(regions.path)         # source path, if loaded from a file
print(regions.identifier()) # content-based identifier (BEDbase-style digest)
print(regions.is_empty())
```

### Region

A single interval. The constructor takes four positional args; the fourth (`rest`) holds any extra BED columns and may be `None`.

```python
r = Region("chr1", 1000, 2000, None)
r.chr, r.start, r.end, r.rest
```

## Region operations

```python
regions.sort()                        # sorts IN PLACE, returns None
merged = regions.reduce()             # new RegionSet: merge overlapping/adjacent
disjoint = regions.disjoin()          # new RegionSet: split into non-overlapping pieces
trimmed = regions.trim(chrom_sizes)   # clamp to chromosome bounds (needs chrom sizes)

widths = regions.widths()             # list of per-region widths
mean_w = regions.mean_region_width()
total_bp = regions.get_nucleotide_length()   # total covered base pairs
stats = regions.chromosome_statistics()
```

> `sort()` mutates the set in place and returns `None` — do not write
> `x = regions.sort()`.

## Set operations

All operate between two `RegionSet`s and return a new `RegionSet`.

```python
set_a = RegionSet("set_a.bed")
set_b = RegionSet("set_b.bed")

union = set_a.union(set_b)
intersection = set_a.intersect_all(set_b)   # intersection of the two sets
difference = set_a.subtract(set_b)          # A minus B (per-base)
only_a = set_a.setdiff(set_b)               # regions of A with no B overlap
```

## Overlap detection

```python
set_a = RegionSet("regions_a.bed")
set_b = RegionSet("regions_b.bed")

# Per-region results, aligned to set_a's order:
set_a.any_overlaps(set_b)     # -> [True, False, ...]
set_a.count_overlaps(set_b)   # -> [1, 0, ...] overlap count per region
set_a.find_overlaps(set_b)    # -> [[idx,...], [], ...] indices into set_b

# Keep only regions of A that overlap B (the "filter overlapping" operation):
overlapping_a = set_a.subset_by_overlaps(set_b)

# Per-region intersection geometry:
clipped = set_a.pintersect(set_b)
```

## Similarity metrics

```python
set_a.jaccard(set_b)             # Jaccard index of the two interval sets
set_a.overlap_coefficient(set_b) # overlap coefficient
set_a.coverage(set_b)            # coverage fraction of set_a covered by set_b

# Total covered base pairs of a single set:
set_a.get_nucleotide_length()
```

## Nearest-neighbour / distance

```python
set_a.closest(set_b)            # nearest region in B for each region in A
set_a.nearest_neighbors(set_b)
set_a.neighbor_distances(set_b)
```

## Export

```python
regions.to_bed("output.bed")          # write BED
regions.to_bed_gz("output.bed.gz")    # gzipped BED
regions.to_bigbed("output.bb", "chrom.sizes")  # BigBed (needs chrom sizes)
```

`RegionSet` also exposes `header()`, `strands()`, `region_widths()`,
`get_max_end_per_chr()`, `promoters()`, `cluster()`, and `distribution()`.
Use `dir(RegionSet)` to enumerate the full set for your version.

## Working with many region sets

`RegionSetList` (also in `gtars.models`) holds multiple `RegionSet`s for batch
operations; `concat` joins region sets. See `dir(RegionSet)` / `dir(RegionSetList)`.

## Tokens on disk

`gtars.utils` reads/writes the `.gtok` binary token format used by the tokenizers:

```python
from gtars.utils import write_tokens_to_gtok, read_tokens_from_gtok

write_tokens_to_gtok("regions.gtok", [0, 2, 5])
ids = read_tokens_from_gtok("regions.gtok")
```

## Performance tips

- Sort/`reduce` region sets before repeated overlap queries.
- For repeated overlap queries against a large fixed database, build an IGD index
  with the CLI (`gtars igd create`) rather than reloading BED files.
- Coordinates are 0-based, half-open `[start, end)` throughout.
