#!/usr/bin/env bash
# Satori Registry Submission Script
# Run each section one at a time. Review edits before committing.
# Usage: Read each section, uncomment and run individually.

set -euo pipefail

WORK_DIR="/tmp/satori-registry-submissions"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

PR_BODY_STANDARD='Adding Satori, a structured Claude skill that blends clinical psychology frameworks (IFS, DBT, CFT, Schema Therapy) and eight wisdom traditions (Stoicism, Buddhism, Taoism, Sufi wisdom, and others) into a disciplined thinking partner.

Key features:
- 211k+ characters of structured reference architecture
- Jungian Shadow Work protocol (5-session arc)
- Dark Night protocol (presence-only mode for non-clinical despair)
- Structured onboarding sequence
- Free, open-source, Apache 2.0

GitHub: https://github.com/MetcalfSolutions/Satori'

echo "=== Satori Registry Submissions ==="
echo "Working directory: $WORK_DIR"
echo ""

# Verify gh is authenticated
if ! gh auth status &>/dev/null; then
  echo "ERROR: gh is not authenticated. Run: gh auth login"
  exit 1
fi
echo "✓ GitHub CLI authenticated"
echo ""

# ──────────────────────────────────────────────
# 1. BehiSecc/awesome-claude-skills
# ──────────────────────────────────────────────
submit_behisecc() {
  echo "=== Submitting to BehiSecc/awesome-claude-skills ==="
  cd "$WORK_DIR"
  gh repo fork BehiSecc/awesome-claude-skills --clone=true 2>/dev/null || true
  cd awesome-claude-skills 2>/dev/null || cd BehiSecc-awesome-claude-skills

  git checkout -b add-satori 2>/dev/null || git checkout add-satori

  echo ""
  echo ">>> MANUAL STEP: Edit README.md"
  echo ">>> Find the appropriate section and add this entry (alphabetically):"
  echo '- [Satori](https://github.com/MetcalfSolutions/Satori) - Clinically informed wisdom companion blending IFS, DBT, Stoicism, Buddhism, and six other traditions into a structured thinking partner.'
  echo ""
  read -p "Press Enter after editing README.md..."

  git add README.md
  git commit -m "Add Satori - clinically informed wisdom companion"
  git push -u origin add-satori
  gh pr create \
    --title "Add Satori - wisdom companion Claude skill" \
    --body "$PR_BODY_STANDARD"

  echo "✓ BehiSecc PR created"
  cd "$WORK_DIR"
}

# ──────────────────────────────────────────────
# 2. majiayu000/claude-skill-registry
# ──────────────────────────────────────────────
submit_majiayu000() {
  echo "=== Submitting to majiayu000/claude-skill-registry ==="
  cd "$WORK_DIR"
  gh repo fork majiayu000/claude-skill-registry --clone=true 2>/dev/null || true
  cd claude-skill-registry 2>/dev/null || cd majiayu000-claude-skill-registry

  git checkout -b add-satori 2>/dev/null || git checkout add-satori

  echo ""
  echo ">>> MANUAL STEP: Edit registry.json"
  echo ">>> Add this JSON entry to the array:"
  cat <<'JSONEOF'
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
JSONEOF
  echo ""
  read -p "Press Enter after editing registry.json..."

  git add .
  git commit -m "Add satori to registry"
  git push -u origin add-satori
  gh pr create \
    --title "Add satori to registry" \
    --body "Adding Satori, a clinically informed wisdom companion.

GitHub: https://github.com/MetcalfSolutions/Satori
License: Apache 2.0"

  echo "✓ majiayu000 PR created"
  cd "$WORK_DIR"
}

# ──────────────────────────────────────────────
# 3. karanb192/awesome-claude-skills
# ──────────────────────────────────────────────
submit_karanb192() {
  echo "=== Submitting to karanb192/awesome-claude-skills ==="
  cd "$WORK_DIR"
  gh repo fork karanb192/awesome-claude-skills --clone=true 2>/dev/null || true
  cd awesome-claude-skills 2>/dev/null || cd karanb192-awesome-claude-skills

  git checkout -b add-satori 2>/dev/null || git checkout add-satori

  echo ""
  echo ">>> MANUAL STEP: Edit README.md"
  echo ">>> Match their exact format (may include star ratings, verification, etc.)"
  echo ""
  read -p "Press Enter after editing README.md..."

  git add README.md
  git commit -m "Add Satori - clinically informed wisdom companion"
  git push -u origin add-satori
  gh pr create \
    --title "Add Satori - wisdom companion Claude skill" \
    --body "$PR_BODY_STANDARD"

  echo "✓ karanb192 PR created"
  cd "$WORK_DIR"
}

