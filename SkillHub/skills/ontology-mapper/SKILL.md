---
name: ontology-mapper
description: >
  Map materials science terms, crystal structures, and sample descriptions to
  standardized ontology classes and properties — resolve natural-language
  concepts to ontology entries with confidence scores, translate Bravais
  lattice types, space groups, and lattice constants into ontology-compliant
  annotations, and produce full sample metadata from structured descriptions.
  Supports any ontology in ontology_registry.json (CMSO, ASMO, etc.). Use
  when annotating simulation inputs with FAIR metadata, translating "BCC
  iron" or "FCC copper" into formal ontology terms, preparing machine-
  readable sample descriptions, or bridging between lab vocabulary and
  ontology vocabulary, even if the user only says "what CMSO terms describe
  my material" or "annotate this sample for me."
allowed-tools: Read, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.2.2"
  security_tier: low
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 6
  last_reviewed: "2026-06-23"
  standards:
    - "CMSO (Computational Material Sample Ontology)"
    - "ASMO (Atomistic Simulation Methods Ontology)"
    - "International Tables for Crystallography (7 crystal systems, 14 Bravais lattices via Pearson symbols, 230 space groups)"
    - "FAIR data principles (Wilkinson et al. 2016)"
---

# Ontology Mapper

## Goal

Translate real-world materials science descriptions into standardized ontology annotations. Given terms like "FCC copper" or structured data like `{"material": "iron", "structure": "BCC", "lattice_a": 2.87}`, produce the corresponding ontology classes and properties for any registered ontology.

## Requirements

- Python 3.10+
- No external dependencies (Python standard library only)
- Requires ontology-explorer's summary JSON and `ontology_registry.json`
- Per-ontology mapping config (`<name>_mappings.json`) for ontology-specific synonyms and labels

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Ontology | Ontology name from registry | `cmso`, `asmo` |
| Term(s) | Natural-language materials concept(s) | `"unit cell"`, `"FCC,copper,lattice"` |
| Crystal system | One of the 7 crystal systems | `cubic`, `hexagonal` |
| Bravais lattice | Lattice type (symbol or common name) | `FCC`, `cF`, `BCC` |
| Space group | Space group number (1-230) | `225` |
| Lattice parameters | a, b, c in angstroms; alpha, beta, gamma in degrees | `a=3.615` |
| Sample description | JSON dict with material properties | `{"material":"copper","structure":"FCC"}` |

## Decision Guidance

```
What do you need to map?
├── A concept or term to find its ontology class
│   └── concept_mapper.py --ontology <name> --term "<term>"
├── Crystal structure parameters to ontology terms
│   └── crystal_mapper.py --ontology <name> --bravais <type> --space-group <N> --a <val>
├── A full sample description to ontology annotations
│   └── sample_annotator.py --ontology <name> --sample '<json>'
└── Multiple terms at once
    └── concept_mapper.py --ontology <name> --terms "term1,term2,term3"
```

> **Ontology scope — crystal/sample annotation is CMSO-only.** `crystal_mapper.py`
> and `sample_annotator.py` emit crystal-structure vocabulary (Crystalline Material,
> Crystal Structure, Unit Cell, Space Group, lattice properties). This vocabulary is
> defined by **CMSO**. **ASMO is a simulation-methods ontology and does not define any
> crystal/sample classes** — so for ASMO use the concept-mapping path
> (`concept_mapper.py`, which resolves terms like DFT, NPT, timestep, PBE to real ASMO
> classes) only. If `sample_annotator.py`/`crystal_mapper.py` is run with an ontology
> whose summary lacks the required classes (e.g. `--ontology asmo`), each unresolvable
> term is flagged in `results.validation_warnings` and given `confidence: 0.0` rather
> than silently emitting an invalid term.

## Script Outputs (JSON Fields)

| Script | Key Outputs |
|--------|-------------|
| `scripts/concept_mapper.py` | `results.matches`, `results.unmatched`, `results.suggestions` |
| `scripts/crystal_mapper.py` | `results.ontology_classes`, `results.ontology_properties`, `results.effective_system`, `results.bravais_lattice`, `results.validation_warnings` |
| `scripts/sample_annotator.py` | `results.annotations`, `results.sample_type`, `results.material_type`, `results.unmapped_fields`, `results.suggested_properties`, `results.validation_warnings` |

