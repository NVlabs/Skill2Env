---
name: discovery
description: 4-6 question framework used when /start, /audit, /poc inputs are too sparse — disambiguates archetype, size, compliance before committing
when_to_use: Phase 0 of any new feature when requirements are vague. Read by architect at /start
applies_to:
  - _default
---

# Discovery Protocol

> Structured question framework used by `/start`, `/audit`, and `/poc` when input is too sparse
> to commit to an archetype + size + compliance combination. Avoids the failure mode of agents
> guessing PROJECT.md fields from a one-sentence description.
>
> **Rule:** never ask more than 8 questions total. Stop the moment the answers map to a clear
> archetype + tier. Most projects need 4–5 questions, not 8.

---

## When to invoke

Invoke this skill when ANY of the following holds for the user's input to `/start`, `/audit`, or `/poc`:

| Trigger | Detection |
|---------|-----------|
| Description shorter than 8 words | `[ $(echo "$DESC" \| wc -w) -lt 8 ]` |
| Vague intent without domain | matches "explore", "figure out", "not sure", "what's best" + no domain noun |
| Conflicting archetype signals | top-2 archetype scores within 1.5 points (Edge Case B/C in TYPE_MAP) |
| Existing repo without PROJECT.md | `/audit` finds code but no `.great_cto/PROJECT.md` |
| User asks "what should I build" | meta-question rather than a build request |

If NONE match → the description is sufficient, skip discovery and proceed to standard archetype detection.

---

## The question set (ask in order, stop early when archetype is clear)

Ask 2–3 questions at a time using `AskUserQuestion`. Do not dump all 8 at once.

### Block 1 — Audience + pain (almost always asked)

**Q1. Who uses this?**
- Internal team (employees / dev tools / ops)
- B2B customers (paying companies, contractual SLAs)
- B2C consumers (public, free or paid)
- AI agents / programmatic clients only
- Mixed (specify)

**Q2. What's broken without this? (one sentence)**
Free-form. Looking for the pain — if user says "it would be nice to have…" you have a research project, not a product.

### Block 2 — System shape (skip if Q1 + Q2 already clear)

**Q3. Greenfield or existing system?**
- Greenfield (clean slate)
- Existing — stack: ___ (paste a `package.json`/`go.mod`/`Cargo.toml`/`requirements.txt` if available)
- Migrating from: ___ to: ___

**Q4. Scale + latency expectations**
- 10s of users, async ok (internal tool)
- 1k users/day, response < 500 ms (typical SaaS)
- 100k+ users/day, response < 100 ms (consumer-scale)
- Real-time (sub-second, streaming) — specify
- Don't know yet (assume "1k users / 500 ms" then)

### Block 3 — Constraints (only if hints exist or compliance suspected)

**Q5. Hard compliance constraints**
- None
- PII (any personal data) → GDPR
- Payment data → PCI-DSS
- Health data → HIPAA
- Financial / regulated → SOC2, ISO 27001, possibly PCI
- Government / defence → FedRAMP, FIPS

**Q6. Time-to-first-deploy?**
- This week (POC / hackathon → use `/poc` not `/start`)
- This month (MVP)
- This quarter (standard feature)
- No deadline (research / strategic)

### Block 4 — Capacity + scope (only if size unclear)

**Q7. Who is shipping this?**
- Solo founder
- 2–5 engineers
- 5–15 engineers
- 15+ engineers, multi-team

**Q8. Name ONE thing this WON'T do.**
Free-form scope cutter. The "no" defines the product more than the "yes". If user can't name one, scope is dangerously open.

---

## Mapping answers → PROJECT.md fields

Apply rules in order. First match wins for each field.

### archetype

| Trigger pattern | archetype |
|-----------------|-----------|
| Q1 = AI agents only OR Q2 mentions "agent / autonomous / LLM-driven action" | `agent-product` |
| Q1 = B2C + Q4 ≥ 100k + Q5 = payment | `commerce` |
| Q1 = internal + Q2 mentions data / analytics / ETL | `data-platform` |
| Q1 = mixed + Q3 mentions K8s / Terraform / IaC | `infra` |
| Q5 = government / defence / clinical | `regulated` |
| Q2 mentions smart contract / DeFi / wallet | `web3` |
| Q2 mentions firmware / device / sensor | `iot-embedded` |
| Q2 mentions SDK / library / CLI / package | `library` |
| Q1 = consumer + Q3 mentions iOS / Android / React Native | `mobile-app` |
| Q1 = internal + Q2 mentions ML / RAG / embeddings | `ai-system` |
| Default | `web-service` |

### project_size (drives pipeline depth)

| Q7 (team) + Q6 (deadline) | project_size |
|---------------------------|--------------|
| solo + this week | `nano` |
| solo + this month | `small` |
| 2–5 + this month | `small` |
| 2–5 + this quarter | `medium` |
| 5–15 + any | `medium` or `large` (depends on Q4 scale) |
| 15+ + any | `large` or `enterprise` |

### compliance + security tier

