---
name: alterlab-vaex
description: Out-of-core tabular analytics with Vaex for billion-row datasets that exceed RAM — lazy evaluation, fast aggregations, big-data visualization, and ML on a single machine. Use when working with large CSV/HDF5/Arrow/Parquet files, computing fast statistics on massive datasets, visualizing big data, or building ML pipelines that do not fit in memory. For distributed clusters prefer dask; for in-memory speed prefer polars. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: No API key required. Runs locally via `uv run python`; requires the vaex Python package.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Vaex

## Overview

Vaex is a high-performance Python library designed for lazy, out-of-core DataFrames to process and visualize tabular datasets that are too large to fit into RAM. Vaex can process over a billion rows per second, enabling interactive data exploration and analysis on datasets with billions of rows.

## When to Use This Skill

Use Vaex when:
- Processing tabular datasets larger than available RAM (gigabytes to terabytes)
- Performing fast statistical aggregations on massive datasets
- Creating visualizations and heatmaps of large datasets
- Building machine learning pipelines on big data
- Converting between data formats (CSV, HDF5, Arrow, Parquet)
- Needing lazy evaluation and virtual columns to avoid memory overhead
- Working with astronomical data, financial time series, or other large-scale scientific datasets

## Core Capabilities

Vaex provides six primary capability areas, each documented in detail in the references directory:

### 1. DataFrames and Data Loading

Load and create Vaex DataFrames from various sources including files (HDF5, CSV, Arrow, Parquet), pandas DataFrames, NumPy arrays, and dictionaries. Reference `references/core_dataframes.md` for:
- Opening large files efficiently
- Converting from pandas/NumPy/Arrow
- Working with example datasets
- Understanding DataFrame structure

### 2. Data Processing and Manipulation

Perform filtering, create virtual columns, use expressions, and aggregate data without loading everything into memory. Reference `references/data_processing.md` for:
- Filtering and selections
- Virtual columns and expressions
- Groupby operations and aggregations
- String operations and datetime handling
- Working with missing data

### 3. Performance and Optimization

Leverage Vaex's lazy evaluation, caching strategies, and memory-efficient operations. Reference `references/performance.md` for:
- Understanding lazy evaluation
- Using `delay=True` for batching operations
- Materializing columns when needed
- Caching strategies
- Asynchronous operations

### 4. Data Visualization

Create interactive visualizations of large datasets including heatmaps, histograms, and scatter plots. Reference `references/visualization.md` for:
- Creating 1D and 2D plots
- Heatmap visualizations
- Working with selections
- Customizing plots and subplots

### 5. Machine Learning Integration

Build ML pipelines with transformers, encoders, and integration with scikit-learn, XGBoost, and other frameworks. Reference `references/machine_learning.md` for:
- Feature scaling and encoding
- PCA and dimensionality reduction
- K-means clustering
- Integration with scikit-learn/XGBoost/CatBoost
- Model serialization and deployment

### 6. I/O Operations

Efficiently read and write data in various formats with optimal performance. Reference `references/io_operations.md` for:
- File format recommendations
- Export strategies
- Working with Apache Arrow
- CSV handling for large files
- Server and remote data access

## Quick Start Pattern

For most Vaex tasks, follow this pattern:

```python
import vaex

# 1. Open or create DataFrame
df = vaex.open('large_file.hdf5')  # or .csv, .arrow, .parquet
# OR
df = vaex.from_pandas(pandas_df)

# 2. Explore the data
print(df)  # Shows first/last rows and column info
df.describe()  # Statistical summary

# 3. Create virtual columns (no memory overhead)
df['new_column'] = df.x ** 2 + df.y

# 4. Filter with selections
df_filtered = df[df.age > 25]

# 5. Compute statistics (fast, lazy evaluation)
mean_val = df.x.mean()
stats = df.groupby('category').agg({'value': 'sum'})

# 6. Visualize
df.plot1d(df.x, limits=[0, 100])
df.plot(df.x, df.y, limits='99.7%')

# 7. Export if needed
df.export_hdf5('output.hdf5')
```

## Working with References

The reference files contain detailed information about each capability area. Load references into context based on the specific task:

- **Basic operations**: Start with `references/core_dataframes.md` and `references/data_processing.md`
- **Performance issues**: Check `references/performance.md`
- **Visualization tasks**: Use `references/visualization.md`
- **ML pipelines**: Reference `references/machine_learning.md`
- **File I/O**: Consult `references/io_operations.md`

## Best Practices

1. **Use HDF5 or Apache Arrow formats** for optimal performance with large datasets
2. **Leverage virtual columns** instead of materializing data to save memory
3. **Batch operations** using `delay=True` when performing multiple calculations
4. **Export to efficient formats** rather than keeping data in CSV
5. **Use expressions** for complex calculations without intermediate storage
6. **Check memory with `df.byte_size()`** and inspect data with `df.describe()` before optimizing

## Common Patterns

### Pattern: Converting Large CSV to HDF5
```python
import vaex

# Open large CSV (processes in chunks automatically)
df = vaex.from_csv('large_file.csv')

# Export to HDF5 for faster future access
df.export_hdf5('large_file.hdf5')

# Future loads are instant
df = vaex.open('large_file.hdf5')
```

### Pattern: Efficient Aggregations
```python
# Use delay=True to batch multiple operations into ONE pass over the data.
# Each delayed call returns a promise; df.execute() runs them together.
mean_x = df.mean(df.x, delay=True)
std_y = df.std(df.y, delay=True)
sum_z = df.sum(df.z, delay=True)

df.execute()              # single pass triggers all pending delayed ops
print(mean_x.get(), std_y.get(), sum_z.get())  # retrieve each result
```

### Pattern: Virtual Columns for Feature Engineering
```python
# No memory overhead - computed on the fly
df['age_squared'] = df.age ** 2
df['full_name'] = df.first_name + ' ' + df.last_name
df['is_adult'] = df.age >= 18
```

## Resources

This skill includes reference documentation in the `references/` directory:

- `core_dataframes.md` - DataFrame creation, loading, and basic structure
- `data_processing.md` - Filtering, expressions, aggregations, and transformations
- `performance.md` - Optimization strategies and lazy evaluation
- `visualization.md` - Plotting and interactive visualizations
- `machine_learning.md` - ML pipelines and model integration
- `io_operations.md` - File formats and data import/export

