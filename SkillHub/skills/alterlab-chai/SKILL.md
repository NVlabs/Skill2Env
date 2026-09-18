---
name: alterlab-chai
description: Predict biomolecular complexes with Chai-1, an open AlphaFold3-style model that folds multi-entity assemblies (proteins, ligands, nucleic acids) from a single typed FASTA — strong on antibody–antigen and protein–ligand complexes, with optional MSA and restraint inputs. Use when predicting an antibody–antigen complex, folding a mixed protein/ligand/nucleic-acid assembly described in one FASTA, or generating a complex with experimental restraints. For binding-affinity prediction or a ligand-focused co-fold prefer alterlab-boltz; for protein-only or protein–protein folding prefer alterlab-alphafold; to dock into a fixed receptor prefer alterlab-diffdock. Part of the AlterLab Academic Skills suite.
license: Apache-2.0
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs the Chai-1 model (`chaidiscovery/chai-lab`; install the `chai_lab` package — TODO(verify) exact pin) under `uv run python`. Requires a CUDA GPU; weights download once and cache (several GB). Input is a single FASTA with typed records (protein/ligand/RNA/DNA); MSAs and restraints are optional. Dispatch heavy runs via alterlab-remote-compute."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Chai-1 (open complex prediction)

## Overview

**Chai-1** (Chai Discovery 2024; `chaidiscovery/chai-lab`) is an open AlphaFold3-style model
that predicts **multi-entity biomolecular complexes** — proteins, small-molecule ligands, and
nucleic acids together — from a **single typed FASTA**. It is particularly used for
**antibody–antigen** and protein–ligand complexes, can run with or without MSAs, and accepts
**restraints** to guide the prediction.

Its niche relative to the other folders: one FASTA describing a *mixed assembly*, and
antibody–antigen in particular. For a ligand co-fold where you specifically want a **binding
affinity**, use `alterlab-boltz`; for a bare protein, use `alterlab-alphafold`.

## When to Use This Skill

Use this skill when the user wants to:
- Predict an **antibody–antigen** complex structure.
- Fold a **mixed assembly** (protein + ligand + nucleic acid) described in one FASTA.
- Run complex prediction **with or without MSAs**, optionally guided by restraints.
- Get an open AlphaFold3-style complex prediction with per-entity confidence.

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Predict a protein–ligand **binding affinity** | `alterlab-boltz` |
| Protein-only or protein–protein folding | `alterlab-alphafold` |
| Dock a ligand into a **fixed** receptor structure | `alterlab-diffdock` |
| Look up an experimental complex structure | `alterlab-pdb` |
| Design antibody/interface sequences | `alterlab-proteinmpnn` / `alterlab-ligandmpnn` |

## Core Capabilities

### 1. Single-FASTA multi-entity input

Chai-1 reads one FASTA whose records are typed by entity. A protein + ligand example:

```text
>protein|antibody-Fv
EVQ...SS
>protein|antigen
MKT...GG
>ligand|cofactor
CC(=O)Oc1ccccc1C(=O)O
```

```bash
# CLI form (verify against installed chai-lab — TODO(verify))
chai-lab fold input.fasta out/
```

The header type tags (`protein`, `ligand`, `rna`, `dna`) tell Chai how to treat each record;
confirm the exact header/type syntax against your installed version.

### 2. Antibody–antigen complexes

The common use case: fold an antibody Fv/Fab against its antigen and read the **interface
confidence** (per-model / interface score) to judge whether the predicted epitope/paratope
contact is trustworthy. Use restraints when you have partial epitope knowledge.

### 3. MSA and restraints

- **MSA optional** — Chai-1 can run single-sequence or with MSAs; MSAs generally improve
  accuracy but cost time. Disclose any hosted-MSA usage for sensitive sequences.
- **Restraints** — supply contact/pocket restraints to bias the prediction toward known
  biology. `TODO(verify)` the restraint file format per version.

### 4. Confidence and GPU dispatch

Read per-entity confidence and the interface score to pick a model. Chai-1 needs a CUDA GPU
and caches weights on first run; batch predictions (e.g. an antibody panel against one antigen)
via `alterlab-remote-compute` (submit → poll → harvest `out/`).

## Resources

- `references/chai_usage.md` — install/pinning, FASTA type-tag syntax, MSA/restraint options,
  outputs, and folder-choice guidance. Loaded on demand.

Part of the AlterLab Academic Skills suite.