# ──────────────────────────────────────────────
# 4. VoltAgent/awesome-agent-skills
# ──────────────────────────────────────────────
submit_voltagent() {
  echo "=== Submitting to VoltAgent/awesome-agent-skills ==="
  cd "$WORK_DIR"
  gh repo fork VoltAgent/awesome-agent-skills --clone=true 2>/dev/null || true
  cd awesome-agent-skills 2>/dev/null || cd VoltAgent-awesome-agent-skills

  git checkout -b add-satori 2>/dev/null || git checkout add-satori

  echo ""
  echo ">>> MANUAL STEP: Edit README.md"
  echo ">>> Add under Community Skills > Other (or best-fit subcategory):"
  echo '- **[MetcalfSolutions/Satori](https://github.com/MetcalfSolutions/Satori)** - Wisdom companion blending psychology and philosophy traditions'
  echo ""
  read -p "Press Enter after editing README.md..."

  git add README.md
  git commit -m "Add skill: MetcalfSolutions/Satori"
  git push -u origin add-satori
  gh pr create \
    --title "Add skill: MetcalfSolutions/Satori" \
    --body "$PR_BODY_STANDARD"

  echo "✓ VoltAgent PR created"
  cd "$WORK_DIR"
}

# ──────────────────────────────────────────────
# 5. sickn33/antigravity-awesome-skills
# ──────────────────────────────────────────────
submit_antigravity() {
  echo "=== Submitting to sickn33/antigravity-awesome-skills ==="
  cd "$WORK_DIR"
  gh repo fork sickn33/antigravity-awesome-skills --clone=true 2>/dev/null || true
  cd antigravity-awesome-skills 2>/dev/null || cd sickn33-antigravity-awesome-skills

  git checkout -b add-satori 2>/dev/null || git checkout add-satori

  mkdir -p skills/satori

  cat > skills/satori/SKILL.md <<'SKILLEOF'
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
SKILLEOF

  # Run validation if available
  if [ -f package.json ]; then
    npm install
    npm run validate || echo "WARNING: Validation failed — review output above"
  fi

  git add skills/satori/SKILL.md
  git commit -m "feat: add satori skill"
  git push -u origin add-satori
  gh pr create \
    --title "feat: add satori wisdom companion skill" \
    --body "Adding Satori, a clinically informed wisdom companion.

GitHub: https://github.com/MetcalfSolutions/Satori
License: Apache 2.0
Risk: safe
Category: personal-development"

  echo "✓ antigravity PR created"
  cd "$WORK_DIR"
}

# ──────────────────────────────────────────────
# 6. ComposioHQ/awesome-claude-skills
# ──────────────────────────────────────────────
submit_composiohq() {
  echo "=== Submitting to ComposioHQ/awesome-claude-skills ==="
  echo "WARNING: This repo may only list official Anthropic skills."
  echo "Check the README first — if all entries link to anthropics/skills/, skip this."
  read -p "Continue? (y/n) " -n 1 -r
  echo ""
  [[ ! $REPLY =~ ^[Yy]$ ]] && { echo "Skipped."; return; }

  cd "$WORK_DIR"
  gh repo fork ComposioHQ/awesome-claude-skills --clone=true 2>/dev/null || true
  cd awesome-claude-skills 2>/dev/null || cd ComposioHQ-awesome-claude-skills

  git checkout -b add-satori 2>/dev/null || git checkout add-satori

  echo ""
  echo ">>> MANUAL STEP: Edit README.md"
  echo ">>> Add under Productivity & Organization (alphabetically):"
  echo '- [satori](https://github.com/MetcalfSolutions/Satori) - Clinically informed wisdom companion blending psychology and philosophy into a structured thinking partner.'
  echo ""
  read -p "Press Enter after editing README.md..."

  git add README.md
  git commit -m "Add Satori - clinically informed wisdom companion"
  git push -u origin add-satori
  gh pr create \
    --title "Add Satori - clinically informed wisdom companion skill" \
    --body "$PR_BODY_STANDARD"

  echo "✓ ComposioHQ PR created"
  cd "$WORK_DIR"
}

# ──────────────────────────────────────────────
# 7. travisvn/awesome-claude-skills
# ──────────────────────────────────────────────
submit_travisvn() {
  echo "=== Submitting to travisvn/awesome-claude-skills ==="
  echo "REQUIREMENTS: 10+ GitHub stars, PR must NOT be AI-generated"
  echo "Write/edit this PR by hand for compliance."
  read -p "Continue? (y/n) " -n 1 -r
  echo ""
  [[ ! $REPLY =~ ^[Yy]$ ]] && { echo "Skipped."; return; }

  cd "$WORK_DIR"
  gh repo fork travisvn/awesome-claude-skills --clone=true 2>/dev/null || true
  cd awesome-claude-skills 2>/dev/null || cd travisvn-awesome-claude-skills

  git checkout -b add-satori 2>/dev/null || git checkout add-satori

  echo ""
  echo ">>> MANUAL STEP: Edit README.md"
  echo ">>> Find the Individual Skills table under Community Skills and add:"
  echo '| **[Satori](https://github.com/MetcalfSolutions/Satori)** | Clinically informed wisdom companion blending IFS, DBT, Stoicism, Buddhism, and six other traditions into a structured thinking partner |'
  echo ""
  read -p "Press Enter after editing README.md..."

  git add README.md
  git commit -m "Add Satori - wisdom companion Claude skill"
  git push -u origin add-satori
  gh pr create \
    --title "Add Satori - wisdom companion Claude skill" \
    --body "$PR_BODY_STANDARD"

  echo "✓ travisvn PR created"
  cd "$WORK_DIR"
}

