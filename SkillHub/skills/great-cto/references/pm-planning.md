# PM Planning Reference

> Used by the `pm` agent. Estimation models, parallelism rules, agent allocation, Gantt templates.

---

## Project modes

> **Important:** In great_cto, all implementation work is done by LLM agents (senior-dev, qa-engineer,
> security-officer), not humans. `team-size` in PROJECT.md = number of human approvers at gates, not
> agent count. Parallel pools always run as concurrent LLM subagents — never serialised by team-size.
> The only hard calendar blockers are `gate:*` checkpoints where a human must respond.

| Mode | Trigger | Depth | LLM wall-clock | Calendar (incl. gates) |
|------|---------|-------|----------------|------------------------|
| **PoC** | `project_size: nano` or `/poc` invocation | 3–10 tasks, 1 agent pool | 0.5–4h | same-day |
| **MVP** | `project_size: small` or explicit POC→MVP | 10–30 tasks, 2–4 agent pools | 2–8h | 1–3 days |
| **Full** | `project_size: medium|large|enterprise` | 30+ tasks, N agent pools | 1–3 days | days–weeks |

---

## Estimation model

> **Unit: LLM agent wall-clock time** — how long a focused senior-dev subagent takes to complete
> a task including reading context, writing code, running tests, and verifying output.
> LLM agents are 5–10x faster than human developers on mechanical coding tasks.
> Estimate task complexity, not human-equivalent effort.

### Task cost by type (LLM agent wall-clock, single senior-dev subagent)

| Task type | Signal | PoC | MVP | Full |
|-----------|--------|-----|-----|------|
| Schema / data model | new tables, migrations | 5 min | 15 min | 30 min |
| API endpoint (CRUD) | REST/GraphQL, no auth | 5 min | 10 min | 20 min |
| API endpoint (auth/billing) | payment, IAM path | 15 min | 30 min | 60 min |
| Frontend component | React/Vue, no API | 5 min | 10 min | 20 min |
| Frontend page (with API) | full data flow | 10 min | 20 min | 45 min |
| Background job / worker | queue, retry logic | 10 min | 20 min | 45 min |
| LLM integration (simple) | single prompt, no tools | 10 min | 20 min | 40 min |
| LLM agent (tool-using) | multi-tool, eval harness | 20 min | 45 min | 90 min |
| Infrastructure (basic) | Docker, CI, env | 5 min | 15 min | 30 min |
| Infrastructure (cloud) | Terraform, IAM, VPC | 15 min | 40 min | 90 min |
| Test suite (unit) | per-module | 5 min | 10 min | 20 min |
| Test suite (integration) | multi-service | 10 min | 25 min | 45 min |
| Security review / CSO | per archetype tier | 10 min | 20 min | 45 min |
| QA report | per feature | 5 min | 15 min | 30 min |

**Buffer rules (account for tool errors, retries, context loading):**
- PoC: no buffer (speed over accuracy)
- MVP: +25% (integration surprises, file conflicts between agents)
- Full: +40% (larger context, more coordination points)

**Gate wait time = human async review, not LLM time:**
- `gate:arch` human review: +0.5–4h (depends on CTO availability)
- `gate:plan` human review: +0.5–4h
- `gate:ship` human review: +0.5–4h
- Report gate wait separately from LLM compute time in all summaries.

---

## Token cost model

> Always estimate LLM cost per task and total project cost. Use claude-sonnet-4-6 as default model.
> Pricing (as of 2026): input $3/M tokens · output $15/M tokens · cache read $0.30/M tokens.
> Prompt caching is active for agent system prompts (assume 80% cache hit rate for long agents).

### Token estimates per task type (input + output, single agent invocation)

| Task type | Input tokens | Output tokens | Cache hit on input | Cost (Sonnet 4.6) |
|-----------|-------------|---------------|-------------------|-------------------|
| Schema / data model | 8k | 1k | 70% | $0.04 |
| API endpoint (CRUD) | 10k | 2k | 70% | $0.05 |
| API endpoint (auth/billing) | 15k | 4k | 70% | $0.09 |
| Frontend component | 8k | 2k | 70% | $0.05 |
| Frontend page (with API) | 12k | 3k | 70% | $0.07 |
| Background job / worker | 12k | 3k | 70% | $0.07 |
| LLM integration (simple) | 10k | 2k | 70% | $0.05 |
| LLM agent (tool-using) | 20k | 5k | 70% | $0.10 |
| Infrastructure (basic) | 8k | 2k | 70% | $0.05 |
| Infrastructure (cloud) | 15k | 4k | 70% | $0.09 |
| Test suite (unit) | 10k | 3k | 70% | $0.07 |
| Test suite (integration) | 15k | 5k | 70% | $0.11 |
| Security review / CSO | 20k | 4k | 70% | $0.09 |
| QA report | 12k | 3k | 70% | $0.07 |

