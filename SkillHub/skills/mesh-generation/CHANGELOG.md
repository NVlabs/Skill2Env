# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- **Verification checklist** section (7 evidence-based items) tying trust in results to concrete artifacts from `grid_sizing.py` (`dx`, `counts`, `notes`) and `mesh_quality.py` (`aspect_ratio`, `quality_flags`, `skewness`), plus per-axis isotropy handling, stability cross-check, and a ≥3-grid convergence study.
- **Common pitfalls & rationalizations** table (6 rows) covering domain-specific shortcuts: misreading `skewness = 0.0` as a quality pass, two-grid "convergence", treating `high_aspect_ratio` as a defect, reusing isotropic `counts` for anisotropic domains, confusing points-per-domain with points-per-feature, and ignoring the dx/dt stability coupling after refinement.

## [1.2.0] - 2026-06-23

### Fixed
- **Skewness science (F1):** `mesh_quality.py` no longer reports a fabricated angle-based "skewness" for orthogonal Cartesian cells. Axis-aligned cells have all 90° interior angles, so true angular skewness is `0`; the script now returns `skewness = 0.0` and never raises `high_skewness`. The previous value (which equalled `1 - 1/aspect_ratio`) is preserved as the informational `size_anisotropy` field. Updated SKILL.md skewness table and `references/quality_metrics.md` accordingly.
- **2D cells (F2):** `mesh_quality.py --dz` is now optional; when omitted the cell is treated as 2D (`dims: 2`) instead of failing with "the following arguments are required: --dz". The documented high-aspect-ratio CLI example now runs as-is.
- **Off-by-one cell counts (F3):** when `dx` is derived from `--resolution`, `counts` is now set to the requested resolution directly (resolution=500 -> 500, was 501). When `--dx` is supplied explicitly, `length/dx` is snapped to the nearest integer within floating-point tolerance, preserving genuine partial cells.
- **Output documentation (F4):** SKILL.md Script Outputs table corrected to the real `results` schema (`dx`, `counts`, `notes`; `aspect_ratio`, `skewness`, `size_anisotropy`, `quality_flags`, `dims`, `notes`) and the `inputs`/`results` nesting.
- **Error-handling docs (F5):** corrected the error table to match actual messages and behavior (`resolution=1` is valid; messages and exit code 2 documented).

### Added
- `size_anisotropy`, `dims`, and `notes` fields to `mesh_quality.py` output.
- dx-override note in `grid_sizing.py` surfacing that `--resolution` is ignored when `--dx` is given (F8); SKILL.md note on per-dimension isotropy and how to mesh anisotropic domains.
- Regression unit tests for F1/F2/F3/F8 and the resolution=1 case.

### Changed
- Eval assertions (cases 1, 2, 4) updated to runnable commands and to pin the corrected skewness behavior as a regression guard.

## [1.1.0] - 2026-03-26

### Added
- Optimized description for agent discovery (agentskills.io compliant)
- Evaluation suite with test cases and assertions
- Security review documentation with risk tier classification
- Standardized metadata block (author, version, security_tier, tested_with)
- This CHANGELOG file

### Changed
- Updated SKILL.md frontmatter with metadata block

## [1.0.0] - 2026-02-25

### Added
- Initial release
- Grid resolution estimation from physics scales, aspect ratio and skewness quality checks, mesh type selection
- CLI scripts with --json output and argparse interface
- Reference documentation
