# Sample Report: Scoped Governance Assessment (Credentials + RBAC)

This sample shows the expected output when a user requests a scoped assessment
targeting specific governance domains. The report follows the output template
defined in [governance-readiness.md](../../../docs/aap/governance-readiness.md).

---

## AAP Governance Assessment: Credential Security + Access Control

**Assessment Date**: 2026-03-15
**AAP Instance**: aap.example.com
**Scope**: Domain 3 (Access Control / RBAC) + Domain 4 (Credential Security)
**Scale Calibration**: Small team (1 inventory, 5 hosts, development only)

**Documents Consulted**:
- [governance-readiness.md](docs/aap/governance-readiness.md) -- Domains 3 and 4 assessment criteria, Red Hat citations

---

### Domain 3: Access Control (RBAC) — PASS

Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.2.1):
> "Use teams inside of organizations to assign permissions to groups of users rather than to users individually."

Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.1.2):
> "Minimize administrative accounts...restrict to the minimum set of users."

**Finding**: 3 users (1 superuser), 2 teams (`dev-operators`, `dev-admins`), 0 individual role assignments, 4 team role assignments. All access is team-based.
**Status**: PASS -- team-based access control implemented; single superuser is acceptable for development
**Recommendation**: No action needed for current scale. If promoting to production, review whether `dev-admins` team permissions follow least privilege.
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/configuring_automation_execution/controller-security-best-practices

---

### Domain 4: Credential Security — WARN

Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.1.4):
> "Remove user access to credentials...credentials should be defined at the organization or team level."

Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.1.5):
> "Enforce separation of duties...different credentials for each piece of automation."

**Finding**: Found 2 credentials, both of type "Machine." Credential `ssh-key` (ID: 3) is used across both dev and staging job templates.
**Status**: WARN -- credentials exist but lack separation of duties
**Recommendation**: Per Red Hat's *Security Best Practices* (Ch. 15, Sec. 15.1.5): Create separate credentials per environment. For current dev-only scale this is low severity, but address before production promotion.
**Source URL**: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/configuring_automation_execution/controller-security-best-practices

---

### Cross-Domain Correlation

| Correlation | Domains | Finding |
|---|---|---|
| RBAC PASS + Credentials WARN | 3 + 4 | Teams exist (good), but shared credentials across environments reduce the benefit of team scoping. Once credentials are separated, assign them to specific teams for full isolation. |

---

### Summary

| Domain | Status | Key Finding |
|---|---|---|
| Access Control (RBAC) | PASS | Team-based access, single superuser |
| Credential Security | WARN | Shared credential across environments |

**Assessed**: 1 PASS, 1 WARN out of 2 domains.

Would you like me to run the full 7-domain assessment for complete coverage?

### Sources Consulted

- Red Hat AAP 2.5 - Security Best Practices: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/configuring_automation_execution/controller-security-best-practices
- Red Hat AAP 2.5 - RBAC: https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.6/html/access_management_and_authentication/gw-managing-access
