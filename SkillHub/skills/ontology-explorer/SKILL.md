---
name: ontology-explorer
description: >
  Parse, navigate, and query materials science ontology structures — browse
  class hierarchies, inspect individual classes and their properties, look up
  object and data property definitions with domain/range, search for ontology
  terms by keyword, and parse or summarize raw OWL/XML files. Currently supports
  CMSO and ASMO; the broader OCDO ecosystem (CDCO, PODO, PLDO, LDO) is planned.
  Use when exploring
  what classes or properties an ontology provides, finding the right CMSO
  term for a crystal structure or simulation concept, understanding
  parent-child class relationships, or onboarding to an unfamiliar materials
  ontology, even if the user only says "what ontology terms describe my
  FCC copper simulation" or "show me the CMSO class hierarchy."
allowed-tools: Read, Bash
metadata:
  author: HeshamFS
  version: "1.2.2"
  standards:
    - "W3C OWL 2 Web Ontology Language; RDF Schema (RDFS) and XSD datatypes"
    - "W3C SKOS Simple Knowledge Organization System (skos:definition / preferred labels)"
    - "OCDO ontologies: CMSO and ASMO (plus CDCO/PODO/PLDO/LDO ecosystem), Helmholtz Metadata Collaboration PURL IRIs"
    - "QUDT (Quantities, Units, Dimensions and Types) vocabulary for physical units (ASMO has unit)"
    - "International Tables for Crystallography: space group numbers 1-230 (Hermann-Mauguin symbols) and the 14 Bravais lattices"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 5
  last_reviewed: "2026-06-23"
---

# Ontology Explorer

## Goal

Enable an agent to understand, navigate, and query the structure of materials science ontologies without loading verbose OWL/XML files directly. Provides fast access to class hierarchies, property definitions, and domain-range relationships through pre-processed JSON summaries.

## Requirements

- Python 3.10+
- No external dependencies (Python standard library only)
- Internet access required only for `owl_parser.py` and `ontology_summarizer.py` when fetching remote OWL files

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Ontology name | Registered ontology to query | `cmso` |
| Class name | A specific class to inspect | `Material`, `UnitCell` |
| Property name | A specific property to look up | `hasMaterial`, `hasSpaceGroupNumber` |
| Search term | Keyword to search across labels | `crystal`, `lattice` |
| OWL source | Path or URL to an OWL/XML file (for parsing/summarizing) | `https://raw.githubusercontent.com/OCDO/cmso/main/cmso.owl` |

## Decision Guidance

```
What do you need?
├── Understand overall ontology structure
│   └── class_browser.py --ontology cmso --list-roots
├── Inspect a specific class
│   └── class_browser.py --ontology cmso --class <name>
├── Find properties for a class
│   └── property_lookup.py --ontology cmso --class <name>
├── Look up a specific property
│   └── property_lookup.py --ontology cmso --property <name>
├── Search for a concept
│   ├── class_browser.py --ontology cmso --search <term>
│   └── property_lookup.py --ontology cmso --search <term>
├── Parse a new/updated OWL file
│   └── owl_parser.py --source <path-or-url>
└── Generate/refresh a summary JSON
    └── ontology_summarizer.py --source <url> --output <path>
```

## Script Outputs (JSON Fields)

| Script | Key Outputs |
|--------|-------------|
| `scripts/owl_parser.py` | `results.metadata`, `results.classes`, `results.object_properties`, `results.data_properties`, `results.class_hierarchy` |
| `scripts/ontology_summarizer.py` | `results.output_file`, `results.statistics` |
| `scripts/class_browser.py` | `results.class_info`, `results.subtree`, `results.properties`, `results.path_to_root`, `results.roots`, `results.search_results` |
| `scripts/property_lookup.py` | `results.property_info`, `results.class_properties`, `results.search_results` |

## Workflow

1. Identify which ontology the user is working with (default: CMSO).
2. Use `class_browser.py --list-roots` to see the top-level concepts.
3. Drill into specific classes with `class_browser.py --class <name>` to see hierarchy, children, and applicable properties.
4. Look up individual properties with `property_lookup.py --property <name>`.
5. If the user mentions a concept but not its ontology name, use `--search` to find matching classes or properties.
6. For a new or updated ontology, run `owl_parser.py` to parse the raw OWL, then `ontology_summarizer.py` to generate a summary JSON.

## Conversational Workflow Example

