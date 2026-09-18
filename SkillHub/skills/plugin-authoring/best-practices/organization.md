# Plugin Organization Best Practices

Guidelines for structuring well-organized, maintainable Claude Code plugins.

## Directory Structure

### Standard Layout

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json           # Manifest only
├── commands/                 # Slash commands (*.md)
├── agents/                   # Sub-agents (*.md)
├── skills/                   # Skills (folders with SKILL.md)
├── hooks/                    # Hook configurations
│   └── hooks.json            # Main hook config file
├── scripts/                  # Hook scripts, utilities
└── README.md                 # User-facing documentation
```

### Key Principles

1. **Manifest isolation**: Only `plugin.json` goes in `.claude-plugin/`
2. **Component separation**: Keep commands, agents, skills, and hooks in separate directories
3. **Relative paths**: All paths in manifests are relative to plugin root
4. **Default directories**: Standard directories (`commands/`, `agents/`, `skills/`, `hooks/`) are automatically discovered
5. **Flat commands**: Command files go directly in `commands/`, not subdirectories (unless using custom paths)
6. **Nested skills**: Skills are folders with `SKILL.md` + support files
7. **Custom paths**: Use component fields in `plugin.json` only for non-standard locations

## File Naming

### Commands

- **Format**: `command-name.md`
- **Case**: kebab-case (lowercase with hyphens)
- **Examples**: `init.md`, `add-command.md`, `validate.md`

### Agents

- **Format**: `agent-name.md`
- **Case**: kebab-case
- **Examples**: `code-reviewer.md`, `test-analyzer.md`

### Skills

- **Format**: `skill-name/SKILL.md` (directory + SKILL.md)
- **Case**: kebab-case for directory
- **Examples**: `plugin-authoring/SKILL.md`, `code-review/SKILL.md`

### Hooks

- **Standard**: `hooks.json` (one per plugin)
- **Scripts**: `scripts/script-name.sh` (kebab-case)

## Skill Organization

### Progressive Disclosure Pattern

Keep `SKILL.md` concise (< 500 lines) and link to detailed files:

```
skills/my-skill/
├── SKILL.md              # Main skill definition (concise)
├── schemas/              # Data format documentation
│   └── config-schema.md
├── templates/            # Reusable templates
│   └── config-template.json
├── examples/             # Usage examples
│   └── basic-usage.md
└── best-practices/       # Detailed guidance
    └── patterns.md
```

### SKILL.md Structure

```markdown
---
name: skill-name
description: What and when (concise, < 200 chars)
allowed-tools: Read, Grep, Glob
---

# Skill Name

[2-3 sentence overview]

## Quick Links
- [Reference 1](./reference1.md)
- [Reference 2](./reference2.md)

## [Concise sections...]
```

## Command Organization

### Simple Plugins

For plugins with few commands (< 5):

```
commands/
├── command1.md
├── command2.md
└── command3.md
```

### Complex Plugins

For plugins with many related commands, consider namespacing:

```
commands/
├── git-commit.md
├── git-push.md
├── git-branch.md
├── test-unit.md
├── test-integration.md
└── test-e2e.md
```

Commands are invoked as `/plugin-name:git-commit`, etc.

## Hook Organization

### Simple Hooks

Hooks configuration goes in `hooks/hooks.json`:

```
hooks/
└── hooks.json
```

Alternatively, hooks can be defined inline in `plugin.json` or specified via the `hooks` field:

```json
{
  "name": "my-plugin",
  "hooks": "./hooks/hooks.json"
}
```

Or inline configuration:

```json
{
  "name": "my-plugin",
  "hooks": {
    "PostToolUse": [...]
  }
}
```

### Complex Hooks

With multiple scripts, organize them under `hooks/scripts/`:

```
hooks/
├── hooks.json
└── scripts/
    ├── pre-write-validation.sh
    ├── post-write-format.sh
    └── session-start-info.sh
```

Reference scripts using the `${CLAUDE_PLUGIN_ROOT}` environment variable:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/pre-write-validation.sh"
          }
        ]
      }
    ]
  }
}
```

## Documentation Structure

### README.md (Required)

User-facing documentation:

```markdown
# Plugin Name

Brief description

## Installation

[How to install]

## Usage

[Commands, examples]

## Configuration

[If applicable]
```

### Additional Docs

For complex plugins:

```
docs/
├── getting-started.md
├── api-reference.md
├── troubleshooting.md
└── examples/
    ├── basic.md
    └── advanced.md
```

## Size Guidelines

### Keep Components Focused

