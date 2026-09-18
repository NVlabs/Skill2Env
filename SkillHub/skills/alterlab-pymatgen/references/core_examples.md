# Core Capability Examples

Copy-paste pymatgen snippets for the nine core capabilities, extracted from the skill
body. Deeper module docs live in `core_classes.md`, `io_formats.md`,
`analysis_modules.md`, and `materials_project_api.md`.

## 1. Structure Creation and Manipulation

**From files:**
```python
# Automatic format detection
struct = Structure.from_file("structure.cif")
struct = Structure.from_file("POSCAR")
mol = Molecule.from_file("molecule.xyz")
```

**From scratch:**
```python
from pymatgen.core import Structure, Lattice

# Using lattice parameters
lattice = Lattice.from_parameters(a=3.84, b=3.84, c=3.84,
                                  alpha=120, beta=90, gamma=60)
coords = [[0, 0, 0], [0.75, 0.5, 0.75]]
struct = Structure(lattice, ["Si", "Si"], coords)

# From space group
struct = Structure.from_spacegroup(
    "Fm-3m",
    Lattice.cubic(3.5),
    ["Si"],
    [[0, 0, 0]]
)
```

**Transformations:**
```python
from pymatgen.transformations.standard_transformations import (
    SupercellTransformation,
    SubstitutionTransformation,
    PrimitiveCellTransformation
)

# Create supercell
trans = SupercellTransformation([[2,0,0],[0,2,0],[0,0,2]])
supercell = trans.apply_transformation(struct)

# Substitute elements
trans = SubstitutionTransformation({"Fe": "Mn"})
new_struct = trans.apply_transformation(struct)

# Get primitive cell
trans = PrimitiveCellTransformation()
primitive = trans.apply_transformation(struct)
```

See `core_classes.md` for Structure, Lattice, Molecule, and related classes.

## 2. File Format Conversion

```python
# Read any format
struct = Structure.from_file("input_file")

# Write to any format
struct.to(filename="output.cif")
struct.to(filename="POSCAR")
struct.to(filename="output.xyz")
```

```bash
# Single file conversion
python scripts/structure_converter.py POSCAR structure.cif

# Batch conversion
python scripts/structure_converter.py *.cif --output-dir ./poscar_files --format poscar
```

See `io_formats.md` for all supported formats and code integrations.

## 3. Structure Analysis and Symmetry

```python
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

sga = SpacegroupAnalyzer(struct)
print(f"Space group: {sga.get_space_group_symbol()}")
print(f"Number: {sga.get_space_group_number()}")
print(f"Crystal system: {sga.get_crystal_system()}")

conventional = sga.get_conventional_standard_structure()
primitive = sga.get_primitive_standard_structure()
```

```python
from pymatgen.analysis.local_env import CrystalNN

cnn = CrystalNN()
neighbors = cnn.get_nn_info(struct, n=0)  # Neighbors of site 0
print(f"Coordination number: {len(neighbors)}")
for neighbor in neighbors:
    site = struct[neighbor['site_index']]
    print(f"  {site.species_string} at {neighbor['weight']:.3f} Å")
```

```bash
python scripts/structure_analyzer.py POSCAR --symmetry --neighbors
python scripts/structure_analyzer.py structure.cif --symmetry --export json
```

See `analysis_modules.md` for all analysis capabilities.

## 4. Phase Diagrams and Thermodynamics

```python
from mp_api.client import MPRester
from pymatgen.analysis.phase_diagram import PhaseDiagram, PDPlotter

with MPRester() as mpr:
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")

pd = PhaseDiagram(entries)

from pymatgen.core import Composition
comp = Composition("LiFeO2")

for entry in entries:
    if entry.composition.reduced_formula == comp.reduced_formula:
        e_above_hull = pd.get_e_above_hull(entry)
        print(f"Energy above hull: {e_above_hull:.4f} eV/atom")
        if e_above_hull > 0.001:
            decomp = pd.get_decomposition(comp)
            print("Decomposes to:", decomp)

plotter = PDPlotter(pd)
plotter.show()
```

```bash
python scripts/phase_diagram_generator.py Li-Fe-O --output li_fe_o.png
python scripts/phase_diagram_generator.py Li-Fe-O --analyze "LiFeO2" --show
```

See the Phase Diagrams section of `analysis_modules.md` and Workflow 2 in
`transformations_workflows.md`.

## 5. Electronic Structure Analysis

```python
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter

vasprun = Vasprun("vasprun.xml")
bs = vasprun.get_band_structure()

band_gap = bs.get_band_gap()
print(f"Band gap: {band_gap['energy']:.3f} eV")
print(f"Direct: {band_gap['direct']}")
print(f"Is metal: {bs.is_metal()}")

plotter = BSPlotter(bs)
plotter.save_plot("band_structure.png")
```

