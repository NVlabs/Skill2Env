# Archetypes — Pipeline Rules by Archetype

> 10 archetypes cover 95% of projects. Domain packs add depth for specialized needs.
> See TYPE_MAP.md for how 75+ specific types resolve to archetypes (internal).

## User-facing scales vs internal sizes

The CTO chats about three scales: `quick` / `standard` / `deep`. Agents read five internal sizes from PROJECT.md:

| User-facing | Internal `size:` values | When |
|-------------|------------------------|------|
| `quick` | `nano` OR `small` | Hotfix, typo, new endpoint, small feature |
| `standard` | `medium` (default) | Standard feature, new service |
| `deep` | `large` OR `enterprise` | Cross-cutting, regulated, arch migration |

`/start` writes the canonical internal name to PROJECT.md. Agents never need to know about the user-facing vocabulary.

For approvals: the CTO chooses `auto` or `review` (default); PROJECT.md stores `auto` / `gates-only` (canonical). Advanced levels (`strict` / `expert` / `step-by-step`) are opt-in, written verbatim.

## Archetype Definitions

Security gate is tier-based since v1.0.102 — see `references/security-tiers.md` for definitions.
Signals emitted by `senior-dev` (new deps, auth-path changes, PII columns, IAM diffs) can **upgrade** the tier at runtime.

| Archetype | Description | Default tier | Default compliance |
|-----------|-------------|--------------|-------------------|
| `web-service` | Backend APIs, web apps, full-stack | **baseline** (→ standard on auth/crypto signals) | OWASP Top 10, GDPR if EU users |
| `mobile-app` | Mobile, desktop, Electron apps | **baseline** (→ standard on payment/biometric signals) | OWASP MASVS, platform privacy |
| `ai-system` | Internal AI/ML: RAG, LLM ops, evals, voice, multimodal — not user-facing agents | **standard** (→ deep on MCP/tool-use) | EU AI Act check, model card |
| `agent-product` | User-facing autonomous agents built on Claude Agent SDK / LangGraph / CrewAI. Agent executes tools on behalf of end-users. | **deep** (always — user input controls tool execution) | OWASP LLM Top 10, EU AI Act, GDPR if storing memory |
| `data-platform` | Pipelines, warehouses, feature stores, analytics | **baseline** (→ standard on PII) | PII classification, data lineage |
| `infra` | IaC, K8s, platform engineering, DevOps tools | **standard** | CIS Benchmarks |
| `library` | SDKs, CLIs, compilers, plugins (consumed by other devs as a dependency) | **baseline** (never off — supply-chain floor) | OpenSSF Scorecard, SBOM |
| `devtools` | Developer platforms: API-first products, SDKs as the product, agent infra, RAG/eval platforms, IDE plugins | **standard** | OpenSSF Scorecard, OpenAPI/GraphQL stability |
| `browser-extension` | MV3 Chrome / Firefox / Safari / Edge extensions | **standard** (→ deep on host_permissions:<all_urls>) | Web Store review, CSP, host_permissions audit |
| `game` | Single/multi-player games, game engines, game services | **baseline** (→ deep on multiplayer + anti-cheat) | COPPA if <13, age ratings (ESRB/PEGI), accessibility |
| `commerce` | E-commerce, payments, SaaS platforms | **standard** (→ deep on PCI dep) | PCI-DSS, SOC2 |
| `web3` | Smart contracts, DeFi, exchanges, wallets | **deep** | SWC Registry, KYC/AML |
| `iot-embedded` | IoT devices, hardware drivers, edge computing | **deep** | ETSI EN 303 645 |
| `regulated` | GxP, critical infra, financial services, automotive | **deep** | Domain-specific (see pack) |

**Tier floor:** `baseline` (CVE + secret scan, ~2 min) runs on **every** pipeline, no exceptions. Previous "no gate" default for `library` is removed — supply-chain attacks made that default indefensible.

## QA Strategy by Archetype

