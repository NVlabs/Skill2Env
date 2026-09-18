---
name: performance-profiling
description: >
  Identify computational bottlenecks, analyze parallel scaling, estimate memory
  requirements, and generate optimization recommendations for materials
  simulations — parse timing logs to find dominant phases (solver, assembly,
  I/O), evaluate strong and weak scaling efficiency, profile memory from mesh
  and field parameters, and detect bottlenecks with actionable fix suggestions.
  Use when a simulation is running slower than expected, investigating MPI
  scaling efficiency, planning HPC resource allocation, deciding whether to
  tune the preconditioner or reduce I/O frequency, or estimating if a problem
  fits in available RAM, even if the user only says "my simulation is too
  slow" or "how many nodes do I need."
allowed-tools: Read, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.2.2"
  security_tier: medium
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 5
  last_reviewed: "2026-06-23"
  standards:
    - "Amdahl (1967), serial-fraction speedup law S(N)=1/(f+(1-f)/N)"
    - "Gustafson (1988), scaled speedup law S(N)=N-f(N-1)"
    - "Gropp, Lusk & Skjellum (1999), Using MPI (parallel scaling and communication)"
    - "Saad (2003), Iterative Methods for Sparse Linear Systems (solver/preconditioner choice)"
    - "Karypis & Kumar (1998), METIS multilevel graph partitioning (load balancing)"
---

# Performance Profiling

## Goal

Provide tools to analyze simulation performance, identify bottlenecks, and recommend optimization strategies for computational materials science simulations.

## Requirements

- Python 3.10+
- No external dependencies (uses Python standard library only)
- Works on Linux, macOS, and Windows

## Inputs to Gather

Before running profiling scripts, collect from the user:

| Input | Description | Example |
|-------|-------------|---------|
| Simulation log | Log file with timing information | `simulation.log` |
| Scaling data | JSON with multi-run performance data | `scaling_data.json` |
| Simulation parameters | JSON with mesh, fields, solver config | `params.json` |
| Available memory | System memory in GB (optional) | `16.0` |

## Decision Guidance

### When to Use Each Script

```
Need to identify slow phases?
├── YES → Use timing_analyzer.py
│         └── Parse simulation logs for timing data
│
Need to understand parallel performance?
├── YES → Use scaling_analyzer.py
│         └── Analyze strong or weak scaling efficiency
│
Need to estimate memory requirements?
├── YES → Use memory_profiler.py
│         └── Estimate memory from problem parameters
│
Need optimization recommendations?
└── YES → Use bottleneck_detector.py
          └── Combine analyses and get actionable advice
```

### Choosing Analysis Thresholds

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Phase dominance | <30% | 30-50% | >50% |
| Parallel efficiency | >0.80 | 0.70-0.80 | <0.70 |
| Memory usage | <60% | 60-80% | >80% |

## Script Outputs (JSON Fields)

All scripts wrap their payload in a top-level object with two keys: `inputs` and `results`. The fields below live under `results`.

| Script | Key Outputs (under `results`) |
|--------|-------------|
| `timing_analyzer.py` | `results.phases`, `results.slowest_phase`, `results.total_time` |
| `scaling_analyzer.py` | `results.results`, `results.efficiency_threshold_processors`, `results.average_efficiency`, `results.baseline` |
| `memory_profiler.py` | `results.total_memory_gb`, `results.per_process_gb`, `results.field_memory_gb`, `results.solver_workspace_gb`, `results.matrix_storage_gb`, `results.warnings` |
| `bottleneck_detector.py` | `results.bottlenecks`, `results.recommendations` |

## Workflow

### Complete Profiling Workflow

1. **Analyze timing** from simulation logs
2. **Analyze scaling** from multi-run data (if available)
3. **Profile memory** from simulation parameters
4. **Detect bottlenecks** and get recommendations
5. **Implement optimizations** based on recommendations
6. **Re-profile** to verify improvements

### Quick Profiling (Timing Only)

1. **Run timing analyzer** on simulation log
2. **Identify dominant phases** (>50% of runtime)
3. **Apply targeted optimizations** to dominant phases

## CLI Examples

### Timing Analysis

```bash
# Basic timing analysis
python3 scripts/timing_analyzer.py \
    --log simulation.log \
    --json

# Custom timing pattern
python3 scripts/timing_analyzer.py \
    --log simulation.log \
    --pattern 'Step\s+(\w+)\s+took\s+([\d.]+)s' \
    --json
```

### Scaling Analysis

```bash
# Strong scaling (fixed problem size)
python3 scripts/scaling_analyzer.py \
    --data scaling_data.json \
    --type strong \
    --json

# Weak scaling (constant work per processor)
python3 scripts/scaling_analyzer.py \
    --data scaling_data.json \
    --type weak \
    --json
```

### Memory Profiling

```bash
# Estimate memory requirements
python3 scripts/memory_profiler.py \
    --params simulation_params.json \
    --available-gb 16.0 \
    --json
```

