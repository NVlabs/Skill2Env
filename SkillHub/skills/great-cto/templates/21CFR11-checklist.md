---
name: 21CFR11-checklist
description: FDA 21 CFR Part 11 (electronic records & signatures) checklist: Subpart B controls (audit trail, access controls, validation), Subpart C electronic signatures (linking, uniqueness, MFA components)
when_to_use: Compliance documentation for regulated archetype with compliance:[gxp] or [21cfr11]. Required for systems creating/maintaining/transmitting FDA-regulated records (pharma, medical devices, clinical trials)
applies_to:
  - regulated
---

# 21CFR11-checklist.md — FDA 21 CFR Part 11 (electronic records & signatures)

> Mandatory artefact when `compliance: [gxp]` or `compliance: [21cfr11]` in PROJECT.md.
> Required by `architect.md` compliance artefact gate.
> Applies to systems that create, modify, maintain, archive, retrieve, or transmit electronic records subject to FDA regulations (pharma / medical device / clinical trials).
> Source: `skills/great_cto/templates/21CFR11-checklist.md`.

## System classification
- System name: {LIMS / ELN / MES / clinical EDC}
- Predicate rule: {21 CFR Part 211 / 820 / 312}
- GxP risk: {high / medium / low}
- Validation status: {validated / in-progress / pending}

## Subpart B — Electronic records (§ 11.10 controls for closed systems)

| Control | Required | Implementation | Evidence | Status |
|---|---|---|---|---|
| (a) Validation | yes | IQ/OQ/PQ documents | `docs/validation/IQ-{system}.md` | __ |
| (b) Generate accurate copies | yes | export to PDF + hash | export procedure SOP | __ |
| (c) Protection of records to enable accurate retrieval | yes | append-only audit log + immutable archive | audit log spec | __ |
| (d) Limiting system access to authorized individuals | yes | RBAC + MFA | access control policy | __ |
| (e) Computer-generated, time-stamped audit trails | yes | append-only log of CRUD on records | `docs/compliance/audit-trail-spec.md` | __ |
| (f) Operational system checks | yes | sequence enforcement, data integrity rules | system design doc | __ |
| (g) Authority checks | yes | role-based action authorisation | access matrix | __ |
| (h) Device checks | yes | terminal / workstation identification | device inventory | __ |
| (i) Determination of training | yes | training records per role | `docs/compliance/training-log.md` | __ |
| (j) Establishment of policies for accountability | yes | electronic signature policy | `docs/compliance/e-sig-policy.md` | __ |
| (k) System documentation controls | yes | doc control + change control SOPs | doc control SOP | __ |

## Subpart C — Electronic signatures (§ 11.50 / 11.70 / 11.100)

| Requirement | Implementation | Status |
|---|---|---|
| § 11.50 Signed electronic records contain printed name + signature date + meaning | {capture in audit log} | __ |
| § 11.70 Linking — signature cannot be excised or transferred between records | {cryptographic binding} | __ |
| § 11.100 Each electronic signature is unique to one individual | {user account uniqueness} | __ |
| § 11.200 Components — at minimum two distinct identification components (e.g. user-ID + password) for non-biometric | {MFA enforcement} | __ |
| § 11.300 Controls for identification codes / passwords | {password policy + rotation} | __ |

## Validation lifecycle
- IQ (Installation Qualification): `docs/validation/IQ-{system}.md`
- OQ (Operational Qualification): `docs/validation/OQ-{system}.md`
- PQ (Performance Qualification): `docs/validation/PQ-{system}.md`
- Re-validation trigger: {after upgrade, after configuration change, periodic — define interval}

## Audit trail requirements
- Field-level changes captured: {yes — list which fields}
- Old value + new value + user + timestamp + reason for change
- Retention: {longer of 5 years OR product shelf life + 1 year}
- Tamper-evident: {hash chain / WORM storage}

## Annual review
- Last reviewed: {date}
- Next due: {date+1y}
- Reviewer: QA Manager

## Sign-off
| Role | Name | Date |
|---|---|---|
| QA Manager | | |
| IT/Validation Lead | | |
| Quality Director | | |
