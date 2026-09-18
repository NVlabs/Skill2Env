---
name: cost-model
description: Cost model template for ARCH docs: pre-deploy estimate of runtime $ (compute + storage + egress + LLM tokens + vendor SaaS), unit economics, kill-switch thresholds
when_to_use: Mandatory in ARCH doc for medium/large projects + ai-system/agent-product/commerce/regulated. Read by architect
applies_to:
  - ai-system
  - agent-product
  - commerce
  - regulated
  - fintech
---

# Cost model — Reference

> Every ARCH doc for non-trivial services includes a **Cost Model** section. Runtime cost estimated *before* deploy — not after the first AWS bill surprise. Unit economics surfaced *before* product-market fit lies to you.

## Scope

Cost model lives **inside each ARCH-*.md** as a section — not a separate file. This keeps cost coupled to the decision it justifies. Cross-service cost aggregation happens in `/digest` quarterly review.

## When required

| Condition | Cost Model section |
|-----------|--------------------|
| `project_size` ≥ `medium` | required |
| `archetype` is `ai-system` / `commerce` / `regulated` | required (any size) |
| greenfield with no cloud deploy yet | placeholder: "TBD pre-deploy" |
| internal library / CLI tool | skip |

## Schema

```markdown
## Cost Model

### Runtime cost (estimated monthly)
| Component | Assumption | Cost |
|-----------|-----------|------|
| Compute: <type × count> | <usage pattern, region> | $<N>/mo |
| Database: <instance> | <AZ / replication> | $<N>/mo |
| Data transfer | <volume> | $<N>/mo |
| External APIs: <vendor> | <unit × rate> | $<N>/mo |
| **Total estimate** | | **$<N>/mo** |

### Unit economics
- Per active user: $<N>/mo (assuming <DAU> DAU)
- Per transaction: $<N> (<total> / <txn-count>)
- Break-even point: needs ≥ <N> paying users at $<price>/mo

### Cost controls
- <vendor>: <specific control — cap, rate limit, cache>
- Infra: <scheduled scale-down / reserved instances>

### Review cadence
- Quarterly via `/digest` (compares actual vs estimate)
- Alert if actual > estimate × 1.2 → architect investigates
```

## Data sources

architect pulls cost inputs from:
- **Compute**: instance type × hours/month (730) × on-demand rate for the region
- **Database**: instance class × hours + storage GB + IO
- **Data transfer**: egress GB × per-GB rate (free between same-region services)
- **External APIs**: rate from vendor register (`docs/vendors/VENDOR-*.md` "Contract" section) × expected volume from ARCH load estimates

When exact pricing changes monthly, use the vendor's own pricing-page rate at the time of ARCH — do not embed URLs, just record the rate used.

## Relationship to OWNERSHIP.md

For teams with ownership assignment, the ARCH Cost Model feeds a per-path cost annotation:

```markdown
| Path | Team | TL | Expected cost/mo | Notes |
|------|------|-----|-------------------|-------|
| services/api | core | @alex | $2000 | 3 containers + RDS |
```

This makes "which team burned the most compute this quarter?" answerable from files.

## Actual-vs-estimate reconciliation

Optional, advisory. If the CTO wires a FinOps source (AWS CostExplorer, GCP billing export, Datadog metering), append to `.great_cto/cost-actual.log`:

```
<YYYY-MM> service:<slug> actual:$<N> estimate:$<N> delta:<+/-%>
```

`/digest` reads this file quarterly; entries > 20% over estimate are flagged.

Not in scope: live FinOps integration. The plugin writes file-only records; a separate cron / GitHub Action populates the log.

## Integration

- **architect**: writes Cost Model section into every qualifying ARCH-*.md; for each entry in the Runtime cost table, references the vendor register when a third-party service is involved
- **`/audit`**: scans IaC files (`*.tf`, `*.yaml`, `helm/values.yaml`) for services deployed without a matching ARCH Cost Model section; advisory finding only (not blocking)
- **`/digest` (quarterly)**: aggregates cost estimates across all ARCH docs; if `.great_cto/cost-actual.log` exists, computes delta; lists services > 20% over estimate for review

## Consumers

- architect — writes at ARCH time
- `/audit` — detects cost-model gaps
- `/digest` — quarterly reconciliation
- Q-review (v1.0.75) — cost trajectory in executive narrative
- Risk register — budget overrun > 50% for a single service triggers an R- entry

## Not in scope (deliberately)

- Live billing integration — files only; external cron handles actuals
- Cost optimization recommendations — that's a specialized FinOps skill, not the CTO plugin
- Per-commit cost impact — too noisy; quarterly granularity is the product