```python
from pymatgen.electronic_structure.plotter import DosPlotter

dos = vasprun.complete_dos
element_dos = dos.get_element_dos()
for element, element_dos_obj in element_dos.items():
    print(f"{element}: {element_dos_obj.get_gap():.3f} eV")

plotter = DosPlotter()
plotter.add_dos("Total DOS", dos)
plotter.show()
```

See the Electronic Structure section of `analysis_modules.md` and the VASP section of
`io_formats.md`.

## 6. Surface and Interface Analysis

```python
from pymatgen.core.surface import SlabGenerator

slabgen = SlabGenerator(
    struct,
    miller_index=(1, 1, 1),
    min_slab_size=10.0,      # Å
    min_vacuum_size=10.0,    # Å
    center_slab=True
)
slabs = slabgen.get_slabs()
for i, slab in enumerate(slabs):
    slab.to(filename=f"slab_{i}.cif")
```

```python
from pymatgen.analysis.wulff import WulffShape

surface_energies = {
    (1, 0, 0): 1.0,
    (1, 1, 0): 1.1,
    (1, 1, 1): 0.9,
}
wulff = WulffShape(struct.lattice, surface_energies)
print(f"Surface area: {wulff.surface_area:.2f} Ų")
print(f"Volume: {wulff.volume:.2f} ų")
wulff.show()
```

```python
from pymatgen.analysis.adsorption import AdsorbateSiteFinder
from pymatgen.core import Molecule

asf = AdsorbateSiteFinder(slab)
ads_sites = asf.find_adsorption_sites()
print(f"On-top sites: {len(ads_sites['ontop'])}")
print(f"Bridge sites: {len(ads_sites['bridge'])}")
print(f"Hollow sites: {len(ads_sites['hollow'])}")

adsorbate = Molecule("O", [[0, 0, 0]])
ads_struct = asf.add_adsorbate(adsorbate, ads_sites["ontop"][0])
```

See the Surface and Interface section of `analysis_modules.md` and Workflows 3 and 9 in
`transformations_workflows.md`.

## 7. Materials Project Database Access

Setup: get an API key from https://next-gen.materialsproject.org/ and set
`export MP_API_KEY="your_key_here"`.

```python
from mp_api.client import MPRester

with MPRester() as mpr:
    materials = mpr.materials.summary.search(formula="Fe2O3")
    materials = mpr.materials.summary.search(chemsys="Li-Fe-O")
    materials = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.05),  # Stable/metastable
        band_gap=(1.0, 3.0)            # Semiconducting
    )
    struct = mpr.get_structure_by_material_id("mp-149")
    bs = mpr.get_bandstructure_by_material_id("mp-149")
    entries = mpr.get_entries_in_chemsys("Li-Fe-O")
```

See `materials_project_api.md` for comprehensive API documentation.

## 8. Computational Workflow Setup

```python
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet, MPNonSCFSet

MPRelaxSet(struct).write_input("./relax_calc")
MPStaticSet(struct).write_input("./static_calc")
MPNonSCFSet(struct, mode="line").write_input("./bandstructure_calc")

# Custom parameters
MPRelaxSet(struct, user_incar_settings={"ENCUT": 600}).write_input("./custom_calc")
```

```python
# Gaussian
from pymatgen.io.gaussian import GaussianInput
GaussianInput(mol, functional="B3LYP", basis_set="6-31G(d)",
              route_parameters={"Opt": None}).write_file("input.gjf")

# Quantum ESPRESSO
from pymatgen.io.pwscf import PWInput
PWInput(struct, control={"calculation": "scf"}).write_file("pw.in")
```

See the Electronic Structure Code I/O section of `io_formats.md` and
`transformations_workflows.md`.

## 9. Advanced Analysis

```python
# Diffraction patterns
from pymatgen.analysis.diffraction.xrd import XRDCalculator
xrd = XRDCalculator(wavelength="CuKa")
pattern = xrd.get_pattern(struct)
# pattern.x = 2θ (deg), pattern.y = intensity, pattern.hkls[i] = list of hkl dicts for peak i
for two_theta, intensity, hkl_info in zip(pattern.x, pattern.y, pattern.hkls):
    hkls = ", ".join(str(h["hkl"]) for h in hkl_info)
    print(f"2θ = {two_theta:.2f}°, I = {intensity:.1f}, hkl = {hkls}")
pattern.plot()
```

```python
# Elastic properties
from pymatgen.analysis.elasticity import ElasticTensor
elastic_tensor = ElasticTensor.from_voigt(matrix)
print(f"Bulk modulus: {elastic_tensor.k_voigt:.1f} GPa")
print(f"Shear modulus: {elastic_tensor.g_voigt:.1f} GPa")
print(f"Young's modulus: {elastic_tensor.y_mod:.1f} GPa")
```

```python
# Magnetic ordering
from pymatgen.transformations.advanced_transformations import MagOrderingTransformation
trans = MagOrderingTransformation({"Fe": 5.0})
mag_structs = trans.apply_transformation(struct, return_ranked_list=True)
lowest_energy_struct = mag_structs[0]['structure']
```

See `analysis_modules.md` for comprehensive analysis module documentation.
