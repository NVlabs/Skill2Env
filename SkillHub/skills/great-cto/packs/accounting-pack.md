---
name: accounting-pack
description: Regulatory + GAAP-controls overlay for bookkeeping / general-ledger / financial-close products. Pairs with enterprise-saas-reviewer (tenant/SSO baseline) or fintech reviewers and accounting-reviewer (ledger-integrity threat model).
when_to_use: Product maintains a general ledger, posts journal entries, runs a month-end close, recognizes contract revenue, or issues 1099s.
applies_to:
  - fintech
  - enterprise-saas
extends:
  - enterprise-saas-pack    # tenant isolation / audit-log baseline (when applicable)
---

# Accounting Compliance Pack

> Loaded automatically when ARCH or PROJECT.md mentions: general ledger, gaap, asc 606, journal entry,
> month-end close, chart of accounts, 1099, three-way reconciliation, revenue recognition, sox itgc.
> Routes through `accounting-reviewer` (threat model) + adds close-signoff gates.
> This pack closes great_cto-k0uf — GL/GAAP auto-attach tokens moved here from
> enterprise-saas-reviewer's stop-gap pattern now that a dedicated reviewer exists.

## Reviewer

- **accounting-reviewer** runs BEFORE senior-dev → writes `TM-accounting-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:close-signoff` | After TM, before senior-dev claims tasks | Controller / finance lead |
| `gate:ship` | Standard | security-officer |

## Required artefacts in every accounting project

| Artefact | Location | Owner |
|---|---|---|
| Double-entry posting engine (balanced debits/credits) | `src/accounting/ledger/` | senior-dev |
| Append-only journal + reversal-entry pattern | `src/accounting/journal/` | senior-dev |
| Preparer/approver SoD RBAC | `src/accounting/rbac/` | senior-dev |
| ASC 606 performance-obligation engine | `src/accounting/revrec/` | senior-dev |
| Period-lock + reopen-with-approval workflow | `src/accounting/close/` | senior-dev |
| Three-way cash reconciliation job | `jobs/cash-reconcile/` | senior-dev |
| 1099 threshold tracker + W-9 gate | `src/accounting/1099/` | senior-dev |

## EVAL suite (in addition to base archetype QA)

- `EVAL-accounting-double-entry-balance` — every posted entry balances debits = credits
- `EVAL-accounting-period-lock-enforcement` — no post to a closed period without reopen-approval
- `EVAL-accounting-asc606-recognition-schedule` — revenue recognized per obligation, not at signing
- `EVAL-accounting-sod-conflict-detection` — same-user prepare+approve flagged automatically

## Month-end close checklist quick reference

1. Sub-ledger cutoffs (AR/AP/inventory)
2. Accruals + deferrals posted
3. Bank/account reconciliations
4. Intercompany eliminations (if applicable)
5. Trial balance review
6. Financial statement generation
7. Close lock (period frozen)

## References

See `agents/accounting-reviewer.md` for full regulatory citations.
