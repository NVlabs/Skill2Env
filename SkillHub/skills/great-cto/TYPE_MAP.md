# Type → Archetype Mapping

> **Internal dispatch table — users never pick types manually.**
> `/start` and `/audit` detect the specific type from description/dependencies, then resolve to one of 13 archetypes + default parameters.
> Agents read `archetype:` from PROJECT.md — the specific type is a stepping stone, not user-facing config.

## Type Detection Keywords

`/start` scores CTO's description against these keyword lists to pick the primary type.

| Keywords | Type |
|----------|------|
| web, fullstack, Next.js, React+backend | `web-fullstack` |
| SPA, single page, Vite, Vue, Angular | `spa-frontend` |
| SSR, Remix, Nuxt, Astro | `ssr-app` |
| static site, Hugo, Gatsby, 11ty, landing page | `static-site` |
| docs, Docusaurus, MkDocs, VitePress | `docs-site` |
| REST API, FastAPI, Express, backend service, HTTP API | `rest-api` |
| GraphQL, Apollo, Hasura, subscriptions | `graphql-api` |
| gRPC, protobuf, RPC | `grpc-service` |
| serverless, Lambda, Cloudflare Workers, edge function | `serverless` |
| microservices, service mesh, Istio, distributed system | `microservices` |
| mobile, iOS, Android, React Native, Flutter app, Swift | `mobile` |
| desktop app, Tauri, WPF, native desktop (not Electron) | `desktop-app` |
| browser extension, Chrome ext, Firefox addon | `browser-extension` |
| VS Code extension, IDE plugin, LSP | `vscode-extension` |
| Electron, cross-platform desktop, Electron+Angular | `electron-app` |
| ML training, PyTorch, fine-tune, model training | `ml-training` |
| inference, ML serving, prediction API, TensorRT | `ml-serving` |
| ETL, Airflow, Spark, data ingestion, pipeline | `data-pipeline` |
| dashboard, D3, Plotly, charts, data visualization | `data-visualization` |
| AI agent, LangChain, autonomous agent, multi-agent | `ai-agent` |
| user-facing agent, Claude Agent SDK, agent product, personal assistant AI, AI copilot, AI assistant app, agent app, agentic product | `agent-product` |
| LangGraph agent, CrewAI, AutoGen agent, multi-agent product, agent-as-a-service | `agent-product` |
| RAG, retrieval, vector DB, embeddings, semantic search | `rag-system` |
| Terraform, Pulumi, IaC, cloud infra, infrastructure as code | `infra-iac` |
| GitHub Actions, CI/CD tool, workflow automation, DevOps tool | `devops-tool` |
| migration, schema change, Flyway, Alembic, database migration | `db-migration` |
| monorepo, Turborepo, Nx, workspace, pnpm workspace | `monorepo` |
| K8s operator, CRD, Kubebuilder, controller | `k8s-operator` |
| Solidity, smart contract, blockchain, EVM | `smart-contract` |
| trading bot, quant, backtest, algorithmic trading, exchange | `trading-bot` |
| DeFi, protocol, AMM, lending, yield, liquidity | `defi-protocol` |
| payment, Stripe, billing, PCI, checkout | `payment-service` |
| WebSocket, realtime, broadcast, presence, live updates | `realtime-system` |
| Kafka, RabbitMQ, message queue, NATS, pub/sub, event bus | `messaging-queue` |
| video, WebRTC, HLS, live streaming, media | `video-streaming` |
| SaaS, multi-tenant, subscription product, B2B platform | `saas-platform` |
| auth, OAuth, OIDC, SSO, identity provider, login | `auth-service` |
| e-commerce, shop, cart, Shopify, checkout flow | `e-commerce` |
| CMS, Strapi, Contentful, headless CMS | `cms-headless` |
| search, Elasticsearch, Meilisearch, full-text search | `search-service` |
| library, SDK, npm package, PyPI package, crate | `library-sdk` |
| CLI, command line tool, terminal tool | `cli-tool` |
| compiler, parser, AST, language implementation | `compiler-lang` |
| WordPress plugin, PHP plugin, WP extension | `wordpress-plugin` |
| embedded, firmware, IoT, RTOS, ESP32, microcontroller | `embedded-iot` |
| kernel driver, device driver, FPGA, ring-0 | `hardware-driver` |
| game, Unity, Unreal, Godot, game engine | `game` |
| evals, LLMOps, model registry, prompt regression | `llm-ops` |
| Snowflake, BigQuery, dbt, Redshift, data warehouse | `data-warehouse` |
| admin panel, internal tool, internal dashboard, Retool, Appsmith | `internal-tool` |
| push notifications, email service, SMS, SendGrid, transactional email | `notification-service` |
| IDP, Backstage, developer portal, golden path, platform engineering | `platform-engineering` |
| MCP server, model context protocol, tool server, Claude tool | `mcp-server` |
| stack migration, EOL upgrade, PHP upgrade, Node upgrade, Python 2 to 3, Angular migration, strangler fig, runtime EOL | `stack-migration` |
| large refactor, mass rename, architectural refactoring, >50 files, monolith decomposition, extract service, boundary refactor | `large-scale-refactor` |
| AI agent framework, LangGraph, CrewAI, AutoGen, multi-agent framework | `ai-agent-framework` |
| AI orchestrator, agent orchestrator, multi-agent orchestration, agent router, workflow orchestrator, agent coordinator | `ai-agent-framework` |
| BFF, backend for frontend, API gateway per client, client-specific backend | `bff` |
| feature flags, LaunchDarkly, Unleash, flag service, feature toggles | `feature-flags-service` |
| Chrome extension MV3, Manifest V3, service worker extension, Chromium ext | `chrome-extension-mv3` |
| custody, MPC wallet, HSM wallet, cold storage, hot wallet, multi-sig wallet, key management, Fireblocks | `custody-wallet` |
| computer vision, image classification, object detection, segmentation, YOLO, OpenCV, Detectron2, OCR, image model | `computer-vision` |
| recommendation engine, collaborative filtering, content-based filtering, matrix factorization, RecSys, two-tower model, ranking model | `recommendation-engine` |
| feature store, Feast, Tecton, Hopsworks, feature registry, point-in-time, online/offline features, feature pipeline | `feature-store` |
| time series, forecasting, Prophet, N-BEATS, temporal fusion transformer, demand forecasting, anomaly in time series | `time-series-forecasting` |
| anomaly detection, fraud detection, outlier detection, log anomaly, AIOps, unsupervised detection, isolation forest | `anomaly-detection` |
| cross-chain bridge, lock-and-mint, light client, relayer, bridge validator, cross-chain messaging, LayerZero, Wormhole, Stargate | `bridge-protocol` |
| centralized exchange, CEX, spot trading, futures exchange, order book exchange, white-label exchange, trading platform | `cex-exchange` |
| critical infrastructure, NIS2, operator of essential services, OES, energy grid, water treatment, transport network, essential service | `critical-infrastructure` |
| DORA, digital operational resilience, financial entity, investment firm, credit institution, ICT risk management, MiFID firm | `financial-services` |
| GxP, 21 CFR Part 11, electronic records, electronic signatures, pharma, biotech, clinical trials, LIMS, ELN, MES, validated system | `gxp-system` |
| ISO 27001, ISMS, information security management system, Statement of Applicability, SoA, Annex A, ISMS scope | `iso27001-scope` |
| TISAX, automotive supplier, VDA ISA, BMW supplier, Mercedes supplier, Volkswagen supplier, prototype protection, AL1, AL2, AL3 | `automotive-supplier` |
| voice agent, voice AI, VAPI, ElevenLabs conversational, Retell AI, voice bot, telephony AI, real-time voice, call center AI | `voice-agent` |
| digital health, mHealth, wearable app, fitness AI, wellness AI, personalised training, heart rate AI, HRV, sleep tracking AI, mental health app, mental wellness, wellbeing app, stress detection, burnout AI, mindfulness AI | `digital-health` |
| wearable integration, Apple Watch, Apple HealthKit, Garmin, Samsung Health, Google Fit, Health Connect, Polar, Fitbit, Whoop, Oura Ring, biometric sync, sensor telemetry | `wearable-platform` |
| nutrition AI, supplement recommendation, personalised nutrition, diet AI, macros AI, meal plan AI, supplement stack | `nutrition-ai` |
| physician HITL, doctor in the loop, clinical review workflow, physician review, human-in-the-loop healthcare, teleconsultation AI, remote patient monitoring, RPM | `clinical-hitl` |
| digital therapeutics, DTx, prescription digital therapeutics, evidence-based app therapy, CBT app, DBT app, exposure therapy app | `digital-therapeutics` |
| edge app, Cloudflare Workers, Deno Deploy, Vercel Edge, Fastly Compute, edge function, edge-first, edge runtime | `edge-app` |
| multimodal, vision + text, audio + text, GPT-4o app, Claude vision, Gemini multimodal, multi-modal AI, image understanding app | `multimodal-app` |
| API platform, public API, developer API, REST platform, OpenAPI-first, API-as-a-product | `api-platform` |
| SDK, multi-language SDK, client libraries, Stainless, openapi-generator, API client | `sdk-platform` |
| developer tool, dev productivity, IDE plugin platform, CLI platform, debugger, observability tool, dev infra | `developer-tools` |
| agent platform, agent infrastructure, agent runtime, multi-tenant agents, agent-as-a-service infrastructure | `agent-platform` |

