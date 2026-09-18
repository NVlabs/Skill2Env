---
name: PCI-DSS-SAQ-A
description: PCI-DSS Self-Assessment Questionnaire A — for e-commerce merchants who fully outsource cardholder data to PSP (Stripe Elements / Checkout). 22 controls subset of full PCI-DSS
when_to_use: Compliance documentation for commerce projects with compliance:[pci-dss-saq-a]. Cheapest PCI scope
applies_to:
  - commerce
---

# PCI-DSS-SAQ-A.md — Self-Assessment Questionnaire A (e-commerce, fully outsourced)

> Mandatory artefact when `compliance: [pci-dss-saq-a]` in PROJECT.md.
> Required by `architect.md` compliance artefact gate.
> SAQ-A applies to **card-not-present** merchants who fully outsource cardholder data functions to PCI-DSS-validated third parties (Stripe Elements, Stripe Checkout, redirected payment pages). The merchant **never electronically stores, processes, or transmits any cardholder data** on its systems.
> Source: `skills/great_cto/templates/PCI-DSS-SAQ-A.md`.

## Eligibility — confirm SAQ-A applies (all must be YES)

| # | Criterion | Answer |
|---|---|---|
| 1 | We accept only card-not-present (e-commerce / mail / phone) transactions | yes |
| 2 | All payment acceptance and processing is **fully outsourced** to PCI-DSS-validated 3rd parties (Stripe / Adyen / Braintree / etc.) | yes |
| 3 | We do not electronically store, process, or transmit cardholder data on our systems or premises | yes |
| 4 | The 3rd party acknowledges PCI-DSS validity (current AOC on file) | yes |
| 5 | We have confirmed our payment-page acceptance method (iframe / hosted-redirect / direct API call from browser to processor) | yes |

If ANY answer is NO → SAQ-A is **not applicable**. Move to SAQ-A-EP or SAQ-D and document.

## Acceptance method
- Provider: {Stripe / Adyen / etc.}
- Method: {Stripe Elements (iframe) / Stripe Checkout (redirect) / direct-to-processor JS}
- Cardholder data never touches our backend: {confirm — describe data flow}
- Tokenisation: card-data → token (`pm_xxx` / `cus_xxx`); only tokens stored

## SAQ-A controls (subset of full PCI-DSS, ~22 controls)

### Requirement 2 — Configuration management
| Control | Implementation | Evidence |
|---|---|---|
| 2.1 | Default vendor passwords changed on all systems | password policy + sample audit |
| 2.2.2 | Only necessary services / protocols enabled | network ACL audit |

### Requirement 6 — Develop and maintain secure systems
| 6.4.3 | Manage all scripts loaded on payment pages (CSP + SRI on third-party scripts; iframe sandboxing) | CSP header + SRI hashes |
| 6.4.5 | Apply secure development practices (peer review, input validation) | secure-SDLC doc |

### Requirement 8 — Identify users and authenticate access
| 8.2.1 | Strong authentication for all admin access | MFA enforced |
| 8.3.1 | MFA on all administrative access (especially anything that could affect payment-page integrity) | MFA log audit |

### Requirement 9 — Restrict physical access
| 9.5.1 | Hard-copy media disposal (n/a in cloud-only setup; document exclusion) | n/a |

### Requirement 12 — Information security policy
| 12.1.1 | Annual review of security policy | last review date |
| 12.6.1 | Security awareness training | training log |
| 12.8.x | Maintain list of service providers + AOC on file | `docs/compliance/PCI-vendors.md` |
| 12.10.1 | Incident response plan | `docs/runbooks/incident-pci.md` |

## Service-provider AOC inventory
| Service provider | Service | AOC date | Renewal due |
|---|---|---|---|
| Stripe | Payment processing + Stripe Elements | {date} | {date+1y} |
| {CDN} | TLS termination on payment page | {date} | {date+1y} |
| {hosting} | Infrastructure (cloud-only) | {date} | {date+1y} |

## Attestation of Compliance (AOC) — merchant
- Merchant name: {legal entity}
- Acquirer / merchant bank: {name}
- Effective date: {date}
- Validity: 1 year
- Signed by: {executive officer with sufficient authority}

## CI grep + gate enforcement (qa-engineer Step 0b)
The PAN grep in `qa-engineer.md` enforces that no full credit-card number ever appears in code or logs. SAQ-A scope must remain clean — if grep finds a candidate PAN, gate fails:

```
grep -rE '\b[0-9]{13,19}\b' src tests --include="*.py" --include="*.ts" \
  | grep -v "test_card\|4242424242424242\|stripe.com"
# expected: empty
```

## Sign-off
| Role | Name | Date |
|---|---|---|
| Internal Security Assessor / QSA | | |
| CTO / executive officer | | |
