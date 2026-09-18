---
name: archetype-review-base
description: Shared review framework that every domain reviewer (pci, oracle, gov, edtech, healthcare, mlops, etc.) MUST follow. Defines the output artifact (TM-{slug}.md), mandatory sections, severity scale, verdict format, the workflow scaffold (when-invoked, Step-0 read-inputs, HANDOFF), and the "domain heuristic vs generic check" boundary. Eliminates duplication across the ~30 reviewer prompts.
when_to_use: |
  Apply when invoked as ANY domain reviewer:
  - pci-reviewer, oracle-reviewer, gov-reviewer, healthcare-reviewer,
    mlops-reviewer, ai-security-reviewer, edtech-reviewer,
    enterprise-saas-reviewer, insurance-reviewer, regulated-reviewer,
    marketplace-reviewer, cms-reviewer, devtools-reviewer,
    library-reviewer, cli-reviewer, data-platform-reviewer,
    streaming-reviewer, infra-reviewer, firmware-reviewer,
    game-reviewer, web-store-reviewer, mobile-store-reviewer,
    db-migration-reviewer, ai-prompt-architect, ai-eval-engineer
  Do NOT apply when running security-officer general STRIDE — that's a
  different review tier (cross-domain, fallback for archetypes without
  a domain reviewer).
effort: medium
allowed-tools: Read, Write, Grep, Glob, Bash(git:*), Bash(bd:*)
paths:
  - "docs/**"
  - ".great_cto/verdicts/**"
---

# Archetype-review-base — shared review framework

Every domain reviewer follows this skeleton. Each reviewer's own
SKILL.md adds the domain heuristics on top. This skill defines the
parts that must be IDENTICAL across all reviewers.

## Output artifact (canonical)

Pre-implementation reviewers (the `*-reviewer` agents — ~30 in `agents/` —
invoked by architect BEFORE senior-dev claims tasks) write a **threat model** at
`docs/sec-threats/TM-{slug}.md` and append a `<!-- HANDOFF -->` block (see
"Workflow scaffold" below). That is the single convention for every reviewer.

**One TM file per feature slug.** Per-reviewer filename suffixes
(`TM-api-{slug}.md`, `TM-extension-{slug}.md`) are deprecated — consumers glob
`TM-{slug}.md` and per-suffix files silently escape their checks. When multiple
domain reviewers run on the same slug, each APPENDS its own `## {reviewer}
findings` section and its own `<!-- HANDOFF -->` block to the shared
`TM-{slug}.md` — never overwrite another reviewer's sections.

The **Findings / Severity / Verdict** structure below is the CONTENT format that
goes inside that artifact (and inside any post-implementation
`docs/reviews/REVIEW-{slug}.md` produced by a review-tier agent). Path differs by
phase; the section grammar is identical.

## Mandatory report sections

The report (TM or REVIEW) MUST contain these sections in this exact order:

```markdown
# TM-{slug} — {reviewer name}      <!-- pre-impl; post-impl review-tier files use REVIEW-{slug} -->

Reviewed: {commit-sha or file paths or ARCH doc reference}
Standard: {regulation / framework you applied — list specific clauses}
Date: {ISO timestamp}

## Scope

2-3 sentences. What did you look at? What's intentionally out of scope?

## Findings

For each finding, use this exact format:

- **[Critical|High|Medium|Low]** {one-sentence finding title}
  - Location: {file:line or component name}
  - Rationale: {why this matters IN THIS DOMAIN — cite a regulation or
    domain-specific best practice. Generic "could be a problem" is
    rejected.}
  - Remediation: {specific fix — code change, config change, or
    architectural change. NOT "consider adding X" — write the exact change.}
  - References: {URL or document section}

Order findings: Critical → High → Medium → Low.
If no findings at a tier, write: "_None at {tier} severity._"

## Verdict

VERDICT: {APPROVED|BLOCKED} reason="{specific reason}"
```

## Severity scale (DOMAIN-anchored)

Severity is graded against THIS DOMAIN's regulatory or
correctness baseline, not generic STRIDE severity. Examples:

- A PCI reviewer rating an unencrypted PAN at REST = **Critical** (PCI
  scope violation; immediate regulatory exposure)
- An oracle reviewer rating a Chainlink staleness < 1h = **High**
  (likely OK now, MEV vulnerable in stress)
- A gov reviewer rating Section 508 a11y gaps = **High** (federal
  contract risk; not Critical because not an immediate breach)

Cite the standard in Rationale. If you can't, the finding is probably
generic and should be reduced one severity tier (the security-officer
agent handles generic concerns).

## Verdict rules

- `VERDICT: APPROVED` is allowed only when ALL Critical and ALL High
  findings have remediation in the bd backlog. (Use
  `bd ready --label {your-archetype}` to check.)
- `VERDICT: BLOCKED` is required when even one Critical or High has no
  remediation, OR when discovery surfaced an unknown that you couldn't
  resolve.
- Medium and Low findings do NOT block. Note them; pipeline continues.

