# Naming Conventions

Consistent naming patterns for Claude Code plugins and components.

## General Principles

1. **Predictable**: Names should indicate purpose
2. **Consistent**: Follow patterns throughout plugin
3. **Case-sensitive**: Respect case conventions for each component type
4. **Descriptive**: Prefer clarity over brevity
5. **Avoid conflicts**: Namespace to prevent collisions

## Plugin Names

### Format

**kebab-case** (lowercase with hyphens)

### Examples

✅ **Good**:
- `plugin-development`
- `code-review-tools`
- `git-workflow`
- `python-helpers`

❌ **Bad**:
- `PluginDevelopment` (camelCase)
- `plugin_development` (snake_case)
- `plugindevelopment` (no separators)
- `PLUGIN-DEVELOPMENT` (uppercase)

### Naming Tips

- **Descriptive**: Name reflects functionality
- **Concise**: 1-3 words typical
- **No prefix**: Don't use "plugin-" prefix (redundant)
  - ✅ `code-review`
  - ❌ `plugin-code-review`

## Command Names

### Format

**kebab-case** (lowercase with hyphens)

Files: `command-name.md`

### Examples

✅ **Good**:
- `init.md` → `/plugin-name:init`
- `add-command.md` → `/plugin-name:add-command`
- `validate-all.md` → `/plugin-name:validate-all`
- `run-tests.md` → `/plugin-name:run-tests`

❌ **Bad**:
- `Init.md` (capitalized)
- `add_command.md` (snake_case)
- `addCommand.md` (camelCase)

### Command Invocation

Commands can be invoked with or without the plugin prefix:

**Full format**: `/plugin-name:command-name`

**Examples**:
- `/plugin-development:init`
- `/git-workflow:commit-push`
- `/test-runner:run-all`

### Namespacing

**Plugin prefix is optional** unless there are name conflicts. When no conflict exists, you can use the command directly:

- Direct: `/format-code` (when no conflict)
- Prefixed: `/my-tools:format-code` (when needed for disambiguation)

Commands are automatically namespaced by plugin name:
- Plugin: `my-tools`
- Command file: `format.md`
- Invocation options:
  - `/format` (if no other plugin has this command)
  - `/my-tools:format` (when needed to disambiguate)

This prevents conflicts between plugins.

### Verb-Based Naming

Start commands with action verbs:

✅ **Good**:
- `create-component`
- `validate-config`
- `run-tests`
- `deploy-app`

❌ **Bad**:
- `component-creation` (noun-based)
- `config-validation` (noun-based)

## Skill Names

### Format

**kebab-case** (lowercase with hyphens)

Directory: `skill-name/`
File: `SKILL.md` (always uppercase)

### Examples

✅ **Good**:
- `plugin-authoring/SKILL.md`
- `code-review/SKILL.md`
- `api-design/SKILL.md`

❌ **Bad**:
- `PluginAuthoring/SKILL.md` (camelCase)
- `plugin_authoring/SKILL.md` (snake_case)
- `plugin-authoring/skill.md` (lowercase skill.md)

### Frontmatter Name

Should match directory name (recommended for consistency):

```markdown
---
name: plugin-authoring    # Matches directory
description: ...
---
```

❌ **Poor practice**:
```
Directory: plugin-authoring/
Frontmatter: name: PluginAuthoring  # Doesn't match! Use kebab-case
```

**Note**: While the `name` field in frontmatter is what Claude uses to discover and reference Skills, having it match the directory name prevents confusion and follows best practices.

### Skill Naming Tips

- **Domain-focused**: Name reflects area of expertise
- **Singular**: `code-review` not `code-reviews`
- **Avoid "skill" suffix**: Name is the capability
  - ✅ `plugin-authoring`
  - ❌ `plugin-authoring-skill`

## Agent Names

### Format

**kebab-case** (lowercase with hyphens)

Files: `agent-name.md`

### Examples

✅ **Good**:
- `code-reviewer.md`
- `test-analyzer.md`
- `security-auditor.md`
- `plugin-reviewer.md`

❌ **Bad**:
- `CodeReviewer.md` (camelCase)
- `code_reviewer.md` (snake_case)

### Agent Naming Tips

- **Role-based**: Name indicates what agent does
- **Often noun**: Describes the agent's role
  - `reviewer`, `analyzer`, `auditor`
- **Suffix optional**: `-er`, `-or` common but not required
  - ✅ `code-reviewer`
  - ✅ `security-audit`

## Hook Script Names

### Format

**kebab-case** (lowercase with hyphens)

Extension: `.sh` for bash scripts

### Examples

