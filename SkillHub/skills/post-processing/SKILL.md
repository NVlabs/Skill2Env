---
name: post-processing
description: >
  Extract, analyze, and summarize simulation output data — pull spatial fields
  at specific timesteps, compute time-series trends and detect steady state,
  extract line profiles through the domain, generate statistical summaries
  and distributions, calculate derived quantities (gradients, fluxes, volume
  fractions, interface area), compare results against analytical solutions or
  experimental data, and produce automated analysis reports. Use when
  interpreting finished simulation results, checking mass or energy
  conservation, comparing two runs or meshes, extracting interface profiles
  from phase-field output, or preparing publication-quality analysis, even
  if the user only says "what do my results look like" or "did my simulation
  reach steady state."
allowed-tools: Read, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.1.3"
  security_tier: medium
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-23"
  eval_cases: 5
  last_reviewed: "2026-06-23"
  standards:
    - "Lp error norms (L1/L2/L-infinity) for numerical convergence/verification studies"
    - "Sample variance with Bessel's correction (n-1 denominator)"
    - "Marching squares/cubes iso-surface extraction (Lorensen & Cline, 1987)"
    - "Central finite differences for gradient computation"
    - "Cahn-Hilliard (conserved) and Allen-Cahn (non-conserved) phase-field dynamics"
---

# Post-Processing Skill

Analyze and extract meaningful information from simulation output data.

## Goal

Transform raw simulation output into actionable insights through field extraction, statistical analysis, derived quantities, visualizations, and comparison with reference data.

## Inputs to Gather

Before running post-processing scripts, collect:

1. **Output Data Location**
   - Path to simulation output files (JSON, CSV, HDF5, VTK)
   - Time step/snapshot indices of interest
   - Field names to extract

   > **Read field names from the file, never assume them.** Before extracting,
   > open the output file (or run `field_extractor.py --input <file> --list
   > --json`) and use only the field names that actually appear under `fields`.
   > Do not invent fields such as `temperature` if they are not present, and do
   > not assume a grid size — read the real `shape`/`count` from the data.

2. **Analysis Type**
   - Field extraction (spatial data at specific times)
   - Time series (temporal evolution of quantities)
   - Line profiles (1D cuts through domain)
   - Statistical summary (mean, std, distributions)
   - Derived quantities (gradients, integrals, fluxes)
   - Comparison to reference data

3. **Output Requirements**
   - Output format (JSON, CSV, tabular)
   - Visualization needs
   - Report format

## Scripts

| Script | Purpose | Key Inputs |
|--------|---------|------------|
| `field_extractor.py` | Extract field data from output files | --input, --field, --timestep |
| `time_series_analyzer.py` | Analyze temporal evolution | --input, --quantity, --window |
| `profile_extractor.py` | Extract line profiles | --input, --field, --start, --end |
| `statistical_analyzer.py` | Compute field statistics | --input, --field, --region |
| `derived_quantities.py` | Calculate derived quantities | --input, --quantity, --params |
| `comparison_tool.py` | Compare to reference data | --simulation, --reference, --metric |
| `report_generator.py` | Generate summary reports | --input, --template, --output |

## Workflow

### 1. Data Inventory

First, understand what data is available:

```bash
# List available fields and timesteps
python scripts/field_extractor.py --input results/ --list --json
```

### 2. Field Extraction

Extract spatial field data at specific timesteps:

```bash
# Extract concentration field at timestep 100
python scripts/field_extractor.py \
    --input results/field_0100.json \
    --field concentration \
    --json

# Extract multiple fields
python scripts/field_extractor.py \
    --input results/field_0100.json \
    --field "phi,concentration,temperature" \
    --json
```

### 3. Time Series Analysis

Analyze temporal evolution of quantities:

```bash
# Extract total energy vs time
python scripts/time_series_analyzer.py \
    --input results/history.json \
    --quantity total_energy \
    --json

# Compute moving average with window
python scripts/time_series_analyzer.py \
    --input results/history.json \
    --quantity mass \
    --window 10 \
    --json

# Detect steady state (relative-variation test; best for physical quantities)
python scripts/time_series_analyzer.py \
    --input results/history.json \
    --quantity residual \
    --detect-steady-state \
    --tolerance 1e-6 \
    --json

# Convergence by absolute threshold (physically correct test for residuals)
python scripts/time_series_analyzer.py \
    --input results/history.json \
    --quantity residual \
    --absolute-threshold 1e-6 \
    --json
```

### 4. Line Profile Extraction

Extract 1D profiles through the domain:

```bash
# Extract profile along x-axis at y=0.5
python scripts/profile_extractor.py \
    --input results/field_0100.json \
    --field concentration \
    --start "0,0.5,0" \
    --end "1,0.5,0" \
    --points 100 \
    --json

# Interface profile (through center)
python scripts/profile_extractor.py \
    --input results/field_0100.json \
    --field phi \
    --axis x \
    --slice-position 0.5 \
    --json
```

### 5. Statistical Analysis

Compute statistics over field data:

```bash
# Global statistics
python scripts/statistical_analyzer.py \
    --input results/field_0100.json \
    --field concentration \
    --json

# Statistics in a specific spatial region (1D/2D fields only).
# Coordinates are derived from the field shape and grid spacing
# (explicit dx/dy, or Lx/Ly via dx = Lx/(nx-1)); only the variables
# x, y, z compared against numbers, joined by and/or, are allowed.
python scripts/statistical_analyzer.py \
    --input results/field_0100.json \
    --field phi \
    --region "x>0.3 and x<0.7" \
    --json

# Distribution analysis
python scripts/statistical_analyzer.py \
    --input results/field_0100.json \
    --field phi \
    --histogram \
    --bins 50 \
    --json
```

### 6. Derived Quantities

Calculate physical quantities from raw data:

```bash
# Compute interface area
python scripts/derived_quantities.py \
    --input results/field_0100.json \
    --quantity interface_area \
    --threshold 0.5 \
    --json

# Compute gradient magnitude
python scripts/derived_quantities.py \
    --input results/field_0100.json \
    --quantity gradient_magnitude \
    --field phi \
    --json

# Compute volume fractions
python scripts/derived_quantities.py \
    --input results/field_0100.json \
    --quantity volume_fraction \
    --field phi \
    --threshold 0.5 \
    --json

# Compute flux through boundary
python scripts/derived_quantities.py \
    --input results/field_0100.json \
    --quantity boundary_flux \
    --field concentration \
    --boundary "x=0" \
    --json
```

### 7. Comparison with Reference

Compare simulation results to reference data:

```bash
# Compare to analytical solution
python scripts/comparison_tool.py \
    --simulation results/profile.json \
    --reference reference/analytical.json \
    --metric l2_error \
    --json

# Compare to experimental data
python scripts/comparison_tool.py \
    --simulation results/history.json \
    --reference experimental_data.csv \
    --metric rmse \
    --interpolate \
    --json

# Compare two simulations
python scripts/comparison_tool.py \
    --simulation results_fine/field.json \
    --reference results_coarse/field.json \
    --metric max_difference \
    --json
```

### 8. Report Generation

Generate automated reports:

```bash
# Generate summary report
python scripts/report_generator.py \
    --input results/ \
    --output report.json \
    --json

# Generate with specific sections
python scripts/report_generator.py \
    --input results/ \
    --sections "summary,statistics,convergence" \
    --output report.json \
    --json
```

## Typical Post-Processing Pipeline

For a complete simulation analysis:

```bash
python scripts/field_extractor.py --input results/ --list --json                                             # 1. inventory
python scripts/statistical_analyzer.py --input results/field_final.json --field phi --json                    # 2. final-state stats
python scripts/time_series_analyzer.py --input results/history.json --quantity residual --detect-steady-state --json   # 3. convergence
python scripts/derived_quantities.py --input results/field_final.json --quantity volume_fraction --field phi --json    # 4. derived quantities
python scripts/comparison_tool.py --simulation results/profile.json --reference benchmark/expected.json --metric l2_error --json   # 5. compare to reference
python scripts/report_generator.py --input results/ --output analysis_report.json --json                      # 6. summary report
```

## Interpretation Guidelines

### Time Series Analysis

Interpret convergence differently depending on the quantity type, because the
two signals the analyzer reports (`convergence.{rate,type}` and
`steady_state.reached`) answer different questions and can legitimately
disagree.

**Residual / error quantities** (e.g. `residual`, `error`):
- Judge convergence by **absolute magnitude vs a tolerance**: a residual at or
  below the target tolerance (e.g. `1e-6`) is converged. Use
  `--absolute-threshold <tol>` to get the `convergence_threshold` block, which
  is the physically correct test for residuals.
- The relative `--detect-steady-state` test answers "has the residual stopped
  changing?", not "has it converged?". For a still-decreasing residual,
  `steady_state.reached = false` is **expected and not a failure**.
- A **plateau** of a residual means a **stalled** solver
  (`convergence.type = "stalled"`), not steady state.
- **Reconcile the signals**: if `convergence.type` is `fast`/`linear` and the
  final residual is small (or `convergence_threshold.reached = true`), report
  the run as **converged** even when `steady_state.reached = false`.

**Physical quantities** (e.g. `energy`, `volume_fraction`, `mass`,
`interface_area`):
- **Monotonic decrease** in energy: system approaching equilibrium.
- **Plateau** (`steady_state.reached = true`): steady state reached.
- **Oscillations**: may indicate the time step is too large.
- **Sudden jumps**: possible numerical instability.

### Statistical Analysis
- **Bimodal distribution** of order parameter: Two-phase mixture
- **High variance**: Heterogeneous microstructure
- **Skewed distribution**: Asymmetric phase fractions

### Comparison Metrics
| Metric | Interpretation |
|--------|----------------|
| L2 error < 1% | Excellent agreement |
| L2 error 1-5% | Good agreement |
| L2 error 5-10% | Moderate agreement |
| L2 error > 10% | Poor agreement, investigate |

## Output Format

All scripts support the `--json` flag for machine-readable output. Most
scripts emit a **flat** top-level object whose keys depend on the script. For
example, `field_extractor.py --include-data` on a single field emits:

```json
{
    "field": "concentration",
    "found": true,
    "data": [[0.1, 0.9], [0.3, 0.6]],
    "shape": [2, 2],
    "min": 0.1,
    "max": 0.9,
    "mean": 0.475,
    "count": 4,
    "source_file": "results/field_0100.json",
    "timestep_info": {"timestep": 100, "time": 1.5}
}
```

Notes on envelope shapes (they are not uniform across scripts):

- `field_extractor.py`, `statistical_analyzer.py`, `time_series_analyzer.py`,
  `profile_extractor.py`, and `comparison_tool.py` emit a flat object with a
  `source_file` key plus script-specific result keys.
- `derived_quantities.py` wraps its payload in an `{ "inputs": {...},
  "results": {...} }` envelope.
- `report_generator.py` emits top-level `report_version` and `generator`
  keys plus the requested report sections.

No script emits top-level `script`, `version`, or `input_file` keys, and
field statistics (`min`/`max`/`mean`/`count`) appear at the top level, not
nested under a `data` object.

## Verification checklist

