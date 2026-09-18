# Satori Registry Submission Guide

> Complete, copy-paste-ready content for each registry. Read each section carefully — formats differ.

---

## Prerequisites

```bash
# Install GitHub CLI if not already installed
brew install gh          # macOS
# or: sudo apt install gh  # Ubuntu/Debian

# Authenticate
gh auth login

# Verify
gh auth status
```

---

## 1. BehiSecc/awesome-claude-skills (8.2k stars — Start Here)

**Format:** Simple bullet list: `- [Name](URL) - Description`
**Sections:** Document Skills, Development, Data/Analysis, Scientific, Writing, etc.
**Best fit section:** Look for a "Productivity" or general section. If none fits, add under the most relevant existing category.

### Entry to add:

```markdown
- [Satori](https://github.com/MetcalfSolutions/Satori) - Clinically informed wisdom companion blending IFS, DBT, Stoicism, Buddhism, and six other traditions into a structured thinking partner.
```

### Commands:

```bash
cd /tmp/satori-registry-submissions
gh repo fork BehiSecc/awesome-claude-skills --clone=true
cd awesome-claude-skills
git checkout -b add-satori

# Edit README.md — find the appropriate section, add the entry alphabetically
# (Satori goes after entries starting with R, before entries starting with T)

git add README.md
git commit -m "Add Satori - clinically informed wisdom companion"
git push -u origin add-satori
gh pr create \
  --title "Add Satori - wisdom companion Claude skill" \
  --body "Adding Satori, a structured Claude skill that blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) and eight wisdom traditions (Stoicism, Buddhism, Taoism, Sufi wisdom, and others) into a disciplined thinking partner.

Key features:
- 211k+ characters of structured reference architecture
- Jungian Shadow Work protocol (5-session arc)
- Dark Night protocol (presence-only mode for non-clinical despair)
- Structured onboarding sequence
- Free, open-source, Apache 2.0

GitHub: https://github.com/MetcalfSolutions/Satori"
cd ..
```

---

## 2. majiayu000/claude-skill-registry (JSON Registry)

**Format:** Structured JSON in `registry.json`
**Process:** Add a JSON entry to the registry file

### JSON entry to add:

```json
{
  "name": "satori",
  "repo": "MetcalfSolutions/Satori",
  "path": ".",
  "description": "Clinically informed wisdom companion blending clinical psychology and eight philosophical traditions into a structured thinking partner with Shadow Work, Dark Night protocol, and guided onboarding.",
  "category": "personal-development",
  "tags": ["mental-health", "psychology", "wisdom", "philosophy", "ifs", "stoicism", "jungian", "conversation"],
  "author": "MetcalfSolutions",
  "source_url": "https://github.com/MetcalfSolutions/Satori",
  "license": "Apache-2.0"
}
```

### Commands:

```bash
cd /tmp/satori-registry-submissions
gh repo fork majiayu000/claude-skill-registry --clone=true
cd claude-skill-registry
git checkout -b add-satori

# Edit registry.json — add the JSON entry above to the array
# Also check if there's a skills/ directory that needs an entry

git add .
git commit -m "Add satori to registry"
git push -u origin add-satori
gh pr create \
  --title "Add satori to registry" \
  --body "Adding Satori, a clinically informed wisdom companion that blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) and eight wisdom traditions into a structured thinking partner.

GitHub: https://github.com/MetcalfSolutions/Satori
License: Apache 2.0"
cd ..
```

---

## 3. karanb192/awesome-claude-skills (237 stars)

**Format:** Entries include name (linked), source repo, description, use case, and star rating.
**Note:** Low activity (8 commits). May not get merged quickly.

### Entry to add (adapt to match their exact format after reading the README):

```markdown
- [Satori](https://github.com/MetcalfSolutions/Satori) - Clinically informed wisdom companion blending IFS, DBT, Stoicism, Buddhism, and six other traditions into a structured thinking partner. Features Shadow Work, Dark Night protocol, and guided onboarding.
```

### Commands:

