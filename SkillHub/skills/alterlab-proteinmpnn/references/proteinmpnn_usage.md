# ProteinMPNN — Usage Reference

Deeper detail for `alterlab-proteinmpnn`. Verify helper-script names, flags, and the checkout
against the upstream `dauparas/ProteinMPNN` README (`TODO(verify)`); the CLI has minor
variations across forks.

## Install

Clone `dauparas/ProteinMPNN`; it ships model weights in-repo (no download). Needs PyTorch —
CPU is fine for typical designs; a GPU only helps very large batches.

## Inputs (helper scripts)

ProteinMPNN reads a parsed JSONL describing chains and optional constraints, produced by the
repo's `helper_scripts/`:

- `parse_multiple_chains.py` — turn PDB(s) into the parsed JSONL.
- `assign_fixed_chains.py` — choose which chains are designed vs. fixed.
- `make_fixed_positions_dict.py` — pin specific residues (keep catalytic/known positions).
- `make_tied_positions_dict.py` — tie positions across chains for symmetry.
- bias dictionaries — up/down-weight specific amino acids (e.g. avoid Cys).

Confirm exact script names/args for your checkout.

## Key run flags (verify per version)

| Flag | Purpose |
|------|---------|
| `--num_seq_per_target N` | sequences designed per backbone |
| `--sampling_temp "0.1"` | sampling temperature(s); lower = conservative, higher = diverse |
| `--pdb_path` / `--jsonl_path` | input structure or parsed JSONL |
| `--out_folder` | output directory |
| soluble model weights | variant biased toward soluble sequences |

## Output

A FASTA per target with several designs; headers carry the model **score** (lower is better)
and native-sequence recovery. Rank by score, then validate the top designs.

## Choosing between the design skills

- **alterlab-proteinmpnn** — sequence for a fixed backbone, no ligand context.
- **alterlab-ligandmpnn** — same idea but with ligand/metal/nucleic-acid context (pocket design).
- **alterlab-rfdiffusion** — generate the backbone itself (upstream of MPNN).
- **alterlab-esm** — generative multimodal design / ESM inverse folding.

## Design → fold → score

Feed each designed sequence to `alterlab-alphafold`, refold, and accept only self-consistent
designs (return to the intended backbone, high pLDDT, low PAE). Batch the folds via
`alterlab-remote-compute`.
