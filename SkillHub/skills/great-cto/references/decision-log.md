---
name: decision-log
description: ADR (Architecture Decision Record) catalogue: format, lifecycle (proposed → accepted → superseded), cross-references to RFCs
when_to_use: Recording architecture decisions. Read by architect + project-auditor
applies_to:
  - _default
---

# Decision Log

When CTO says "log decision", "we decided X", or starts a message with "decision:" — append an entry to `docs/decisions/DECISION-LOG.md`.

## Scope

**Non-architectural decisions only** — process changes, vendor picks, waivers, reversible calls.

Architectural decisions still go to individual ADR files (`docs/decisions/ADR-NNN.md`), handled by architect. Do not duplicate ADRs in the Decision Log.

## Append logic

```bash
mkdir -p docs/decisions
LOG="docs/decisions/DECISION-LOG.md"
[ ! -f "$LOG" ] && printf '# Decision Log\n\n' > "$LOG"
NEXT_ID=$(grep -c "^## D-" "$LOG" 2>/dev/null | awk '{printf "%04d", $1+1}')
```

## Entry format

Ask CTO for the missing fields in one message. **Max 1 question** — if 3+ fields are missing, ask only for a one-line description and infer the rest from recent context.

```markdown
## D-<NEXT_ID> — <YYYY-MM-DD> — <one-line title>
**Context:** <why this came up>
**Decision:** <what was decided>
**Alternatives considered:** <what was rejected>
**Reversible:** <yes | partial | no> (<cost to reverse>)
**Owner:** @cto
**Related:** <bd:T-NNN, ADR-NNN, RFC-NNN — if any>
```

Append with a blank line before and after the entry.

## Confirmation

After appending, tell CTO:
```
Logged: D-<NEXT_ID> — <title>
```

No further action needed. The entry surfaces automatically in `/inbox` under "Recent decisions".

## ADR vs Decision Log — choosing

| If the decision is... | Put it in... |
|-----------------------|--------------|
| Structural/architectural (pattern, tech stack, module boundary) | ADR file via architect |
| Reversible process choice (vendor, workflow, tooling) | Decision Log |
| Waiver ("we accept this risk", "we skip this check for now") | Decision Log |
| Trade-off between two roughly equal options | Decision Log (can upgrade to ADR if later discovered structural) |

When unsure, default to Decision Log — promoting to ADR later is cheap; downgrading an ADR is awkward.