### Bottleneck Detection

```bash
# Detect bottlenecks from timing only
python3 scripts/bottleneck_detector.py \
    --timing timing_results.json \
    --json

# Comprehensive analysis with all inputs
python3 scripts/bottleneck_detector.py \
    --timing timing_results.json \
    --scaling scaling_results.json \
    --memory memory_results.json \
    --json
```

## Conversational Workflow Example

**User**: My simulation is taking too long. Can you help me identify what's slow?

**Agent workflow**:
1. Ask for simulation log file
2. Run timing analyzer:
   ```bash
   python3 scripts/timing_analyzer.py --log simulation.log --json
   ```
3. Interpret results (the detector flags solver/assembly phases above 50% and I/O phases above 30%; >70% is high severity):
   - If solver dominates (>50%, high above 70%): Recommend preconditioner tuning
   - If assembly dominates (>50%): Recommend caching or vectorization
   - If I/O dominates (>30%): Recommend reducing output frequency
4. If user has multi-run data, analyze scaling:
   ```bash
   python3 scripts/scaling_analyzer.py --data scaling.json --type strong --json
   ```
5. Generate comprehensive recommendations:
   ```bash
   python3 scripts/bottleneck_detector.py --timing timing.json --scaling scaling.json --json
   ```

## Interpretation Guidance

### Timing Analysis

The detector applies per-type dominance thresholds: solver/assembly/general phases are flagged above **50%** of runtime; I/O phases above **30%**. Any flagged phase above **70%** is reported as high severity.

| Scenario | Meaning | Action |
|----------|---------|--------|
| Solver >50% (high >70%) | Solver-dominated | Tune preconditioner, check tolerance |
| Assembly >50% | Assembly-dominated | Cache matrices, vectorize, parallelize |
| I/O >30% | I/O-dominated | Reduce frequency, use parallel I/O |
| Balanced (below thresholds) | Well-balanced | Look for algorithmic improvements |

### Scaling Analysis

| Efficiency | Meaning | Action |
|------------|---------|--------|
| >0.80 | Excellent scaling | Continue scaling up |
| 0.70-0.80 | Good scaling | Monitor at larger scales |
| 0.50-0.70 | Poor scaling | Investigate communication/load balance |
| <0.50 | Very poor scaling | Reduce processor count or redesign |

### Memory Profile

| Usage | Meaning | Action |
|-------|---------|--------|
| <60% available | Safe | No action needed |
| 60-80% available | Moderate | Monitor, consider optimization |
| >80% available | High | Reduce resolution or increase processors |
| >100% available | Exceeds capacity | Must reduce problem size |

The estimate follows the three-term formula `Total = Field + Solver Workspace + Matrix Storage` (see `references/profiling_guide.md`). Matrix storage and solver workspace depend on `solver.type`:

- `iterative` (default): sparse matrix (default 7-point stencil, override via `solver.stencil_nnz`) plus workspace vectors.
- `direct`: sparse matrix scaled by a conservative fill-in factor (`solver.fillin_factor`, default 10) to reflect factorization fill-in — a direct solver estimates far more memory than an iterative one for the same mesh.
- `matrix-free`: no assembled matrix; workspace vectors only.

