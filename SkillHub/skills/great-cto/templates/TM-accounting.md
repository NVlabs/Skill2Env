# TM-accounting-{slug} — Bookkeeping / GL / Financial-Close Threat Model

**Owner:** accounting-reviewer
**ARCH ref:** docs/architecture/ARCH-{slug}.md
**Date:** {YYYY-MM-DD}
**Verdict:** signed-off | blocked

---

## 1. Scope

- **Ledger surface:** [ ] general ledger  [ ] sub-ledgers (AR/AP)  [ ] chart of accounts
- **Revenue model:** [ ] subscription  [ ] usage-based  [ ] multi-element contract  [ ] ASC 606 in scope
- **Close process:** [ ] month-end close  [ ] period lock  [ ] three-way reconciliation
- **Filings:** [ ] 1099-NEC/MISC  [ ] 1096 transmittal
- **SOX scope:** [ ] public company / IPO-track  [ ] SOX ITGC audit applies

## 2. Compliance applicability matrix

| Regime | Applies? | Reason |
|---|---|---|
| GAAP (accrual-basis) | yes / no | … |
| ASC 606 revenue recognition | yes / no | … |
| SOX ITGC | yes / no | … |
| 1099/1096 filing | yes / no | … |
| Double-entry / audit-trail immutability | yes / no | always applies if ledger exists |

## 3. Findings

### Critical

| ID | Finding | Mitigation | Gate |
|---|---|---|---|
| A-C-1 | … | … | gate:close-signoff |

### High

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

### Medium / Low

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

## 4. Required artefacts before senior-dev claims tasks

- [ ] Double-entry balance enforcement (debits = credits) at persistence layer
- [ ] Append-only audit trail + reversal-entry correction pattern
- [ ] Preparer/approver SoD in RBAC + automated SoD-conflict report
- [ ] ASC 606 performance-obligation modeling (if contract revenue)
- [ ] Period-lock mechanism + explicit reopen-with-approval workflow
- [ ] Three-way cash reconciliation (bank / ledger / settlement) with exception queue
- [ ] Chart-of-accounts change-approval workflow
- [ ] Cumulative annual per-payee payment tracking + W-9 gate

## 5. EVAL suite required

- EVAL-accounting-double-entry-balance
- EVAL-accounting-period-lock-enforcement
- EVAL-accounting-asc606-recognition-schedule
- EVAL-accounting-sod-conflict-detection

## 6. Human gates

| Gate | Owner | Trigger |
|---|---|---|
| gate:close-signoff | controller/finance lead | after TM, before senior-dev |
| gate:ship | security-officer | standard |

<!-- HANDOFF -->
accounting-reviewer-verdict: signed-off
critical-findings: 0
high-findings: 0
