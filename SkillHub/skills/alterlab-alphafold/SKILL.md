---
name: alterlab-alphafold
description: Predict protein 3D structures with AlphaFold2 via ColabFold — MMseqs2-accelerated MSAs, monomer and AlphaFold2-Multimer complex folding, and confidence-based validation (pLDDT, pTM/ipTM, PAE). Use when folding a protein sequence or complex from FASTA, generating a predicted structure with confidence metrics, ranking models, or checking self-consistency of a design. For co-folding a protein WITH a small-molecule ligand or predicting binding affinity prefer alterlab-boltz; for antibody–antigen or one-FASTA multi-entity complexes prefer alterlab-chai; to LOOK UP an already-computed structure prefer alterlab-alphafold-db; for ESM embeddings or inverse folding prefer alterlab-esm. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs via ColabFold (`colabfold_batch`; install `colabfold[alphafold]` — TODO(verify) exact pin) under `uv run python`. Requires a CUDA GPU for folding (JAX/CUDA); the MSA step uses the hosted MMseqs2 API by default or a local database. AF2 network weights are downloaded once and cached (~several GB). Dispatch heavy runs via alterlab-remote-compute."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# AlphaFold (via ColabFold)

## Overview

Predict a protein's 3D structure from its amino-acid sequence with **AlphaFold2**, run through
**ColabFold** (Mirdita et al., *Nature Methods* 2022) — which replaces AlphaFold's slow
genetic-database MSA search with the fast **MMseqs2** API, making folding practical on a
single GPU. Handles single chains (monomer) and complexes via **AlphaFold2-Multimer** (Evans
et al. 2021), and reports per-residue and per-interface **confidence metrics** so you know
which parts of a prediction to trust.

This skill **runs** folding and returns structures + confidence. To retrieve an
*already-computed* AlphaFold prediction for a known UniProt entry without running anything,
use `alterlab-alphafold-db` instead.

## When to Use This Skill

Use this skill when the user wants to:
- Fold a protein sequence (FASTA) into a predicted 3D structure (PDB/mmCIF).
- Predict a protein **complex** (AF2-Multimer) and score the interface (ipTM).
- Rank multiple models and read confidence (pLDDT, pTM, PAE) to judge reliability.
- Validate a designed sequence by refolding it and checking self-consistency vs. a target.

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Co-fold a protein **with a ligand** (SMILES/CCD) or predict binding affinity | `alterlab-boltz` |
| Antibody–antigen / arbitrary multi-entity complex from one FASTA | `alterlab-chai` |
| Look up a **precomputed** AlphaFold model by UniProt id | `alterlab-alphafold-db` |
| ESM embeddings, inverse folding, generative design | `alterlab-esm` |
| Dock a ligand into an existing structure | `alterlab-diffdock` |
| De-novo backbone generation | `alterlab-rfdiffusion` |

## Core Capabilities

### 1. Monomer folding

```bash
# One sequence per FASTA record; MSAs via the hosted MMseqs2 API (--msa-mode)
colabfold_batch input.fasta out/ --num-models 5 --num-recycle 3
```

Outputs per record: ranked `*_relaxed_rank_001_*.pdb`, a JSON with `plddt`/`pae`, and
coverage/pLDDT plots. `TODO(verify)` exact flag names against your installed ColabFold.

### 2. Complex folding (AF2-Multimer)

Join chains with a colon in one FASTA record to fold a complex:

```text
>my_complex
MKT...AAA:MSE...GGG
```

```bash
colabfold_batch complex.fasta out/ --model-type alphafold2_multimer_v3
```

Read **ipTM** (interface confidence) and the inter-chain **PAE** block to judge whether the
predicted interface is meaningful, not just the intra-chain pLDDT.

### 3. Confidence and validation

| Metric | Reads |
|--------|-------|
| **pLDDT** (0–100, per residue) | local confidence; <50 = likely disordered/unreliable |
| **pTM** | global fold confidence |
| **ipTM** | interface confidence (complexes) — the number that matters for binding |
| **PAE** | expected positional error between residue pairs; low off-diagonal = confident relative orientation |

**Self-consistency check** (validating a design): fold the candidate, then compare to the
intended backbone (e.g. TM-score / RMSD). A design that folds back to its target with high
pLDDT and low PAE is self-consistent — the standard acceptance gate in a
design→fold→score loop (see `alterlab-proteinmpnn`, `alterlab-rfdiffusion`).

### 4. Running on a GPU

Folding needs a CUDA GPU. For anything beyond a quick monomer, dispatch through
`alterlab-remote-compute` (SLURM or a managed GPU provider): submit `colabfold_batch`, poll
to completion, and harvest `out/`.

## Resources

- `references/colabfold_usage.md` — install/pinning, MSA modes (API vs. local DB), templates,
  relaxation, batch/array runs, and full metric interpretation. Loaded on demand.

Part of the AlterLab Academic Skills suite.
