---
name: enterprise-pack
description: Compliance frameworks for regulated industries: DORA (financial entities), NIS2 (essential services), GxP/21CFR11 (pharma/medical), ISO 27001 (ISMS), TISAX (automotive), SOX (US public)
when_to_use: Building for regulated industries (financial services, pharma, medical devices, automotive supply chain, US public companies)
applies_to:
  - regulated
---

# Enterprise Domain Pack

> Extends `regulated` archetype with deep compliance checklists for GxP, NIS2, DORA, TISAX, ISO 27001, and SOX.
> Loaded when `packs: [enterprise-pack]` is in PROJECT.md or auto-loaded for `regulated` archetype.

## Compliance Deep Checklists

### `21cfr11` — FDA 21 CFR Part 11

**Electronic Records (§11.10):**
- [ ] Access control: unique user IDs, no shared accounts
- [ ] Audit trail: all record creation/modification/deletion with timestamp + user + reason
- [ ] Audit trail cannot be modified or disabled by users
- [ ] Record retention: electronic records available for FDA inspection for required period
- [ ] System validation: IQ/OQ/PQ documented and current

**Electronic Signatures (§11.50 + §11.70):**
- [ ] Signatures include: printed name, date/time, meaning (review, approval, authorship)
- [ ] Signatures linked to their respective records (cannot be transferred)
- [ ] Signing authority verified before each use
- [ ] Failed login lockout after configured attempts

**Validation Protocol:**
- [ ] **IQ** (Installation Qualification): system installed per specifications, hardware/software inventory documented
- [ ] **OQ** (Operational Qualification): system operates per design specs across expected ranges
- [ ] **PQ** (Performance Qualification): system performs reliably in real operating conditions
- [ ] Change control: any change triggers re-validation of affected qualification
- [ ] CAPA process: corrective/preventive actions documented for any validation failure

**Data Integrity (ALCOA+):**
- [ ] Attributable: every entry traceable to a person
- [ ] Legible: data readable throughout retention period
- [ ] Contemporaneous: recorded at time of activity
- [ ] Original: first-capture data preserved
- [ ] Accurate: error-free, verified
- [ ] Complete, Consistent, Enduring, Available

**Artifact**: `docs/compliance/21CFR11-checklist.md` + `docs/compliance/IQ-OQ-PQ-protocol.md`

### `nis2` — NIS2 Directive (EU)

**Article 21 — 10 Mandatory Measures:**
1. [ ] Risk analysis and information system security policies
2. [ ] Incident handling (detection, response, reporting)
3. [ ] Business continuity and crisis management
4. [ ] Supply chain security (direct suppliers + service providers)
5. [ ] Security in network and information systems acquisition, development, maintenance
6. [ ] Policies for assessing effectiveness of cybersecurity risk-management measures
7. [ ] Basic cyber hygiene practices and cybersecurity training
8. [ ] Policies on use of cryptography and encryption
9. [ ] Human resources security, access control, asset management
10. [ ] Multi-factor authentication, secured voice/video/text, secured emergency communication

**Article 23 — Incident Reporting:**
- [ ] Early warning: within 24 hours of significant incident
- [ ] Incident notification: within 72 hours with initial assessment
- [ ] Final report: within 1 month with root cause, impact, mitigation
- [ ] Competent authority identified and notification channel tested

**Artifact**: `docs/compliance/NIS2-article21-audit.md` + `docs/compliance/NIS2-incident-procedure.md`

### `dora` — Digital Operational Resilience Act (EU Financial)

**ICT Risk Management (Art. 6-10):**
- [ ] ICT risk management framework documented and approved by management
- [ ] ICT assets inventory current (all systems, networks, data)
- [ ] Business impact analysis for critical functions
- [ ] Risk assessment methodology defined and applied

**Incident Management (Art. 17-19):**
- [ ] ICT-related incident classification policy (major incident criteria: >24h disruption OR >10% clients affected OR significant financial impact)
- [ ] Incident detection and monitoring tools in place
- [ ] Incident response procedures documented and tested

**Third-Party ICT Risk (Art. 28-30):**
- [ ] Register of all third-party ICT service providers (current)
- [ ] Contractual arrangements include: SLA, audit rights, exit strategy
- [ ] Concentration risk assessment (single provider dependency)
- [ ] Sub-outsourcing chain documented

**TLPT (Art. 26):**
- [ ] Threat-Led Penetration Testing programme (3-year cycle)
- [ ] TLPT scope covers critical functions
- [ ] TLPT results feed into risk assessment

