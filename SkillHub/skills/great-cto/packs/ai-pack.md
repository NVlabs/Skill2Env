---
name: ai-pack
description: Domain-specific depth for AI/ML projects: LLM serving (vLLM/Ollama), prompt programming (DSPy), evaluation frameworks (Ragas/Promptfoo/Braintrust), vector DB selection, RAG patterns
when_to_use: Building internal AI/ML systems (RAG, MCP servers, LLM ops, ML training/serving, voice, multimodal — not user-facing agents)
applies_to:
  - ai-system
---

# AI Domain Pack

> Extends `ai-system` archetype with domain-specific depth for voice agents, multimodal apps, RAG systems, LLM ops, ML training/serving, and computer vision.
> Loaded when `packs: [ai-pack]` is in PROJECT.md or auto-loaded for `ai-system` archetype.

## QA Extras Reference

Each `qa-extras` value below adds specific checks to qa-engineer's test plan.

### `wer` — Word Error Rate (voice-agent)
- **What**: Measure ASR accuracy on domain-specific vocabulary
- **Tool**: Compare ASR transcript vs reference transcript
- **Threshold**: WER ≤ 5% on domain vocab, WER ≤ 10% on general speech
- **Edge inputs**: accented speech, background noise (cafe, car, street), low-bandwidth audio

### `ttfb` — Time to First Byte (voice-agent)
- **What**: Latency from user speech end to first audio response byte
- **Tool**: Measure via WebSocket timestamp delta or telephony CDR
- **Threshold**: TTFB ≤ 300ms p95, end-to-end turn latency ≤ 800ms p95
- **Edge inputs**: long utterances (>10s), rapid back-to-back turns

### `barge-in` — Interruption Handling (voice-agent)
- **What**: Test that user can interrupt agent mid-response and agent handles gracefully
- **Tool**: Send interrupt signal at random points during agent speech
- **Threshold**: Correct barge-in handling ≥ 95% of interruptions
- **Edge inputs**: partial words, background noise mistaken as interrupt

### `dtmf-fallback` — Touch-tone Fallback (voice-agent)
- **What**: Test DTMF digit recognition for menu navigation fallback
- **Tool**: Send DTMF tones via telephony test harness
- **Threshold**: 100% digit recognition accuracy, menu navigation correct

### `concurrent-calls` — Load Test (voice-agent)
- **What**: Test system under target concurrent call volume × 2
- **Tool**: Load test harness (k6 + WebSocket or SIPp for telephony)
- **Threshold**: No call drops, latency within SLA at 2× target volume

### `retrieval-quality` — RAG Retrieval (rag-system)
- **What**: Measure retrieval relevance and coverage
- **Tool**: Eval suite with known query-document pairs
- **Threshold**: Recall@10 ≥ 0.7, precision@5 ≥ 0.6, no hallucinated sources
- **Edge inputs**: ambiguous queries, out-of-scope queries (should return "I don't know")

### `prompt-regression` — Prompt Quality (llm-ops)
- **What**: Detect quality degradation after prompt changes
- **Tool**: Run eval suite before and after prompt change
- **Threshold**: Score drop ≤ 2% vs baseline on all eval dimensions
- **Compare**: before-prompt eval → after-prompt eval, dimension by dimension

### `cost-cap` — Cost Control (llm-ops, ai-agent)
- **What**: Verify per-request and per-session cost stays within budget
- **Tool**: Log token usage per request, compute cost at model pricing
- **Threshold**: Per-request cost ≤ PROJECT.md `cost-cap:` value, per-session ≤ 10× per-request

### `per-modality-accuracy` — Per-Modality Eval (multimodal-app)
- **What**: Test each input modality independently
- **Tool**: Separate eval sets for text, image, audio inputs
- **Threshold**: Each modality ≥ baseline from PROJECT.md, no modality >10% below others

### `hallucination` — Factual Accuracy (multimodal-app, rag-system, llm-ops)
- **What**: Detect fabricated information in model outputs
- **Tool**: Eval set with known-answer queries + adversarial prompts
- **Threshold**: Hallucination rate ≤ 2% on factual eval set

### `cross-modal` — Cross-Modal Consistency (multimodal-app)
- **What**: Same query via different modalities should produce coherent responses
- **Tool**: Submit identical queries as text, image, and audio; compare outputs
- **Threshold**: Semantic similarity ≥ 0.85 across modalities for equivalent queries

### `tool-injection` — Tool Argument Safety (mcp-server)
- **What**: Test that tool arguments cannot be manipulated via prompt injection
- **Tool**: Adversarial inputs containing shell commands, SQL, path traversal
- **Threshold**: 0 successful injections

### `schema-enforcement` — Schema Validation (mcp-server)
- **What**: Verify all tool calls conform to declared JSON schemas
- **Tool**: Fuzz tool arguments with invalid types, missing fields, extra fields
- **Threshold**: 100% schema violations rejected, 0 false rejections on valid input

### `bias-audit` — Bias/Fairness (ml-training, ml-serving, computer-vision)
- **What**: Check model for disparate impact across protected groups
- **Tool**: Evaluate model predictions across demographic slices
- **Threshold**: Disparate impact ratio ≥ 0.8, equal opportunity difference ≤ 0.1
- **Report**: Include in model card

### `model-card` — Model Documentation (ml-training, ml-serving, computer-vision, recommendation-engine)
- **What**: Mandatory model documentation
- **Required fields**: model details, intended use, training data summary, quantitative analysis, ethical considerations, limitations
- **Where**: `docs/model-cards/MODEL-CARD-<name>.md`

### `drift-monitoring` — Production Drift (ml-serving)
- **What**: Detect data/concept drift in production
- **Tool**: Statistical comparison of input distribution vs training distribution
- **Threshold**: Alert on KL divergence > 0.1 or PSI > 0.2
- **SLA**: Alert within 15 minutes of drift detection

