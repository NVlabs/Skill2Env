# Datamol Worked Workflow Recipes

End-to-end, copy-ready pipelines and multi-step recipes extracted from the skill body so `SKILL.md` stays lean; each block is self-contained and assumes `import datamol as dm`.

## Complete Pipeline: Data Loading → Filtering → Analysis

```python
import datamol as dm
import pandas as pd

# 1. Load molecules
df = dm.read_sdf("compounds.sdf")

# 2. Standardize
df['mol'] = df['mol'].apply(lambda m: dm.standardize_mol(m) if m else None)
df = df[df['mol'].notna()]  # Remove failed molecules

# 3. Compute descriptors
desc_df = dm.descriptors.batch_compute_many_descriptors(
    df['mol'].tolist(),
    n_jobs=-1,
    progress=True
)

# 4. Filter by drug-likeness (batch_compute_many_descriptors uses the same keys
#    as compute_many_descriptors: clogp, n_lipinski_hbd, n_lipinski_hba)
druglike = (
    (desc_df['mw'] <= 500) &
    (desc_df['clogp'] <= 5) &
    (desc_df['n_lipinski_hbd'] <= 5) &
    (desc_df['n_lipinski_hba'] <= 10)
)
filtered_df = df[druglike.values]

# 5. Cluster and select diverse subset
diverse_mols = dm.pick_diverse(
    filtered_df['mol'].tolist(),
    npick=100
)

# 6. Visualize results
dm.viz.to_image(
    diverse_mols,
    legends=[dm.to_smiles(m) for m in diverse_mols],
    outfile="diverse_compounds.png",
    n_cols=10
)
```

## Structure-Activity Relationship (SAR) Analysis

```python
# Group by scaffold
scaffolds = [dm.to_scaffold_murcko(mol) for mol in mols]
scaffold_smiles = [dm.to_smiles(s) for s in scaffolds]

# Create DataFrame with activities
sar_df = pd.DataFrame({
    'mol': mols,
    'scaffold': scaffold_smiles,
    'activity': activities  # User-provided activity data
})

# Analyze each scaffold series
for scaffold, group in sar_df.groupby('scaffold'):
    if len(group) >= 3:  # Need multiple examples
        print(f"\nScaffold: {scaffold}")
        print(f"Count: {len(group)}")
        print(f"Activity range: {group['activity'].min():.2f} - {group['activity'].max():.2f}")

        # Visualize with activities as legends
        dm.viz.to_image(
            group['mol'].tolist(),
            legends=[f"Activity: {act:.2f}" for act in group['activity']],
            align=True  # Align by common substructure
        )
```

## Virtual Screening Pipeline

```python
# 1. Calculate Tanimoto distances between query actives and the library.
#    dm.cdist takes the molecules directly (it fingerprints internally),
#    returning an (n_query, n_library) distance matrix.
import numpy as np

distances = dm.cdist(query_actives, library_mols, n_jobs=-1)

# 3. Find closest matches (min distance to any query)
min_distances = distances.min(axis=0)
similarities = 1 - min_distances  # Convert distance to similarity

# 4. Rank and select top hits
top_indices = np.argsort(similarities)[::-1][:100]  # Top 100
top_hits = [library_mols[i] for i in top_indices]
top_scores = [similarities[i] for i in top_indices]

# 5. Visualize hits
dm.viz.to_image(
    top_hits[:20],
    legends=[f"Sim: {score:.3f}" for score in top_scores[:20]],
    outfile="screening_hits.png"
)
```

## Scaffold-Based Analysis

```python
# Group compounds by scaffold
from collections import Counter

scaffolds = [dm.to_scaffold_murcko(mol) for mol in mols]
scaffold_smiles = [dm.to_smiles(s) for s in scaffolds]

# Count scaffold frequency
scaffold_counts = Counter(scaffold_smiles)
most_common = scaffold_counts.most_common(10)

# Create scaffold-to-molecules mapping
scaffold_groups = {}
for mol, scaf_smi in zip(mols, scaffold_smiles):
    if scaf_smi not in scaffold_groups:
        scaffold_groups[scaf_smi] = []
    scaffold_groups[scaf_smi].append(mol)
```

## Scaffold-Based Train/Test Splitting (for ML)

```python
# Ensure train and test sets have different scaffolds
scaffold_to_mols = {}
for mol, scaf in zip(mols, scaffold_smiles):
    if scaf not in scaffold_to_mols:
        scaffold_to_mols[scaf] = []
    scaffold_to_mols[scaf].append(mol)

# Split scaffolds into train/test
import random
scaffolds = list(scaffold_to_mols.keys())
random.shuffle(scaffolds)
split_idx = int(0.8 * len(scaffolds))
train_scaffolds = scaffolds[:split_idx]
test_scaffolds = scaffolds[split_idx:]

# Get molecules for each split
train_mols = [mol for scaf in train_scaffolds for mol in scaffold_to_mols[scaf]]
test_mols = [mol for scaf in test_scaffolds for mol in scaffold_to_mols[scaf]]
```

## Fragment Frequency and Overlap Scoring

```python
# Find common fragments across compound library
from collections import Counter

all_fragments = []
for mol in mols:
    frags = dm.fragment.brics(mol)
    all_fragments.extend(frags)

fragment_counts = Counter(all_fragments)
common_frags = fragment_counts.most_common(20)

# Fragment-based scoring
def fragment_score(mol, reference_fragments):
    mol_frags = dm.fragment.brics(mol)
    overlap = mol_frags.intersection(reference_fragments)
    return len(overlap) / len(mol_frags) if mol_frags else 0
```

## Integration with Machine Learning

```python
# Feature generation
X = np.array([dm.to_fp(mol) for mol in mols])

# Or descriptors
desc_df = dm.descriptors.batch_compute_many_descriptors(mols, n_jobs=-1)
X = desc_df.values

# Train model
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X, y_target)

# Predict
predictions = model.predict(X_test)
```

## Robust Error Handling Wrappers

```python
# Safe molecule creation
def safe_to_mol(smiles):
    try:
        mol = dm.to_mol(smiles)
        if mol is not None:
            mol = dm.standardize_mol(mol)
        return mol
    except Exception as e:
        print(f"Failed to process {smiles}: {e}")
        return None

# Safe batch processing
valid_mols = []
for smiles in smiles_list:
    mol = safe_to_mol(smiles)
    if mol is not None:
        valid_mols.append(mol)
```