**Cost formula per task:**
```
cost = (input_tokens × 0.000003 × (1 - cache_hit × 0.9)) + (output_tokens × 0.000015)
```

**Multi-turn adjustment:** complex tasks spawn multiple agent turns; multiply base cost × turns (typically 2–5 turns per task for senior-dev).

**Project total cost rule:**
- PoC: aim for < $1 total
- MVP: aim for < $5 total
- Full: < $20 per feature; flag if > $50/feature

Always show: `Total LLM cost estimate: $X.XX (optimistic) – $X.XX (pessimistic)` in the plan summary.

---

## Human equivalent cost model

> Used for the LLM vs Human cost comparison in every PLAN doc.
> Rates are mid-senior US market (2026). Adjust for local market by applying a multiplier.

### Role rates (USD/hour)

| Role | Rate/h | Used for |
|------|--------|----------|
| Solutions Architect | $200 | architect tasks (architecture, ADRs) |
| Senior Backend Dev | $150 | SCHEMA, API, SVC tasks |
| Senior Frontend Dev | $130 | UI tasks |
| ML / AI Engineer | $180 | LLM tasks |
| DevOps Engineer | $120 | INFRA tasks |
| QA Engineer | $80 | TEST tasks |
| Security Engineer | $200 | CSO, SEC tasks |
| Project Manager (human) | $120 | PM planning tasks |

### Human hours per task type (mid estimate)

| Task type | Role | Human hours | Human cost |
|-----------|------|-------------|------------|
| Schema / data model | Backend Dev | 2–4h | $300–600 |
| API endpoint (CRUD) | Backend Dev | 3–6h | $450–900 |
| API endpoint (auth/billing) | Backend Dev | 6–12h | $900–1,800 |
| Frontend component | Frontend Dev | 2–4h | $260–520 |
| Frontend page (with API) | Frontend Dev | 4–8h | $520–1,040 |
| Background job / worker | Backend Dev | 4–8h | $600–1,200 |
| LLM integration (simple) | ML Engineer | 4–8h | $720–1,440 |
| LLM agent (tool-using) | ML Engineer | 12–24h | $2,160–4,320 |
| Infrastructure (basic) | DevOps | 2–4h | $240–480 |
| Infrastructure (cloud) | DevOps | 6–16h | $720–1,920 |
| Test suite (unit) | QA Engineer | 2–4h | $160–320 |
| Test suite (integration) | QA Engineer | 4–8h | $320–640 |
| Security review / CSO | Security Eng | 4–16h | $800–3,200 |
| Architecture (architect) | Architect | 4–8h | $800–1,600 |
| PM planning (human PM) | PM | 3–8h | $360–960 |
| QA report | QA Engineer | 2–4h | $160–320 |

### Cost and time comparison formula

```
# Time
llm_time_total   = sum(llm_minutes_per_task)              # wall-clock agent compute
human_time_total = sum(human_hours_mid × 60) × 1.3       # +30% coordination overhead
time_savings     = human_time_total / llm_time_total      # e.g. 80x faster

# Cost
llm_cost_total   = sum(token_cost_per_task × avg_turns)
human_cost_total = sum(human_hours_mid × role_rate) × 1.3
cost_savings     = human_cost_total / llm_cost_total      # e.g. 3,000x cheaper
savings_usd      = human_cost_total - llm_cost_total
```

**Expected savings range:**

| Mode | LLM time | Human time | Time savings | LLM cost | Human cost | Cost savings |
|------|----------|------------|--------------|----------|------------|--------------|
| PoC | 30–90 min | 40–120h | ~50–80x faster | $0.50–2 | $5K–15K | ~3,000–10,000x |
| MVP | 2–6h | 200–600h | ~60–100x faster | $2–8 | $15K–50K | ~3,000–10,000x |
| Full | 4–16h | 500h–2,000h | ~60–100x faster | $5–25 | $30K–150K | ~3,000–10,000x |

