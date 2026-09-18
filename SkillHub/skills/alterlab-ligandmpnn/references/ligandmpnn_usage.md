# LigandMPNN — Usage Reference

Deeper detail for `alterlab-ligandmpnn`. Verify flags, `--model_type` names, and checkpoints
against the upstream `dauparas/LigandMPNN` README (`TODO(verify)`).

## Install

Clone `dauparas/LigandMPNN`; download the model checkpoints per its instructions (small, no
account). Needs PyTorch — CPU is adequate for typical designs.

## Model types

LigandMPNN exposes several model types via `--model_type` (e.g. the ligand-aware model and a
plain ProteinMPNN-equivalent). Pick the ligand model when a ligand/metal/nucleic-acid is
present; confirm the exact identifiers for your checkout.

## Input

The input structure (PDB/mmCIF) must include the **non-protein atoms** — the ligand and/or
metal (HETATM) and any nucleic-acid chains — so the model conditions on them. If the ligand is
absent from the file, the design is not ligand-aware (use `alterlab-proteinmpnn` instead).

## Site-restricted design

Restrict design to residues near the ligand (design the pocket, keep the scaffold) using the
repo's fixed/redesign specification. This is the common enzyme/binder pocket workflow. Verify
argument names per version.

## Choosing between the design skills

- **alterlab-ligandmpnn** — sequence design conditioned on a ligand/metal/nucleic acid.
- **alterlab-proteinmpnn** — sequence design with protein context only.
- **alterlab-rfdiffusion** — generate/scaffold the backbone or functional site.
- **alterlab-boltz** / **alterlab-diffdock** — get a ligand pose (co-fold / dock), not a sequence.

## Pipeline

Scaffold a functional site with `alterlab-rfdiffusion` → design the pocket sequence here →
validate by refolding with `alterlab-alphafold` → obtain a pose/affinity with `alterlab-boltz`
or `alterlab-diffdock`. Batch heavy steps via `alterlab-remote-compute`.
