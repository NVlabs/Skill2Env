---
name: secure-sdlc
description: Secure SDLC mapping: which security activity at which phase (threat model at ARCH, SAST at impl, pen-test at release), gates between phases
when_to_use: AI/agent/commerce/web3/iot/regulated archetypes. Read by architect + security-officer
applies_to:
  - ai-system
  - agent-product
  - commerce
  - web3
  - iot-embedded
  - regulated
  - fintech
  - browser-extension
---

# Secure SDLC — reference

Mapping of great_cto components to NIST SSDF (SP 800-218), SLSA, and EU DORA practices. Use this as the authoritative crosswalk when an auditor or CTO asks "how does great_cto cover X?"

## Why this mapping exists

Security isn't a phase — it's a thread through the pipeline. This reference documents **where** each secure-SDLC practice lives so a new contributor can find it, and an auditor can trace it. great_cto does not promise certification readiness; it promises a honest, documented, defensible workflow.

## Framework coverage at a glance

| Framework | Version | Coverage |
|---|---|---|
| **NIST SSDF** | SP 800-218 (Feb 2022) | ~65% — core PS / PW / RV practices |
| **SLSA** | v1.0 | L1–L2 achievable; L3+ requires external infra |
| **EU DORA** | Reg. 2022/2554 | Partial — ICT risk, incident response, third-party register |
| **OWASP SAMM** | v2 | informational — not explicitly mapped |
| **ISO 27001** | 2022 | advisory — core clauses referenced, Annex A partial |

## SSDF practice mapping

SSDF organises practices into four groups: **PO** (Prepare Org), **PS** (Protect Software), **PW** (Produce Well-Secured Software), **RV** (Respond to Vulnerabilities). Only PS/PW/RV are in scope for great_cto (PO is organisational policy outside the tool).

### PS — Protect the Software itself

| Practice | Required output | great_cto component | Status |
|---|---|---|---|
| **PS.1** Protect all forms of code | version control, backups | git + `.great_cto/` artefacts committed | ✓ |
| **PS.2** Provide a mechanism to verify software release integrity | hash/signature on release | `/sbom` + release SBOM artefact (v1.0.94) | ◐ (no signing yet) |
| **PS.3** Archive & protect each software release | retain build artefacts + provenance | `docs/releases/RELEASE-*.md` + `SBOM-<version>.json` | ◐ (no attestation) |

### PW — Produce Well-Secured Software

| Practice | Required output | great_cto component | Status |
|---|---|---|---|
| **PW.1** Design software to meet security requirements & mitigate risks | threat model, security requirements | `/threat-model` + `## Security` section in ARCH-*.md (v1.0.94) | ✓ |
| **PW.2** Review the design for compliance | design review | `security-officer` reviews ARCH pre-merge | ✓ |
| **PW.4** Reuse existing well-secured software | SBOM + vulnerability scan of deps | `/audit` dep scan + `/sbom` (v1.0.94) | ◐ |
| **PW.5** Create source code adhering to secure coding practices | secure coding standards, code review | `senior-dev` + `code-review` (11-angle) + OWASP lens | ✓ |
| **PW.6** Configure compilation & build processes to improve executable security | harden build | out of scope for framework; documented in archetype | ◐ |
| **PW.7** Review and/or analyse human-readable code | code review (SAST) | `security-officer` runs SAST per archetype | ◐ (no baseline yet) |
| **PW.8** Test executable code (DAST, fuzzing) | dynamic testing | `qa-engineer` runs integration + perf; DAST/fuzzing by archetype | ◐ |
| **PW.9** Configure software to have secure settings by default | secure defaults | archetype templates ship with secure defaults | ✓ |

### RV — Respond to Vulnerabilities

| Practice | Required output | great_cto component | Status |
|---|---|---|---|
| **RV.1** Identify & confirm vulnerabilities on an ongoing basis | CVE monitoring, dep scan | `/audit` CVE scan (cached 24h) | ✓ |
| **RV.2** Assess, prioritise, and remediate vulnerabilities | triage + fix | `l3-support` for prod issues, `security-officer` for pre-deploy | ✓ |
| **RV.3** Analyse vulnerabilities to identify root causes | postmortem | `PM-*.md` + Agent Verdict Audit + pattern library | ✓ |

## SLSA mapping

SLSA levels (v1.0) define supply-chain integrity guarantees.

| Level | Requirements | great_cto status |
|---|---|---|
| **L1** — documented build process | Build reproducibly, produce provenance | ✓ with `/sbom` (v1.0.94) |
| **L2** — authenticated provenance | Build runs on hosted service, produces signed attestation | ◐ — requires GitHub Actions / Buildkite with OIDC. Scaffold in archetype. |
| **L3** — source + build hardening | Isolated build, non-falsifiable provenance | out of scope — external infra |
| **L4** — two-party review, reproducible | — | out of scope |

**Practical stance:** great_cto targets **SLSA L1–L2**. `devops` agent emits SBOM on every production deploy (L1); archetype templates include CI config that produces signed provenance via cosign + OIDC if the team wants L2.

## DORA mapping (EU Digital Operational Resilience Act)

Applies to financial entities in the EU from January 2025. Partial coverage — full compliance requires legal/operational steps outside great_cto.

| DORA article | What it requires | great_cto component | Status |
|---|---|---|---|
| **Art. 5–15** ICT risk management framework | documented risk framework | `docs/risks/RISK-REGISTER.md` + archetype pre-mortem | ◐ (no ICT-specific categories yet) |
| **Art. 17–23** ICT incident reporting | classify + notify within 24h/72h/1mo | `PM-*.md` (ops) — `PM-SEC-*.md` planned for v1.0.95 | ✗ (planned) |
| **Art. 24–27** Operational resilience testing | regular testing, TLPT every 3y for significant | manual; pentest cadence documented in archetype | ◐ |
| **Art. 28–44** ICT third-party risk | register + exit strategy + SLA | `docs/vendors/VENDOR-*.md` with criticality + exit-strategy + SLA (v1.0.94) | ✓ |
| **Art. 45** Information sharing | threat intel exchange | out of scope | ✗ |

## What's explicitly **out of scope**

great_cto will not:

- Claim compliance certification for any framework
- Auto-submit regulatory notifications (DORA Art. 19, GDPR Art. 33) — these are legal acts, not engineering acts
- Replace a dedicated security team for regulated-sector entities
- Provide immutable/tamper-evident audit log (requires external signing infrastructure)

## Consumer agents

| Agent | Reads this file to... |
|---|---|
| `architect` | decide whether `## Security` section is mandatory in ARCH, invoke `/threat-model` |
| `security-officer` | verify every SSDF practice has evidence before gate vote |
| `devops` | invoke `/sbom` on production deploy |
| `l3-support` | classify security vs ops incidents |
| `/audit` | cross-reference deps with SBOM + vendor register |

## Evolution

This reference is updated as new commands/agents add coverage. Every v1.0.x release that touches security should update the Status column here and reference the framework practice in the CHANGELOG.
