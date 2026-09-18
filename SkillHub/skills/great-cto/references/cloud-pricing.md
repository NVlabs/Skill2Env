---
name: cloud-pricing
description: Rate tables used by architect — pipeline token/cost estimate by project size, and per-component cloud pricing (AWS/GCP/Azure) for the ARCH doc Cost Estimate section
when_to_use: architect Checkpoint A (pipeline cost estimate) and Workflow Step 3 (Cost Estimate section)
---

# Cloud & pipeline pricing — Reference

> Rate tables only. For the cost-model *methodology* (schema, unit economics,
> kill-switch thresholds), see `skills/great_cto/references/cost-model.md`.
> These tables are pure data — update in place when prices drift, no prose
> changes needed elsewhere.

## Pipeline cost estimate (by project size)

Shown at architect Checkpoint A before writing the ARCH doc — how much the
agent pipeline itself will cost to run for this feature.

| Size | Tokens | Cost | Time |
|------|--------|------|------|
| nano | ~50K | ~$0.10 | ~5min |
| small | ~400K | ~$1.00 | ~20min |
| medium | ~1M | ~$4-6 | ~45min |
| large | ~2M | ~$10-14 | ~90min |
| enterprise | ~3.5M | ~$20-30 | ~2-3h |

Adjustments:
- MANDATORY security gate archetype → add ~20% to cost estimate.
- `advisor-max-uses` > 0 on any agent → note "Advisor (Opus) calls add ~$0.50-2.00".

## Cloud component pricing (monthly, baseline tier, single region)

Used in the ARCH doc's `## Cost Estimate` section — match each new component
this feature introduces to a row and sum.

| Component type | AWS/mo | GCP/mo | Azure/mo |
|---------------|--------|--------|---------|
| RDS db.t3.medium | ~$60 | ~$55 | ~$65 |
| Lambda 1M req | ~$2 | ~$3 | ~$2 |
| ECS Fargate 0.5vCPU | ~$15 | ~$13 | ~$16 |
| S3/GCS 100GB | ~$3 | ~$2 | ~$2 |
| ALB | ~$20 | ~$18 | ~$20 |
| Redis cache.t3.micro | ~$15 | ~$16 | ~$14 |
| EKS node t3.medium | ~$30 | ~$27 | ~$32 |

*(table-version: 2026-04 — update quarterly)*

If no new cloud components → write "No new cloud components — no cost delta."
Always label: *"Rough estimate — baseline tier, single region. Actual cost depends on traffic."*
