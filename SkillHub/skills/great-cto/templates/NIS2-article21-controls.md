---
name: NIS2-article21-controls
description: EU NIS2 Directive cybersecurity risk-management measures (10 categories per Article 21(2)): policies, incident handling, business continuity, supply chain, secure SDLC, MFA, training. Reporting per Article 23 (24h/72h/1mo)
when_to_use: Compliance documentation for regulated archetype with compliance:[nis2]. Required for EU essential and important entities
applies_to:
  - regulated
---

# NIS2-article21-controls.md — Cybersecurity risk management measures

> Mandatory artefact when `compliance: [nis2]` in PROJECT.md.
> Required by `architect.md` compliance artefact gate.
> NIS2 Directive (EU) 2022/2555. Applies to essential and important entities. Article 21 mandates cybersecurity risk-management measures.
> Source: `skills/great_cto/templates/NIS2-article21-controls.md`.

## Entity classification
- Sector: {Annex I essential / Annex II important}
- Subsector: {energy / transport / banking / health / digital infrastructure / etc.}
- Member state of establishment: {country}
- National competent authority: {NCA}

## Article 21(2) — minimum measures (10 categories)

| # | Measure | Implementation | Owner | Evidence | Status |
|---|---|---|---|---|---|
| a | Policies on risk analysis and information system security | {ISMS doc / policy ref} | CISO | `docs/compliance/policy-isms.md` | __ |
| b | Incident handling | {SOC playbooks / runbooks} | SOC lead | `docs/runbooks/incident-*.md` | __ |
| c | Business continuity (backup, disaster recovery, crisis management) | {DR plan + RTO/RPO} | Ops | `docs/dr-plan.md` | __ |
| d | Supply chain security including security-related aspects of relationships between entities and direct suppliers | {vendor security review} | Procurement | `docs/compliance/vendor-security-reviews.md` | __ |
| e | Security in network and information systems acquisition, development, and maintenance, including vulnerability handling and disclosure | {secure SDLC / VDP} | Eng | `docs/compliance/secure-sdlc.md` + `SECURITY.md` | __ |
| f | Policies and procedures to assess the effectiveness of cybersecurity risk-management measures | {audit cadence} | Internal Audit | `docs/compliance/measure-effectiveness.md` | __ |
| g | Basic cyber hygiene practices and cybersecurity training | {training records, MFA enforcement} | HR + IT | `docs/compliance/training-log.md` | __ |
| h | Policies and procedures regarding the use of cryptography and, where appropriate, encryption | {crypto inventory + key mgmt} | CISO | `docs/compliance/crypto-policy.md` | __ |
| i | Human resources security, access control policies, and asset management | {RBAC, least-privilege, joiner-mover-leaver} | IT + HR | `docs/compliance/access-control.md` | __ |
| j | Use of multi-factor authentication or continuous authentication solutions, secured voice/video/text comms, secured emergency comms | {MFA enforcement, comms tooling} | IT | `docs/compliance/mfa-deployment.md` | __ |

## Article 23 — Reporting obligations

| Trigger | Deadline | Recipient |
|---|---|---|
| Significant incident — early warning | ≤ 24 hours from awareness | CSIRT / NCA |
| Significant incident — formal notification | ≤ 72 hours | CSIRT / NCA |
| Final report | ≤ 1 month | CSIRT / NCA |

## Article 32–33 — Supervisory measures
- Last on-site inspection: {date / N/A}
- Last security audit (independent): {date}
- Open findings: {count + status}

## Sign-off
| Role | Name | Date |
|---|---|---|
| Management body | | |
| CISO | | |
