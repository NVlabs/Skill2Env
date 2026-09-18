---
name: ARCH-ai
description: Mandatory ARCH document template for AI/agent projects: Trust Boundaries, LLM Scope (deterministic vs LLM-decided), Failure Modes (≥5 from OWASP LLM Top 10), Cost Model, Kill-switch, Eval set, Security section
when_to_use: Writing ARCH-{slug}.md for ai-system or agent-product archetype. Required by architect Step 0a + SECURITY_REQUIRED block
applies_to:
  - ai-system
  - agent-product
---

# ARCH-{slug}.md — AI/Agent project template

> **Reader:** the engineer joining this project in 6 months. Be exact about what is deterministic and what the LLM decides.
> **Source:** `skills/great_cto/templates/ARCH-ai.md`. Mandatory for `archetype: ai-system | agent-product`.
> Required by `architect.md` Step 0a + SECURITY_REQUIRED block. Cannot ship to production without `## Security`.

## Decision (one sentence)
{What architecture will we build, in plain language, for the named reader.}

## Trust Boundaries
| Boundary | What crosses it | Untrusted? | Sanitisation |
|---|---|---|---|
| User → API | request body, auth header | yes | schema validation, rate limit, auth |
| API → LLM | system prompt + user input + retrieved context | **input**: yes; **system prompt**: trusted | prompt-injection filter on user input; sandbox retrieved content |
| LLM → tool layer | tool name + JSON args | yes (LLM is hostile to system prompt) | tool allowlist, arg schema, scope check |
| Tool → external API | per-tool credentials | varies | per-user OAuth (not service account) |
| External → LLM (RAG) | retrieved documents | **yes** | sandbox content as data, not instructions |

Every "yes" row above must have a mitigation in `## Security` AND a test case in `tests/eval/EVAL-*.md`.

## LLM Scope — what the model decides vs deterministic code
| Decision | Where it happens | Why |
|---|---|---|
| {e.g. classify intent} | LLM | needs flexible NL understanding |
| {e.g. format response} | LLM | template-style generation |
| {e.g. compute price} | code | determinism + audit trail required |
| {e.g. send email} | code (with LLM-generated draft + human confirm) | irreversible action |
| {e.g. run SQL} | code (parameterised), LLM only suggests intent | injection risk |

Default rule: **if it touches money, identity, irreversible state, or compliance — it's deterministic code, not the LLM**.

## Failure Modes (≥ 5 — derived from agent-pack OWASP LLM Top 10)
| # | Mode | Probability × Impact | Detection | Mitigation | Tested in |
|---|---|---|---|---|---|
| F1 | Prompt injection via user input | M × H | output filter, eval suite | input sanitisation + system-prompt isolation | EVAL-prompt-injection.md |
| F2 | Prompt injection via retrieved content (RAG poisoning) | M × H | output filter, anomaly detection | sandbox content as data, never as instructions | EVAL-rag-poisoning.md |
| F3 | Tool misuse (LLM calls wrong tool / wrong args) | H × M | output schema validation | tool allowlist + arg schema enforcement | EVAL-tool-misuse.md |
| F4 | Cost runaway (loop / large context) | M × M | per-session BudgetTracker | MAX_ITERATIONS, asyncio.timeout, budget cap | EVAL-budget-overrun.md |
| F5 | Hallucination on factual claims | H × M | citation requirement, refuse-when-uncertain prompt | RAG with source links + grounded-answer eval | EVAL-citation.md |
| F6 | Cross-user data leak (multi-tenant) | L × H | isolation test in CI | per-user namespace at repo layer | EVAL-cross-user-isolation.md |

## Cost Model
| Item | Per-call | Daily volume | Monthly | Notes |
|---|---|---|---|---|
| LLM input (gpt-4o-mini @ $0.15/1M tokens) | ~$0.0001 | 10k calls | ~$30 | tokens × rate |
| LLM output | ~$0.0006 | 10k × 200 tokens | ~$120 | streamed |
| Vector DB (Pinecone / pgvector) | n/a | n/a | $50 | fixed |
| **Total estimate** | | | **$200/mo** | |
| **Cap (`monthly-budget-llm-usd`)** | | | **$300/mo** | 50% headroom; project-auditor flags P0 if exceeded |

## Kill-switch
**Who:** {role / on-call rotation}
**How:** {feature flag / config change / API key revoke / wholesale shutoff endpoint}
**Time to stop:** {target ≤ N minutes from decision}
**Tested:** {date of last drill}

## Eval set — minimum scenarios
- `tests/eval/EVAL-citation.md` — golden grounding cases
- `tests/eval/EVAL-refuse-when-uncertain.md` — model says "I don't know" instead of fabricating
- `tests/eval/EVAL-output-schema.md` — model output validates against expected JSON schema
- `tests/eval/EVAL-prompt-injection.md` — Garak suite or custom 50-prompt set, **0 bypasses**
- `tests/eval/EVAL-budget-overrun.md` — runaway loop hits cost cap and stops cleanly

For `agent-product`: add `EVAL-cross-user-isolation.md` and `EVAL-tool-misuse.md`.

## Out of scope (explicit)
- {e.g. Real-time streaming — phase 2}
- {e.g. Image input — needs separate ARCH}
- {e.g. Fine-tuning — vendor model only}

## Security
> **Mandatory for ai-system / agent-product.** Cross-link `docs/sec-threats/TM-{slug}.md`.

- **Prompt-injection** vector covered: input sanitisation + retrieved-content sandboxing + output filter (Llama Guard 3 / Anthropic safety) — see `THREAT-MODEL-AI.md` § Prompt Injection
- **Output exfiltration**: regex + NER filter on every output for PII / SSN / API keys / internal hostnames before returning to user
- **Tool sandboxing**: LLM-suggested URLs run through allowlist (scheme + port + IP range); `requests.get` taking LLM output is P0 flag
- **Cost runaway**: BudgetTracker per session ($0.50 default, $5 max); MAX_ITERATIONS=20; asyncio.timeout=300s
- **Cross-user isolation** (agent-product only): repository layer enforces `WHERE user_id = :ctx.user_id`; never prompt-level
- **Supply chain**: model pinned to specific version, evaluator runs on every prompt change
- **Audit log**: every tool call recorded with `(user_id, server, tool, params_hash, result_hash, latency_ms)`, PII redacted, 90-day retention

## Safeguards ← senior-dev reads before writing any code; security-officer cross-checks at CSO

> Non-negotiable invariants for this AI/agent feature.

### LLM safety
- [ ] User input sanitised (strip injection patterns) before passing to LLM
- [ ] No PII in prompts without explicit consent gate
- [ ] Per-request token budget enforced — hard cap, not soft warn
- [ ] Output filter active (Llama Guard / Anthropic safety API / custom classifier)

### Cost & abuse
- [ ] Per-user monthly spend cap enforced at request layer — not just dashboard alert
- [ ] BudgetTracker called before every LLM invocation; reject if over limit
- [ ] Anomaly threshold: >10× p95 token count → auto-block + alert

### Data isolation
- [ ] Every memory/vector operation scoped by `tenant_id` — no cross-user leakage
- [ ] Tool outputs never stored in shared context without sanitisation

### Auditability
- [ ] Every tool call logged: `(user_id, tool, params_hash, result_hash, latency_ms)` — PII redacted
- [ ] Eval suite gate: ≥3 EVAL-*.md scenarios must pass before gate:ship

## Open questions
- {Items the maintainer must decide before next ARCH revision}
