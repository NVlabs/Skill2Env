---
name: venice-models
description: Discover Venice models, their capabilities, constraints, and pricing. Covers GET /models (with ?type filter), /models/traits, /models/compatibility_mapping, the ModelResponse schema (capabilities, constraints, pricing per type), and how to use this to pick the right model programmatically.
---

# Venice Models

Three read-only endpoints for model discovery — all `GET`:

| Endpoint | Returns |
|---|---|
| `/models` | Full model catalog with `model_spec` (capabilities, constraints, pricing). |
| `/models/traits` | Trait → model ID mapping (e.g. `"default"`, `"fastest"`, `"default_reasoning"`, `"highest_quality"`). |
| `/models/compatibility_mapping` | Legacy / OpenAI / third-party model ID → Venice model ID aliases. |

All three take an optional `?type=` filter: `text`, `image`, `video`, `music`, `tts`, `asr`, `embedding`, `upscale`, `inpaint`, `all`, `code`.

All three are authenticated (Bearer API key or x402 SIWE) like every other `/api/v1` route.

## Use when

- You need to pick a model at runtime based on capabilities (vision, reasoning, function calling, E2EE, X search, multi-image, …).
- You need to validate a request against a model's `constraints` (prompt length, aspect ratio, resolution, steps).
- You need the current **price per million tokens / per image / per second / per 1k chars** to build a cost estimate.
- You want to resolve a user-friendly trait name (e.g. `default`, `default_reasoning`, `highest_quality`) or a frontier-style ID (`openai-gpt-54-pro`, `claude-opus-4-7`) to a concrete Venice model ID.

## `GET /models`

```bash
curl "https://api.venice.ai/api/v1/models?type=text"
```

```json
{
  "object": "list",
  "type": "text",
  "data": [
    {
      "id": "zai-org-glm-5-1",
      "created": 1699000000,
      "model_spec": {
        "name": "GLM 5.1",
        "description": "Balanced blend of speed and capability...",
        "availableContextTokens": 200000,
        "maxCompletionTokens": 24000,
        "privacy": "private",
        "beta": false,
        "betaModel": false,
        "modelSource": "https://huggingface.co/zai-org/GLM-5.1",
        "offline": false,
        "capabilities": { ... },
        "constraints": { ... },
        "pricing": { ... },
        "regionRestrictions": ["US"],
        "deprecation": {"date": "2025-03-01T00:00:00.000Z"}
      }
    }
  ]
}
```

### `model_spec.capabilities` — text models

| Flag | Meaning |
|---|---|
| `optimizedForCode` | Tuned for coding tasks. |
| `quantization` | `fp4` / `fp8` / `fp16` / `bf16` / `int8` / `int4` / `not-available`. |
| `supportsFunctionCalling` | Tools are allowed. |
| `supportsReasoning` | Emits `<thinking>...</thinking>` blocks (and/or provider-specific `reasoning_content`). |
| `supportsReasoningEffort` | Honors `reasoning.effort` / `reasoning_effort`. |
| `supportsResponseSchema` | Honors `response_format: json_schema`. |
| `supportsMultipleImages` + `maxImages` | Multi-image vision support. |
| `supportsVision` | Accepts `image_url` parts. |
| `supportsVideoInput` | Accepts `video_url` parts. |
| `supportsWebSearch` | Honors `venice_parameters.enable_web_search`. |
| `supportsLogProbs` | Honors `logprobs` / `top_logprobs`. |
| `supportsTeeAttestation` | Runs inside a TEE with hardware attestation. |
| `supportsE2EE` | End-to-end encrypted inference available (requires TEE). |
| `supportsXSearch` | xAI native web + X/Twitter search. |
| `supportsAudioInput` | Accepts audio-content message parts (set by the runtime capability builder — not part of the OpenAPI strict schema but appears on `/models` responses). |

### `model_spec.constraints` — by model family

- **Text** — `temperature.default`, `top_p.default`, and `{frequency,presence,repetition}_penalty.default`.
- **Image** — `promptCharacterLimit`, `widthHeightDivisor`, `steps.{default,max}`, optional `aspectRatios[]` + `defaultAspectRatio`, optional `resolutions[]` + `defaultResolution` (the last two appear only on models that use ratio/resolution-based sizing).
- **Video** — `aspect_ratios[]`, `resolutions[]`, `durations[]`, `model_type` (`text-to-video`/`image-to-video`/`video`), `audio`, `audio_configurable`, `prompt_character_limit`.
- **Inpaint / edit** — `aspectRatios[]`, `promptCharacterLimit`, `combineImages`.
- **TTS / Music** (fields surface at the top level of `model_spec`, not inside `constraints`) — `voices[]`, `default_voice`, `supports_lyrics`, `lyrics_required`, `supports_lyrics_optimizer`, `supports_force_instrumental`, `supports_speed`, `supports_language_code`, `min_speed`, `max_speed`, `min_prompt_length`, `prompt_character_limit`. Internal TTS per-model toggles like `supportsPromptParam` / `supportsTemperatureParam` / `supportsTopPParam` exist on the model definitions but are **not** merged into `/models` output today — treat the speech request schema as the support matrix.
- **Embedding** (top-level, not inside `constraints`) — `embeddingDimensions`, `maxInputTokens`, `supportsCustomDimensions`.

### `model_spec.pricing` — by model family

