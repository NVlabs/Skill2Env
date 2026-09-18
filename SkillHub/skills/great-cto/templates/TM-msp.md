# TM-msp-{slug} — Managed Service Provider Threat Model

**Owner:** msp-reviewer
**ARCH ref:** docs/architecture/ARCH-{slug}.md
**Date:** {YYYY-MM-DD}
**Verdict:** signed-off | blocked

---

## 1. Scope

- **Platform type:** [ ] RMM  [ ] PSA  [ ] combined RMM+PSA  [ ] client-facing portal
- **Client count / scale:** …
- **Credential vaulting:** [ ] in scope  [ ] out of scope (delegated to external vault)
- **SOC 2 status:** [ ] Type 1  [ ] Type 2  [ ] not yet attested

## 2. Compliance applicability matrix

| Regime | Applies? | Reason |
|---|---|---|
| Multi-tenant client (credential/session) isolation | yes / no | … |
| SOC 2 for MSPs | yes / no | … |
| DPA / GDPR Art. 28 (processor) | yes / no | … |
| CIPP breach-notification chain | yes / no | … |
| SLA tracking (patch/backup) | yes / no | … |

## 3. Findings

### Critical

| ID | Finding | Mitigation | Gate |
|---|---|---|---|
| M-C-1 | … | … | gate:msp-controls |

### High

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

### Medium / Low

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

## 4. Required artefacts before senior-dev claims tasks

- [ ] Credential/session-level client isolation (not just data-level tenant isolation)
- [ ] Per-client credential vault (encrypted, MFA-gated, full retrieval audit log)
- [ ] RMM script-execution scoping + approval/audit trail per client
- [ ] Technician-to-client access mapping, explicit and per-client revocable
- [ ] Per-client SLA compliance tracking (patch cadence, backup restore-test verification)
- [ ] Multi-client incident-notification chain for platform-level compromise
- [ ] Incident records scoped to affected clients

## 5. EVAL suite required

- EVAL-msp-credential-isolation
- EVAL-msp-vault-access-audit
- EVAL-msp-rmm-script-scoping
- EVAL-msp-incident-notification-chain

## 6. Human gates

| Gate | Owner | Trigger |
|---|---|---|
| gate:msp-controls | security lead / MSP operations | after TM, before senior-dev |
| gate:ship | security-officer | standard |

<!-- HANDOFF -->
msp-reviewer-verdict: signed-off
critical-findings: 0
high-findings: 0
