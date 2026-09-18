# ASMO — Atomistic Simulation Methods Ontology

## Overview

ASMO describes **how** atomistic simulations are performed: the computational methods, algorithms, potentials, input parameters, and calculated properties. It complements CMSO (which describes **what** is being simulated — the material sample) by capturing the simulation methodology.

- **IRI**: `http://purls.helmholtz-metadaten.de/asmo/`
- **Version**: 1.0.0
- **License**: CC BY 4.0
- **105 classes** | **25 object properties** | **16 data properties**

> **Note on named individuals:** The ASMO documentation describes specific implementations (e.g., Nose-Hoover thermostat, Parrinello-Rahman barostat, NVT/NPT/NVE ensembles) as conceptual instances. However, the current OWL file does **not** declare these as `owl:Class` or `owl:NamedIndividual`. They are listed in the Usage Patterns section below for reference, but programmatic queries should use the parent classes (Thermostat, Barostat, Statistical Ensemble).

## Domain Model

```
Simulation (Activity)
├── uses → Computational Method (DFT, MD, MC, Molecular Statics, AIMD)
├── uses → Interatomic Potential (LJ, EAM, MEAM, ML, Force Field, SW)
├── uses → Simulation Algorithm (Thermostat, Barostat, EOS Fitting, ...)
├── has → Statistical Ensemble
├── has → Input Parameter (Energy Cutoff, KPoint Mesh, Time Step, PBC)
├── has → Output Parameter
├── produces → Calculated Property (Energy, Moduli, Strain, Stress, ...)
└── acts on → Computational Sample (from CMSO)
```

## Class Hierarchy

### Computational Methods
```
Computational Method
├── Ab Initio Molecular Dynamics (AIMD)
├── Density Functional Theory (DFT)
├── Molecular Dynamics (MD)
├── Molecular Statics
└── Monte Carlo Method
    └── Kinetic Monte Carlo Method
```

### Interatomic Potentials
```
Interatomic Potential
├── Embedded Atom Model (EAM)
├── Force Field
├── Lennard-Jones Potential
├── Machine Learning Potential
├── Modified Embedded Atom Model (MEAM)
└── Stillinger-Weber Potential
```

### Simulation Algorithms
```
Simulation Algorithm
├── ANNNI Model
├── Barostat
├── Compression Test
├── Equation of State Fit
├── Nanoindentation
├── Quasi-Harmonic Approximation
├── Tensile Test
├── Thermodynamic Integration
└── Thermostat
```

Common implementations (described in ASMO documentation, not formal OWL classes):
- Thermostats: Andersen, Berendsen, Nose-Hoover, Langevin
- Barostats: Andersen, Berendsen, Parrinello-Rahman
- EOS models: Birch-Murnaghan, Murnaghan, Vinet, Rose

### Statistical Ensembles

The `Statistical Ensemble` class has no formal subclasses in the OWL file. Common ensemble types described in the ASMO documentation:
- Microcanonical Ensemble (NVE)
- Canonical Ensemble (NVT)
- Isothermal-Isobaric Ensemble (NPT)
- Grand Canonical Ensemble

### Calculated Properties
```
Calculated Property
├── Bulk Modulus
├── Elastic Constant
├── Elastic Tensor
├── Flow Stress
├── Formation Energy
├── Kinetic Energy
├── Poisson's Ratio
├── Potential Energy
├── Shear Modulus
├── Simulation Cell Length
├── Simulation Cell Volume
├── Specific Heat Capacity
├── Strain
├── Thermal Expansion Coefficient
├── Thermodynamic Free Energy
│   ├── Gibbs Free Energy
│   └── Helmholtz Free Energy
├── Total Energy
├── Total Magnetic Moment
├── Virial Pressure
├── Yield Stress
└── Young's Modulus
```

### Physical Quantities
```
Physical Quantity
├── Energy
│   └── Free Energy
├── Force
├── Length
├── Mass
├── Pressure
├── Stress
├── Temperature
├── Time
│   ├── Simulation Run Time
│   └── Simulation Time
└── Volume
```

### Input Parameters
```
Input Parameter
├── Energy Cutoff
├── KPoint Mesh
├── Number Of Ionic Steps
├── Periodic Boundary Condition
├── Strain Rate
├── Time Step
└── Volume Range
```

### Exchange Correlation Functionals (from MDO)
```
Exchange Correlation Energy Functional
├── Generalized Gradient Approximation (GGA)
├── Hybrid Functional
│   ├── Hybrid Generalized Gradient Approximation
│   └── Hybrid Meta Generalized Gradient Approximation
├── Local Density Approximation (LDA)
└── Meta Generalized Gradient Approximation
```

### Structure Manipulation
```
Structure Manipulation (Activity)
├── Point Defect Creation
└── Spatial Transformation
    ├── Rotation
    ├── Shear
    └── Translation
```

### Mathematical Operations
```
Mathematical Operation (Activity)
├── Addition
├── Division
├── Exponentiation
├── Multiplication
└── Subtraction
```

## Key Object Properties

| Property | Domain | Range | Purpose |
|----------|--------|-------|---------|
| `has computational method` | Activity | Computational Method | Link simulation to its method |
| `has interatomic potential` | Activity | Interatomic Potential | Link simulation to potential used |
| `uses simulation algorithm` | Simulation | Simulation Algorithm | Link to thermostat, barostat, etc. |
| `has statistical ensemble` | Activity | Statistical Ensemble | Ensemble used in the simulation |
| `has input parameter` | Simulation | Input Parameter | Energy cutoff, k-points, etc. |
| `has output parameter` | Simulation | Output Parameter | Simulation outputs |
| `has calculated property` | Computational Sample | Calculated Property | Results on the sample |
| `was calculated by` | Calculated Property | Activity | Provenance of a result |
| `has unit` | (any) | Unit | Physical units (via QUDT) |
| `has XC functional` | DFT | XC Functional | Exchange-correlation choice |
| `has relaxation DOF` | Energy Calculation | Relaxation Degrees of Freedom | Relaxation constraints |

## Relationship to CMSO

ASMO imports from CMSO:
- `Computational Sample` — the material being simulated
- `Simulation Cell` — the periodic box
- `Plane`, `Vector` — geometric primitives

**Typical usage pattern**: CMSO describes the sample (crystal structure, composition, defects), ASMO describes what you do with it (DFT calculation, MD simulation with EAM potential).

## Usage Patterns

### DFT Energy Calculation
```
Simulation → Energy Calculation
  has computational method → Density Functional Theory
  has XC functional → Generalized Gradient Approximation (e.g., PBE)
  has input parameter → Energy Cutoff (500 eV)
  has input parameter → KPoint Mesh
  has calculated property → Total Energy
  has calculated property → Formation Energy
```

### MD Simulation
```
Simulation
  has computational method → Molecular Dynamics
  has interatomic potential → Embedded Atom Model
  uses simulation algorithm → Thermostat (e.g., Nose-Hoover)
  uses simulation algorithm → Barostat (e.g., Parrinello-Rahman)
  has statistical ensemble → Statistical Ensemble (e.g., NPT)
  has input parameter → Time Step
  has calculated property → Kinetic Energy, Potential Energy
```

### Elastic Constants Calculation
```
Simulation → Energy Calculation
  has computational method → Density Functional Theory
  has calculated property → Elastic Tensor
  has calculated property → Bulk Modulus
  has calculated property → Shear Modulus
  has calculated property → Young's Modulus
  has calculated property → Poisson's Ratio
```