## Workflow

1. If the user provides natural-language terms, use `concept_mapper.py` to find matching ontology classes.
2. If the user describes crystal structure parameters, use `crystal_mapper.py` to map them and validate constraints.
3. For a complete sample description, use `sample_annotator.py` to produce full ontology annotations.
4. Review any validation warnings (e.g., lattice parameter mismatches for the crystal system).
5. Check `unmapped_fields` and `suggested_properties` for completeness.

## Conversational Workflow Example

```
User: I'm setting up an MD simulation of BCC iron with lattice parameter 2.87 angstroms.
      What CMSO terms should I use?

Agent: Let me map your iron sample to CMSO ontology terms.

[Runs: sample_annotator.py --ontology cmso --sample '{"material":"iron","structure":"BCC","lattice_a":2.87,"space_group":229}' --json]

Your BCC iron simulation maps to these CMSO annotations:

- **Sample**: Atomic Scale Sample (subclass of Computational Sample)
- **Material**: Crystalline Material
- **Unit Cell**: Bravais lattice = "cI" (body-centered cubic)
- **Space Group**: number = 229 (Im-3m)
- **Lattice**: a = 2.87 Å
- **Element**: Fe

Suggested additions:
- Number of atoms in the simulation cell
- Simulation cell vectors and angles
```

## CLI Examples

```bash
# Map a single concept
python3 skills/ontology/ontology-mapper/scripts/concept_mapper.py \
  --ontology cmso --term "space group" --json

# Map multiple terms
python3 skills/ontology/ontology-mapper/scripts/concept_mapper.py \
  --ontology cmso --terms "FCC,copper,lattice constant" --json

# Map crystal parameters (with ontology-specific labels)
python3 skills/ontology/ontology-mapper/scripts/crystal_mapper.py \
  --ontology cmso --bravais FCC --space-group 225 --a 3.615 --json

# Map crystal parameters (generic labels, no ontology specified)
python3 skills/ontology/ontology-mapper/scripts/crystal_mapper.py \
  --bravais FCC --space-group 225 --a 3.615 --json

# Annotate a full sample
python3 skills/ontology/ontology-mapper/scripts/sample_annotator.py \
  --ontology cmso \
  --sample '{"material":"copper","structure":"FCC","space_group":225,"lattice_a":3.615}' \
  --json
```

## Adding a New Ontology

To support a new ontology, create a `<name>_mappings.json` in `references/`:

```json
{
  "ontology": "myonto",
  "synonyms": { "simulation method": "Simulation Method", ... },
  "property_synonyms": { "timestep": "has timestep", ... },
  "material_type_rules": { "keyword_rules": [...], "default": "Material" },
  "sample_schema": { "sample_class": "Simulation", ... },
  "crystal_output": { "base_classes": [...], "property_map": {...} },
  "annotation_routing": { "unit_cell_indicators": [...], ... }
}
```

Then add `"mappings_file": "myonto_mappings.json"` to the ontology's entry in `ontology_registry.json`. No code changes needed.

