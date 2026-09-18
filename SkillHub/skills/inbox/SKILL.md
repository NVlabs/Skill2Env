---
name: inbox
description: "Email triage system that handles both one-time setup and recurring triage in a single skill. Auto-detects state: if no knowledge base exists at ${WORKSPACE}/Email/, runs an 8-section onboarding interview (grill-me discipline, one question at a time) to build a 7-file personalized KB, then offers to run triage immediately. If the KB already exists, skips setup and goes straight to triage — searches recent emails, classifies them via the user's taxonomy, researches new senders, generates TAKE IT/WORTH/PASS/FLAG recommendations, drafts replies (NEVER sends), delivers a report, and updates the KB. Use with 'update' argument to refresh preferences. Setup triggers: 'set up my inbox', 'configure inbox triage', 'set up my email system', 'configure email triage', 'build my email knowledge base', 'initialize email management'. Triage triggers: 'triage my inbox', 'inbox triage', 'check my email', 'run email triage', 'process my inbox', 'what's new in my email', 'handle my email', 'email triage'."
metadata:
  paired_skills: "self-contained — setup and triage in one skill"
---

# Inbox — Email Triage System

Self-contained email triage skill. Handles setup and recurring triage in a single command. Detects its own state and routes accordingly — no need to remember which mode to run.

## State Detection (Always First)

Before anything else, check for the KB:

| State | Route |
|---|---|
| Argument is `update` | → **Update Mode** |
| `${WORKSPACE}/Email/email-taxonomy.md` does NOT exist | → **Setup Mode** |
| `${WORKSPACE}/Email/email-taxonomy.md` exists | → **Triage Mode** |

**Edge cases:**
- User says "set up my inbox" but KB exists → acknowledge, ask: "run triage / update preferences / both?"
- User says "triage my inbox" but no KB → "No knowledge base found. Running setup first, then triage immediately after." → Setup → Triage
- Partial KB (some files missing) → list which files are missing, ask: "run full setup / fill in only the missing sections?"

---

## SETUP MODE — Build the Knowledge Base

Runs when no KB exists.

### Conduct Discipline

**Do NOT generate all files at once.** Walk through the 8 sections one at a time. Each section commits its file(s) before moving on. Partial completion (user drops off mid-interview) still produces a usable partial KB.

- **One question per turn.** Never bundle — even across section boundaries.
- **"Why I'm asking" on every question** — users answer better when they know what's at stake.
- **Forcing format where possible.** Multi-choice > open-ended.
- **Dependency-ordered.** Section N informs Section N+1.

See `references/grill_me_section_walk.md` for the 8-section discipline detail.

### Knowledge Base — 7 Files to Produce

Write to `${WORKSPACE}/Email/`:

| File | Purpose | Required? |
|---|---|---|
| `email-taxonomy.md` | Classification system + report preferences | **Yes** |
| `email-patterns.md` | Reply voice, tone, templates, hard rules | **Yes** |
| `evaluation-framework.md` | Decision tree for opportunity emails | Only if user receives pitches/opportunities |
| `rate-card.md` | Pricing, terms, negotiation posture | Only if user has pricing |
| `blocklist.md` | Auto-skip senders + learned decline patterns | **Yes** (seeded, grows over time) |
| `tracker.md` | Active follow-ups, overdue items, deadlines | **Yes** (starts mostly empty) |
| `triage-log/` | Directory for per-run logs | **Yes** (created empty) |

### Stop Condition

~25–31 questions total across 8 sections. Hard ceiling: 35 questions including sub-clarifications. Section 4 (Evaluation Framework) is skipped entirely when Section 1 surfaced no opportunity-email category. After Section 8's confirmation + handoff message, intake is closed — to change preferences, use `update` mode.

### Section 1: The Big Picture

Six grill-me questions, one at a time:

- **S1.Q1:** "What do you do? Give me your role and business in 1–2 sentences. *Why I'm asking:* Context shapes what email patterns to expect — a solo creator's inbox looks nothing like an enterprise PM's."
- **S1.Q2:** "What dominates your inbox? Pick the top 1–2: sales pitches / client work / internal team / newsletters / customer support / financial / other. *Why I'm asking:* Dominant categories drive the taxonomy."
- **S1.Q3:** "Rough volume split — e.g., '60% business inquiries, 20% ops, 20% noise'. *Why I'm asking:* The split tells me where to focus triage effort."
- **S1.Q4:** "Which email address(es) should triage cover? *Why I'm asking:* If multiple, I'll set up per-address taxonomies."
- **S1.Q5:** "Run frequency: once daily / 2x daily / 3x daily / on-demand only? *Why I'm asking:* Drives the default search window in triage (9h overlap for 2x/day)."
- **S1.Q6:** "Anyone helping manage email — assistant, VA, team — or solo? *Why I'm asking:* Persona handling differs for delegated inboxes."

