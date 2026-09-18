# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- SKILL.md: "Verification checklist" section (7 evidence-based checkbox items)
  tying trust in results to concrete artifacts from the scripts'
  JSON outputs (stencil width/symmetry, coefficient sum-to-zero and catalog
  cross-check, even-accuracy exit code, `error_scale`/`reduction_if_halved`,
  >=3-grid observed-order study, explicit boundary stencils, and
  non-smooth scheme selection) and the `references/` guidance.
- SKILL.md: "Common pitfalls & rationalizations" table (7 rows) covering
  domain-specific shortcuts (treating the echoed `accuracy` field as a
  measured order, expecting odd central accuracy to round up, assuming
  monotone error improvement, two-grid "convergence", interior-only order
  claims, high-order central FD at shocks, and custom-offset misuse).

## [1.2.0] - 2026-06-23

### Fixed
- `stencil_generator.py`: central scheme now rejects odd `--accuracy` with
  `accuracy must be even for central` (exit 2) instead of silently rounding up
  and mislabeling the achieved order (F3).
- `stencil_generator.py`: added an upper bound on derivative order
  (`order must be <= 6`) and accuracy (`<= 8`), backing the Security
  "small, bounded matrices" claim (F4).
- SKILL.md Security/Input-Validation, Error-Handling table, Script-Outputs
  table, and Safety Measures corrected to match actual script behavior:
  `--scheme` allowlist is `central/forward/backward` (not upwind/compact),
  error message text matches the code, and the order upper bound is documented (F2, F4).
- SKILL.md CLI example for `truncation_error.py` no longer passes the
  unsupported `--order` flag (F1); evals.json eval 3 assertion 1 updated to
  match (F7).
- SKILL.md conversational example no longer injects an unjustified `--periodic`
  assumption; the scheme selector now consistently recommends Central FD for the
  central stencil that is generated (F6).

### Added
- `stencil_generator.py`: hardened custom `--offsets` handling (length cap of
  51, distinct-integer requirement, must exceed derivative order) and finite
  `--dx` validation.
- `truncation_error.py`: finite validation for `--dx`/`--scale` and an accuracy
  cap (`<= 12`).
- `scheme_selector.py`: for smooth (non-periodic) problems, now lists
  "Higher-order upwind (2nd/4th)" as an alternative and points to
  `truncation_error.py`, making the tool output self-supporting (F5).
- Regression unit tests for the central even-accuracy check, the order upper
  bound, custom-offset validation, finite-input validation, and the smooth
  scheme-selector recommendations.

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
- Finite-difference stencil generation (`--scheme` values: central/forward/backward), scheme selection (upwind/compact/spectral are conceptual recommendations emitted by `scheme_selector.py`, not stencil-generator schemes), truncation error estimation
- CLI scripts with --json output and argparse interface
- Reference documentation
