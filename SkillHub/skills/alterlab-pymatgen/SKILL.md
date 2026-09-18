---
name: alterlab-pymatgen
description: Analyzes and manipulates materials with the pymatgen toolkit — crystal structures and molecules, phase diagrams and thermodynamic stability, electronic structure (band structures, DOS), surfaces and interfaces, and Materials Project database access. Use when working with crystal structures in materials science, converting between structure formats (CIF, POSCAR, XYZ), analyzing symmetry or space groups, computing phase diagrams, querying the Materials Project API, or handling VASP, Gaussian, or Quantum ESPRESSO output. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: Runs locally via `uv run python`; requires the pymatgen Python package. Materials Project database queries need a free MP_API_KEY.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Pymatgen - Python Materials Genomics

## Overview

Pymatgen is a comprehensive Python library for materials analysis that powers the
Materials Project. Create, analyze, and manipulate crystal structures and molecules;
compute phase diagrams and thermodynamic properties; analyze electronic structure (band
structures, DOS); generate surfaces and interfaces; and access the Materials Project
database. Supports 100+ file formats from various computational codes.

## When to Use This Skill

Use when:
- Working with crystal structures or molecular systems in materials science
- Converting between structure file formats (CIF, POSCAR, XYZ, etc.)
- Analyzing symmetry, space groups, or coordination environments
- Computing phase diagrams or assessing thermodynamic stability
- Analyzing electronic structure (band gaps, DOS, band structures)
- Generating surfaces/slabs or studying interfaces
- Accessing the Materials Project database programmatically
- Setting up high-throughput computational workflows
- Working with VASP, Gaussian, Quantum ESPRESSO, or other codes

## Quick Start

```bash
uv pip install pymatgen           # core
uv pip install pymatgen mp-api    # + Materials Project API access
uv pip install pymatgen[analysis] # extended analysis tools
uv pip install pymatgen[vis]      # visualization tools
```

```python
from pymatgen.core import Structure, Lattice

struct = Structure.from_file("POSCAR")        # auto format detection
struct.to(filename="structure.cif")           # write any format
print(struct.composition.reduced_formula)
print(struct.get_space_group_info())
print(f"{struct.density:.2f} g/cm³")
```

```bash
export MP_API_KEY="your_api_key_here"   # for Materials Project access
```

## Core Capabilities (routing)

Each capability has a copy-paste code block in `references/core_examples.md` and deeper
module docs in the references listed below.

1. **Structure creation & manipulation** — from files, from scratch (lattice params or
   space group), transformations (supercell, substitution, primitive). → `core_classes.md`
2. **File-format conversion** — `from_file()`/`to()` plus `scripts/structure_converter.py`
   for single/batch. → `io_formats.md`
3. **Structure analysis & symmetry** — `SpacegroupAnalyzer`, `CrystalNN`, plus
   `scripts/structure_analyzer.py`. → `analysis_modules.md`
4. **Phase diagrams & thermodynamics** — `PhaseDiagram`, energy-above-hull, decomposition,
   plus `scripts/phase_diagram_generator.py`. → `analysis_modules.md`, `transformations_workflows.md`
5. **Electronic structure** — band structures and DOS from `Vasprun`, band gaps,
   metallicity. → `analysis_modules.md`, `io_formats.md`
6. **Surfaces & interfaces** — `SlabGenerator`, `WulffShape`, `AdsorbateSiteFinder`.
   → `analysis_modules.md`, `transformations_workflows.md`
7. **Materials Project access** — `MPRester` search and retrieval with property filters.
   → `materials_project_api.md`
8. **Computational workflow setup** — VASP input sets (`MPRelaxSet`, `MPStaticSet`,
   `MPNonSCFSet`), Gaussian, Quantum ESPRESSO. → `io_formats.md`, `transformations_workflows.md`
9. **Advanced analysis** — XRD patterns, elastic tensors, magnetic ordering.
   → `analysis_modules.md`

Multi-step worked examples (high-throughput generation, band-structure pipeline, surface
energy): `references/common_workflows_code.md`.

## Bundled Resources

### Scripts (`scripts/`)

- **`structure_converter.py`**: convert between structure file formats (batch + auto
  detection). Usage: `python scripts/structure_converter.py POSCAR structure.cif`
- **`structure_analyzer.py`**: symmetry, coordination, lattice parameters, distance
  matrix. Usage: `python scripts/structure_analyzer.py structure.cif --symmetry --neighbors`
- **`phase_diagram_generator.py`**: phase diagrams from Materials Project, stability
  analysis. Usage: `python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2"`

All scripts include detailed help, e.g. `python scripts/structure_converter.py --help`

### References (`references/`)

- **`core_examples.md`**: copy-paste code for all nine core capabilities
- **`common_workflows_code.md`**: multi-step worked workflow code
- **`core_classes.md`**: Element, Structure, Lattice, Molecule, Composition classes
- **`io_formats.md`**: file-format support and code integration (VASP, Gaussian, etc.)
- **`analysis_modules.md`**: phase diagrams, surfaces, electronic structure, symmetry
- **`materials_project_api.md`**: complete Materials Project API guide
- **`transformations_workflows.md`**: transformations framework and 10 common workflows

## Best Practices

**Structures**: use auto format detection; prefer `IStructure` when immutable; reduce to
primitive cell with `SpacegroupAnalyzer`; validate for overlapping atoms / bad bond
lengths. **File I/O**: prefer `from_file()`/`to()`; specify format when detection fails;
use `as_dict()`/`from_dict()` for version-safe storage. **MP API**: always use the context
manager; batch queries; cache results; filter by property. **Workflows**: prefer input
sets over manual INCAR; verify convergence; track transformations for provenance.
**Performance**: use primitive cells; bound neighbor-search cutoffs; parallelize where
possible.

## Units and Conventions

Lengths in Å, energies in eV, angles in degrees, magnetic moments in μB, time in fs.
Convert with `pymatgen.core.units`.

## Integration

Integrates with ASE, Phonopy, BoltzTraP, Atomate/Fireworks, AiiDA, Zeo++, and OpenBabel.

## Troubleshooting

- **Import errors**: `uv pip install pymatgen[analysis,vis]`
- **API key not found**: `export MP_API_KEY="your_key_here"`
- **Structure read failures**: try explicit format, e.g. `Structure.from_file("file.txt", fmt="cif")`
- **Symmetry analysis fails**: increase tolerance, e.g. `SpacegroupAnalyzer(struct, symprec=0.1)`

## Additional Resources

Docs: https://pymatgen.org/ · Materials Project: https://materialsproject.org/ ·
GitHub: https://github.com/materialsproject/pymatgen · Forum: https://matsci.org/ ·
Example notebooks: https://matgenb.materialsvirtuallab.org/

## Version Notes

Designed for pymatgen 2024.x and later. For the Materials Project API, use the `mp-api`
package (separate from legacy `pymatgen.ext.matproj`). Requirements: Python ≥ 3.10,
pymatgen ≥ 2023.x, mp-api (for Materials Project access).