**Action:** Build mental model. Do NOT write files yet. Note whether opportunity emails are a category (drives S4 skip-logic).

### Section 2: Email Categories

Propose 5–7 categories based on Section 1 — pre-recommend a subset:

- New Opportunities
- Active Conversations
- Action Required
- Financial
- Important/Personal
- Informational
- Ignore/Low Priority

Three forcing questions, one at a time:

- **S2.Q1:** "Here's my proposed taxonomy: [list]. Does this match your inbox reality — yes / mostly / no? *Why I'm asking:* If 'no', I need to redo the taxonomy before any other section makes sense."
- **S2.Q2:** "Missing categories? List them. (Skip if none.) *Why I'm asking:* Missing categories produce uncategorized emails downstream, which hurts triage quality."
- **S2.Q3:** "Which category takes the MOST time per email? *Why I'm asking:* That's where draft-reply effort needs to focus most."

**Action:** Generate `email-taxonomy.md` with categories, signals, and default actions per category.

### Section 3: Reply Style & Voice

Six grill-me questions plus the critical sample request:

- **S3.Q1:** "Register: formal / casual / in-between? *Why I'm asking:* Calibrates default voice; we'll refine from samples next."
- **S3.Q2:** "Three communication pet peeves — phrases you hate, openings you avoid. *Why I'm asking:* I treat these as forbidden tokens in drafts."
- **S3.Q3:** "Phrases or sign-offs you always use — list as many as come to mind. *Why I'm asking:* These are your voice fingerprints."
- **S3.Q4:** "Different persona for different contexts — e.g., assistant replies as you? *Why I'm asking:* Persona context changes pronoun + signature handling."
- **S3.Q5:** "Typical reply length — one-liner / short paragraph / longer? *Why I'm asking:* Length is the easiest voice signal to get wrong."
- **S3.Q6:** "Hard rules — never X / always Y? *Why I'm asking:* Hard rules are enforced as non-negotiable in every draft."

**S3.SAMPLES (highest-quality input):**

> **Paste 3–5 real sent emails from your inbox.**
>
> *Why I'm asking:* Self-description of voice is unreliable. Real samples are the best signal — use `scripts/voice_sample_analyzer.py` to extract patterns.

**Action:** Generate `email-patterns.md`. See `references/voice_calibration.md` for the sample-extraction discipline.

### Section 4: Evaluation Framework (Conditional)

**Skip if Section 1 surfaced no opportunity emails.** Otherwise six grill-me questions:

- **S4.Q1:** "First thing you check when pitched something — give me your gut filter. *Why I'm asking:* That's the top of the decision tree."
- **S4.Q2:** "Three instant deal-breakers. *Why I'm asking:* These become PASS-auto signals."
- **S4.Q3:** "Three things that make you immediately interested. *Why I'm asking:* These become TAKE-IT signals."
- **S4.Q4:** "Standard pricing / terms — or 'no fixed pricing'? *Why I'm asking:* If you have a rate card, I'll generate one."
- **S4.Q5:** "Negotiation posture: firm / flexible / depends on context? *Why I'm asking:* Drives draft tone on counter-offers."
- **S4.Q6:** "VIP senders or organizations that always get engagement. *Why I'm asking:* VIP list bypasses normal PASS filters."

**Action:** Generate `evaluation-framework.md` + `rate-card.md` (if pricing exists).

### Section 5: Blocklist & Patterns

- **S5.Q1:** "Senders or domains to always skip. (Skip if none.) *Why I'm asking:* Auto-blocklist saves the most time per run."
- **S5.Q2:** "Patterns in emails you always delete. *Why I'm asking:* Patterns let triage auto-skip variants without exact-match maintenance."
- **S5.Q3:** "Specific companies / recruiters / newsletters wasting time. *Why I'm asking:* These seed the blocklist; triage will add more as you override decisions."

**Action:** Generate `blocklist.md`.

### Section 6: Current State

- **S6.Q1:** "Active threads you're tracking — list with one-line context each. (Skip if none.) *Why I'm asking:* These become tracker entries so triage knows existing context."
- **S6.Q2:** "Overdue replies? *Why I'm asking:* Triage flags these as priority every run until resolved."
- **S6.Q3:** "Time-sensitive items with deadlines? *Why I'm asking:* Tracker enforces deadlines and surfaces them as overdue at the right time."

**Action:** Generate `tracker.md` + create empty `triage-log/` directory.

### Section 7: Report Preferences

- **S7.Q1:** "Delivery format: email draft to self / file in workspace / chat summary only. *Why I'm asking:* The triage report goes here every run."
- **S7.Q2:** "Detail level: 30-second scan / detailed breakdown / both. *Why I'm asking:* Affects report length."
- **S7.Q3:** "Anything always shown first — e.g., overdue payments, VIP messages? *Why I'm asking:* Custom top-of-report rules surface what you care about above standard sections."

