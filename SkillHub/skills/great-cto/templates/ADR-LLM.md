---
name: ADR-LLM
description: ADR template for LLM model selection: provider + version pinning (no floating tags), temperature, max tokens, fallback policy, alternatives considered, cost estimate, eval suite re-run on version change
when_to_use: Choosing LLM model for AI project. One ADR per primary model decision
applies_to:
  - ai-system
  - agent-product
---

# ADR-{NN}-LLM-{model}.md — LLM model selection

> Records the choice of LLM provider, model version, temperature, fallback policy. One ADR per primary model decision.
> Source: `skills/great_cto/templates/ADR-LLM.md`.

## Status
{Proposed | Accepted | Superseded by ADR-NN}

## Context
- Project: {name}
- Archetype: {ai-system | agent-product}
- Use case: {classification / generation / agentic tool use / RAG / summarization}
- Constraints: {latency target, monthly budget cap, data residency}

## Decision
We will use `{provider}/{model-version}` (e.g. `anthropic/claude-sonnet-4-6-20250615` or `openai/gpt-4o-2024-11-20`).

**Pinned to specific version**, not the floating tag. Floating tags (`gpt-4o`, `claude-3-5-sonnet`) silently upgrade and break our eval suite without notice.

| Parameter | Value | Why |
|---|---|---|
| Model version | `{exact-version}` | pinned for reproducibility |
| Temperature | `{0.0 / 0.3 / 0.7}` | {0.0 for classification & extraction; 0.3 for code; 0.7 for creative} |
| Max output tokens | `{N}` | bound cost and latency |
| Streaming | `{yes / no}` | UX requirement |
| Top-p | `{1.0 / 0.9}` | default unless tuned |
| Stop sequences | `{...}` | to prevent runaway |

## Alternatives considered

| Option | Pro | Con | Why rejected |
|---|---|---|---|
| `gpt-4o-mini` | 10× cheaper | weaker reasoning on multi-step | reasoning quality below threshold for our use case |
| `claude-haiku-4-5` | fast, cheap | smaller context | context too small for our RAG payload |
| `llama-3.3-70b` (self-hosted) | data residency | infra burden | team size 3, not infra-ready |

## Fallback policy

| Condition | Action |
|---|---|
| Provider 5xx / timeout > 30s | Retry once with exponential backoff |
| Provider quota exceeded | Fail over to `{secondary-provider}/{model}` (rate-limited per archetype) |
| Critical outage | Surface error to user, do not silently downgrade — model swaps shift behaviour |

## Cost estimate
- Per call: ~`{$0.00X}`
- Daily volume: ~`{N}` calls
- Monthly: ~`${N}` (within `monthly-budget-llm-usd: $X` set in PROJECT.md)

## Eval suite locked to this version
On model version change:
1. Update this ADR (mark old as Superseded)
2. Re-run full eval suite (`tests/eval/EVAL-*.md`) on new version
3. Block ship if any eval regresses; document accepted regressions in `## Regressions` below

## Regressions (filled when superseded)
| Eval | Before | After | Accepted? | Sign-off |
|---|---|---|---|---|
| | | | | |

## Compliance notes
- {EU AI Act check: is model on Annex III high-risk list? — record assessment}
- {Data residency: where does the provider process? GDPR?}
- {SOC 2 / ISO 27001 vendor evidence: link to VENDOR-{provider}.md}
