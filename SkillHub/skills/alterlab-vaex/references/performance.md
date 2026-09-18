# Performance and Optimization

This reference covers Vaex's performance features including lazy evaluation, caching, memory management, async operations, and optimization strategies for processing massive datasets.

## Understanding Lazy Evaluation

Lazy evaluation is the foundation of Vaex's performance:

### How Lazy Evaluation Works

```python
import vaex

df = vaex.open('large_file.hdf5')

# No computation happens here - just defines what to compute
df['total'] = df.price * df.quantity
df['log_price'] = df.price.log()
mean_expr = df.total.mean()

# Computation happens here (when result is needed)
result = mean_expr  # Now the mean is actually calculated
```

**Key concepts:**
- **Expressions** are lazy - they define computations without executing them
- **Materialization** happens when you access the result
- **Query optimization** happens automatically before execution

### When Does Evaluation Happen?

```python
# These trigger evaluation:
print(df.x.mean())                    # Accessing value
array = df.x.values                   # Getting NumPy array
pdf = df.to_pandas_df()              # Converting to pandas
df.export_hdf5('output.hdf5')       # Exporting

# These do NOT trigger evaluation:
df['new_col'] = df.x + df.y          # Creating virtual column
expr = df.x.mean()                    # Creating expression
df_filtered = df[df.x > 10]          # Creating filtered view
```

## Batching Operations with delay=True

Execute multiple operations together for better performance:

### Basic Delayed Execution

```python
# Without delay - each operation processes entire dataset
mean_x = df.x.mean()      # Pass 1 through data
std_x = df.x.std()        # Pass 2 through data
max_x = df.x.max()        # Pass 3 through data

# With delay - single pass through dataset.
# Each delayed call returns a promise; df.execute() runs all pending ops together.
mean_x = df.mean(df.x, delay=True)
std_x = df.std(df.x, delay=True)
max_x = df.max(df.x, delay=True)

df.execute()        # Single pass triggers all delayed operations
print(mean_x.get()) # mean
print(std_x.get())  # std
print(max_x.get())  # max
```

### Delayed Execution with Multiple Columns

```python
# Compute statistics for many columns efficiently.
# Build the promises first, run one pass, then collect with .get().
columns = ['sales', 'quantity', 'profit', 'cost']
promises = {
    column: (df.mean(df[column], delay=True), df.std(df[column], delay=True))
    for column in columns
}

df.execute()  # Single pass over the data

stats = {
    column: {'mean': mean_p.get(), 'std': std_p.get()}
    for column, (mean_p, std_p) in promises.items()
}
```

### When to Use delay=True

Use `delay=True` when:
- Computing multiple aggregations
- Computing statistics on many columns
- Building dashboards or reports
- Any scenario requiring multiple passes through data

```python
# Bad: 4 passes through dataset
mean1 = df.col1.mean()
mean2 = df.col2.mean()
mean3 = df.col3.mean()
mean4 = df.col4.mean()

# Good: 1 pass through dataset
promises = [
    df.mean(df.col1, delay=True),
    df.mean(df.col2, delay=True),
    df.mean(df.col3, delay=True),
    df.mean(df.col4, delay=True),
]
df.execute()
results = [p.get() for p in promises]
```

## Composing Delayed Computations

Vaex's delayed mechanism is promise-based (not Python `async`/`await`). Use the
`@vaex.delayed` decorator to chain post-processing onto delayed results; the whole
chain runs when `df.execute()` is called.

```python
import vaex

df = vaex.open('large_file.hdf5')

@vaex.delayed
def normalized_range(min_val, max_val):
    # Runs once the two delayed aggregations resolve
    return (max_val - min_val)

# Build the chain (nothing computed yet)
result = normalized_range(df.min(df.x, delay=True), df.max(df.x, delay=True))

df.execute()       # Single pass triggers the aggregations and the chained function
print(result.get())
```

### Retrieving a single delayed result

```python
# A delayed call returns a promise
promise = df.mean(df.x, delay=True)

# Do other work / build more promises...

df.execute()           # Trigger the pass over the data
result = promise.get() # Now the value is available
```

## Virtual Columns vs Materialized Columns

Understanding the difference is crucial for performance:

### Virtual Columns (Preferred)

```python
# Virtual column - computed on-the-fly, zero memory
df['total'] = df.price * df.quantity
df['log_sales'] = df.sales.log()
df['full_name'] = df.first_name + ' ' + df.last_name

# Check if a column is virtual
print('total' in df.virtual_columns)  # True = virtual (lazy expression)

# Benefits:
# - Zero memory overhead
# - Always up-to-date if source data changes
# - Fast to create
```

### Materialized Columns

```python
# Materialize an existing virtual column in place (computes once, stores in RAM).
# materialize(column=None) materializes all virtual columns when column is omitted.
df = df.materialize('total')

# When to materialize:
# - Column computed repeatedly (amortize cost)
# - Complex expression used in many operations
# - Need to export data
```

### Deciding: Virtual vs Materialized