## Mapping Table

| Specific type | Archetype | Default params | Overrides |
|--------------|-----------|---------------|-----------|
| `rest-api` | `web-service` | compliance: [owasp-api] |  |
| `graphql-api` | `web-service` | compliance: [owasp-api], qa-extras: [depth-limit, complexity-limit] |  |
| `grpc-service` | `web-service` | compliance: [owasp-api] |  |
| `bff` | `web-service` | compliance: [owasp-api] |  |
| `web-fullstack` | `web-service` | compliance: [owasp, gdpr-cookie] |  |
| `spa-frontend` | `web-service` | compliance: [owasp, gdpr-cookie, csp] |  |
| `ssr-app` | `web-service` | compliance: [owasp, csp] |  |
| `static-site` | `web-service` |  |   |
| `docs-site` | `web-service` |  |   |
| `cms-headless` | `web-service` | compliance: [owasp] |  |
| `internal-tool` | `web-service` | compliance: [rbac] |  |
| `realtime-system` | `web-service` | performance-sla: p95 < 50ms |  |
| `notification-service` | `web-service` | compliance: [can-spam, gdpr, casl] |  |
| `messaging-queue` | `web-service` | qa-extras: [message-ordering, idempotency] |  |
| `search-service` | `web-service` | qa-extras: [relevance-eval] |  |
| `feature-flags-service` | `web-service` | qa-extras: [flag-consistency] |  |
| `microservices` | `web-service` | qa-extras: [contract-test] |  |
| `serverless` | `web-service` | qa-extras: [cold-start] |  |
| `mobile` | `mobile-app` | compliance: [owasp-masvs, att, play-api-34] |  |
| `electron-app` | `mobile-app` | compliance: [electron-security] |  |
| `desktop-app` | `mobile-app` |  |  |
| `browser-extension` | `browser-extension` | compliance: [csp, mv3-security], packs: [browser-extension-pack] |  |
| `chrome-extension-mv3` | `browser-extension` | compliance: [csp, mv3-security], packs: [browser-extension-pack] |  |
| `vscode-extension` | `library` | compliance: [openssf], packs: [library-pack] | IDE plugins ship as marketplace packages, not browser extensions |
| `ai-agent` | `ai-system` | compliance: [eu-ai-act] |   |
| `agent-product` | `agent-product` | compliance: [owasp-llm, eu-ai-act], packs: [agent-pack] |  |
| `ai-agent-framework` | `ai-system` | compliance: [eu-ai-act] |  |
| `rag-system` | `ai-system` | compliance: [eu-ai-act], qa-extras: [retrieval-quality] |  |
| `mcp-server` | `ai-system` | qa-extras: [tool-injection, schema-enforcement] |   |
| `llm-ops` | `ai-system` | compliance: [eu-ai-act], qa-extras: [prompt-regression, cost-cap] |  |
| `ml-training` | `ai-system` | qa-extras: [bias-audit, data-poisoning, model-card] |  |
| `ml-serving` | `ai-system` | qa-extras: [drift-monitoring, model-card] |  |
| `computer-vision` | `ai-system` | qa-extras: [edge-compat, model-card, bias-audit] |  |
| `recommendation-engine` | `ai-system` | qa-extras: [popularity-bias, diversity, model-card] |  |
| `anomaly-detection` | `ai-system` | qa-extras: [false-positive-rate, threshold-justification] |  |
| `voice-agent` | `ai-system` | compliance: [tcpa, gdpr-biometric], qa-extras: [wer, ttfb, barge-in] |   |
| `multimodal-app` | `ai-system` | compliance: [eu-ai-act], qa-extras: [per-modality-accuracy, hallucination, cross-modal] |   |
| `data-pipeline` | `data-platform` |  |  |
| `data-warehouse` | `data-platform` | compliance: [pii-classification, data-lineage] |  |
| `data-visualization` | `data-platform` | qa-extras: [snapshot-regression] |  |
| `feature-store` | `data-platform` | qa-extras: [point-in-time, online-offline-consistency] |  |
| `time-series-forecasting` | `data-platform` | qa-extras: [backtest-validation] |  |
| `infra-iac` | `infra` | deploy-method: terraform, qa-extras: [checkov, tfsec] |  |
| `k8s-operator` | `infra` | deploy-method: helm, compliance: [cis-k8s] |  |
| `platform-engineering` | `infra` | deploy-method: terraform |  |
| `devops-tool` | `infra` |  |  |
| `db-migration` | `infra` | qa-extras: [rollback-dry-run, schema-diff] |  |
| `edge-app` | `infra` | qa-extras: [cold-start-50ms, bundle-1mb, no-nodejs-api, multi-region-latency] |  |
| `library-sdk` | `library` | compliance: [openssf], qa-extras: [semver, cross-version-compat] |  |
| `cli-tool` | `library` |  |  |
| `compiler-lang` | `library` | qa-extras: [cross-version-compat, benchmark-regression] |  |
| `wordpress-plugin` | `library` | compliance: [owasp] |  |
| `game` | `game` | compliance: [coppa, age-rating, accessibility], qa-extras: [fps-benchmark, memory-profiling, netcode, anti-cheat], packs: [game-pack] |  |
| `e-commerce` | `commerce` | compliance: [pci-dss, owasp] |   |
| `payment-service` | `commerce` | compliance: [pci-dss, sox] | min-size: enterprise |
| `saas-platform` | `commerce` | compliance: [soc2] |   |
| `auth-service` | `commerce` | compliance: [owasp-auth] |   |
| `smart-contract` | `web3` |  |   |
| `defi-protocol` | `web3` | qa-extras: [formal-verification, flash-loan-sim] |   |
| `trading-bot` | `web3` | qa-extras: [kill-switch] |   |
| `custody-wallet` | `web3` | compliance: [fatf, ccss, ofac] | min-size: enterprise |
| `bridge-protocol` | `web3` | qa-extras: [formal-verification, economic-attack-sim] |   |
| `cex-exchange` | `web3` | compliance: [kyc-aml, fatf, ofac, pci-dss] | min-size: enterprise |
| `embedded-iot` | `iot-embedded` | compliance: [etsi-303-645] |   |
| `hardware-driver` | `iot-embedded` | qa-extras: [hil-test] |  |
| `critical-infrastructure` | `regulated` | compliance: [nis2] | min-size: enterprise |
| `financial-services` | `regulated` | compliance: [dora] | min-size: enterprise |
| `gxp-system` | `regulated` | compliance: [21cfr11] | min-size: enterprise |
| `iso27001-scope` | `regulated` | compliance: [iso27001] | min-size: enterprise |
| `automotive-supplier` | `regulated` | compliance: [tisax] | min-size: enterprise |
| `defense-cui-system` | `defense-govcon` | compliance: [cmmc-2.0, nist-800-171, dfars-252.204-7012, itar, section-889], reviewers: [cmmc-reviewer] | min-size: enterprise; security gate: deep |
| `api-platform` | `devtools` | compliance: [openssf, api-stability, soc2-type-2, gdpr], qa-extras: [openapi-lint, contract-test, deprecation-channel], packs: [devtools-pack] |  |
| `sdk-platform` | `devtools` | compliance: [openssf, api-stability, semver], qa-extras: [cross-version-compat, multi-language-parity], packs: [devtools-pack] |  |
| `developer-tools` | `devtools` | compliance: [openssf, soc2-type-2], qa-extras: [docs-as-product, dx-survey], packs: [devtools-pack] |  |
| `agent-platform` | `devtools` | compliance: [openssf, eu-ai-act, soc2-type-2], qa-extras: [tool-injection, schema-enforcement, multi-tenant-isolation], packs: [devtools-pack, agent-pack] |  |
| `large-scale-refactor` | `web-service` | qa-extras: [snapshot-regression, dep-graph] |   |
| `stack-migration` | `web-service` | qa-extras: [snapshot-regression, dual-runtime] |   |
| `monorepo` | `web-service` | qa-extras: [affected-only-test] |  |
| `video-streaming` | `web-service` | qa-extras: [webrtc-security, cdn-latency] |  |
| `digital-health` | `agent-product` | compliance: [hipaa, gdpr-art9, eu-ai-act, ftc-health-breach], packs: [digital-health-pack, ai-pack], qa-extras: [hitl-boundary, supplement-safety, refuse-to-diagnose, safe-messaging, gdpr-consent-revocation] | security gate: standard → deep on any clinical signal |
| `wearable-platform` | `agent-product` | compliance: [gdpr-art9, ccpa-spi, healthkit-policy, health-connect-policy], packs: [digital-health-pack], qa-extras: [data-minimisation, platform-policy-compliance, wearable-api-access] |  |
| `nutrition-ai` | `ai-system` | compliance: [ftc-claims, dshea, gdpr-art9], packs: [digital-health-pack], qa-extras: [supplement-safety, drug-interaction-check, refuse-to-diagnose] |  |
| `clinical-hitl` | `agent-product` | compliance: [hipaa, gdpr-art9, eu-ai-act-annex3], packs: [digital-health-pack, clinical-pack], qa-extras: [hitl-boundary, hitl-sla, physician-credentialing] | security gate: deep; min-size: large |
| `digital-therapeutics` | `regulated` | compliance: [21cfr11, hipaa, gdpr-art9, eu-ai-act-annex3, iso14971], packs: [digital-health-pack, clinical-pack], qa-extras: [rct-equivalence, clinical-validation, refuse-to-diagnose] | min-size: enterprise; security gate: deep |

