---
name: tax-pack
description: Regulatory + preparer-compliance overlay for tax preparation / filing products. Pairs with regulated-reviewer (general fintech compliance baseline) and tax-reviewer (IRS filing-integrity threat model).
when_to_use: Product prepares or files tax returns, integrates with IRS e-file (MeF), or involves a paid-preparer (CPA/EA) role.
applies_to:
  - fintech
extends:
  - regulated-pack    # general fintech compliance baseline
---

# Tax Compliance Pack

> Loaded automatically when ARCH or PROJECT.md mentions: ptin, circular 230, form 8879, mef,
> pub 4557, section 7216, tax prep, e-file, irs.
> Routes through `tax-reviewer` (threat model) + adds filing-signoff gates.

## Reviewer

- **tax-reviewer** runs BEFORE senior-dev → writes `TM-tax-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:tax-filing-signoff` | After TM, before senior-dev claims tasks | EA/CPA compliance lead |
| `gate:ship` | Standard | security-officer |

## Required artefacts in every tax-prep project

| Artefact | Location | Owner |
|---|---|---|
| MeF schema validator (current tax year) | `src/tax/mef/` | senior-dev |
| Form 8879 authorization gate | `src/tax/8879/` | senior-dev |
| PTIN capture/validation | `src/tax/preparer/` | senior-dev |
| Taxpayer-PII encryption + access log | `src/tax/pii/` | senior-dev |
| §7216 consent capture | `src/tax/consent-7216/` | senior-dev |
| Identity-verification / SIRF anomaly detection | `src/tax/fraud-detect/` | senior-dev |
| Multi-state nexus determination engine | `src/tax/nexus/` | senior-dev |

## EVAL suite (in addition to regulated-pack QA)

- `EVAL-tax-mef-schema-validation` — rejects submission against stale/wrong tax-year schema
- `EVAL-tax-8879-gate-before-transmit` — e-file blocked without valid signed 8879 on file
- `EVAL-tax-7216-consent-enforcement` — secondary data use blocked without specific consent
- `EVAL-tax-identity-fraud-detection` — anomalous refund-destination patterns flagged

## IRC §7216 quick reference — what needs specific consent

| Use | Consent required? |
|---|---|
| Preparing the current return | No (core service) |
| Preparer's own marketing/cross-sell | Yes — specific, written |
| Sharing with third-party analytics/LLM vendor | Yes — specific, written |
| Using data to train/fine-tune an AI model | Yes — specific, written |

## References

See `agents/tax-reviewer.md` for full regulatory citations.
