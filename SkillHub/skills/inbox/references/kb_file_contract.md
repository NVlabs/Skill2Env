# Knowledge Base File Contract

This reference covers both sides of the 7-file contract: what setup writes and what triage reads. Both modes of the `inbox` skill must agree on every file name, section header, and field exactly.

## The 7 Files at `${WORKSPACE}/Email/`

| File | Required? | Written by | Read by triage for |
|---|---|---|---|
| `email-taxonomy.md` | **yes** | Section 2 + Section 7 | Classification rules + report preferences |
| `email-patterns.md` | **yes** | Section 3 | Voice rules + hard rules + templates |
| `evaluation-framework.md` | conditional | Section 4 (only if S1 surfaced opportunities) | TAKE-IT / PASS signals + VIP list + decision tree |
| `rate-card.md` | conditional | Section 4 (only if user has pricing) | Pricing + negotiation posture for opportunity drafts |
| `blocklist.md` | **yes** (seeded) | Section 5 | Auto-skip rules; appended with new declines each run |
| `tracker.md` | **yes** (seeded) | Section 6 | Active follow-ups; updated each run |
| `triage-log/` | **yes** (empty dir) | Section 6 | Per-run logs written to `<date>-<label>.md` |

---

## File Specs — What Setup Writes

### email-taxonomy.md

```markdown
# Email Taxonomy

## Categories

### {Category Name}
- Signals: {trigger phrases, sender patterns, subject markers}
- Default action: {classify | draft-reply | skip | flag-for-review}
- Typical volume: {N% of inbox}

### {Category 2}
...

## Report Preferences

- Delivery format: {email-draft-to-self | file-in-workspace | chat-summary-only}
- Detail level: {30-second-scan | detailed-breakdown | both}
- Always-shown-first: {overdue payments | VIP messages | custom rules}
```

Generated at: end of Section 2 (categories) + appended at end of Section 7 (Report Preferences).

### email-patterns.md

```markdown
# Email Patterns

## Voice Register
{formal | casual | in-between}

## Pet Peeves (Forbidden Tokens)
- {phrase 1}
- {phrase 2}

## Sign-Offs (Voice Fingerprints)
- {sign-off 1}
- ...

## Persona Context
{single-user | delegated (assistant replies as user) | multi-persona}

## Typical Reply Length
{one-liner | short-paragraph | longer}

## Hard Rules (Non-Negotiable in Every Draft)
- Never: {X}
- Always: {Y}

## Voice Patterns (Extracted from Samples)
- Opening phrases observed: {list}
- Sentence length distribution: {short / medium / long mix}
- Casual / formal markers: {list}

## Templates (Repeated Replies)
- {template name}: {body}
```

The "Voice Patterns" section comes from `scripts/voice_sample_analyzer.py` if samples were provided; otherwise marked `[calibration may need iteration — voice samples not collected during setup]`.

### evaluation-framework.md (conditional)

```markdown
# Evaluation Framework (Opportunity Emails)

## Gut Filter (First Check)
{user's gut filter from S4.Q1}

## TAKE-IT Signals
- {signal 1}
- {signal 2}
- {signal 3}

## PASS Signals (Instant Deal-Breakers)
- {deal-breaker 1}
- {deal-breaker 2}

## Decision Tree

1. If sender in VIP list → TAKE IT (skip filter)
2. If any PASS signal matches → PASS (auto-decline draft)
3. If all TAKE-IT signals match → TAKE IT (auto-engage draft)
4. If partial TAKE-IT match → WORTH CONSIDERING
5. If unusual / ambiguous → FLAG FOR REVIEW

## VIP List (Bypass PASS Filters)
- {sender / domain}

## Negotiation Posture
{firm | flexible | depends-on-context}
```

Skipped entirely if S1 surfaced no opportunity-email category.

### rate-card.md (conditional)

```markdown
# Rate Card

## Standard Pricing
- {service}: {price}

## Terms
- Payment: {net X days | upfront | milestone}
- Revisions included: {N}
- Rush fee: {Y%}

## Counter-Offer Patterns
- If they offer < {floor}: {how to counter}
- If timeline is tight: {how to counter}
```

