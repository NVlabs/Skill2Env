---
name: IMPL-BRIEF-template
description: Per-task implementation brief — files to modify / files NOT to modify (anti-scope-creep guardrail) / step-by-step + paired API-CONTRACT, TEST-SPEC, and ACCEPTANCE. Emitted per impl task by pm (or architect); read by senior-dev before writing code. Machine-checkable via scripts/lib/impl-brief.mjs.
when_to_use: pm Step 7b emits one IMPL-BRIEF per senior-dev task into docs/impl-briefs/IMPL-BRIEF-<task-id>.md. senior-dev reads it before claiming the task and runs the scope check before commit. Cuts scope creep — a changed file outside the allow/deny lists is flagged.
applies_to:
  - ai-system
  - agent-product
  - commerce
  - web3
  - browser-extension
  - game
  - regulated
  - fintech
  - iot-embedded
  - data-platform
  - mobile-app
  - library
  - enterprise
  - web-app
  - devtools
  - infra
  - marketing-site
---

# IMPL-BRIEF-{task-id}.md — implementation brief for one task

> **One brief per senior-dev task.** Emitted by `pm.md` Step 7b (derived from the ARCH
> doc + the PLAN task row); read by `senior-dev.md` Step 4 before any code is written.
> Source: `skills/great_cto/templates/IMPL-BRIEF-template.md`. Destination:
> `docs/impl-briefs/IMPL-BRIEF-<bd-task-id>.md`.
>
> **Why this exists (governance Phase 3):** an unscoped task invites scope creep — the
> implementer touches files nobody reviewed, or re-derives an API the ARCH already pinned.
> This brief makes the boundary explicit and **machine-checkable**:
> `node scripts/lib/impl-brief.mjs check <brief> <changed-files…>` flags any file that
> falls outside `## Files to modify` or matches `## Files NOT to modify`.

## Task

- **bd task:** `{bd-task-id}` — `{task title from PLAN}`
- **Feature:** `{feature-slug}` · PLAN: `docs/plans/PLAN-{feature-slug}.md`
- **ARCH:** `docs/architecture/ARCH-{feature-slug}.md` · component: `{component this task builds}`
- **Implements REQ / UC:** `{REQ-n, UC-n — or "none" if infra/chore}`

## Files to modify

> The allowlist. Every entry is a path or glob the implementer is expected to touch.
> List the file **and the reason**, so review knows what each change is for.
> `scripts/lib/impl-brief.mjs check` treats a changed file NOT matched here as a
> scope-creep warning.

| File / glob | Why it changes |
|---|---|
| `{src/feature/foo.ts}` | {add endpoint X handler} |
| `{tests/feature/foo.test.ts}` | {RED tests for endpoint X} |
| `{src/feature/index.ts}` | {wire the new handler into the router} |

## Files NOT to modify

> The denylist — the anti-scope-creep guardrail. These are tempting-but-out-of-bounds:
> shared modules another task owns, generated files, config the ARCH froze, god-nodes
> from `.great_cto/CODEBASE.md`. A changed file matching any entry is a **hard scope
> violation** (`check` exits non-zero), not a warning. If you genuinely need to touch one,
> stop and go back to pm/architect — don't silently widen scope.

| File / glob | Why it's off-limits | Who owns it |
|---|---|---|
| `{src/shared/auth/**}` | {owned by WP-2, parallel task — would conflict} | {senior-dev #2} |
| `{db/schema.sql}` | {ARCH froze the schema for this phase} | {architect} |
| `{src/generated/**}` | {generated artefact — edit the source, not the output} | {build} |

## Step-by-step

> The implementation sequence. Keep steps to ~2–5 min of work each, RED→GREEN→REFACTOR.

1. {Write failing test in `tests/feature/foo.test.ts` for the happy path of endpoint X.}
2. {Implement `foo.ts` handler until the test passes.}
3. {Add the error-path test (invalid input → 400) and make it pass.}
4. {Wire the handler into `index.ts`; run the full suite.}

## API-CONTRACT

> The interface this task must honour — copied/narrowed from the ARCH `## API contracts`.
> Pin it here so the implementer doesn't re-invent signatures or response shapes.

- **Surface:** `{function signature / HTTP route + method / CLI subcommand}`
- **Input:** `{params, types, required vs optional, validation rules}`
- **Output (success):** `{return type / response body shape / exit code 0}`
- **Errors:** `{error type / status code / message contract for each failure mode}`
- **Invariants:** `{idempotency? auth required? rate limit? no breaking change in MINOR?}`

## TEST-SPEC

> The tests this task must add (the RED list). qa-engineer and the Proof Loop check these
> exist and pass. Each row → at least one test case.

| # | Case | Expected |
|---|---|---|
| 1 | {happy path — valid input} | {200 + body shape, or returns value V} |
| 2 | {invalid input} | {400 + error contract from API-CONTRACT} |
| 3 | {boundary / edge case} | {documented behaviour} |
| 4 | {regression guard for a known postmortem, if any} | {no recurrence} |

- Coverage target: `{from PROJECT.md, default ≥80%}`
- Run: `{exact test command, e.g. npm test -- foo.test.ts}`

## ACCEPTANCE

> Done = all boxes checked. senior-dev verifies these in the Step 10 Proof Loop before
> closing the bd task; mirrors the ARCH Definition of Done, narrowed to this task.

- [ ] Every row in **TEST-SPEC** has a passing test
- [ ] Every REQ/UC in **Task** is implemented and has a test that proves it
- [ ] No file outside **Files to modify** was changed (`impl-brief.mjs check` clean), or a
      signed exception covers the deviation
- [ ] No file in **Files NOT to modify** was touched
- [ ] API-CONTRACT honoured exactly (signatures + error contract)
- [ ] Coverage ≥ target; lint clean; no hardcoded secrets

## Out of scope / deferred

> What this task explicitly does NOT do — pushed to a later task or phase. Prevents the
> implementer from "while I'm here…" expansion.

- {e.g. caching the endpoint response — deferred to WP-5}
- {e.g. i18n of error messages — out of scope this phase}

## Revision history

| Date | Author | Change |
|---|---|---|
| {YYYY-MM-DD} | {pm / architect} | Initial brief |
