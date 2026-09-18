---
name: ADR-PROMPT
description: ADR template for system prompt versioning: full prompt text, sha256 hash for CI drift detection, why each instruction is there, what's deliberately NOT in the prompt, eval coverage per prompt, revision history
when_to_use: Versioning system prompts for any LLM role (extractor, summariser, agent, classifier). Required by ai-prompt-architect output
applies_to:
  - ai-system
  - agent-product
---

# ADR-{NN}-PROMPT-{name}.md — System prompt versioning

> Records the system prompt for a named role (extractor, summariser, agent, classifier). Every prompt change ships as a new ADR or appended revision to keep eval-suite results meaningful.
> Source: `skills/great_cto/templates/ADR-PROMPT.md`.

## Status
{Proposed | Active | Superseded by ADR-NN}

## Context
- Role: {extractor / summariser / agent / classifier}
- Used by: {file path / endpoint / agent name}
- Linked model: `ADR-{NN}-LLM-{model}.md`

## Prompt v{X.Y.Z}

```text
{Full system prompt — exact text the model sees, no placeholders.}
```

**Hash:** `{sha256 of the prompt above — used by CI to detect drift}`

**Length:** {N tokens / M characters}

## Why these instructions
| Instruction | Why it's there |
|---|---|
| {e.g. "Always cite sources"} | grounds output, mitigates hallucination (per TM § F5) |
| {e.g. "Never run shell commands"} | bounds tool use (per TM § F3) |
| {e.g. "If uncertain, say 'I don't know'"} | refuse-when-uncertain, tested in `EVAL-refuse.md` |
| {e.g. "Output JSON matching this schema..."} | output schema stability, tested in `EVAL-schema.md` |

## What's deliberately NOT in the prompt
- Negotiable tone instructions ("be friendly") — leave to user prompt; system prompt is authority-only
- Brand voice (handled at output filter or post-processing)
- Language switching (handled by deterministic code based on user locale)

## Eval coverage for this prompt

| Eval file | What it tests |
|---|---|
| `tests/eval/EVAL-citation.md` | every claim has a source |
| `tests/eval/EVAL-refuse.md` | model says "I don't know" instead of fabricating |
| `tests/eval/EVAL-output-schema.md` | output validates against schema |
| `tests/eval/EVAL-prompt-injection.md` | role override resistance |
| {add per scenario} | |

## Revision history

| Date | Version | Hash | Changed | Eval impact | Reviewer |
|---|---|---|---|---|---|
| {YYYY-MM-DD} | 1.0.0 | {hash} | initial | baseline | {who} |
| {YYYY-MM-DD} | 1.1.0 | {hash} | added "cite sources" | EVAL-citation pass-rate up 88→97% | {who} |

## CI enforcement

`great_cto` CI hook compares the prompt hash on every PR. If the prompt text changes:
1. New ADR-PROMPT entry required (or revision row above)
2. Full eval suite must run
3. Any regression → block merge OR document as accepted in this ADR

This prevents the silent-prompt-drift failure mode where someone edits the prompt and breaks 3 eval cases that go unnoticed for 6 weeks.
