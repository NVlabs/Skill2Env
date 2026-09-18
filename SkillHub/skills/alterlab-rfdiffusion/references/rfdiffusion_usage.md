# RFdiffusion — Usage Reference

Deeper detail for `alterlab-rfdiffusion`. Verify config keys, the contig grammar, and weights
against the upstream `RosettaCommons/RFdiffusion` README (`TODO(verify)`) — RFdiffusion uses a
Hydra config and the syntax is version-specific.

## Install

Clone `RosettaCommons/RFdiffusion`, install its environment (PyTorch + the SE(3)-transformer
dependency), and download model weights per its instructions (several GB, no account). A CUDA
GPU is required for practical generation.

## Contig map

`contigmap.contigs` is the core control:

- `'[100-100]'` — a single 100-residue chain (unconditional).
- ranges + fixed segments — mix generated lengths with fixed motif residues from an input PDB
  for **motif scaffolding**.
- multiple chains / symmetry blocks — for complexes and symmetric assemblies.

Confirm the exact contig grammar and symmetry keys for your version.

## Common modes (verify keys per version)

| Mode | Config sketch |
|------|---------------|
| Unconditional | `contigmap.contigs=[N-N]`, `inference.num_designs=K` |
| Motif scaffolding | fixed motif ranges + generated segments; `inference.input_pdb` |
| Binder design | target PDB + `ppi.hotspot_res=[...]` |
| Symmetric | symmetry config (cyclic/dihedral) |

## Outputs

Backbone PDBs (no sequence) plus trajectory/metadata. These are the input to sequence design.

## Design → fold → score

1. **Generate** backbones (RFdiffusion).
2. **Sequence** with `alterlab-proteinmpnn` (or `alterlab-ligandmpnn` when a ligand/metal is
   part of the site).
3. **Validate** by refolding with `alterlab-alphafold`; for binders, read ipTM at the
   interface. Keep only self-consistent designs.

Generation and the fold sweep are GPU-heavy — dispatch both via `alterlab-remote-compute`
(submit → poll → harvest).

## Choosing between the skills

- **alterlab-rfdiffusion** — make the backbone / scaffold a motif / design a binder backbone.
- **alterlab-proteinmpnn** / **alterlab-ligandmpnn** — sequence for a backbone (± ligand).
- **alterlab-alphafold** — fold/validate a sequence.
- **alterlab-esm** — generative multimodal design as an alternative paradigm.
