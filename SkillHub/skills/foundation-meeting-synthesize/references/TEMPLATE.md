---
artifact_type: meeting-synthesis
version: 1.0
generated_at: {{ISO 8601 timestamp}}
generated_by_skill: foundation-meeting-synthesize

project: {{project-slug}}
topics:
  - {{topic-slug}}

time_range:
  start: {{YYYY-MM-DD}}
  end: {{YYYY-MM-DD}}

scope_filter: "{{filter applied, or 'none'}}"

source_meetings:
  - {{recap-filename-1.md}}
  - {{recap-filename-2.md}}
  - {{recap-filename-3.md}}

input_quality: {{high | medium | low (weighted across sources)}}
confidence: {{high | medium | low}}
visibility: team
status: draft
---

# Meeting synthesis: {{Topic / initiative / scope}}

## Shareable summary

> [guidance: scope + 2-3 sentence headline takeaway + 3-5 key themes + top open items + top prioritized follow-ups]

**Synthesis scope**: {{Topic}} across {{N}} meetings, {{Date range}}

{{2-3 sentence headline takeaway capturing the arc or state}}

**Key themes**:
- {{Theme 1}}
- {{Theme 2}}
- {{Theme 3}}

**Top open items**:
- {{Stalled thread 1}}
- {{Stalled thread 2}}

**Top priority follow-ups**:
- {{High-priority follow-up 1}}
- {{High-priority follow-up 2}}

---

## Full synthesis

### Scope

- **Topic or initiative**: {{Name}}
- **Time range**: {{Start date}} to {{End date}}
- **Meetings included** ({{N}}):
  - {{Date}}: {{Meeting name}} ([recap filename]({{path}})) [input quality: {{level}}]
  - {{Date}}: {{Meeting name}} ([recap filename]({{path}})) [input quality: {{level}}]
- **Scope filter applied**: {{filter description or "none"}}
- **Sources used**: {{Recaps / notes / transcripts mix}}

### Timeline

> [guidance: plain-text markdown chronological rendering, no binary images. Each entry: date | event | shift. Flag contradictions and low-confidence items inline.]

```
{{Date}}  |  {{Meeting / event name}}
          |  → {{Key decision or shift}}
          |  {{Optional: confidence or flag}}
          |
{{Date}}  |  {{Meeting / event name}}
          |  → {{Key decision or shift}}
          |  [!] {{Contradiction flag if applicable}}
          |
{{Date}}  |  {{Meeting / event name}}
          |  → {{Key decision or shift}}
```

### Themes

#### {{Theme 1}} [confidence: {{level}}. {{rationale, e.g., "appears in 5/5 meetings"}}]

{{Description of the theme and where it appeared}}

- {{Meeting date}}: {{Manifestation}}
- {{Meeting date}}: {{Manifestation}}

#### {{Theme 2}} [confidence: {{level}}]

{{Description}}

> [guidance: repeat per theme]

### Stakeholder position tracking

**{{Stakeholder 1}}**

- **Position evolution**: {{Initial view → Current view}}
- **Key statements**:
  - {{Date}}: "{{paraphrased position}}"
  - {{Date}}: "{{paraphrased position}}"
- **Alignment state**: {{aligned with team / divergent / shifting}}

**{{Stakeholder 2}}**

> [guidance: repeat per key stakeholder]

### Consolidated decision list

> [guidance: decisions from across all meetings in scope, chronological, with source citations]

| Date | Decision | Context | Meeting | Confidence |
|------|----------|---------|---------|------------|
| {{Date}} | {{Decision}} | {{Brief context}} | {{Meeting name}} | {{level}} |

### Decision evolution (resolved)

> [v1.1.0. split from contradictions. Decision evolution captures supersedes-chains: later decisions that replaced earlier ones. Historical context. NO [!] visual emphasis. this is expected, not a red flag.]

**{{Topic 1}}**

- **{{Earlier date}}** ({{Meeting}}): {{Earlier decision}}
- **{{Later date}}** ({{Meeting}}): {{Later decision supersedes earlier}}
- **Context**: {{why the shift. new evidence, stakeholder input, reality-check}}

### Unresolved contradictions (⚠)

> [guidance: the highest-value archaeology output. decisions or positions CURRENTLY in conflict that need reconciliation. Reserve [!] emphasis for this section only. If no live contradictions, state "No live unresolved contradictions as of {{date}}."]

**[!] {{Contradiction 1}}**

- **{{Date}}** ({{Meeting}}): {{Earlier decision or position}}
- **{{Date}}** ({{Meeting}}): {{Later decision or position that conflicts}}
- **Status**: unresolved. needs reconciliation

**[!] {{Contradiction 2}}**

> [guidance: repeat structure for unresolved cases only]

### Open items and stalled threads

- **{{Open item 1}}**: {{Why it is stuck, when it last surfaced, last meeting to touch it}}
- **{{Open item 2}}**: {{Why it is stuck, when it last surfaced}}

### Narrative summary

> [guidance: the "story" of this meeting set in 2-3 paragraphs. what happened, what changed, where we are, what is at stake. Prose, not bullets.]

{{Paragraph 1}}

{{Paragraph 2}}

{{Paragraph 3}}

### Prioritized follow-up suggestions

> [guidance: the "now what". actionable next steps ranked by priority]

**[High priority]**

- {{Follow-up 1}}: {{Why this matters now, suggested owner or forum}}
- {{Follow-up 2}}: {{Why this matters now}}

**[Medium priority]**

- {{Follow-up 3}}: {{Rationale}}
- {{Follow-up 4}}: {{Rationale}}

**[Lower priority / monitor]**

- {{Follow-up 5}}: {{Rationale}}

---

## Sources & References

### Primary inputs (source meetings)

- {{recap-filename-1.md}} ({{date}}). input quality: {{level}}
- {{recap-filename-2.md}} ({{date}}). input quality: {{level}}
- {{recap-filename-3.md}} ({{date}}). input quality: {{level}}

### Referenced artifacts

- Prior syntheses on this topic: {{filenames or "none"}}
- Related project briefs: {{filenames or "none"}}

### External references

- {{Docs cited across the meeting set}}

### Generation context

- **Generated**: {{Timestamp}}
- **Skill version**: 1.0.0
- **Input quality**: {{weighted average across sources}}. {{rationale}}
- **Overall confidence**: {{level}}. {{rationale}}
- **Known gaps**: {{topics or time periods with thin coverage}}
- **Scope filter**: {{as applied, or "none"}}
- **Format hint**: {{default | board-prep | onboarding | retro-input | exec-brief}}
