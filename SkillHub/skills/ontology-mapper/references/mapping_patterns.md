# Common CMSO Mapping Patterns

## FCC Copper

Input: `{"material": "copper", "structure": "FCC", "space_group": 225, "lattice_a": 3.615}`

Mapping:
- **Computational Sample** -> **Atomic Scale Sample**
- **Material** -> **Crystalline Material**
- **Crystal Structure** -> hasSpaceGroup (225, "Fm-3m")
- **Unit Cell** -> hasBravaisLattice "cF", hasLength_x 3.615
- **Chemical Element** -> hasChemicalSymbol "Cu"

## BCC Iron

Input: `{"material": "iron", "structure": "BCC", "space_group": 229, "lattice_a": 2.87}`

Mapping:
- **Material** -> **Crystalline Material**
- **Unit Cell** -> hasBravaisLattice "cI", hasLength_x 2.87
- **Space Group** -> hasSpaceGroupNumber 229
- **Chemical Element** -> hasChemicalSymbol "Fe"

## Hexagonal Titanium

Input: `{"material": "titanium", "system": "hexagonal", "lattice_a": 2.95, "lattice_c": 4.68, "space_group": 194}`

Mapping:
- **Material** -> **Crystalline Material**
- **Unit Cell** -> hasBravaisLattice "hP", hasLength_x 2.95, hasLength_z 4.68
- **Space Group** -> hasSpaceGroupNumber 194

## Polycrystalline Steel

Input: `{"material": "polycrystalline steel", "elements": ["Fe", "C", "Mn"]}`

Mapping:
- **Material** -> **Polycrystal**
- **Chemical Element** (x3): Fe, C, Mn

## Amorphous SiO2

Input: `{"material": "amorphous SiO2", "elements": ["Si", "O"]}`

Mapping:
- **Material** -> **Amorphous Material**
- No Crystal Structure, Unit Cell, or Space Group
- **Chemical Element** (x2): Si, O

## Property Mapping Reference

| Input field | CMSO Property | CMSO Class |
|-------------|--------------|------------|
| `lattice_a` | has length x | Unit Cell |
| `lattice_b` | has length y | Unit Cell |
| `lattice_c` | has length z | Unit Cell |
| `alpha` | has angle alpha | Angle |
| `beta` | has angle beta | Angle |
| `gamma` | has angle gamma | Angle |
| `space_group` | has space group number | Crystal Structure |
| `structure` / `bravais` | has Bravais lattice | Unit Cell |
| `elements` | has chemical symbol | Chemical Element |
| `num_atoms` | has number of atoms | Atomic Scale Sample |
