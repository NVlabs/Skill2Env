<!--
SPDX-License-Identifier: CC-BY-4.0
Adapted from https://github.com/yzhao062/agent-style (v0.3.1), RULES.md (CC-BY-4.0).
Subset of 7 rules tuned for great_cto agent output (reports, CHANGELOGs,
audit findings, security/QA write-ups). One BAD/GOOD pair per rule — see
upstream for the full 5-example blocks and per-source citations.
-->

# Prose Style — 7 Rules for Agent Output

When you write prose for a human reader (audit findings, QA reports, CSO reports, CHANGELOG entries, /digest, /inbox summaries), follow these rules. They exist to make agent-written text land with founders and on-call engineers instead of reading like AI boilerplate.

**Escape hatch (Orwell 1946 Rule 6):** *"Break any of these rules sooner than say anything outright barbarous."* Rules are guides to clarity, not ends.

---

## RULE-01 — Do Not Assume the Reader Shares Your Tacit Knowledge

**Directive.** Before any technical paragraph, pick the reader one level below your own expertise. For great_cto that is: a solo founder or junior engineer who has never seen this codebase. If a term would make them pause, define it or rewrite around it.

- BAD: `The API uses JWT with RS256 refresh tokens rotated via the OIDC flow.`
- GOOD: `Authentication uses short-lived signed tokens (JWT with RS256) issued by our OIDC identity provider. Clients refresh these tokens before expiry through the standard OIDC refresh flow.`

**Why it matters for agents.** LLMs default to a near-expert register because their training corpus sits there. Solo-founder users of great_cto are not a peer of that distribution.

---

## RULE-03 — Do Not Use Abstract Language When a Concrete Term Exists

**Directive.** Replace category nouns (`factors`, `aspects`, `issues`, `considerations`, `elements`) with the specific items they point at. If "what exactly?" takes more than one clause, the sentence was hiding the work.

- BAD: `The model shows improvements across various metrics.`
- GOOD: `F1 rose 3.2 points (0.812 → 0.844) on FEVER; hallucination rate fell from 11.3% to 6.8% on TruthfulQA.`

**Why it matters for agents.** `/audit` and `/inbox` output carrying "several issues" or "multiple considerations" is indistinguishable from the LLM hedging. Name the things.

---

## RULE-04 — Do Not Include Needless Words

**Directive.** `in order to` → `to`. `due to the fact that` → `because`. `at this point in time` → `now`. `it is important to note that` → (delete, state the fact). `may potentially` / `could possibly` → `may` / `could`. Every filler phrase delays substance by one comma.

- BAD: `It is important to note that the learning rate was reduced in order to prevent divergence.`
- GOOD: `We reduced the learning rate to prevent divergence.`

**Why it matters for agents.** Filler phrases are the #2 visible AI-tell after clichés. A subset is mechanically denied in `enforcement/prose-deny.txt`.

---

## RULE-05 — Do Not Use Dying Metaphors or Prefabricated Phrases

**Directive.** If a phrase feels off-the-shelf ("push the boundaries", "unlock the full potential", "paves the way", "industry-leading", "state-of-the-art", "paradigm shift") — restate in plain technical terms with specific numbers or mechanism, or delete the sentence.

- BAD: `Our groundbreaking approach represents a paradigm shift in observability.`
- GOOD: `Our tracer captures p99 latency per-span with 50ns overhead, down from the 400ns of OpenTelemetry's default SDK.`

**Why it matters for agents.** The most visible AI-tell signal in generated prose. Deny-list catches the common offenders; the rest is judgment.

---

## RULE-08 — Do Not Overstate or Understate Claims Relative to Evidence

**Directive.** Match word strength to evidence strength. `proves` only if it proves. `suggests` / `indicates` for one result; `confirms` only after replication. `significant` only with a test. `faster` always carries a number and a comparator.

- BAD: `Our changes significantly improve performance.`
- GOOD: `p95 latency on `/search` dropped from 320ms to 210ms after the cache change (n=1 week, prod traffic).`

**Why it matters for agents.** Audit findings, security severity ratings, and QA verdicts go to stakeholders. Over-claiming destroys the agent's credibility for the next finding.

---

## RULE-A — Do Not Convert Prose into Bullets Unless the Content Is a List

**Directive.** Bullets are for enumerable, parallel items (≥3 of equal weight). Two items = a sentence. Paragraph of flowing argument = a paragraph. Nested 1-item bullets are never correct.

- BAD:
  - The change reduces latency.
  - It also lowers memory usage.
- GOOD: `The change reduces latency and lowers memory usage.`

**Why it matters for agents.** Bulleting everything is an LLM tic that fragments cause-and-effect into floating facts.

---

## RULE-H — Support Factual Claims with Citation or Concrete Evidence (critical)

**Directive.** Every factual claim in an agent report carries one of: file:line reference, commit SHA, metric with unit and source, CVE/CWE ID, or a direct quote. If a finding has no evidence pointer, it is not a finding — it is a guess. Flag it as "unverified" or drop it. **Never invent references.**

- BAD: `The authentication layer appears to have a race condition.`
- GOOD: ``Race condition: `src/auth/session.ts:142-156` reads `session.user` before the `await lock.acquire()` at line 149. Repro: 2 concurrent POSTs to `/login` cause `user` to be set from the second request's context (verified on commit `a3f21bb`).``

**Why it matters for agents.** The single worst failure mode of LLM-driven review: handwavy claims and fabricated citations. security-officer, qa-engineer, and project-auditor MUST cite evidence. `/audit` without file:line is not audit.

---

## How Agents Use This Skill

- **security-officer, qa-engineer, project-auditor**: every finding requires RULE-H evidence pointer; every severity claim requires RULE-08 calibration.
- **qa-engineer**: runs a warn-only grep against its own report for RULE-04/05 deny-phrases before emitting.
- **senior-dev, architect**: consulted on CHANGELOG / architecture-doc output.

Upstream reference: https://github.com/yzhao062/agent-style (v0.3.1).
