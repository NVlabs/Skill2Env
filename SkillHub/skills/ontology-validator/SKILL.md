---
name: ontology-validator
description: >
  Validate material sample annotations against ontology constraints — check
  that class names and property names exist in the ontology, verify domain
  and range consistency for object property relationships, assess annotation
  completeness (required, recommended, and optional properties), and flag
  unknown or misspelled terms. Use when verifying that CMSO or other
  ontology annotations are correct before publishing, checking whether all
  required properties are present for a class like Crystal Structure or
  Unit Cell, auditing relationship triples between instances, or catching
  annotation errors early in a FAIR data workflow, even if the user only
  says "is my annotation correct" or "what am I missing."
allowed-tools: Read, Bash
metadata:
  author: HeshamFS
  version: "1.2.2"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 5
  last_reviewed: "2026-06-23"
  standards:
    - "CMSO — Computational Material Sample Ontology v0.0.1 (OCDO, purls.helmholtz-metadaten.de/cmso/)"
    - "ASMO — Atomistic Simulation Methods Ontology (OCDO)"
    - "W3C OWL 2 / RDFS domain, range, and rdfs:subClassOf semantics"
    - "FAIR Guiding Principles (Wilkinson et al. 2016)"
---

# Ontology Validator

## Goal

Validate that material sample annotations comply with ontology constraints: correct class names, valid properties, consistent domain/range relationships, and required fields present.

## Requirements

- Python 3.10+
- No external dependencies (Python standard library only)
- Requires ontology-explorer's `cmso_summary.json` and `ontology_registry.json`

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Annotation | JSON dict or list of annotation dicts | `{"class":"UnitCell","properties":{"has Bravais lattice":"cF"}}` |
| Class name | Class to check completeness for | `Crystal Structure` |
| Provided properties | Comma-separated property names | `"has unit cell,has space group"` |
| Relationships | JSON array of subject-property-object triples | `[{"subject_class":"Material","property":"has structure","object_class":"Crystal Structure"}]` |

## Decision Guidance

```
What do you need to validate?
├── An annotation (classes and properties are correct)
│   └── schema_checker.py --ontology cmso --annotation '<json>'
├── Completeness of a class annotation
│   └── completeness_checker.py --ontology cmso --class <name> --provided <props>
└── Object property relationships
    └── relationship_checker.py --ontology cmso --relationships '<json>'
```

## Script Outputs (JSON Fields)

| Script | Key Outputs |
|--------|-------------|
| `scripts/schema_checker.py` | `results.valid`, `results.errors` (each unknown_class/unknown_property error carries a `suggestions` array of nearest matches), `results.warnings`, `results.class_valid`, `results.properties_valid` |
| `scripts/completeness_checker.py` | `results.completeness_score`, `results.required_missing`, `results.recommended_missing`, `results.optional_missing`, `results.unrecognized` |
| `scripts/relationship_checker.py` | `results.valid`, `results.results`, `results.errors` |

## Workflow

1. After mapping a sample with ontology-mapper, pass the annotations to `schema_checker.py` to verify correctness.
2. For a specific class, use `completeness_checker.py` to see what required/recommended properties are missing.
3. When building relationships between instances, use `relationship_checker.py` to ensure domain/range consistency.

## Conversational Workflow Example

```
User: I annotated my sample as CrystalStructure with properties hasUnitCell and hasBasis.
      Is this correct and complete?

Agent: Let me both validate the annotation and check its completeness.

[Runs: schema_checker.py --ontology cmso --annotation
       '{"class":"Crystal Structure","properties":{"has unit cell":true,"has basis":true}}' --json]
[Runs: completeness_checker.py --ontology cmso --class "Crystal Structure"
       --provided "has unit cell,has basis" --json]

From schema_checker.py (results.warnings):
- has unit cell: valid for Crystal Structure
- has basis: domain_mismatch warning — its domain is "Unit Cell", not
  Crystal Structure (so this property belongs on the Unit Cell instance)

From completeness_checker.py (results, completeness_score = 0.5):
- **required_missing**: has space group

So: add "has space group" to the Crystal Structure annotation, and move
"has basis" onto the Unit Cell annotation. (The domain insight comes from
schema_checker.py's warnings; completeness_checker.py only reports the
missing required "has space group".)
```

## CLI Examples

```bash
# Validate an annotation
python3 skills/ontology/ontology-validator/scripts/schema_checker.py \
  --ontology cmso \
  --annotation '{"class":"Unit Cell","properties":{"has Bravais lattice":"cF"}}' \
  --json

# Check completeness
python3 skills/ontology/ontology-validator/scripts/completeness_checker.py \
  --ontology cmso \
  --class "Crystal Structure" \
  --provided "has unit cell,has space group" \
  --json

# Validate relationships
python3 skills/ontology/ontology-validator/scripts/relationship_checker.py \
  --ontology cmso \
  --relationships '[{"subject_class":"Computational Sample","property":"has material","object_class":"Material"}]' \
  --json
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Class 'X' not found ... (did you mean 'Y'?)` | Invalid/misspelled class name | Apply the nearest-match `suggestions` from the error, or use ontology-explorer to find the correct name |
| `Property 'X' not found ... (did you mean 'Y'?)` | Invalid/misspelled property name | Apply the nearest-match `suggestions` from the error, or use property_lookup.py to search |
| `Annotation must be a dict` | Wrong input format | Provide valid JSON dict |
| `Relationships must be a non-empty list` | Wrong input format | Provide JSON array of relationship dicts |

## Interpretation Guidance

