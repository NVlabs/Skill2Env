---
name: alterlab-deeptools
description: Process and visualize deep-sequencing coverage with the deepTools CLI — convert BAM to bigWig (bamCoverage), build log2 ratio tracks (bamCompare), run QC (multiBamSummary correlation, PCA, plotFingerprint), apply the ATAC-seq Tn5 shift (alignmentSieve --ATACshift), and make TSS/peak heatmaps and profiles (computeMatrix, plotHeatmap, plotProfile). Use for coverage tracks, signal heatmaps/profiles, normalization (RPGC/CPM/RPKM), and effective-genome-size lookups for ChIP-seq, ATAC-seq, MNase-seq, or RNA-seq. NOT for per-read/CIGAR/MAPQ BAM record access — that is pysam. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with the skill's Python package installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# deepTools: NGS Data Analysis Toolkit

## Overview

deepTools is a comprehensive suite of Python command-line tools designed for processing and analyzing high-throughput sequencing data. Use deepTools to perform quality control, normalize data, compare samples, and generate publication-quality visualizations for ChIP-seq, RNA-seq, ATAC-seq, MNase-seq, and other NGS experiments.

**Core capabilities:**
- Convert BAM alignments to normalized coverage tracks (bigWig/bedGraph)
- Quality control assessment (fingerprint, correlation, coverage)
- Sample comparison and correlation analysis
- Heatmap and profile plot generation around genomic features
- Enrichment analysis and peak region visualization

## When to Use This Skill

This skill should be used when:

- **File conversion**: "Convert BAM to bigWig", "generate coverage tracks", "normalize ChIP-seq data"
- **Quality control**: "check ChIP quality", "compare replicates", "assess sequencing depth", "QC analysis"
- **Visualization**: "create heatmap around TSS", "plot ChIP signal", "visualize enrichment", "generate profile plot"
- **Sample comparison**: "compare treatment vs control", "correlate samples", "PCA analysis"
- **Analysis workflows**: "analyze ChIP-seq data", "RNA-seq coverage", "ATAC-seq analysis", "complete workflow"
- **Working with specific file types**: BAM files, bigWig files, BED region files in genomics context

## Quick Start

For users new to deepTools, start with file validation and common workflows:

### 1. Validate Input Files

Before running any analysis, validate BAM, bigWig, and BED files using the validation script:

```bash
python scripts/validate_files.py --bam sample1.bam sample2.bam --bed regions.bed
```

This checks file existence, BAM indices, and format correctness.

### 2. Generate Workflow Template

For standard analyses, use the workflow generator to create customized scripts:

```bash
# List available workflows
python scripts/workflow_generator.py --list

# Generate ChIP-seq QC workflow
python scripts/workflow_generator.py chipseq_qc -o qc_workflow.sh \
    --input-bam Input.bam --chip-bams "ChIP1.bam ChIP2.bam" \
    --genome-size 2913022398

# Make executable and run
chmod +x qc_workflow.sh
./qc_workflow.sh
```

### 3. Most Common Operations

See `assets/quick_reference.md` for frequently used commands and parameters.

## Installation

```bash
uv pip install deeptools
```

## Core Workflows

deepTools workflows typically follow this pattern: **QC → Normalization → Comparison/Visualization**

### ChIP-seq Quality Control Workflow

When users request ChIP-seq QC or quality assessment:

1. **Generate workflow script** using `scripts/workflow_generator.py chipseq_qc`
2. **Key QC steps**:
   - Sample correlation (multiBamSummary + plotCorrelation)
   - PCA analysis (plotPCA)
   - Coverage assessment (plotCoverage)
   - Fragment size validation (bamPEFragmentSize)
   - ChIP enrichment strength (plotFingerprint)

**Interpreting results:**
- **Correlation**: Replicates should cluster together with high correlation (>0.9)
- **Fingerprint**: Strong ChIP shows steep rise; flat diagonal indicates poor enrichment
- **Coverage**: Assess if sequencing depth is adequate for analysis

Full workflow details in `references/workflows.md` → "ChIP-seq Quality Control Workflow"

### ChIP-seq Complete Analysis Workflow

For full ChIP-seq analysis from BAM to visualizations:

1. **Generate coverage tracks** with normalization (bamCoverage)
2. **Create comparison tracks** (bamCompare for log2 ratio)
3. **Compute signal matrices** around features (computeMatrix)
4. **Generate visualizations** (plotHeatmap, plotProfile)
5. **Enrichment analysis** at peaks (plotEnrichment)

Use `scripts/workflow_generator.py chipseq_analysis` to generate template.

Complete command sequences in `references/workflows.md` → "ChIP-seq Analysis Workflow"

### RNA-seq Coverage Workflow

For strand-specific RNA-seq coverage tracks:

Use bamCoverage with `--filterRNAstrand` to separate forward and reverse strands.