```python
# Virtual is better when:
# - Column is simple (x + y, x * 2, etc.)
# - Column used infrequently
# - Memory is limited

# Materialize when:
# - Complex computation (multiple operations)
# - Used repeatedly in aggregations
# - Slows down other operations

# Example: Complex calculation used many times
df['complex'] = (df.x.log() * df.y.sqrt() + df.z ** 2).values  # Materialize
```

## Caching Strategies

Vaex automatically caches some operations, but you can optimize further:

### Automatic Caching

```python
# First call computes and caches
mean1 = df.x.mean()  # Computes

# Second call uses cache
mean2 = df.x.mean()  # From cache (instant)

# Cache invalidated if DataFrame changes
df['new_col'] = df.x + 1
mean3 = df.x.mean()  # Recomputes
```

### State Management

```python
# Save DataFrame state (includes virtual columns)
df.state_write('state.json')

# Load state later
df_new = vaex.open('data.hdf5')
df_new.state_load('state.json')  # Restores virtual columns, selections
```

### Checkpoint Pattern

```python
# Export intermediate results for complex pipelines
df['processed'] = complex_calculation(df)

# Save checkpoint
df.export_hdf5('checkpoint.hdf5')

# Resume from checkpoint
df = vaex.open('checkpoint.hdf5')
# Continue processing...
```

## Memory Management

Optimize memory usage for very large datasets:

### Memory-Mapped Files

```python
# HDF5 and Arrow are memory-mapped (optimal)
df = vaex.open('data.hdf5')  # No memory used until accessed

# File stays on disk, only accessed portions loaded to RAM
mean = df.x.mean()  # Streams through data, minimal memory
```

### Chunked Processing

```python
# Process large DataFrame in chunks
chunk_size = 1_000_000

for i1, i2, chunk in df.to_pandas_df(chunk_size=chunk_size):
    # Process chunk (careful: defeats Vaex's purpose)
    process_chunk(chunk)

# Better: Use Vaex operations directly (no chunking needed)
result = df.x.mean()  # Handles large data automatically
```

### Monitoring Memory Usage

```python
# Check DataFrame memory footprint
print(df.byte_size())  # Bytes used by materialized columns

# Check which columns are materialized vs virtual
for col in df.get_column_names():
    kind = 'virtual' if col in df.virtual_columns else 'materialized'
    print(f"{col}: {kind}")

# Time an operation
import time
start = time.time()
result = df.x.mean()
print(f"mean computed in {time.time() - start:.3f}s")
```

## Parallel Computation

Vaex automatically parallelizes operations:

### Multithreading

```python
# Vaex uses all CPU cores by default
import vaex

# Operations automatically parallelize across all cores
mean = df.x.mean()  # Uses all threads

# Cap the thread pool via the environment before importing vaex, e.g.:
#   VAEX_NUM_THREADS=8 python script.py
```

### Going Distributed

Vaex is single-machine out-of-core. If you genuinely need a multi-node cluster
(10s of TB, custom task graphs, a scheduler dashboard), reach for **Dask** instead
— see the `alterlab-dask` skill. Convert a column to a Dask array when you need to
hand data off:

```python
arr = df.x.to_dask_array()  # bridge a single column into the Dask ecosystem
```

## JIT Compilation

Vaex can JIT-compile arithmetic expressions for a speed boost.

### `.jit_numba()` / `.jit_pythran()` on expressions

```python
import vaex

df = vaex.open('large_file.hdf5')

# Build an expression as usual, then JIT-compile it.
# Vaex generates and compiles optimized code for the expression.
df['dist'] = (df.x ** 2 + df.y ** 2).jit_numba()   # requires numba
# Alternative backend: (df.x ** 2 + df.y ** 2).jit_pythran()

mean_dist = df.dist.mean()  # runs over the JIT-compiled expression
```

### Registering a custom Python function

```python
# Register a NumPy-vectorized function, then use it inside expressions.
@vaex.register_function()
def squared_sum(x, y):
    return x ** 2 + y ** 2  # x, y arrive as NumPy arrays

df['custom'] = df.func.squared_sum(df.x, df.y)
result = df.custom.mean()
```

## Optimization Strategies

### Strategy 1: Minimize Materializations

```python
# Bad: Creates many materialized columns
df['a'] = (df.x + df.y).values
df['b'] = (df.a * 2).values
df['c'] = (df.b + df.z).values

# Good: Keep virtual until final export
df['a'] = df.x + df.y
df['b'] = df.a * 2
df['c'] = df.b + df.z
# Only materialize if exporting:
# df.export_hdf5('output.hdf5')
```

### Strategy 2: Use Selections Instead of Filtering

```python
# Less efficient: Creates new DataFrames
df_high = df[df.value > 100]
df_low = df[df.value <= 100]
mean_high = df_high.value.mean()
mean_low = df_low.value.mean()

# More efficient: Use selections
df.select(df.value > 100, name='high')
df.select(df.value <= 100, name='low')
mean_high = df.value.mean(selection='high')
mean_low = df.value.mean(selection='low')
```

