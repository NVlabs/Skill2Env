# Boltz-2 — Usage Reference

Deeper detail for `alterlab-boltz`. Boltz is under active development; verify the input schema,
flags, and package pin against your installed version (`TODO(verify)`), using the upstream
`jwohlwend/boltz` README as the source of truth.

## Install

Install the `boltz` package into a CUDA-enabled environment (weights download on first run and
cache locally). Exact version pins and the CUDA/torch build are environment-specific —
`TODO(verify)` for your GPU/driver.

## Input

Boltz accepts either a FASTA (with typed records) or a YAML spec that lists every entity:

- **protein** chains (sequence)
- **ligand** entities by **SMILES** or **CCD** code
- **nucleic-acid** chains (DNA/RNA)
- constraints / templates where supported

A YAML spec is the clearest way to express a protein+ligand complex. Confirm the exact schema
keys against the installed version — the field names have changed across releases.

## Run

```bash
boltz predict complex.yaml --out_dir out/ --use_msa_server
```

- `--use_msa_server` — fetch protein MSAs from the hosted server (sends the sequence out;
  disclose for sensitive/proprietary sequences). Supply a precomputed MSA to stay offline.
- Output: predicted structure(s) with confidence; ligand placed in the co-folded pose.

## Binding affinity

Boltz-2 adds affinity prediction for protein–ligand pairs. Use it to **rank** candidates in a
screen; it is a model estimate, not a measured Kd/Ki. Validate top ranks against measured data
(`alterlab-bindingdb`) or experiment. `TODO(verify)` the affinity flag/output field name.

## Choosing between the folding skills

- **alterlab-boltz** — complex WITH a ligand / nucleic acid, or affinity. Open AF3-style.
- **alterlab-alphafold** — protein or protein–protein only (AF2/ColabFold), rich confidence.
- **alterlab-chai** — antibody–antigen and general one-FASTA multi-entity complexes (Chai-1).
- **alterlab-diffdock** — the receptor structure is already known/fixed and you only need to
  place a ligand (docking), not co-fold the protein.

## GPU dispatch

Batch a ligand series against one target as separate predictions via
`alterlab-remote-compute` (submit → poll → harvest).
