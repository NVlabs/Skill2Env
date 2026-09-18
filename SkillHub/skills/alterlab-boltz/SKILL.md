---
name: alterlab-boltz
description: Co-fold biomolecular complexes with Boltz-2, an open AlphaFold3-style model — predict protein + ligand (SMILES/CCD), protein + nucleic-acid, and multi-chain structures in one pass, with binding-affinity prediction. Use when folding a protein together with a small-molecule ligand, predicting a holo (ligand-bound) complex or its binding affinity, or co-folding protein–DNA/RNA assemblies. For protein-only or protein–protein folding without ligands prefer alterlab-alphafold; for antibody–antigen complexes prefer alterlab-chai; to dock a ligand into a FIXED receptor structure prefer alterlab-diffdock; to look up an existing structure prefer alterlab-pdb. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs the Boltz-2 model (`jwohlwend/boltz`; install the `boltz` package — TODO(verify) exact pin) under `uv run python`. Requires a CUDA GPU; model weights download once and cache (several GB). Inputs are a FASTA or a YAML spec listing chains + ligands (SMILES/CCD). Dispatch heavy runs via alterlab-remote-compute."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Boltz-2 (open AlphaFold3-style co-folding)

## Overview

**Boltz-2** (Passaro, Wohlwend et al. 2025; `jwohlwend/boltz`) is an open, commercially usable
biomolecular structure model in the AlphaFold3 family: it **co-folds** proteins together with
small-molecule **ligands**, nucleic acids, and multiple chains in a single prediction, and can
predict **binding affinity** — capabilities AlphaFold2/ColabFold does not have. Use it when the
biology is a *complex with a ligand or other molecule types*, not a bare protein.

## When to Use This Skill

Use this skill when the user wants to:
- Co-fold a protein **with a small-molecule ligand** (SMILES or CCD code) into a holo complex.
- Predict a **binding affinity** alongside a co-folded pose.
- Fold **protein–nucleic-acid** or multi-entity assemblies in one pass.
- Get an open AlphaFold3-style prediction without proprietary access.

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Protein-only or protein–protein folding, no ligand | `alterlab-alphafold` |
| Antibody–antigen / general one-FASTA multi-entity complex | `alterlab-chai` |
| Dock a ligand into an **existing, fixed** receptor structure | `alterlab-diffdock` |
| Retrieve an experimentally determined structure | `alterlab-pdb` |
| Design a binding-pocket sequence around a ligand | `alterlab-ligandmpnn` |

## Core Capabilities

### 1. Protein + ligand co-folding

Describe the complex in a YAML spec (chains + ligand by SMILES or CCD), then predict:

```yaml
# complex.yaml (schema — TODO(verify) against installed boltz)
version: 1
sequences:
  - protein: { id: A, sequence: "MKT...GGG" }
  - ligand:  { id: L, smiles: "CC(=O)Oc1ccccc1C(=O)O" }
```

```bash
boltz predict complex.yaml --out_dir out/ --use_msa_server
```

Outputs the co-folded structure (protein + placed ligand) plus per-model confidence.
`--use_msa_server` fetches the protein MSA from the hosted service (disclose for sensitive
sequences); a local MSA can be supplied instead.

### 2. Binding-affinity prediction

Boltz-2 can predict a binding-affinity value for a protein–ligand pair alongside the pose —
useful for triage/ranking in virtual screening. Treat predicted affinities as a *ranking*
signal, not a measured constant; confirm hits experimentally or against measured data
(`alterlab-bindingdb`). `TODO(verify)` the exact affinity-output flag/field per version.

### 3. Confidence and validation

Read the per-model confidence (and, for the interface, the model's interface score) to decide
which pose to trust. For a ligand pose specifically, sanity-check that the ligand sits in a
plausible pocket and that protein confidence around the site is high. Cross-check a docked
alternative with `alterlab-diffdock` when the receptor structure is already known and fixed.

### 4. Running on a GPU

Boltz-2 needs a CUDA GPU and downloads weights once. Batch predictions (e.g. a ligand series
against one target) via `alterlab-remote-compute`: submit → poll → harvest `out/`.

## Resources

- `references/boltz_usage.md` — install/pinning, YAML/FASTA input schema, MSA options,
  affinity output, and multi-entity examples. Loaded on demand.

Part of the AlterLab Academic Skills suite.
