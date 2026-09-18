---
name: poc-mode
description: POC/MVP mode: relaxed gates (no full ARCH, no full QA, no security audit), explicit kill-switch + graduation criteria to promote to production mode
when_to_use: Throwaway prototypes and time-boxed POCs. Read by architect at /poc + senior-dev when project_size=nano
applies_to:
  - _default
---

# POC / MVP mode — reference

CTO work has three distinct rigor levels, not one. This reference documents
what great_cto agents **skip** when `mode:` in `PROJECT.md` is `poc` or
`mvp`, and what gets restored when `/promote` runs.

Philosophy: **POCs answer questions; production ships them.** If the mode
is `poc`, we strip away ceremony that's correct for production but harmful
for a 3-day experiment. The cost of this optimisation is a **hard
forbidding line** — POC code cannot see production without `/promote`.

---

## Mode semantics

| Mode | Purpose | Timebox | Code fate | Default |
|---|---|---|---|---|
| `production` | Ongoing, real users | ongoing | long-lived | ✓ |
| `mvp` | First shippable version, real users, minimal features | 2–8 weeks | survives, churns | — |
| `poc` | Hypothesis-driven experiment | 1–14 days (max 1× 7d extension) | throwaway by default | — |

Set via `/start` (new project picks mode) or `/poc <hypothesis>` (flips
existing project into POC mode for one experiment).

---

## Skip matrix

Column headers are the mode. ✓ = full; ○ = minimal/lite; ✗ = skip entirely.

