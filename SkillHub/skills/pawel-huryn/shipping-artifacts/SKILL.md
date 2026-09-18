---
name: shipping-artifacts
description: "The durable documentation set that makes an AI-built (vibe-coded) app reviewable before shipping. A small core every app needs — architecture, user/permission flows, permissions, variables/secrets, and a test-coverage map — plus conditional docs added only when they apply: emails, scheduled work, SEO, and embedded agents/automation. Defines what each doc must capture and how a reviewer or auditor uses it. Use when documenting a codebase for handoff, mapping user journeys and trust-boundary crossings, planning test coverage, or preparing for a security or performance audit."
---

# Shipping Artifacts: The Docs That Make AI-Built Code Reviewable

## Purpose

AI agents write code fast, but they leave no durable record of *intent* — what the system is supposed to do, who is allowed to do what, where the secrets live, which rules are actually verified. Without that record, no human (and no auditing agent) can tell whether the code is safe to ship. This skill defines the small set of documents that restore reviewability.

These docs live in `/documentation/` and are written for two readers: a human reviewer and the next AI coding agent. They are the **intended-state** half of every later audit — a security or performance review is only as good as the intent it can compare the code against.

## How the set is organized

The set is **not** a fixed list — it is a small **core** plus **conditional** docs you add only when the capability exists.

- **Core docs** — every reviewable app has these surfaces, so always produce them.
- **Conditional docs** — include one only if the app actually has that capability. If it doesn't, write a single line in `architecture.md` ("No scheduled work — no `cron.md`.") rather than inventing an empty document. Reviewability comes from an honest map, and "we don't do X" is part of the map.
- Most docs are reverse-engineered from code by `/document-app`. The one exception is `tests.md`, which is *derived from the other docs* by `/derive-tests` — it is the verification map, not a description of a subsystem.

Be brutally honest about the current state without being paranoid. The job is an accurate map, not a clean bill of health. Each doc is short, table-and-bullet heavy, and skips generic theory.

## Core documents

Each entry: file · one-line purpose · what it must capture · how a reviewer uses it.

1. **`architecture.md`** — what the system is and how it hangs together.
   - Must capture: product overview + key assumptions; tech stack; how auth/sessions/claims flow end to end; the trust boundaries (e.g. service-role vs. client); a short **Known risks / assumptions** list (each entry backed by where it shows up in the code, not a generic checklist); a "Related Documents" index of every other doc produced.
   - Reviewer use: the root document — everything else is cross-referenced from here.

2. **`flows.md`** — the journeys where permissions and side effects are actually exercised.
   - Must capture: each load-bearing flow as actor + precondition + success outcome; the step-by-step sequence across UI → server → data → jobs → providers → agents; the **authz check at each protected step** (which claim/role/scope, on which resource, and the expected *deny* case); the **trust-boundary crossings** (browser→server, server→provider, job→app, agent→tool, webhook→app); the state changes and side effects each step causes (writes, emails queued, jobs triggered, outbound calls).
   - Reviewer use: the runtime view a static `permissions.md` matrix can't show — *where* and *in what order* authorization is enforced, and where it can be skipped.
   - **Anti-PRD rule:** a flow that doesn't touch permissions, data integrity, external side effects, money, privacy, or operational safety does not belong here. This is a security/operations map, not a feature spec.

3. **`permissions.md`** — who is allowed to do what.
   - Must capture: roles/claims; where scope is derived (token vs. DB); a resource × operation × role matrix; which tables have row-level security and which rely on code-enforced checks.
   - Reviewer use: the baseline an access-control audit compares the code against. `flows.md` shows it in motion; this is the static reference.

4. **`variables.md`** — configuration and secrets, mapped to risk.
   - Must capture: a table of Name · used-by · scope (server/client) · source · rotation · risk; explicit confirmation that no secret is bundled client-side; a pre-go-live checklist.
   - Reviewer use: the secrets/PII-leak surface and the rotation plan during incident response.

5. **`tests.md`** — the verification map: which documented rules are actually checked, which are only proposed, and which are checked by nothing.
   - Must capture, in three clearly separated sections so the map can't read falsely green:
     - **Existing coverage** — tests that are in the repo *today*, each tied to the rule it pins (so the map reflects reality, not a wish-list).
     - **Proposed tests** — recommended cases not yet written, marked by **test type** (automated unit/integration · guarded live · manual review).
     - **Gaps** — documented rules with no verification at all, ranked by what crossing them exposes.
   - Each row carries: use-case → rule → expected behavior (including the deny/negative case) → evidence source (doc + code) → status (existing / proposed / none). It also notes which checks are CI-required and gate merges to `main`.
   - Reviewer use: the operational form of "documented == implemented" — it shows whether each rule the other docs claim is actually pinned by a test today, only proposed, or unverified.
   - Produced by `/derive-tests` (not `/document-app`), because it is derived from the other docs and the existing test suite rather than read off a subsystem.

## Conditional documents (include only when the capability exists)

6. **`emails.md`** — every notification the system sends. *Include only if the app sends transactional or automated email.*
   - Must capture: the queue → processor → provider path; templates and the variables they accept; retry/backoff behavior; where to look when a send fails.
   - Reviewer use: spotting unvalidated template inputs and PII exposure boundaries.

7. **`cron.md`** — all scheduled work and how to operate it safely. *Include only if scheduled or background jobs exist.*
   - Must capture: an inventory table (job → schedule → function → secrets → limits → retry); how each job stays idempotent; how internal calls authenticate; where to see last runs.
   - Reviewer use: finding forgeable triggers and unbounded background jobs.

8. **`seo.md`** — how a single-page app handles SEO and social previews. *Include only if there are public/indexable or bot-facing routes.*
   - Must capture: the preview approach (static meta / prerender / edge HTML); a route → needs-SEO → public-data-only table; how dynamic metadata is sanitized; bot-vs-human routing.
   - Reviewer use: catching public-data-only violations and metadata injection on bot routes.

9. **`automation.md`** — embedded agents and other automation paths. *Include only if the app embeds AI agents, LLM workflows, tool-calling, webhooks, or external automation.*
   - Must capture, per automation/agent: trigger + owner + whether it runs automatically or only after approval; the inputs it may read and the **exact tools/APIs it may call** (the tool surface is itself a hard guardrail); where **steering** lives (the prompt) vs. the **non-prompt hard guardrails**; the **output contract** back to the app (schema, validation, failure handling); **app-owned side effects vs. agent-owned suggestions**; and the controls — approval gates, audit/timeline logging, rate limits, retries, kill switch.
   - Reviewer use: makes hidden automation paths visible and draws the line between what an agent *proposes* and what the app *enforces* — the highest-risk surface in modern AI-built apps.

## Notes

- Each produced doc adds a reference to itself in `architecture.md` under a "Related Documents" section, so the set stays discoverable.
- Skip any conditional document that doesn't apply, and say so in one line rather than inventing content.
- Keep examples and finished templates out of these docs — they describe *this* system, not the general method.
- The agent operating-context file (`CLAUDE.md` / `AGENTS.md`) is a *different* artifact — instructions derived from these docs, not system documentation. It is produced at the handoff step by `/ship-check`, not here.
- `tests.md` is produced by `/derive-tests`; the rest are produced by `/document-app`.
- Do not include an "updated date" line; the file's history is the source of truth.
