# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- **Verification checklist** section (7 evidence-based checkbox items) tying agent self-checks to concrete script outputs: confirming `results.errors` is empty rather than trusting `valid`, recording each `domain_mismatch` warning with an explicit keep-or-move decision, checking `required_missing` before quoting `completeness_score`, verifying `suggestions[0]` exists before applying it, inspecting per-triple `results.results[i].valid` from `relationship_checker.py`, and confirming the correct `--ontology` was loaded.
- **Common pitfalls & rationalizations** table (7 rows) capturing domain-specific shortcuts and their corrections — e.g. high completeness score masking a missing required property, dismissing `domain_mismatch` warnings, blindly trusting `difflib` suggestions, treating partial relationship passes as success, equating `valid:true` with semantic correctness, and the exact-equality-not-substring subclass matching rule.

## [1.2.0] - 2026-06-23

### Fixed
- **Domain matching now uses exact class equality plus subclass traversal** instead of naive substring containment in both `completeness_checker.py` and `schema_checker.py`. Previously, because many CMSO class names are substrings of others (e.g. "Material" in "Crystalline Material", "Unit" in "Unit Cell"), the tools produced wrong completeness recommendations and missed/false domain-mismatch warnings. A bare `Material` no longer recommends `has crystallographic defect` (a `Crystalline Material` property); `Unit` (the measurement unit) no longer inherits `Unit Cell` properties; and `schema_checker.py` now correctly warns on a `Unit Cell`-domain property applied to `Unit`, while no longer warning when the class IS-A the domain (subclasses).
- Subclass-aware traversal also correctly credits subclasses with inherited domain properties (e.g. `Lattice Vector` inherits `Vector` component properties).

### Added
- Nearest-match suggestions: `schema_checker.py` now attaches a `suggestions` array (and an inline "did you mean 'X'?" hint) to `unknown_class` and `unknown_property` errors using stdlib `difflib`. Surfaces corrections that case-insensitive matching misses (e.g. `has_unit_cell` -> `has unit cell`, `CrystalStructurr` -> `Crystal Structure`).
- Input-validation caps across all three scripts (exit code 2 on violation): 1,000,000-byte cap on raw JSON inputs and annotation files; max 1000 annotations/relationships/provided properties per call; 500-character cap per class/property name; type checks that names are strings.

### Changed
- Corrected eval suite: eval 1 now uses the real property `has lattice parameter` (CMSO has no per-axis `has lattice parameter a`) so it is a clean positive case; eval 4 now asserts that nearest-match `suggestions` surface; eval 5 now uses `Atomic Scale Sample` with a genuine missing required property (`has simulation cell`, score 0.2) so its "low score / required_missing" assertions are truthful.
- SKILL.md: rewrote the Conversational Workflow Example to attribute the domain-mismatch insight to `schema_checker.py` (the tool that actually produces it) and the missing-required finding to `completeness_checker.py`; documented that `completeness_score` weights all property tiers equally so `required_missing` must be checked first; documented the new `suggestions` output and input caps.

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
- Schema validation for ontology annotations, completeness checking (required/recommended/optional properties), relationship domain/range verification
- CLI scripts with --json output and argparse interface
- Reference documentation
