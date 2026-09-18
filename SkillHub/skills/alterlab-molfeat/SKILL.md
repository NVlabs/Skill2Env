---
name: alterlab-molfeat
description: Featurizes molecules for machine learning with molfeat (100+ featurizers) — ECFP/MACCS/MAP4 fingerprints, RDKit and Mordred physicochemical descriptors, and pretrained embeddings (ChemBERTa, ChemGPT, GIN) exposed as scikit-learn transformers that convert SMILES into feature vectors. Use when turning molecules into ML-ready feature matrices for QSAR/QSPR or virtual screening, or benchmarking fingerprint against descriptor and embedding representations; for training models and MoleculeNet benchmarks on those features prefer alterlab-deepchem, and for low-level fingerprint or descriptor primitives prefer alterlab-rdkit. Part of the AlterLab Academic Skills suite.
license: Apache-2.0
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: "Self-contained — runs under `uv run python` with the skill's Python package installed; no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Molfeat - Molecular Featurization Hub

## Overview

Molfeat is a comprehensive Python library for molecular featurization that unifies 100+ pre-trained embeddings and hand-crafted featurizers. Convert chemical structures (SMILES strings or RDKit molecules) into numerical representations for machine learning tasks including QSAR modeling, virtual screening, similarity searching, and deep learning applications. Features fast parallel processing, scikit-learn compatible transformers, and built-in caching.

## When to Use This Skill

This skill should be used when working with:
- **Molecular machine learning**: Building QSAR/QSPR models, property prediction
- **Virtual screening**: Ranking compound libraries for biological activity
- **Similarity searching**: Finding structurally similar molecules
- **Chemical space analysis**: Clustering, visualization, dimensionality reduction
- **Deep learning**: Training neural networks on molecular data
- **Featurization pipelines**: Converting SMILES to ML-ready representations
- **Cheminformatics**: Any task requiring molecular feature extraction

## Installation

```bash
uv pip install molfeat

# With all optional dependencies
uv pip install "molfeat[all]"
```

**Optional dependencies for specific featurizers:**
- `molfeat[dgl]` - GNN models (GIN variants)
- `molfeat[graphormer]` - Graphormer models
- `molfeat[transformer]` - ChemBERTa, ChemGPT, MolT5
- `molfeat[fcd]` - FCD descriptors
- `molfeat[map4]` - MAP4 fingerprints

## Core Concepts

Molfeat organizes featurization into three hierarchical classes:

### 1. Calculators (`molfeat.calc`)

Callable objects that convert individual molecules into feature vectors. Accept RDKit `Chem.Mol` objects or SMILES strings.

**Use calculators for:**
- Single molecule featurization
- Custom processing loops
- Direct feature computation

**Example:**
```python
from molfeat.calc import FPCalculator

calc = FPCalculator("ecfp", radius=3, fpSize=2048)
features = calc("CCO")  # Returns numpy array (2048,)
```

### 2. Transformers (`molfeat.trans`)

Scikit-learn compatible transformers that wrap calculators for batch processing with parallelization.

**Use transformers for:**
- Batch featurization of molecular datasets
- Integration with scikit-learn pipelines
- Parallel processing (automatic CPU utilization)

**Example:**
```python
from molfeat.trans import MoleculeTransformer
from molfeat.calc import FPCalculator

transformer = MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)
features = transformer(smiles_list)  # Parallel processing
```

### 3. Pretrained Transformers (`molfeat.trans.pretrained`)

Specialized transformers for deep learning models with batched inference and caching.

**Use pretrained transformers for:**
- State-of-the-art molecular embeddings
- Transfer learning from large chemical datasets
- Deep learning feature extraction

**Example:**
```python
from molfeat.trans.pretrained import PretrainedMolTransformer

transformer = PretrainedMolTransformer("ChemBERTa-77M-MLM", n_jobs=-1)
embeddings = transformer(smiles_list)  # Deep learning embeddings
```

## Quick Start Workflow

