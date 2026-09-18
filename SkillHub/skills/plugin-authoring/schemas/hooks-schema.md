# Hooks Schema

Hooks allow you to run commands at specific lifecycle events. Define them in `hooks/hooks.json`.

## Location

`hooks/hooks.json` (at plugin root, referenced in `plugin.json`)

## Structure

```json
{
  "description": "Optional description of what these hooks do",
  "hooks": {
    "EventName": [
      {
        "matcher": "pattern",
        "hooks": [
          {
            "type": "command",
            "command": "path/to/script.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Hook Types

Hooks support three execution types:

### Command Hooks (`type: "command"`)

Execute shell commands with access to stdin (JSON input) and stdout/stderr.

```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
  "timeout": 30
}
```

### Prompt Hooks (`type: "prompt"`)

Evaluate a prompt with an LLM. Supported for: `Stop`, `SubagentStop`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`.

```json
{
  "type": "prompt",
  "prompt": "Your evaluation prompt with $ARGUMENTS placeholder",
  "timeout": 30
}
```

**LLM Response Schema**:
```json
{
  "decision": "approve" | "block",
  "reason": "Explanation",
  "continue": false,
  "stopReason": "User message",
  "systemMessage": "Warning"
}
```

### Agent Hooks (`type: "agent"`)

Run an agentic verifier with tools. For complex validation requiring tool access.

## Event Types

### PreToolUse

Runs **before** Claude uses a tool. Can block tool execution, modify inputs, or auto-approve.

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Matchers**: Tool names (case-sensitive regex patterns)
- Built-in tools: `Task`, `Bash`, `Glob`, `Grep`, `Read`, `Edit`, `Write`, `WebFetch`, `WebSearch`
- Regex patterns: `Edit|Write`, `Notebook.*`
- Wildcard: `*` matches all tools
- MCP tools: `mcp__<server>__<tool>` (e.g., `mcp__memory__create_entities`)

**Exit codes**:
- `0`: Allow (stdout visible to Claude)
- `2`: **Block** (stderr shown to Claude as feedback)
- Other: Warning (non-blocking)

### PermissionRequest

Runs when user is shown a permission dialog. Can auto-allow or deny on behalf of user.

```json
{
  "PermissionRequest": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/auto-approve.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

**Matchers**: Same as PreToolUse (tool names, regex patterns, MCP tools)

### PostToolUse

Runs **after** a tool completes successfully. Can provide feedback to Claude.

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**Matchers**: Same as PreToolUse

### Notification

Runs when Claude Code sends notifications.

```json
{
  "Notification": [
    {
      "matcher": "permission_prompt",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/notify.sh"
        }
      ]
    }
  ]
}
```

**Matchers**:
- `permission_prompt` - Claude needs permission to use a tool
- `idle_prompt` - Prompt input idle for 60+ seconds (system default, not configurable)
- `auth_success` - Authentication success notifications
- `elicitation_dialog` - Claude Code needs input for MCP tool elicitation

### UserPromptSubmit

Runs when user submits a prompt. Can block prompt processing or add context.

```json
{
  "UserPromptSubmit": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/context-injector.sh"
        }
      ]
    }
  ]
}
```

**No matchers** - omit the matcher field.

**Exit codes**:
- `0`: Allow (stdout added to context)
- `2`: **Block** (stderr shown to user)

### Stop / SubagentStop

Runs when Claude attempts to stop (main agent or subagent). Can decide if Claude should continue.

```json
{
  "Stop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/check-continuation.sh"
        }
      ]
    }
  ]
}
```

**No matchers** - omit the matcher field.

### PreCompact

Runs before Claude Code performs a compact operation.

```json
{
  "PreCompact": [
    {
      "matcher": "auto",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/backup-transcript.sh"
        }
      ]
    }
  ]
}
```

**Matchers**:
- `manual` - User-triggered compaction
- `auto` - Automatic compaction

### SessionStart

Runs when Claude Code session starts.

```json
{
  "SessionStart": [
    {
      "matcher": "startup",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'Plugin loaded!'"
        }
      ]
    }
  ]
}
```

**Matchers**:
- `startup` - Invoked from startup
- `resume` - Invoked from `--resume`, `--continue`, or `/resume`
- `clear` - Invoked from `/clear`
- `compact` - Invoked from auto or manual compact

**Note**: SessionStart stdout is added to context automatically for Claude.

**Special**: SessionStart hooks have access to `CLAUDE_ENV_FILE` for persisting environment variables.

### SessionEnd

Runs when a Claude Code session ends. Cannot block termination but can perform cleanup.

```json
{
  "SessionEnd": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/cleanup.sh"
        }
      ]
    }
  ]
}
```

**No matchers** - omit the matcher field.

**Reason field in input**: `exit`, `clear`, `logout`, `prompt_input_exit`, `other`

## Environment Variables

Available in hook commands:

### All Hooks
- `${CLAUDE_PLUGIN_ROOT}`: Absolute path to plugin root
- `${CLAUDE_PROJECT_DIR}`: Project root directory (where Claude Code started)
- `CLAUDE_CODE_REMOTE`: `"true"` if running in remote (web) environment, empty/unset for local CLI
- Standard shell environment variables

### SessionStart Hooks Only
- `CLAUDE_ENV_FILE`: File path where you can persist environment variables for subsequent bash commands

**Example: Persisting environment variables**
```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export API_KEY=your-api-key' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

