# Testing Workflow

A step-by-step guide to testing plugins locally during development.

## Overview

Testing plugins locally uses a **dev marketplace** that points to your working plugin directory. This allows you to:
- Test changes without publishing
- Iterate quickly
- Validate before distribution

## Setup: One-Time

### 1. Create Dev Marketplace Structure

```bash
# From your project root
mkdir -p dev-marketplace/.claude-plugin
```

### 2. Create marketplace.json

Create `dev-marketplace/.claude-plugin/marketplace.json`:

```json
{
  "name": "dev-marketplace",
  "owner": {
    "name": "Developer"
  },
  "metadata": {
    "description": "Local development marketplace",
    "version": "0.1.0"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "description": "Plugin under development",
      "source": "../plugins/my-plugin"
    }
  ]
}
```

**Key**: `source` points to your plugin directory (relative path from marketplace).

### 3. Add Marketplace to Claude Code

```bash
claude
/plugin marketplace add ./dev-marketplace
```

Verify:
```bash
/plugin marketplace list
```

You should see `dev-marketplace` listed.

## Iteration Loop

### Install Plugin

```bash
/plugin install my-plugin@dev-marketplace
```

### Test Commands

```bash
/my-plugin:command-name args
```

Or test via `/help` to see if commands appear.

### Make Changes

Edit your plugin files (commands, skills, etc.).

### Reinstall

```bash
/plugin uninstall my-plugin@dev-marketplace
/plugin install my-plugin@dev-marketplace
```

**Note**: You must uninstall/reinstall to pick up changes.

### Repeat

Continue the edit → reinstall → test cycle.

## Validation

Before each test cycle, validate your plugin:

```bash
/plugin-development:validate
```

This checks:
- `plugin.json` exists and is valid JSON
- Component directories exist
- Paths are correct
- No common mistakes

## Debugging

### Plugin Not Loading

1. Check `plugin.json` exists at `.claude-plugin/plugin.json`
2. Verify JSON syntax: `cat .claude-plugin/plugin.json | jq .`
3. Check paths are relative: `./commands/` not `/absolute/path/`

### Commands Not Showing

1. Verify `commands` field in `plugin.json` points to `./commands/`
2. Check command files have `.md` extension
3. Verify frontmatter has `description` field
4. Reinstall the plugin

### Hooks Not Running

1. Check `hooks` field in `plugin.json` points to correct path
2. Verify `hooks.json` is valid JSON
3. Make scripts executable: `chmod +x scripts/*.sh`
4. Test script directly: `./scripts/validate-plugin.sh`
5. Use `claude --debug` to see hook execution

### Skills Not Triggering

1. Check `skills` field in `plugin.json` (if specified)
2. Verify `SKILL.md` has frontmatter with `name` and `description`
3. Ensure `name` matches directory name (lowercase, hyphenated)
4. Check `description` includes clear trigger conditions

## Advanced: Debug Mode

Run Claude Code in debug mode to see detailed plugin loading:

```bash
claude --debug
```

This shows:
- Plugin registration
- Component discovery
- Hook execution
- Tool usage

Look for errors related to your plugin in the output.

## Multiple Plugins

You can test multiple plugins from one dev marketplace:

```json
{
  "plugins": [
    {
      "name": "plugin-one",
      "source": "../plugins/plugin-one"
    },
    {
      "name": "plugin-two",
      "source": "../plugins/plugin-two"
    }
  ]
}
```

Install each separately:
```bash
/plugin install plugin-one@dev-marketplace
/plugin install plugin-two@dev-marketplace
```

## Clean Up

### Uninstall Plugin

```bash
/plugin uninstall my-plugin@dev-marketplace
```

### Remove Marketplace

```bash
/plugin marketplace remove dev-marketplace
```

## Best Practices

1. **Validate first**: Always run `/plugin-development:validate` before testing
2. **Small changes**: Test incrementally, don't make many changes at once
3. **Check logs**: Use `--debug` when troubleshooting
4. **Script testing**: Test hook scripts directly before adding to hooks.json
5. **Clean installs**: Uninstall fully before reinstalling to avoid cache issues

## Troubleshooting Checklist

```
□ plugin.json exists and is valid JSON
□ All paths are relative (start with ./)
□ Component directories exist (commands/, etc.)
□ Command files have .md extension
□ Scripts are executable (chmod +x)
□ marketplace.json plugin name matches plugin.json name
□ Reinstalled after making changes
```

## Example Session

```bash
# One-time setup
mkdir -p dev-marketplace/.claude-plugin
# ... create marketplace.json ...
/plugin marketplace add ./dev-marketplace

# Development loop
/plugin install my-plugin@dev-marketplace
/my-plugin:test-command

# Make changes to plugin files...

/plugin-development:validate
/plugin uninstall my-plugin@dev-marketplace
/plugin install my-plugin@dev-marketplace
/my-plugin:test-command

# Repeat...
```
