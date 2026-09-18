---
name: llm-router
description: LLM router config (OpenRouter / Kimi K2): when to delegate to cheaper models, fallback chains, observability, $/token tracking
when_to_use: Cost-optimised AI workflows. Read by architect + senior-dev when LLM-cost is material
applies_to:
  - ai-system
  - agent-product
---

# LLM Router (OpenRouter / Kimi K2)

A zero-dependency MCP server that lets specific great_cto agents delegate
routine work to a cheap model (Kimi K2 via OpenRouter) instead of burning
Sonnet/Opus tokens. Optional — the pipeline works fully without it.

## Why

Anthropic tokens are the single largest cost of running great_cto on an
active project. Most agent calls genuinely need Sonnet — architecture
decisions, TDD code generation, security review. But ~20–30% of the work
is **grunt work**: summarizing 10k lines of logs, generating boilerplate
smoke tests for a POC, rewriting a commit list into a digest paragraph.

Routing that grunt work to Kimi K2 (≈ 5–6× cheaper per token) saves real
money without compromising the critical path.

## What it is NOT

- Not a Sonnet replacement. Architecture, security, production code
  generation stay on native Claude.
- Not automatic. Each agent that uses the router does so **explicitly**
  via `mcp__great_cto_llm_router__ask_kimi`, in documented situations.
- Not a fallback for outages. If OpenRouter is down, the tool returns a
  `fallback` signal and the caller does the task natively.

## Setup

One-time, per machine or per project:

```bash
# Preferred — per-project secret, git-ignored:
echo "OPENROUTER_API_KEY=sk-or-v1-..." >> .env.local

# Or user-wide:
mkdir -p ~/.great_cto
echo "OPENROUTER_API_KEY=sk-or-v1-..." >> ~/.great_cto/secrets.env
chmod 600 ~/.great_cto/secrets.env
```

Get a key at <https://openrouter.ai/keys>. Top up $5–10 to start.

Restart Claude Code session — the MCP server reads env vars on start.

Verify: `/doctor` → "LLM router: ✓ key live".

## Config (env vars)

| Var | Default | Notes |
|---|---|---|
| `OPENROUTER_API_KEY` | (none) | required to enable |
| `GREAT_CTO_ROUTER_MODEL` | `moonshotai/kimi-k2` | any OpenRouter model slug |
| `GREAT_CTO_ROUTER_MAX_TOKENS` | `4096` | output cap |
| `GREAT_CTO_ROUTER_TIMEOUT` | `60` | seconds |

To use a different cheap model, e.g. DeepSeek or Mistral Large:
```
GREAT_CTO_ROUTER_MODEL=deepseek/deepseek-chat
```

## Which agents use it, and when

| Agent / command | When to delegate | When to NOT |
|---|---|---|
| `l3-support` | routine log triage, error clustering, stack-trace summarization | P0/P1 reasoning, postmortem writing, root-cause synthesis |
| `senior-dev` | POC-mode smoke tests, boilerplate scaffolding | MVP/production code, refactors, security-sensitive code |
| `qa-engineer` | POC-mode smoke generation, test-name brainstorming | production QA plan, bug triage, regression analysis |
| `/digest` | (reserved, future) commit-log summarization for weekly report | cost/DORA calculations — deterministic, no LLM needed |

**Never delegate**: `architect` (architecture), `security-officer` (CSO),
`devops` (deploy reasoning), `/audit` (depends on deterministic lints).

## Tool contract

```jsonc
// Call
{
  "name": "ask_kimi",
  "arguments": {
    "task": "Summarize these 8k lines of NGINX access logs — cluster by status code and path prefix.",
    "context": "<log content, ≤20k chars>",
    "system": "optional persona override"
  }
}

// Success response (text content)
// [model=moonshotai/kimi-k2 tokens=3210 elapsed=2.4s]
//
// <model output>

// Fallback response (text content, JSON-shaped)
// {"error": "OPENROUTER_API_KEY not set", "fallback": "caller must use native Claude reasoning"}
```

Rule: if `fallback` is present in the response, **do the task natively and
move on** — do not prompt CTO for setup, do not block the pipeline.

## Cost tracking

Every successful call appends a JSONL record to
`.great_cto/llm-router-usage.log`. `/digest` reads this and reports:

```
LLM ROUTER
  Calls: 42 | Tokens: 1,280,000
  Kimi spend: $0.52 | Sonnet-equiv: $3.40 | Saved: $2.88
```

`/doctor` also pings OpenRouter `/auth/key` to show live quota.

## Security

- `.env.local` must be in `.gitignore` — `/start` enforces this, `/doctor`
  warns if it's not.
- senior-dev credential-scan recognizes OpenRouter keys
  (`sk-or-v1-[a-f0-9]{32,}`) and blocks them from being written to code
  or committed files.
- Context passed to Kimi is observable by OpenRouter. Do **not** pass
  production secrets, PII, or customer data through the router. If the
  log you're triaging contains secrets, redact first or do triage
  natively.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `/doctor` says "not configured" after I set the key | session not restarted | exit Claude Code, reopen |
| "HTTP 401" from router | key wrong or revoked | rotate at openrouter.ai/keys |
| "HTTP 402" | out of credits | top up at openrouter.ai |
| Model not found | wrong slug | check <https://openrouter.ai/models> |
| Slow responses | Kimi K2 under load | raise `GREAT_CTO_ROUTER_TIMEOUT` or switch model |

## When NOT to use the router at all

- Single-person project shipping one feature a week — savings are rounding
  error, not worth the setup.
- Strict compliance env (HIPAA, PCI) where third-party LLMs outside your
  BAA are disallowed.
- Offline / air-gapped dev — router needs the internet.

In any of these — skip it. Pipeline runs identically.