```bash
cd /tmp/satori-registry-submissions
gh repo fork karanb192/awesome-claude-skills --clone=true
cd awesome-claude-skills
git checkout -b add-satori

# Read README.md carefully — they may use a more complex format with
# verification status, star ratings, etc. Match their format exactly.

git add README.md
git commit -m "Add Satori - clinically informed wisdom companion"
git push -u origin add-satori
gh pr create \
  --title "Add Satori - wisdom companion Claude skill" \
  --body "Adding Satori, a structured Claude skill that blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) and eight wisdom traditions into a disciplined thinking partner.

Key features:
- 211k+ characters of structured reference architecture
- Jungian Shadow Work protocol (5-session arc)
- Dark Night protocol (presence-only mode for non-clinical despair)
- Structured onboarding sequence
- Free, open-source, Apache 2.0

GitHub: https://github.com/MetcalfSolutions/Satori"
cd ..
```

---

## 4. VoltAgent/awesome-agent-skills

**Format:** `- **[author/skill-name](URL)** - Short description` (max 10 words!)
**Section:** Community Skills > most relevant subcategory (likely "Other" or "Productivity and Collaboration")
**Caveat:** Requires "real community usage" — brand-new skills may be rejected.

### Entry to add:

```markdown
- **[MetcalfSolutions/Satori](https://github.com/MetcalfSolutions/Satori)** - Wisdom companion blending psychology and philosophy traditions
```

### Commands:

```bash
cd /tmp/satori-registry-submissions
gh repo fork VoltAgent/awesome-agent-skills --clone=true
cd awesome-agent-skills
git checkout -b add-satori

# Edit README.md — add under Community Skills > Other (or best-fit subcategory)

git add README.md
git commit -m "Add skill: MetcalfSolutions/Satori"
git push -u origin add-satori
gh pr create \
  --title "Add skill: MetcalfSolutions/Satori" \
  --body "Adding MetcalfSolutions/Satori, a clinically informed wisdom companion that blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) and eight wisdom traditions into a structured conversation partner.

Key features:
- 211k+ characters of structured reference architecture
- Jungian Shadow Work protocol (5-session arc)
- Dark Night protocol for non-clinical despair
- Structured onboarding sequence
- Free, open-source, Apache 2.0

GitHub: https://github.com/MetcalfSolutions/Satori"
cd ..
```

---

## 5. sickn33/antigravity-awesome-skills (1,372+ skills)

**Format:** Each skill is a file at `skills/<skill-name>/SKILL.md` with YAML frontmatter. Not a README edit.
**Commit format:** `feat: add satori skill`
**Validation:** Run `npm run validate` before submitting PR.

### File to create: `skills/satori/SKILL.md`

```markdown
---
name: satori
description: "Clinically informed wisdom companion blending psychology and philosophy into a structured thinking partner"
category: personal-development
risk: safe
source: community
date_added: "2026-04-05"
author: MetcalfSolutions
tags: [mental-health, psychology, wisdom, philosophy, ifs, stoicism, jungian, conversation]
tools: [claude]
---

## Overview

Satori is a clinically informed AI wisdom companion built as a Claude skill. It blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) with eight philosophical traditions (Stoicism, Buddhism, Taoism, Sufi wisdom, Jungian depth psychology, and others) into a structured thinking partner.

## When to Use

- When seeking a structured philosophical or psychological conversation partner
- When exploring internal conflicts through IFS or Jungian frameworks
- When working through difficult emotions using DBT-informed approaches
- When needing presence-based support during periods of deep despair (Dark Night protocol)

## How It Works

Satori operates as a SKILL.md-based Claude skill with 211k+ characters of structured reference architecture. It provides:

1. **Guided onboarding** that establishes the relationship framework
2. **Multiple therapeutic modalities** (IFS, DBT, CFT, Schema Therapy)
3. **Eight wisdom traditions** for philosophical depth
4. **Specialized protocols** for specific situations

## Examples

- "I'd like to explore a recurring pattern in my relationships" → IFS-informed parts work
- "I'm feeling deep existential despair" → Dark Night protocol (presence-only mode)
- "Help me understand my shadow" → Jungian Shadow Work (5-session arc)

## Best Practices

- Satori is a thinking partner, not a therapy replacement
- Allow the onboarding sequence to complete for best results
- Engage honestly — the system responds to authentic engagement

## Security & Safety Notes

- No data collection or external API calls
- All processing happens within the Claude conversation
- Explicitly not a clinical tool — includes appropriate disclaimers
- Safe for general use

## Related Skills

None currently.
```