Note: human estimate includes coordination overhead (+30%: meetings, review cycles, context-switching, handoffs).
LLM estimate is pure token cost. No idle time, no context-switching penalty, no vacation, no meetings.

---

## Parallelism rules

### Can run in parallel (independent)
- Tasks that own disjoint files (no shared modules)
- Test writing after implementation of the same component (different files)
- Documentation and implementation
- Multiple API endpoints with no shared state
- Multiple frontend components with no shared context/store
- Infrastructure provisioning and application code (when no circular dep)

### Must be sequential (dependent)
- Schema migration → API layer (API reads schema)
- API layer → frontend (frontend calls API)
- Auth system → any endpoint behind auth
- CI pipeline → deploy (CI must pass first)
- `gate:plan` → senior-dev tasks (human must approve plan)
- `gate:arch` → PM plan (plan reads approved ARCH)
- LLM prompt → eval harness (harness tests the prompt)
- Any P0 security fix → next feature work

### Parallel signal in ARCH doc
Look for these patterns in ARCH doc to identify parallel-safe tasks:
```
"independent modules", "separate service", "separate route",
"no shared state", "stateless", "orthogonal"
```

---

## Agent allocation matrix

| Concurrency | When to use | Example |
|-------------|-------------|---------|
| 1 agent | PoC / sequential chain / nano project | Single senior-dev, one task at a time |
| 2–3 agents | MVP with 2+ independent modules | Frontend + backend in parallel |
| 4–6 agents | Full project with multiple services | API + worker + auth + frontend + tests |
| 7+ agents | Large enterprise / monorepo | Rare — coordination overhead exceeds benefit |

**Per-task agent recommendation:**
- Simple CRUD endpoint: 1 senior-dev
- Complex feature (auth + API + frontend): 1 senior-dev (sequential) or 2 (split by layer)
- Service-level work: 1 dedicated senior-dev per service
- Test suite: 1 qa-engineer (after all impls complete for a module)
- Security pass: 1 security-officer (after QA, before gate:ship)
- Each `gate:*`: 0 agents (human decision point)

---

## Gantt diagram format (Mermaid)

```
gantt
    title <Project Name> — <Mode> Plan
    dateFormat  YYYY-MM-DD
    axisFormat  %m/%d

    section Architecture
    gate:arch (human approval)    :crit, milestone, gate_arch, 2024-01-01, 0d
    
    section Foundation
    DB schema migration           :done,  t1, after gate_arch, 2h
    Auth service scaffold         :       t2, after gate_arch, 3h

    section API Layer
    POST /api/users               :       t3, after t1, 2h
    GET  /api/users               :       t4, after t1, 1h

    section Frontend
    Login page                    :       t5, after t3, 3h
    Dashboard page                :       t6, after t4, 4h

    section QA + Security
    QA report                     :       qa, after t5 t6, 1h
    Security review (CSO)         :       cso, after qa, 45m
    gate:ship (human approval)    :crit, milestone, gate_ship, after cso, 0d
```

**Rendering:** Mermaid renders in GitHub, Notion, and Claude Code preview. Always generate mermaid block + ASCII fallback table.

---

## ASCII Gantt fallback (when Mermaid can't render)

```
TASK                          │ D1  │ D2  │ D3  │ D4  │ D5  │
──────────────────────────────┼─────┼─────┼─────┼─────┼─────┤
[GATE] gate:arch              │ ●   │     │     │     │     │
DB schema                     │ ███ │     │     │     │     │
Auth scaffold                 │ ███ │     │     │     │     │
POST /api/users               │     │ ██  │     │     │     │
GET  /api/users               │     │ █   │     │     │     │
Login page         (parallel) │     │ ███ │     │     │     │
Dashboard page     (parallel) │     │     │ ████│     │     │
QA report                     │     │     │     │ ██  │     │
Security CSO                  │     │     │     │  ██ │     │
[GATE] gate:ship              │     │     │     │     │ ●   │
```

`●` = human gate (wait for approval)  
`███` = agent work  
`(parallel)` = multiple agents active simultaneously

---

## PLAN-*.md artefact schema

