---
name: procurement-pack
description: Regulatory + financial-controls overlay for purchasing / source-to-pay products. Pairs with enterprise-saas-reviewer (tenant/SSO baseline) and procurement-reviewer (three-way match + SoD threat model).
when_to_use: Product manages purchase orders, vendor payments, spend-approval workflows, or e-procurement (punchout/cXML) integration.
applies_to:
  - enterprise-saas
  - enterprise
extends:
  - enterprise-saas-pack    # multi-tenant / SSO / audit-log baseline
---

# Procurement Compliance Pack

> Loaded automatically when ARCH or PROJECT.md mentions: purchase order, three-way match,
> procurement, requisition, rfp, rfq, vendor onboarding, ofac, punchout, cxml, spend analytics,
> maverick spend.
> Routes through `procurement-reviewer` (threat model) + adds financial-controls gates.

## Reviewer

- **procurement-reviewer** runs BEFORE senior-dev → writes `TM-procurement-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:procurement-controls` | After TM, before senior-dev claims tasks | Finance / controller |
| `gate:ship` | Standard | security-officer |

## Required artefacts in every procurement project

| Artefact | Location | Owner |
|---|---|---|
| Three-way match engine (PO/receipt/invoice) | `src/procurement/match/` | senior-dev |
| SoD-enforcing RBAC roles | `src/procurement/rbac/` | senior-dev |
| SoD-conflict detection report | `jobs/sod-audit/` | senior-dev |
| Approval-threshold routing engine | `src/procurement/approvals/` | senior-dev |
| OFAC/sanctions screening integration | `src/procurement/vendor-screen/` | senior-dev |
| Punchout/cXML session-token handler | `src/procurement/punchout/` | senior-dev |
| Spend-analytics + maverick-spend report | `src/procurement/analytics/` | senior-dev |

## EVAL suite (in addition to enterprise-saas-pack QA)

- `EVAL-procurement-three-way-match-enforcement` — payment blocked on PO/receipt/invoice mismatch
- `EVAL-procurement-sod-conflict-detection` — same-user request+approve flagged automatically
- `EVAL-procurement-ofac-screening-gate` — vendor unpayable until clean sanctions screen
- `EVAL-procurement-threshold-split-detection` — aggregate spend catches split purchases

## Three-way match tolerance quick reference

| Field | Typical tolerance | Escalation |
|---|---|---|
| Quantity | 0% (exact) or small % for consumables | Auto-hold on mismatch |
| Unit price | 0-5% variance | Buyer review above threshold |
| Vendor identity | 0% (exact match) | Hard block, no override without second approver |

## References

See `agents/procurement-reviewer.md` for full regulatory citations.