### Strategy 3: Batch Aggregations

```python
# Less efficient: Multiple passes
stats = {
    'mean': df.x.mean(),
    'std': df.x.std(),
    'min': df.x.min(),
    'max': df.x.max()
}

# More efficient: Single pass
promises = [
    df.mean(df.x, delay=True),
    df.std(df.x, delay=True),
    df.min(df.x, delay=True),
    df.max(df.x, delay=True),
]
df.execute()
stats = dict(zip(['mean', 'std', 'min', 'max'], [p.get() for p in promises]))
```

### Strategy 4: Choose Optimal File Formats

```python
# Slow: Large CSV
df = vaex.from_csv('huge.csv')  # Can take minutes

# Fast: HDF5 or Arrow
df = vaex.open('huge.hdf5')     # Instant
df = vaex.open('huge.arrow')    # Instant

# One-time conversion
df = vaex.from_csv('huge.csv', convert='huge.hdf5')
# Future loads: vaex.open('huge.hdf5')
```

### Strategy 5: Optimize Expressions

```python
# Less efficient: Repeated calculations
df['result'] = df.x.log() + df.x.log() * 2

# More efficient: Reuse calculations
df['log_x'] = df.x.log()
df['result'] = df.log_x + df.log_x * 2

# Even better: Combine operations
df['result'] = df.x.log() * 3  # Simplified math
```

## Performance Profiling

### Basic Profiling

```python
import time
import vaex

df = vaex.open('large_file.hdf5')

# Time operations
start = time.time()
result = df.x.mean()
elapsed = time.time() - start
print(f"Computed in {elapsed:.2f} seconds")
```

### Progress Reporting

```python
# Many Vaex operations accept progress=True to show a progress bar,
# which doubles as a rough timing/feedback tool for long passes.
result = df.groupby('category', agg={'value': 'sum'}, progress=True)
df.export_hdf5('out.hdf5', progress=True)
```

### Benchmarking Patterns

```python
# Compare strategies
def benchmark_operation(operation, name):
    start = time.time()
    result = operation()
    elapsed = time.time() - start
    print(f"{name}: {elapsed:.3f}s")
    return result

# Test different approaches
benchmark_operation(lambda: df.x.mean(), "Direct mean")
benchmark_operation(lambda: df[df.x > 0].x.mean(), "Filtered mean")
benchmark_operation(lambda: df.x.mean(selection='positive'), "Selection mean")
```

## Common Performance Issues and Solutions

### Issue: Slow Aggregations

```python
# Problem: Multiple separate aggregations
for col in df.column_names:
    print(f"{col}: {df[col].mean()}")

# Solution: Batch with delay=True
promises = [df.mean(df[col], delay=True) for col in df.column_names]
df.execute()
for col, p in zip(df.column_names, promises):
    print(f"{col}: {p.get()}")
```

### Issue: High Memory Usage

```python
# Problem: Materializing large virtual columns
df['large_col'] = (complex_expression).values

# Solution: Keep virtual, or materialize and export
df['large_col'] = complex_expression  # Virtual
# Or: df.export_hdf5('with_new_col.hdf5')
```

### Issue: Slow Exports

```python
# Problem: Exporting with many virtual columns
df.export_csv('output.csv')  # Slow if many virtual columns

# Solution: Export to HDF5 or Arrow (faster)
df.export_hdf5('output.hdf5')
df.export_arrow('output.arrow')

# Or materialize first for CSV
df_materialized = df.materialize()
df_materialized.export_csv('output.csv')
```

### Issue: Repeated Complex Calculations

```python
# Problem: Complex virtual column used repeatedly
df['complex'] = df.x.log() * df.y.sqrt() + df.z ** 3
result1 = df.groupby('cat1').agg({'complex': 'mean'})
result2 = df.groupby('cat2').agg({'complex': 'sum'})
result3 = df.complex.std()

# Solution: Materialize once
df['complex'] = (df.x.log() * df.y.sqrt() + df.z ** 3).values
# Or: df = df.materialize('complex')
```

## Performance Best Practices Summary

1. **Use HDF5 or Arrow formats** - Orders of magnitude faster than CSV
2. **Leverage lazy evaluation** - Don't force computation until necessary
3. **Batch operations with delay=True** - Minimize passes through data
4. **Keep columns virtual** - Materialize only when beneficial
5. **Use selections not filters** - More efficient for multiple segments
6. **Profile your code** - Identify bottlenecks before optimizing
7. **Avoid `.values` and `.to_pandas_df()`** - Keep operations in Vaex
8. **Parallelize naturally** - Vaex uses all cores automatically
9. **Export to efficient formats** - Checkpoint complex pipelines
10. **Optimize expressions** - Simplify math and reuse calculations

## Related Resources

- For DataFrame basics: See `core_dataframes.md`
- For data operations: See `data_processing.md`
- For file I/O optimization: See `io_operations.md`
