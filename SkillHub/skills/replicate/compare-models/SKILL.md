---
name: compare-models
description: Compare Replicate models by cost, speed, quality, and capabilities.
---

## Docs

- Reference: <https://replicate.com/docs/llms.txt>
- OpenAPI schema: <https://api.replicate.com/openapi.json>
- MCP server: <https://mcp.replicate.com>
- Per-model docs: `https://replicate.com/{owner}/{model}/llms.txt`
- Set `Accept: text/markdown` when requesting docs pages for Markdown responses.

## Workflow

1. Search or browse collections to build a shortlist of candidate models.
2. Fetch each model's schema to compare inputs, outputs, and capabilities.
3. Check pricing from model metadata or the Replicate website.
4. Run a small batch of test predictions to compare output quality.
5. Pick the model that best fits your constraints (cost, latency, quality).

## What to compare

- **Speed**: Check `metrics.predict_time` on completed predictions for actual inference time. Official models are always warm. Community models can cold-boot.
- **Cost**: Official models have predictable per-run pricing. Community models charge by compute time (GPU-seconds). Run a few predictions and check the `metrics` field for actual cost.
- **Quality**: Run the same prompts through each model and compare outputs. Quality is subjective. Match it to your use case, not a leaderboard.
- **Capabilities**: Compare input schemas for supported features (reference images, masks, aspect ratios, streaming, multi-image input). Check output formats.

## Key tradeoffs

- Lowest cost: smaller/distilled models. Accept slower inference and lower quality.
- Lowest latency: official models or schnell/turbo variants. Accept higher cost per run.
- Highest quality: pro/max/quality variants. Accept slower inference and higher cost.
- Most control: models with ControlNet, masks, or reference images. Accept more complex input setup.

## Official vs community models

- Official models: always warm, stable APIs, predictable pricing, maintained by Replicate.
- Community models: may cold-boot, require version pinning, maintained by the author.
- If a community model meets your needs and an official model doesn't, consider creating a deployment for consistent uptime.

## Prompting guidance

For prompting techniques and task-specific guidance:

- Image generation and editing: see the [prompt-images](../prompt-images/SKILL.md) skill.
- Video generation: see the [prompt-videos](../prompt-videos/SKILL.md) skill.
