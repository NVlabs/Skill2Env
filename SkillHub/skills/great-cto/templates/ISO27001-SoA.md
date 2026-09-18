---
name: ISO27001-SoA
description: ISO/IEC 27001:2022 Statement of Applicability per clause 6.1.3(d): Annex A 93 controls (Organizational/People/Physical/Technological), applicability + justification per control + risk register cross-reference
when_to_use: Compliance documentation for regulated archetype with compliance:[iso27001]. Required for ISMS certification
applies_to:
  - regulated
---

# ISO27001-SoA.md — Statement of Applicability

> Mandatory artefact when `compliance: [iso27001]` in PROJECT.md.
> Required by `architect.md` compliance artefact gate.
> ISO/IEC 27001:2022 — clause 6.1.3(d). The Statement of Applicability declares which Annex A controls are applicable, which are excluded, and the justification.
> Source: `skills/great_cto/templates/ISO27001-SoA.md`.

## ISMS scope
- Organisation: {legal name}
- Sites: {locations in scope}
- Information assets: {high-level list — see asset register}
- Exclusions: {what is OUT of scope and why}
- ISMS owner: {role / person}
- Version: {N} | Approved: {date}

## Annex A 2022 controls (93 controls in 4 themes)

### A.5 Organizational controls (37 controls)
| Control | Title | Applicable | Reason if excluded | Implementation reference | Status |
|---|---|---|---|---|---|
| 5.1 | Policies for information security | yes | — | `policy-isms.md` | implemented |
| 5.2 | Information security roles and responsibilities | yes | — | `org-chart.md` | implemented |
| 5.3 | Segregation of duties | yes | — | `access-matrix.md` | implemented |
| 5.4 | Management responsibilities | yes | — | board minutes | implemented |
| 5.5 | Contact with authorities | yes | — | `incident-runbook.md` | implemented |
| 5.6 | Contact with special interest groups | yes | — | ISAC membership | implemented |
| 5.7 | Threat intelligence | yes | — | `tip-feed.md` | implemented |
| 5.8 | Information security in project management | yes | — | this template | implemented |
| ... | (continue through 5.37) | | | | |

### A.6 People controls (8 controls)
| 6.1 | Screening | yes | — | HR onboarding | implemented |
| 6.2 | Terms and conditions of employment | yes | — | employment contracts | implemented |
| 6.3 | Information security awareness, education and training | yes | — | training records | implemented |
| 6.4 | Disciplinary process | yes | — | HR policy | implemented |
| 6.5 | Responsibilities after termination or change of employment | yes | — | leaver process | implemented |
| 6.6 | Confidentiality or non-disclosure agreements | yes | — | NDA template | implemented |
| 6.7 | Remote working | yes | — | remote work policy | implemented |
| 6.8 | Information security event reporting | yes | — | `incident-runbook.md` | implemented |

### A.7 Physical controls (14 controls)
| 7.1 | Physical security perimeters | yes/no | {if cloud-only: "exclusion — cloud provider responsible per shared responsibility model"} | | |
| ... | | | | | |

### A.8 Technological controls (34 controls)
| 8.1 | User endpoint devices | yes | — | MDM policy | implemented |
| 8.2 | Privileged access rights | yes | — | PAM tooling | implemented |
| 8.3 | Information access restriction | yes | — | RBAC + ABAC | implemented |
| 8.4 | Access to source code | yes | — | git access policy | implemented |
| 8.5 | Secure authentication | yes | — | MFA enforcement | implemented |
| 8.6 | Capacity management | yes | — | monitoring + autoscale | implemented |
| 8.7 | Protection against malware | yes | — | endpoint AV / EDR | implemented |
| 8.8 | Management of technical vulnerabilities | yes | — | CVE scanning + patch SLA | implemented |
| 8.9 | Configuration management | yes | — | IaC + drift detection | implemented |
| 8.10 | Information deletion | yes | — | crypto-shredding policy | implemented |
| 8.11 | Data masking | yes/no | | | |
| 8.12 | Data leakage prevention | yes | — | DLP tooling | implemented |
| ... | (continue through 8.34) | | | | |

## Risk assessment cross-reference
For each "applicable: yes", risk register entry: `docs/compliance/risk-register.md` row R-NN.

## Internal audit + management review
- Last internal audit: {date} — findings: `docs/audit/iso27001-{date}.md`
- Last management review: {date}
- Next surveillance audit (external): {date}
- Certification body: {body name}
- Certificate number: {if certified}
- Certificate validity: {date — date+3y}

## Sign-off
| Role | Name | Date |
|---|---|---|
| ISMS Owner | | |
| CISO | | |
| Top Management | | |