| Step | production | mvp | poc |
|---|:-:|:-:|:-:|
| `architect` ARCH document | ✓ full | ○ condensed | ○ **1-pager** (Problem / Decision / Risks only) |
| Non-goals section required | ✓ | ✓ | ○ (POC file's Out-of-scope substitutes) |
| Threat model (`TM-*.md`) | ✓ for security-critical archetypes | ○ required only for security-critical surfaces | ✗ |
| ARCH `## Security` section | ✓ for security-critical archetypes | ○ inline note OK | ✗ |
| SBOM (`SBOM-*.json`) | ✓ every release | ○ first production release | ✗ |
| Cost model | ✓ medium/large projects | ○ rough estimate OK | ✗ |
| `senior-dev` TDD rigor | ✓ strict RED→GREEN→REFACTOR | ✓ strict for critical paths | ○ **smoke test only**, no coverage target |
| `qa-engineer` QA report | ✓ full coverage + states + errors | ○ coverage + happy path | ○ **smoke test pass/fail**, written to `docs/qa-reports/QA-poc-<slug>.md` |
| `security-officer` CSO | ✓ required | ○ minimal | ✗ — except `credential-scan` (no hardcoded secrets, ever) |
| `gate:arch` blocking | ✓ | ✓ | ○ **advisory** (no `bd` task, visible in /inbox) |
| `gate:ship` blocking | ✓ | ✓ | ○ **advisory** — deploys only to preview/dev envs |
| `devops` production deploy | ✓ | ✓ | ✗ **prohibited** — POC code deploys only to `preview`/`dev`/`local` |
| Retrospectives | ✓ every feature | ○ per milestone | ✗ (learning captured via `/poc decide` instead) |
| Pentest | quarterly | pre-production | ✗ |
| Dependency audit (`/audit` CVE scan) | ✓ | ✓ | ○ skipped unless POC crosses day 7 |
| Anti-pattern lint (`/audit lint`) | ✓ | ✓ | ○ advisory only |
| `/digest` inclusion | ✓ | ✓ | ○ POC appears as "ongoing experiment" block, not feature |

## AI archetype overrides — `ai-system` and `agent-product` cannot fully skip security in POC mode

The skip matrix above applies to most archetypes. AI archetypes are different because the cost of a prompt-injection bypass or a leaked API key in a "throwaway" PoC is the same as in production — the model doesn't care that you labelled the project PoC.

| Step | poc — non-AI | poc — `ai-system` | poc — `agent-product` |
|---|:-:|:-:|:-:|
| Threat model | ✗ | ○ **3-section minimum**: prompt-injection vector, output exfiltration, cost runaway | ○ **5-section minimum**: above + tool-call sandbox + cross-user isolation if multi-tenant |
| Eval set (`tests/eval/EVAL-*.md`) | ✗ | ○ **3 scenarios minimum**: golden citation, refuse-when-uncertain, output-schema-stability | ○ **5 scenarios minimum**: above + 1 prompt-injection case + 1 budget-overrun case |
| `monthly-budget-llm-usd` in PROJECT.md | optional | **mandatory** — even at $5/mo, agents check it | **mandatory** |
| Cost guardrail in code | optional | ○ at minimum, log every LLM call's cost; project-auditor flags absence as P1 | ○ same + per-session BudgetTracker (see agent-pack) |
| `credential-scan` for LLM API keys | per default rule | mandatory — same as default | mandatory — same as default |
| Kill-switch documented | ✗ | ○ 1-line note in ARCH: "how to stop this and who can do it within N minutes" | ○ same |
| SSRF / URL allowlist if tool layer fetches user-suggested URLs | n/a | ○ scheme-and-port allowlist required even in PoC; scan for `requests.get` taking LLM-output is P0 | ○ same |

**Rule of thumb**: in AI PoC mode, you skip ARCH ceremony, TDD strictness, and full pentest — but you do NOT skip the threats that are unique to AI (prompt injection, cost runaway, tool-call abuse, model-jailbreak). Those are baseline risks regardless of project lifetime.

When the AI PoC promotes via `/promote`, the eval set and threat model upgrade to the full schema; the lite versions become the historical record of what the team knew at PoC time.

## The `credential-scan` exception

POC mode skips `security-officer` **except** for one hard rule: **no
hardcoded secrets**. Even in a 3-day POC, hardcoded API keys / passwords /
tokens get committed to git history and become a breach vector. Agents run
this check regardless of mode:

- `senior-dev` post-condition: grep the diff for common secret shapes
  (`sk-[A-Z]`, `AKIA[0-9A-Z]{16}`, `-----BEGIN * PRIVATE KEY-----`, long
  base64 strings in `.env` patterns).
- If found: fail the POC build and write the finding to
  `.great_cto/sec-findings.log`. POC continues only after secret is
  moved to environment variable or `.env.local` (git-ignored).

This is the only security rule that never relaxes.

---

## Agent behaviour in POC mode

Every agent checks `mode:` early in its workflow:

```bash
MODE=$(grep "^mode:" .great_cto/PROJECT.md 2>/dev/null | awk '{print $2}')
MODE=${MODE:-production}
```

Then branches on `$MODE`:

- **`architect`** — skip threat-model + cost-model + full ARCH sections;
  produce 1-pager instead. Note clearly at top: "POC ARCH — will be
  expanded by `/promote`."
- **`senior-dev`** — skip coverage target; write one smoke test per
  hypothesis criterion. Honour the credential-scan exception regardless.
- **`qa-engineer`** — smoke-only report; explicit line "This is POC QA,
  NOT production QA. See poc-mode.md."
- **`security-officer`** — skip full CSO; run credential-scan only. Write
  a one-line verdict to `.great_cto/verdicts/security-officer.log`.
- **`devops`** — refuse to deploy to `production` env if `mode: poc`.
  Preview/dev/local deploys are fine. Halt with: "POC mode — /promote
  required before production deploy."
- **`l3-support`** — unchanged. If POC code somehow ends up in production
  and breaks (shouldn't happen, but), l3-support treats it as any other
  incident.
- **`project-auditor`** — `/audit` notes POC mode at top of report:
  "Project is in POC mode — audit findings are informational."

---

## Forced-decision deadline

When `poc_expires:` date arrives:

- `/inbox` shows a **red** banner: "⚠ POC-<slug> expired — run `/poc decide`"
- No `mode: production` flip possible until `/poc decide` resolves
- `devops` refuses all deploys (including preview) from the POC branch
- After 7 days past expiry with no decision: `/inbox` escalates to "POC
  abandoned — agents will auto-revert `mode: production` on next session"
  (we don't actually auto-revert — we nag, but the code rots visibly)

This is deliberate. A POC that drifts past its deadline is either (a) not
a POC, it's a feature — in which case `/poc decide → SHIP → /promote`, or
(b) a zombie — kill it.

---

## What `/promote` restores

Promotion runs the steps POC mode skipped. Each is a gate — promotion is
all-or-nothing. See `commands/promote.md` for the full flow.

| Restored step | Agent / command |
|---|---|
| Full ARCH | `architect` expands 1-pager |
| Threat model (if archetype requires) | `/threat-model <slug>` |
| SBOM | `/sbom` |
| Cost model | `architect` adds `## Cost Model` section |
| Full CSO | `security-officer` |
| Full QA | `qa-engineer` |
| Blocking gates | `bd create gate:arch` + `gate:ship` |
| Decision log entry | appended to `docs/decisions/DECISION-LOG.md` |

---

## Anti-patterns

Documented here as negatives — these are ways POC mode gets abused.

1. **"Just ship the POC — we'll clean up later."** No. POC → `/promote` or
   POC → kill. There is no "ship without promotion" path. `devops` blocks it.
2. **Extending the timebox repeatedly.** Max 1 extension, max 7 days. After
   that, it's not a POC, it's a feature without a plan.
3. **POC without observable success criteria.** "It works" is not a
   criterion. If you can't write a human-verifiable criterion, you don't
   have a hypothesis — you have a vibe.
4. **Parallel POCs.** `/poc` refuses to start a second one while one is
   active. Multi-tasking experiments is how they all fail.
5. **POC for a known-good technology.** If you've used the tool before and
   know it works, you don't need a POC — you need to write the feature.
   POC exists for genuine uncertainty.

---

## When NOT to use POC mode

- **Spikes** (1-hour experiments in a REPL) — no command needed, just code
- **Refactors** — use normal feature pipeline
- **Bug fixes** — use normal hotfix path via `l3-support`
- **Known-good extensions** — if it's a feature of an understood system,
  `/start` or create an ARCH directly
- **Customer demos** — if real customers will touch it, it's MVP at
  minimum, not POC

POC mode is specifically for **pre-feature uncertainty reduction**. When
you genuinely don't know if a technical approach will work, and a
throwaway experiment will tell you faster than a full feature build.