```
User: I have an FCC copper simulation. What CMSO classes should I use to describe it?

Agent: Let me explore the CMSO ontology to find the relevant classes. I'll run
a few targeted searches and property lookups (the answer below is synthesized
from several commands, per the Workflow section).

[Runs: class_browser.py --ontology cmso --search "crystal" --json]
  → Crystalline Material, Crystal Structure (among others)
[Runs: class_browser.py --ontology cmso --search "sample" --json]
  → Computational Sample, Atomic Scale Sample
[Runs: class_browser.py --ontology cmso --search "unit cell" --json]
  → Unit Cell
[Runs: class_browser.py --ontology cmso --search "space group" --json]
  → Space Group
[Runs: class_browser.py --ontology cmso --search "element" --json]
  → Chemical Element
[Runs: property_lookup.py --ontology cmso --property "has material" --json]
  → domain Computational Sample → range Material
[Runs: property_lookup.py --ontology cmso --property "has structure" --json]
  → domain Material → range Structure
[Runs: property_lookup.py --ontology cmso --property "has unit cell" --json]
  → domain Crystal Structure → range Unit Cell

For an FCC copper simulation, the relevant CMSO classes are:

- **Computational Sample** → **Atomic Scale Sample**: your simulation is an atomic-scale sample
- **Material** → **Crystalline Material**: copper is crystalline
- **Crystal Structure**: describes the FCC arrangement
- **Unit Cell**: the repeating FCC unit cell (a=b=c=3.615 Å, α=β=γ=90°)
- **Space Group**: FCC copper is space group 225 (Fm-3m)
- **Chemical Element**: Cu

The key relationship chain (from the property domains/ranges above):
  Computational Sample → has material → Material → has structure → Structure
  → (Crystal Structure) → has unit cell → Unit Cell

Shall I look up the specific properties for any of these classes?
```

## CLI Examples

```bash
# List root classes in CMSO
python3 skills/ontology/ontology-explorer/scripts/class_browser.py \
  --ontology cmso --list-roots --json

# Inspect the Material class hierarchy
python3 skills/ontology/ontology-explorer/scripts/class_browser.py \
  --ontology cmso --class Material --json

# Search for crystal-related classes
python3 skills/ontology/ontology-explorer/scripts/class_browser.py \
  --ontology cmso --search crystal --json

# Find all properties for UnitCell
python3 skills/ontology/ontology-explorer/scripts/property_lookup.py \
  --ontology cmso --class UnitCell --json

# Look up a specific property
python3 skills/ontology/ontology-explorer/scripts/property_lookup.py \
  --ontology cmso --property "has space group" --json

# Parse a remote OWL file
python3 skills/ontology/ontology-explorer/scripts/owl_parser.py \
  --source https://raw.githubusercontent.com/OCDO/cmso/main/cmso.owl --json

# Generate a summary JSON from an OWL file
python3 skills/ontology/ontology-explorer/scripts/ontology_summarizer.py \
  --source https://raw.githubusercontent.com/OCDO/cmso/main/cmso.owl \
  --output summary.json --json
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Ontology 'X' not in registry` | Ontology name not registered | Check `references/ontology_registry.json` for available names |
| `Class 'X' not found` | Class label doesn't match any entry | Use `--search` to find similar names, or `--list-roots` to see available classes |
| `Property 'X' not found` | Property label doesn't match | Use `--search` to find similar properties |
| `Cannot parse OWL source` | Invalid XML or unreachable URL | Check file path or URL; ensure the file is valid OWL/XML |
| `Summary file not found` | Summary JSON hasn't been generated | Run `ontology_summarizer.py` first |

## Interpretation Guidance

- **Class hierarchy**: root classes are the broadest concepts; leaf classes are the most specific. A class inherits all properties from its ancestors.
- **Object properties**: show how classes relate to each other (domain → range). A property with domain `UnitCell` and range `Basis` means a unit cell *has a* basis.
- **Data properties**: show what literal values a class carries. A property with domain `ChemicalElement` and range `xsd:string` means an element has a string-valued attribute.
- **Union domains**: a property can apply to more than one class. When it does, the domain is shown as the classes joined with a pipe, e.g. `A | B`. (The bundled CMSO/ASMO summaries currently contain no union-domain properties.)
- **Search relevance**: 1.0 = label match, 0.5 = description match only.

## Verification checklist

Before presenting any class, property, or relationship as fact, confirm and record:

- [ ] Resolved the target via `class_browser.py --class <name>` (or `property_lookup.py`) and recorded the exact canonical `label` returned in `results.class_info.label` / `results.property_info.name` — do not quote a name the agent typed; quote the label the tool resolved (e.g. `UnitCell` → `Unit Cell`).
- [ ] For every relationship chain stated, cited the actual `domain` and `range` from a `property_lookup.py --property <name>` call (recorded `results.property_info.domain` and `.range`), rather than inferring the link from class names.
- [ ] When a property's `domain` contains a pipe (`A | B`), reported it as a union (applies to each listed class) and confirmed the class in question matches one normalized member — did not silently assume single-class domain.
- [ ] For `--search` results, recorded each match's `relevance` and stated whether it was a label match (1.0) or description-only match (0.5); did not present a 0.5 description hit as a confirmed term match.
- [ ] Identified the ontology by its registry key (`cmso` or `asmo`) and confirmed it exists in `references/ontology_registry.json`; did not query an unregistered ontology or conflate CMSO and ASMO terms.
- [ ] When relying on a generated/refreshed summary, recorded its `metadata.source_url` and `metadata.generated_at` and the `statistics` (`num_classes`, `num_object_properties`, `num_data_properties`) so the result is traceable to a specific OWL source.
- [ ] Treated absent parents, descriptions, or domain/range as missing data (not as "no such relationship"), since the parser extracts only simple `rdfs:subClassOf` and declared domains/ranges and does no reasoning.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "The class name `UnitCell` returned nothing, so the term doesn't exist." | Labels carry spaces (`Unit Cell`). The tools resolve exact → case-insensitive → space-normalized; if a direct guess fails, run `--search` and use the canonical `label` the tool returns, not the typed string. |
| "These two classes are obviously related, so I'll state the link." | Relationships exist only where an object property declares them. Verify with `property_lookup.py --property <name>` and quote the recorded `domain → range`; never infer a triple from class names alone. |
| "The script ran and printed results, so the answer is complete." | Run success ≠ completeness. A missing `parent`, `description`, or `domain/range` means the OWL lacked that annotation — the parser does no inference and ignores complex OWL restrictions. State what is absent. |
| "`--search crystal` matched it, so it's the right term." | A match may be relevance 0.5 (description-only), not a label match. Check the `relevance` field and prefer 1.0 label matches; report 0.5 hits as "mentioned in the description," not as the canonical term. |
| "A property has one domain class." | Domains can be unions (`A | B`). Split on `|` and check each normalized member; a property may legitimately apply to several classes. The bundled CMSO/ASMO summaries currently have none, but parsed/refreshed ones can. |
| "Any OCDO ontology will work / CMSO and ASMO are interchangeable." | Only `cmso` and `asmo` are registered; CDCO/PODO/PLDO/LDO are planned, not available. Pick the correct registry key and don't mix terms across ontologies. |
| "I'll point the parser at this `http://` OWL URL." | `owl_parser.py`/`ontology_summarizer.py` reject non-`https://` URLs by design. Use an `https://` source or a local file path. |

## Security

### Input Validation
- `--ontology` is validated against registered ontology names in `ontology_registry.json` (fixed allowlist)
- `--class` and `--property` names are validated against a safe-character pattern to prevent injection
- `--search` terms are length-limited and used only for substring matching against pre-processed labels (never interpolated into queries or code)
- `--source` for `owl_parser.py` accepts file paths or URLs; URLs are validated against `https://` scheme only

### File Access
- `class_browser.py` and `property_lookup.py` read pre-processed JSON summary files from the `references/` directory (read-only)
- `owl_parser.py` reads a single OWL/XML file from a local path or HTTPS URL; remote fetches have a 30-second timeout
- `ontology_summarizer.py` writes a single JSON summary file to the path specified by `--output`
- No scripts modify or delete existing files

### Tool Restrictions
- **Read**: Used to inspect script source, reference files, and ontology summaries
- **Bash**: Used to execute the four Python scripts (`owl_parser.py`, `ontology_summarizer.py`, `class_browser.py`, `property_lookup.py`) with explicit argument lists; URL fetching is contained within the Python scripts with timeout limits

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- OWL/XML parsing uses Python's `xml.etree.ElementTree` which does not resolve external entities by default, mitigating XXE attacks
- Remote URL fetching is limited to HTTPS with a 30-second timeout to prevent abuse
- Search results are capped in count to prevent output flooding

## Limitations

- Only supports OWL/XML format (not Turtle, JSON-LD, or N-Triples)
- Does not support OWL reasoning or inference (e.g., does not compute transitive closures)
- Class hierarchy extraction handles simple `rdfs:subClassOf` only (not complex OWL restrictions)
- Descriptions may be missing for classes that lack `rdfs:comment`, `skos:definition`, or IAO annotations
- URL fetching requires internet access and may time out (30-second limit)

## References

- [OWL/RDF Primer](references/owl_primer.md) — brief introduction to OWL concepts
- [CMSO Guide](references/cmso_guide.md) — narrative guide to the CMSO ontology
- [Ontology Registry](references/ontology_registry.json) — registered ontologies and their metadata
- [CMSO Summary](references/cmso_summary.json) — pre-processed CMSO structure
- [CMSO Documentation](https://ocdo.github.io/cmso/) — official CMSO docs
- [CMSO Repository](https://github.com/OCDO/cmso) — source OWL file and development

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-06-24 | 1.2.2 | Added a Verification checklist (evidence-based, tied to canonical-label resolution, recorded domain/range, union domains, search relevance, registry keys, and summary provenance) and a Common pitfalls & rationalizations table. |
| 2026-06-23 | 1.2.0 | Fixed property_lookup `--class` to resolve canonical labels (spaceless names like `UnitCell` now match), made class/property domain matching consistent across tools, enforced documented security controls (safe-character pattern, length caps, search-result caps, HTTPS-only URLs), corrected union-domain doc example and eval assertions, scoped description to CMSO/ASMO. |
| 2026-02-25 | 1.0 | Initial release with CMSO support |