- **Errors** indicate definite problems (unknown class/property, range mismatch)
- **Warnings** indicate potential issues (domain mismatch — may be intentional for subclasses)
- **Completeness score**: 0.0-1.0 ratio of provided vs. total tracked
  properties. It weights required, recommended, and optional properties
  **equally**, so a moderate score (e.g. 0.5-0.67) can coexist with missing
  required properties. ALWAYS check `required_missing` first: a non-empty
  `required_missing` means the annotation is invalid regardless of the score.
- **required_missing**: must fix for valid annotation
- **recommended_missing**: should fix for quality
- **unrecognized**: may indicate typos or properties from a different ontology

## Verification checklist

- [ ] Ran `schema_checker.py --json` and recorded `results.valid`; confirmed `results.errors` is an empty array (a `valid:true` with any `unknown_class`/`unknown_property` error cannot occur, but confirm the array length is 0 rather than trusting the boolean alone).
- [ ] For every `domain_mismatch` entry in `results.warnings`, recorded the property, its reported `domain`, and the class it was applied to, then made an explicit keep-or-move decision (warnings are not auto-fixed and may be intentional for a subclass).
- [ ] Ran `completeness_checker.py --json` and confirmed `results.required_missing` is empty BEFORE quoting `completeness_score` — a non-empty `required_missing` means the annotation is invalid no matter how high the score is.
- [ ] Recorded the exact `completeness_score` together with the `required_missing`, `recommended_missing`, and `optional_missing` lists (do not paraphrase the score as "complete" while any required item is missing).
- [ ] For each unknown class/property error, recorded the `suggestions[0]` value and confirmed the corrected name actually exists in the ontology (re-ran the checker, or checked via ontology-explorer) rather than assuming the top suggestion is right.
- [ ] Ran `relationship_checker.py --json` for every subject-property-object triple and confirmed each per-triple `results.results[i].valid` is true; recorded any `results.errors` strings naming the offending `domain` or `range`.
- [ ] Confirmed the `--ontology` used (e.g. `cmso`, `asmo`) matches the ontology the annotation was authored against — a class can be "unknown" simply because the wrong constraints/summary file was loaded.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|------------------------------|
| "completeness_score is 0.67, so the annotation is basically complete." | The score weights required, recommended, and optional tiers **equally**, so a high score can still hide a missing required property. Check `required_missing` first; a non-empty list means invalid regardless of score. |
| "schema_checker returned only warnings, no errors, so I'll ignore them." | `domain_mismatch` warnings flag a property attached to a class that is not (a subclass of) its domain — often the property belongs on a different instance. Record each warning and decide explicitly; don't auto-dismiss. |
| "The class name didn't match but the validator gave a suggestion, so I'll just use it." | `suggestions` come from stdlib `difflib` fuzzy matching (cutoff 0.6) and can be wrong or empty. Verify the suggested name exists in the ontology before applying it. |
| "Two of the three relationships passed, so the triples are fine." | `results.valid` is the AND over all triples; you must inspect each `results.results[i]` and its `errors`. A single failing domain/range check invalidates the relationship set. |
| "It returned valid:true, so the annotation is semantically correct." | The checker only verifies class/property existence and domain/range against a **manually curated** constraints file. It does not check data types, cardinality, or value plausibility — `valid:true` is necessary, not sufficient. |
| "Property exists in the ontology, so it applies to my class." | Existence is checked against the full property set; domain applicability is a separate subclass-aware check. A real property can still trigger a `domain_mismatch` warning on the wrong class. |
| "I'll trust the bare class name; substrings are close enough." | Domain/subclass matching is exact-equality plus parent traversal, NOT substring containment. `Material` is not credited with `Crystalline Material` properties; use the precise ontology class name. |

## Security

### Input Validation
- `--ontology` is validated against registered ontology names in `ontology_registry.json` (fixed allowlist)
- `--annotation` JSON is parsed with `json.loads()` and validated as a dict with required `class` and `properties` keys
- `--class` names are validated against known classes in the ontology summary; unknown classes produce clear errors
- `--provided` property names are validated as comma-separated strings and matched against known properties
- `--relationships` JSON is parsed and validated as a non-empty list of dicts, each requiring `subject_class`, `property`, and `object_class` keys
- Size/length caps reject abusive input (exit code 2): raw JSON inputs and annotation files are capped at 1,000,000 bytes; at most 1000 annotations/relationships/provided properties per call; each class or property name is capped at 500 characters. Class and property names must be strings.

### File Access
- Scripts read pre-processed JSON files from the `references/` directory: `ontology_registry.json`, `cmso_summary.json`, `cmso_constraints.json` (all read-only)
- No scripts write to the filesystem; all output goes to stdout
- No network access is required

### Tool Restrictions
- **Read**: Used to inspect script source, reference files, and ontology constraint data
- **Bash**: Used to execute the three Python validation scripts (`schema_checker.py`, `completeness_checker.py`, `relationship_checker.py`) with explicit argument lists

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- JSON input parsing uses `json.loads()` only (no pickle, no YAML with unsafe loaders)
- Validation logic operates on pre-loaded in-memory data structures; no dynamic file discovery or traversal

## Limitations

- Constraints file is manually curated, not derived from OWL axioms
- Does not validate data types (e.g., whether a value is actually a float vs string)
- Does not validate cardinality (e.g., exactly one space group per structure)
- Subclass checking uses simple parent traversal, not full OWL reasoning

## References

- [Validation Rules](references/validation_rules.md) — what is validated and why
- [CMSO Constraints](references/cmso_constraints.json) — required/recommended properties per class
- [CMSO Guide](../ontology-explorer/references/cmso_guide.md) — CMSO ontology overview

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-06-23 | 1.2.0 | Subclass-aware domain matching (fixes substring false positives/negatives), nearest-match suggestions on unknown class/property, input size/length caps, eval and doc corrections |
| 2026-02-25 | 1.0 | Initial release with CMSO validation support |
