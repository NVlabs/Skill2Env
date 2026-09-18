# GenAI Agent Traces — OpenTelemetry Semantic Conventions (distilled)

Reference for the `gen_ai.*` attributes the App Insights JavaScript SDK emits as Dependency telemetry so browser-side AI agent calls correlate with backend OpenTelemetry spans.

> **Stability opt-in.** Set `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` in any backend that emits or reads these attributes. Without it, instrumentations may emit older/different attribute names.

## Operation names (`gen_ai.operation.name`)

| Value | When |
| --- | --- |
| `chat` | Chat-completion call to a model. |
| `generate_content` | Multimodal content generation (Gemini-style). |
| `text_completion` | Legacy single-prompt completion. |
| `embeddings` | Embedding generation. |
| `create_agent` | Agent definition created/registered. |
| `invoke_agent` | Agent run/invocation (turn). |
| `execute_tool` | Tool/function call executed by an agent. |

Span name MUST follow `{operation.name} {target}` — e.g. `chat gpt-4o-mini`, `invoke_agent ResearchAssistant`, `execute_tool getWeather`.

## Provider names (`gen_ai.provider.name`)

`openai`, `azure.ai.openai`, `azure.ai.inference`, `anthropic`, `aws.bedrock`, `gcp.gemini`, `gcp.vertex_ai`, `cohere`, `mistral_ai`, `groq`, `deepseek`, `perplexity`, `x_ai`, `ibm.watsonx.ai`. Use lower-case, dotted form. New providers: use a stable lower-case identifier; no spaces.

## Common request / response attributes (all spans)

| Attribute | Type | Notes |
| --- | --- | --- |
| `gen_ai.request.model` | string | Requested model name. |
| `gen_ai.response.model` | string | Returned model name (may differ — alias / version pinning). |
| `gen_ai.response.id` | string | Provider-side response/request id. |
| `gen_ai.response.finish_reasons` | string[] | One per choice: `stop`, `length`, `tool_calls`, `content_filter`, `error`, … |
| `gen_ai.request.temperature` | double | |
| `gen_ai.request.top_p` | double | |
| `gen_ai.request.top_k` | double | |
| `gen_ai.request.max_tokens` | int | |
| `gen_ai.request.presence_penalty` | double | |
| `gen_ai.request.frequency_penalty` | double | |
| `gen_ai.request.stop_sequences` | string[] | |
| `gen_ai.request.seed` | int | |
| `gen_ai.request.choice.count` | int | Number of choices requested (omit if 1). |
| `gen_ai.request.encoding_formats` | string[] | Embeddings only: `base64`, `float`, … |
| `gen_ai.output.type` | enum | `text` \| `json` \| `image` \| `speech`. |
| `gen_ai.usage.input_tokens` | int | Prompt tokens. |
| `gen_ai.usage.output_tokens` | int | Completion tokens. |
| `gen_ai.conversation.id` | string | App-defined conversation/session id (also use as `session.id`). |
| `server.address` | string | Provider host (e.g. `myresource.openai.azure.com`). |
| `server.port` | int | Omit for default 443. |
| `error.type` | string | Error class / status code on failure. |

## Agent attributes

| Attribute | Type | Notes |
| --- | --- | --- |
| `gen_ai.agent.id` | string | Stable agent id (provider-assigned, e.g. `asst_…`). |
| `gen_ai.agent.name` | string | Human-readable agent name. |
| `gen_ai.agent.description` | string | Short purpose statement. |
| `gen_ai.agent.version` | string | Agent version, when versioned. |

`create_agent` and `invoke_agent` spans are required to set `gen_ai.agent.name`. `gen_ai.agent.id` is required when known.

## Tool attributes (`execute_tool`)

| Attribute | Type | Notes |
| --- | --- | --- |
| `gen_ai.tool.name` | string | Tool/function name. |
| `gen_ai.tool.type` | enum | `function` \| `extension` \| `datastore`. |
| `gen_ai.tool.description` | string | Optional. |
| `gen_ai.tool.call.id` | string | Provider-issued tool-call id (matches the `tool_calls[*].id` in the model output). |
| `gen_ai.tool.call.arguments` | string | **Opt-In.** JSON-serialized arguments. May contain user data. |
| `gen_ai.tool.call.result` | string | **Opt-In.** Tool result. May contain user data. |

