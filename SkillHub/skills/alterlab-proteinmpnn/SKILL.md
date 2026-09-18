---
name: alterlab-proteinmpnn
description: Design protein sequences for a fixed backbone with ProteinMPNN (Dauparas 2022) — message-passing inverse folding that outputs sequences predicted to fold to a given structure, with fixed positions, tied/symmetric chains, amino-acid bias, and a soluble-model variant. Use when inverse-folding a backbone PDB into sequences, redesigning selected positions, imposing symmetry across chains, or generating the sequence step of a design→fold→score loop. For pocket/interface design WITH a bound ligand, metal, or nucleic acid prefer alterlab-ligandmpnn; to GENERATE a new backbone prefer alterlab-rfdiffusion; to refold and validate a design prefer alterlab-alphafold; for generative multimodal design prefer alterlab-esm. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Runs `protein_mpnn_run.py` from `dauparas/ProteinMPNN` (PyTorch) under `uv run python`. The model is small — it runs on CPU and does not require a GPU (a GPU only speeds large batches). Network weights ship with the repo (no download/account). Input is a backbone PDB; output is a FASTA of designed sequences with scores."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# ProteinMPNN (fixed-backbone sequence design)

## Overview

**ProteinMPNN** (Dauparas et al., *Science* 2022; `dauparas/ProteinMPNN`) solves the
**inverse-folding** problem: given a protein **backbone** (a 3D structure with no or a
placeholder sequence), it designs amino-acid **sequences predicted to fold to that
backbone**. It is fast, robust, runs on CPU, and is the standard "sequence" step between
backbone generation (`alterlab-rfdiffusion`) and structure validation
(`alterlab-alphafold`).

## When to Use This Skill

Use this skill when the user wants to:
- **Inverse-fold** a backbone PDB into one or more candidate sequences.
- **Redesign** only selected positions while fixing the rest (partial design).
- Enforce **symmetry** by tying residues/chains so homo-oligomers get identical sequences.
- Bias the amino-acid composition (e.g. avoid cysteines) or use the **soluble** model.
- Produce the sequence step of a **design → fold → score** loop.

### Does NOT Trigger

| Scenario | Use instead |
|----------|-------------|
| Design a pocket/interface **with a ligand, metal, or nucleic acid** present | `alterlab-ligandmpnn` |
| **Generate** a new backbone (no starting structure) | `alterlab-rfdiffusion` |
| Refold a designed sequence to check it (validation) | `alterlab-alphafold` |
| Generative multimodal (sequence+structure+function) design | `alterlab-esm` |

## Core Capabilities

### 1. Basic inverse folding

```bash
# Parse the PDB, then design sequences (dauparas/ProteinMPNN CLI — TODO(verify) flags/version).
# The parser lives in the repo's helper_scripts directory; run it by name:
python parse_multiple_chains.py --input_path=pdbs/ --output_path=parsed.jsonl
python protein_mpnn_run.py \
  --jsonl_path parsed.jsonl --out_folder out/ \
  --num_seq_per_target 8 --sampling_temp "0.1"
```

Lower `--sampling_temp` (e.g. 0.1) gives conservative, high-confidence designs; higher
temperatures increase diversity. Output FASTA headers carry the model **score** (lower =
better) and sequence recovery.

### 2. Fixed positions and chains

Supply a fixed-positions spec (JSONL from the helper scripts) to keep catalytic/known
residues while redesigning the rest, and a chain spec to design only some chains. Verify the
exact helper-script names against your checkout (`TODO(verify)`).

### 3. Symmetry / tied positions

Tie positions across chains so a homo-oligomer receives one sequence applied symmetrically —
essential for symmetric `alterlab-rfdiffusion` outputs.

### 4. Design → fold → score loop

The canonical de-novo pipeline:

1. **Generate** a backbone with `alterlab-rfdiffusion`.
2. **Design** sequences for it here (ProteinMPNN), sampling several per backbone.
3. **Score** by refolding each with `alterlab-alphafold` and accepting only self-consistent
   designs (returns to the target backbone with high pLDDT, low PAE).

## Resources

- `references/proteinmpnn_usage.md` — install/pinning, helper-script inputs (fixed positions,
  tied chains, bias), the soluble model, temperature guidance, and loop integration. Loaded on
  demand.

Part of the AlterLab Academic Skills suite.