### Commands:

```bash
cd /tmp/satori-registry-submissions
gh repo fork sickn33/antigravity-awesome-skills --clone=true
cd antigravity-awesome-skills
git checkout -b add-satori

mkdir -p skills/satori
# Create the SKILL.md file with the content above

npm install  # if package.json exists
npm run validate  # validate before committing

git add skills/satori/SKILL.md
git commit -m "feat: add satori skill"
git push -u origin add-satori
gh pr create \
  --title "feat: add satori wisdom companion skill" \
  --body "Adding Satori, a clinically informed wisdom companion that blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) and eight wisdom traditions into a structured thinking partner.

GitHub: https://github.com/MetcalfSolutions/Satori
License: Apache 2.0
Risk: safe
Category: personal-development"
cd ..
```

---

## 6. ComposioHQ/awesome-claude-skills (32.5k stars)

**Format:** `- [skill-name](URL) - Short description ending with period.`
**Sections:** Document Processing, Development & Code Tools, Data & Analysis, Business & Marketing, Communication & Writing, Creative & Media, Productivity & Organization, Collaboration & Project Management, Security & Systems
**Sorting:** Alphabetical within sections.
**Best fit:** Productivity & Organization

### CAVEAT

This repo's entries currently link to `https://github.com/anthropics/skills/tree/main/skills/...` — they may only list skills from the official Anthropic skills repository. Check the current README before submitting. If all entries point to the official repo, this may not accept external community skills.

### Entry to add (if external skills are accepted):

```markdown
- [satori](https://github.com/MetcalfSolutions/Satori) - Clinically informed wisdom companion blending psychology and philosophy into a structured thinking partner.
```

Insert alphabetically under "Productivity & Organization" (after entries starting with R, before T).

### Commands:

```bash
cd /tmp/satori-registry-submissions
gh repo fork ComposioHQ/awesome-claude-skills --clone=true
cd awesome-claude-skills
git checkout -b add-satori

# FIRST: Check if any entries link to external repos (not anthropics/skills)
# If ALL entries are anthropics/skills links, skip this submission

git add README.md
git commit -m "Add Satori - clinically informed wisdom companion"
git push -u origin add-satori
gh pr create \
  --title "Add Satori - clinically informed wisdom companion skill" \
  --body "Adding Satori, a structured Claude skill that blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) and eight wisdom traditions (Stoicism, Buddhism, Taoism, Sufi wisdom, and others) into a disciplined thinking partner.

Key features:
- 211k+ characters of structured reference architecture
- Jungian Shadow Work protocol (5-session arc)
- Dark Night protocol (presence-only mode for non-clinical despair)
- Structured onboarding sequence
- Free, open-source, Apache 2.0

GitHub: https://github.com/MetcalfSolutions/Satori"
cd ..
```

---

## 7. travisvn/awesome-claude-skills

**Format:** Table format for community skills: `| **[skill-name](URL)** | Description |`
**Section:** Community Skills > Individual Skills (table)
**IMPORTANT REQUIREMENTS:**
- **Minimum 10 GitHub stars required**
- **PRs must NOT be "explicitly generated/submitted with AI-assistance"**
- One item per PR preferred

### Entry to add:

```markdown
| **[Satori](https://github.com/MetcalfSolutions/Satori)** | Clinically informed wisdom companion blending IFS, DBT, Stoicism, Buddhism, and six other traditions into a structured thinking partner |
```

### Commands:

```bash
cd /tmp/satori-registry-submissions
gh repo fork travisvn/awesome-claude-skills --clone=true
cd awesome-claude-skills
git checkout -b add-satori

# Edit README.md — find the Individual Skills table under Community Skills
# Add the entry row

git add README.md
git commit -m "Add Satori - wisdom companion Claude skill"
git push -u origin add-satori
gh pr create \
  --title "Add Satori - wisdom companion Claude skill" \
  --body "Adding Satori, a structured Claude skill that blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) and eight wisdom traditions into a disciplined thinking partner.

Key features:
- 211k+ characters of structured reference architecture
- Jungian Shadow Work protocol (5-session arc)
- Dark Night protocol (presence-only mode for non-clinical despair)
- Structured onboarding sequence
- Free, open-source, Apache 2.0

GitHub: https://github.com/MetcalfSolutions/Satori"
cd ..
```

