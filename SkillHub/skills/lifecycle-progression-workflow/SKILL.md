---
name: lifecycle-progression-workflow
description: "Build workflows to automate contact progression through the sales funnel: Lead to MQL to SQL to Opportunity to Customer. Each transition is triggered by a specific event (score threshold, meeting booked, deal created, deal won)."
license: MIT
metadata:
  author: tomgranot
  version: "1.0"
  category: automation-workflows
---

# Lifecycle Stage Progression Workflow

Automate the contact journey through the sales funnel with four progression workflows, each triggered by a specific business event.

## Progression Paths

| From | To | Trigger |
|------|----|---------|
| Lead | MQL | Lead score exceeds threshold |
| MQL | SQL | Meeting booked |
| SQL | Opportunity | Deal created and associated |
| Opportunity | Customer | Deal marked as closed-won |

## Prerequisites

- HubSpot Marketing Professional or Enterprise plan
- Lead scoring model configured (run `/build-lead-scoring` first)
- Deal pipeline set up with a "Closed Won" stage
- Meeting tool or integration configured (for SQL transition)

## Building the Workflow: Three Options

### Option 1: Manual UI Build

Follow the step-by-step instructions in the "Execute" section below. This is the most reliable method and gives you full control over every trigger, branch, and action.

### Option 2: HubSpot Breeze AI

HubSpot's built-in Breeze AI can generate workflow skeletons from natural language prompts. Navigate to **Automation > Workflows > Create workflow > "Describe what you want"** and paste one prompt per workflow. You will need to create four separate workflows:

**Workflow 1 -- Lead to MQL:**
```
Create a contact-based workflow that triggers when a contact's HubSpot score
is greater than or equal to [your MQL threshold] AND their lifecycle stage is "Lead".
The workflow should set the lifecycle stage to "Marketing Qualified Lead"
and send an internal notification to the marketing team.
```

**Workflow 2 -- MQL to SQL:**
```
Create a contact-based workflow that triggers when a meeting is booked with
a contact AND their lifecycle stage is "Marketing Qualified Lead".
The workflow should set the lifecycle stage to "Sales Qualified Lead"
and send an internal notification to the sales owner.
```

**Workflow 3 -- SQL to Opportunity:**
```
Create a contact-based workflow that triggers when a contact has an associated
deal created AND their lifecycle stage is "Sales Qualified Lead".
The workflow should set the lifecycle stage to "Opportunity".
```

**Workflow 4 -- Opportunity to Customer:**
```
Create a contact-based workflow that triggers when a contact's associated deal
stage equals "Closed Won" AND their lifecycle stage is "Opportunity".
The workflow should set the lifecycle stage to "Customer"
and send an internal notification to the CS/onboarding team.
```

**CRITICAL WARNING: Breeze trigger limitations.** Breeze creates **event-based triggers (OR logic)** instead of **filter-based triggers (AND logic)**. Each of these four workflows requires AND logic between the event condition and the current lifecycle stage. After Breeze creates each workflow, you MUST manually verify and fix the trigger/enrollment conditions in the UI to ensure both conditions are ANDed together. Breeze is best used for creating the workflow skeleton (actions, branches, delays) -- the trigger conditions almost always need manual correction.

**Additional Breeze limitations for these workflows:**
- Breeze **cannot** configure re-enrollment rules
- Breeze may not correctly set the lifecycle stage condition as part of the enrollment trigger (it may create it as a branch instead)

### Option 3: Claude Anthropic Chrome Extension

The Claude Anthropic Chrome extension lets Claude see and interact with the HubSpot workflow builder UI directly. You can describe the workflow logic in natural language and Claude will click through the UI to build it. This is often more accurate than Breeze for workflows requiring precise AND-logic triggers, because Claude can verify each trigger condition visually.

To use this approach:
1. Open the HubSpot workflow builder in Chrome (Automation > Workflows > Create workflow)
2. Activate the Claude Chrome extension
3. Describe each of the four progression workflows using the specifications from this skill
4. Build them one at a time, verifying triggers before moving to the next

> **Note on Fast Mode**: If you're using Claude Code's Fast Mode to speed up workflow creation,
> be aware of the billing model: Haiku usage is included in your subscription, but Opus in
> Fast Mode consumes extra credits. For workflow building tasks (which are UI-heavy and may
> require many interactions), consider whether the speed tradeoff is worth the credit cost.

## Step-by-Step Build Instructions

### Stage 1: Before — Plan Thresholds

1. Define your MQL score threshold (typically 40-60 on a 0-100 scale). Adjust after 30-60 days of observation.
2. Confirm your deal pipeline stages include a clear "Closed Won" equivalent.
3. Document current lifecycle stage distribution (run the audit or check the property breakdown) so you can measure the impact.

### Stage 2: Execute — Build Four Workflows

Build each as a separate contact-based workflow.

#### Workflow 1: Lead to MQL

1. **Trigger:** HubSpot score is greater than or equal to [threshold] AND lifecycle stage is "Lead"
2. **Action:** Set lifecycle stage to "Marketing Qualified Lead"
3. **Action (optional):** Send internal notification to marketing team
4. **Re-enrollment:** OFF

#### Workflow 2: MQL to SQL

1. **Trigger:** Meeting booked (use "Meeting activity date" is known, or "Number of meetings booked" is greater than 0) AND lifecycle stage is "Marketing Qualified Lead"
2. **Action:** Set lifecycle stage to "Sales Qualified Lead"
3. **Action (optional):** Send internal notification to sales owner
4. **Re-enrollment:** OFF

#### Workflow 3: SQL to Opportunity

1. **Trigger:** Associated deal is created (use "Number of associated deals" is greater than 0) AND lifecycle stage is "Sales Qualified Lead"
2. **Action:** Set lifecycle stage to "Opportunity"
3. **Re-enrollment:** OFF

#### Workflow 4: Opportunity to Customer

1. **Trigger:** Associated deal stage equals "Closed Won" AND lifecycle stage is "Opportunity"
2. **Action:** Set lifecycle stage to "Customer"
3. **Action (optional):** Send internal notification to CS/onboarding team
4. **Re-enrollment:** OFF

#### Workflow Settings (all four)

- Re-enrollment: OFF (lifecycle should only progress forward)
- Suppression list: None needed — the lifecycle stage condition prevents backwards movement
- Time zone: Not applicable

### Stage 3: After — Verify

1. Test each workflow with a test contact:
   - Manually adjust score/create meeting/create deal/close deal and confirm progression.
2. Verify that workflows do not conflict — a contact should not be enrolled in two progression workflows simultaneously.
3. Check that lifecycle stages only move forward (HubSpot enforces this by default, but verify).
4. After one week, review the workflow history for each. Check for:
   - Contacts stuck at a stage despite meeting criteria
   - Unexpected enrollment volumes

### Stage 4: Rollback

1. Turn off any or all four workflows.
2. Lifecycle stages already set remain — HubSpot does not allow backward movement without manual override or a dedicated reset workflow.
3. If stages were set incorrectly, create a temporary workflow or use the API to reset affected contacts.

## Notes

- **Backward movement:** HubSpot prevents lifecycle stage from going backward by default. If a deal is lost and the contact should return to MQL, you need a separate "regression" workflow that explicitly sets the stage.
- **Multiple deals:** If a contact has multiple deals, the Opportunity-to-Customer workflow fires when any associated deal is closed-won. This is usually the desired behavior.
- **Score decay:** If your lead scoring model includes decay, a contact's score may drop below the MQL threshold after promotion. This is fine — the lifecycle stage is already set and will not regress.
