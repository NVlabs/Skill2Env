---
name: rcm-pack
description: Regulatory + compliance overlay for healthcare Revenue Cycle Management / medical-billing products. Pairs with healthcare-reviewer (HIPAA/PHI) and rcm-reviewer (coding + claims threat model).
when_to_use: Product submits or scrubs medical claims, assigns CPT/HCPCS/ICD-10 codes, processes ERA/835 remittance, or calculates patient financial responsibility.
applies_to:
  - healthcare
extends:
  - healthcare-pack    # HIPAA/PHI/HL7/FHIR baseline
---

# RCM Compliance Pack

> Loaded automatically when ARCH or PROJECT.md mentions: medical coding, icd-10, cpt, hcpcs, drg,
> revenue cycle, rcm, claim scrub, 837, 835, cms-1500, ub-04, prior auth, denial, ncci, modifier, payer.
> Routes through `rcm-reviewer` (threat model) + adds coding-signoff gates.

## Reviewer

- **rcm-reviewer** runs BEFORE senior-dev → writes `TM-rcm-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:coding-signoff` | After TM, before senior-dev claims tasks (FCA-high paths) | Certified coder (CPC/CCS) |
| `gate:ship` | Standard | security-officer |

## Required artefacts in every RCM project

| Artefact | Location | Owner |
|---|---|---|
| Documentation-evidence trace (code → chart note) | `src/rcm/evidence/` | senior-dev |
| Confidence-floor coder-escalation queue | `src/rcm/coder-queue/` | senior-dev |
| NCCI PTP/MUE edit checker (current quarterly tables) | `src/rcm/ncci/` | senior-dev |
| Prior-auth requirement matrix (payer × CPT/HCPCS) | `src/rcm/prior-auth/` | senior-dev |
| 835/837 EDI parser (HIPAA 5010 validated) | `src/rcm/edi/` | senior-dev |
| Good-faith-estimate generator (No Surprises Act) | `src/rcm/gfe/` | senior-dev |
| NPI/taxonomy validator (NPPES-backed) | `src/rcm/npi/` | senior-dev |

## EVAL suite (in addition to healthcare-pack QA)

- `EVAL-rcm-upcoding-detection` — flags codes exceeding documented service complexity
- `EVAL-rcm-ncci-edit-coverage` — PTP/MUE edits applied against current quarterly release
- `EVAL-rcm-coder-escalation-threshold` — low-confidence codes route to CPC/CCS, never auto-submit
- `EVAL-rcm-835-reconciliation-accuracy` — posted amounts match remittance-advice line items

## Denial-code (CARC/RARC) workflow quick reference

| Category | Action |
|---|---|
| Missing/invalid prior auth | Resubmit with auth number |
| Medical necessity (LCD/NCD mismatch) | Appeal with supporting documentation |
| Timely filing | Non-recoverable — track deadlines proactively |
| Duplicate claim | Verify + write off |

## References

See `agents/rcm-reviewer.md` for full regulatory citations.
