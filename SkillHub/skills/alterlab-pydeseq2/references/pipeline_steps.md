# PyDESeq2 Pipeline Steps and Designs

Worked code for the full DESeq2 pipeline: data prep, design, fitting, testing, shrinkage, export, and common experimental designs.

## Quick Start Workflow

Standard differential expression analysis end to end:

```python
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# 1. Load data
counts_df = pd.read_csv("counts.csv", index_col=0).T  # Transpose to samples × genes
metadata = pd.read_csv("metadata.csv", index_col=0)

# 2. Filter low-count genes
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# 3. Initialize and fit DESeq2
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True
)
dds.deseq2()

# 4. Perform statistical testing
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

# 5. Access results
results = ds.results_df
significant = results[results.padj < 0.05]
print(f"Found {len(significant)} significant genes")
```

## Step 1: Data Preparation

**Input requirements:**
- **Count matrix:** Samples × genes DataFrame with non-negative integer read counts
- **Metadata:** Samples × variables DataFrame with experimental factors

**Common data loading patterns:**

```python
# From CSV (typical format: genes × samples, needs transpose)
counts_df = pd.read_csv("counts.csv", index_col=0).T
metadata = pd.read_csv("metadata.csv", index_col=0)

# From TSV
counts_df = pd.read_csv("counts.tsv", sep="\t", index_col=0).T

# From AnnData
import anndata as ad
adata = ad.read_h5ad("data.h5ad")
counts_df = pd.DataFrame(adata.X, index=adata.obs_names, columns=adata.var_names)
metadata = adata.obs
```

**Data filtering:**

```python
# Remove low-count genes
genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

# Remove samples with missing metadata
samples_to_keep = ~metadata.condition.isna()
counts_df = counts_df.loc[samples_to_keep]
metadata = metadata.loc[samples_to_keep]
```

## Step 2: Design Specification

The design formula specifies how gene expression is modeled.

**Single-factor designs:**
```python
design = "~condition"  # Simple two-group comparison
```

**Multi-factor designs:**
```python
design = "~batch + condition"  # Control for batch effects
design = "~age + condition"     # Include continuous covariate
design = "~group + condition + group:condition"  # Interaction effects
```

**Design formula guidelines:**
- Use Wilkinson formula notation (R-style)
- Put adjustment variables (e.g., batch) before the main variable of interest
- Ensure variables exist as columns in the metadata DataFrame
- Use appropriate data types (categorical for discrete variables)

## Step 3: DESeq2 Fitting

```python
from pydeseq2.dds import DeseqDataSet
from pydeseq2.default_inference import DefaultInference

dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True,                          # Refit after removing outliers
    inference=DefaultInference(n_cpus=1),      # Parallelism lives on the inference object (0.4+)
)

# Run the complete DESeq2 pipeline
dds.deseq2()
```

**What `deseq2()` does:**
1. Computes size factors (normalization)
2. Fits genewise dispersions
3. Fits dispersion trend curve
4. Computes dispersion priors
5. Fits MAP dispersions (shrinkage)
6. Fits log fold changes
7. Calculates Cook's distances (outlier detection)
8. Refits if outliers detected (optional)

## Step 4: Statistical Testing

```python
from pydeseq2.ds import DeseqStats

ds = DeseqStats(
    dds,
    contrast=["condition", "treated", "control"],  # Test treated vs control
    alpha=0.05,                # Significance threshold
    cooks_filter=True,         # Filter outliers
    independent_filter=True    # Filter low-power tests
)

ds.summary()
```

**Contrast specification:**
- Format: `[variable, test_level, reference_level]`
- Example: `["condition", "treated", "control"]` tests treated vs control
- If `None`, uses the last coefficient in the design

**Result DataFrame columns:**
- `baseMean`: Mean normalized count across samples
- `log2FoldChange`: Log2 fold change between conditions
- `lfcSE`: Standard error of LFC
- `stat`: Wald test statistic
- `pvalue`: Raw p-value
- `padj`: Adjusted p-value (FDR-corrected via Benjamini-Hochberg)

## Step 5: Optional LFC Shrinkage

```python
ds.lfc_shrink()  # Applies apeGLM shrinkage
```

**When to use LFC shrinkage:**
- For visualization (volcano plots, heatmaps)
- For ranking genes by effect size
- When prioritizing genes for follow-up experiments

**Important:** Shrinkage affects only the log2FoldChange values, not the statistical test results (p-values remain unchanged). Use shrunk values for visualization but report unshrunken p-values for significance.

## Step 6: Result Export

```python
import pickle

# Export results as CSV
ds.results_df.to_csv("deseq2_results.csv")

# Save significant genes only
significant = ds.results_df[ds.results_df.padj < 0.05]
significant.to_csv("significant_genes.csv")

# Save DeseqDataSet for later use
with open("dds_result.pkl", "wb") as f:
    pickle.dump(dds.to_picklable_anndata(), f)
```

## Common Experimental Designs

### Two-Group Comparison
```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()

results = ds.results_df
significant = results[results.padj < 0.05]
```

### Multiple Comparisons
```python
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~condition")
dds.deseq2()

treatments = ["treatment_A", "treatment_B", "treatment_C"]
all_results = {}

for treatment in treatments:
    ds = DeseqStats(dds, contrast=["condition", treatment, "control"])
    ds.summary()
    all_results[treatment] = ds.results_df

    sig_count = len(ds.results_df[ds.results_df.padj < 0.05])
    print(f"{treatment}: {sig_count} significant genes")
```

### Accounting for Batch Effects
```python
# Include batch in design
dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~batch + condition")
dds.deseq2()

# Test condition while controlling for batch
ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```

### Continuous Covariates
```python
# Ensure continuous variable is numeric
metadata["age"] = pd.to_numeric(metadata["age"])

dds = DeseqDataSet(counts=counts_df, metadata=metadata, design="~age + condition")
dds.deseq2()

ds = DeseqStats(dds, contrast=["condition", "treated", "control"])
ds.summary()
```