```markdown
# PLAN-<feature-slug>.md

## Mode
poc | mvp | full

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | N (incl. 2 gates) |
| Parallel pools | N |
| Max concurrent agents | N |
| LLM compute time | Xmin–Xmin (critical path, excl. gates) |
| Gate wait budget | ~6h (3 gates × 2h async) |
| **LLM cost estimate** | **$X.XX – $X.XX** (optimistic / pessimistic) |
| **Human equivalent** | **$X,XXX – $X,XXX** (mid-senior US rates) |
| **Savings** | **~XXXx cheaper** |

## Dependency graph
task-1 → task-2 → task-4
task-1 → task-3 (parallel with task-2) → task-4

## Gantt
<mermaid gantt block>

## Task breakdown

| ID | Task | Type | Agent | Model | Deps | LLM time | Token cost | Human equiv |
|----|------|------|-------|-------|------|----------|------------|-------------|
| T1 | DB schema | SCHEMA | senior-dev | Sonnet | gate:arch | 15min | $0.04×3t=$0.12 | $300–600 |
| T2 | Auth service | SVC | senior-dev | Sonnet | T1 | 30min | $0.09×4t=$0.36 | $900–1,800 |
| T3 | POST /users | API | senior-dev | Sonnet | T1 | 10min | $0.05×3t=$0.15 | $450–900 |
| T4 | GET /users | API | senior-dev | Sonnet | T1 | 10min | $0.05×2t=$0.10 | $450–900 |
| T5 | QA report | TEST | qa-engineer | Haiku | T3 T4 | 15min | $0.01×2t=$0.02 | $160–320 |
| — | architect | ARCH | architect | Opus | — | 20min | $0.50 | $800–1,600 |
| — | pm | PLAN | pm | Sonnet | gate:arch | 15min | $0.15 | $360–960 |

`t` = agent turns

## Agent pools

**Pool A** (sequential chain): T1 → T2 → T5  ← 1 senior-dev
**Pool B** (parallel): T3 ∥ T4              ← 1–2 senior-devs

Minimum agents needed: 2 senior-dev + 1 qa-engineer

## Gates

| Gate | After | Blocks |
|------|-------|--------|
| gate:arch | Architecture approval | All implementation |
| gate:plan | Plan approval | senior-dev Pool A + B |
| gate:ship | QA + security pass | Deploy |

## Cost comparison: LLM agents vs Human team

|  | LLM agents | Human team |
|--|-----------|------------|
| **Total time** | ~Xmin (agent compute) | ~Xh (calendar, excl. nights/weekends) |
| **Cost (optimistic)** | $X.XX | $X,XXX |
| **Cost (pessimistic)** | $X.XX | $X,XXX |
| **Time savings** | — | ~XXx faster |
| **Cost savings** | — | ~XXXx cheaper · ~$X,XXX saved |

**LLM time + cost breakdown:**
| Agent | Time | Cost |
|-------|------|------|
| architect | ~Xmin | $X.XX (Opus 4.8) |
| pm | ~Xmin | $X.XX (Sonnet 4.6) |
| senior-dev (N tasks) | ~Xmin | $X.XX (Sonnet 4.6) |
| qa-engineer | ~Xmin | $X.XX (Haiku 4.5) |
| security-officer | ~Xmin | $X.XX (Sonnet 4.6) |
| devops | ~Xmin | $X.XX (Haiku 4.5) |
| **Total** | **~Xmin** | **$X.XX** |

**Human time + cost breakdown:**
| Role | Hours | Rate | Cost |
|------|-------|------|------|
| Solutions Architect | Xh | $200/h | $XXX |
| Backend Dev | Xh | $150/h | $XXX |
| Frontend Dev | Xh | $130/h | $XXX |
| QA Engineer | Xh | $80/h | $XXX |
| Security Eng | Xh | $200/h | $XXX |
| DevOps | Xh | $120/h | $XXX |
| Coordination overhead (+30%) | — | — | $XXX |
| **Total** | **~Xh** | — | **$X,XXX** |

> Rates: mid-senior US market 2026.
> Human hours include coordination overhead (meetings, review cycles, context-switching, handoffs).
> LLM cost = token cost only. No salary, no benefits, no idle time between tasks.

## Risks
- T2 (auth) may expand if OAuth provider API changes → +50% buffer on T2
- T5 (QA) may find regressions in T3/T4 → loop back estimated 30min

## Revision history
v1 — <date> — initial plan
```
