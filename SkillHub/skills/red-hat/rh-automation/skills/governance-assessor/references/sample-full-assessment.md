# Sample Report: Full Governance Readiness Assessment

This sample shows the expected output when a user requests a full platform governance audit.
The report follows the output template defined in [governance-readiness.md](../../../docs/aap/governance-readiness.md).

---

## AAP Governance Readiness Report

**Assessment Date**: 2026-03-15
**AAP Instance**: aap.example.com
**Domains Assessed**: 7 + 1 bonus
**Scale Calibration**: Enterprise (3 inventories, 87 hosts across production, staging, and development)

**Documents Consulted**:
- [governance-readiness.md](docs/aap/governance-readiness.md) -- 7-domain assessment framework, Red Hat citations, decision tables

---

### Domain 1: Workflow Governance — GAP

Per Red Hat's *Automation Controller User Guide* (Ch. 9: Workflows):
> "Workflows enable you to configure a sequence of disparate job templates and link them together."

**Finding**: Found 0 workflow job templates and 14 standalone job templates. Workflow coverage ratio: 0%.
**Status**: GAP -- no workflow job templates exist
**Recommendation**: Per Red Hat's *Workflows* (Ch. 9): Create workflow job templates to wrap production job templates with approval nodes and failure-handling paths.
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/using_automation_execution/controller-workflows

---

### Domain 2: Notification Coverage — WARN

Per Red Hat's *Automation Controller User Guide* (Ch. 25: Notifications):
> "You can set notifications on job start and job end, including job failure."

**Finding**: Found 2 notification templates (1 Email, 1 Slack). However, neither is bound to any job template -- notifications exist but are unused.
**Status**: WARN -- notification templates exist but are not bound to job templates (depth query downgrade from initial PASS)
**Recommendation**: Per Red Hat's *Notifications* (Ch. 25): Bind notification templates to production job templates, at minimum for failure events.
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/using_automation_execution/controller-notifications

---

### Domain 3: Access Control (RBAC) — GAP

Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.2.1):
> "Use teams inside of organizations to assign permissions to groups of users rather than to users individually."

Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.1.2):
> "Minimize administrative accounts...restrict to the minimum set of users."

**Finding**: 6 users (2 superusers), 0 teams, 8 individual role assignments, 0 team role assignments.
**Status**: GAP -- no teams exist; all permissions assigned to individual users
**Recommendation**: Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.2.1): Create teams (e.g., `automation-operators`, `automation-admins`) and migrate individual role assignments to team-based assignments.
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/configuring_automation_execution/controller-security-best-practices

---

### Domain 4: Credential Security — WARN

Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.1.4):
> "Remove user access to credentials...credentials should be defined at the organization or team level."

Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.1.5):
> "Enforce separation of duties...different credentials for each piece of automation."

**Finding**: 3 credentials (2 Machine, 1 SCM), 2 credential types. Credential `ssh-prod` (ID: 5) is used across both staging and production job templates.
**Status**: WARN -- credentials exist but lack separation of duties across environments
**Recommendation**: Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.1.5): Create separate credentials per environment (e.g., `ssh-prod`, `ssh-staging`, `ssh-dev`).
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/configuring_automation_execution/controller-security-best-practices

---

### Domain 5: Execution Environments — PASS

Per Red Hat's *Creating and Consuming Execution Environments* (AAP 2.6):
> "Execution environments are container images that serve as Ansible control nodes."

**Finding**: 3 execution environments (2 custom, 1 default). Custom EEs use pinned image tags.
**Status**: PASS -- custom execution environments configured with pinned versions
**Recommendation**: No action needed. Continue using pinned image tags and consider implementing image signing.
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/creating_and_consuming_execution_environments

---

### Domain 6: Workload Isolation — PASS

Per Red Hat's *Configuring Automation Execution* (Ch. 17: Instance Groups):
> "Instance groups can be used to assign jobs to run on specific sets of instances."

