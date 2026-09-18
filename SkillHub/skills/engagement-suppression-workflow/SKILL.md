---
name: engagement-suppression-workflow
description: "Build a two-tier sunset workflow that re-engages dormant contacts before suppressing them. Tier 1 triggers a re-engagement campaign after a configurable inactivity window. Tier 2 suppresses contacts that fail to re-engage within a configurable re-engagement window."
license: MIT
metadata:
  author: tomgranot
  version: "1.0"
  category: automation-workflows
---

# Engagement-Based Suppression Workflow

Build a two-tier sunset system that protects email deliverability while giving disengaged contacts a fair chance to re-engage before suppression.

## Why Two Tiers Matter

Suppressing contacts immediately after inactivity is aggressive and loses potential re-activations. A two-tier approach:
- **Tier 1** (inactive for your sunset window — typically 120-270 days): Triggers a re-engagement campaign — a last chance to interact.
- **Tier 2** (your re-engagement window after Tier 1 — typically 21-45 days — with still no engagement): Suppresses the contact from marketing emails.

This preserves deliverability scores while maximizing the recoverable audience.

## Prerequisites

- HubSpot Marketing Professional or Enterprise plan
- A re-engagement email campaign or sequence ready to send
- A custom dropdown property to track suppression status (e.g., `engagement_flag` or `reengagement_status` — dropdown with values: "re-engagement sent", "suppressed")

## Workflow Design

```
TRIGGER: Last engagement date > [sunset window] ago
         AND email is known
         AND not globally unsubscribed
         AND [suppression status property] is unknown
              │
              ▼
     ┌────────────────────┐
     │ Set [status prop]   │
     │ = "re-engagement    │
     │    sent"            │
     └────────┬───────────┘
              │
              ▼
     ┌────────────────────┐
     │ Enroll in           │
     │ re-engagement       │
     │ campaign/sequence   │
     └────────┬───────────┘
              │
              ▼
     ┌────────────────────┐
     │ Delay: [re-engage    │
     │  window] days       │
     └────────┬───────────┘
              │
              ▼
     ┌────────────────────┐
     │ IF/THEN BRANCH:     │
     │ Any engagement in   │
     │ re-engage window?   │
     ├──────────┬─────────┘
     │ YES      │ NO
     │          │
     ▼          ▼
   Clear     Set [status prop]
   status    = "suppressed"
   prop      + set non-marketing
```

## Building the Workflow: Three Options

### Option 1: Manual UI Build

Follow the step-by-step instructions in the "Execute" section below. This is the most reliable method and gives you full control over every trigger, branch, and action.

### Option 2: HubSpot Breeze AI

HubSpot's built-in Breeze AI can generate a workflow skeleton from a natural language prompt. Navigate to **Automation > Workflows > Create workflow > "Describe what you want"** and paste the following prompt:

```
Create a contact-based workflow for a two-tier sunset/re-engagement system.
Enrollment trigger: contacts where the last email open date is more than [sunset window] days ago,
AND email is known, AND they are not globally unsubscribed, AND a custom property
"[your suppression status property]" is unknown.

The workflow should:
1. Set the contact property "[your suppression status property]" to "re-engagement sent"
2. Enroll the contact in a re-engagement email sequence
3. Wait [re-engagement window] days
4. Check if the contact has opened or clicked any email in the last [re-engagement window] days
   - If YES (re-engaged): clear the "[your suppression status property]" property
   - If NO (still disengaged): set "[your suppression status property]" to "suppressed" and set the contact
     as a non-marketing contact
```

**CRITICAL WARNING: Breeze trigger limitations.** Breeze creates **event-based triggers (OR logic)** instead of **filter-based triggers (AND logic)**. This is a known limitation. After Breeze creates the workflow, you MUST manually verify and fix the trigger/enrollment conditions in the UI. The enrollment trigger for this workflow requires AND logic across four conditions -- Breeze will likely create them as separate OR conditions, which would enroll contacts incorrectly. Breeze is best used for creating the workflow skeleton (actions, branches, delays) -- the trigger conditions almost always need manual correction.