| Archetype | Primary QA | Secondary QA | Default threshold |
|-----------|-----------|-------------|------------------|
| `web-service` | Unit + integration + E2E (Playwright) + OWASP scan | Load test (k6), contract test (Pact) | p95 < 200ms, coverage ≥ 80%, 0 OWASP critical |
| `mobile-app` | Unit + UI test + device matrix | Accessibility audit, perf profiling | Launch < 2s, crash rate < 0.1%, coverage ≥ 75% |
| `ai-system` | Eval suite (accuracy/F1/BLEU per task) + prompt regression + cost cap test | Bias/fairness audit, hallucination rate test | Accuracy ≥ baseline, cost ≤ 2× baseline, hallucination ≤ 2% |
| `agent-product` | Agent evals (task completion rate, tool accuracy) + prompt injection test suite + cost regression | Cross-user isolation test, loop bound verification, output filter test | Task completion ≥ 80%, 0 prompt injection bypasses, cost ≤ budget cap, 0 cross-user leaks |
| `data-platform` | Data contract validation + schema test + lineage audit | Freshness SLA, PII scan | 0 schema violations, lineage 100% traced, freshness ≤ SLA |
| `infra` | Terratest / `terraform plan` + CIS benchmark scan | DR failover drill, cost delta check | 0 CIS critical, plan matches intent, cost delta < 20% |
| `library` | Unit + cross-version compat matrix + semver check | Benchmark regression, bundle size | 0 breaking changes (unless major), coverage ≥ 90% |
| `devtools` | Unit + integration + SDK example test (each language) + OpenAPI/GraphQL contract test | API spec linting, SDK auto-gen verification, docs build | 0 breaking spec changes (unless major), SDK examples pass on all supported runtimes, docs build clean |
| `browser-extension` | Unit + content script test + MV3 service worker lifecycle test + cross-browser smoke | Web Store review pre-flight, host_permissions audit, performance profile | 0 Web Store policy violations, host_permissions justified, no eval/innerHTML on untrusted input |
| `game` | Unit + gameplay smoke (deterministic) + frame-time budget + memory profile per platform | Multiplayer netcode test (latency injection), anti-cheat verification, age-rating pre-flight | 60 FPS sustained on baseline device, no memory leaks across 1h play, multiplayer rollback recovers within N frames |
| `commerce` | Unit + E2E checkout flow + idempotency proof + PCI scan | Load test, reconciliation test | p95 < 200ms, 0 PCI findings, idempotency verified |
| `web3` | Unit + fuzz (Echidna) + static analysis (Slither) + formal verification | Economic attack sim, gas optimization | 0 Slither high/critical, fuzz 10k+ runs, formal spec verified |
| `iot-embedded` | QEMU/HIL test + OTA update test + ETSI checklist | Power profiling, field condition sim | 0 ETSI critical, OTA verified, memory < limit |
| `regulated` | Full compliance suite per domain (see enterprise-pack) | Pentest, audit trail completeness | 0 compliance violations, audit trail 100% |

## Deploy Method by Archetype

| Archetype | Deploy | Rollback |
|-----------|--------|----------|
| `web-service` | Canary (1%→5%→25%→100%) or blue-green | Previous container tag / git revert |
| `mobile-app` | Staged rollout (1%→10%→50%→100%) per app store | Rollback store version / feature flag disable |
| `ai-system` | Shadow mode → A/B test → full traffic | Previous model version / prompt rollback |
| `agent-product` | Feature flag off → 1% canary (monitor cost + errors) → 10% → 100%. Async agents via queue. | Disable feature flag / drain queue / roll back agent version |
| `data-platform` | Backfill → validate → promote | Restore previous pipeline version, re-run |
| `infra` | `terraform apply` / `helm upgrade` with plan review | `terraform apply` previous state / `helm rollback` |
| `library` | Publish to registry (staging tag → release tag) | Yank + publish previous version |
| `devtools` | API: canary 1%→5%→25%→100% on tenant boundaries. SDK: publish per language registry (npm/PyPI/crates/Maven/NuGet) on tag. Docs site: atomic deploy. | API: traffic-shift to previous version. SDK: yank + restore previous version, dispatch deprecation note via SDK telemetry. |
| `browser-extension` | Web Store staged rollout (1%→10%→50%→100%) per browser. Submit + wait for review (Chrome ~24h, Firefox ~24-72h, Safari ~7d, Edge ~24h). | Submit previous version as new build (Web Stores have no instant rollback). Pre-stage emergency previous build before risky release. |
| `game` | Console: certification → staged via store dashboard. PC (Steam): branch system (default branch + opt-in beta). Mobile: standard store rollout. Live-service: feature flag + remote config. | Roll back via store dashboard branch swap (Steam < 5min, console depends on cert). Live-service: feature flag off, drain matchmaking, hotfix patch. |
| `commerce` | Canary with transaction monitoring | Instant traffic shift to previous version |
| `web3` | Timelock → multisig → deploy (proxy upgrade if upgradeable) | Emergency pause / proxy downgrade |
| `iot-embedded` | OTA staged rollout (1%→10%→100% of devices) | OTA rollback to previous firmware |
| `regulated` | Validated deploy: approval chain → change control → deploy → verify | Documented rollback per compliance framework |

## Gates by Archetype × Size

