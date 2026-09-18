---
name: mesh-generation
description: >
  Plan and evaluate mesh generation for numerical simulations — estimate grid
  resolution from physics scales (interface width, boundary layers, wavelengths),
  check aspect ratios and skewness against quality thresholds, choose between
  structured, unstructured, and adaptive mesh refinement strategies, and compute
  grid sizing for 1D/2D/3D domains. Use when setting up a new mesh, diagnosing
  poor solver convergence caused by mesh quality, deciding how many points to
  place across a phase-field interface or boundary layer, or preparing a mesh
  convergence study, even if the user only asks "what resolution do I need"
  or "why is my solver failing."
allowed-tools: Read, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.2.2"
  standards:
    - "ANSYS Fluent/ICEM equiangle skewness metric (max(|90-theta|)/90 for quads/hexes; (theta_max-60)/120 for triangles)"
    - "Knupp (2001), Algebraic mesh quality metrics (aspect ratio, Jacobian ratio, warpage)"
    - "Shewchuk (2002), What Is a Good Linear Finite Element? (triangle radius-ratio and minimum-angle quality, Delaunay)"
    - "Jasak (1996) / OpenFOAM finite-volume non-orthogonality correction"
    - "Roache (1998), Verification and Validation in Computational Science (grid/mesh convergence study)"
  security_tier: medium
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 4
  last_reviewed: "2026-06-23"
---

# Mesh Generation

## Goal

Provide a consistent workflow for selecting mesh resolution and checking mesh quality for PDE simulations.

## Requirements

- Python 3.10+
- No external dependencies (uses stdlib)

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Domain size | Physical dimensions | `1.0 × 1.0 m` |
| Feature size | Smallest feature to resolve | `0.01 m` |
| Points per feature | Resolution requirement | `10 points` |
| Aspect ratio limit | Maximum dx/dy ratio | `5:1` |
| Quality threshold | Skewness limit | `< 0.8` |

## Decision Guidance

### Resolution Selection

```
What is the smallest feature size?
├── Interface width → dx ≤ width / 5
├── Boundary layer → dx ≤ layer_thickness / 10
├── Wave length → dx ≤ lambda / 20
└── Diffusion length → dx ≤ sqrt(D × dt) / 2
```

### Mesh Type Selection

| Problem | Recommended Mesh |
|---------|------------------|
| Simple geometry, uniform | Structured Cartesian |
| Complex geometry | Unstructured triangular/tetrahedral |
| Boundary layers | Hybrid (structured near walls) |
| Adaptive refinement | Quadtree/Octree or AMR |

## Script Outputs (JSON Fields)

All scripts emit a top-level object with `inputs` (the echoed CLI values) and
`results` (the computed fields below). Index as `result["results"]["..."]`.

| Script | `results` Fields |
|--------|------------------|
| `scripts/grid_sizing.py` | `dx`, `counts` (list of per-dimension cell counts, length == `dims`), `notes` |
| `scripts/mesh_quality.py` | `aspect_ratio`, `skewness`, `size_anisotropy`, `quality_flags`, `dims`, `notes` |

`mesh_quality.py` describes axis-aligned (orthogonal Cartesian) cells defined
purely by edge spacings. For such cells every interior angle is 90°, so the true
angular `skewness` is always `0.0` and `high_skewness` is never flagged.
Cell elongation is reported separately via `aspect_ratio` and the redundant
convenience field `size_anisotropy` (= `1 - 1/aspect_ratio`).

## Workflow

1. **Estimate resolution** - From physics scales
2. **Compute grid sizing** - Run `scripts/grid_sizing.py`
3. **Check quality metrics** - Run `scripts/mesh_quality.py`
4. **Adjust if needed** - Fix aspect ratios, reduce skewness
5. **Validate** - Mesh convergence study

## Conversational Workflow Example

**User**: I need to mesh a 1mm × 1mm domain for a phase-field simulation with interface width of 10 μm.

**Agent workflow**:
1. Compute grid sizing:
   ```bash
   python3 scripts/grid_sizing.py --length 0.001 --resolution 200 --json
   ```
2. Verify interface is resolved: dx = 5 μm, interface width = 10 μm → 2 points per interface width.
3. Recommend: Increase to 500 points (dx = 2 μm) for 5 points across interface.

