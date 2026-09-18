---
artifact_type: meeting-brief
version: 1.0
generated_at: {{ISO 8601 timestamp}}
generated_by_skill: foundation-meeting-brief

meeting_title: "{{Meeting title}}"
meeting_date: {{YYYY-MM-DD}}
meeting_start_time: "{{HH:MM timezone}}"
meeting_type: {{type or null}}

project: {{project-slug or null}}
topics:
  - {{topic-slug}}

attendees:
  - name: {{name}}
    role: {{role or null}}

stakeholders:
  - name: {{name}}
    position: "{{known or inferred view}}"
  - name: {{name}}
    position: "{{view}}"

primary_ask: "{{What the user needs from the meeting}}"

related_agenda: {{filename if exists, else null}}

input_quality: {{high | medium | low}}
confidence: {{high | medium | low}}
visibility: private
status: draft
---

# Meeting brief: {{Meeting title}}

## Shareable summary

> [guidance: private-use by default. Share only with trusted advisor, co-presenter, or manager if needed. Flags purpose, top 3 goals, key risk, primary ask.]

**{{Meeting title}}** | {{Date}}
**Purpose**: {{One-line purpose}}
**Top goals**:
1. {{Goal 1}}
2. {{Goal 2}}
3. {{Goal 3}}
**Key risk**: {{One-line risk or tension to watch}}
**Primary ask**: {{What the user needs from the meeting}}

---

## Full brief

### Context

- **Meeting**: {{Title}}, {{Date}}, {{Duration}}
- **Format**: {{In-person / remote / hybrid}}
- **Attendees and roles**: {{List}}
- **Chair or facilitator**: {{Name}}

### Background

> [guidance: relevant history, prior decisions, recent developments the user needs top-of-mind]

- {{Point 1}}
- {{Point 2}}
- {{Point 3}}

### Stakeholder reads

> [guidance: per key attendee, capture position, stakes, likely concerns, relationship state, tactical notes]

**{{Stakeholder 1}}** ({{Role}})

- **Position on topic**: {{Known or inferred view}} [confidence: {{level}}]
- **Stakes**: {{What they win or lose}}
- **Likely concerns**: {{What they'll push on}}
- **Relationship state**: {{Strong / neutral / strained}}
- **Tactical notes**: {{How to engage them}}

**{{Stakeholder 2}}** ({{Role}})

- **Position on topic**: {{view}} [confidence: {{level}}]
- **Stakes**: {{stakes}}
- **Likely concerns**: {{concerns}}
- **Relationship state**: {{state}}
- **Tactical notes**: {{notes}}

### Desired outcomes (ranked)

1. **Must achieve**: {{Non-negotiable outcome}}
2. **Should achieve**: {{Strong preference}}
3. **Nice to achieve**: {{Bonus outcome}}

### Key messages

> [guidance: what the user wants to communicate, in priority order, phrased for delivery]

1. {{Message 1}}
2. {{Message 2}}
3. {{Message 3}}

### Anticipated questions and responses

| Question | Prepared response |
|----------|-------------------|
| {{Q1}} | {{Response}} |
| {{Q2}} | {{Response}} |
| {{Q3}} | {{Response}} |

### Risks and tensions

- **{{Risk 1}}**: {{Mitigation}}
- **{{Risk 2}}**: {{Mitigation}}

### Asks

- **From {{Person}}**: {{What the user needs, by when}}
- **From {{Person}}**: {{ask}}

### Success signals

> [guidance: how the user will know the meeting went well in the moment. behavioral cues, not just outcome markers]

- {{Signal 1}}
- {{Signal 2}}

---

## Sources & References

### Primary inputs

- User-provided context: {{summary}}
- Stakeholder summaries (if discovered): {{filenames}}

### Referenced artifacts

- Agenda: {{filename if exists}}
- Prior recaps on this topic: {{filenames}}
- Related stakeholder summaries: {{filenames}}

### External references

- {{Relevant docs and links}}

### Generation context

- **Generated**: {{Timestamp}}
- **Skill version**: 1.0.0
- **Input quality**: {{high | medium | low}}. {{rationale}}
- **Overall confidence**: {{high | medium | low}}. {{rationale}}
- **Known gaps**: {{List or "None identified"}}
- **Inferences applied**: {{list of inferred values with confidence}}
- **Anti-meeting check**: {{Ran. override accepted | Ran. async alternative produced instead}}