| Gate | nano | small | medium | large | enterprise |
|------|------|-------|--------|-------|-----------|
| `gate:arch` | — | — | ✅ | ✅ | ✅ |
| `gate:code` | — | — | if strict | ✅ | ✅ |
| `gate:ship` | — | ✅ | ✅ | ✅ | ✅ |
| `gate:compliance` | — | — | — | — | ✅ |

Override: if archetype has `security gate: mandatory` → minimum `medium` size → always includes security-officer.

**Single source of truth for mandatory security gate** — archetypes with `mandatory` in the table above:
`ai-system`, `commerce`, `web3`, `iot-embedded`, `regulated`

**v1.0.102+ note:** per-type `security-gate:` overrides in TYPE_MAP.md are deprecated and
ignored. Tier derives from archetype + signals (see `references/security-tiers.md`). The
archetypes listed above are the only mandatory-security set; everything else runs at its
archetype default tier and upgrades on signal.

## Required Agents by Size

| Agent | nano | small | medium | large | enterprise |
|-------|------|-------|--------|-------|-----------|
| architect | — | ✅ | ✅ | ✅ | ✅ |
| senior-dev | ✅ | ✅ | ✅ | ✅ | ✅ |
| qa-engineer | — | ✅ lightweight | ✅ | ✅ | ✅ |
| security-officer | — | if mandatory | ✅ if mandatory | ✅ | ✅ |
| devops | — | ✅ simple | ✅ | ✅ canary | ✅ canary |
| l3-support | — | — | ✅ 15min | ✅ 30min | ✅ 60min+ |

### AI specialist subagents (v1.0.134+, ai-system / agent-product only)

| Subagent | nano | small | medium | large | enterprise | When invoked |
|---|---|---|---|---|---|---|
| ai-security-reviewer | — | ✅ | ✅ | ✅ | ✅ | security-officer pre-impl mode delegates here for AI archetypes |
| ai-prompt-architect | — | ✅ | ✅ | ✅ | ✅ | After threat model exists, when ARCH § LLM Scope identifies named LLM roles |
| ai-eval-engineer | — | ✅ | ✅ | ✅ | ✅ | After ADR-PROMPT files exist; qa-engineer Step 0b delegates EVAL creation |

Pipeline for `ai-system` / `agent-product`: architect → ai-security-reviewer → ai-prompt-architect → ai-eval-engineer → senior-dev → qa-engineer → security-officer post-impl → devops.

### Browser-extension specialist subagent (v1.0.136+)

| Subagent | When invoked | What it produces |
|---|---|---|
| web-store-reviewer | After architect writes ARCH for browser-extension archetype; security-officer pre-impl delegates here | TM-{slug}.md with permissions audit, single-purpose check, CSP audit, three-worlds isolation review, cross-browser compat review; ARCH § Web Store Pre-flight checklist |

Pipeline for `browser-extension`: architect → web-store-reviewer → senior-dev → qa-engineer (re-checks manifest static rules) → security-officer post-impl → devops (Web Store unlisted/internal channel).

### Commerce / Web3 / IoT specialist subagents (v1.0.143+)

| Subagent | Archetype | When invoked | What it produces |
|---|---|---|---|
| pci-reviewer | `commerce` | security-officer pre-impl delegates here | TM with PCI-DSS scope decision (SAQ-A vs SAQ-D), idempotency proof requirements, webhook signature validation, refund/dispute flow, SCA/PSD2 (EU), PSP failover |
| oracle-reviewer | `web3` | security-officer pre-impl delegates here | TM with subtype block-ship gate (lending → flash-loan-sim, AMM → k-invariant, bridge → cross-chain integrity), oracle strategy (Chainlink + Pyth + TWAP), MEV protection, upgradeability decision matrix, L2 resilience, custody/multisig, bug bounty TVL tier |
| firmware-reviewer | `iot-embedded` | security-officer pre-impl delegates here | TM with OTA strategy (signing + A/B partitions + auto-rollback + fleet rollout), ETSI EN 303 645 13 provisions, secure boot, HIL test design, wireless protocol security (BLE / Wi-Fi / Zigbee / Matter / LoRa), supply chain |

Pipeline for `commerce`: architect → pci-reviewer → senior-dev → qa-engineer (idempotency + PAN grep) → security-officer post-impl → devops (transaction monitoring canary).

Pipeline for `web3`: architect → oracle-reviewer → senior-dev → qa-engineer (Slither + Foundry fuzz) → security-officer post-impl → devops (timelock-gated proxy upgrade).

Pipeline for `iot-embedded`: architect → firmware-reviewer → senior-dev → qa-engineer (HIL/QEMU tests) → security-officer post-impl → devops (OTA staged rollout).