**Action:** Append report preferences to `email-taxonomy.md`.

### Section 8: Confirmation & Handoff

List every file created with a one-sentence summary. Run `scripts/kb_validator.py --workspace ${WORKSPACE}` to confirm the 7-file contract is satisfied.

Then ask:

> **Your triage system is ready. Run triage now?**
> 1. Yes — process my inbox immediately
> 2. No — I'll invoke it separately

If yes → transition directly to **Triage Mode** below.

### Privacy Boundary

**Never persist passwords, full account numbers, SSNs, or other sensitive credentials in KB files.** If volunteered during the interview, acknowledge but don't store — write `[stored separately by user]` in the relevant file.

---

## TRIAGE MODE — Recurring Email Triage

Runs when KB exists. Light-intake by design.

### DRAFTS ONLY — Never Send

> **This skill creates drafts. It NEVER sends.**

Non-negotiable. The `scripts/draft_safety_validator.py` enforces it post-run. Any send-shaped tool call in the action log fails validation. See `references/drafts_only_safety.md`.

### Step 0: Grill-Me Intake (0–2 Optional Override Questions)

**Q1** (only when on-demand run is outside normal cadence):
> **Override the default 9-hour search window? yes (specify hours) / no.**
>
> *Why I'm asking:* If you're running outside your normal cadence, you may want a wider or narrower window.

**Q2** (only when user invokes with category-skip intent):
> **Skip any categories this run? E.g., "skip newsletters".**
>
> *Why I'm asking:* Sometimes you just want to scan opportunities or clear active threads.

**Max 2 questions.** Default invocations skip both and run with KB-default preferences.

### Step 1: Determine Search Window

Use `scripts/search_window_calculator.py --cadence <CADENCE> --now <ISO>`:

| Cadence (from email-taxonomy.md) | Default window |
|---|---|
| once daily | 26h |
| 2x daily | 9h |
| 3x daily | 6h |
| on-demand only | 24h (asks Q1) |

### Step 2: Email Search

Two queries:

- **Primary:** Inbox + sent after `window_start`
- **Secondary:** Starred unread (catch flagged items missed in primary)

Collect per email: sender, subject, date, snippet, thread ID, labels.

Provider adapter:

| Provider | Tool |
|---|---|
| Gmail | Gmail MCP |
| Outlook / Microsoft 365 | Outlook MCP |
| IMAP (Fastmail, ProtonMail, etc.) | IMAP MCP if available; halt otherwise |
| (no email tool available) | Halt: "No email tool registered for this session." |

### Step 3: Classification

Apply taxonomy from `email-taxonomy.md`. For lowest-priority category (newsletters/automation/spam): skip thread reads entirely. For everything else: read full thread.

### Step 4: Sender Research

For senders not in tracker / blocklist / prior logs:

1. Check `blocklist.md` → if matched, auto-skip
2. Check `tracker.md` → if known thread, note existing context
3. For opportunity senders: web search for legitimacy, social presence, intermediary status

**Skip entirely** for: known senders, internal email, automated notifications, obvious low-priority.

### Step 5: Recommendations

