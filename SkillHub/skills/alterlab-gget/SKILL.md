---
name: alterlab-gget
description: "Run fast one-liner queries to 20+ bioinformatics databases from the gget CLI or Python — gene info (Ensembl), BLAST, AlphaFold structures, Enrichr enrichment, and more. Use for quick interactive lookups of genes, sequences, structures, or pathways — for batch processing or advanced BLAST use biopython, for multi-database Python workflows use bioservices. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Install with `uv pip install gget`; core modules need no API key or account. cosmic needs a COSMIC account; gpt needs an OpenAI key; alphafold/cellxgene/elm/gpt need a one-time `gget setup`."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# gget

## Overview

gget is a command-line bioinformatics tool and Python package providing unified access to 20+ genomic databases and analysis methods. Query gene information, sequence analysis, protein structures, expression data, and disease associations through a consistent interface. All gget modules work both as command-line tools and as Python functions.

**Important**: The databases queried by gget are continuously updated, which sometimes changes their structure. gget modules are tested automatically on a biweekly basis and updated to match new database structures when necessary.

## Installation

Install gget in a clean virtual environment to avoid conflicts:

```bash
# Install (or upgrade) into a clean environment
uv pip install --upgrade gget

# In Python/Jupyter
import gget
```

## Quick Start

Basic usage pattern for all modules:

```bash
# Command-line
gget <module> [arguments] [options]

# Python
gget.module(arguments, options)
```

Most modules return:
- **Command-line**: JSON (default) or CSV with `-csv` flag
- **Python**: DataFrame or dictionary

Common flags across modules:
- `-o/--out`: Save results to file
- `-q/--quiet`: Suppress progress information
- `-csv`: Return CSV format (command-line only)

## Module Catalog

Pick a module, then see `references/module_examples.md` for worked CLI + Python
examples and `references/module_reference.md` for the full parameter table.

| Module | Purpose | Queried source |
|--------|---------|----------------|
| `ref` | Reference genome download links/metadata | Ensembl |
| `search` | Find genes by name/description | Ensembl |
| `info` | Gene/transcript metadata (~1000 IDs max) | Ensembl, UniProt, NCBI |
| `seq` | Nucleotide/amino-acid sequences (FASTA) | Ensembl |
| `blast` | BLAST against standard databases | NCBI BLAST |
| `blat` | Genomic position of a sequence | UCSC BLAT |
| `muscle` | Multiple sequence alignment | Muscle5 (local) |
| `diamond` | Fast local protein/translated alignment | DIAMOND (local) |
| `pdb` | Experimental protein structures + metadata | RCSB PDB |
| `alphafold` | Predict 3D protein structure (setup req.) | AlphaFold2 (local) |
| `elm` | Eukaryotic linear motifs (setup req.) | ELM |
| `archs4` | Correlated genes / tissue expression | ARCHS4 |
| `cellxgene` | Single-cell RNA-seq (setup req.) | CZ CELLxGENE Census |
| `enrichr` | Ontology/pathway enrichment | Enrichr |
| `bgee` | Orthologs and expression | Bgee |
| `opentargets` | Disease/drug associations | OpenTargets |
| `cbio` | Cancer genomics heatmaps | cBioPortal |
| `cosmic` | Somatic cancer mutations (license/account) | COSMIC |
| `mutate` | Generate mutated sequences | local |
| `gpt` | Natural-language text generation (setup req.) | OpenAI API |
| `setup` | Install third-party deps for a module | local |

**Setup-required modules** (`gget setup <module>` before first use):
`alphafold` (~4GB params, needs `uv pip install openmm` first), `cellxgene`,
`elm`, `gpt`.

## Routing

- **Quick interactive lookup** (gene info, BLAST, one structure, one enrichment) →
  use gget directly; see `references/module_examples.md`.
- **Batch processing / advanced BLAST** → use the **biopython** skill.
- **Multi-database Python workflows** → use the **bioservices** skill.
- **Chaining several gget modules into a pipeline** → see `references/workflows.md`
  and the ready-made `scripts/` (gene_analysis, batch_sequence_analysis,
  enrichment_pipeline).

## Best Practices (essentials)

- Use `--limit` to bound large queries; save with `-o/--out` for reproducibility.
- Gene symbols are **case-sensitive** in cellxgene ('PAX7' vs 'Pax7').
- Run `gget setup` before first use of alphafold, cellxgene, elm, gpt.
- Process max ~1000 Ensembl IDs at once with `gget info`.
- Database structures change; keep gget updated: `uv pip install --upgrade gget`.
- Use virtual environments to avoid dependency conflicts.

## Output Formats

- **Command-line**: JSON default; `-csv` for CSV; FASTA (`seq`, `mutate`);
  PDB (`pdb`, `alphafold`); PNG (`cbio plot`).
- **Python**: DataFrame/dict default; `json=True` for JSON; `save=True` or
  `out="filename"` to write; AnnData for `cellxgene`.

## References

- `references/module_examples.md` — worked CLI + Python examples for every module
- `references/module_reference.md` — full parameter tables for all modules
- `references/database_info.md` — queried databases and their update frequencies
- `references/workflows.md` — extended multi-module workflow examples

For additional help:
- Official documentation: https://pachterlab.github.io/gget/
- GitHub issues: https://github.com/pachterlab/gget/issues
- Citation: Luebbert, L. & Pachter, L. (2023). Efficient querying of genomic reference databases with gget. Bioinformatics. https://doi.org/10.1093/bioinformatics/btac836

