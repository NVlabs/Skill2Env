# Common Plugin Mistakes

Avoid these patterns that cause silent failures.

## Directory Structure

### Components Inside .claude-plugin/

```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json
│   ├── commands/      # WRONG!
│   └── agents/        # WRONG!
```

**Why it fails**: Claude Code only looks for `plugin.json` inside `.claude-plugin/`. Components are discovered at plugin root, not inside the manifest directory.

**Fix**:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json    # Only this file here
├── commands/          # At root
├── agents/            # At root
└── skills/            # At root
```

---

## plugin.json Configuration

### Specifying Standard Paths

```json
{
  "name": "my-plugin",
  "commands": "./commands/",
  "agents": "./agents/"
}
```

**Why it fails**: When you specify component paths, you're telling Claude Code to use ONLY those paths. Standard directories (`commands/`, `agents/`, `skills/`, `hooks/`) are auto-discovered—explicitly specifying them can interfere with discovery.

**Fix**:
```json
{
  "name": "my-plugin"
}
```

Only add component fields for **non-standard** locations like `./custom-commands/`.

### Absolute Paths

```json
{
  "commands": "/Users/you/plugins/my-plugin/commands/"
}
```

**Why it fails**: Absolute paths break when plugin is installed on another machine or in a different location.

**Fix**: Always use relative paths starting with `./`:
```json
{
  "commands": ["./custom/cmd.md"]
}
```

---

## Hook Scripts

### Relative Paths in Hook Commands

```json
{
  "command": "./scripts/format.sh"
}
```

**Why it fails**: Relative paths resolve from where Claude Code runs (the project directory), not from the plugin location. Works during development in the plugin directory, breaks completely when plugin is installed elsewhere.

**Fix**: Always use `${CLAUDE_PLUGIN_ROOT}`:
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
}
```

### Non-Executable Scripts

```bash
# Created script but forgot: chmod +x scripts/format.sh
```

**Why it fails**: Hook silently fails with no error message. You'll spend hours debugging why the hook "isn't running."

**Fix**: Always make scripts executable:
```bash
chmod +x scripts/*.sh
```

### Missing Timeout on Slow Operations

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh"
  // No timeout specified
}
```

**Why it fails**: Default timeout is 60 seconds. If your script takes longer, it's killed silently.

**Fix**: Set appropriate timeout:
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh",
  "timeout": 120
}
```

### Wrong Matcher Syntax

```json
{
  "PreToolUse": [
    {
      "matcher": "write",  // Wrong case!
      "hooks": [...]
    }
  ]
}
```

**Why it fails**: Matchers are case-sensitive. `"write"` won't match the `Write` tool.

**Fix**: Use exact tool names:
```json
{
  "matcher": "Write|Edit"
}
```

---

## Skill Configuration

### Name Doesn't Match Directory

```
skills/my-skill/SKILL.md
---
name: MySkill   # Doesn't match directory!
---
```

**Why it fails**: Discovery uses directory name. Mismatched names cause confusion and potential discovery issues.

**Fix**: Name must match directory in kebab-case:
```
skills/my-skill/SKILL.md
---
name: my-skill  # Matches directory
---
```

### Reserved Words in Skill Name

```yaml
name: claude-helper      # Contains 'claude'!
name: anthropic-tools    # Contains 'anthropic'!
```

**Why it fails**: Names containing 'claude' or 'anthropic' are reserved and will be rejected.

**Fix**: Use different naming:
```yaml
name: assistant-helper
name: ai-tools
```

### Description Missing "When to Use"

```yaml
description: Helps with code review
```

**Why it fails**: Claude uses descriptions to decide when to activate skills. Without trigger conditions, skill may not activate when needed.

**Fix**: Include both what AND when:
```yaml
description: Provides code review guidance. Use when reviewing PRs, examining code quality, or preparing code for review.
```

### Skill Over 500 Lines

```markdown
# SKILL.md (2000 lines of content)
Everything inline...
```

**Why it fails**: Large skills consume excessive context tokens and may not be fully processed.

**Fix**: Use progressive disclosure:
```markdown
# SKILL.md (~300 lines)
## Quick Links
- [Detailed API Reference](./reference.md)
- [Examples](./examples.md)
```

---

## Marketplace Configuration

### Plugin Name Mismatch

```json
// marketplace.json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/other-name"  // Directory doesn't match!
    }
  ]
}

// plugins/other-name/.claude-plugin/plugin.json
{
  "name": "other-name"  // Doesn't match marketplace entry!
}
```

**Why it fails**: The `name` in marketplace.json must match the `name` in the plugin's plugin.json.

**Fix**: Ensure names match:
```json
// Both must use "my-plugin"
```

### Absolute Source Paths

```json
{
  "source": "/Users/you/dev/plugins/my-plugin"
}
```

**Why it fails**: Breaks for anyone else using the marketplace.

**Fix**: Use relative paths:
```json
{
  "source": "./plugins/my-plugin"
}
```

---

## Validation Skipping

### Testing Without Validation

```bash
# Skip validation, jump straight to testing
/plugin install my-plugin@dev-marketplace
# Wonder why nothing works...
```

**Why it fails**: Many issues are silent. Plugin loads but components don't work. Hours wasted debugging.

**Fix**: ALWAYS validate first:
```bash
/plugin-development:validate
# Fix any issues BEFORE testing
/plugin install my-plugin@dev-marketplace
```

---

## Prevention Checklist

Before testing any plugin:

```
□ Components at plugin root (not inside .claude-plugin/)
□ No component fields in plugin.json for standard directories
□ Hooks use ${CLAUDE_PLUGIN_ROOT} for all paths
□ Scripts are executable (chmod +x)
□ Skill names match directory names (kebab-case)
□ Skill names don't contain 'claude' or 'anthropic'
□ Skill descriptions include when to use
□ Marketplace plugin names match plugin.json names
□ All paths are relative (start with ./)
□ /plugin-development:validate passes
```

## Quick Diagnostic

| Symptom | Likely Cause | Check |
|---------|--------------|-------|
| Plugin doesn't load | plugin.json location or syntax | `.claude-plugin/plugin.json` exists? Valid JSON? |
| Commands don't appear | Wrong directory or missing frontmatter | `commands/*.md` at root? Has `description` frontmatter? |
| Hooks don't run | Path or permission issue | Using `${CLAUDE_PLUGIN_ROOT}`? Scripts executable? |
| Skill doesn't trigger | Description missing triggers | Includes "when to use"? |
| Marketplace install fails | Name mismatch | Names identical in marketplace.json and plugin.json? |
