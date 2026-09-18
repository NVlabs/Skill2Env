# TM-rcm-{slug} — Revenue Cycle Management / Medical Coding Threat Model

**Owner:** rcm-reviewer
**ARCH ref:** docs/architecture/ARCH-{slug}.md
**Date:** {YYYY-MM-DD}
**Verdict:** signed-off | blocked

---

## 1. Scope

- **Claim forms:** [ ] CMS-1500 (professional)  [ ] UB-04 (institutional)
- **Coding surface:** [ ] CPT  [ ] HCPCS  [ ] ICD-10-CM  [ ] AI/LLM-assisted coding
- **Transactions:** [ ] 837 (claim)  [ ] 835 (remittance)  [ ] 270/271 (eligibility)  [ ] 278 (prior auth)
- **Patient billing:** [ ] good-faith estimates  [ ] balance billing  [ ] No Surprises Act scope

## 2. Compliance applicability matrix

| Regime | Applies? | Reason |
|---|---|---|
| False Claims Act (upcoding/unbundling exposure) | yes / no | … |
| OIG Work Plan enforcement patterns | yes / no | … |
| NCCI PTP edits + MUEs | yes / no | … |
| HIPAA 5010 EDI (837/835) | yes / no | … |
| No Surprises Act (GFE / balance billing) | yes / no | … |
| NPI / taxonomy validation | yes / no | … |
| Prior-authorization requirements | yes / no | payer-specific |

## 3. Findings

### Critical

| ID | Finding | Mitigation | Gate |
|---|---|---|---|
| R-C-1 | … | … | gate:coding-signoff |

### High

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

### Medium / Low

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

## 4. Required artefacts before senior-dev claims tasks

- [ ] Documentation-evidence trace for every autonomously-assigned code
- [ ] Confidence floor routing low-confidence codes to certified coder (CPC/CCS) sign-off
- [ ] NCCI PTP + MUE pre-submission checks (current quarterly tables)
- [ ] CPT↔ICD-10 medical-necessity (LCD/NCD) linkage validation
- [ ] Required-field validation per claim form type (CMS-1500 / UB-04)
- [ ] Prior-authorization requirement check (payer + CPT/HCPCS specific)
- [ ] NPI checksum + taxonomy-code validation against NPPES
- [ ] 835/837 parsing validated against HIPAA 5010 implementation guide
- [ ] Auto-posting variance-flagging (vs. expected billed amount)
- [ ] No Surprises Act good-faith-estimate generation (self-pay/uninsured, ≥3 business days out)

## 5. EVAL suite required

- EVAL-rcm-upcoding-detection
- EVAL-rcm-ncci-edit-coverage
- EVAL-rcm-coder-escalation-threshold
- EVAL-rcm-835-reconciliation-accuracy

## 6. Human gates

| Gate | Owner | Trigger |
|---|---|---|
| gate:coding-signoff | certified coder (CPC/CCS) | after TM, before senior-dev, for FCA-high paths |
| gate:ship | security-officer | standard |

<!-- HANDOFF -->
rcm-reviewer-verdict: signed-off
critical-findings: 0
high-findings: 0
