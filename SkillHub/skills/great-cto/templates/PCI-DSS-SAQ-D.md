---
name: PCI-DSS-SAQ-D
description: PCI-DSS Self-Assessment Questionnaire D — full PCI-DSS scope. ~250 sub-controls. For merchants storing/processing/transmitting CHD on own systems (custom vault, direct API integration)
when_to_use: Compliance documentation for commerce projects with compliance:[pci-dss] (full scope). Most expensive scope; only when SAQ-A unavailable
applies_to:
  - commerce
---

# PCI-DSS-SAQ-D.md — Self-Assessment Questionnaire D (full PCI-DSS scope)

> Mandatory artefact when `compliance: [pci-dss]` (default → SAQ-D unless `[pci-dss-saq-a]` or `[pci-dss-saq-a-ep]` specified) in PROJECT.md.
> Required by `architect.md` compliance artefact gate.
> SAQ-D applies when the merchant **electronically stores, processes, or transmits cardholder data** on its own systems (e.g. payment terminal, custom card-handling code, vault, payment service provider built in-house). Most comprehensive — covers all 12 PCI-DSS requirements + ~250 sub-controls.
> Source: `skills/great_cto/templates/PCI-DSS-SAQ-D.md`.

## When SAQ-D applies
- We store, process, or transmit cardholder data ourselves (PAN, CHD)
- We have built our own payment vault / token service
- We process card data via direct API integration (server-to-server with raw PAN)
- We are a service provider (not just a merchant)

If you can outsource fully, prefer SAQ-A. SAQ-D is the most expensive scope; treat as a last-resort architecture choice.

## CDE (Cardholder Data Environment) scope diagram
- Network diagram: `docs/compliance/PCI-network-diagram.png` (mandatory artefact per req. 1.1.2)
- Data-flow diagram: `docs/compliance/PCI-data-flow.png` (mandatory per 1.1.3)
- CDE boundary defined: {VLAN / VPC / segment list}

## Twelve requirements — high-level checklist

### Build and Maintain a Secure Network and Systems
| Req | Topic | Implemented | Evidence |
|---|---|---|---|
| 1 | Install + maintain network security controls (firewalls + segmentation between CDE and untrusted) | __ | network-diagram.png, firewall rule set |
| 2 | Apply secure configurations to all system components (no defaults, hardened baseline) | __ | CIS benchmark scan results |

### Protect Account Data
| 3 | Protect stored account data (PAN encryption / tokenisation / truncation; SAD never stored after authorisation) | __ | KMS config, key rotation log |
| 4 | Protect cardholder data with strong cryptography during transmission over open public networks (TLS 1.2+ everywhere) | __ | TLS audit report, SSL Labs grade |

### Maintain a Vulnerability Management Programme
| 5 | Protect all systems and networks from malicious software | __ | EDR / AV deployment + alerts |
| 6 | Develop and maintain secure systems and software (secure-SDLC, vulnerability mgmt, code review) | __ | `docs/compliance/secure-sdlc.md` + change log |

### Implement Strong Access Control Measures
| 7 | Restrict access to system components and cardholder data by business need-to-know (RBAC, least privilege) | __ | access matrix |
| 8 | Identify users and authenticate access to system components (unique IDs, MFA on all CDE access) | __ | IAM config |
| 9 | Restrict physical access to cardholder data (data centre access logs, secure disposal) | __ | facility access logs (or mark n/a if cloud-only with provider AOC) |

### Regularly Monitor and Test Networks
| 10 | Log and monitor all access to system components and cardholder data | __ | SIEM logs + retention policy (1 year, 90 days online) |
| 11 | Test security of systems and networks regularly (quarterly internal + external ASV scans, annual pen test) | __ | scan reports, pentest report |

### Maintain an Information Security Policy
| 12 | Support information security with organisational policies and programmes (annual review, training, incident plan) | __ | policy + training records |

## Quarterly scans + annual pentest

| Test | Frequency | Last performed | Next due | Result |
|---|---|---|---|---|
| Internal vulnerability scan | quarterly | {date} | {date+90d} | clean / N findings |
| External ASV scan | quarterly | {date} | {date+90d} | passing / failed (re-scan) |
| Penetration test (network + app) | annual + on major change | {date} | {date+1y} | clean / findings remediated |
| Segmentation testing | annual + on major change | {date} | {date+1y} | passing |

## Approved Scanning Vendor (ASV)
- Vendor: {name from PCI SSC list}
- Engagement contract date: {date}

## QSA (Qualified Security Assessor) — required for service providers + Level 1 merchants
- QSA company: {name}
- Lead assessor: {name}
- Last full assessment: {date}
- ROC (Report on Compliance) date: {date}

## Compensating controls log
| Req # | Reason for compensating control | Description | Approver | Date |
|---|---|---|---|---|
| | | | | |

## Sign-off
| Role | Name | Date |
|---|---|---|
| Internal Security Assessor / QSA | | |
| CISO | | |
| CTO / executive officer | | |
