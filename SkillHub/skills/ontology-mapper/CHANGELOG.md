# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- **Verification checklist** section (6 evidence-based items) tying trust in results to
  concrete artifacts: empty/explained `results.validation_warnings`, recorded
  `match_type`/`confidence` per match, recorded `effective_system` and resolved Bravais
  Pearson symbol, lattice-constraint warning review, `unmatched`/`unmapped_fields`
  review, and `suggested_properties` triage.
- **Common pitfalls & rationalizations** table (6 rows) covering domain-specific
  shortcuts: trusting emitted annotations without reading `validation_warnings`, using
  ASMO for crystal/sample annotation, treating substring/description hits as
  high-confidence, "correcting" the 0.9 synonym precedence for terms that also match a
  class label, assuming a valid space group implies a consistent system, and assuming a
  free-text `structure` field resolved to a Bravais lattice.

## [1.2.0] - 2026-06-23

### Fixed
- **ASMO crystal/sample annotation correctness (F1):** `sample_annotator.py` now
  validates every emitted class/property against the loaded ontology summary. Terms not
  defined in the ontology are flagged with a `validation_warning` (and `confidence: 0.0`)
  and aggregated in a new `results.validation_warnings` field, instead of silently
  emitting unresolvable terms. Removed the invalid `crystal_output`, `sample_schema`,
  `material_type_rules` and `annotation_routing` blocks from `asmo_mappings.json` (ASMO
  is a simulation-methods ontology with no crystal/sample vocabulary); ASMO retains the
  concept-mapping path (`synonyms`/`property_synonyms`), which resolves correctly.
- **Unmatched-term suggestion (F4):** `concept_mapper.py` now emits a self-contained,
  runnable command — `python skills/ontology/ontology-explorer/scripts/class_browser.py
  --ontology <name> --search '<term>'` — including the correct path and required
  `--ontology` flag (placeholder when invoked via `--summary-file`).

### Changed
- **Confidence-score documentation (F3):** SKILL.md now states that the per-ontology
  synonym table is consulted before exact-label matching, so a term that is both a
  synonym key and a class label (e.g. `space group`, `unit cell`, `atom`) is reported as
  a 0.9 synonym match (matched class/IRI still correct).
- Documented that crystal/sample annotation is CMSO-only and that ASMO supports the
  concept-mapping path only.
- Corrected evals.json: eval #1 wording (synonym precedence), eval #4 assertion 3
  (`copper` is unmatched; `grain boundary` maps to Crystal Defect), runnable suggestion
  wording; added eval #6 covering the ASMO crystalline-sample validation regression.

### Security
- Hardened input validation to match the SKILL.md Security section: `--term`/`--terms`
  length (200 chars) and count (100) caps; `--bravais` validated against a fixed
  allowlist of recognized names/Pearson symbols; `--sample` key count (100) and string
  value length (500) caps.

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
- Concept-to-ontology mapping with confidence scores, crystal structure translation (Bravais/space group), full sample annotation generation
- CLI scripts with --json output and argparse interface
- Reference documentation
