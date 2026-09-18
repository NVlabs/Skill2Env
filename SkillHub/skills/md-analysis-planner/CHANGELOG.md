# Changelog

## 1.2.2 - 2026-06-24

- Add a "Verification checklist" section (7 evidence-based items) tying trust in
  trajectory-derived results to the planner's own outputs: `analysis_plan`
  statuses, `required_data` presence, diffusive-regime log-log slope ~1,
  Yeh-Hummer 1/L finite-size correction, PBC unwrap via `cell` + `image flags`,
  the `equilibration_checks`, and block-averaged uncertainties.
- Add a "Common pitfalls & rationalizations" section (6 rows) documenting
  domain-specific MD post-processing shortcuts (fitting non-diffusive MSD,
  skipping the finite-size correction, using wrapped positions, faking VACF/VDOS
  without velocities, fitting before equilibration, quoting values without error
  bars) and the correct practice for each.

## 1.1.0 - 2026-06-23

- Fix status demotion bug (F1): a `blocked` goal (e.g. VACF/VDOS with no stored
  velocities) is no longer silently downgraded to `needs time axis` when the
  timestep is also missing. Statuses now follow a strict severity ordering
  (`blocked` > `needs time axis` > `needs review` > `ready`) and are never
  demoted. Both relevant warnings are still emitted.
- Surface safety-critical fields in the default non-JSON output (F2): the
  human-readable mode now prints `Required data:`, a `PBC:` note, and a
  `Warnings:` section (also mirrored to stderr).
- Add diffusion guidance to the structured output (F4): emit diffusive-regime
  (log-log MSD slope ~1) and Yeh-Hummer 1/L finite-size warnings, and include
  `cell` and `image flags` in `required_data` when an unwrap is required.
- Repair eval case `vacf_missing_velocities` (F3): with the F1 fix the faithful
  positions-only/no-timestep VDOS run now genuinely reports `blocked`, so the
  expected `blocked` token is produced.
- Harden input validation to match the documented Security safeguards: cap
  `system`/`trajectory_format`/goal length (256 chars) and goal count (64);
  invalid input exits with code 2.
- Add regression unit tests for each fix.

## 1.0.0 - 2026-05-18

- Initial MD analysis planning skill.
