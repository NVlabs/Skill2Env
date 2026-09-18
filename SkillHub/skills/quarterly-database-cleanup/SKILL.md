---
name: quarterly-database-cleanup
description: "Run a comprehensive quarterly CRM audit covering list health, bounce monitoring, data quality, scoring calibration, engagement metrics, and property cleanup. Produces a health report with quarter-over-quarter trend comparison."
license: MIT
metadata:
  author: tomgranot
  version: "1.0"
  category: ongoing-maintenance
---

# Quarterly Database Cleanup

A structured quarterly audit that catches data drift before it becomes a crisis. Run this at the start of each quarter (or monthly if the database is large or fast-growing).

## Prerequisites

- HubSpot API token in `.env`
- Python with `hubspot-api-client` installed via `uv`
- Previous quarter's report (for trend comparison) — optional on first run

## Audit Checklist

### 1. List Health
- Count total active lists, static lists, and unused lists (zero members)
- Identify lists not referenced by any workflow or email
- Flag duplicate or overlapping lists

### 2. Bounce Monitoring
- Count contacts with 1, 2, and 3+ bounces
- Hard bounce rate vs. previous quarter
- Review contacts flagged by bounce monitoring workflow

### 3. Data Quality
- Missing email, company, industry, country, lifecycle stage
- Compare percentages to previous quarter
- Flag any property completeness that dropped more than 5%

### 4. Scoring Calibration
- Review lead score distribution (histogram)
- Check MQL conversion rate — are high-scoring leads actually converting?
- Adjust scoring model if conversion rate is below 10% or above 50%

### 5. Engagement Metrics
- Active contacts (engagement in last 90 days) as % of total
- Zombie contacts (no engagement in 6+ months) as % of total
- Email open rate and click rate trends

### 6. Property Cleanup
- Custom properties with zero populated records
- Properties not used in any list, workflow, or form
- Test/temp properties that should be archived

## Step-by-Step Instructions

### Stage 1: Before — Gather Baselines

1. Locate the previous quarter's report (if it exists) in `reports/`.
2. Run `/hubspot-audit` to get fresh numbers across all dimensions.

### Stage 2: Execute — Deep Review

For each checklist item above:

1. Pull current metrics via the HubSpot API (reuse audit script patterns).
2. Compare to the previous quarter's numbers.
3. Flag any metric that worsened by more than 5 percentage points.
4. Document specific contacts, lists, or properties that need action.

### Stage 3: After — Generate Report

Save a report to `reports/quarterly-cleanup-{YYYY-Q#}.md` with this structure:

```markdown
# Quarterly Database Health Report — YYYY Q#

## Summary

| Metric | Last Quarter | This Quarter | Change |
|--------|-------------|-------------|--------|
| Total contacts | XX,XXX | XX,XXX | +X% |
| Data completeness | XX% | XX% | +X% |
| Bounce rate | X.X% | X.X% | -X% |
| Zombie contacts | XX% | XX% | -X% |
| Unused lists | XX | XX | -XX |

## Action Items

1. [item with owner and deadline]
2. ...

## Detailed Findings

[One section per checklist item with metrics and recommendations]
```

### Stage 4: Rollback

This is a read-only audit — no rollback needed. Action items from the report are executed separately through their respective skills.

## Scheduling

- Set a recurring calendar reminder for the first Monday of each quarter.
- Assign an owner for each action item in the report.
- Review the previous quarter's action items for completion before starting the new audit.