## Jurisdiction Compliance Rows

Jurisdiction tags are derived from `detect.ts` output and written into PROJECT.md as `jurisdiction: [...]`. The orchestrator reads this list and routes to the appropriate reviewer alongside the primary archetype reviewer.

| Jurisdiction tag | Archetype scope | Compliance added | Reviewer dispatched |
|-----------------|-----------------|------------------|---------------------|
| `eu-facing` | any archetype | `jurisdiction: [eu]` | `gdpr-reviewer` — gdpr, eu-ai-act, nis2 |
| `us-ca-facing` | any archetype | `jurisdiction: [us-ca]` | `us-privacy-reviewer` — ccpa, cpra |
| `india-facing` | any archetype | `jurisdiction: [in]` | `dpdpa-reviewer` — dpdpa, rbi-localisation |
| `multi-jurisdiction` | any archetype | `jurisdiction: [eu, us-ca]` | `gdpr-reviewer` + `us-privacy-reviewer` — gdpr, ccpa, eu-ai-act |
| `brazil-facing` | any archetype | `jurisdiction: [br]` | `gdpr-reviewer` — lgpd |
| `uk-facing` | any archetype | `jurisdiction: [uk]` | `gdpr-reviewer` — uk-gdpr, fca |

## How /start Uses This Table

1. `/start` detects specific type (e.g. `voice-agent`) using keyword matching
2. Looks up archetype in this table → `ai-system`
3. Merges default params from this table with any user overrides
4. Writes to PROJECT.md:
   ```yaml
   primary: voice-agent          # specific type (for reference)
   archetype: ai-system          # pipeline rules come from here
   compliance: [tcpa, gdpr-biometric]
   qa-extras: [wer, ttfb, barge-in]
   # tier computed from archetype: see references/security-tiers.md
   ```
5. Agents read `archetype:` + params — not `primary:` — for all pipeline decisions

## When Type Is Not In This Table

If `/start` detects a type not listed here:
- Default archetype: `web-service`
- Default params: none
- `/start` warns: "Type `<type>` not in archetype map — defaulting to `web-service`. Run `/audit` to refine."