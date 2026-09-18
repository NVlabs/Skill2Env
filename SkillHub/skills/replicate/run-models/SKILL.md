---
name: run-models
description: Run AI models on Replicate via predictions, webhooks, and streaming.
---

## Docs

- Reference: <https://replicate.com/docs/llms.txt>
- OpenAPI schema: <https://api.replicate.com/openapi.json>
- MCP server: <https://mcp.replicate.com>
- Per-model docs: `https://replicate.com/{owner}/{model}/llms.txt`
- Set `Accept: text/markdown` when requesting docs pages for Markdown responses.

## Workflow

1. **Choose the right model** - Search with the API or ask the user.
2. **Get model metadata** - Fetch input and output schema via API.
3. **Create prediction** - POST to /v1/predictions.
4. **Poll for results** - GET prediction until status is "succeeded".
5. **Return output** - Usually URLs to generated content.

## Three ways to get output

1. Create a prediction, store its id from the response, and poll until completion.
2. Set a `Prefer: wait` header when creating a prediction for a blocking synchronous response. Only recommended for very fast models. Max 60 seconds.
3. Set an HTTPS webhook URL when creating a prediction, and Replicate will POST to that URL when the prediction completes.

## Guidelines

- Use the `POST /v1/predictions` endpoint, as it supports both official and community models.
- Every model has its own OpenAPI schema. Always fetch and check model schemas to make sure you're setting valid inputs. Even popular models change their schemas.
- Validate input parameters against schema constraints (`minimum`, `maximum`, `enum` values). Don't generate values that violate them.
- When unsure about a parameter value, use the model's default example or omit the optional parameter.
- Don't set optional inputs unless you have a reason to. Stick to the required inputs and let the model's defaults do the work.
- Use HTTPS URLs for file inputs whenever possible. You can also send base64-encoded files, but they should be avoided.
- Fire off multiple predictions concurrently. Don't wait for one to finish before starting the next.
- Output file URLs expire after 1 hour, so back them up if you need to keep them, using a service like Cloudflare R2.
- Webhooks are a good mechanism for receiving and storing prediction output.

## Predictions

- A prediction goes through these states: `starting` -> `processing` -> `succeeded` / `failed` / `canceled`.
- Official models use `owner/name` format. Community models require `owner/name:version_id`.
- The `POST /v1/predictions` endpoint handles both.

## Webhooks

- Set `webhook` to an HTTPS URL when creating a prediction. Replicate POSTs the full prediction object when it completes.
- Filter events with `webhook_events_filter`: `start`, `output`, `logs`, `completed`.
- Validate webhook signatures using the `Webhook-ID`, `Webhook-Timestamp`, and `Webhook-Signature` headers. Get the signing secret from `GET /v1/webhooks/default/secret`.

## Prediction lifetime

- Set `lifetime` to auto-cancel predictions that run too long (e.g. `30s`, `5m`, `1h`). Measured from creation time.

## Streaming

- Language models that support streaming include a `stream` URL in the response. Use SSE to receive incremental output.

## File handling

- Prefer HTTPS URLs for file inputs. Output URLs from one prediction can be passed directly as file inputs to the next model.
- Output file URLs expire after 1 hour. Download and store them immediately if you need to keep them.

## Multi-model workflows

- Chain models by passing output URLs as file inputs to the next model.
- Start all independent predictions in parallel, then collect results.
- Output URLs are valid for 1 hour, which is enough for pipeline steps.
