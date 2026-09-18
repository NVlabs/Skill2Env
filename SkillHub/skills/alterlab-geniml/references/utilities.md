# Geniml Utilities and Additional Tools

## BBClient: BED File Caching

### Overview

BBClient provides efficient caching of BED files from remote sources, enabling faster repeated access and integration with R workflows.

### When to Use

Use BBClient when:
- Repeatedly accessing BED files from remote databases
- Working with BEDbase repositories
- Integrating genomic data with R pipelines
- Need local caching for performance

### Python Usage

`load_bed(bed_id)` downloads (if needed) and caches a BED file from BEDbase and returns a `gtars` `RegionSet`. The default cache folder is `~/.bbcache`.

```python
from geniml.bbclient import BBClient

# Initialize client (default cache_folder='~/.bbcache')
client = BBClient(cache_folder='~/.bbcache')

# Fetch + cache a BED file by its BEDbase digest/id -> RegionSet
region_set = client.load_bed('<bedbase-bed-id>')

# Bedsets and local files are supported too:
#   client.load_bedset('<bedset-id>')
#   client.add_bed_to_cache('local.bed')
# Inspect what is cached: client.list_beds(), client.list_bedsets()
```

There is no `get_regions` method — iterate the returned `RegionSet` directly.

### R Integration

```r
library(reticulate)
bbclient <- import("geniml.bbclient")

client <- bbclient$BBClient(cache_folder = "~/.bbcache")
region_set <- client$load_bed("<bedbase-bed-id>")
```

### Best Practices

- Use a cache directory with ample storage and keep it consistent across analyses
- Prune unused cached files periodically (`remove_bedfile_from_cache`)

---

## BEDshift: BED File Randomization

### Overview

BEDshift provides tools for randomizing BED files while preserving genomic context, essential for generating null distributions and statistical testing.

### When to Use

Use BEDshift when:
- Creating null models for statistical testing
- Generating control datasets
- Assessing significance of genomic overlaps
- Benchmarking analysis methods

### Python Usage

BEDshift is a class, `Bedshift(bedfile_path, chrom_sizes=None, delimiter='\t')`. You apply perturbation operations (each takes a *rate* in 0-1), then write out. Perturbations: `add`, `drop`, `shift`, `cut`, `merge` (and `*_from_file` variants); `all_perturbations(...)` applies several at once.

```python
from geniml.bedshift.bedshift import Bedshift

bs = Bedshift('peaks.bed', chrom_sizes='hg38.chrom.sizes')
bs.set_seed(42)

# Shift 30% of regions (shiftrate, shiftmean, shiftstdev), drop 10% (droprate),
# then write the perturbed BED
bs.shift(0.3, 0, 150)
bs.drop(0.1)
bs.to_bed('randomized_peaks.bed')

# Reset to the original regions to start another independent replicate
bs.reset_bed()
```

To generate many null replicates, loop and write a file per iteration (or use the CLI `-r/--repeat`).

### CLI Usage

Flags are `-b/--bedfile`, a genome via `-g/--genome` (refgenie id) **or** chrom sizes via `-l/--chrom-lengths`, perturbation rates (`-d` drop, `-a` add, `-s` shift, `-c` cut, `-m` merge), `-r/--repeat`, `-o/--outputfile`, `--seed`. There is no `--input`, `--preserve-chrom`, or `--iterations` flag.

```bash
geniml bedshift \
  -b peaks.bed \
  -g hg38 \
  -s 0.3 \
  -d 0.1 \
  -r 100 \
  -o randomized_peaks.bed \
  --seed 42
```

### Best Practices

- Choose perturbation rates that match your null hypothesis
- Generate multiple replicates (`-r`) for robust statistics
- Record the seed and rates for reproducibility

---

## Evaluation: Model Assessment Tools

### Overview

Geniml provides evaluation utilities for assessing embedding quality and model performance.

### When to Use

Use evaluation tools when:
- Validating trained embeddings
- Comparing different models
- Assessing clustering quality
- Publishing model results

### Embedding Evaluation

geniml's evaluation lives in the `geniml.eval` package, exposed mainly through the CLI command `geniml eval` (the import path is `geniml.eval`, **not** `geniml.evaluation`). Run `geniml eval --help` for the metrics/flags in your version.

For ad-hoc cluster-quality checks, compute standard metrics directly with scikit-learn on the embeddings (`adata.obsm['scembed_X']` or a region-embedding matrix) and your labels:

```python
from sklearn.metrics import (
    silhouette_score, davies_bouldin_score, calinski_harabasz_score
)

X = adata.obsm['scembed_X']
labels = adata.obs['leiden']

print("Silhouette:", silhouette_score(X, labels))            # -1..1, higher better
print("Davies-Bouldin:", davies_bouldin_score(X, labels))     # >=0, lower better
print("Calinski-Harabasz:", calinski_harabasz_score(X, labels))  # higher better
```

### Cell-Type Annotation Evaluation

When you have predicted vs. true labels, score with sklearn:

```python
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

y_true = adata.obs['true_celltype']
y_pred = adata.obs['predicted_celltype']
print("Accuracy:", accuracy_score(y_true, y_pred))
print("Macro F1:", f1_score(y_true, y_pred, average='macro'))
```

### Best Practices

- Use multiple complementary metrics
- Compare against baseline models
- Report metrics on held-out test data
- Visualize embeddings (UMAP/t-SNE) alongside metrics

---

## Tokenization: Region Tokenization Utilities

### Overview

Tokenization converts genomic regions into discrete tokens using a reference universe, enabling word2vec-style training.

### When to Use

Tokenization is a required preprocessing step for:
- Region2Vec training
- scEmbed model training
- Any embedding method requiring discrete tokens

### Hard Tokenization

Strict overlap-based tokenization. Import the real function `hard_tokenization_main` from `geniml.tokenization.main` (shells out to `bedtools`):

```python
from geniml.tokenization.main import hard_tokenization_main

hard_tokenization_main(
    src_folder='bed_files/',
    dst_folder='tokenized/',
    universe_file='universe.bed',
    fraction=1e-9,
)
```

**Parameters:**
- `fraction`: minimum **overlap fraction** required to assign a region to a universe token (default 1e-9). This is an overlap threshold, not a p-value. Use a larger value (e.g. 1e-6) to be more permissive.

### Modern tokenizer (gtars)

The current/object-oriented path uses the `gtars` `Tokenizer`, which `Region2VecExModel` and `ScEmbed` use internally:

```python
from gtars.tokenizers import Tokenizer

tokenizer = Tokenizer('universe.bed')
# tokenizer(regions) -> tokenized regions; pass `tokenizer=...` to a model constructor
```

### Best Practices

- **Universe quality**: Use comprehensive, well-constructed universes
- **Threshold selection**: Smaller `fraction` is stricter
- **Validation**: Check what % of input regions land on a universe token before training
- **Consistency**: Use the same universe and parameters across related analyses

Aim for high tokenization coverage (>80%) before training; very low coverage usually means the universe doesn't match the assembly or is too sparse.

---

## Text2BedNN: Search Backend

### Overview

Text2BedNN creates neural network-based search backends for querying genomic regions using natural language or metadata.

### When to Use

Use Text2BedNN when:
- Building search interfaces for genomic databases
- Enabling natural language queries over BED files
- Creating metadata-aware search systems
- Deploying interactive genomic search applications

### Architecture (real modules)

Search is split across two packages — confirm the exact class signatures in your installed version before wiring them up:

- `geniml.search.backends` — vector index backends, e.g. `HNSWBackend` (needs `hnswlib`) and a file backend. These store/query region embeddings.
- `geniml.search.query2vec` — turns a query (text or region) into a vector.
- `geniml.search.interfaces` — search interface wiring the encoder to a backend.
- `geniml.text2bednn.text2bednn` — the natural-language→BED neural model that maps text embeddings into the region-embedding space.

### Workflow (conceptual)

1. Train a region/metadata model (Region2Vec or BEDspace) to get region embeddings.
2. Load them into a backend (e.g. `from geniml.search.backends import HNSWBackend`).
3. Encode the query with a `query2vec` encoder (or the trained `text2bednn` model for natural-language text).
4. Query the backend for nearest regions.

### Best Practices

- Train embeddings with rich metadata for better search
- Index large collections for comprehensive coverage
- Validate search relevance on known queries
- `HNSWBackend` requires `hnswlib`; on newer Python it may warn/fail to import — pin a compatible Python if you need it

---

## Additional Tools

### I/O

geniml's I/O is class-based, in `geniml.io.io` — `RegionSet`, `BedSet`, `Region`, `TokenizedRegionSet` (there are no `read_bed`/`write_bed`/`load_universe` helper functions). A `RegionSet` wraps a BED file and is iterable:

```python
from geniml.io import RegionSet

rs = RegionSet('peaks.bed')        # load
for region in rs:                  # iterate Region objects
    ...
```

`BBClient.load_bed()` also returns a (gtars) region set for remote/cached files.

### Saving / loading models

The embedding models persist themselves — there is no generic `geniml.models.save_model`. Use the model's own methods:

```python
model.export('my_model/')                 # ScEmbed / Region2VecExModel -> checkpoint.pt, config.yaml, universe.bed
model = ScEmbed.from_pretrained('my_model/')
```

### Common Patterns

End-to-end region-embedding pipeline (verified imports):

```python
from geniml.tokenization.main import hard_tokenization_main
from geniml.region2vec.main_legacy import region2vec

# 1. Build a universe via the CLI first: `geniml build-universe cc ...`
# 2. Tokenize (needs the bedtools binary)
hard_tokenization_main('beds/', 'tokens/', 'universe.bed', fraction=1e-9)

# 3. Train embeddings
region2vec(token_folder='tokens/', save_dir='model/', num_shufflings=1000, embedding_dim=100)

# 4. Evaluate cluster quality with sklearn metrics (see Evaluation section above)
```

This modular design allows flexible composition of geniml tools for diverse genomic ML workflows.
