---
name: alterlab-rdkit
description: Provides the RDKit cheminformatics toolkit for low-level, fine-grained molecular primitives — SMILES/SDF parsing, descriptors (MW, LogP, TPSA), fingerprints, substructure/SMARTS search, 2D/3D coordinate generation, similarity, and reaction handling. Use when custom sanitization, specialized fingerprint or descriptor algorithms, reaction enumeration, or conformer generation demand direct API control; for a high-level pandas-friendly wrapper over RDKit prefer alterlab-datamol, and for turning molecules into ML feature vectors prefer alterlab-molfeat. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with the skill's Python package installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# RDKit Cheminformatics Toolkit

## Overview

RDKit is a comprehensive cheminformatics library providing Python APIs for molecular analysis and manipulation. This skill provides guidance for reading/writing molecular structures, calculating descriptors, fingerprinting, substructure searching, chemical reactions, 2D/3D coordinate generation, and molecular visualization. Use this skill for drug discovery, computational chemistry, and cheminformatics research tasks.

## When to Use

Reach for this skill when you need fine-grained molecular control: custom sanitization, specialized fingerprints or descriptors, reaction enumeration, conformer generation, or programmatic drawing. For standard, high-level workflows with a simpler interface, prefer **datamol** (a wrapper around RDKit).

## Core Capabilities

RDKit exposes twelve capability areas. Each is summarized below with the single most common call; **complete, runnable recipes for every area live in `references/code_recipes.md`.**

### 1. Molecular I/O and Creation

Read and write molecules across SMILES, MOL/SDF, MOL2, PDB, and InChI. Batch-process with Supplier/Writer objects, including `ForwardSDMolSupplier` and `MultithreadedSDMolSupplier` for large or gzipped files.

```python
from rdkit import Chem
mol = Chem.MolFromSmiles('Cc1ccccc1')   # returns Mol or None
smiles = Chem.MolToSmiles(mol)          # canonical SMILES
```

Every `MolFrom*` function returns `None` on failure — always check before use. Molecules are auto-sanitized on import.

### 2. Molecular Sanitization and Validation

Parsing runs a 13-step sanitization (valence checks, aromaticity perception, chirality assignment). Control it with `sanitize=False`, `SanitizeMol`, partial `sanitizeOps`, and diagnose failures with `DetectChemistryProblems`.

```python
mol = Chem.MolFromSmiles('C1=CC=CC=C1', sanitize=False)
problems = Chem.DetectChemistryProblems(mol)
```

Common failure modes: valence overflow, kekulization errors on invalid aromatic rings, and unassigned radicals.

### 3. Molecular Analysis and Properties

Iterate atoms/bonds, query ring membership (`GetRingInfo`, `GetSymmSSSR`), inspect stereochemistry (`FindMolChiralCenters`, `AssignStereochemistryFrom3D`, `bond.GetStereo`), and decompose structures (`GetMolFrags`, `FragmentOnBonds`, Murcko scaffolds).

```python
for atom in mol.GetAtoms():
    print(atom.GetSymbol(), atom.GetIdx(), atom.GetDegree())
```

### 4. Molecular Descriptors and Properties

Compute individual descriptors (`MolWt`, `MolLogP`, `TPSA`, `NumHDonors`, `NumHAcceptors`, `NumRotatableBonds`) or all at once with `CalcMolDescriptors`. Supports Lipinski Rule-of-Five drug-likeness checks.

```python
from rdkit.Chem import Descriptors
all_descriptors = Descriptors.CalcMolDescriptors(mol)   # dict of every descriptor
```

The full catalog of available descriptors is documented in `references/descriptors_reference.md`.

### 5. Fingerprints and Molecular Similarity

Generate RDKit topological, Morgan (ECFP-like), MACCS, atom-pair, topological-torsion, and Avalon fingerprints via `rdFingerprintGenerator`. Compare with Tanimoto/Dice/Cosine (and bulk variants), and cluster with Butina.

```python
from rdkit.Chem import rdFingerprintGenerator
from rdkit import DataStructs
gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
sim = DataStructs.TanimotoSimilarity(gen.GetFingerprint(mol1), gen.GetFingerprint(mol2))
```

### 6. Substructure Searching and SMARTS

Match SMARTS queries with `HasSubstructMatch`, `GetSubstructMatch`, and `GetSubstructMatches`. Remember that unspecified query properties match anything, and aromatic/charged query atoms won't match aliphatic/uncharged targets.

```python
query = Chem.MolFromSmarts('C(=O)[OH]')   # carboxylic acid
matches = mol.GetSubstructMatches(query)
```

A curated library of functional-group, ring, pharmacophore, and PAINS SMARTS patterns is in `references/smarts_patterns.md`.

### 7. Chemical Reactions

Define transformations as reaction SMARTS (`reactants >> products`), apply with `RunReactants`, and compute reaction similarity via difference fingerprints. Atom mapping preserves atom identity across the transform.

```python
from rdkit.Chem import AllChem
rxn = AllChem.ReactionFromSmarts('[C:1]=[O:2]>>[C:1][O:2]')
products = rxn.RunReactants((mol,))
```

### 8. 2D and 3D Coordinate Generation

Generate 2D depiction coordinates (`Compute2DCoords`, template alignment) and 3D conformers via ETKDG (`EmbedMolecule`, `EmbedMultipleConfs`), optimize with UFF/MMFF, and align/compare conformers by RMSD.

```python
from rdkit.Chem import AllChem
AllChem.EmbedMolecule(mol, randomSeed=42)
AllChem.MMFFOptimizeMolecule(mol)
```

### 9. Molecular Visualization

Render molecules to PIL images, files, or grids (`MolToImage`, `MolToFile`, `MolsToGridImage`), highlight substructures, customize drawings via `MolDraw2DCairo`, integrate with Jupyter, and visualize fingerprint bits.