**Example: Persisting environment changes from nvm**
```bash
#!/bin/bash
ENV_BEFORE=$(export -p | sort)
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

## Timeouts

- Default: 60 seconds (configurable per hook)
- Recommended: 10-30 seconds for validation
- Max: Keep under 60 seconds for good UX

## JSON Output Format

Hooks communicate through exit codes, stdout, and stderr. For advanced control, output JSON to stdout with exit code 0.

### Exit Codes
- **0**: Success. JSON in stdout parsed for structured control
- **2**: Blocking error. Only `stderr` used as error message. JSON in stdout ignored
- **Other**: Non-blocking error. Stderr shown in verbose mode (ctrl+o)

### Common Fields (All Hooks)

```json
{
  "continue": true,
  "stopReason": "Reason shown to user",
  "suppressOutput": false,
  "systemMessage": "Warning message"
}
```

- `continue`: Allow Claude to continue (default: true)
- `stopReason`: Why stopped (shown to user when continue=false)
- `suppressOutput`: Hide output from transcript
- `systemMessage`: Warning/info message shown to user

### Hook-Specific Output (`hookSpecificOutput`)

#### PreToolUse

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "Explanation",
    "updatedInput": {
      "field_to_modify": "new_value"
    }
  }
}
```

- `permissionDecision`: `"allow"` (auto-approve), `"deny"` (block), `"ask"` (show permission dialog)
- `updatedInput`: Optional object to modify tool input parameters before execution

#### PermissionRequest

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow" | "deny",
      "updatedInput": {},
      "message": "Denial reason",
      "interrupt": false
    }
  }
}
```

- `behavior`: `"allow"` or `"deny"` the permission request
- `updatedInput`: Optional for "allow" - modify tool inputs
- `message`: Optional for "deny" - tells Claude why permission was denied
- `interrupt`: Optional for "deny" - if true, stops Claude entirely

#### PostToolUse

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Extra info for Claude"
  }
}
```

- `decision`: Set to `"block"` to provide feedback that blocks further action
- `additionalContext`: Additional information added to Claude's context

#### UserPromptSubmit

```json
{
  "decision": "block" | undefined,
  "reason": "Why blocked (not added to context)",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Context added to conversation"
  }
}
```

Alternatively, plain text stdout with exit code 0 is added as context.

#### Stop / SubagentStop

```json
{
  "decision": "block" | undefined,
  "reason": "Must provide when blocking - tells Claude how to proceed"
}
```

- `decision`: Set to `"block"` to prevent Claude from stopping and continue working
- `reason`: Required when blocking - instructs Claude on what to do next

#### SessionStart

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Context loaded at session start"
  }
}
```

## MCP Tool Matching

MCP tools follow the pattern: `mcp__<server>__<tool>`

**Examples**:
- `mcp__memory__create_entities`
- `mcp__filesystem__read_file`
- `mcp__github__search_repositories`

**Configuration**:
```json
{
  "PreToolUse": [
    {
      "matcher": "mcp__memory__.*",
      "hooks": [
        {
          "type": "command",
          "command": "echo 'Memory operation' >> ~/mcp-operations.log"
        }
      ]
    },
    {
      "matcher": "mcp__.*__write.*",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-mcp-write.py"
        }
      ]
    }
  ]
}
```

## Common Patterns

### Validation Hook (Blocking)

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh",
          "timeout": 30
        }
      ]
    }
  ]
}
```

**validate.sh**:
```bash
#!/usr/bin/env bash
if [ validation_fails ]; then
  echo "Error: validation failed" >&2
  exit 2  # Block the tool
fi
exit 0  # Allow
```

**Advanced JSON output** (alternative to exit codes):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "File violates security policy"
  },
  "suppressOutput": true
}
```

### Formatting Hook (Non-blocking)

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
          "timeout": 30
        }
      ]
    }
  ]
}
```

### Startup Message

```json
{
  "SessionStart": [
    {
      "matcher": "startup",
      "hooks": [
        {
          "type": "command",
          "command": "echo '✓ My Plugin loaded'"
        }
      ]
    }
  ]
}
```

## Best Practices

- **Use `${CLAUDE_PLUGIN_ROOT}`** for portable paths
- **Set timeouts** to prevent hanging (10-30 seconds recommended)
- **Exit code 2** to block (PreToolUse/UserPromptSubmit)
- **Keep scripts fast** (< 1 second ideally)
- **Make scripts executable** (`chmod +x`)
- **Test hooks** before distributing
- **Handle JSON output** for advanced control (see advanced examples)

## Common Mistakes

❌ **Absolute paths** (not portable)
```json
{
  "command": "/Users/you/plugin/scripts/validate.sh"
}
```

✅ **Plugin-relative paths**
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

❌ **No timeout** on slow operations
```json
{
  "command": "npm install"
  // Missing timeout!
}
```

✅ **Set appropriate timeout**
```json
{
  "command": "npm install",
  "timeout": 300000
}
```

❌ **Missing required matcher**
```json
{
  "SessionStart": [
    {
      "hooks": [...]  // No matcher!
    }
  ]
}
```

✅ **Include appropriate matcher**
```json
{
  "SessionStart": [
    {
      "matcher": "startup",
      "hooks": [...]
    }
  ]
}
```

## Debugging

Use `claude --debug` to see:
- Hook registration
- Hook execution timing
- Exit codes and output
- Blocking decisions
