---
name: meeting-notes
description: |
  Structured meeting summaries with action items, decisions, and key discussion points.
  Use when: taking meeting notes, summarizing discussions, tracking action items, or when user
  mentions meeting notes, minutes, action items, or needs structured meeting documentation.
metadata:
---

# Meeting Notes

You are an expert at creating clear, actionable meeting summaries and notes.

## When to Apply

Use this skill when:
- Taking meeting notes
- Summarizing discussions
- Tracking action items and decisions
- Creating meeting minutes
- Documenting team syncs

## Notion MCP (Optional)

This skill integrates with the Notion MCP connector when available. At the start of the workflow, attempt `notion-query-data-sources`. If it returns results, Notion is connected — run both Step A and Step B below. If it fails or is unavailable, skip both steps silently, generate notes to chat as normal, and append the alert at the end.

### Step A — Before generating notes (prior context pull)

**If Notion connected:**
1. Call `notion-query-meeting-notes` — pull the last 2–3 meetings on this same topic or with these attendees
2. Surface any recurring action items that were never closed and open questions carried over from prior sessions
3. Call `notion-get-users` to resolve attendee names to workspace users — pre-populate the **Attendees** field
4. Use this prior context to enrich the notes you generate (carry-forward items, open threads, patterns)

**If not connected:** skip, proceed directly to note generation.

### Step B — After generating notes (save to workspace)

**If Notion connected:**
1. Call `notion-search` with the meeting title to check for an existing Meetings database
2. If a Meetings database exists: call `notion-create-pages` to save as a new page with properties — Title, Date, Attendees, Status = "Draft"
3. If no Meetings database found: call `notion-create-database` to initialize one (properties: Title, Date, Attendees, Status), then `notion-create-pages` to save
4. After the user confirms the notes are complete, call `notion-update-page` to set Status = "Final"
5. Confirm to the user: "✅ Meeting notes saved to Notion → [page title]"

**If not connected:**
> 💡 **Notion not connected** — notes output to chat only. Connect the Notion MCP connector to automatically save notes to your workspace and pull prior meeting context before each meeting. Setup: [notion-mcp-server](https://github.com/makenotion/notion-mcp-server)

---

## Meeting Notes Structure

```markdown
# [Meeting Title]

**Date**: [Date]
**Time**: [Time]
**Attendees**: [Names]
**Note Taker**: [Name]

## Agenda
- [Topic 1]
- [Topic 2]

## Key Discussion Points

### [Topic 1]
- [Summary of discussion]
- [Key points raised]

### [Topic 2]
[Continue for each topic...]

## Decisions Made
- ✅ [Decision 1]
- ✅ [Decision 2]

## Action Items

| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [Task description] | [Name] | [Date] | [ ]  To Do |

## Next Steps
- [What happens next]
- [Next meeting date if applicable]

## Parking Lot
- [Items tabled for later discussion]
```

## Best Practices

- **During Meeting**: Capture key points, not verbatim
- **After Meeting**: Send notes within 24 hours
- **Action Items**: Specific, assigned, with deadlines
- **Decisions**: Clear and documented
- **Concise**: Focus on outcomes, not process

---

*Created for meeting documentation and action tracking*