---

## 8. e2b-dev/awesome-ai-agents (27.1k stars — Tier 3)

**Format:** Detailed format with title, description, expandable details block containing category tags, feature list, and links.
**Position Satori as:** A "cognitive agent" / conversational agent, not just a prompt.

### Entry to add:

```markdown
### Satori

Clinically informed AI wisdom companion that blends clinical psychology frameworks and eight philosophical traditions into a structured thinking partner.

<details>

**Category:** Conversational, Personal Development

- Blends IFS, DBT, CFT, Schema Therapy with Stoicism, Buddhism, Taoism, Sufi wisdom, and Jungian depth psychology
- Jungian Shadow Work protocol (5-session arc)
- Dark Night protocol (presence-only mode for non-clinical despair)
- 211k+ characters of structured reference architecture
- Free, open-source (Apache 2.0)

[GitHub](https://github.com/MetcalfSolutions/Satori)

</details>
```

### Commands:

```bash
cd /tmp/satori-registry-submissions
gh repo fork e2b-dev/awesome-ai-agents --clone=true
cd awesome-ai-agents
git checkout -b add-satori

# Edit README.md — find the open-source section, add entry

git add README.md
git commit -m "Add Satori - clinically informed wisdom companion agent"
git push -u origin add-satori
gh pr create \
  --title "Add Satori - wisdom companion cognitive agent" \
  --body "Adding Satori, a clinically informed AI wisdom companion that blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) and eight philosophical traditions into a structured thinking partner.

Positioning: Satori operates as a cognitive agent with 211k+ characters of structured reference architecture, not a simple prompt. It includes multi-session protocols (Shadow Work 5-session arc), state-aware responses (Dark Night protocol), and guided onboarding.

GitHub: https://github.com/MetcalfSolutions/Satori
License: Apache 2.0"
cd ..
```

---

## 9. kyrolabs/awesome-agents (Tier 3)

**Format:** Linked project name + 1-2 sentence description + shields.io star badge.
**Best section:** Conversational / General Agents

### Entry to add:

```markdown
- [Satori](https://github.com/MetcalfSolutions/Satori) - Clinically informed wisdom companion blending IFS, DBT, Stoicism, Buddhism, and six other traditions into a structured thinking partner for Claude. ![GitHub stars](https://img.shields.io/github/stars/MetcalfSolutions/Satori?style=social)
```

### Commands:

```bash
cd /tmp/satori-registry-submissions
gh repo fork kyrolabs/awesome-agents --clone=true
cd awesome-agents
git checkout -b add-satori

# Edit README.md — find conversational/general agents section

git add README.md
git commit -m "Add Satori - clinically informed wisdom companion"
git push -u origin add-satori
gh pr create \
  --title "Add Satori - wisdom companion agent" \
  --body "Adding Satori, a clinically informed AI wisdom companion that blends clinical psychology and eight philosophical traditions into a structured thinking partner.

GitHub: https://github.com/MetcalfSolutions/Satori
License: Apache 2.0"
cd ..
```

---

## 10. Shubhamsaboo/awesome-llm-apps — SKIP

**Reason:** This is a runnable code collection, not a link list. Projects contain actual application code in the repo. Satori is a Claude skill (SKILL.md), not a standalone LLM application with runnable code. Not a good fit.

---

## Execution Order (Recommended)

1. BehiSecc (simplest, most active)
2. majiayu000 (JSON, automated)
3. karanb192 (simple format)
4. VoltAgent (if you have community traction to point to)
5. antigravity (structured, needs validation)
6. ComposioHQ (verify external submissions accepted first)
7. travisvn (ensure 10+ stars, write PR by hand)
8. e2b-dev (detailed format)
9. kyrolabs (framework-focused)