# ──────────────────────────────────────────────
# 8. e2b-dev/awesome-ai-agents (Tier 3)
# ──────────────────────────────────────────────
submit_e2b() {
  echo "=== Submitting to e2b-dev/awesome-ai-agents ==="
  cd "$WORK_DIR"
  gh repo fork e2b-dev/awesome-ai-agents --clone=true 2>/dev/null || true
  cd awesome-ai-agents 2>/dev/null || cd e2b-dev-awesome-ai-agents

  git checkout -b add-satori 2>/dev/null || git checkout add-satori

  echo ""
  echo ">>> MANUAL STEP: Edit README.md"
  echo ">>> Find the open-source section and add the detailed entry."
  echo ">>> See SUBMISSION-GUIDE.md #8 for the exact format."
  echo ""
  read -p "Press Enter after editing README.md..."

  git add README.md
  git commit -m "Add Satori - clinically informed wisdom companion agent"
  git push -u origin add-satori
  gh pr create \
    --title "Add Satori - wisdom companion cognitive agent" \
    --body "Adding Satori, a clinically informed AI wisdom companion that operates as a cognitive agent with 211k+ characters of structured reference architecture.

GitHub: https://github.com/MetcalfSolutions/Satori
License: Apache 2.0"

  echo "✓ e2b-dev PR created"
  cd "$WORK_DIR"
}

# ──────────────────────────────────────────────
# 9. kyrolabs/awesome-agents (Tier 3)
# ──────────────────────────────────────────────
submit_kyrolabs() {
  echo "=== Submitting to kyrolabs/awesome-agents ==="
  cd "$WORK_DIR"
  gh repo fork kyrolabs/awesome-agents --clone=true 2>/dev/null || true
  cd awesome-agents 2>/dev/null || cd kyrolabs-awesome-agents

  git checkout -b add-satori 2>/dev/null || git checkout add-satori

  echo ""
  echo ">>> MANUAL STEP: Edit README.md"
  echo ">>> Find the Conversational/General Agents section and add:"
  echo '- [Satori](https://github.com/MetcalfSolutions/Satori) - Clinically informed wisdom companion blending IFS, DBT, Stoicism, Buddhism, and six other traditions into a structured thinking partner for Claude. ![GitHub stars](https://img.shields.io/github/stars/MetcalfSolutions/Satori?style=social)'
  echo ""
  read -p "Press Enter after editing README.md..."

  git add README.md
  git commit -m "Add Satori - clinically informed wisdom companion"
  git push -u origin add-satori
  gh pr create \
    --title "Add Satori - wisdom companion agent" \
    --body "Adding Satori, a clinically informed AI wisdom companion.

GitHub: https://github.com/MetcalfSolutions/Satori
License: Apache 2.0"

  echo "✓ kyrolabs PR created"
  cd "$WORK_DIR"
}

# ──────────────────────────────────────────────
# Run submissions
# Uncomment the ones you want to run:
# ──────────────────────────────────────────────

echo ""
echo "Available submission functions:"
echo "  submit_behisecc      # BehiSecc/awesome-claude-skills (8.2k stars)"
echo "  submit_majiayu000    # majiayu000/claude-skill-registry (JSON)"
echo "  submit_karanb192     # karanb192/awesome-claude-skills"
echo "  submit_voltagent     # VoltAgent/awesome-agent-skills"
echo "  submit_antigravity   # sickn33/antigravity-awesome-skills"
echo "  submit_composiohq    # ComposioHQ/awesome-claude-skills (32.5k stars)"
echo "  submit_travisvn      # travisvn/awesome-claude-skills (requires 10+ stars)"
echo "  submit_e2b           # e2b-dev/awesome-ai-agents (Tier 3)"
echo "  submit_kyrolabs      # kyrolabs/awesome-agents (Tier 3)"
echo ""
echo "Source each function or uncomment below to run:"

# submit_behisecc
# submit_majiayu000
# submit_karanb192
# submit_voltagent
# submit_antigravity
# submit_composiohq
# submit_travisvn
# submit_e2b
# submit_kyrolabs
