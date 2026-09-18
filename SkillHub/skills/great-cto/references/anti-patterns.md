---
name: anti-patterns
description: Catalog of recurring failure modes across architectures: god-objects, hidden coupling, premature abstraction, distributed monolith, eager caching, sync-over-async
when_to_use: Pattern lookup at architecture time (architect Step 0) and during code review
applies_to:
  - _default
---

# Anti-patterns — reference

Negative rules are sharper than positive guidance. This file is the curated blocklist of
shapes engineering artefacts take when they're theatrical rather than useful. Each entry
has a **tell** (grep-able string or structural signal) so `/audit` and gate-owning agents
can detect and flag them mechanically, not argue aesthetics.

Inspired by the anti-cliché blocklist pattern (ConardLi/web-design-skill). Applied here
to architecture docs, threat models, SBOMs, postmortems, and gate verdicts.

**How to use.** Agents that produce artefacts (`architect`, `security-officer`,
`qa-engineer`, `l3-support`) read this file before drafting. Agents that consume gates
(CTO via `/inbox`) can request `/audit lint` to scan all current artefacts against it.

---

## ARCH documents (`docs/architecture/ARCH-*.md`)

| # | NEVER | Tell | Do instead |
|---|---|---|---|
| A1 | Ship ARCH without explicit **Non-goals** | no `## Non-goals` or `## Out of scope` section | Name 3 things the feature deliberately won't do |
| A2 | Marketing adjectives in service descriptions | `scalable\|reliable\|performant\|robust\|cutting-edge\|best-in-class` | Specific SLO / throughput number |
| A3 | Unnamed infrastructure | `a database\|a queue\|a cache\|some storage` (without vendor) | Exact product + version (e.g. "Postgres 16", "Redis 7") |
| A4 | "We'll add monitoring/logging/tracing later" | `later\|future\|phase 2.*monitor\|TODO.*observab` | Observability listed in the build plan, not deferred |
| A5 | Copy-paste microservices diagram with no contract | has diagram but no `## Contracts` or `## API` section | Request/response schema per service-to-service edge |
| A6 | Greenfield rewrite without migration path | `rewrite\|replace` + no `## Migration` section | Parallel-run plan or decommission date for old system |
| A7 | Stack justified by resume-driven development | `Kafka\|Kubernetes\|microservices` + team-size < 5 | ADR with archetype match + 2 rejected alternatives |
| A8 | `## Security` section is one line | Security header followed by < 3 lines | STRIDE summary or pointer to `TM-<slug>.md` |

---

## Threat models (`docs/threat-models/TM-*.md`)

| # | NEVER | Tell | Do instead |
|---|---|---|---|
| T1 | Mitigation = "input validation" / "sanitisation" alone | mitigation column contains only `validation\|sanitis` | Name the library + the specific check (e.g. "zod schema at controller boundary") |
| T2 | STRIDE category left blank or "N/A" without reason | `Spoofing.*N/A\|Tampering.*N/A` without rationale | Either a threat entry or explicit "no surface for this" + why |
| T3 | Accepted risks without **owner** + **expiry** | `## Accepted risks` section missing owner or expiry column | Named owner + review date ≤ 90 days |
| T4 | No dataflow diagram | no Mermaid / no `flowchart\|graph` block | Mermaid flowchart with trust boundaries as dashed lines |
| T5 | Threats lifted from template unchanged | exact string match against TM template boilerplate | Drop the row or rewrite with feature-specific detail |
| T6 | Critical threat without mitigation mapping | row marked `Critical\|High` with empty mitigation | Every Critical / High maps to a concrete control |

---

## SBOM (`docs/releases/SBOM-*.json`)