## Pre-Mesh Checklist

- [ ] Define target resolution per feature/interface
- [ ] Ensure dx meets stability constraints (see numerical-stability)
- [ ] Check aspect ratio < limit (typically 5:1)
- [ ] Check skewness < threshold (typically 0.8)
- [ ] Validate mesh convergence with refinement study

## CLI Examples

```bash
# Compute grid sizing for 1D domain
python3 scripts/grid_sizing.py --length 1.0 --resolution 200 --json

# Check mesh quality (3D cell)
python3 scripts/mesh_quality.py --dx 1.0 --dy 0.5 --dz 0.5 --json

# High aspect ratio check (2D cell; --dz omitted is treated as 2D)
python3 scripts/mesh_quality.py --dx 1.0 --dy 0.1 --json
```

## Error Handling

All validation errors are written to stderr and the script exits with code `2`.

| Error message | Cause | Resolution |
|---------------|-------|------------|
| `length must be positive, got ...` | Non-positive domain size | Use a positive value |
| `resolution must be positive, got ...` | Non-positive resolution (`resolution=1` is a valid single-cell mesh) | Use a positive integer |
| `dims must be one of (1, 2, 3), got ...` | Unsupported dimension count | Use `1`, `2`, or `3` |
| `<name> must be a finite positive number, got ...` | `dx`/`dy`/`dz` not finite or not positive | Use a finite positive value |
| `<name> exceeds maximum (...), got ...` | Input above the resource-exhaustion bound | Use a smaller value |

## Interpretation Guidance

### Aspect Ratio

| Aspect Ratio | Quality | Impact |
|--------------|---------|--------|
| 1:1 | Excellent | Optimal accuracy |
| 1:1 - 3:1 | Good | Acceptable |
| 3:1 - 5:1 | Fair | May affect accuracy |
| > 5:1 | Poor | Solver issues likely |

### Skewness

Skewness is the angular deviation from the ideal cell shape
(`max(|90° - θ_i|) / 90°` for quads/hexes — see `references/quality_metrics.md`).
`mesh_quality.py` works from axis-aligned edge spacings, which describe
orthogonal Cartesian cells whose interior angles are all exactly 90°; it
therefore always reports `skewness = 0.0` for these cells. The thresholds below
apply when a genuine skewness value is obtained from real cell-corner geometry
(e.g. from an unstructured mesh), not from `dx/dy/dz` spacings.

| Skewness | Quality | Impact |
|----------|---------|--------|
| 0 - 0.25 | Excellent | Optimal |
| 0.25 - 0.50 | Good | Acceptable |
| 0.50 - 0.80 | Fair | May affect accuracy |
| > 0.80 | Poor | Likely problems |

> Note: cell elongation is **not** skewness. An anisotropic but orthogonal cell
> (e.g. a wall-aligned boundary-layer cell) has high `aspect_ratio` /
> `size_anisotropy` but zero skewness, and is often perfectly acceptable.

### Resolution Guidelines

| Application | Points per Feature |
|-------------|-------------------|
| Phase-field interface | 5-10 |
| Boundary layer | 10-20 |
| Shock | 3-5 (with capturing) |
| Wave propagation | 10-20 per wavelength |
| Smooth gradients | 5-10 |

## Verification checklist