**Only include the `sample_schema`, `crystal_output`, `material_type_rules` and
`annotation_routing` blocks if every class/property they name actually exists in that
ontology's summary.** `sample_annotator.py` validates emitted terms against the loaded
summary and flags any that are undefined (`results.validation_warnings`, `confidence: 0.0`).
For example, `asmo_mappings.json` deliberately ships **only** `synonyms` and
`property_synonyms` because ASMO is a simulation-methods ontology with no crystal/sample
vocabulary — its concept terms (DFT, NPT, timestep, PBE) all resolve, but a crystal/sample
config would emit unresolvable terms.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `space_group must be between 1 and 230` | Invalid space group number | Use a valid space group number |
| `a must be positive` | Non-positive lattice parameter | Provide positive values in angstroms |
| `Unrecognized Bravais lattice '<x>'` | Bravais symbol/name not in the recognized set | Use a common name (FCC, BCC, HCP) or a Pearson symbol (cF, cI, hP, ...) |
| `Term exceeds maximum length of 200 characters` | A `--term`/`--terms` entry is too long | Shorten the term |
| `Too many terms (max 100)` | More than 100 terms supplied | Split into smaller batches |
| `Sample must be a non-empty dict` | Empty or missing sample data | Provide a valid JSON sample dict |
| `Sample has too many keys (max 100)` | Oversized sample dict | Reduce the number of sample keys |
| Validation warnings (lattice) | Lattice parameters inconsistent with crystal system | Check that a=b=c for cubic, etc. |
| `results.validation_warnings` (terms) | Emitted class/property not defined in the chosen ontology (e.g. crystal terms for ASMO) | Use CMSO for crystal/sample annotation; use ASMO only for concept mapping |

## Interpretation Guidance

- **Confidence scores**: 1.0 = exact label match, 0.9 = synonym-table match, 0.7 = substring match, 0.5 = description match. Note: the per-ontology synonym table is consulted *before* exact-label matching, so a term that is both a synonym key and a class label (e.g. `space group`, `unit cell`, `atom`) is reported as a 0.9 synonym match even though it coincides exactly with a class label — the matched class and IRI are still correct.
- **`sample_annotator.py` validation warnings**: every emitted class/property is checked against the loaded ontology summary. Terms not defined in that ontology are flagged in `results.validation_warnings` (and the corresponding annotation gets a `validation_warning` field with `confidence: 0.0`). This is how the annotator signals that a crystal/sample term cannot resolve to an IRI in the chosen ontology (e.g. running `--ontology asmo` on a crystalline sample — see below).
- **Validation warnings**: indicate potential mistakes (e.g., specifying a!=b for cubic). These are warnings, not errors — the mapping still proceeds.
- **Unmapped fields**: input keys that the annotator doesn't recognize. These may need manual mapping.
- **Suggested properties**: additional ontology properties that would make the annotation more complete.

## Verification checklist

- [ ] Confirmed `results.validation_warnings` is empty (or every entry is explained) — a non-empty list means an emitted class/property is **not defined in the chosen ontology** and was given `confidence: 0.0`; do not report such terms as valid annotations.
- [ ] Recorded the `match_type` and `confidence` for each concept match and confirmed the chosen term is acceptable for its tier (1.0 exact, 0.9 synonym, 0.7 substring, 0.5 description); for any `substring_*` or `description_class` match, verified the matched class is actually the intended concept and not an incidental string hit.
- [ ] For crystal mappings, recorded `results.effective_system` and `results.bravais_lattice` (the resolved Pearson symbol, e.g. `cF`/`cI`), and confirmed the input Bravais/space-group/system are mutually consistent (no "space group N implies X but Y was specified" warning in `validation_warnings`).
- [ ] Checked lattice-parameter constraints against `effective_system` — confirmed no warnings such as "Cubic requires a=b" / angle-90 violations, or explicitly justified each one (warnings are advisory, the mapping still proceeds).
- [ ] Listed `results.unmatched` (concept) and `results.unmapped_fields` (sample) and confirmed nothing materially important was silently dropped; ran the emitted `class_browser.py` suggestion for any unmatched term that should have resolved.
- [ ] Reviewed `results.suggested_properties` and recorded which missing fields (elements, space_group, lattice_a, ...) are intentionally omitted vs. should be added before the annotation is considered complete.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "The script printed annotations, so the sample is correctly annotated." | Emission is not validation. `sample_annotator.py` will emit a term and then flag it with `validation_warning` / `confidence: 0.0` if it is not in the ontology — always read `results.validation_warnings` before trusting the output. |
| "I'll annotate this crystalline sample with `--ontology asmo`." | ASMO is a simulation-methods ontology with **no crystal/sample vocabulary**; every crystal term comes back at `confidence: 0.0`. Use CMSO for crystal/sample annotation; use ASMO only via the concept-mapping path. |
| "It matched the term, so the mapping is high-confidence." | A match can be a 0.7 substring or 0.5 description hit (e.g. an incidental substring inside an unrelated label). Check `confidence`/`match_type`; treat anything below an exact/synonym match as a candidate to verify, not a fact. |
| "`space group` matched a class label, so that's a 1.0 exact match." | The per-ontology synonym table is consulted **before** exact-label matching, so synonym-key terms (`space group`, `unit cell`, `atom`) report as 0.9 synonym matches even when they equal a class label. The matched class/IRI is still correct — do not "correct" the confidence. |
| "The space group is valid (1–230), so my crystal system is fine." | A valid space group can still contradict an explicitly given `--system` or Bravais lattice. Read `effective_system` and check for a "space group N implies X but Y was specified" entry in `validation_warnings`. |
| "My sample has a `structure` field, so the Bravais lattice resolved." | In the sample path `strict_bravais=False`: free-text structures (e.g. `rocksalt`, `perovskite`) are passed through unmapped with a warning, leaving `bravais_lattice` null. Verify `results.bravais_lattice` is the expected Pearson symbol, or supply FCC/BCC/HCP/a Pearson code. |

