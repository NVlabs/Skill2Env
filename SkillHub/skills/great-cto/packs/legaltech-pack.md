---
name: legaltech-pack
description: Legal-services / legal-tech overlay. Pairs legal-reviewer.
when_to_use: Product serves law firms, solo practitioners, or in-house legal teams — matter management, client intake, trust accounting, or e-filing.
applies_to:
  - legal
extends: []
---

# Legal-Tech Compliance Pack

> Loaded when ARCH mentions: matter, docket, litigation, retainer, IOLTA, Clio, MyCase, PACER, ECF, conflict check, engagement letter, paralegal, law firm, attorney.

## Reviewer

- **legal-reviewer** → `TM-legal-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:upl-review` | Any client-facing AI/automation output touching client-specific facts | Supervising attorney |
| `gate:ship` | Standard | security-officer |

## Required artefacts

| Artefact | Owner |
|---|---|
| UPL surface audit (information vs. advice line, per output) | legal-reviewer |
| Attorney-review gate on client-specific-fact outputs | senior-dev |
| Trust vs. operating account separation + per-client ledgers | senior-dev |
| Monthly three-way trust reconciliation job | senior-dev |
| Conflict-of-interest check blocking intake until cleared | senior-dev |
| Matter-level access control + outbound metadata scrubbing | senior-dev |
| FRCP 5.2 (or state equivalent) pre-e-filing redaction gate | senior-dev |
| Legal-hold override on auto-purge/retention-expiry | senior-dev |
| Engagement-letter-on-file gate before matter proceeds past intake | senior-dev |

## EVAL suite

- `EVAL-upl-gate-coverage` (every client-specific-fact output has an attorney-review gate)
- `EVAL-trust-ledger-integrity` (client ledger sums reconcile against trust bank balance)
- `EVAL-conflict-check-blocking` (intake cannot finalize with an uncleared conflict)
- `EVAL-matter-isolation` (cross-matter data leakage in AI/search surfaces)
- `EVAL-efiling-redaction` (FRCP 5.2 fields redacted pre-submission)

## Anti-patterns to block in review

- AI output recommending a specific legal course of action without an attorney-review gate
- Trust-account withdrawal before an invoice/billing event
- Single shared vector index / search surface across all clients' matter content
- Intake proceeding to representation before conflict check clears
- E-filing submission without FRCP 5.2 (or state equivalent) redaction applied
