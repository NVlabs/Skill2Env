# TM-tax-{slug} — Tax Preparation / Filing Threat Model

**Owner:** tax-reviewer
**ARCH ref:** docs/architecture/ARCH-{slug}.md
**Date:** {YYYY-MM-DD}
**Verdict:** signed-off | blocked

---

## 1. Scope

- **Return types:** [ ] 1040 individual  [ ] 1120/1120S/1065 business  [ ] state returns
- **Filing mode:** [ ] self-file (consumer)  [ ] paid-preparer tool  [ ] embedded/white-label
- **E-file integration:** [ ] direct MeF  [ ] via third-party transmitter
- **Corporate provision:** [ ] ASC 740 in scope  [ ] not applicable (individual-only)

## 2. Compliance applicability matrix

| Regime | Applies? | Reason |
|---|---|---|
| IRS MeF e-file schema validation | yes / no | … |
| PTIN / Circular 230 (paid preparer) | yes / no | … |
| IRS Pub 4557 / GLBA Safeguards Rule / WISP | yes / no | always applies if taxpayer PII stored |
| Form 8879 e-signature authorization | yes / no | … |
| IRC §7216 consent-to-disclose | yes / no | … |
| Multi-state nexus | yes / no | … |
| ASC 740 (corporate) | yes / no | … |

## 3. Findings

### Critical

| ID | Finding | Mitigation | Gate |
|---|---|---|---|
| T-C-1 | … | … | gate:tax-filing-signoff |

### High

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

### Medium / Low

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

## 4. Required artefacts before senior-dev claims tasks

- [ ] E-file transmission validated against current tax-year MeF schema
- [ ] EFIN/transmitter credentials handled as secrets
- [ ] Form 8879 (or equivalent) authorization captured + retained (3-yr) before transmission
- [ ] PTIN captured/validated for paid-preparer roles
- [ ] Circular 230 contingent-fee compliance check
- [ ] Taxpayer PII encryption at rest/in transit + access logging
- [ ] WISP-supporting artifacts (access logs, retention/deletion policy)
- [ ] IRC §7216 explicit consent gate for secondary data use
- [ ] Identity-verification controls beyond SSN+demographics (SIRF mitigation)
- [ ] State-specific, updatable multi-state nexus determination (if applicable)

## 5. EVAL suite required

- EVAL-tax-mef-schema-validation
- EVAL-tax-8879-gate-before-transmit
- EVAL-tax-7216-consent-enforcement
- EVAL-tax-identity-fraud-detection

## 6. Human gates

| Gate | Owner | Trigger |
|---|---|---|
| gate:tax-filing-signoff | EA/CPA compliance lead | after TM, before senior-dev |
| gate:ship | security-officer | standard |

<!-- HANDOFF -->
tax-reviewer-verdict: signed-off
critical-findings: 0
high-findings: 0