Q5 maps directly. If Q5 = none AND Q1 = B2C + Q4 ≥ 100k → still upgrade to `standard` tier (volume creates obligation even without explicit regulation).

### poc-mode trigger

If Q6 = "this week" OR Q2 contains "validate / test the idea / not sure if it works" → reroute to `/poc`, not `/start`.

---

## Synthesis: propose 2–3 approaches before committing

After mapping, **never silently write PROJECT.md.** Instead, propose 2–3 concrete approaches with explicit tradeoffs, then let the CTO pick.

Format:

```
Based on your answers, here are 2–3 ways to approach this:

OPTION A — <name> (recommended)
  Archetype: <a>
  Size: <s>
  Compliance: <c>
  Pros: <2 specific pros derived from answers>
  Cons: <1 specific con>
  First milestone: <concrete deliverable in week 1>

OPTION B — <alternative shape>
  Archetype: <different>
  Size: <maybe smaller>
  Pros: <faster / cheaper / less risk>
  Cons: <ceiling lower>
  First milestone: <concrete>

OPTION C — <radical alternative>
  Maybe: skip building entirely (use existing tool X)
  Or:    /poc instead of /start
  Or:    different archetype entirely if Q1+Q2 reveal misfit

Which direction? (A / B / C / hybrid — describe)
```

The C option is mandatory and often the most valuable — sometimes the right answer is "don't build this, use Stripe / Auth0 / Postgres directly".

---

## Stop conditions

Stop the question flow as soon as ANY holds:

- Top-1 archetype score ≥ 6 AND ≥ 2 points above #2 → confident enough
- 5 questions answered
- User says "just pick something / I don't know / use defaults" → use defaults from ARCHETYPES.md `web-service + medium + standard tier` and proceed; mark in PROJECT.md `discovery: defaulted`
- User says "I want to talk through this freely" → invoke `superpowers:brainstorming` skill instead of continuing the structured Q&A

---

## Open-ended fallback: superpowers:brainstorming

For genuinely fuzzy ideation ("I want to do something with AI for legal", "build something cool with crypto"), structured Q&A makes the user feel interrogated. In those cases, invoke the **superpowers:brainstorming** skill — it explores intent in a more conversational, divergent way.

Heuristic: if Q1 reveals "I'm not sure who would use it" → switch to brainstorming. Discovery is for narrowing scope; brainstorming is for finding scope.

---

## What to write after CTO picks an option

The output depends on which option was chosen.

### Option A or B picked → write `.great_cto/PROJECT.md`

```markdown
# <project-name>

primary: <archetype>
project_size: <size>
phase: planning
team-size: <number>
compliance: <list>
discovery: completed
discovery-summary: |
  Audience: <Q1 answer summary>
  Pain: <Q2 verbatim>
  Scope cut: <Q8 verbatim>
  Chosen approach: Option <A|B> — <one-line reason>
```

If Option B → also run `/poc "<the falsifiable hypothesis>"` after creating PROJECT.md.

The `discovery-summary` field is read by `architect` at ARCH time so it can preserve user intent in the architecture doc — not just the field values.

### Option C picked → write `.great_cto/DISCOVERY-NO-BUILD.md` instead

When the user picks "don't build it / use vendor X" the pipeline must NOT start.
Write a DISCOVERY-NO-BUILD.md that captures the decision so future sessions don't re-ask:

```markdown
# Discovery Outcome: NO BUILD (Option C)

Date: <YYYY-MM-DD>
Outcome: do-not-build

## Inputs
- Initial description: "<verbatim>"
- Audience: <Q1>
- Pain: <Q2>
- Compliance: <Q5>
- Team: <Q7>

## Why no build
<one paragraph: why building from scratch is wrong for this constraint set>

## Vendor shortlist (evaluate in next 7 days)
| Vendor | Pricing | GDPR | PCI | Notes |
|--------|---------|------|-----|-------|
| <name> | <approx> | ✓/✗ | ✓/✗ | <fit notes> |

## Re-evaluation criteria (revisit in 6 months)
Build your own only if ALL hold:
1. <demand-validated condition — typically "N paying customers using vendor">
2. <ROI condition — typically "vendor cost > $X/year">
3. <ceiling condition — typically "hit a customization vendor can't fix">
4. <capacity condition — typically "funding to hire N engineers">

If conditions hold later → run `/start "<refined description>"`.

## Action items
- [ ] /poc "vendor evaluation: <vendor-A> vs <vendor-B> on 50 sample <items>" — 7 day timebox
- [ ] After vendor pick: integrate via their API
- [ ] Calendar reminder: revisit build-vs-buy in 6 months
```

**Critical**: do NOT also write PROJECT.md in this case. The presence of DISCOVERY-NO-BUILD.md tells `/start` "this project decided not to build — running /start again should re-confirm or supersede this decision".

---

## Privacy

Discovery answers can contain client names, internal product info, business model details. **Do not write them to KE files** if a discovery-related learning gets crystallized later. Generic technology lessons only.
