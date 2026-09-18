---
name: bounce-monitoring-workflow
description: "Build a workflow to protect sender reputation through automated bounce monitoring. Auto-suppresses contacts above a configurable bounce threshold, alerts on hard bounces, and flags high-bounce contacts for weekly manual review."
license: MIT
metadata:
  author: tomgranot
  version: "1.0"
  category: automation-workflows
---

# Bounce Monitoring Workflow

Protect your email sender reputation with automated bounce detection and suppression. This workflow catches bounces as they happen rather than waiting for periodic cleanup.

## How It Works

| Condition | Action |
|-----------|--------|
| Hard bounce detected | Alert admin immediately, suppress contact |
| Suppression threshold reached (commonly 2-3 bounces) | Auto-suppress from marketing emails |
| Review threshold reached (commonly 3-5 bounces) | Flag for weekly manual review (delete vs. recover) |

## Prerequisites

- HubSpot Marketing Professional or Enterprise plan
- A custom contact property (e.g., `email_health_flag` or `delivery_status`) — checkbox or dropdown with value: "flagged for review"
- Admin email or Slack channel for hard bounce alerts

## Building the Workflow: Three Options

### Option 1: Manual UI Build

Follow the step-by-step instructions in the "Execute" section below. This is the most reliable method and gives you full control over every trigger, branch, and action.

### Option 2: HubSpot Breeze AI

HubSpot's built-in Breeze AI can generate a workflow skeleton from a natural language prompt. Navigate to **Automation > Workflows > Create workflow > "Describe what you want"** and paste the following prompt:

```
Create a contact-based workflow that triggers when the "Email Bounce" property
is known (has a value). The workflow should:

1. First, check if the contact has a hard bounce reason (hard_bounce_reason is known):
   - If YES: send an internal notification saying "Hard bounce: [email]" and set the
     contact as a non-marketing contact
   - If NO: continue to the next check

2. Check if the bounce count is greater than or equal to [your suppression threshold, commonly 2-3]:
   - If YES: set the contact as a non-marketing contact, then check if bounce count
     is >= [your review threshold, commonly 3-5]. If so, set a custom property
     "[your bounce review property]" to "flagged" and send an internal notification
     saying "Contact [email] has [review threshold]+ bounces - review for deletion"
   - If NO: end (below threshold, monitor only)

Enable re-enrollment so the contact re-enters if their bounce count increases.
```

**CRITICAL WARNING: Breeze trigger limitations.** Breeze creates **event-based triggers (OR logic)** instead of **filter-based triggers (AND logic)**. After Breeze creates the workflow, you MUST manually verify and fix the trigger/enrollment conditions in the UI. Breeze is best used for creating the workflow skeleton (actions, branches, delays) -- the trigger conditions almost always need manual correction.

**Additional Breeze limitations for this workflow:**
- Breeze **cannot** create "is unknown" branch conditions -- you must verify that branch conditions checking for hard bounce reason are correctly configured
- Breeze **cannot** configure re-enrollment rules -- you must enable re-enrollment manually
- Breeze may flatten the nested branch structure (hard bounce check > 2+ bounces > 3+ bounces) into a single level

### Option 3: Claude Anthropic Chrome Extension

The Claude Anthropic Chrome extension lets Claude see and interact with the HubSpot workflow builder UI directly. You can describe the workflow logic in natural language and Claude will click through the UI to build it. This is often more accurate than Breeze for workflows with nested branching logic (this workflow has three levels of branches), because Claude can verify the branch hierarchy visually.

To use this approach:
1. Open the HubSpot workflow builder in Chrome (Automation > Workflows > Create workflow)
2. Activate the Claude Chrome extension
3. Describe the workflow using the design table and instructions from this skill

> **Note on Fast Mode**: If you're using Claude Code's Fast Mode to speed up workflow creation,
> be aware of the billing model: Haiku usage is included in your subscription, but Opus in
> Fast Mode consumes extra credits. For workflow building tasks (which are UI-heavy and may
> require many interactions), consider whether the speed tradeoff is worth the credit cost.

## Step-by-Step Build Instructions

### Stage 1: Before — Create Properties

1. Create your bounce review property (e.g., `email_health_flag` or `delivery_status`):
   - Object: Contact
   - Type: Single checkbox or dropdown
   - Group: Contact information

2. Identify your current bounce baseline — run a quick search for contacts where `hs_email_bounce` > 0 to understand the starting volume.

### Stage 2: Execute — Build the Workflow

Build a single contact-based workflow with branching logic.

1. **Trigger:** `hs_email_bounce` is known (fires when bounce count updates)

2. **Branch 1: Hard bounce check**
   - Condition: `hs_email_hard_bounce_reason_enum` is known
   - **YES:**
     - Send internal notification: "Hard bounce: {email} — {hs_email_hard_bounce_reason_enum}"
     - Set `hs_marketable_status` to non-marketing (workflow action)
   - **NO:** Continue to Branch 2

3. **Branch 2: Bounce count >= your suppression threshold (commonly 2-3)**
   - Condition: `hs_email_bounce` is greater than or equal to your suppression threshold
   - **YES:**
     - Set `hs_marketable_status` to non-marketing (workflow action)
     - Continue to Branch 3
   - **NO:** No action (below threshold — monitor only)

4. **Branch 3: Bounce count >= your review threshold (commonly 3-5)**
   - Condition: `hs_email_bounce` is greater than or equal to your review threshold
   - **YES:**
     - Set your bounce review property = flagged
     - Send internal notification: "Contact {email} has [review threshold]+ bounces — review for deletion"
   - **NO:** No further action

5. **Settings:**
   - Re-enrollment: ON (contact should re-enter if bounce count increases)
   - Goal: None

6. **Turn on the workflow.**

### Stage 3: After — Verify

1. Check workflow history after the first week of email sends.
2. Review the flagged contacts list weekly — decide for each contact:
   - **Delete** if the email is clearly invalid (typo domain, defunct company)
   - **Attempt recovery** if the domain is valid (could be a temporary mailbox issue)
3. Monitor overall bounce rate in HubSpot email health dashboard.

### Stage 4: Rollback

1. Turn off the workflow.
2. Contacts already suppressed remain non-marketing. To reverse:
   - Filter contacts suppressed by this workflow (check your bounce review property or workflow history)
   - Manually set back to marketing contacts in the UI
3. Clear your bounce review property values in bulk if needed.

## Weekly Review Process

For contacts flagged at your review threshold:

1. Export the flagged contacts list.
2. For each contact, check:
   - Is the email domain still active? (Quick MX record check)
   - Is this a known customer or high-value contact?
   - Was the bounce recent or historical?
3. **Delete** contacts with invalid domains or clearly fake emails.
4. **Keep suppressed** contacts with valid domains but repeated soft bounces.
5. Clear the bounce review property after review.
