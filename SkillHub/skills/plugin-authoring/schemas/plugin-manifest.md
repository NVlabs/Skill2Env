# Plugin Manifest Schema

The `plugin.json` file in `.claude-plugin/` defines your plugin's metadata and optionally custom component paths.

## Location

`.claude-plugin/plugin.json` (at plugin root)

## Required Fields

```json
{
  "name": "plugin-name"
}
```

- **name**: kebab-case string, unique identifier (REQUIRED)

## Optional Fields

### Standard Metadata

```json
{
  "version": "1.0.0",
  "description": "What your plugin does",
  "author": {
    "name": "Your Name",
    "email": "you@example.com",
    "url": "https://github.com/your-username"
  },
  "homepage": "https://your-plugin-homepage.com",
  "repository": "https://github.com/your-org/your-repo",
  "license": "MIT",
  "keywords": ["tag1", "tag2"]
}
```

- **version**: Semantic version format (optional metadata)
- **description**: Brief explanation of plugin purpose (optional metadata)
- **author**: Can be string or object with name, email, url
- **homepage**: Documentation URL (optional metadata)
- **repository**: Source code URL (optional metadata)
- **license**: License identifier like "MIT" (optional metadata)
- **keywords**: Array of tags for discovery (optional metadata)

### Component Configuration (Custom Paths Only)

**IMPORTANT**: Only include these fields if you're using **non-standard** paths. If using standard directory structure (`commands/`, `agents/`, `skills/`, `hooks/`), omit these fields entirely.

```json
{
  "commands": ["./custom/path/cmd1.md", "./custom/path/cmd2.md"],
  "agents": "./custom/agents/",
  "hooks": "./custom/hooks/hooks.json",
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["path/to/server.js"]
    }
  },
  "lspServers": "./.lsp.json",
  "outputStyles": "./styles/"
}
```

### Component Path Rules

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `commands` | string\|array | Additional command files/directories | `"./custom/cmd.md"` or `["./cmd1.md"]` |
| `agents` | string\|array | Additional agent files/directories | `"./custom/agents/"` or `["./agents/reviewer.md"]` |
| `skills` | string\|array | Additional skill directories | `"./custom/skills/"` |
| `hooks` | string\|object | Hook config path or inline config | `"./hooks.json"` |
| `mcpServers` | string\|object | MCP config path or inline config | `"./mcp-config.json"` |
| `outputStyles` | string\|array | Additional output style files/directories | `"./styles/"` or `["./style1.md"]` |
| `lspServers` | string\|object | LSP config path or inline config | `"./.lsp.json"` |

All paths must be **relative to plugin root** (where `.claude-plugin/` lives) and start with `./`

**Note**: Custom paths supplement default directories - they don't replace them. If `commands/` exists, it's loaded in addition to custom command paths.

### Skills Configuration

For Skills (Agent Skills) provided by your plugin, you can restrict which tools Claude can use:

```json
{
  "name": "my-skill-plugin",
  "skills": [
    {
      "name": "safe-reader",
      "allowed-tools": ["Read", "Grep", "Glob"]
    }
  ]
}
```

However, the recommended approach is to specify `allowed-tools` directly in the `SKILL.md` frontmatter:

```yaml
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

### Environment Variables

**`${CLAUDE_PLUGIN_ROOT}`** is a special environment variable available in your plugin that contains the absolute path to your plugin directory. Use this in hooks, MCP servers, and scripts to ensure correct paths regardless of installation location.

```json
{
  "name": "my-plugin",
  "hooks": "./hooks/hooks.json"
}
```

Where `hooks/hooks.json` contains:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Or inline hooks:

```json
{
  "name": "my-plugin",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
          }
        ]
      }
    ]
  }
}
```

Use `${CLAUDE_PLUGIN_ROOT}` for:
- Scripts executed by hooks
- MCP server paths
- Config files referenced by components
- Any file paths in your plugin configuration

### Hook Types

Hooks support three execution types:

| Type | Description | Use Case |
|------|-------------|----------|
| `command` | Execute shell commands/scripts | Run linters, formatters, validation scripts |
| `prompt` | Evaluate prompt with LLM (uses `$ARGUMENTS`) | Context-aware decisions, natural language checks |
| `agent` | Run agentic verifier with tools | Complex verification requiring tool access |

**Command Hook Example**:
```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh",
  "timeout": 30
}
```

**Prompt Hook Example** (for Stop, SubagentStop, UserPromptSubmit, PreToolUse, PermissionRequest):
```json
{
  "type": "prompt",
  "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete.",
  "timeout": 30
}
```

### Hook Events

Claude Code supports the following hook events:

| Event | Description |
|-------|-------------|
| `PreToolUse` | Runs after Claude creates tool parameters, before processing the tool call |
| `PostToolUse` | Runs immediately after a tool completes successfully |
| `PermissionRequest` | Runs when a permission dialog is shown to the user |
| `UserPromptSubmit` | Runs when the user submits a prompt, before Claude processes it |
| `Notification` | Runs when Claude Code sends notifications |
| `Stop` | Runs when the main Claude Code agent finishes responding |
| `SubagentStop` | Runs when a Claude Code subagent (Task tool call) finishes responding |
| `SessionStart` | Runs when Claude Code starts or resumes a session |
| `SessionEnd` | Runs when a Claude Code session ends |
| `PreCompact` | Runs before a compact operation |

### Hook Matchers

For `PreToolUse`, `PermissionRequest`, and `PostToolUse` events, use matchers to target specific tools:

| Pattern | Behavior |
|---------|----------|
| `Write` | Exact match (case-sensitive) |
| `Edit\|Write` | Regex alternation |
| `Notebook.*` | Regex patterns |
| `*` or `""` | Match all tools |
| `mcp__memory__.*` | Match MCP tools |

### LSP Server Configuration

Configure Language Server Protocol servers for code intelligence:

**File Configuration** (`.lsp.json` at plugin root):
```json
{
  "lspServers": "./.lsp.json"
}
```

**Inline Configuration**:
```json
{
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    },
    "python": {
      "command": "pyright-langserver",
      "args": ["--stdio"],
      "extensionToLanguage": {
        ".py": "python",
        ".pyi": "python"
      }
    }
  }
}
```

**LSP Configuration Fields**:
- **command**: The language server binary name
- **args**: Arguments to pass to the server
- **extensionToLanguage**: Maps file extensions to language identifiers

**Note**: Users must have the language server binary installed on their machine.

## Examples

### Standard Directory Structure (Recommended)

```json
{
  "name": "my-dev-tools"
}
```

**Minimal plugin** - The simplest possible plugin. Claude Code automatically discovers `commands/`, `agents/`, `skills/`, and `hooks/` directories.

```json
{
  "name": "my-dev-tools",
  "version": "1.2.0",
  "description": "Developer productivity tools for Claude Code",
  "author": {
    "name": "Dev Team",
    "email": "dev@company.com"
  },
  "license": "MIT",
  "keywords": ["productivity", "tools"]
}
```

**With metadata** - Adding optional metadata for better discovery and documentation.

### Custom Paths

```json
{
  "name": "enterprise-plugin",
  "description": "Enterprise development tools",
  "author": {
    "name": "Your Name"
  },
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

**Note**: Using custom paths to organize components. The `description` and `author` fields are optional metadata.

## Common Mistakes

**Wrong**: Including component fields with standard paths
```json
{
  "name": "my-plugin",
  "commands": "./commands/",
  "agents": "./agents/"
}
```

**Correct**: Omit component fields for standard paths
```json
{
  "name": "my-plugin"
}
```

**Wrong**: Absolute paths
```json
{
  "commands": "/Users/you/plugins/my-plugin/commands/"
}
```

**Correct**: Relative paths starting with `./`
```json
{
  "commands": ["./custom/cmd.md"]
}
```

**Wrong**: Placing component directories inside `.claude-plugin/`
```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json
│   ├── commands/       # Wrong location!
│   └── agents/         # Wrong location!
```

**Correct**: Component directories at plugin root
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json     # Only plugin.json goes here
├── commands/           # At plugin root
├── agents/             # At plugin root
└── skills/             # At plugin root
```

## Agents Path Formats

Both directory paths and file arrays are valid for agents:

**Directory Path**:
```json
{
  "agents": "./custom/agents/"
}
```

**Array of Files**:
```json
{
  "agents": ["./agents/reviewer.md", "./agents/tester.md"]
}
```

**Mixed (using default + custom)**:
```json
{
  "agents": "./specialized-agents/"
}
```
This loads both the default `agents/` directory AND `./specialized-agents/`.

## Validation

Use `/plugin-development:validate` to check your manifest structure.
