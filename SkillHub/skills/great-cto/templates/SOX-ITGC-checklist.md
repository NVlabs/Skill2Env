---
name: SOX-ITGC-checklist
description: Sarbanes-Oxley §404 IT General Controls (4 domains: Change Management, Logical Access, Computer Operations, Program Development). 25 controls + test methodology + materiality assessment
when_to_use: Compliance documentation for regulated archetype with compliance:[sox]. Required for US public companies + foreign issuers
applies_to:
  - regulated
---

# SOX-ITGC-checklist.md — IT General Controls (Sarbanes-Oxley §404)

> Mandatory artefact when `compliance: [sox]` in PROJECT.md.
> Required by `architect.md` compliance artefact gate.
> Applies to public US companies + foreign issuers. ITGCs cover IT systems supporting financial reporting per PCAOB AS 2201 / SAS 109.
> Source: `skills/great_cto/templates/SOX-ITGC-checklist.md`.

## Scope
- Financial reporting systems in scope: {ERP / GL / billing / reconciliation / consolidation}
- Material weakness threshold: {as defined by external auditor}
- Test period: {fiscal year start — end}
- ITGC owner: {role}

## Four ITGC domains

### 1. Change Management
| Control | Description | Frequency | Tester | Status |
|---|---|---|---|---|
| CM-01 | All production code changes go through documented approval (PR / change ticket) | every change | sample 25 / quarter | __ |
| CM-02 | Segregation of duties: developer cannot deploy own code to production | continuous | quarterly user review | __ |
| CM-03 | Emergency changes documented within 24 hours and reviewed retroactively | as needed | every emergency | __ |
| CM-04 | Database schema changes versioned in migration files + peer-reviewed | every change | sample 25 / quarter | __ |
| CM-05 | Configuration changes (IaC) require approval + change record | every change | sample 25 / quarter | __ |

### 2. Logical Access (Identity & Access Management)
| Control | Description | Frequency | Tester | Status |
|---|---|---|---|---|
| LA-01 | New user access requires documented business justification + approver | per joiner | sample / quarter | __ |
| LA-02 | Terminated users disabled within 24 hours of termination | per leaver | every leaver | __ |
| LA-03 | Privileged access (DB admin, prod sudo, GL super-user) reviewed quarterly | quarterly | every quarter | __ |
| LA-04 | Password policy enforced (length, rotation, MFA on privileged accounts) | continuous | quarterly review | __ |
| LA-05 | Service-account credentials rotated per policy + audit logged | quarterly | every rotation | __ |
| LA-06 | Authentication / authorisation logs reviewed monthly | monthly | every month | __ |

### 3. Computer Operations
| Control | Description | Frequency | Tester | Status |
|---|---|---|---|---|
| CO-01 | Production batch jobs monitored; failures resolved within SLA | continuous | sample 25 / quarter | __ |
| CO-02 | Backups run per schedule; restores tested at least annually | nightly + annual restore | every restore | __ |
| CO-03 | Capacity & performance monitored; alerts on anomalies | continuous | quarterly | __ |
| CO-04 | Incident logs retained per retention policy + linked to root cause | per incident | sample / quarter | __ |
| CO-05 | DR / BC plan tested annually; gaps remediated | annual | every test | __ |

### 4. Program Development (system implementation / acquisition)
| Control | Description | Frequency | Tester | Status |
|---|---|---|---|---|
| PD-01 | System acquisitions and major upgrades go through documented project lifecycle | per project | sample / year | __ |
| PD-02 | UAT documented and signed off by business owner before go-live | per major release | every release | __ |
| PD-03 | Data conversion (e.g. system migration) reconciled to source totals | per migration | every migration | __ |
| PD-04 | Vendor / third-party assessments before integration with financial systems | per new vendor | every onboarding | __ |

## Test results — current period
| Control # | Sample size | Exceptions | Severity | Compensating control | Auditor sign-off |
|---|---|---|---|---|---|
| CM-01 | 25 | 0 | n/a | n/a | __ |
| LA-02 | 12 leavers | 1 (delayed 26h vs 24h SLA) | low | manual review caught it | __ |

## Material weakness / significant deficiency log
| Date | Description | Severity | Remediation | Status |
|---|---|---|---|---|
| | | | | |

## Sign-off
| Role | Name | Date |
|---|---|---|
| CFO | | |
| CIO | | |
| Internal Audit | | |
| External auditor | | |