- **LLM** — `input.{usd,diem}`, `output.{usd,diem}` per 1 000 000 tokens, plus optional `cache_input` (reads), `cache_write` (writes, e.g. Anthropic 1.25×), and `extended.*` tier triggered by `context_token_threshold`.
- **Image** — either `generation.{usd,diem}` per image (flat) or `resolutions.<tier>.{usd,diem}` (per `1K`/`2K`/`4K`). Every image row also carries a global `upscale.{2x,4x}.{usd,diem}` block (derived from shared upscale SKUs) — treat it as account-wide upscale pricing, not a signal that this specific model can upscale. Combine with the inpaint/upscale model's own capability check to decide what's actually callable.
- **Inpaint / edit** — `inpaint.{usd,diem}` per edit.
- **Video** — **not currently returned on `/models`.** `calculatePricing()` has no video branch, so video entries have no `model_spec.pricing`. Use `POST /video/quote` for the authoritative per-request price.
- **Music / long audio** — `generation.{usd,diem}` (per job), `per_second.{usd,diem}` (per second generated), `per_thousand_characters.{usd,diem}` (character-priced narration), or `durations.<tier>.{usd,diem,min_seconds,max_seconds}` (duration-bucketed).
- **TTS** — `input.{usd,diem}` per **1 000 000 input characters**.
- **ASR** — `per_audio_second.{usd,diem}`.
- **Embeddings** — `input.{usd,diem}` per 1 000 000 tokens.

Crypto RPC pricing is **not** in `/models` — it's tier × chain multipliers on `/crypto/rpc/{network}` (see [`venice-crypto-rpc`](../venice-crypto-rpc/SKILL.md)).

### Other top-level `model_spec` fields

| Field | Use |
|---|---|
| `privacy` (`private` / `anonymized`) | Zero data retention if `private`. |
| `beta` / `betaModel` | Gated to beta users (`beta: true` ⇒ need access). |
| `offline` | Currently unavailable; skip. |
| `regionRestrictions[]` | Country codes. `403` outside them. |
| `deprecation.date` | Retirement date. Migrate before. |

## `GET /models/traits`

```bash
curl "https://api.venice.ai/api/v1/models/traits?type=text"
```

Returns `{ object: "list", type: "text", data: { "default": "zai-org-glm-5-1", "fastest": "grok-41-fast", "most_uncensored": "venice-uncensored", "default_reasoning": "...", "default_code": "...", "default_vision": "...", "function_calling_default": "...", "most_intelligent": "..." } }` for `type=text`. For `type=image`, expect keys like `default`, `fastest`, `highest_quality`, `eliza-default`. Trait keys come from the internal `ApiModelTraits` / `LLMApiModelTraits` / `ImageApiModelTraits` enums.

Use this to avoid hard-coding model IDs — resolve a trait at boot and cache for the session.

## `GET /models/compatibility_mapping`

```bash
curl "https://api.venice.ai/api/v1/models/compatibility_mapping?type=text"
```

Returns `{ object: "list", type: "text", data: { "openai-gpt-54-pro": "zai-org-glm-5-1", "claude-opus-4-7": "claude-opus-4-7", "gpt-5-4-pro": "openai-gpt-54-pro", ... } }`. Both OpenAI-style IDs (`openai-gpt-54-pro`) and vendor-style aliases (`gpt-5-4-pro`) may appear as keys.

Lets an OpenAI-style client call Venice with its native model IDs — Venice substitutes behind the scenes. Useful when porting existing code.

## Common patterns

### Pick a vision+reasoning model at runtime

```ts
const list = await fetch(`${base}/models?type=text`).then(r => r.json())
const match = list.data.find((m: any) =>
  m.model_spec.capabilities.supportsVision &&
  m.model_spec.capabilities.supportsReasoning &&
  !m.model_spec.offline &&
  !m.model_spec.beta
)
```

### Validate an image request before submit

```ts
const spec = (await fetch(`${base}/models?type=image`).then(r => r.json()))
  .data.find((m: any) => m.id === myModel)!.model_spec

const { widthHeightDivisor, promptCharacterLimit, aspectRatios } = spec.constraints
if (prompt.length > promptCharacterLimit) throw new Error('prompt too long')
if (width % widthHeightDivisor !== 0) throw new Error('width not divisible')
if (aspectRatios && !aspectRatios.includes(myAspect)) throw new Error('bad aspect')
```

### Estimate LLM cost

```ts
const p = spec.pricing
const cost =
  (inputTokens / 1_000_000) * p.input.usd +
  (outputTokens / 1_000_000) * p.output.usd +
  (cachedTokens / 1_000_000) * (p.cache_input?.usd ?? 0)
```

For extended-context runs, check if `inputTokens > p.extended?.context_token_threshold` and switch to `p.extended.*` rates.

## `?type=code`

`type=code` is a convenience filter returning text models with `capabilities.optimizedForCode === true`. Same response shape as `type=text`.

## Gotchas

- The catalog changes — cache for minutes, not days.
- `beta: true` models require beta-flagged keys — otherwise `401` with "only available to Pro users".
- `offline: true` means the model exists in the catalog but can't currently serve requests — treat it as absent for scheduling.
- `model_spec.pricing` can be **missing** on free / internal models — guard against `undefined`.
- `traits` differ by `type` — there's no "global default"; always pass `?type=...`.
- `compatibility_mapping` resolves model IDs, not capabilities. If your caller sends `openai-gpt-54-pro` but needs vision, verify via the resolved Venice model's `capabilities.supportsVision`.
