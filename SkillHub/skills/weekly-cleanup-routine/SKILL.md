---
name: weekly-cleanup-routine
description: "A lightweight 5-minute weekly health check covering bounce monitoring, new contact quality, workflow health, list growth trends, and data quality sampling. Quick early warning system, not a comprehensive audit."
license: MIT
metadata:
  author: tomgranot
  version: "1.0"
  category: ongoing-maintenance
---

# Weekly Cleanup Routine

A fast, 5-minute weekly check that catches problems early. This is not a deep audit — it is a spot-check designed to surface issues before they compound.

## Prerequisites

- HubSpot portal access
- Bounce monitoring workflow active (run `/bounce-monitoring-workflow` first)

## The 5-Minute Checklist

### Stage 1: Before — Open Dashboards

Open HubSpot in your browser. Have the following views ready:
- Email health dashboard
- Workflow dashboard
- Contacts list view (sorted by create date, descending)

### Stage 2: Execute — Five Spot Checks

#### 1. Bounce Monitoring (1 min)
- Check the `email_health_flag` list. How many contacts were flagged this week?
- If more than 10, investigate the source (bad import? form spam?).
- If zero, confirm the workflow is still active.

#### 2. New Contact Quality (1 min)
- Filter contacts created in the last 7 days.
- Spot-check 5-10 new contacts. Do they have:
  - Valid email addresses?
  - Company name populated?
  - Lifecycle stage set?
- If quality is low, check the source (which form, import, or integration created them).

#### 3. Workflow Health (1 min)
- Open the workflow dashboard. Look for:
  - Any workflows showing errors (red indicators)
  - Any workflows with zero enrollments that should be active
  - Any workflows that were accidentally turned off

#### 4. List Growth Trends (1 min)
- Check your key segment lists (customers, MQLs, suppressed).
- Is any list growing or shrinking unexpectedly?
- A sudden spike in suppressed contacts could indicate a deliverability problem.

#### 5. Data Quality Sample (1 min)
- Pull 10 random contacts from the database.
- Check: email, company, lifecycle stage, owner.
- If more than 2 out of 10 have gaps, flag for a deeper review.

### Stage 3: After — Log and Escalate

Keep a simple weekly log (spreadsheet or note):

| Date | Bounces | New Contact Quality | Workflow Issues | List Anomalies | Data Quality |
|------|---------|-------------------|-----------------|----------------|--------------|
| YYYY-MM-DD | X flagged | Good/Bad | None/Details | None/Details | X/10 complete |

Escalate anything that appears two weeks in a row.

### Stage 4: Rollback

This is a read-only review — no rollback needed. Any fixes identified are executed through their respective skills.

## Scheduling

- Run every Monday morning.
- Set a recurring 15-minute calendar block (5 minutes for the check, 10 minutes buffer for any follow-up).
- If you miss a week, do not double up — just run the next scheduled check.
