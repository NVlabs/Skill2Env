---
name: hr-ai-pack
description: HR-AI / AI-recruiting overlay. Pairs hr-ai-reviewer.
when_to_use: Product makes employment-related decisions — hiring, screening, interview analysis, performance review, workforce management.
applies_to:
  - ai-system
  - agent-product
  - enterprise
extends:
  - ai-pack
---

# HR-AI Compliance Pack

> Loaded when ARCH mentions: recruit, hiring, candidate, resume, interview, ATS, talent, performance review, workforce scheduling.

## Reviewer

- **hr-ai-reviewer** → `TM-hrai-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:aedt-audit` | Annual (NYC LL 144) bias-audit report | Independent auditor |
| `gate:ship` | Standard | security-officer |

## Required artefacts

| Artefact | Owner |
|---|---|
| AEDT applicability assessment (NYC LL 144 in/out) | architect |
| Bias-audit pipeline (4/5-rule, intersectional) | ai-eval-engineer |
| Candidate 10-day pre-use notice template | senior-dev |
| Per-decision explainability record (retained for FOIA) | senior-dev |
| Disability-accommodation alternative path | architect |
| Resume-PDF prompt-injection guardrail | ai-security-reviewer |
| GDPR Art. 22 human-review request workflow | senior-dev |
| Annual third-party auditor engagement | regulatory-lead |

## EVAL suite

- `EVAL-bias-by-protected-class` (4/5-rule on sex × race intersectional)
- `EVAL-explainability-completeness` (per-decision rationale present)
- `EVAL-resume-injection` (PDF jailbreak via uploaded CV)
- `EVAL-opt-out-honored` (candidate refused AI → not used)
- `EVAL-disability-accommodation` (alternative path triggered correctly)

## State / region applicability quick matrix

| Region | Regulation | Trigger |
|---|---|---|
| NYC | LL 144 AEDT | Hiring/promotion AI for NYC role or NYC resident |
| Illinois | AIVIA | AI analysis of video interview |
| Colorado | SB 205 (Feb 2026) | "High-risk AI" employment use |
| Maryland | HB 1202 | Facial recognition in pre-employment |
| EU | AI Act Annex III | Any employment-decision AI (Aug 2026) |
| Globally | GDPR Art. 22 | Solely-automated employment decisions |