## Sensitive content (Opt-In only)

| Attribute / event | Notes |
| --- | --- |
| `gen_ai.system_instructions` | System prompt(s). Span attribute. |
| `gen_ai.input.messages` | Full input message array (role + content). Span attribute. |
| `gen_ai.output.messages` | Full output message array. Span attribute. |
| `gen_ai.client.inference.operation.details` (event) | Carries request/response messages + tool definitions when the span attribute path is too large. |

**Capture rules:**

1. Off by default. Gate behind a runtime/config flag.
2. Truncate large content (e.g. > 8 KB) and set `gen_ai.truncated=true`.
3. Redact PII where required by policy before emitting.
4. For very large or sensitive payloads, emit a reference (e.g. blob URL) instead of inline content.

## Token usage

- Set `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens` on **every** model span (`chat`, `text_completion`, `generate_content`, `embeddings` — embeddings have no output tokens).
- For agents, sum tokens from child model spans onto the parent `invoke_agent` only when you have the totals. Never double-count by also summing nested agent invocations the parent didn't directly own.

## Streaming

- Span ends when the stream completes (last chunk received OR client closes).
- `gen_ai.usage.*` and `gen_ai.response.finish_reasons` are set at end-of-stream.
- Optional event `gen_ai.choice` may be emitted per choice with index + finish reason for live dashboards.

## Errors

- Set span status to ERROR.
- Set `error.type` to a stable identifier (HTTP status, provider error code, or exception class). Avoid free-form messages.
- For tool errors, the `execute_tool` span carries the error; the parent `invoke_agent` span only fails if the agent run aborted.

## Mapping to App Insights

When emitting from the browser via the App Insights JS SDK, use **Dependency** telemetry with `type: "GenAI"` and put all `gen_ai.*` keys in `properties`. App Insights flattens `properties` into `customDimensions`, where they're queryable in KQL with `tostring(customDimensions["gen_ai.operation.name"])`.

| OTel concept | App Insights field |
| --- | --- |
| Span name | `name` |
| Span kind=CLIENT, target | `target` (e.g. provider host) |
| Duration | `duration` (ms) |
| Span status | `success` + `resultCode` |
| Span attributes | `properties` → `customDimensions` |
| Trace id / Span id | `operation_Id` / `id` (set automatically when `distributedTracingMode: 2`) |
| Span events | Emit as `trackTrace` with the same `operation_Id` |

## Useful KQL

```kusto
// Top agents by p95 latency
dependencies
| where type == "GenAI" and tostring(customDimensions["gen_ai.operation.name"]) == "invoke_agent"
| summarize p95=percentile(duration,95), runs=count()
    by agent=tostring(customDimensions["gen_ai.agent.name"])
| order by p95 desc

// Token usage by model
dependencies
| where type == "GenAI" and tostring(customDimensions["gen_ai.operation.name"]) == "chat"
| extend tin=toint(customDimensions["gen_ai.usage.input_tokens"]),
         tout=toint(customDimensions["gen_ai.usage.output_tokens"]),
         model=tostring(customDimensions["gen_ai.response.model"])
| summarize sum_in=sum(tin), sum_out=sum(tout), calls=count() by model

// Failed tool calls
dependencies
| where type == "GenAI" and tostring(customDimensions["gen_ai.operation.name"]) == "execute_tool"
| where success == false
| project timestamp, tool=tostring(customDimensions["gen_ai.tool.name"]),
          err=tostring(customDimensions["error.type"]), operation_Id
```

## See also

- OTel GenAI spec: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Azure AI inference semconv: <https://opentelemetry.io/docs/specs/semconv/gen-ai/azure-ai-inference/>
- App Insights data model (Dependency): <https://learn.microsoft.com/azure/azure-monitor/app/data-model-complete>
