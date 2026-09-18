---
name: agent-style
description: 21 prose-style rules for technical writing in agent outputs (no fluff, active voice, concrete numbers, no apologetics) — adapted from Strunk/White/Orwell/Pinker
when_to_use: Writing ARCH/QA/CSO reports. Read by qa-engineer + project-auditor to enforce prose quality
applies_to:
  - _default
---

# Agent Writing Style — 21 rules

> Condensed adaptation of [yzhao062/agent-style](https://github.com/yzhao062/agent-style) v0.3.1
> (CC BY 4.0). Source: 12 rules from Strunk & White / Orwell / Pinker, 9 from
> field observation of LLM output 2022–2026. Apply at **generation time** —
> these are not a post-hoc linter. When a rule fights the sentence, drop the rule.

## Scope

**Apply to**: ARCH docs, ADRs, RFCs, CSO reports, QA reports, postmortems, runbooks,
CHANGELOG entries, commit messages, board reports, error messages, release notes.

**Do not apply to**: code identifiers, log lines, JSON keys, structured data fields,
test names. These have their own conventions.

## Severity

- **critical** — reader cannot understand or trust the prose if violated
- **high** — externally visible AI-tell or recurring clarity failure that breaks skim-reading
- **medium** — local readability cost
- **low** — polish; flagged for consistency

---

## Audience and Reader State

### RULE-01 — Resist the Curse of Knowledge (critical)

Name the reader before writing: junior engineer for API docs, on-call for runbooks,
cross-panel reviewer for proposals, release reader for changelogs. If they would pause
to infer what a term means, define it or rewrite.

- BAD: `The API uses JWT with RS256 refresh tokens rotated via the OIDC flow.`
- GOOD: `Authentication uses short-lived signed tokens (JWT with RS256) issued by our OIDC identity provider. Clients refresh these tokens before expiry through the standard OIDC refresh flow.`

## Voice and Directness

### RULE-02 — Active voice when the agent matters (high)

"Y did X" not "X was done by Y" — active voice names the agent and shortens the sentence.
Passive is correct only when agent is genuinely unknown or irrelevant (scientific
attribution, observation of phenomena).

- BAD (postmortem): `The incident was caused by a misconfigured load balancer rule.`
- GOOD: `A misconfigured load balancer rule (typo in the ingress-nginx path-rewrite regex) routed /auth/* to the wrong upstream and caused the incident.`

## Word Choice

### RULE-03 — Concrete over abstract (high)

Replace category words (`factors`, `aspects`, `considerations`, `issues`, `elements`)
with the specific items. If you reach for a category word, ask: what exactly?

- BAD: `The model shows improvements across various metrics.`
- GOOD: `The model improves F1 by 3.2 points (0.812 → 0.844) on FEVER and cuts hallucination rate from 11.3% to 6.8% on TruthfulQA.`

### RULE-04 — Omit needless words (medium)

Strunk's rule. "In order to" → "to". "It should be noted that" → drop. "At this point in time" → "now".

### RULE-05 — Avoid dying metaphors and prefab phrases (medium)

"Move the needle", "best-in-class", "low-hanging fruit", "deep dive", "leverage", "synergy"
in technical prose. If everyone says it, no one reads it.

### RULE-06 — Everyday words over jargon when both work (medium)

"Use" beats "utilize". "End" beats "terminate". "Show" beats "demonstrate". Jargon is
free when it earns its place (PCI-DSS, MV3, RPO are correct technical terms);
empty when it's affect ("operationalize", "actionable insights").

## Claims and Calibration

### RULE-07 — Affirmative form for affirmative claims (medium)

"Trivial" not "not important". "Forgot" not "did not remember". "Often" not "not infrequently".

### RULE-08 — Calibrate claims to evidence (high)

If you say "significantly faster" without a number, the reader cannot verify. If you say
"roughly 3× faster on a 10-run microbenchmark, single-machine, no network", they can.

- BAD: `Significantly improves performance.`
- GOOD: `Cuts p95 from 450ms to 120ms on the checkout endpoint at 1k RPS (k6, 3 runs, no warm-up).`

## Sentence Structure

### RULE-09 — Parallel structure for coordinate ideas (medium)

If three list items, three same-shape verbs.

- BAD: `The pipeline detects, will identify, and is going to fix.`
- GOOD: `The pipeline detects, identifies, and fixes.`

### RULE-10 — Keep related words together (high)

Modifier next to the thing it modifies. Subject next to verb. Long subordinate clauses
between subject and verb force the reader to hold the sentence in working memory.

### RULE-11 — Stress position at the end (medium)

The end of the sentence is where readers store what they remember. Put new or important
information there, not in the middle.

### RULE-12 — Break long sentences; vary length (medium)

If > 30 words, split. Mix short and long. A monotonic sentence rhythm is an AI-tell.

---

## Observed LLM Patterns (RULE-A through RULE-I)

### RULE-A — Bullets only for genuine lists (high)

Don't convert prose into bullets when the content is a connected argument. Bullets fragment
reasoning that needed to flow as paragraphs. Two-sentence bullets are a sign you needed prose.

### RULE-B — No em/en dashes as casual punctuation (high)

The em-dash habit (`X — and that's why`) is the loudest AI-tell of 2024–2026. Use commas,
parentheses, periods, or rewrite. Reserve em-dash for genuine asides where parens are wrong.

### RULE-C — No consecutive sentences starting with the same word (medium)

"This X. This Y. This Z." — pick different openers.

### RULE-D — Don't overuse "Additionally / Furthermore / Moreover" (high)

These are throat-clearing transitions LLMs ship by default. Drop the connector or use
a stronger one ("Even so", "By contrast", "The exception:").

### RULE-E — Don't close every paragraph with a summary sentence (high)

LLM habit: "In summary, X." after every section. The reader just read the section. Trust
them. Close with new information or a transition, not a recap.

### RULE-F — Consistent terms; do not redefine abbreviations (medium)

If the doc says "rollback" once, don't switch to "rollbacks", "rolling back", "the rollback
process" in the same section. Pick a phrase, stick with it.

### RULE-G — Title Case for headings (low)

`## Subscription Reactivation Flow` not `## Subscription reactivation flow` (sentence case
is fine if used consistently throughout the doc; pick one and don't mix).

### RULE-H — Support claims with citation or evidence; no handwaving (critical)

"Studies show", "industry best practice", "everyone agrees" — without a link, a number,
or a specific reference, the reader can't verify the claim. AI hallucinates citations
when given soft directives — be exact about source or admit you don't have one.

- BAD: `Industry best practice is to use UUIDs for primary keys.`
- GOOD: `For primary keys, prefer UUIDs over auto-increment integers when keys may be exposed in URLs (e.g. /users/:id) — auto-increment leaks count and ordering. See [PostgreSQL Wiki: Don't Do This — UUID](https://wiki.postgresql.org/wiki/Don%27t_Do_This).`

### RULE-I — Full forms over contractions in technical prose (low)

"Do not" not "don't" in formal documents (ADRs, CSOs, postmortems, contracts). Casual
contractions are fine in commit messages, runbooks, error strings.

---

## Quick Self-Check Before Writing

Before generating prose, the agent runs a 5-second checklist:

1. **Reader named?** (Rule 01)
2. **Active voice unless agent unknown?** (Rule 02)
3. **No filler bullets / no em-dash habit / no "Additionally / In summary"?** (Rules A, B, D, E)
4. **Numbers attached to every claim of improvement?** (Rule 08)
5. **Citations or admitted absence of source?** (Rule H)

These five cover ~80% of AI-tells in technical prose. The remaining 16 rules add polish
but do not change whether the document is trustworthy.

---

## Source

Curated from: yzhao062/agent-style v0.3.1 (CC BY 4.0). Original 21-rule expanded source
with full BAD/GOOD examples and rationale: <https://github.com/yzhao062/agent-style/blob/main/RULES.md>.

Strunk & White, *The Elements of Style* (1959, 4th ed. 2000) — Rules 03, 04, 09.
George Orwell, "Politics and the English Language" (1946) — Rules 02, 05.
Steven Pinker, *The Sense of Style* (2014), Ch. 3 — Rules 01, 03.