**Important:** NEVER use `--extendReads` for RNA-seq (would extend over splice junctions).

Use normalization: CPM for fixed bins, RPKM for gene-level analysis.

Template available: `scripts/workflow_generator.py rnaseq_coverage`

Details in `references/workflows.md` → "RNA-seq Coverage Workflow"

### ATAC-seq Analysis Workflow

ATAC-seq requires Tn5 offset correction:

1. **Shift reads** using alignmentSieve with `--ATACshift`
2. **Generate coverage** with bamCoverage
3. **Analyze fragment sizes** (expect nucleosome ladder pattern)
4. **Visualize at peaks** if available

Template: `scripts/workflow_generator.py atacseq`

Full workflow in `references/workflows.md` → "ATAC-seq Workflow"

## Tool Categories and Common Tasks

deepTools commands group into three categories. Quick command examples for each
live in `references/usage_playbook.md` → "Inline Command Examples by Category";
full parameter documentation is in `references/tools_reference.md`.

- **BAM/bigWig processing** — bamCoverage, bamCompare, multiBamSummary,
  multiBigwigSummary, correctGCBias, alignmentSieve
  (`tools_reference.md` → "BAM and bigWig File Processing Tools")
- **Quality control** — plotFingerprint, plotCoverage, plotCorrelation, plotPCA,
  bamPEFragmentSize (`tools_reference.md` → "Quality Control Tools")
- **Visualization** — computeMatrix, plotHeatmap, plotProfile, plotEnrichment
  (`tools_reference.md` → "Visualization Tools")

## Normalization Methods

Choosing the correct normalization is critical for valid comparisons. Consult `references/normalization_methods.md` for comprehensive guidance.

**Quick selection guide:**

- **ChIP-seq coverage**: Use RPGC or CPM
- **ChIP-seq comparison**: Use bamCompare with log2 and readCount
- **RNA-seq bins**: Use CPM
- **RNA-seq genes**: Use RPKM (accounts for gene length)
- **ATAC-seq**: Use RPGC or CPM

**Normalization methods:**
- **RPGC**: 1× genome coverage (requires --effectiveGenomeSize)
- **CPM**: Counts per million mapped reads
- **RPKM**: Reads per kb per million (accounts for region length)
- **BPM**: Bins per million
- **None**: Raw counts (not recommended for comparisons)

Full explanation: `references/normalization_methods.md`

## Effective Genome Sizes

RPGC normalization requires effective genome size. Common values:

| Organism | Assembly | Size | Usage |
|----------|----------|------|-------|
| Human | GRCh38/hg38 | 2,913,022,398 | `--effectiveGenomeSize 2913022398` |
| Mouse | GRCm38/mm10 | 2,652,783,500 | `--effectiveGenomeSize 2652783500` |
| Zebrafish | GRCz11 | 1,368,780,147 | `--effectiveGenomeSize 1368780147` |
| *Drosophila* | dm6 | 142,573,017 | `--effectiveGenomeSize 142573017` |
| *C. elegans* | ce10/ce11 | 100,286,401 | `--effectiveGenomeSize 100286401` |

Complete table with read-length-specific values: `references/effective_genome_sizes.md`

## Common Parameters Across Tools

Many deepTools commands share these options:

**Performance:**
- `--numberOfProcessors, -p`: Enable parallel processing (always use available cores)
- `--region`: Process specific regions for testing (e.g., `chr1:1-1000000`)

**Read Filtering:**
- `--ignoreDuplicates`: Remove PCR duplicates (recommended for most analyses)
- `--minMappingQuality`: Filter by alignment quality (e.g., `--minMappingQuality 10`)
- `--minFragmentLength` / `--maxFragmentLength`: Fragment length bounds
- `--samFlagInclude` / `--samFlagExclude`: SAM flag filtering

**Read Processing:**
- `--extendReads`: Extend to fragment length (ChIP-seq: YES, RNA-seq: NO)
- `--centerReads`: Center at fragment midpoint for sharper signals

## Best Practices

### File Validation
**Always validate files first** using `scripts/validate_files.py` to check:
- File existence and readability
- BAM indices present (.bai files)
- BED format correctness
- File sizes reasonable

### Analysis Strategy

1. **Start with QC**: Run correlation, coverage, and fingerprint analysis before proceeding
2. **Test on small regions**: Use `--region chr1:1-10000000` for parameter testing
3. **Document commands**: Save full command lines for reproducibility
4. **Use consistent normalization**: Apply same method across samples in comparisons
5. **Verify genome assembly**: Ensure BAM and BED files use matching genome builds

### ChIP-seq Specific

- **Always extend reads** for ChIP-seq: `--extendReads 200`
- **Remove duplicates**: Use `--ignoreDuplicates` in most cases
- **Check enrichment first**: Run plotFingerprint before detailed analysis
- **GC correction**: Only apply if significant bias detected; never use `--ignoreDuplicates` after GC correction