✅ **Good**:
- `validate-plugin.sh`
- `format-code.sh`
- `pre-write-check.sh`
- `session-start-info.sh`

❌ **Bad**:
- `validatePlugin.sh` (camelCase)
- `validate_plugin.sh` (snake_case)
- `VALIDATE-PLUGIN.sh` (uppercase)

### Hook Naming Tips

- **Purpose-based**: Name indicates what hook does
- **Event optional**: Can include event in name
  - `pre-write-validate.sh`
  - `post-write-format.sh`

## Marketplace Names

### Format

**kebab-case** (lowercase with hyphens)

### Examples

✅ **Good**:
- `team-tools`
- `acme-plugins`
- `dev-marketplace`
- `internal-tools`

❌ **Bad**:
- `TeamTools` (camelCase)
- `team_tools` (snake_case)

## Variable and Argument Names

### In Commands

Use uppercase with underscores for built-in variables:
- `$ARGUMENTS`: All arguments as string
- `$1`, `$2`, etc.: Individual arguments

### In Documentation

Use lowercase with hyphens in examples:
```markdown
argument-hint: [plugin-name] [command-type]
```

## File Extensions

### Markdown

- Commands: `.md`
- Agents: `.md`
- Skills: `SKILL.md` (specific name)
- Documentation: `.md`

### Configuration

- Plugin manifest: `plugin.json`
- Marketplace manifest: `marketplace.json`
- Hooks config: `hooks.json`

### Scripts

- Bash: `.sh`
- Python: `.py`
- Node: `.js`

## Directory Names

### Standard Directories

Use these exact names:
- `commands/` (not `command/` or `cmd/`)
- `agents/` (not `agent/` or `subagents/`)
- `skills/` (not `skill/`)
- `hooks/` (not `hook/`)
- `scripts/` (not `script/` or `bin/`)

### Custom Directories

For additional organization, use kebab-case:
- `templates/`
- `schemas/`
- `examples/`
- `best-practices/`
- `test-fixtures/`

## Metadata Fields

### In plugin.json

```json
{
  "name": "kebab-case",
  "description": "Sentence case with capital first letter",
  "keywords": ["lowercase", "multi-word-hyphenated"],
  "license": "UPPERCASE (e.g., MIT, Apache-2.0)"
}
```

### Author Names

Use natural capitalization:
```json
{
  "author": {
    "name": "John Smith",
    "email": "john@example.com"
  }
}
```

## Category and Tag Conventions

### Categories

Use singular, lowercase:
- `development`
- `productivity`
- `utilities`
- `devops`

### Tags

Use lowercase, hyphenated for multi-word:
- `code-review`
- `testing`
- `deployment`
- `git-workflow`

## Consistency Checklist

```
□ Plugin name: kebab-case
□ Commands: kebab-case, .md extension
□ Skills: kebab-case directory, SKILL.md file
□ Agents: kebab-case, .md extension
□ Scripts: kebab-case, appropriate extension
□ Directories: standard names (commands/, agents/, etc.)
□ Frontmatter names match directory/file names
□ Categories and tags: lowercase
```

## Examples by Component

### Complete Plugin

```
my-dev-tools/                    # kebab-case
├── .claude-plugin/
│   └── plugin.json              # name: "my-dev-tools"
├── commands/
│   ├── format-code.md           # kebab-case
│   ├── run-tests.md             # kebab-case
│   └── validate-all.md          # kebab-case
├── agents/
│   └── code-reviewer.md         # kebab-case
├── skills/
│   └── code-quality/            # kebab-case
│       └── SKILL.md             # UPPERCASE
├── hooks/
│   └── hooks.json
└── scripts/
    ├── pre-write-check.sh       # kebab-case
    └── post-write-format.sh     # kebab-case
```

### Invocations

```bash
/my-dev-tools:format-code
/my-dev-tools:run-tests
/my-dev-tools:validate-all
```

## Anti-Patterns

### ❌ Mixed Case

```
MyDevTools/
├── commands/
│   ├── FormatCode.md      # Wrong!
│   └── runTests.md        # Wrong!
```

### ❌ Inconsistent Separators

```
my_dev_tools/              # snake_case
├── commands/
│   ├── format-code.md     # kebab-case
│   └── runTests.md        # camelCase
```

### ❌ Wrong SKILL.md Case

```
skills/
└── my-skill/
    └── skill.md           # Should be SKILL.md
```

## When in Doubt

Follow these defaults:
- **Files/directories**: kebab-case
- **SKILL.md**: Always uppercase
- **JSON fields**: Follow schema (usually camelCase for author fields, kebab-case for names)
- **Invocation**: `/plugin-name:command-name` (always kebab-case)
