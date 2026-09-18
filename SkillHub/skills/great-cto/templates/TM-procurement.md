# TM-procurement-{slug} — Purchasing / Source-to-Pay Threat Model

**Owner:** procurement-reviewer
**ARCH ref:** docs/architecture/ARCH-{slug}.md
**Date:** {YYYY-MM-DD}
**Verdict:** signed-off | blocked

---

## 1. Scope

- **Purchasing surface:** [ ] PO creation  [ ] receiving  [ ] invoice matching  [ ] payment release
- **Vendor management:** [ ] onboarding  [ ] sanctions screening  [ ] banking-detail changes
- **Sourcing:** [ ] RFP/RFQ  [ ] punchout/cXML catalog  [ ] preferred-vendor catalog
- **SOX scope:** [ ] public company / IPO-track  [ ] SOX ITGC audit applies

## 2. Compliance applicability matrix

| Regime | Applies? | Reason |
|---|---|---|
| Three-way match control | yes / no | … |
| Segregation of duties (SoD) | yes / no | … |
| OFAC / sanctions screening | yes / no | … |
| SOX procurement ITGC | yes / no | … |
| Competitive-bid fairness | yes / no | … |

## 3. Findings

### Critical

| ID | Finding | Mitigation | Gate |
|---|---|---|---|
| P-C-1 | … | … | gate:procurement-controls |

### High

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

### Medium / Low

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

## 4. Required artefacts before senior-dev claims tasks

- [ ] Three-way match hard-block on payment release + auditable override path
- [ ] SoD-enforcing RBAC (requester / approver / receiver as distinct roles)
- [ ] Automated SoD-conflict detection report
- [ ] Tiered approval-threshold routing + threshold-splitting detection
- [ ] OFAC/sanctions screening gate on vendor onboarding + banking-detail re-screen
- [ ] Vendor-master edit access separated from payment-approval access
- [ ] Sealed RFP/RFQ bid submissions until deadline
- [ ] Single-use, short-lived, session-scoped punchout/cXML tokens
- [ ] Config-as-a-control on approval-threshold + vendor-master changes
- [ ] Maverick-spend distinct reporting category

## 5. EVAL suite required

- EVAL-procurement-three-way-match-enforcement
- EVAL-procurement-sod-conflict-detection
- EVAL-procurement-ofac-screening-gate
- EVAL-procurement-threshold-split-detection

## 6. Human gates

| Gate | Owner | Trigger |
|---|---|---|
| gate:procurement-controls | finance/controller | after TM, before senior-dev |
| gate:ship | security-officer | standard |

<!-- HANDOFF -->
procurement-reviewer-verdict: signed-off
critical-findings: 0
high-findings: 0