### Basic Featurization

```python
import datamol as dm
from molfeat.calc import FPCalculator
from molfeat.trans import MoleculeTransformer

# Load molecular data
smiles = ["CCO", "CC(=O)O", "c1ccccc1", "CC(C)O"]

# Create calculator and transformer
calc = FPCalculator("ecfp", radius=3)
transformer = MoleculeTransformer(calc, n_jobs=-1)

# Featurize molecules
features = transformer(smiles)
print(f"Shape: {features.shape}")  # (4, 2048)
```

### Save and Load Configuration

```python
# Save featurizer configuration for reproducibility
transformer.to_state_yaml_file("featurizer_config.yml")

# Reload exact configuration
loaded = MoleculeTransformer.from_state_yaml_file("featurizer_config.yml")
```

### Handle Errors Gracefully

```python
# Process dataset with potentially invalid SMILES
transformer = MoleculeTransformer(
    calc,
    n_jobs=-1,
    ignore_errors=True,  # Continue on failures
    verbose=True          # Log error details
)

features = transformer(smiles_with_errors)
# Returns None for failed molecules
```

## Choosing the Right Featurizer

### For Traditional Machine Learning (RF, SVM, XGBoost)

**Start with fingerprints:**
```python
# ECFP - Most popular, general-purpose
FPCalculator("ecfp", radius=3, fpSize=2048)

# MACCS - Fast, good for scaffold hopping
FPCalculator("maccs")

# MAP4 - Efficient for large-scale screening
FPCalculator("map4")
```

**For interpretable models:**
```python
# RDKit 2D descriptors (200+ named properties)
from molfeat.calc import RDKitDescriptors2D
RDKitDescriptors2D()

# Mordred (1800+ comprehensive descriptors)
from molfeat.calc import MordredDescriptors
MordredDescriptors()
```

**Combine multiple featurizers:**
```python
from molfeat.trans import FeatConcat

concat = FeatConcat([
    FPCalculator("maccs"),      # 167 dimensions
    FPCalculator("ecfp")         # 2048 dimensions
])  # Result: 2215-dimensional combined features
```

### For Deep Learning

**Transformer-based embeddings:**
```python
# ChemBERTa - Pre-trained on 77M PubChem compounds
PretrainedMolTransformer("ChemBERTa-77M-MLM")

# ChemGPT - Autoregressive language model
PretrainedMolTransformer("ChemGPT-1.2B")
```

**Graph neural networks:**
```python
# GIN models with different pre-training objectives
PretrainedMolTransformer("gin-supervised-masking")
PretrainedMolTransformer("gin-supervised-infomax")

# Graphormer for quantum chemistry
PretrainedMolTransformer("Graphormer-pcqm4mv2")
```

### For Similarity Searching

```python
# ECFP - General purpose, most widely used
FPCalculator("ecfp")

# MACCS - Fast, scaffold-based similarity
FPCalculator("maccs")

# MAP4 - Efficient for large databases
FPCalculator("map4")

# USR/USRCAT - 3D shape similarity
from molfeat.calc import USRDescriptors
USRDescriptors()
```

### For Pharmacophore-Based Approaches

```python
# FCFP - Functional group based
FPCalculator("fcfp")

# CATS - Pharmacophore pair distributions
from molfeat.calc import CATSCalculator
CATSCalculator(mode="2D")

# Gobbi - Explicit pharmacophore features
FPCalculator("gobbi2D")
```

## Common Workflows and Advanced Patterns

End-to-end recipes (QSAR model building, virtual screening, similarity search, scikit-learn pipeline integration, comparing featurizers), ModelStore discovery, and advanced usage (custom preprocessing, chunked batch processing, caching expensive embeddings) have moved to keep this body lean.

Full copy-ready workflow and advanced-pattern recipes: see `references/workflows_and_patterns.md`. Additional runnable examples (PyTorch training, grid search, 3D conformers) live in `references/examples.md`.

## Performance Tips

