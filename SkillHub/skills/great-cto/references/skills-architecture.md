---
name: skills-architecture
description: 4-tier skills system (built-in / external deps / personal / on-demand) and how agents discover + load them via skills-registry.json
when_to_use: Understanding how skills work. Read by /doctor + agents for open-world discovery
applies_to:
  - _default
---

# Skills architecture (v1.0.139+)

> How great_cto discovers, loads, and refreshes skills across 4 tiers — from built-in packs to your personal library to on-demand template fetch.

## Why 4 tiers

Skills come from different places with different update cadences and trust levels. Conflating them produces a registry that's either bloated (everything-eligible) or stale (only-canonical). Four tiers handle that explicitly:

| Tier | Source | Update cadence | Trust |
|---|---|---|---|
| **1** | great_cto built-in (`packs/`, `templates/`, `references/`) | per plugin release | maintained by plugin author |
| **2** | declared external dependencies (superpowers, anthropics/skills, beads) | 7d cache, auto-pull | upstream-maintained |
| **3** | personal repo (default `avelikiy/ai-agent-skills`, override via `GREAT_CTO_PERSONAL_SKILLS` env) | 24h cache, auto-pull | you-maintained |
| **4** | on-demand fetch (Template Bridge `/template`) + MCP servers | per-invocation | varies |

## Discovery flow (per session)

```
SessionStart hook
  ↓
1. Plugin install / version check  (existing — check-update.sh)
2. Catalog clone (davila7/templates) — already there
3. Anthropic skills clone/pull     (NEW v1.0.139, 7d cache)
4. Personal skills clone/pull      (NEW v1.0.139, 1d cache)
5. skill-discover.sh               (NEW v1.0.139, 24h cache)
   → writes ~/.great_cto/skills-registry.json
6. bd prime (existing)
7. Status output (existing)
```

All git operations run in background (`&`) so they don't block session start. First session may hit cold-cache delay (~10–30 s depending on bandwidth); subsequent sessions are instant.

## Registry schema (`~/.great_cto/skills-registry.json`)

```json
{
  "discovered_at": "2026-04-28T05:38:52Z",
  "plugin_version": "1.0.139",

  "tier1_great_cto": [
    {"name": "agent-pack", "source": "great_cto:packs", "path": "...", "summary": "..."},
    {"name": "ARCH-ai", "source": "great_cto:templates", "path": "...", "summary": "..."}
  ],

  "tier2_external": [
    {"name": "superpowers:test-driven-development", "source": "obra/superpowers", "path": "...", "summary": "..."},
    {"name": "anthropic:rag-patterns", "source": "anthropics/skills", "path": "...", "summary": "..."}
  ],

  "tier3_personal": [
    {"name": "personal:rag-cascading-search", "source": "personal/ai-agent-skills", "path": "...", "summary": "..."}
  ],

  "archetype_packs": {
    "ai-system": ["agent-pack", "ai-pack", "ARCH-ai", "THREAT-MODEL-AI", ...],
    "commerce": ["commerce-pack", "PCI-DSS-SAQ-A", ...],
    ...
  }
}
```

## How agents use the registry

Agents at Step 0a (or as part of pattern-lookup) consult the registry:

```bash
ARCHETYPE=$(grep "^archetype:" .great_cto/PROJECT.md | awk '{print $2}')
REGISTRY="$HOME/.great_cto/skills-registry.json"

if [ -f "$REGISTRY" ]; then
  # 1. Load archetype-specific packs (tier 1)
  PACKS=$(python3 -c "
import json, sys
d = json.load(open('$REGISTRY'))
for p in d.get('archetype_packs', {}).get('$ARCHETYPE', []):
    print(p)
")
  for pack in $PACKS; do
    PATH=$(python3 -c "
import json
d = json.load(open('$REGISTRY'))
for tier in ['tier1_great_cto', 'tier2_external', 'tier3_personal']:
    for s in d.get(tier, []):
        if s['name'] == '$pack' or s['name'].endswith(':$pack'):
            print(s['path']); break
")
    [ -n "$PATH" ] && echo "  Loading: $pack from $PATH"
    # The agent then `Read`s the path
  done

  # 2. Optional: search for additional skills matching task keywords
  # (future v1.0.140+ — semantic match between feature description and skill summaries)
fi
```

## Adding a new skill

### To Tier 1 (great_cto built-in)

PR against `skills/great_cto/packs/*.md` or `templates/*.md`. Ships in next plugin release.

### To Tier 2 (anthropics/skills)

External — file PR against https://github.com/anthropics/skills.

### To Tier 3 (personal)

```bash
cd ~/.great_cto/personal-skills        # or wherever your personal repo is cloned
mkdir skills/<my-new-skill>
$EDITOR skills/<my-new-skill>/SKILL.md  # write per superpowers:writing-skills format
git add . && git commit -m "add <my-new-skill>" && git push
# Next /doctor --skills-refresh picks it up; or wait 24h for auto-refresh
```

### To Tier 4 (on-demand)

No persistent install. Use `/template fetch <name>` (Template Bridge) or invoke an MCP server tool — picked up at runtime.

## SKILL.md format (canonical)

```yaml
---
name: <slug>
description: One-sentence what this skill does
when_to_use: When LLM should invoke / consult this skill
applies_to:                    # optional — limits skill to specific archetypes
  - ai-system
  - agent-product
sources:                       # optional — links to upstream patterns
  - https://...
---

## Pattern
<the actual pattern in plain text + code>

## Why
<reasoning + alternatives considered>

## How
<step-by-step>

## Anti-patterns
<what NOT to do>
```

`description` must be the first thing the LLM scans — it decides whether to consult full SKILL.md based on this line. Keep it concrete and specific.

## Manual control

| Command | Effect |
|---|---|
| `/doctor --skills` | Show registry summary + archetype-relevant skills |
| `/doctor --skills-refresh` | Force re-scan all 4 tiers immediately |
| `bash scripts/skill-discover.sh` | Same as above (direct invocation) |
| `cat ~/.great_cto/skills-registry.json` | Raw view |
| `GREAT_CTO_PERSONAL_SKILLS=/path/to/repo` | Override personal-skills location (env var) |

## What's NOT here

- **Marketplace integration** — Anthropic's Plugin Marketplace not yet open. When it does, expect Tier 2 to gain `marketplace:` source, registry schema may grow a `marketplace_skills` array.
- **Semantic skill search** — current registry is name-keyed only. Future: embed `description` field, allow LLM agents to search "find a skill for X" instead of knowing the name.
- **Skill versioning** — current registry shows whatever's in tip-of-main on cloned repos. No pinning. Acceptable for personal + canonical sources; revisit if community-skills churn becomes painful.
- **Skill conflict resolution** — if two tiers define `rag-pattern`, both appear in registry with `tier1:rag-pattern` vs `personal:rag-pattern` namespace. Agent picks by priority (built-in > external > personal in current default; future: preference config).

## Why these design choices

| Decision | Why |
|---|---|
| 4 tiers, not 1 flat list | Different update cadences, different trust levels |
| Git clones (not API fetch) | Offline-capable; no API rate limits; works behind firewalls |
| 24h cache on registry | Cheap re-scan; rebuilds in <1s; faster than disk-walk every session |
| 7d cache on Anthropic skills | Upstream changes are slow; weekly pull is enough |
| 1d cache on personal | You commit changes daily; pull frequency matches |
| Background `&` for clones | First session not blocked by cold-cache pulls |
| `~/.great_cto/` not `~/.claude/` | Plugin-namespaced, doesn't interfere with Claude Code's own skills dir |
