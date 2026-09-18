# ColabFold / AlphaFold2 — Usage Reference

Deeper detail for `alterlab-alphafold`. Verify commands and pins against your installed
ColabFold version before relying on them — flags shift between releases (`TODO(verify)`).

## Install

ColabFold couples a folding engine (AlphaFold2 via JAX, or an alternative) with the MMseqs2
MSA step. A common install path is the `colabfold` package with the AlphaFold extra plus a
CUDA-matched JAX build. Because JAX/CUDA pins are environment-specific, treat the exact
versions as `TODO(verify)` for your GPU/driver, and prefer the upstream `sokrypton/ColabFold`
install notes.

## MSA modes

- **API (default)** — sequences are searched against the hosted MMseqs2 server. Fastest to
  start; sends your sequence to a public service (disclose this for sensitive sequences).
- **Local database** — point ColabFold at a local MMseqs2 database for offline / private runs;
  needed on air-gapped HPC.

## Key flags (verify names per version)

| Flag | Purpose |
|------|---------|
| `--num-models N` | how many of the 5 AF2 models to run |
| `--num-recycle N` | recycling iterations (more can help hard targets) |
| `--model-type alphafold2_multimer_v3` | use the multimer models for complexes |
| `--templates` | use structural templates |
| `--amber` / `--relax` | run relaxation on the top model |
| `--msa-mode` | MSA source (API vs. local) |

## Outputs

Per FASTA record ColabFold writes: ranked relaxed/unrelaxed structures (`*_rank_00N_*.pdb` or
`.cif`), a scores JSON with `plddt` and `pae` arrays, and coverage/pLDDT/PAE plots. Rank 1 is
the highest-confidence model.

## Metric interpretation

- **pLDDT** (0–100, per residue): >90 very high, 70–90 confident, 50–70 low, <50 likely
  disordered.
- **pTM / ipTM**: global fold / interface confidence (0–1). For complexes, ipTM is the
  load-bearing number; a common "confident interface" heuristic is ipTM ≳ 0.6 (`TODO(verify)`
  against current literature for your use case).
- **PAE**: N×N expected error (Å) between residue pairs; confident relative domain/chain
  orientation shows as low off-diagonal blocks.

## Design self-consistency

For a design→fold→score loop, refold the designed sequence and accept only if it returns to
the intended backbone with high pLDDT and low PAE (compare via TM-score/RMSD). This is the
validation gate referenced by `alterlab-proteinmpnn`, `alterlab-ligandmpnn`, and
`alterlab-rfdiffusion`.

## GPU dispatch

`colabfold_batch` needs a CUDA GPU. Batch many targets as a SLURM array or a cloud GPU job via
`alterlab-remote-compute` (submit → poll `sacct`/provider status → harvest `out/`).