### `data-poisoning` — Training Data Integrity (ml-training)
- **What**: Check training data for poisoning vectors
- **Tool**: Outlier detection on training set, label consistency check
- **Threshold**: 0 known poisoning patterns detected

## Compliance Extras

### `eu-ai-act` — EU AI Act Annex III Check
1. Classify system: is it high-risk per Annex III? (biometric, education, employment, credit, law enforcement, migration, justice)
2. If high-risk: conformity assessment required + register in EU AI database before deploy
3. Document in `docs/compliance/EU-AI-ACT-classification.md`
4. Mandatory regardless of risk level: transparency obligations (users must know they're interacting with AI)

### `tcpa` — Telephone Consumer Protection Act (US)
1. Prior express written consent for recorded/automated calls
2. Opt-out mechanism within 10 days of request
3. No autodial to mobile without consent
4. Call recording notice per jurisdiction (1-party vs 2-party consent states)
5. Document consent flow in `docs/compliance/TCPA-consent.md`

### `gdpr-biometric` — GDPR Article 9 (Voice as Biometric)
1. If voice is used for identification (not just communication): explicit consent required
2. DPIA mandatory before processing
3. Data minimization: don't store voice data longer than needed
4. Right to erasure: must be able to delete all voice recordings per user
5. Document in `docs/compliance/GDPR-biometric-DPIA.md`

## Tooling Reference (2026 stack)

The AI tooling landscape moves fast. As of 2026, here's what to default to:

### LLM serving (on-prem / self-hosted)

| Tool | When |
|------|------|
| **vLLM** | Production GPU serving, throughput-optimised, supports continuous batching | Default for self-hosted GPU |
| **Ollama** | Local dev, single-user, easy model management | Default for laptop / dev workstation |
| **llama.cpp** | CPU inference, embedded, edge | When GPU isn't available |
| **TGI** (HuggingFace Text Generation Inference) | Alternative to vLLM | Same role; comparable perf |
| **TensorRT-LLM** | NVIDIA-specific, lowest latency | When you've committed to NVIDIA stack and need every ms |

For most teams: vLLM in production, Ollama for local dev. Don't roll your own serving on top of `transformers` library — it's an order of magnitude slower than vLLM.

### Prompt engineering / programmatic prompting

| Tool | When |
|------|------|
| **DSPy** | Compose prompts as programs, optimise with metrics. Best when you have eval data and want to systematically improve. |
| **Guidance** | Constrained generation (force JSON, force grammar). Good for structured output. |
| **Outlines** | Similar to Guidance; cleaner API; pure Python |
| **Instructor** | Pydantic-based structured output for OpenAI/Anthropic APIs |
| **LangChain / LlamaIndex** | Full agent framework with retrieval; use when you need the kitchen sink |

For new project starting in 2026: **Instructor** for simple typed outputs, **DSPy** for systematic prompt improvement, **vercel-ai-sdk** for streaming UI in React/Next.js.

**Anti-pattern**: building everything on raw f-strings + JSON.parse. Works for prototype, breaks at scale when prompts evolve and you need to A/B test variations.

### LLM evaluation

| Tool | When |
|------|------|
| **Ragas** | RAG-specific evaluation (faithfulness, answer relevancy, context precision) |
| **DeepEval** | Pytest-style LLM evals; CI-friendly |
| **Braintrust** | Hosted eval + experimentation, dashboards, regression detection |
| **Humanloop** | Hosted, focuses on prompt management + evaluation |
| **Langfuse evals** | If you're already using Langfuse for observability |
| **Promptfoo** | YAML-driven, runs in CI, good for prompt regression |

For new project: **Promptfoo** (free, CI-native) for regression testing, plus **Braintrust** if budget allows for hosted experimentation. Add Ragas if you have a RAG system.

### Local-first / privacy-preserving LLM

When the use case requires no data leaves device:

- **Ollama** + open models (Llama 3.x, Qwen 2.5, Mistral)
- **WebLLM** (browser-based via WebGPU)
- **mlc-llm** (cross-platform, mobile-capable)
- **Llamafile** (single-file LLM)

Model choice for local: Llama 3.3 70B if you have the GPU, Qwen 2.5 32B for speed, Phi-3 Mini for embedded.

### Vector databases

| Tool | When |
|------|------|
| **Pinecone** | Managed, default for SaaS without infra team |
| **Weaviate** | Self-hosted or managed, hybrid search built-in |
| **Qdrant** | Self-hosted, fastest open-source, Rust core |
| **pgvector** (Postgres) | Already on Postgres, want to keep one DB | Default if vector count < 10M |
| **Turbopuffer** | Cheapest scalable, S3-backed, serverless |
| **LanceDB** | Embedded, columnar, great for local + edge |

For new project on Postgres: pgvector. Switch to dedicated when query latency hurts at scale (~10M+ vectors).

### Observability for LLM apps

| Tool | When |
|------|------|
| **Langfuse** | Open-source, self-hostable, full LLM observability + eval |
| **Helicone** | Drop-in proxy, instant tracing, cheap |
| **Langsmith** | LangChain-native, hosted, expensive |
| **Honeycomb** | If you already use Honeycomb for general APM, has LLM support |

Default for new: Langfuse self-hosted. Free, complete, owns your data.

### Recommended `PROJECT.md` for new ai-system project

```yaml
primary: rag-system
archetype: ai-system
project_size: medium
stack: [python, fastapi, openai-sdk, vllm, pgvector]
team-size: 2
compliance: [eu-ai-act]
qa-extras: [retrieval-quality, hallucination, prompt-regression, cost-cap]
packs: [ai-pack]
```