**Finding**: 3 instance groups (`default`, `production`, `development`). Production and development workloads are separated.
**Status**: PASS -- workload isolation implemented between environments
**Recommendation**: No action needed. Consider setting `max_forks` limits on instance groups for capacity management.
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/using_automation_execution/controller-instance-groups

---

### Domain 7: Audit Trail — PASS

Per Red Hat's *Activity Stream* documentation:
> "The Activity Stream shows all changes and events in the automation controller."

**Finding**: 247 activity stream entries. Most recent: 2026-03-15T14:22:00Z. Active logging confirmed.
**Status**: PASS -- activity stream is operational with recent entries
**Recommendation**: No action needed. Consider configuring external log aggregation for long-term retention per Red Hat's *Hardening Guide*.
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/using_automation_execution/assembly-controller-activity-stream

---

### Bonus: External Authentication — WARN

Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.2.2):
> "Connecting to external account sources by LDAP, SAML 2.0, and certain OAuth providers."

**Finding**: 0 external authenticators configured. All 6 users authenticate locally.
**Status**: WARN -- no external authentication; local-only auth with 2 superusers
**Recommendation**: Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.2.2): Configure LDAP or SAML authentication to enforce centralized account management and MFA.
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/configuring_automation_execution/controller-security-best-practices

---

### Compound Risk Analysis

| Correlation | Domains | Finding | Elevated Recommendation |
|---|---|---|---|
| RBAC GAP + Credentials exist | 3 + 4 | Without teams, credentials are necessarily user-scoped | Fix RBAC first (create teams) to enable team-scoped credential management |
| No Workflows + Unbound Notifications | 1 + 2 | No governance controls AND no automated alerting on production failures | Highest-risk combination -- create at minimum a failure notification binding while workflows are built |
| Multiple superusers + local auth | 3 + Bonus | 2 superuser accounts without MFA have maximum blast radius | Configure external authentication to enforce MFA on superuser accounts |

---

### Summary

| Domain | Status | Key Finding |
|---|---|---|
| Workflow Governance | GAP | No workflow job templates; 14 standalone templates |
| Notification Coverage | WARN | 2 templates exist but not bound to any jobs |
| Access Control (RBAC) | GAP | No teams; all permissions individual |
| Credential Security | WARN | Credential shared across staging and production |
| Execution Environments | PASS | 2 custom EEs with pinned tags |
| Workload Isolation | PASS | Separate instance groups for prod/dev |
| Audit Trail | PASS | Active, 247 entries |
| External Authentication | WARN | Local-only, no MFA |

**Overall**: 3 PASS, 3 WARN, 2 GAP out of 8 domains assessed.

### Recommended Fix Order

1. **RBAC (Domain 3)** -- Foundation for team-scoped credentials and least-privilege access
2. **Workflows (Domain 1)** -- Enables approval gates and failure-handling paths
3. **Notification Bindings (Domain 2)** -- Bind existing templates to production jobs
4. **Credential Separation (Domain 4)** -- After teams exist, create per-environment credentials
5. **External Authentication (Bonus)** -- Enforce MFA for superuser accounts

### Sources Consulted

- Red Hat AAP 2.5 - Security Best Practices: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/configuring_automation_execution/controller-security-best-practices
- Red Hat AAP 2.5 - Workflows: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/using_automation_execution/controller-workflows
- Red Hat AAP 2.5 - Notifications: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/using_automation_execution/controller-notifications
- Red Hat AAP 2.5 - Instance Groups: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/using_automation_execution/controller-instance-groups
- Red Hat AAP 2.5 - Activity Stream: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/using_automation_execution/assembly-controller-activity-stream
- Red Hat AAP 2.6 - Execution Environments: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/creating_and_consuming_execution_environments
- Red Hat AAP 2.5 - RBAC: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/access_management_and_authentication/gw-managing-access
