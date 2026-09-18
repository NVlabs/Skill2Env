---
name: alterlab-ligandmpnn
description: Design protein sequences around bound ligands, metals, and nucleic acids with LigandMPNN (Dauparas 2023) — inverse folding that conditions on non-protein context, so binding-pocket and metal-site residues are chosen to fit the actual ligand. Use when designing a small-molecule or metal binding pocket, redesigning residues that contact a ligand/ion/nucleic acid, or doing enzyme active-site design where the substrate matters. For backbone sequence design with NO ligand/metal context prefer alterlab-proteinmpnn; to GENERATE a backbone or scaffold a functional site prefer alterlab-rfdiffusion; to validate a design by refolding prefer alterlab-alphafold; to co-fold or dock the ligand prefer alterlab-boltz or alterlab-diffdock. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs LigandMPNN (`dauparas/LigandMPNN`, PyTorch) under `uv run python` via its `run.py`. Model checkpoints download once (small; no account). CPU works for typical sizes; a GPU only speeds large batches. Input is a structure containing the protein PLUS the ligand/metal/nucleic-acid atoms (e.g. a PDB with the HETATM records)."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# LigandMPNN (ligand-aware sequence design)

## Overview

**LigandMPNN** (Dauparas et al. 2023; `dauparas/LigandMPNN`) extends ProteinMPNN's inverse
folding to **condition on non-protein context** — small-molecule ligands, metal ions, and
nucleic acids. Because the model *sees* the ligand/metal atoms, the residues it designs for a
**binding pocket** or **metal site** are chosen to complement what is actually bound, which
plain ProteinMPNN (protein-atoms-only) cannot do.

Use it whenever the design target is a **site that contacts a ligand or ion**. For sequence
design of a backbone with no bound context, use `alterlab-proteinmpnn`.

## When to Use This Skill

Use this skill when the user wants to:
- Design a **small-molecule binding pocket** so the residues fit the ligand.
- Design a **metal-coordinating site** (e.g. Zn/Fe) with the ion in context.
- Redesign residues that **contact a ligand, ion, or nucleic acid**.
- Do **enzyme active-site** design where the substrate/cofactor should guide the choice.

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Sequence design for a backbone with **no** ligand/metal context | `alterlab-proteinmpnn` |
| **Generate** a backbone or scaffold a functional motif | `alterlab-rfdiffusion` |
| Validate a design by refolding | `alterlab-alphafold` |
| Co-fold the protein WITH the ligand from scratch | `alterlab-boltz` |
| Dock a ligand into a fixed pocket (pose, not sequence) | `alterlab-diffdock` |

## Core Capabilities

### 1. Ligand-aware pocket design

```bash
# dauparas/LigandMPNN CLI — TODO(verify) flags/checkpoint names against your checkout
python run.py \
  --model_type ligand_mpnn \
  --pdb_path complex_with_ligand.pdb \
  --out_folder out/ \
  --number_of_batches 8
```

The input PDB must contain the ligand/metal atoms (HETATM). LigandMPNN designs pocket residues
that fit that context; supply a fixed-positions/redesign spec to target only the site.

### 2. Metal-site and nucleic-acid context

Provide the coordinating ion or the nucleic-acid chain in the structure so the model conditions
on it — critical for metalloenzyme and DNA/RNA-binding designs.

### 3. Site-focused redesign

Restrict design to the residues within a shell of the ligand (redesign the pocket, keep the
scaffold), analogous to ProteinMPNN's fixed-positions workflow. Verify the exact argument names
for your version (`TODO(verify)`).

### 4. In the design pipeline

LigandMPNN provides the **sequence** step when the functional site involves a ligand: scaffold
or generate the site with `alterlab-rfdiffusion`, design the pocket sequence here, then validate
by refolding (`alterlab-alphafold`) and — if you need a pose/affinity — co-fold with
`alterlab-boltz` or dock with `alterlab-diffdock`.

## Resources

- `references/ligandmpnn_usage.md` — install/pinning, model types, HETATM/context input,
  site-restricted design, and pipeline integration. Loaded on demand.

Part of the AlterLab Academic Skills suite.