Skipped if user has no fixed pricing (S4.Q4 = "no fixed pricing").

### blocklist.md (required, seeded)

```markdown
# Blocklist

## Sender / Domain Auto-Skip
- {sender}: {reason} — added {date}

## Decline Patterns (Pattern-Match Auto-Skip)
- "{pattern phrase}": {reason}

## Recently Removed (User Overrode)
- {sender}: removed on {date} — user override
```

Seeded at end of Section 5. Triage appends new declines + observed patterns on every run.

### tracker.md (required, seeded)

```markdown
# Tracker

## Active Follow-Ups

| Item | Context | Deadline | Status |
|---|---|---|---|
| {thread} | {one-line context} | {date} | pending |

## Overdue
- {thread}: missed deadline {date} — {context}

## Resolved (Recent)

## Update Log
- {date}: {what changed} — by {triage run | user}
```

Seeded at end of Section 6. Triage updates on every run.

### triage-log/ (required, empty directory)

Empty directory created at end of Section 6. Triage writes per-run logs to `triage-log/<YYYY-MM-DD>-<run-label>.md`.

---

## What Triage Reads From Each File

### email-taxonomy.md

- All `### {Category Name}` headers under `## Categories`
- Per category: signals + default action
- `## Report Preferences` section (delivery format, detail level, top-of-report rules)

If categories section is empty or malformed → halt: "email-taxonomy.md has no usable categories. Re-run setup."

### email-patterns.md

- `## Voice Register`
- `## Hard Rules` (non-negotiable in every draft)
- `## Pet Peeves` / Forbidden Tokens (NEVER appear in drafts)
- `## Sign-Offs` (rotate through in drafts)
- `## Voice Patterns (Extracted from Samples)` if present
- `## Templates` if present
- `## Voice Calibration Status` — if "samples not collected", use conservative defaults (medium-formal, short-paragraph) on early runs

### evaluation-framework.md (conditional)

- `## Gut Filter` — applied first to opportunity emails
- `## TAKE-IT Signals` — auto-engage if ALL match
- `## PASS Signals` — auto-decline if ANY match
- `## Decision Tree` — branch logic
- `## VIP List` — bypass PASS filters
- `## Negotiation Posture` — drives counter-offer tone

### rate-card.md (conditional)

- `## Standard Pricing` — drives auto-decline when offer < floor
- `## Terms` — payment, revisions, rush
- `## Counter-Offer Patterns`

### blocklist.md (read + append)

- `## Sender / Domain Auto-Skip` — exact match auto-skip
- `## Decline Patterns` — phrase match auto-skip
- `## Recently Removed` — DON'T re-block these

Triage appends: new declined senders + new patterns; removes if user overrode.

### tracker.md (read + update)

- `## Active Follow-Ups` — surfaces in report's "Action Needed"
- `## Overdue` — flagged in every run until resolved
- `## Resolved (Recent)` — for context, not surfaced

Triage updates: adds new follow-ups, updates existing, marks resolved, flags overdue, removes resolved older than 30 days, appends to update log.

### triage-log/ (write only)

Per-run log at `triage-log/<YYYY-MM-DD>-<run-label>.md`:
- Emails processed (count + classifications)
- Recommendations (with reasoning)
- Drafts created (with thread IDs)
- KB updates (explicit before/after)
- Follow-ups added / resolved
- Notable observations

Audit trail for `scripts/draft_safety_validator.py`. After every run, the validator scans the log for send-shaped tool calls.

---

## Fail-Fast Behavior on Missing Files

Triage performs read validation before any other step. Required core files:

- `email-taxonomy.md`
- `email-patterns.md`
- `blocklist.md`
- `tracker.md`
- `triage-log/` (must be a directory)

If any are missing → halt and route to setup or update mode.

## Validation

Run `scripts/kb_validator.py --workspace ${WORKSPACE}` after Section 8 confirmation. It checks:
- All required files exist
- Conditional files exist only if their triggering section ran
- Each file has the expected H1 + section structure
- `triage-log/` is a directory, not a file