## Parameters (override archetype defaults via PROJECT.md)

These parameters customize behavior without changing archetype:

```yaml
# PROJECT.md — parameter section
archetype: web-service
approval-level: strict

# Compliance (additive — each adds checklist items)
compliance: [gdpr, pci-dss, hipaa, sox]

# Security (v1.0.102+ tier model — see references/security-tiers.md)
default-tier: standard            # override archetype's default tier (rarely needed)
tier-override-reason: "explain why" # mandatory when downgrading from archetype default

# Performance SLA (overrides archetype default)
performance-sla: p95 < 100ms

# QA extras (from domain packs — extend base QA)
qa-extras: [wer, ttfb, barge-in]  # voice-specific from ai-pack

# Cloud (triggers Well-Architected review in ARCH doc)
cloud: aws

# Domain pack (loads additional rules)
packs: [ai-pack, enterprise-pack]
```

### Parameter Resolution Order

1. **Archetype base** — default QA, deploy, thresholds from table above
2. **approval-level** — gates and checkpoints scaled per level
3. **compliance: []** — each value adds compliance checklist items to security-officer
4. **qa-extras: []** — each value adds QA checks to qa-engineer (from domain pack)
5. **Explicit overrides** — `performance-sla`, `security-gate`, `review_mode` override any default
6. **Domain pack** — `packs: [ai-pack]` loads additional type-specific depth

### Packs Auto-load Map

Each archetype auto-loads a domain pack when the archetype is detected. Multiple packs can be combined.

| Archetype | Auto-loaded pack | What the pack adds |
|-----------|------------------|--------------------|
| `web-service` | `web-pack` | Framework decision tree (Next/Nuxt/Hono/Fastify), ORM choice, edge runtime constraints, auth providers, perf budgets |
| `mobile-app` | `mobile-pack` | Native vs Flutter vs RN vs KMM decision, App Store / Play submission gotchas, MASVS V1-V8 detailed checklist, OTA update patterns |
| `ai-system` | `ai-pack` | LLM serving (vLLM/Ollama), prompt programming (DSPy/Instructor), evaluation (Ragas/Promptfoo/Braintrust), vector DBs |
| `agent-product` | `agent-pack` | OWASP LLM Top 10, agent constitution, budget cap, tool sandboxing, isolation, Langfuse observability |
| `data-platform` | `data-pack` | dbt/Dagster/Polars/DuckDB/Iceberg, lakehouse patterns, streaming, data quality |
| `infra` | `infra-pack` | Terraform/Pulumi/CDK decision, GitOps (ArgoCD/Flux), FinOps + Karpenter, secrets, observability stack |
| `library` | `library-pack` | OpenSSF Scorecard, npm provenance, PyPI Trusted Publishing, SBOM (Syft), semver enforcement, deprecation policy |
| `devtools` | `devtools-pack` | API-first design, OpenAPI/GraphQL spec stability, multi-language SDK quality, docs as product, deprecation channels, dev relations |
| `browser-extension` | `browser-extension-pack` | MV3 service worker, content script isolation, host_permissions audit, Web Store review pre-flight, cross-browser compat |
| `game` | `game-pack` | Engine choice (Unity/Unreal/Godot/custom), multiplayer netcode (rollback/lockstep), anti-cheat, monetization (IAP/loot box compliance), platform certifications, age ratings |
| `commerce` | `commerce-pack` | Stripe/Adyen/Paddle decision, subscription billing, idempotency, fraud detection, PCI-DSS scope reduction, tax |
| `web3` | `web3-pack` | Slither/Echidna/Foundry/Certora, KYC/AML, custody (HSM/MPC/Shamir), MEV protection |
| `iot-embedded` | (no dedicated pack — use detection signals) | platformio.ini, Zephyr (`west.yml`), ESP-IDF detected from filesystem |
| `regulated` | `enterprise-pack` | DORA, NIS2, GxP/21CFR11, ISO 27001, TISAX detailed checklists |

**Multi-pack combinations** — common stacking patterns:

- `[ai-pack, enterprise-pack]` — regulated AI system (e.g. healthcare diagnosis)
- `[web-pack, commerce-pack]` — SaaS with checkout
- `[mobile-pack, commerce-pack]` — mobile app with in-app purchases
- `[infra-pack, enterprise-pack]` — regulated infrastructure (financial services, critical infra)
- `[library-pack, ai-pack]` — open-source LLM SDK

### Parameter Values