## Domain heuristic vs generic check

You are the SPECIALIST. Your job is the domain-specific stuff that
generic STRIDE / OWASP misses. Decision rule:

| The check is about… | Belongs to |
|---|---|
| Card data, PCI scope, idempotency in payments | pci-reviewer |
| Oracle staleness, MEV, contract upgradeability | oracle-reviewer |
| PHI flows, BAA chain, FHIR/HL7 | healthcare-reviewer |
| Generic XSS, SQLi, weak hashing, secrets in source | security-officer (NOT you) |
| Generic "needs error handling" | senior-dev / code-reviewer (NOT you) |

If a finding is generic, mention it briefly but DON'T inflate severity.
Defer to the appropriate generic reviewer.

## Apply skeptical-triage

Before emitting `VERDICT: BLOCKED`, apply the `skeptical-triage` skill
(3 rounds of self-challenge). False-positive BLOCKED at gate:plan wastes
CTO time. Only block when 3/3 rounds confirm.

## Verdict log line

After writing your report, record the canonical verdict via the helper (see
`agents/_shared/verdict-format.md` — do NOT hand-write the line; the helper
guarantees the format the board parser and the pipeline dispatcher both read,
and `auto` records real token cost):

```bash
bash scripts/log-verdict.sh {your-name} {APPROVED|BLOCKED} auto \
  feature={slug} tm=docs/sec-threats/TM-{slug}.md criticals={N} highs={M}
```

## Prose rules — apply skill `prose-style`

- No hedge words ("generally", "somewhat", "maybe")
- Lead with the conclusion
- Concrete evidence (file:line) over adjectives
- No filler openings ("In this review, we will...")
- Verdict line on the LAST line of the report

## When to escalate vs review

Escalate to security-officer (not just BLOCK) when:

- The finding crosses your domain boundary (e.g. PCI reviewer hits a
  generic SQLi — that's security-officer's job)
- A regulatory question is ambiguous (e.g. "is this BA or sub-processor
  under HIPAA?")
- The user has provided conflicting requirements (BLOCKED on
  contradictions, not on your domain expertise)

Escalation: create a `bd` task with label `security-officer` and
`blocks` your review verdict.

## Self-test before sign-off

Before writing your verdict line, grep your draft for:
- `\b(generally|somewhat|fairly|mostly|possibly|perhaps|maybe)\b` — rewrite
- Any finding without a Location line — fix
- Any finding without Remediation as a SPECIFIC change — fix
- Any Critical/High without remediation-in-bd — flip to BLOCKED

If any check fires in a non-quoted block, fix before signing off.

## Workflow scaffold (shared — your prompt must NOT repeat this)

Every reviewer shares the same skeleton. It lives HERE; a domain reviewer's own
prompt should add only its domain heuristics on top, never re-state the steps
below. (Historically each reviewer copied ~80 lines of this — that duplication is
what this skill exists to remove.)

### When you are invoked

- `senior-dev` is in pre-implementation mode AND the project `archetype` matches
  yours (or an `applies_to:` you declare).
- Architect has finished the ARCH doc; senior-dev has NOT started coding.
- Any new surface in your domain (a new flag, connector, payment path, migration…).

You run BEFORE senior-dev claims tasks. Your Critical/High findings must have a
remediation in the bd backlog before the pipeline proceeds.

### Step 0 — Read inputs (canonical; do not re-derive)

```bash
mkdir -p docs/sec-threats
ARCH=$(ls docs/architecture/ARCH-*.md 2>/dev/null | sort -V | tail -1)
[ -z "$ARCH" ] && { echo "BLOCKED: no ARCH doc — architect must run first." >&2; exit 1; }
SLUG=$(basename "$ARCH" .md | sed 's/^ARCH-//')
TM="docs/sec-threats/TM-${SLUG}.md"
```

Then read, in order: the ARCH doc's domain-relevant sections, the source files in
your domain, and any `.great_cto/PROJECT.md` fields your domain needs (e.g.
`code-sets:`, `payers:`, `compliance:`).

### Output — `docs/sec-threats/TM-${SLUG}.md`

Use your domain template at `skills/great_cto/templates/TM-{archetype}.md` if one
exists, else the Findings/Severity/Verdict grammar above. End the file with a
hand-off block the orchestrator parses:

```yaml
<!-- HANDOFF -->
{your-name}-verdict: signed-off | blocked
critical-findings: <N>
high-findings: <M>
must-implement-before-senior-dev:
  - <specific change 1>
  - <specific change 2>
gate: <gate:domain-signoff or — if none>
```

### Do NOT include in your prompt

- A "## Skills used" footer — your `skills:` frontmatter is the source of truth.
- A re-statement of the severity scale, verdict rules, prose rules, escalation
  policy, or self-test — all defined above in THIS skill.
- A copy of the Step-0 bash — it is canonical here.

See `skills/archetype-review-base/reviewer-template.md` for the minimal shape a
domain reviewer should follow after this scaffold is factored out.
