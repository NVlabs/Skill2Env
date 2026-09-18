# Chai-1 — Usage Reference

Deeper detail for `alterlab-chai`. Verify the FASTA type-tag syntax, restraint format, flags,
and package pin against your installed `chai_lab` version (`TODO(verify)`), using the upstream
`chaidiscovery/chai-lab` README as the source of truth.

## Install

Install the `chai_lab` package into a CUDA-enabled environment; weights download on first run
and cache locally. The torch/CUDA build is environment-specific — `TODO(verify)`.

## Input: one typed FASTA

Chai-1 takes a single FASTA whose records are typed by entity. Types include `protein`,
`ligand` (SMILES), `rna`, and `dna`. The exact header/type-tag convention has varied across
releases — confirm against the installed version before scripting. A Python API is also
available (`chai_lab.chai1`) if you prefer to build inputs programmatically.

## MSAs

Chai-1 can run single-sequence or with MSAs. MSAs typically improve accuracy at a time cost.
If MSAs are fetched from a hosted service, disclose it for sensitive sequences; supply local
MSAs to stay offline.

## Restraints

Chai-1 accepts restraints (e.g. contacts) to bias predictions toward known biology — valuable
for antibody–antigen when you have partial epitope information. `TODO(verify)` the restraint
file format for your version.

## Outputs

Predicted complex structure(s) (mmCIF/PDB) with per-model and per-entity confidence, including
an interface score for judging contacts. Rank by confidence and inspect the interface.

## Choosing between the folding skills

| Task | Skill |
|------|-------|
| Antibody–antigen; mixed one-FASTA assembly | `alterlab-chai` |
| Protein–ligand co-fold **with binding affinity** | `alterlab-boltz` |
| Protein / protein–protein only (AF2 confidence) | `alterlab-alphafold` |
| Ligand pose into a **fixed** receptor (docking) | `alterlab-diffdock` |

## GPU dispatch

Batch an antibody panel against one antigen as separate predictions via
`alterlab-remote-compute` (submit → poll → harvest).