The estimate is intentionally conservative so a "will it fit in RAM?" decision does not silently under-estimate.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Log file not found` | Invalid path | Verify log file path |
| `No timing data found` | Pattern mismatch | Provide custom pattern with --pattern |
| `At least 2 runs required` | Insufficient data | Provide more scaling runs |
| `Missing required parameters` | Incomplete params | Add mesh and fields to params file |

## Optimization Strategies by Bottleneck Type

### Solver Bottlenecks
- Use algebraic multigrid (AMG) preconditioner
- Tighten solver tolerance if over-solving
- Consider direct solver for small problems
- Profile matrix assembly vs solve time

### Assembly Bottlenecks
- Cache element matrices if geometry is static
- Use vectorized assembly routines
- Consider matrix-free methods
- Parallelize assembly with coloring

### I/O Bottlenecks
- Reduce output frequency
- Use parallel I/O (HDF5, MPI-IO)
- Write to fast scratch storage
- Compress output data

### Scaling Bottlenecks
- Investigate communication overhead
- Check for load imbalance
- Reduce synchronization points
- Use asynchronous communication
- Consider hybrid MPI+OpenMP

### Memory Bottlenecks
- Reduce mesh resolution
- Use iterative solver (lower memory than direct)
- Enable out-of-core computation
- Increase number of processors
- Use single precision where appropriate

## Verification checklist

Before trusting a profiling result or acting on a recommendation, record the concrete evidence below:

- [ ] Confirmed `timing_analyzer.py` actually matched entries — `results.phases` is non-empty and `results.total_time` > 0; if a custom `--pattern` was used and `results.message`/`suggested_patterns` appeared, the pattern was fixed and re-run (an empty `phases` list silently looks like a fast simulation).
- [ ] Cross-checked that the sum of `phases[].percentage` is ~100% and that named phases cover the wall-clock time — unaccounted-for time means missing log lines, not a balanced run.
- [ ] For scaling claims, used >=2 runs spanning a real processor range and recorded `results.average_efficiency` and `results.efficiency_threshold_processors` from `scaling_analyzer.py`; verified the `--type` (strong vs weak) matches how the runs were generated (fixed total size vs fixed work-per-rank).
- [ ] Recorded the memory breakdown from `memory_profiler.py` (`field_memory_gb`, `solver_workspace_gb`, `matrix_storage_gb`, `total_memory_gb`) and confirmed `solver.type` (iterative / direct / matrix-free) matches the real solver — a direct solve carries the ~10x fill-in factor and a wrong type makes the "fits in RAM?" answer unsafe.
- [ ] Checked `results.warnings` and compared `total_memory_gb` (and `per_process_gb`) against the actual `--available-gb`; treated >80% as the documented "high" band, not a pass.
- [ ] For each `bottleneck_detector.py` recommendation, confirmed the driving `bottleneck` (its `category`, `value`, and `threshold`) is consistent with the timing/scaling/memory inputs that were actually supplied — recommendations only reflect the JSON files passed via `--timing`/`--scaling`/`--memory`.
- [ ] After implementing an optimization, re-ran the relevant analyzer and recorded the before/after `value` to confirm the bottleneck actually moved (re-profile step of the workflow).

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|------------------------------|
| "`timing_analyzer.py` returned no bottlenecks, so the run is balanced." | An empty/low result is often a pattern mismatch — `phases` may be empty or partial. Verify `total_time` matches wall-clock and that phase percentages sum to ~100% before concluding "balanced". |
| "Two runs scaled fine, so it scales." | Two points only give an average efficiency; they cannot reveal where efficiency falls off. Add more processor counts and check `efficiency_threshold_processors`, and confirm you used the correct `--type` (strong vs weak). |
| "Iterative vs direct is just a flag; memory is about the same." | `memory_profiler.py` applies a conservative ~10x fill-in factor for `direct` and stores no matrix for `matrix-free`. Setting the wrong `solver.type` can under-estimate RAM by an order of magnitude — set it to the real solver. |
| "It fits in `--available-gb` total, so we're fine." | The relevant number for an MPI run is `per_process_gb` against per-node/per-rank RAM, and >80% of total already triggers a warning. Check the per-process figure and the `warnings` list, not just the total. |
| "I/O is under 50%, so I/O isn't the bottleneck." | I/O is flagged at the lower **30%** threshold, not 50%. A 30-50% I/O phase is a real bottleneck the detector reports — reduce output frequency or use parallel I/O. |
| "The recommendation says tune the preconditioner, so the solver is the problem." | Recommendations are only as complete as the JSON you passed in. If `--scaling`/`--memory` were omitted, those bottlenecks are simply invisible — feed all available analyses before trusting the priority ranking. |

## Security

### Input Validation
- User-supplied `--pattern` regex values are validated for length (500 chars max) and rejected if they contain constructs prone to catastrophic backtracking (ReDoS)
- Scaling data entries are validated for finite time values, integer processor counts, and bounded run count (10,000 max)
- `available_gb` is validated as a positive finite number; mesh dimensions and field parameters are validated as positive integers
- `--type` (scaling type) is validated against a fixed allowlist (`strong`, `weak`)
- All loaded JSON files must have an object (dict) as root element

### File Access
- `timing_analyzer.py` reads a single log file specified by `--log`; log files are capped at 500 MB and rejected before parsing
- `scaling_analyzer.py`, `memory_profiler.py`, and `bottleneck_detector.py` read JSON files capped at 100 MB
- Phase names extracted from log files are truncated to 200 characters and stripped of control characters to prevent prompt-injection payloads from propagating into agent context
- No scripts write to the filesystem; all output goes to stdout

### Tool Restrictions
- **Read**: Used to inspect script source, references, simulation logs, and result files
- **Write**: Used to save profiling reports or optimization recommendations; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate log files, result files, and search references
- The skill's `allowed-tools` excludes `Bash` to prevent the agent from executing arbitrary commands when processing untrusted simulation logs or result files

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- Reduced tool surface (no Bash) limits the agent to read/write operations only
- Phase names and diagnostic strings are sanitized before inclusion in output to prevent injection

## Limitations

- **Log parsing**: Depends on pattern matching; may miss unusual formats
- **Scaling analysis**: Requires at least 2 runs for meaningful results
- **Memory estimation**: Approximate; actual usage may vary
- **Recommendations**: General guidance; may need domain-specific tuning

## References

- `references/profiling_guide.md` - Profiling concepts and interpretation
- `references/optimization_strategies.md` - Detailed optimization approaches

## Version History

See `CHANGELOG.md` for the authoritative, dated release history.