Apply `evaluation-framework.md` (skip this step entirely if file doesn't exist):

| Category | When | Output |
|---|---|---|
| **TAKE IT** | Meets criteria | Recommend engaging; draft reply (Step 6) |
| **WORTH CONSIDERING** | Has potential, needs user judgment | Surface context; draft for user to edit |
| **PASS** | Doesn't meet criteria | Brief "why" (1–3 sentences); draft polite decline |
| **FLAG FOR REVIEW** | Unusual; needs direct user decision | Surface fully; NO draft |

See `references/triage_decision_framework.md` for the framework canon.

### Step 6: Drafts

Draft using `email-patterns.md` voice rules. **NEVER call any send operation. Only create drafts.**

Draft body must honor:
- Voice register + forbidden tokens (S3.Q2 pet peeves)
- Sign-off patterns + persona context
- Hard rules (S3.Q6 — non-negotiable)
- Reply length per `email-patterns.md`

**Do NOT draft for:** newsletters, automation, FYI threads, already-replied threads, blocked senders.

Tone by recommendation:
- TAKE IT → engaged + concrete next step
- WORTH → curious + 1–2 clarifying questions
- PASS → polite decline + brief reason (no hedging promises)
- FLAG → NO draft

### Step 7: Report Delivery

Honor preference from `email-taxonomy.md`. Default: email draft to self.

**Subject:** `Inbox Triage — [Day], [Month Date] ([Run Label])`

**Sections (in order):**
1. **Overview** — 2–3 sentences. What happened? Anything urgent?
2. **Stats** — Processed / drafts created / action needed / skipped
3. **Action Needed** — Overdue items, decisions, drafts to review, deadlines
4. **Quick Reference** — One line per email: `**Sender** — summary + recommendation`
5. **Detailed Cards** — Opportunities, active threads, flags. No draft text previews.
6. **Footer** — Timestamp + KB update summary

**HTML formatting (if applicable):** inline CSS only (Gmail strips `<style>`). Color-coded: green → TAKE IT, amber → WORTH CONSIDERING, red → PASS, purple → FLAG FOR REVIEW, blue → active conversation.

### Step 8: Knowledge Base Update

**`blocklist.md`:** append new declined senders + patterns; remove if user overrode.

**`tracker.md`:** append new follow-ups, update existing, mark resolved, flag overdue, remove resolved items older than 30 days, add entry to update log.

After 5+ runs, suggest KB improvements: "You always decline emails from X — add as auto-skip?"

### Step 9: Internal Log

Save to `${WORKSPACE}/Email/triage-log/[YYYY-MM-DD]-[run-label].md`:
- Emails processed with classifications
- Recommendations made
- Drafts created (with thread refs)
- KB updates made
- Notable observations

Audit trail for `scripts/draft_safety_validator.py`.

### Step 10: Empty Inbox Handling

Even with zero new emails:
1. Check `tracker.md` for items due today or overdue
2. Generate minimal report: "No new actionable emails since last run"
3. Flag overdue items

Skip Steps 3–6 entirely on empty inbox.

---

## UPDATE MODE — Refresh Preferences

Triggered by `/notion inbox update` or "update my inbox preferences."

1. Detect existing files at `${WORKSPACE}/Email/`
2. For each file, ask: **replace / merge / skip**
3. Walk only the sections whose files the user chose to update
4. Skip sections whose files the user kept

---

## Critical Rules

1. **DRAFTS ONLY — NEVER SEND.** Non-negotiable.
2. **Privacy.** No passwords / credentials in KB files.
3. **Accuracy over speed.** When unsure, flag for review.
4. **Respect the KB.** Documented preferences are source of truth. Don't override with judgment.
5. **Transparency.** Note every KB change in the triage log.
6. **First runs need oversight.** Document this expectation for the user.

## Error Handling

| Situation | Behavior |
|---|---|
| No KB + triage invoked | Run setup first, then triage |
| KB exists + setup invoked | Acknowledge; offer triage / update / both |
| Partial KB (missing files) | List gaps; offer full setup or fill missing sections only |
| Workspace inaccessible | Stop; tell user where files would go; ask for path |
| Email tool unavailable | Halt with clear message |
| User refuses voice samples | Use self-description; flag in patterns file that calibration may need iteration |
| User drops off mid-interview | Honor partial KB; committed files are usable |
| 100+ new emails | Flag volume; offer to focus on priority categories only |
| Sender in both blocklist and tracker | Tracker wins; note inconsistency in log |

## Portability

- **Claude Code CLI:** Native — writes markdown files directly to filesystem, uses Gmail/Outlook MCP.
- **Claude.ai web:** Generate files as artifacts; instruct user to save to workspace.

## Tooling

| Script | Role |
|---|---|
| `scripts/kb_validator.py` | Validates the 7-file KB after setup (required files present, conditional files match sections run, headers + structure correct). |
| `scripts/section_progress_tracker.py` | JSON-backed walk state across the 8 interview sections. |
| `scripts/voice_sample_analyzer.py` | Extracts voice patterns from pasted sent-email samples. |
| `scripts/kb_reader.py` | Reads + validates the 7-file KB at triage start. Halts on missing required files. |
| `scripts/search_window_calculator.py` | Computes `window_start` from cadence + current time. Returns `run_label`. Honors Q1 override. |
| `scripts/draft_safety_validator.py` | Post-run scan of action log for any send-shaped tool call. FAIL if detected. |

## References

- `references/grill_me_section_walk.md` — 8-section discipline, skip-logic, commit-per-section
- `references/voice_calibration.md` — sample-based voice extraction theory + anti-patterns
- `references/kb_file_contract.md` — 7-file contract (structure, sections, read behavior)
- `references/triage_decision_framework.md` — TAKE IT / WORTH / PASS / FLAG taxonomy
- `references/drafts_only_safety.md` — NEVER-SEND discipline canon

## Anti-Patterns To Reject

- Sending emails — drafts only, non-negotiable
- Generating all KB files at once instead of walking sections
- Asking all questions in one batch (breaks grill-me discipline)
- Persisting sensitive credentials in KB
- Operating triage without KB files
- Skipping KB updates at end of triage run
- Overriding user's documented preferences with own judgment
- Skipping the "why this question matters" on setup questions
- Including draft text previews in triage report (drafts are already in email client)
- Provider lock-in without adapter pattern