**Additional Breeze limitations for this workflow:**
- Breeze **cannot** create "is unknown" branch conditions -- you must add these manually
- Breeze **cannot** configure re-enrollment rules
- Breeze **cannot** set up workflow goals (early exit on re-engagement)

### Option 3: Claude Anthropic Chrome Extension

The Claude Anthropic Chrome extension lets Claude see and interact with the HubSpot workflow builder UI directly. You can describe the workflow logic in natural language and Claude will click through the UI to build it. This is often more accurate than Breeze for complex workflows because Claude can verify each step visually, including the multi-condition AND enrollment trigger and the "is unknown" checks that Breeze cannot handle.

To use this approach:
1. Open the HubSpot workflow builder in Chrome (Automation > Workflows > Create workflow)
2. Activate the Claude Chrome extension
3. Describe the workflow using the design diagram and instructions from this skill

> **Note on Fast Mode**: If you're using Claude Code's Fast Mode to speed up workflow creation,
> be aware of the billing model: Haiku usage is included in your subscription, but Opus in
> Fast Mode consumes extra credits. For workflow building tasks (which are UI-heavy and may
> require many interactions), consider whether the speed tradeoff is worth the credit cost.

## Step-by-Step Build Instructions

### Stage 1: Before — Prepare

1. **Create your suppression status property** (e.g., `engagement_flag` or `reengagement_status`) if it does not exist:
   - Object: Contact
   - Type: Dropdown select
   - Options: "re-engagement sent", "suppressed", blank/unknown
   - Group: Contact information

2. **Create or identify a re-engagement email/sequence.** A simple 1-2 email series asking "Still interested?" with a clear CTA works well.

3. **Define "engagement"** for your branch condition. Recommended: email open OR email click OR form submission OR page view within your re-engagement window (typically 21-45 days).

### Stage 2: Execute — Build the Workflow

1. **Set enrollment trigger:**
   - `hs_email_last_open_date` is more than your sunset window (typically 120-270 days) ago OR is unknown
   - AND `email` is known
   - AND `hs_email_optout` is not true
   - AND your suppression status property is unknown

2. **Action: Set contact property**
   - Your suppression status property = "re-engagement sent"

3. **Action: Enroll in re-engagement sequence** (or send re-engagement email)

4. **Delay: your re-engagement window (typically 21-45 days)**

5. **If/then branch:**
   - Condition: `hs_email_last_open_date` is less than [re-engagement window] days ago OR `hs_email_last_click_date` is less than [re-engagement window] days ago
   - **YES (re-engaged):** Set your suppression status property to blank/unknown (clears flag, contact returns to normal)
   - **NO (still disengaged):** Set your suppression status property = "suppressed" and set `hs_marketable_status` to non-marketing contact (via workflow action — this is the only way to set it, as the API is read-only)

6. **Settings:**
   - Re-enrollment: OFF
   - Goal: Contact opens or clicks any email (optional — exits workflow early)

7. **Turn on the workflow.**

### Stage 3: After — Verify

1. Spot-check 10-20 contacts that entered the workflow. Confirm:
   - Re-engagement email was sent
   - After 30 days, disengaged contacts were suppressed
   - Re-engaged contacts had their suppression status property cleared
2. Monitor deliverability metrics weekly for the first month.
3. Track how many contacts re-engage vs. get suppressed — adjust the sunset window if needed.

### Stage 4: Rollback

1. Turn off the workflow.
2. To reverse suppressions: filter contacts where your suppression status property = "suppressed" and manually set them back to marketing contacts in the UI.
3. Clear the suppression status property values in bulk if needed.

## Tuning

- **Shorten the sunset window** (e.g., 90-120 days) for aggressive deliverability improvement.
- **Lengthen the re-engagement window** (e.g., 45-60 days) if your email cadence is low.
- **Exclude recent customers** — add a filter to skip contacts with lifecycle stage = Customer or with a closed-won deal in the last 12 months.
