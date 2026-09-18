# Coverage / Accumulation Tracks (uniwig)

The `uniwig` module turns a sorted BED or BAM file into accumulation / coverage
tracks. In v0.8 it is exposed through the **CLI only** (requires the `uniwig`
feature); there is no `gtars.uniwig` Python module.

## CLI usage

`uniwig` is a single subcommand (no `generate` sub-subcommand). Its real flags
include `--file`, `--filetype`, `--chromref`, `--fileheader`, `--outputtype`,
`--counttype`, `--smoothsize`, `--stepsize`, `--threads`, and others. Flag values
(e.g. accepted output types) vary by version, so confirm with `--help`:

```bash
gtars uniwig --help
```

Typical invocation (sorted BED input, BigWig-style output prefix):

```bash
gtars uniwig --file fragments.bed \
             --filetype bed \
             --fileheader coverage \
             --outputtype bw \
             --smoothsize 25 \
             --stepsize 1
```

- `--file` / `--filetype` — input path and `bed` or `bam`
- `--fileheader` — output file prefix
- `--outputtype` — output format/style (see `--help` for accepted values)
- `--smoothsize` / `--stepsize` — smoothing window and resolution
- uniwig can emit start/end/core accumulation tracks; consult `--help` for the
  exact set produced by your version

> Input BED/BAM should be coordinate-sorted. uniwig is built for ATAC-seq /
> ChIP-seq accumulation tracks for genome-browser visualization.

## Python alternative: covered base pairs

For a quick in-memory measure (not a browser track), `RegionSet.get_nucleotide_length()`
returns the total number of base pairs covered by a region set:

```python
from gtars.models import RegionSet

regions = RegionSet("atac_fragments.bed")
covered_bp = regions.get_nucleotide_length()
```

Note: `RegionSet.coverage(other)` is a *fraction* between two sets (how much of one
is covered by the other), not a per-position profile and not a single-set total.
For tracks to load into IGV/UCSC, use the `uniwig` CLI above.

## Use cases

### ATAC-seq accessibility track

```bash
gtars uniwig --file atac_fragments.bed --filetype bed \
             --fileheader atac --outputtype bw
```

### ChIP-seq coverage from aligned reads

```bash
gtars uniwig --file chip.bam --filetype bam \
             --fileheader chip --outputtype bw
```

## Performance notes

- BigWig output is recommended for large datasets and genome browsers.
- Use `--threads` to parallelize across chromosomes.
- Keep input sorted to avoid an extra sort pass.
