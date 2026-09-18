---
name: ARCH-default
description: Standard ARCH document template for archetypes without dedicated templates: Decision with alternatives, Components, API contracts, Data model, Non-goals, Implementation work-packages, Cost, Risks
when_to_use: Writing ARCH for web-service, library, mobile-app, data-platform, infra archetypes
applies_to:
  - web-service
  - library
  - mobile-app
  - data-platform
  - infra
---

# ARCH-{slug}.md — Standard architecture document

> **Reader:** the engineer joining in 6 months. Be exact about decisions, trade-offs, and what you chose NOT to do.
> **Source:** `skills/great_cto/templates/ARCH-default.md`. Default for archetypes: web-service, library, mobile-app, data-platform, infra. AI / commerce / web3 / regulated / browser-extension / game have their own templates.

## Decision (one sentence)
{What we're building, in plain language, for the named reader.}

## Problem
- What pain are we solving?
- Who feels it?
- Evidence that it exists (issue ticket count, support load, SLO breach, lost revenue)?

## Decision (with alternatives)

### Option A — chosen
**What:** {approach}
**Why:** {1-line rationale}
**Trade-offs accepted:** {what we lose}

### Option B — rejected
**What:** {alternative}
**Why rejected:** {concrete reason — cost, complexity, time-to-market, team skill}

### Option C — rejected
**What:** {do nothing OR use existing tool X}
**Why rejected:** {why building is justified}

## Components
| Component | Responsibility | Technology | Owner |
|---|---|---|---|
| {API gateway} | {auth, rate limit, routing} | {Caddy / Nginx / Kong} | {team} |
| {Service A} | {user-facing endpoint X} | {language + framework} | {team} |
| {Database} | {persistent state for X, Y} | {Postgres / DynamoDB / Redis} | {team} |
| {Background worker} | {async job X} | {Celery / BullMQ / SQS+Lambda} | {team} |

## API contracts (if external interfaces)
- OpenAPI spec: `api/openapi.yaml` (generated / hand-maintained)
- GraphQL schema: `api/schema.graphql` (if applicable)
- Public endpoints: {list with request/response shape}
- Authentication: {Bearer JWT / OAuth / API key / mTLS}
- Versioning rule: no breaking change in MINOR/PATCH

## Data model
- ER diagram or schema file: `db/schema.sql` / `db/schema.prisma`
- Migration tooling: {Flyway / Alembic / Prisma migrate / db-migrate}
- Migration safety rules: see `references/db-migration.md`
- PII columns: {flag if any — drives data-platform compliance}

## Non-goals (explicit out-of-scope)
- {e.g. we don't support real-time updates — phase 2}
- {e.g. we don't handle internationalisation — English-only for now}
- {e.g. we don't migrate legacy data — fresh slate}

## Implementation tasks (work-packages)
Each row → one bd task created by architect.

| WP | Title | Effort | Owner | Depends on |
|---|---|---|---|---|
| WP-1 | {set up DB schema + migrations} | M | senior-dev | — |
| WP-2 | {build endpoint X} | M | senior-dev | WP-1 |
| WP-3 | {add tests + CI} | S | senior-dev | WP-2 |
| WP-4 | {deploy script + canary} | S | devops | WP-3 |

## Definition of Done
- [ ] All work-packages closed in bd
- [ ] Tests pass (unit + integration; coverage target from PROJECT.md)
- [ ] /review 12-angle scan: 0 P0 findings
- [ ] qa-engineer report: PASS
- [ ] security-officer post-impl: APPROVED (if security-gate: mandatory)
- [ ] devops canary deploy successful
- [ ] Release notes drafted

## Cost estimate (medium / large / enterprise projects)
| Item | Per-unit cost | Volume | Monthly |
|---|---|---|---|
| Compute | {$0.10/hr × 730} | {N instances} | {$X} |
| Storage | {$0.10/GB} | {N GB} | {$X} |
| Egress | {$0.09/GB} | {N GB} | {$X} |
| Third-party SaaS | {Stripe / Sentry / Datadog} | {tier} | {$X} |
| **Total** | | | **${total}** |

Cap (`monthly-budget` in PROJECT.md): {$N} → {N% headroom}

## Safeguards ← senior-dev reads before writing any code; security-officer cross-checks at CSO

> Non-negotiable invariants for this feature. `senior-dev`: acknowledge every item before starting.
> Add/remove items per archetype. Never leave this section empty.

### Data integrity
- [ ] {e.g. All monetary values stored as integer cents — never float or string}
- [ ] {e.g. Mutations to `orders` table wrapped in transaction — no partial writes}

### Security
- [ ] {e.g. Auth check on every route under `/api/admin/*`}
- [ ] {e.g. Raw DB errors never exposed in API response body}
- [ ] {e.g. No secrets, PII, or card data in logs}

### Performance
- [ ] {e.g. Max request payload: 10 MB — reject with 413 before processing}
- [ ] {e.g. Every DB query has a timeout ≤ 5 s}

### API contracts
- [ ] {e.g. No breaking change to existing endpoint signatures in this feature}
- [ ] {e.g. Deprecation header added before removing any field}

> **Archetype hints (fill in the relevant ones, delete the rest):**
> - `commerce`: idempotency key on every payment mutation; card data via PSP JS only — never our server
> - `ai-system / agent-product`: per-user cost cap enforced; user input sanitised before LLM call; no PII in prompts
> - `web3`: CEI pattern on every state-changing function; ReentrancyGuard on ETH-receiving contracts
> - `iot-embedded`: no dynamic allocation in interrupt handlers; watchdog on critical paths
> - `regulated / fintech`: immutable audit log for every state change; data-residency constraint honoured

## Risks
| # | Risk | Probability × Impact | Mitigation |
|---|---|---|---|
| R-1 | {DB migration takes 4 h, blocks deploy window} | M × H | run migration in shadow first, validate, then promote |
| R-2 | {Stripe webhook delivery delayed > SLA} | L × M | DB reconciliation job hourly (commerce-pack pattern) |

## Stack considerations
- Why this stack vs alternatives evaluated: {1-2 sentences}
- Known unmitigated pre-mortem scenarios: {flag with PRE-{slug}.md row reference}

## Open questions
- {Items the maintainer must decide before next ARCH revision}