### RNA-seq Specific

- **Never extend reads** for RNA-seq (would span splice junctions)
- **Strand-specific**: Use `--filterRNAstrand forward/reverse` for stranded libraries
- **Normalization**: CPM for bins, RPKM for genes

### ATAC-seq Specific

- **Apply Tn5 correction**: Use alignmentSieve with `--ATACshift`
- **Fragment filtering**: Set appropriate min/max fragment lengths
- **Check nucleosome pattern**: Fragment size plot should show ladder pattern

### Performance Optimization

1. **Use multiple processors**: `--numberOfProcessors 8` (or available cores)
2. **Increase bin size** for faster processing and smaller files
3. **Process chromosomes separately** for memory-limited systems
4. **Pre-filter BAM files** using alignmentSieve to create reusable filtered files
5. **Use bigWig over bedGraph**: Compressed and faster to process

## Troubleshooting

### Common Issues

**BAM index missing:**
```bash
samtools index input.bam
```

**Out of memory:**
Process chromosomes individually using `--region`:
```bash
bamCoverage --bam input.bam -o chr1.bw --region chr1
```

**Slow processing:**
Increase `--numberOfProcessors` and/or increase `--binSize`

**bigWig files too large:**
Increase bin size: `--binSize 50` or larger

### Validation Errors

Run validation script to identify issues:
```bash
python scripts/validate_files.py --bam *.bam --bed regions.bed
```

Common errors and solutions explained in script output.

## Reference Documentation

Load the matching reference on demand:

| Reference | Load when |
|-----------|-----------|
| `references/tools_reference.md` | User asks about a specific tool, parameter, or detailed usage. All commands by category (BAM/bigWig 9, QC 6, visualization 3, misc 2) with parameters, examples, and notes. |
| `references/workflows.md` | User needs a complete analysis pipeline. ChIP-seq QC, ChIP-seq analysis, RNA-seq coverage, ATAC-seq, multi-sample comparison, peak region analysis, performance tips. |
| `references/normalization_methods.md` | User asks about normalization, comparing samples, or which method to use. Per-method detail (RPGC/CPM/RPKM/BPM…), formulas, selection guide, pitfalls. |
| `references/effective_genome_sizes.md` | User needs a genome size for RPGC normalization or GC-bias correction. Per-organism and read-length-specific values, custom-genome calculation. |
| `references/usage_playbook.md` | Driving the skill: per-request playbooks, example interactions, quick command examples by category, and grep recipes for searching the references above. |

## Helper Scripts

### scripts/validate_files.py

Validates BAM, bigWig, and BED files for deepTools analysis. Checks file existence, indices, and format.

**Usage:**
```bash
python scripts/validate_files.py --bam sample1.bam sample2.bam \
    --bed peaks.bed --bigwig signal.bw
```

**When to use:** Before starting any analysis, or when troubleshooting errors.

### scripts/workflow_generator.py

Generates customizable bash script templates for common deepTools workflows.

**Available workflows:**
- `chipseq_qc`: ChIP-seq quality control
- `chipseq_analysis`: Complete ChIP-seq analysis
- `rnaseq_coverage`: Strand-specific RNA-seq coverage
- `atacseq`: ATAC-seq with Tn5 correction

**Usage:**
```bash
# List workflows
python scripts/workflow_generator.py --list

# Generate workflow
python scripts/workflow_generator.py chipseq_qc -o qc.sh \
    --input-bam Input.bam --chip-bams "ChIP1.bam ChIP2.bam" \
    --genome-size 2913022398 --threads 8

# Run generated workflow
chmod +x qc.sh
./qc.sh
```

**When to use:** Users request standard workflows or need template scripts to customize.

## Assets

### assets/quick_reference.md

Quick reference card with most common commands, effective genome sizes, and typical workflow pattern.

**When to use:** Users need quick command examples without detailed documentation.

## Handling User Requests

Per-request playbooks (new vs experienced users, task-specific responses for
"convert BAM to bigWig" / "check ChIP quality" / "create heatmap" /
"compare samples"), example interactions, and grep recipes for searching the
references all live in `references/usage_playbook.md`. The common thread:
validate files first → pick the right workflow/normalization → generate or run
the command → explain the result.

## Key Reminders

- **Extend reads carefully**: `--extendReads` YES for ChIP-seq, NO for RNA-seq (would span splice junctions)
- **Normalization is mutually exclusive in bamCompare**: RPGC is a `--normalizeUsing` value; `--scaleFactorsMethod` only takes readCount/SES/None
- **RPGC requires `--effectiveGenomeSize`**; verify the assembly matches your BAM/BED genome build
- **Check QC first** (plotFingerprint, correlation) before detailed analysis; test parameters on a `--region`