## Security

### Input Validation
- `--ontology` is validated against registered ontology names in `ontology_registry.json` (fixed allowlist)
- `--term` and `--terms` are length-limited and used only for substring matching against pre-processed synonym tables (never interpolated into code)
- `--bravais` is validated against a fixed set of recognized lattice type symbols
- `--space-group` is validated as an integer between 1 and 230
- Lattice parameters (`--a`, `--b`, `--c`, `--alpha`, `--beta`, `--gamma`) are validated as finite positive numbers
- `--sample` JSON is parsed with `json.loads()` and validated as a non-empty dict; keys and values are type-checked

### File Access
- Scripts read pre-processed JSON files from the `references/` directory: `ontology_registry.json`, `*_mappings.json`, `*_summary.json`, `crystal_systems.json`, `element_data.json` (all read-only)
- No scripts write to the filesystem; all output goes to stdout
- No network access is required

### Tool Restrictions
- **Read**: Used to inspect script source, reference files, and ontology data
- **Grep**: Used to search reference files for mapping patterns or ontology terms
- **Glob**: Used to locate reference files and ontology data
- Notably, this skill has **no Bash or Write access**, giving it the lowest attack surface of all skills

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- No subprocess calls of any kind; all logic runs within Python scripts invoked by the agent
- No file writes; the skill is purely read-only and analytical
- Minimal tool surface (Read, Grep, Glob only) means the agent cannot execute arbitrary commands or modify the filesystem

## Limitations

- Concept mapping uses string matching and a per-ontology synonym table; it does not understand arbitrary natural language
- Crystal system validation checks basic constraints only (not all crystallographic rules)
- The element resolver recognizes common element names and symbols but may miss unusual spellings
- Bravais lattice aliases cover common usage (FCC, BCC, HCP) but not all crystallographic notation variants

## References

- [Mapping Patterns](references/mapping_patterns.md) — common mapping examples
- [Crystal Systems](references/crystal_systems.json) — crystal system definitions and Bravais lattices
- [Element Data](references/element_data.json) — periodic table data
- [CMSO Mappings](references/cmso_mappings.json) — CMSO-specific synonym tables and annotation config
- [CMSO Guide](../ontology-explorer/references/cmso_guide.md) — CMSO ontology overview
- [Ontology Explorer](../ontology-explorer/) — sibling skill; `scripts/class_browser.py --ontology <name> --search <term>` browses classes when a concept is unmatched

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-06-23 | 1.2 | Validate emitted terms against the loaded ontology (ASMO crystal/sample terms now flagged, not silently emitted); document ASMO is concept-mapping only; clarify synonym-vs-exact confidence precedence; self-contained class_browser suggestion; harden input validation (term/sample size caps, Bravais allowlist) |
| 2026-02-25 | 1.1 | Refactored for multi-ontology support: externalized CMSO-specific knowledge to config |
| 2026-02-25 | 1.0 | Initial release with CMSO mapping support |