- [ ] Recorded `dx` and `counts` from `grid_sizing.py --json` and confirmed the smallest physical feature gets enough points (interface ≥5×dx, boundary layer ≥10×dx, wavelength ≥20×dx per Resolution Selection above).
- [ ] For an anisotropic domain, ran `grid_sizing.py` once per differing edge length (or applied `--dx` per axis) — did NOT apply a single `--length`-derived count to unequal edges.
- [ ] Checked the `notes` field for "Grid does not fully cover length" and resolved any partial-coverage warning before trusting `counts`.
- [ ] Logged `aspect_ratio` and `quality_flags` from `mesh_quality.py --json`; confirmed `high_aspect_ratio` is absent OR that the elongation is intentional and physics-aligned (e.g. wall-aligned boundary-layer cell with AR≤100 along the wall).
- [ ] Confirmed the reported `skewness = 0.0` is the expected orthogonal-Cartesian result, NOT a measured quality pass — for unstructured/non-orthogonal cells, obtained a real angle-based skewness from cell-corner geometry and checked it against the <0.8 threshold.
- [ ] Verified `dx` also satisfies the solver's stability constraint (cross-check with numerical-stability) before committing to the resolution.
- [ ] Ran a mesh convergence study (≥3 successively refined grids) and confirmed the quantity of interest changes monotonically/asymptotically before declaring the mesh adequate.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|------------------------------|
| "`skewness` came back 0.0, so the mesh quality is fine." | `mesh_quality.py` always returns `skewness = 0.0` for axis-aligned spacings — it is a definitional property of orthogonal cells, not a measurement. Real skewness needs cell-corner angles from an unstructured mesh; don't read 0.0 as a passing quality check. |
| "Two grids gave nearly the same answer, so the mesh is converged." | Two grids cannot establish the observed order or the asymptotic range. Use ≥3 successively refined grids and confirm the quantity of interest is converging before quoting any result as mesh-independent. |
| "High `aspect_ratio` was flagged, so the cell is bad." | Elongation is not skewness. A wall-aligned boundary-layer cell with AR up to ~100 is acceptable when aligned with the flow/field; check `size_anisotropy` and the physics, not just the `high_aspect_ratio` flag. |
| "I'll set one `--length` and reuse the `counts` for all axes." | `grid_sizing.py` is isotropic per call — it applies the single derived count to every dimension. For unequal edges this over/under-resolves axes; run it per edge length or supply `--dx` per axis. |
| "`dx = length/resolution` resolves my feature because resolution is large." | Points-per-domain is not points-per-feature. A fine global `dx` can still place too few cells across a thin interface/layer; check `feature_size / dx` against the Resolution Guidelines (5-10 for interfaces, 10-20 for boundary layers). |
| "The mesh is fine enough, so I can ignore the time step." | Mesh resolution and temporal stability are coupled: shrinking `dx` tightens explicit CFL/diffusion limits. A refined mesh that violates the solver's stability constraint diverges — re-check `dt` against numerical-stability after any refinement. |

## Security

### Input Validation
- All inputs (`length`, `resolution`, `dx`, `dy`, `dz`) are validated as finite positive numbers with upper bounds to prevent resource exhaustion
- `dims` is restricted to `{1, 2, 3}`
- `argparse` type parameters reject non-numeric input at the CLI boundary before any processing occurs

### File Access
- Scripts read no external files; all inputs are provided via CLI arguments
- Scripts write only to stdout (JSON output); no files are created unless the agent explicitly uses the Write tool

### Tool Restrictions
- **Read**: Used to inspect script source, references, and user configuration files
- **Write**: Used to save grid sizing results or mesh quality reports; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate relevant files and search references
- The skill's `allowed-tools` excludes `Bash` to prevent the agent from executing arbitrary commands when processing user-provided inputs

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- Reduced tool surface (no Bash) means the agent should use `Read` and `Write` to prepare inputs and capture outputs rather than constructing shell commands from user text
- All output is deterministic JSON with no shell-interpretable content

## Limitations

- **2D/3D only**: No unstructured mesh generation
- **Quality metrics**: Aspect ratio and size anisotropy from axis-aligned spacings only; skewness is reported as 0 for these orthogonal cells (true angular skewness requires real cell-corner geometry)
- **No mesh generation**: Sizing recommendations only
- **Isotropic per call**: `grid_sizing.py` takes a single `--length` and applies the resulting count to every dimension. For an anisotropic domain (e.g. 10 cm × 5 cm), run it once per differing edge length, or compute `dx` from physics and apply it per axis (e.g. `--length 0.10 --dx 5e-5`, then `--length 0.05 --dx 5e-5`).

## References

- `references/mesh_types.md` - Structured vs unstructured
- `references/quality_metrics.md` - Aspect ratio/skewness thresholds

## Version History

- **v1.2.0** (2026-06-23): Corrected skewness science (orthogonal cells now report skewness 0), added `size_anisotropy`, made `mesh_quality.py --dz` optional (2D cells), fixed grid_sizing off-by-one for resolution-derived counts, surfaced dx-override note, corrected output/error-handling docs
- **v1.1.0** (2024-12-24): Enhanced documentation, decision guidance, examples
- **v1.0.0**: Initial release with 2 mesh quality scripts