**Artifact**: `docs/compliance/DORA-ICT-risk-assessment.md` + `docs/compliance/DORA-third-party-register.md`

### `tisax` — Trusted Information Security Assessment Exchange

**VDA ISA Questionnaire:**
- [ ] Information security policy and organization
- [ ] Human resources security (NDA, training, termination)
- [ ] Physical and environmental security
- [ ] Operations security (change management, malware, logging)
- [ ] Communications security (network segmentation, transfer policies)
- [ ] Access control (user management, MFA, privileged access)
- [ ] Cryptography (key management, TLS requirements)
- [ ] Supplier relationships
- [ ] Incident management
- [ ] Business continuity

**Assessment Levels:**
- **AL1** (Normal): Self-assessment, standard information security
- **AL2** (High): Includes prototype protection, verified by auditor
  - [ ] Prototype data classification (P-marking: highly confidential)
  - [ ] Physical access restrictions for prototype areas
  - [ ] Logical access restrictions for prototype data
  - [ ] Photography/recording restrictions documented
- **AL3** (Very High): Special protection measures, high attack potential scenarios
  - [ ] All AL2 measures + penetration test every 6 months
  - [ ] Physical intrusion detection for prototype areas

**OEM-Specific:**
- [ ] BMW ISP requirements (if applicable)
- [ ] Volkswagen Group ISMS requirements (if applicable)
- [ ] Mercedes-Benz supplier requirements (if applicable)

**Artifact**: `docs/compliance/TISAX-VDA-ISA-results.md` + `docs/compliance/TISAX-AL-determination.md`

### `iso27001` — ISO 27001:2022

**Annex A Controls (93 total, organized by theme):**

**A.5 Organisational (37 controls):**
- [ ] A.5.1 Policies for information security
- [ ] A.5.2 Information security roles and responsibilities
- [ ] A.5.7 Threat intelligence
- [ ] A.5.23 Information security for use of cloud services
- [ ] A.5.29 Information security during disruption

**A.6 People (8 controls):**
- [ ] A.6.1 Screening (background checks)
- [ ] A.6.2 Terms and conditions of employment (NDA)
- [ ] A.6.3 Information security awareness, education and training

**A.7 Physical (14 controls):**
- [ ] A.7.1 Physical security perimeters
- [ ] A.7.4 Physical security monitoring

**A.8 Technological (34 controls):**
- [ ] A.8.2 Privileged access rights (PAM)
- [ ] A.8.5 Secure authentication (MFA)
- [ ] A.8.8 Management of technical vulnerabilities (patch SLA)
- [ ] A.8.9 Configuration management
- [ ] A.8.12 Data leakage prevention
- [ ] A.8.15 Logging
- [ ] A.8.16 Monitoring activities
- [ ] A.8.24 Use of cryptography
- [ ] A.8.25 Secure development life cycle
- [ ] A.8.28 Secure coding

**Statement of Applicability (SoA):**
- [ ] All 93 controls addressed: implemented OR excluded with documented justification
- [ ] SoA coverage ≥ 90% (controls implemented / total applicable)
- [ ] SoA signed by management

**Risk Assessment (ISO 27005):**
- [ ] Risk methodology defined (threats × vulnerabilities × likelihood × impact)
- [ ] Risk register current
- [ ] Residual risks accepted by management
- [ ] Risk treatment plan for unacceptable risks

**Artifact**: `docs/compliance/ISO27001-SoA.md` + `docs/compliance/ISO27005-risk-assessment.md`

### `sox` — SOX IT General Controls

**Change Management:**
- [ ] All production changes have: change ticket + approval + test evidence
- [ ] Segregation between development and production environments
- [ ] Emergency change process documented (with post-facto approval)
- [ ] No unauthorized changes deployed (verified via log comparison)

**Logical Access:**
- [ ] User provisioning: approved access request for every user
- [ ] User deprovisioning: access revoked within 24h of termination
- [ ] Quarterly access review: all privileged accounts reviewed
- [ ] No shared accounts
- [ ] MFA on all privileged access
- [ ] Password policy enforced (complexity + rotation)

**Computer Operations:**
- [ ] Automated job monitoring in place
- [ ] Backup schedule documented and tested (restore test < 90 days)
- [ ] DR/BCP test completed within last 12 months
- [ ] Monitoring alerts for job failures

**Segregation of Duties:**
- [ ] Developers cannot deploy directly to production
- [ ] Approver ≠ requester enforced for all changes
- [ ] Financial data access requires separate authorization

**Artifact**: `docs/compliance/SOX-ITGC-checklist.md`