- **Commands**: 50-200 lines (including examples)
- **Skills**: SKILL.md < 500 lines, plus support files
- **Agents**: 100-400 lines
- **Hooks**: Keep scripts fast (< 1 second runtime)

### When to Split

Consider splitting when:
- Single skill > 500 lines → Create multiple skills
- Many related commands → Create separate plugins
- Complex logic → Move to support files with progressive disclosure

## Common Patterns

### Multi-Component Plugin

Combines multiple component types:

```
my-dev-tools/
├── .claude-plugin/plugin.json
├── commands/          # Quick actions
│   ├── format.md
│   └── lint.md
├── agents/            # Deep analysis
│   └── code-reviewer.md
├── skills/            # Ambient guidance
│   └── code-review/SKILL.md
└── hooks/             # Automation
    ├── hooks.json
    └── scripts/
```

### Command-Only Plugin

Simple plugins with just commands:

```
utility-commands/
├── .claude-plugin/plugin.json
├── commands/
│   ├── command1.md
│   ├── command2.md
│   └── command3.md
└── README.md
```

### Skill-Focused Plugin

Domain expertise plugins:

```
framework-expert/
├── .claude-plugin/plugin.json
├── skills/
│   └── framework-guidance/
│       ├── SKILL.md
│       ├── schemas/
│       ├── templates/
│       └── examples/
└── README.md
```

## Versioning

### Plugin Versioning

Use **SemVer** in `plugin.json`:
- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backward compatible
- **Patch** (0.0.1): Bug fixes

### Change Documentation

Maintain `CHANGELOG.md`:

```markdown
# Changelog

## [1.1.0] - 2024-01-15
### Added
- New command: validate-all

### Changed
- Improved error messages

## [1.0.0] - 2024-01-01
### Added
- Initial release
```

## Testing Organization

### Test Structure

```
tests/
├── commands/
│   ├── test-command1.sh
│   └── test-command2.sh
├── hooks/
│   ├── test-validation.sh
│   └── test-formatting.sh
└── integration/
    └── test-workflow.sh
```

### Validation Scripts

Keep in `scripts/` for reuse:

```
scripts/
├── validate-plugin.sh      # Used by hooks
├── validate-commands.sh    # Used by tests
└── validate-manifest.sh    # Used by CI
```

## Anti-Patterns

### ❌ Don't: Components in .claude-plugin/

```
.claude-plugin/
├── plugin.json
├── commands/        # Wrong!
└── hooks.json       # Wrong!
```

### ✅ Do: Components at Plugin Root

```
.claude-plugin/
└── plugin.json      # Only manifest
commands/            # At root
hooks/               # At root
```

### ❌ Don't: Specify Default Paths in Manifest

```json
{
  "name": "my-plugin",
  "commands": "./commands/",
  "agents": "./agents/"
}
```

### ✅ Do: Omit Component Fields When Using Default Directories

```json
{
  "name": "my-plugin"
}
```

When using standard directories (`commands/`, `agents/`, `skills/`, `hooks/`), they are automatically discovered and you don't need to specify them in `plugin.json`. Only use component fields (`commands`, `agents`, etc.) when:
1. Using non-standard directory names (e.g., `./custom-commands/`)
2. Including specific individual files (e.g., `["./commands/special.md"]`)
3. Combining custom paths with default paths

### ❌ Don't: Absolute Paths

```json
{
  "commands": ["/Users/you/plugins/my-plugin/commands/cmd.md"]
}
```

### ✅ Do: Relative Paths (for custom paths only)

```json
{
  "commands": ["./custom/cmd.md"]
}
```

### ❌ Don't: Monolithic Skills

```markdown
# SKILL.md (3000 lines)
[Everything in one file...]
```

### ✅ Do: Progressive Disclosure

```markdown
# SKILL.md (400 lines)
Quick Links:
- [Details](./details.md)
- [Examples](./examples/)
```

## Summary Checklist

```
□ Manifest isolated in .claude-plugin/
□ Components at plugin root (not inside .claude-plugin/)
□ Default directories (commands/, agents/, skills/, hooks/) are automatically discovered
□ Component fields in plugin.json only when using custom paths
□ Kebab-case naming throughout
□ Relative paths in all configs (start with ./)
□ Skills use progressive disclosure
□ Commands are focused (< 200 lines)
□ Scripts are executable
□ Hooks reference scripts using ${CLAUDE_PLUGIN_ROOT}
□ README.md documents usage
□ Version follows SemVer
□ CHANGELOG.md tracks changes
```
