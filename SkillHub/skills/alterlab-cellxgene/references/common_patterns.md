# Additional Patterns and Pitfalls

This file holds patterns that go beyond the core workflows. For the standard
query recipes see `querying_expression.md` (open / explore / `get_anndata` /
`axis_query`) and `ml_and_scanpy.md` (PyTorch dataloader, scanpy, multi-dataset
concatenation). The best-practices checklist lives in
`best_practices_and_troubleshooting.md`.

## Incremental Variance (Welford's Algorithm)

When computing variance out-of-core over a query too large for RAM, accumulate
it in one pass with Welford's online algorithm. Vectorize per batch rather than
looping over individual values:

```python
import numpy as np

n = 0
mean = 0.0
M2 = 0.0

for batch in query.X("raw").tables():
    values = batch["soma_data"].to_numpy()
    # Chan et al. parallel/batch update
    b_n = len(values)
    if b_n == 0:
        continue
    b_mean = values.mean()
    b_M2 = ((values - b_mean) ** 2).sum()
    delta = b_mean - mean
    new_n = n + b_n
    mean += delta * b_n / new_n
    M2 += b_M2 + delta**2 * n * b_n / new_n
    n = new_n

variance = M2 / (n - 1) if n > 1 else float("nan")
```

Note: `X("raw")` returns only the *stored* (nonzero) entries, so a mean/variance
computed this way is over observed nonzero values. To get statistics over the
full dense matrix (including implicit zeros), divide sums by
`n_cells * n_genes` from the query shape instead of by the number of nonzero
entries.

## Filter by Ontology Term for Cross-Dataset Consistency

Free-text labels (`cell_type == 'B cell'`) can vary subtly across datasets;
ontology term IDs are canonical and more reliable for population-scale queries:

```python
# Equivalent to 'B cell' but stable across all datasets
obs_value_filter="cell_type_ontology_term_id == 'CL:0000236' and is_primary_data == True"
```

## Batch Processing Across Conditions

For systematic analyses sweeping one factor, loop the query and collect results.
Pin `census_version` once and reuse the open handle:

```python
tissues = ["lung", "liver", "kidney", "heart"]
results = {}

with cellxgene_census.open_soma(census_version="2023-07-25") as census:
    for tissue in tissues:
        adata = cellxgene_census.get_anndata(
            census=census,
            organism="Homo sapiens",
            obs_value_filter=f"tissue_general == '{tissue}' and is_primary_data == True",
        )
        results[tissue] = analyze(adata)
```

## Common Pitfalls to Avoid

1. **Forgetting `is_primary_data == True`** — silently counts duplicate cells that appear in multiple datasets.
2. **Loading before estimating** — run a `get_obs` count first; switch to `axis_query` out-of-core above ~100k cells.
3. **Skipping the context manager** — leak open SOMA/TileDB handles.
4. **Unpinned version** — results drift when the `stable` release rolls forward; pin `census_version`.
5. **Overly broad queries** — start focused, then widen.
6. **Ignoring the presence matrix** — a gene absent from a dataset reads as all-zero, not missing; check `get_presence_matrix` before interpreting zeros.
7. **Mixing count types** — UMI molecule counts and full-length read counts coexist in `raw` and may need different normalization.
8. **Using deprecated APIs** — ML loaders are now in `tiledbsoma_ml`, not `cellxgene_census.experimental.ml`; concatenate with `anndata.concat`, not `adata.concatenate`.