Before trusting or reporting a post-processing result, produce and record the
concrete evidence below (tied to this skill's scripts and output keys):

- [ ] **Listed the real fields first.** Ran `field_extractor.py --list --json`
      and recorded the actual `fields` names and `shape`; every later `--field`
      argument is one that appears in that list (no assumed `temperature`, no
      guessed grid size).
- [ ] **Used the right convergence test for the quantity type.** For a residual/error,
      recorded `convergence_threshold.reached` and `final_value` from
      `--absolute-threshold <tol>` (the `|x_final| <= tol` test) rather than
      relying on `steady_state.reached`; for a physical quantity, recorded
      `steady_state.{reached,relative_variation,value}` from `--detect-steady-state`.
- [ ] **Reconciled the two convergence signals.** Logged `convergence.type` and
      `convergence.rate` alongside `steady_state.reached`, and confirmed a
      `convergence.type = "stalled"` is read as a stalled solver (not steady
      state), and a still-decreasing residual with `steady_state.reached = false`
      is not reported as a failure.
- [ ] **Checked conservation against a tolerance.** Recorded the conserved
      integral (`derived_quantities.py --quantity mass` / `integral`, or
      `volume_fraction`) at the first and last timestep and confirmed the drift
      is within the documented tolerance for the dynamics (≈0 for Cahn-Hilliard
      conserved order parameter; expected to change for Allen-Cahn).
- [ ] **Confirmed grid spacing is physical.** Recorded the `spacing` block
      (`dx`/`dy`/`dz`) echoed by `derived_quantities.py` and verified it came
      from explicit `dx`/`dy` or the correct `Lx/(nx-1)` derivation — and that no
      `WARNING: explicit dx ... inconsistent with Lx` line was emitted to stderr.
- [ ] **Verified no non-finite values corrupted the result.** Confirmed
      derived-quantity scripts did not raise `Field contains non-finite value`
      (NaN/Inf) and that reported `min`/`max` are physically plausible (e.g. an
      order parameter stays within its expected bounds).
- [ ] **Qualified comparison error against the documented bands.** Recorded the
      `comparison_tool.py` metric value (e.g. `l2_error`) and mapped it to the
      agreement band in this skill (<1% excellent ... >10% poor, investigate),
      confirming the simulation and reference were aligned/interpolated onto the
      same axis first.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "`steady_state.reached = false`, so the solver didn't converge." | The relative steady-state test asks "has it stopped changing?", which is false for a still-decreasing residual. For residuals use `--absolute-threshold <tol>` and read `convergence_threshold.reached`; reconcile with `convergence.type`/`rate`. |
| "The residual plateaued, so it reached steady state." | A flat residual is a *stalled* solver (`convergence.type = "stalled"`, rate > 0.99), not convergence. Confirm the plateau value is actually at/below tolerance before calling it converged. |
| "I'll just extract `temperature` / assume a 256×256 grid." | Field names and shape are not guaranteed. Run `field_extractor.py --list --json` first and use only the `fields` and `shape` that the file actually reports. |
| "Two grids/runs agree, so the result is mesh-independent." | `comparison_tool.py` on two fields only bounds their difference; it does not establish the asymptotic range. Use >=3 resolutions to estimate an observed order before claiming mesh independence. |
| "Volume fraction looks stable, so mass is conserved." | A stable `volume_fraction` (a thresholded count) is not the conserved integral. Check `--quantity integral`/`mass` drift between first and last timestep against tolerance — and only expect ≈0 drift for conserved (Cahn-Hilliard) dynamics. |
| "Default `dx=1.0` is fine for the derived quantity." | When no spacing is in the file the scripts fall back to `dx=dy=dz=1.0`, so any length/area/flux/integral is in grid units, not physical units. Supply `--dx`/`--dy` (or `Lx`/`Ly` in the file) and verify the echoed `spacing` block. |
| "It ran and emitted JSON, so the numbers are valid." | Completion is not correctness. Verify conservation drift, the convergence verdict, finite values, and the comparison error band before reporting. |

## Security

### Input Validation
- User-provided field names are validated against `[a-zA-Z_][a-zA-Z0-9_.-]*` to prevent injection via crafted field names
- `statistical_analyzer.py` validates `--region` conditions against a strict allowlist before use: only the coordinate variables `x`, `y`, `z` compared (`< <= > >= == !=`) against numeric literals and joined by `and`/`or` are accepted; anything else exits with code 2. The parsed condition is applied as a real coordinate mask (no `eval`/`exec`), so the reported statistics describe the requested region
- `profile_extractor.py` validates the field name against the same pattern and point coordinates as finite numbers with max 3 dimensions
- `--metric` values in `comparison_tool.py` are validated against a fixed allowlist (`l1_error`, `l2_error`, `linf_error`, `rmse`, `mae`, `max_difference`, `correlation`, `r_squared`); unknown metrics return an error
- `--sections` in `report_generator.py` are validated against the known section names (`summary`, `statistics`, `convergence`, `validation`, `files`, `parameters`, `all`); unknown sections exit with code 2
- `--bins` (statistical_analyzer), `--points` (profile_extractor), and `--window` (time_series_analyzer) are validated as positive integers with upper bounds; out-of-range values exit with code 2

### File Access
- All JSON and CSV loading functions reject files exceeding 500 MB before parsing
- Loaded JSON files must have an object (dict) as root element
- `report_generator.py` caps directory listing at 10,000 entries to prevent resource exhaustion
- Scripts read user-specified simulation output files (JSON, CSV) but do not traverse directories beyond what is explicitly provided
- Output goes to stdout (JSON) unless the agent uses Write to save reports

### Tool Restrictions
- **Read**: Used to inspect script source, references, and simulation output files
- **Write**: Used to save analysis results, comparison reports, or generated summaries; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate simulation output files and search references
- The skill's `allowed-tools` excludes `Bash` to prevent the agent from executing arbitrary commands when processing untrusted simulation output files

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation — region parsing uses regex matching, never code evaluation
- All subprocess calls use explicit argument lists (no `shell=True`)
- Reduced tool surface (no Bash) limits the agent to read/write operations only
- Field names and region expressions are sanitized before use to prevent injection

## References

For detailed information, see:

- `references/data_formats.md` - Supported input/output formats
- `references/statistical_methods.md` - Statistical analysis methods
- `references/derived_quantities_guide.md` - Physical quantity calculations
- `references/comparison_metrics.md` - Error metrics and interpretation

## Requirements

- Python 3.10+
- NumPy (for numerical operations)
- No other external dependencies for core functionality

## Version History

See `CHANGELOG.md` for the authoritative record.

- v1.1.3 (2026-06-24): Added a "Verification checklist" (evidence-based, tied to
  the scripts' real output keys: field listing, residual-vs-physical convergence,
  signal reconciliation, conservation drift, grid-spacing sanity, non-finite
  guards, comparison error bands) and a "Common pitfalls & rationalizations"
  table before the Security section. Documentation only; no script behavior change.
- v1.1.2 (2026-06-23): Made the eval suite self-contained and discriminating —
  copied the real fixtures into `evals/files/` (only `phi`/`concentration` fields
  on a 10x10 grid; residual series ending at 5e-6), rewrote every eval prompt to
  reference those exact files, and added deterministic `script_checks` pinning the
  verified script outputs (including the correct verdict that the 1e-6 absolute
  residual threshold is NOT reached). Added guidance to read field names from the
  output file rather than assuming them.
- v1.1.1 (2026-06-23): Implemented real coordinate-based `--region` filtering in
  `statistical_analyzer.py`; fixed `report_generator.py` to read nested
  `fields.*.values` output; gave explicit `dx`/`dy`/`dz` precedence in
  `derived_quantities.py` grid spacing; added an `--absolute-threshold`
  convergence mode and residual-vs-physical interpretation guidance; corrected
  the Output Format example and version metadata; added `--bins`/`--window`
  bounds validation.
- v1.1.0 (2026-03-26): Optimized description, evaluation suite, security review,
  standardized metadata, CHANGELOG.
- v1.0.0 (2026-02-25): Initial release.
