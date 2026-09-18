# Command-Line Interface

The gtars CLI is the `gtars-cli` crate (binary name `gtars`), separate from the
Python package. Subcommand availability depends on the Cargo features compiled in,
and exact flag sets evolve across versions — **always confirm with
`gtars <command> --help`**. Subcommand names below verified against the v0.8 CLI.

## Installation

```bash
# Common feature set
cargo install gtars-cli --features "uniwig overlaprs igd bbcache scoring fragsplit genomicdist"

# Subset
cargo install gtars-cli --features "uniwig igd"
```

## Subcommands (verified)

| Command | Feature | Purpose |
|---|---|---|
| `igd` | `igd` | Create or search an Integrated Genome Database (overlap index) |
| `overlaprs` | `overlaprs` | Pairwise BED overlap from the command line |
| `uniwig` | `uniwig` | Accumulation / coverage tracks from a BED or BAM file |
| `bbcache` | `bbcache` | Cache/manage BED files (e.g. from BEDbase) |
| `pb` | `fragsplit` | Split fragment files into pseudobulks by cluster label |
| `scoring` | `scoring` | Score region/fragment files against a reference |
| `genomicdist` | `genomicdist` | Genomic distribution analysis |
| `ranges` | (built-in) | Range operations |
| `consensus` | (built-in) | Consensus region operations |
| `prep` | (built-in) | Preprocessing utilities |

> Note: the fragment-splitting command is **`pb`** (pseudobulk), not `fragsplit`,
> even though the feature that enables it is named `fragsplit`.

## IGD

IGD has two subcommands: `create` and `search`.

```bash
gtars igd create --help    # build a database (typically from a directory of BEDs)
gtars igd search --help    # query the database with regions
```

## uniwig

A single subcommand (no `generate` sub-subcommand). Real flags include `--file`,
`--filetype` (`bed`/`bam`), `--fileheader`, `--outputtype`, `--counttype`,
`--smoothsize`, `--stepsize`, `--threads`.

```bash
gtars uniwig --file fragments.bed --filetype bed \
             --fileheader coverage --outputtype bw
gtars uniwig --help        # accepted --outputtype values vary by version
```

## pb (fragment pseudobulking)

Takes a fragments file and a cluster-mapping file. Real flags include
`--fragments` and `--mapping`.

```bash
gtars pb --fragments fragments.bed.gz --mapping cluster_mapping.tsv
gtars pb --help
```

## overlaprs / scoring / bbcache / genomicdist

Flag sets vary; inspect each:

```bash
gtars overlaprs --help
gtars scoring --help
gtars bbcache --help
gtars genomicdist --help
```

## Input/output formats

### BED
```
chr1    1000    2000
chr1    3000    4000
chr2    5000    6000
```
Coordinates are 0-based, half-open `[start, end)`.

### Fragment files
Single-cell fragments, typically gzipped BED-like (`chrom start end barcode ...`),
paired with a separate cluster-mapping file for `pb`.

### Coverage output
uniwig writes BigWig / accumulation tracks for genome-browser visualization.

## Tips

- Compile only the features you need to keep the binary small.
- Coordinate-sort BED/BAM inputs before `uniwig` and IGD operations.
- For repeated overlap queries against a fixed database, build an IGD index once
  (`gtars igd create`) and `search` it many times.