| # | NEVER | Tell | Do instead |
|---|---|---|---|
| S1 | 1-component SBOM (tool didn't actually run) | `components` array length < 5 | Re-run with `/sec sbom` — genuine manifest has dozens |
| S2 | Missing integrity hashes | no `hashes` field on components | Use native tool output (npm sbom, cyclonedx-py) which includes hashes |
| S3 | Version ranges instead of pins | version field contains `^\|~\|>=\|*` | Exact versions; ranges belong in manifest, not SBOM snapshot |
| S4 | No SBOM link in RELEASE doc | RELEASE-*.md without `SBOM-*.json` reference | Cross-ref in RELEASE under `## Artefacts` |

---

## Postmortems (`docs/postmortems/PM-*.md` and `PM-SEC-*.md`)

| # | NEVER | Tell | Do instead |
|---|---|---|---|
| P1 | Root cause = "human error" | `root cause.*human error\|operator mistake` | Keep asking "why" — humans make errors because of system design |
| P2 | Action items without **owner** + **date** | AI rows without `@\|owner:` or missing date | Assign a name and a deadline to every action |
| P3 | Same lesson as a prior PM (not learning) | `What slowed down:` text matches a prior PM verbatim | Escalate to recurring-pattern review; propose systemic fix |
| P4 | Timeline missing detection lag | no `T+` minutes from first-signal to first-human | Compute MTTD explicitly |
| P5 | "5 whys" skipped | no nested why chain | At least 3 levels; stop only when root is a system property |
| P6 | PM-SEC missing notification log | PM-SEC-*.md without `## Notification log` | Log every external comm with T+, recipient, channel, status |

---

## Gate verdicts (agent sign-offs in `.great_cto/verdicts/*.log`)

| # | NEVER | Tell | Do instead |
|---|---|---|---|
| G1 | PASS verdict with zero evidence | verdict line has no artefact path / no finding count | Link the QA report / CSO report or state "N/A because X" |
| G2 | "No issues found" on a non-trivial change | diff > 100 LOC, verdict = `PASS.*no issues` | At minimum: one risk noted, even if accepted |
| G3 | Verdict timestamps cluster (batch rubber-stamp) | 3+ verdicts within 60 seconds from same agent | Genuine review takes longer; flag via `/inbox` drift signal |
| G4 | Gate closed by author (self-approval) | verdict emitter == artefact author in git log | Another agent / human must close the gate |

---

## Cross-doc link rot (`docs/**/*.md`)

Docs reference each other: ARCH → ADR, PM → ARCH, TM → ARCH, RELEASE → SBOM. Links rot
silently when files are renamed or deleted. Inspired by the ghost-link lint pattern
(cablate/llm-atomic-wiki).

| # | NEVER | Tell | Do instead |
|---|---|---|---|
| L1 | Relative markdown link to a non-existent file | markdown link syntax pointing to a missing `.md` file | Fix path or remove the reference |
| L2 | Inline artefact reference without matching file | bare `ARCH-<slug>.md` / `PM-<date>.md` / `ADR-NNNN.md` / `RFC-NNNN.md` / `TM-<slug>.md` / `SBOM-<ver>.json` mentioned in prose but file absent | Rename the live artefact or remove the stale ref |
| L3 | Orphan ADR / RFC (no incoming links) | `docs/adr/ADR-*.md` or `docs/rfcs/RFC-*.md` with zero references from any other doc | Link from relevant ARCH / decision log, or archive |
| L4 | Expired temporal markers | `current version\|latest release\|TBD\|to be determined` in doc older than 90 days | Replace with concrete version/date or remove the section |

---

## How `/audit lint` uses this

`/audit` with `lint` flag (or the implicit lint pass in full audit) scans:

- `docs/architecture/ARCH-*.md` against A1–A8
- `docs/threat-models/TM-*.md` against T1–T6
- `docs/releases/SBOM-*.json` against S1–S4
- `docs/postmortems/PM-*.md` and `PM-SEC-*.md` against P1–P6
- `.great_cto/verdicts/*.log` against G1–G4
- all `docs/**/*.md` against L1–L4 (cross-doc link rot)

Matches become findings in the AUDIT report under `## Anti-pattern findings`, with the
rule ID (e.g. `A3`), file path, line number, and quoted offending substring. Severity is
advisory — anti-patterns don't block gates, they get flagged for author awareness.

**False-positive handling.** If a pattern is intentional (e.g. `a queue` is literally
the product name), add a waiver line: `<!-- anti-pattern-waiver: A3 reason:<why> -->`
on the offending line. Lint respects waivers.

---

## What this is **not**

- Not a style guide — no opinions on prose quality
- Not a linter for code — strictly artefact-level
- Not exhaustive — add rules when a cliché recurs across ≥ 3 projects
- Not a blocker — findings are advisory, not gate-denying

New rules land here only when they're **detectable** (grep-able tell) and **common**
(seen in multiple real projects). Otherwise they belong in the relevant agent prompt
as guidance, not in this blocklist.
