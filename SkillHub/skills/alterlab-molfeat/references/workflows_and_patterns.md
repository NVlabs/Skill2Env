# Molfeat Workflows and Advanced Patterns

Copy-ready recipes for end-to-end molfeat workflows, ModelStore discovery, and advanced usage patterns extracted from the skill body.

## Common Workflows

### Building a QSAR Model

```python
from molfeat.trans import MoleculeTransformer
from molfeat.calc import FPCalculator
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

# Featurize molecules
transformer = MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)
X = transformer(smiles_train)

# Train model
model = RandomForestRegressor(n_estimators=100)
scores = cross_val_score(model, X, y_train, cv=5)
print(f"R² = {scores.mean():.3f}")

# Save configuration for deployment
transformer.to_state_yaml_file("production_featurizer.yml")
```

### Virtual Screening Pipeline

```python
from sklearn.ensemble import RandomForestClassifier

# Train on known actives/inactives
transformer = MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)
X_train = transformer(train_smiles)
clf = RandomForestClassifier(n_estimators=500)
clf.fit(X_train, train_labels)

# Screen large library
X_screen = transformer(screening_library)  # e.g., 1M compounds
predictions = clf.predict_proba(X_screen)[:, 1]

# Rank and select top hits
top_indices = predictions.argsort()[::-1][:1000]
top_hits = [screening_library[i] for i in top_indices]
```

### Similarity Search

```python
from sklearn.metrics.pairwise import cosine_similarity

# Query molecule
calc = FPCalculator("ecfp")
query_fp = calc(query_smiles).reshape(1, -1)

# Database fingerprints
transformer = MoleculeTransformer(calc, n_jobs=-1)
database_fps = transformer(database_smiles)

# Compute similarity
similarities = cosine_similarity(query_fp, database_fps)[0]
top_similar = similarities.argsort()[-10:][::-1]
```

### Scikit-learn Pipeline Integration

```python
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# Create end-to-end pipeline
pipeline = Pipeline([
    ('featurizer', MoleculeTransformer(FPCalculator("ecfp"), n_jobs=-1)),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Train and predict directly on SMILES
pipeline.fit(smiles_train, y_train)
predictions = pipeline.predict(smiles_test)
```

### Comparing Multiple Featurizers

```python
featurizers = {
    'ECFP': FPCalculator("ecfp"),
    'MACCS': FPCalculator("maccs"),
    'Descriptors': RDKitDescriptors2D(),
    'ChemBERTa': PretrainedMolTransformer("ChemBERTa-77M-MLM")
}

results = {}
for name, feat in featurizers.items():
    transformer = MoleculeTransformer(feat, n_jobs=-1)
    X = transformer(smiles)
    # Evaluate with your ML model
    score = evaluate_model(X, y)
    results[name] = score
```

## Discovering Available Featurizers

Use the ModelStore to explore all available featurizers:

```python
from molfeat.store.modelstore import ModelStore

store = ModelStore()

# List all available models
all_models = store.available_models
print(f"Total featurizers: {len(all_models)}")

# Search for specific models
chemberta_models = store.search(name="ChemBERTa")
for model in chemberta_models:
    print(f"- {model.name}: {model.description}")

# Get usage information
model_card = store.search(name="ChemBERTa-77M-MLM")[0]
model_card.usage()  # Display usage examples

# Load model
transformer = store.load("ChemBERTa-77M-MLM")
```

## Advanced Features

### Custom Preprocessing

```python
class CustomTransformer(MoleculeTransformer):
    def preprocess(self, mol):
        """Custom preprocessing pipeline"""
        if isinstance(mol, str):
            mol = dm.to_mol(mol)
        mol = dm.standardize_mol(mol)
        mol = dm.remove_salts(mol)
        return mol

transformer = CustomTransformer(FPCalculator("ecfp"), n_jobs=-1)
```

### Batch Processing Large Datasets

```python
def featurize_in_chunks(smiles_list, transformer, chunk_size=10000):
    """Process large datasets in chunks to manage memory"""
    all_features = []
    for i in range(0, len(smiles_list), chunk_size):
        chunk = smiles_list[i:i+chunk_size]
        features = transformer(chunk)
        all_features.append(features)
    return np.vstack(all_features)
```

### Caching Expensive Embeddings

```python
import pickle

cache_file = "embeddings_cache.pkl"
transformer = PretrainedMolTransformer("ChemBERTa-77M-MLM", n_jobs=-1)

try:
    with open(cache_file, "rb") as f:
        embeddings = pickle.load(f)
except FileNotFoundError:
    embeddings = transformer(smiles_list)
    with open(cache_file, "wb") as f:
        pickle.dump(embeddings, f)
```
