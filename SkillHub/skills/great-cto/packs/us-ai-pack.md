---
name: us-ai-pack
description: US AI-governance overlay (US analogue of EU AI Act). Pairs us-ai-reviewer.
when_to_use: Product makes/influences a consequential decision (employment, lending, housing, insurance, healthcare, education, legal) or is a generative-AI consumer feature, with US (esp. CO/UT/TX/CA) users.
applies_to:
  - ai-system
  - agent-product
  - enterprise-saas
  - healthcare
  - fintech
---

# US AI-Governance Pack

> Loaded when ARCH mentions: NIST AI RMF, Colorado AI Act / SB 205, algorithmic discrimination, consequential/automated decision, high-risk AI, Utah AI, TRAIGA, AB 2013, SB 942, AI disclosure, AI governance.

## Reviewer

- **us-ai-reviewer** → `TM-usai-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:ai-governance` | Pre-implementation — classification + state-duty mapping | security-officer |
| `gate:ship` | Standard | security-officer |

## Required artefacts

| Artefact | Owner |
|---|---|
| Consequential-decision / generative-consumer classification | architect |
| State applicability matrix (CO SB 205 / UT / TX / CA) | us-ai-reviewer |
| NIST AI RMF control map (GOVERN/MAP/MEASURE/MANAGE) | architect |
| CO SB 205: impact assessment + consumer notice + appeal-to-human path | senior-dev |
| Algorithmic-discrimination / bias testing | ai-eval-engineer |
| Generative-AI disclosure (UT/TX) | senior-dev |
| CA AB 2013 training-data documentation + SB 942 provenance | senior-dev |
