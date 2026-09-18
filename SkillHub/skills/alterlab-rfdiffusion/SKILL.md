---
name: alterlab-rfdiffusion
description: Generate de-novo protein backbones with RFdiffusion (Watson 2023) — a diffusion model for unconditional monomer generation, motif scaffolding, binder design against a target, and symmetric oligomers. Use when generating a new protein backbone from scratch, scaffolding a functional motif into a fold, designing a binder backbone to a target surface, or building symmetric assemblies; RFdiffusion produces the STRUCTURE, then alterlab-proteinmpnn designs its sequence and alterlab-alphafold validates it. For sequence design of an existing backbone prefer alterlab-proteinmpnn (or alterlab-ligandmpnn with a ligand); to fold a known sequence prefer alterlab-alphafold; for generative multimodal design prefer alterlab-esm. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs RFdiffusion (`RosettaCommons/RFdiffusion`, PyTorch + SE(3)-transformer) under `uv run python` via `run_inference.py`. Requires a CUDA GPU for practical generation; model weights download once and cache (several GB; no account). Outputs backbone PDBs (no sequence) — pair with alterlab-proteinmpnn then alterlab-alphafold. Dispatch runs via alterlab-remote-compute."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# RFdiffusion (de-novo backbone generation)

## Overview

**RFdiffusion** (Watson et al., *Nature* 2023; `RosettaCommons/RFdiffusion`) is a diffusion
model that **generates protein backbones** — new 3D structures, not sequences. It supports
unconditional generation, **motif scaffolding** (build a fold around a fixed functional
motif), **binder design** (generate a backbone that binds a target surface), and **symmetric**
assemblies. It is the structure-generation step that *starts* the de-novo design pipeline;
`alterlab-proteinmpnn` then designs sequences for the backbone and `alterlab-alphafold`
validates them.

## When to Use This Skill

Use this skill when the user wants to:
- **Generate** a novel protein backbone from scratch (unconditional).
- **Scaffold** a functional motif (e.g. a binding loop / catalytic geometry) into a new fold.
- Design a **binder** backbone against a given target protein surface / hotspots.
- Build **symmetric** oligomers (cyclic/dihedral) as backbones.

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Design the **sequence** for an existing backbone | `alterlab-proteinmpnn` |
| Design a pocket sequence **with a ligand/metal** present | `alterlab-ligandmpnn` |
| **Fold** a known sequence into a structure | `alterlab-alphafold` |
| Generative multimodal (sequence+structure) design | `alterlab-esm` |

## Core Capabilities

### 1. Unconditional generation

```bash
# RosettaCommons/RFdiffusion — run_inference.py drives generation (Hydra config).
# It lives in the repo's scripts directory; TODO(verify) config keys/version.
python run_inference.py \
  'contigmap.contigs=[100-100]' \
  inference.output_prefix=out/uncond \
  inference.num_designs=10
```

`contigmap.contigs` specifies what to build (here, a 100-residue monomer). Outputs backbone
PDBs with no sequence.

### 2. Motif scaffolding

Fix a functional motif (residues from an input PDB) and let RFdiffusion build a supporting
fold around it — the way to transplant a binding/catalytic geometry into a new, stable
scaffold. Contig syntax mixes fixed motif ranges with generated segments (`TODO(verify)` the
exact contig grammar for your version).

### 3. Binder design

Provide a target structure and hotspot residues; RFdiffusion generates binder backbones docked
against that surface. Follow with sequence design (`alterlab-proteinmpnn`) and an interface
validation refold (`alterlab-alphafold`, read ipTM).

### 4. The full design → fold → score loop

1. **Generate** backbones here (RFdiffusion).
2. **Design** sequences with `alterlab-proteinmpnn` (or `alterlab-ligandmpnn` if a ligand is
   present).
3. **Score** by refolding with `alterlab-alphafold` and keeping only self-consistent designs.

GPU-heavy — dispatch generation and the fold sweep via `alterlab-remote-compute`.

## Resources

- `references/rfdiffusion_usage.md` — install/pinning, contig grammar, motif/binder/symmetry
  configs, and loop integration. Loaded on demand.

Part of the AlterLab Academic Skills suite.
