---
name: TISAX-VDA-ISA-results
description: TISAX VDA ISA assessment results: Information Security + Prototype Protection + Data Protection objectives. Maturity scale 0-5 across 9 chapters. AL1/AL2/AL3 levels
when_to_use: Compliance documentation for regulated archetype with compliance:[tisax]. Required for automotive supply chain (BMW/Mercedes/VW/Audi suppliers)
applies_to:
  - regulated
---

# TISAX-VDA-ISA-results.md — Trusted Information Security Assessment Exchange

> Mandatory artefact when `compliance: [tisax]` in PROJECT.md.
> Required by `architect.md` compliance artefact gate.
> Required for automotive supply chain (BMW, Mercedes, Volkswagen, Audi, etc.). Based on VDA ISA (Information Security Assessment) catalogue.
> Source: `skills/great_cto/templates/TISAX-VDA-ISA-results.md`.

## Assessment scope
- Locations: {sites in scope}
- Assessment level (AL):
  - **AL1** — self-assessment (low protection need)
  - **AL2** — plausibility check by 3rd-party auditor (high protection need)
  - **AL3** — site audit (very high protection need / prototype protection / data with personal-data classification HIGH)
- Selected: {AL1 / AL2 / AL3}
- Audit provider: {ENX-listed audit provider}
- Last assessment date: {date}
- Next due: {date+3y}

## Objectives in scope
| Objective | Required level | Status |
|---|---|---|
| Information Security | yes | __ |
| Prototype Protection | {if handling pre-series prototypes} | __ |
| Data Protection (GDPR) | {if processing personal data on behalf of OEM} | __ |

## VDA ISA catalogue results (condensed)

| Chapter | Maturity target | Current maturity | Gap |
|---|---|---|---|
| 1. IS Policies and Organization | 3 | __ | __ |
| 2. Human Resources Security | 3 | __ | __ |
| 3. Physical Security and Business Continuity | 3 | __ | __ |
| 4. Identity and Access Management | 3 | __ | __ |
| 5. IT Security / Cyber Security | 3 | __ | __ |
| 6. Supplier Relationships | 3 | __ | __ |
| 7. Compliance | 3 | __ | __ |
| 8. Prototype Protection (if applicable) | 3 | __ | __ |
| 9. Data Protection (if applicable) | 3 | __ | __ |

Maturity scale: 0 (incomplete) → 1 (performed) → 2 (managed) → 3 (established) → 4 (predictable) → 5 (optimizing).

## Findings + corrective actions
| Control # | Finding severity | Description | Action | Due | Owner |
|---|---|---|---|---|---|
| 1.2.4 | major | {description} | {action} | {date} | {role} |

## Label issued
- Label: {Information Security Standard / Prototype Protection / etc.}
- Validity: 3 years from assessment date
- ENX portal entry: {URL}

## Sign-off
| Role | Name | Date |
|---|---|---|
| Information Security Officer | | |
| Audit lead (ENX provider) | | |
| Management | | |
