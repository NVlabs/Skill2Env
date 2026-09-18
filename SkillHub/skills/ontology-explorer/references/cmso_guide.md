# CMSO — Computational Material Sample Ontology Guide

## Overview

CMSO describes computational material samples (structures used in simulations) at the atomic scale. It provides a standardized vocabulary for crystal structures, chemical composition, simulation cells, and crystallographic defects.

- **IRI**: `http://purls.helmholtz-metadaten.de/cmso/`
- **Version**: 0.0.1
- **License**: CC-BY-4.0
- **Repository**: https://github.com/OCDO/cmso
- **Documentation**: https://ocdo.github.io/cmso/

## Domain Model

The core chain of relationships in CMSO:

```
ComputationalSample
  ├── hasMaterial ─────→ Material
  │                        └── hasStructure ──→ Structure
  │                                               └── (CrystalStructure)
  │                                                     ├── hasUnitCell ──→ UnitCell
  │                                                     │                    ├── hasBasis ──→ Basis
  │                                                     │                    ├── hasLatticeParameter ──→ LatticeParameter
  │                                                     │                    └── hasBravaisLattice (string)
  │                                                     └── hasSpaceGroup ──→ SpaceGroup
  ├── hasSimulationCell ──→ SimulationCell
  │                           ├── hasVector ──→ SimulationCellVector
  │                           ├── hasAngle ──→ SimulationCellAngle
  │                           └── hasVolume (float)
  ├── hasSpecies ─────→ ChemicalSpecies
  │                       └── hasElement ──→ ChemicalElement
  └── hasAttribute ───→ AtomAttribute (AtomicPosition, AtomicVelocity, ...)
```

## Class Hierarchy

### Computational Samples (by length scale)

```
ComputationalSample
├── Atomic Scale Sample      ← primary focus of CMSO
├── Nanoscale Sample
├── Microscale Sample
├── Mesoscale Sample
└── Macroscale Sample
```

### Materials

```
Material
├── Crystalline Material
│   ├── Bicrystal
│   └── Polycrystal
└── Amorphous Material
```

### Structure

```
Structure
├── Crystal Structure        ← linked to UnitCell, SpaceGroup
└── Microstructure
```

### Chemical Species

```
Chemical Species
├── Atom
└── Molecule
```

### Atomic Attributes

```
Atom Attribute
├── Atomic Position          ← Cartesian coordinates preferred
├── Atomic Velocity
├── Atomic Force
├── Coordination Number
└── Occupancy
```

### Vectors and Angles

```
Vector                          Angle
├── Lattice Vector              ├── Lattice Angle
├── Simulation Cell Vector      └── Simulation Cell Angle
└── Normal Vector
```

## Key Properties by Class

### ComputationalSample
| Property | Type | Target | Description |
|----------|------|--------|-------------|
| hasMaterial | object | Material | The material this sample represents |
| hasSpecies | object | ChemicalSpecies | Chemical species present |

### AtomicScaleSample (extends ComputationalSample)
| Property | Type | Target | Description |
|----------|------|--------|-------------|
| hasSimulationCell | object | SimulationCell | The computational box |
| hasAttribute | object | AtomAttribute | Per-atom properties |
| hasNumberOfAtoms | data | integer | Total atom count |

### CrystalStructure
| Property | Type | Target | Description |
|----------|------|--------|-------------|
| hasUnitCell | object | UnitCell | The repeating unit |
| hasSpaceGroup | object | SpaceGroup | Symmetry group |

### UnitCell
| Property | Type | Target | Description |
|----------|------|--------|-------------|
| hasBasis | object | Basis | Atom arrangement |
| hasLatticeParameter | object | LatticeParameter | Cell dimensions |
| hasBravaisLattice | data | string | One of 14 Bravais lattice types |
| hasVector | object | Vector | Lattice vectors |
| hasAngle | object | Angle | Lattice angles |

### SimulationCell
| Property | Type | Target | Description |
|----------|------|--------|-------------|
| hasVector | object | Vector | Cell vectors |
| hasAngle | object | Angle | Cell angles |
| hasVolume | data | float | Cell volume |
| hasRepetition_x/y/z | data | integer | How many unit cells in each direction |

### ChemicalElement
| Property | Type | Target | Description |
|----------|------|--------|-------------|
| hasChemicalSymbol | data | string | Element symbol (e.g., "Cu") |
| hasAtomicPercent | data | float | Atomic fraction |
| hasWeightPercent | data | float | Weight fraction |
| hasElementRatio | data | float | Ratio (0-1) |

### SpaceGroup
| Property | Type | Target | Description |
|----------|------|--------|-------------|
| hasSpaceGroupNumber | data | integer | 1-230 |
| hasSpaceGroupSymbol | data | string | Hermann-Mauguin symbol |

## Common Usage Patterns

### Describing FCC Copper
- **Material**: CrystallineMaterial
- **Structure**: CrystalStructure → hasSpaceGroup (225, "Fm-3m")
- **UnitCell**: hasBravaisLattice "cF" (face-centered cubic), lattice a=b=c=3.615 Å, α=β=γ=90°
- **Species**: Atom → ChemicalElement (Cu)

### Describing a Polycrystalline Steel
- **Material**: Polycrystal (subclass of CrystallineMaterial)
- **SimulationCell**: hasNumberOfGrains, hasGrainSize
- **Species**: multiple ChemicalElements (Fe, C, ...)

### Describing an Amorphous Structure
- **Material**: AmorphousMaterial
- **No CrystalStructure** (no unit cell, space group, or Bravais lattice)
- **SimulationCell**: still has vectors, angles, volume

## Related Ontologies (OCDO Ecosystem)

| Ontology | Acronym | Focus |
|----------|---------|-------|
| Atomistic Simulation Methods Ontology | ASMO | Simulation methods (DFT, MD, MC) |
| Crystallographic Defect Core Ontology | CDCO | Core defect vocabulary |
| Point Defect Ontology | PODO | Vacancies, interstitials |
| Plane Defect Ontology | PLDO | Grain boundaries, stacking faults |
| Line Defect Ontology | LDO | Dislocations |

CMSO's `Material` class is equivalent to CDCO's `Material` class, enabling seamless integration of defect descriptions with sample descriptions.