1. **Use parallelization**: Set `n_jobs=-1` to utilize all CPU cores
2. **Batch processing**: Process multiple molecules at once instead of loops
3. **Choose appropriate featurizers**: Fingerprints are faster than deep learning models
4. **Cache pretrained models**: Leverage built-in caching for repeated use
5. **Use float32**: Set `dtype=np.float32` when precision allows
6. **Handle errors efficiently**: Use `ignore_errors=True` for large datasets

## Common Featurizers Reference

**Quick reference for frequently used featurizers:**

| Featurizer | Type | Dimensions | Speed | Use Case |
|------------|------|------------|-------|----------|
| `ecfp` | Fingerprint | 2048 | Fast | General purpose |
| `maccs` | Fingerprint | 167 | Very fast | Scaffold similarity |
| `desc2D` | Descriptors | 200+ | Fast | Interpretable models |
| `mordred` | Descriptors | 1800+ | Medium | Comprehensive features |
| `map4` | Fingerprint | 1024 | Fast | Large-scale screening |
| `ChemBERTa-77M-MLM` | Deep learning | 768 | Slow* | Transfer learning |
| `gin-supervised-masking` | GNN | Variable | Slow* | Graph-based models |

*First run is slow; subsequent runs benefit from caching

## Resources

This skill includes comprehensive reference documentation:

### references/api_reference.md
Complete API documentation covering:
- `molfeat.calc` - All calculator classes and parameters
- `molfeat.trans` - Transformer classes and methods
- `molfeat.store` - ModelStore usage
- Common patterns and integration examples
- Performance optimization tips

**When to load:** Reference when implementing specific calculators, understanding transformer parameters, or integrating with scikit-learn/PyTorch.

### references/available_featurizers.md
Comprehensive catalog of all 100+ featurizers organized by category:
- Transformer-based language models (ChemBERTa, ChemGPT)
- Graph neural networks (GIN, Graphormer)
- Molecular descriptors (RDKit, Mordred)
- Fingerprints (ECFP, MACCS, MAP4, and 15+ others)
- Pharmacophore descriptors (CATS, Gobbi)
- Shape descriptors (USR, ElectroShape)
- Scaffold-based descriptors

**When to load:** Reference when selecting the optimal featurizer for a specific task, exploring available options, or understanding featurizer characteristics.

**Search tip:** Use grep to find specific featurizer types:
```bash
grep -i "chembert" references/available_featurizers.md
grep -i "pharmacophore" references/available_featurizers.md
```

### references/examples.md
Practical code examples for common scenarios:
- Installation and quick start
- Calculator and transformer examples
- Pretrained model usage
- Scikit-learn and PyTorch integration
- Virtual screening workflows
- QSAR model building
- Similarity searching
- Troubleshooting and best practices

**When to load:** Reference when implementing specific workflows, troubleshooting issues, or learning molfeat patterns.

## Troubleshooting

### Invalid Molecules
Enable error handling to skip invalid SMILES:
```python
transformer = MoleculeTransformer(
    calc,
    ignore_errors=True,
    verbose=True
)
```

### Memory Issues with Large Datasets
Process in chunks or use streaming approaches for datasets > 100K molecules.

### Pretrained Model Dependencies
Some models require additional packages. Install specific extras:
```bash
uv pip install "molfeat[transformer]"  # For ChemBERTa/ChemGPT
uv pip install "molfeat[dgl]"          # For GIN models
```

### Reproducibility
Save exact configurations and document versions:
```python
transformer.to_state_yaml_file("config.yml")
import molfeat
print(f"molfeat version: {molfeat.__version__}")
```

## Additional Resources

- **Official Documentation**: https://molfeat-docs.datamol.io/
- **GitHub Repository**: https://github.com/datamol-io/molfeat
- **PyPI Package**: https://pypi.org/project/molfeat/
- **Tutorial**: https://portal.valencelabs.com/datamol/post/types-of-featurizers-b1e8HHrbFMkbun6

