# PyDESeq2 Result Interpretation, Plots, and Troubleshooting

Code for filtering/ranking significant genes, quality metrics, volcano/MA plots, and resolving common errors.

## Identifying Significant Genes

```python
# Filter by adjusted p-value
significant = ds.results_df[ds.results_df.padj < 0.05]

# Filter by both significance and effect size
sig_and_large = ds.results_df[
    (ds.results_df.padj < 0.05) &
    (abs(ds.results_df.log2FoldChange) > 1)
]

# Separate up- and down-regulated
upregulated = significant[significant.log2FoldChange > 0]
downregulated = significant[significant.log2FoldChange < 0]

print(f"Upregulated: {len(upregulated)}")
print(f"Downregulated: {len(downregulated)}")
```

## Ranking and Sorting

```python
import numpy as np

# Sort by adjusted p-value
top_by_padj = ds.results_df.sort_values("padj").head(20)

# Sort by absolute fold change (use shrunk values)
ds.lfc_shrink()
ds.results_df["abs_lfc"] = abs(ds.results_df.log2FoldChange)
top_by_lfc = ds.results_df.sort_values("abs_lfc", ascending=False).head(20)

# Sort by a combined metric
ds.results_df["score"] = -np.log10(ds.results_df.padj) * abs(ds.results_df.log2FoldChange)
top_combined = ds.results_df.sort_values("score", ascending=False).head(20)
```

## Quality Metrics

```python
# Check normalization (size factors should be close to 1)
print("Size factors:", dds.obsm["size_factors"])

# Examine dispersion estimates
import matplotlib.pyplot as plt
plt.hist(dds.varm["dispersions"], bins=50)
plt.xlabel("Dispersion")
plt.ylabel("Frequency")
plt.title("Dispersion Distribution")
plt.show()

# Check p-value distribution (should be mostly flat with peak near 0)
plt.hist(ds.results_df.pvalue.dropna(), bins=50)
plt.xlabel("P-value")
plt.ylabel("Frequency")
plt.title("P-value Distribution")
plt.show()
```

## Volcano Plot

Visualize significance vs effect size:

```python
import matplotlib.pyplot as plt
import numpy as np

results = ds.results_df.copy()
results["-log10(padj)"] = -np.log10(results.padj)

plt.figure(figsize=(10, 6))
significant = results.padj < 0.05

plt.scatter(
    results.loc[~significant, "log2FoldChange"],
    results.loc[~significant, "-log10(padj)"],
    alpha=0.3, s=10, c='gray', label='Not significant'
)
plt.scatter(
    results.loc[significant, "log2FoldChange"],
    results.loc[significant, "-log10(padj)"],
    alpha=0.6, s=10, c='red', label='padj < 0.05'
)

plt.axhline(-np.log10(0.05), color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log2 Fold Change")
plt.ylabel("-Log10(Adjusted P-value)")
plt.title("Volcano Plot")
plt.legend()
plt.savefig("volcano_plot.png", dpi=300)
```

## MA Plot

Show fold change vs mean expression:

```python
plt.figure(figsize=(10, 6))

plt.scatter(
    np.log10(results.loc[~significant, "baseMean"] + 1),
    results.loc[~significant, "log2FoldChange"],
    alpha=0.3, s=10, c='gray'
)
plt.scatter(
    np.log10(results.loc[significant, "baseMean"] + 1),
    results.loc[significant, "log2FoldChange"],
    alpha=0.6, s=10, c='red'
)

plt.axhline(0, color='blue', linestyle='--', alpha=0.5)
plt.xlabel("Log10(Base Mean + 1)")
plt.ylabel("Log2 Fold Change")
plt.title("MA Plot")
plt.savefig("ma_plot.png", dpi=300)
```

## Troubleshooting

### Data Format Problems

**Issue:** "Index mismatch between counts and metadata"

**Solution:** Ensure sample names match exactly
```python
print("Counts samples:", counts_df.index.tolist())
print("Metadata samples:", metadata.index.tolist())

# Take intersection if needed
common = counts_df.index.intersection(metadata.index)
counts_df = counts_df.loc[common]
metadata = metadata.loc[common]
```

**Issue:** "All genes have zero counts"

**Solution:** Check if data needs transposition
```python
print(f"Counts shape: {counts_df.shape}")
# If genes > samples, transpose is needed
if counts_df.shape[1] < counts_df.shape[0]:
    counts_df = counts_df.T
```

### Design Matrix Issues

**Issue:** "Design matrix is not full rank"

**Cause:** Confounded variables (e.g., all treated samples in one batch)

**Solution:** Remove confounded variable or add interaction term
```python
# Check confounding
print(pd.crosstab(metadata.condition, metadata.batch))

# Either simplify design or add interaction
design = "~condition"  # Remove batch
# OR
design = "~condition + batch + condition:batch"  # Model interaction
```

### No Significant Genes

**Diagnostics:**
```python
# Check dispersion distribution
plt.hist(dds.varm["dispersions"], bins=50)
plt.show()

# Check size factors
print(dds.obsm["size_factors"])

# Look at top genes by raw p-value
print(ds.results_df.nsmallest(20, "pvalue"))
```

**Possible causes:**
- Small effect sizes
- High biological variability
- Insufficient sample size
- Technical issues (batch effects, outliers)