| Value | What it adds |
|-------|-------------|
| `gdpr` | Privacy notice, consent mechanism, right-to-erasure, DPIA |
| `pci-dss` | PCI-DSS SAQ-D checklist (custom card-handling), TLS audit, MFA enforcement |
| `pci-dss-saq-a` | PCI-DSS SAQ-A (fully outsourced via Stripe Elements / hosted fields): tokenization-only verification, no PAN in logs grep scan, third-party validation |
| `pci-dss-saq-a-ep` | PCI-DSS SAQ-A-EP (direct-post / iframe): SAQ-A controls + script-injection protection (CSP, SRI, no inline JS on payment pages) |
| `hipaa` | PHI isolation, access log, BAA verification |
| `sox` | SOX ITGC: change management, logical access, computer ops, SoD |
| `soc2` | Access controls, audit logging, encryption at rest + transit |
| `iso27001` | Annex A 93 controls, SoA, risk register, internal audit |
| `dora` | ICT risk assessment, third-party register, TLPT, incident classification |
| `nis2` | Article 21 measures, Article 23 reporting, supply chain security |
| `21cfr11` | Electronic records, signatures, IQ/OQ/PQ, audit trail, CAPA |
| `tisax` | VDA ISA checklist, AL determination, prototype protection |
| `togaf` | ADM phase mapping in ARCH doc |
| `eu-ai-act` | Annex III high-risk check, conformity assessment, EUAI database |
| `tcpa` | Call recording consent, opt-out, autodial restrictions |
| `ccpa` | California privacy rights, opt-out of sale |
| `casl` | Canadian anti-spam, express consent |
| `eu-vat` | EU VAT OSS scheme, VAT-ID validation, reverse-charge B2B handling, quarterly OSS return |
| `consumer-rights-directive` | EU 14-day right of withdrawal, pre-contract disclosures, cancel-anytime UX |
| `csp` | Content-Security-Policy header audit, no `unsafe-eval` / `unsafe-inline`, SRI on external scripts |
| `mv3-security` | Manifest V3 specifics: service-worker lifecycle, declarativeNetRequest, no remote code, host-permissions justification |
| `age-rating` | ESRB / PEGI / USK / CERO / IARC questionnaire submitted; rating displayed in store listing |
| `accessibility` | CVAA (US) + EAA (EU) checklist: subtitle support, remappable controls, color-blind modes, no flicker |
| `coppa` | US under-13 protections: parental consent, no behavioural ads, restricted chat |
| `openssf` | OpenSSF Scorecard ≥ 7, npm provenance, PyPI Trusted Publishing, signed releases |
| `api-stability` | OpenAPI / GraphQL spec linting, no breaking changes in MINOR/PATCH, deprecation channel |
| `soc2-type-2` | SOC 2 Type II: 6+ months continuous evidence collection, access reviews, change management |

## Domain Overlays (Wave 1-4 specialised reviewers)

> Overlay packs ride on top of existing archetypes via `applies_to + applies_when` instead of creating new archetypes. Loaded automatically when ARCH or PROJECT.md mentions the trigger signals listed below.

| Pack | Reviewer(s) | Triggers on | Base archetypes | Human gates added |
|---|---|---|---|---|
| `voice-pack` | voice-ai-reviewer | twilio, vonage, livekit, deepgram, elevenlabs, ivr, telephony, tts/stt | ai-system, agent-product | gate:voice-compliance |
| `hr-ai-pack` | hr-ai-reviewer | recruit, hiring, candidate, resume, interview, ATS, performance review, workforce scheduling | ai-system, agent-product, enterprise | gate:aedt-audit |
| `api-platform-pack` | api-platform-reviewer | public API, partner API, REST, GraphQL, gRPC, webhook, SDK, OpenAPI, dev portal | devtools, library, ai-system, agent-product, web-service | gate:api-contract |

### Activation logic

Overlays are loaded by `architect` when running discovery:

1. Read ARCH-{slug}.md + PROJECT.md
2. For each pack, run its trigger regex (defined in `skills/great_cto/packs/*-pack.md` and the corresponding reviewer agent's `Step 0`).
3. If signals present → invoke reviewer(s) → write `TM-{type}-{slug}.md` → emit HANDOFF → block `senior-dev` until human-gates listed above are cleared.

### Human-gate summary (per overlay)

24 new gate types added by Wave 1-4 overlays, layered on top of existing `gate:plan` / `gate:ship` / `gate:promote`:

| Gate | Set by | Cleared by | Triggered when |
|---|---|---|---|
| `gate:voice-compliance` | voice-ai-reviewer | regulatory lead | voice pack active |
| `gate:aedt-audit` | hr-ai-reviewer | independent auditor | NYC LL 144 in scope (annual) |
| `gate:api-contract` | api-platform-reviewer | architect + DX-lead | before v1 GA |