```python
from rdkit.Chem import Draw
img = Draw.MolsToGridImage([mol1, mol2], molsPerRow=2, subImgSize=(200, 200))
```

### 10. Molecular Modification

Add/remove hydrogens (`AddHs`/`RemoveHs`), kekulize or reset aromaticity, replace substructures (`ReplaceSubstructs`), and neutralize charges with `rdMolStandardize.Uncharger`.

```python
mol_h = Chem.AddHs(mol)   # explicit hydrogens for 3D work or H-dependent properties
```

### 11. Molecular Hashes and Standardization

Generate canonical, scaffold, and regioisomer hashes with `rdMolHash.MolHash`, and produce randomized SMILES for ML data augmentation.

```python
from rdkit.Chem import rdMolHash
scaffold_hash = rdMolHash.MolHash(mol, rdMolHash.HashFunction.MurckoScaffold)
```

### 12. Pharmacophore and 3D Features

Build a feature factory from `BaseFeatures.fdef` and extract pharmacophore features (donors, acceptors, aromatic, hydrophobic) with `GetFeaturesForMol`.

```python
from rdkit.Chem import ChemicalFeatures
features = factory.GetFeaturesForMol(mol)   # each has GetFamily/GetType/GetAtomIds
```

## Common Workflows

Reusable end-to-end recipes. Ready-to-run scripts for the same tasks also live in `scripts/` (see below).

### Drug-likeness Analysis

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def analyze_druglikeness(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    # Calculate Lipinski descriptors
    results = {
        'MW': Descriptors.MolWt(mol),
        'LogP': Descriptors.MolLogP(mol),
        'HBD': Descriptors.NumHDonors(mol),
        'HBA': Descriptors.NumHAcceptors(mol),
        'TPSA': Descriptors.TPSA(mol),
        'RotBonds': Descriptors.NumRotatableBonds(mol)
    }

    # Check Lipinski's Rule of Five
    results['Lipinski'] = (
        results['MW'] <= 500 and
        results['LogP'] <= 5 and
        results['HBD'] <= 5 and
        results['HBA'] <= 10
    )

    return results
```

### Similarity Screening

```python
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
from rdkit import DataStructs

def similarity_screen(query_smiles, database_smiles, threshold=0.7):
    mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    query_mol = Chem.MolFromSmiles(query_smiles)
    query_fp = mfpgen.GetFingerprint(query_mol)

    hits = []
    for idx, smiles in enumerate(database_smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            fp = mfpgen.GetFingerprint(mol)
            sim = DataStructs.TanimotoSimilarity(query_fp, fp)
            if sim >= threshold:
                hits.append((idx, smiles, sim))

    return sorted(hits, key=lambda x: x[2], reverse=True)
```

### Substructure Filtering

```python
from rdkit import Chem

def filter_by_substructure(smiles_list, pattern_smarts):
    query = Chem.MolFromSmarts(pattern_smarts)

    hits = []
    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if mol and mol.HasSubstructMatch(query):
            hits.append(smiles)

    return hits
```

## Best Practices

### Error Handling

Always check for `None` when parsing molecules:

```python
mol = Chem.MolFromSmiles(smiles)
if mol is None:
    print(f"Failed to parse: {smiles}")
    continue
```

### Performance Optimization

Pickle molecules for fast reloading instead of reparsing, and use bulk operations for fingerprints and similarity:

```python
import pickle
with open('molecules.pkl', 'wb') as f:
    pickle.dump(mols, f)   # load side is much faster than reparsing SMILES/SDF

mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
fps = [mfpgen.GetFingerprint(mol) for mol in mols]
similarities = DataStructs.BulkTanimotoSimilarity(fps[0], fps[1:])
```

### Thread Safety

RDKit operations are generally thread-safe for molecule I/O, coordinate generation, fingerprinting and descriptors, substructure searching, reactions, and drawing. **Not thread-safe:** MolSuppliers when accessed concurrently — don't share a supplier object across threads.

### Memory Management

For large datasets, stream instead of loading everything at once:

```python
# Avoid loading the entire file into memory
with open('large.sdf') as f:
    suppl = Chem.ForwardSDMolSupplier(f)
    for mol in suppl:
        # Process one molecule at a time
        pass

# Parallel processing
suppl = Chem.MultithreadedSDMolSupplier('large.sdf', numWriterThreads=4)
```

## Common Pitfalls

1. **Forgetting to check for None:** Always validate molecules after parsing
2. **Sanitization failures:** Use `DetectChemistryProblems()` to debug
3. **Missing hydrogens:** Use `AddHs()` when calculating properties that depend on hydrogen
4. **2D vs 3D:** Generate appropriate coordinates before visualization or 3D analysis
5. **SMARTS matching rules:** Remember that unspecified properties match anything
6. **Thread safety with MolSuppliers:** Don't share supplier objects across threads

## Resources

### references/

- `code_recipes.md` — Full runnable code for all twelve capability areas above
- `api_reference.md` — Comprehensive listing of RDKit modules, functions, and classes organized by functionality
- `descriptors_reference.md` — Complete list of available molecular descriptors with descriptions
- `smarts_patterns.md` — Common SMARTS patterns for functional groups and structural features

Load these references when needing specific API details, parameter information, or pattern examples.

### scripts/

Example scripts for common RDKit workflows:

- `molecular_properties.py` — Calculate comprehensive molecular properties and descriptors
- `similarity_search.py` — Perform fingerprint-based similarity screening
- `substructure_filter.py` — Filter molecules by substructure patterns

These scripts can be executed directly or used as templates for custom workflows.

Part of the AlterLab Academic Skills suite.
