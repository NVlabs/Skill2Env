---
name: msp-pack
description: Multi-client blast-radius and credential-vaulting overlay for Managed Service Provider (MSP) platforms. Pairs with enterprise-saas-reviewer (standard tenant baseline) and msp-reviewer (client-isolation threat model).
when_to_use: Product is an RMM/PSA platform or otherwise gives one operator privileged remote access across many distinct downstream client environments.
applies_to:
  - enterprise-saas
  - devtools
extends:
  - enterprise-saas-pack    # baseline tenant/access-log controls
---

# MSP Compliance Pack

> Loaded automatically when ARCH or PROJECT.md mentions: msa, sla, rmm, psa, multi-tenant,
> managed service (provider), credential vault.
> Routes through `msp-reviewer` (threat model) + adds client-isolation gates.

## Reviewer

- **msp-reviewer** runs BEFORE senior-dev → writes `TM-msp-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:msp-controls` | After TM, before senior-dev claims tasks | Security lead / MSP operations |
| `gate:ship` | Standard | security-officer |

## Required artefacts in every MSP project

| Artefact | Location | Owner |
|---|---|---|
| Credential/session-level client isolation | `src/msp/isolation/` | senior-dev |
| Per-client credential vault | `src/msp/vault/` | senior-dev |
| RMM script-execution scoping + audit trail | `src/msp/rmm/` | senior-dev |
| Technician-to-client access mapping | `src/msp/access-map/` | senior-dev |
| Per-client SLA tracker (patch/backup) | `src/msp/sla/` | senior-dev |
| Multi-client incident-notification chain | `src/msp/incident-notify/` | senior-dev |

## EVAL suite (in addition to enterprise-saas-pack QA)

- `EVAL-msp-credential-isolation` — technician session on Client A cannot reach Client B
- `EVAL-msp-vault-access-audit` — every credential retrieval logged with who/when/client
- `EVAL-msp-rmm-script-scoping` — script execution blocked outside technician's client roster
- `EVAL-msp-incident-notification-chain` — platform-level incident triggers all-affected-client alert

## The Kaseya lesson (why isolation ≠ data-tenancy)

Standard SaaS multi-tenancy isolates *data*. An MSP platform additionally grants *remote execution*
across every managed client — the 2021 Kaseya VSA ransomware incident propagated through exactly this
pattern: one compromised RMM instance became a supply-chain attack against every downstream MSP client
simultaneously. Treat credential/session isolation as a distinct, higher-severity control from data
isolation.

## References

See `agents/msp-reviewer.md` for full regulatory citations.
