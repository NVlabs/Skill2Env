---
name: DORA-ICT-risk-assessment
description: EU Digital Operational Resilience Act ICT risk assessment per Article 6/8/11/17-23. Governance, risk framework, response/recovery, incident management + reporting (≤4h initial, ≤72h formal, ≤1mo final)
when_to_use: Compliance documentation for regulated archetype with compliance:[dora]. Required for EU financial entities
applies_to:
  - regulated
---

# DORA-ICT-risk-assessment.md — EU Digital Operational Resilience Act

> Mandatory artefact when `compliance: [dora]` in PROJECT.md.
> Required by `architect.md` compliance artefact gate — exits 1 if missing.
> DORA applies to financial entities (banks, investment firms, insurers, crypto-asset service providers) operating in the EU. Source: Regulation (EU) 2022/2554.
> Source: `skills/great_cto/templates/DORA-ICT-risk-assessment.md`.

## Scope
- Financial entity: {legal name + classification}
- Critical / Important Functions covered: {list of CIFs per Article 8}
- Reporting period: {YYYY-Q1 — YYYY-Q4}
- ICT risk register: `docs/compliance/DORA-ICT-risk-register.md`

## Article 6 — Governance and organisation
| Requirement | Owner | Evidence | Status |
|---|---|---|---|
| Management body has overall responsibility for ICT risk | CTO + CISO | board minutes ref | __ |
| ICT risk management framework documented and reviewed annually | CISO | this document | __ |
| Internal audit reviews framework | Internal Audit | last audit date / report ref | __ |

## Article 8 — ICT risk management framework
| Component | Description |
|---|---|
| Risk identification | per `docs/compliance/DORA-ICT-risk-register.md` |
| Protection & prevention | controls per Article 9 (encryption, segmentation, secure SDLC) |
| Detection | log monitoring, IDS/IPS, anomaly detection |
| Response & recovery | per Article 11, RTO/RPO documented per CIF |
| Learning & evolving | post-incident review process |

## Article 11 — Response and recovery
| CIF | RTO | RPO | DR site | Last failover test |
|---|---|---|---|---|
| {CIF name} | 4h | 15min | {region} | {date} |

## Article 17–23 — ICT-related incident management & reporting
- Incident classification matrix: `docs/compliance/DORA-incident-classification.md`
- Major incident threshold: {per Article 18 RTS criteria}
- Reporting timelines:
  - Initial notification: ≤ 4 hours from awareness
  - Intermediate report: ≤ 72 hours
  - Final report: ≤ 1 month
- National competent authority: {NCA name}
- Reporting channel: {portal URL / email}

## Article 24–27 — Digital operational resilience testing
| Test type | Frequency | Last performed | Next due |
|---|---|---|---|
| Vulnerability assessment | continuous (CI/CD) | ongoing | n/a |
| Penetration test | annual | {date} | {date+1y} |
| TLPT (Threat-Led Penetration Test, Article 26) | every 3 years (if classified by NCA) | {date or N/A} | {date or N/A} |
| Scenario-based DR test | annual | {date} | {date+1y} |

## Article 28–44 — ICT third-party risk management
- Third-party register: `docs/compliance/DORA-third-party-register.md` (separate mandatory artefact)
- Critical-or-important third-party providers (Article 31): {list}
- Concentration risk assessment: {date / approach}

## Article 45–49 — Information sharing
- Threat intelligence sharing arrangements: {ISAC participation, list of partners}

## Sign-off
| Role | Name | Date | Signature |
|---|---|---|---|
| Management body | | | |
| CISO | | | |
| Internal Audit | | | |
