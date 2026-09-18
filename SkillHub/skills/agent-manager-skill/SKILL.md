---
name: agent-manager
description: Employee agent lifecycle management system. Use when working with agents/ directory employee agents - starting, stopping, monitoring, or assigning tasks to Dev/QA agents running in tmux sessions. Completely independent of CAO, uses only tmux + Python.
license: MIT
allowed-tools: [Read, Write, Edit, Bash, Task]
---

# Agent Manager

Employee agent orchestration system for managing AI agents in tmux sessions. A simple, dependency-light alternative to CAO.

## Quick Start

```bash
# Project-local install path varies by tool. If `.agent/skills/` doesn't exist, try `.claude/skills/`.
# List all agents
python3 .agent/skills/agent-manager/scripts/main.py list
python3 .claude/skills/agent-manager/scripts/main.py list

# (use the same path you chose above for the remaining commands)
# Start dev agent
python3 .agent/skills/agent-manager/scripts/main.py start dev

# Monitor output (live)
python3 .agent/skills/agent-manager/scripts/main.py monitor dev --follow

# Assign task
python3 .agent/skills/agent-manager/scripts/main.py assign dev <<EOF
Fix the login bug in the auth module
EOF

# Stop agent
python3 .agent/skills/agent-manager/scripts/main.py stop dev
```

### Command Path Parity (Docs Baseline)

For consistency with `README.md` and runbook examples, define one CLI alias and reuse it in your session:

```bash
# Installed skill path (pick one that exists)
CLI="python3 .agent/skills/agent-manager/scripts/main.py"
# CLI="python3 .claude/skills/agent-manager/scripts/main.py"

# If operating from a cloned repo instead of installed skill:
# CLI="python3 agent-manager/scripts/main.py"

$CLI doctor
$CLI list
$CLI status EMP_0001
```

## Core Concepts

### Agent Configuration

Agents are defined in `agents/EMP_*.md` files with YAML frontmatter:

```yaml
---
name: dev
description: Dev Agent (project-agnostic)
working_directory: ${REPO_ROOT}
launcher: ${REPO_ROOT}/projects/claude-code-switch/ccc
launcher_args:
  - cp
  - --dangerously-skip-permissions
skills:
  - review-pr
  - bsc-contract-development
---

# DEV AGENT

## Role and Identity
You are the Dev Agent...
```

**Fields:**
- `name`: Agent identifier (dev, qa)
- `description`: Agent description
- `enabled`: Whether agent can be started (default: `true`, set `false` to disable)
- `working_directory`: Default working directory (supports `${REPO_ROOT}`)
- `launcher`: Full path OR provider name
- `launcher_args`: Arguments for launcher
- `launcher_config`: Optional launcher/provider-specific startup config
- `skills`: Array of skill names from `.agent/skills/` (optional, injected at start)
- `schedules`: Array of scheduled jobs (optional, see Scheduling section)
- `tmux`: Optional tmux layout metadata (layout + target pane)

### Tmux Sessions

Each agent runs in a dedicated tmux session (`agent-{name}`):

- **Easy monitoring**: `tmux capture-pane -t agent-dev`
- **Direct interaction**: `tmux attach -t agent-dev`
- **Clean separation**: No process pollution

### Optional: Tmux Layouts

You can auto-create a tmux layout and launch the agent in a specific pane:

```yaml
tmux:
  layout:
    split: h
    panes:
      - {}
      - split: v
        panes:
          - {}
          - {}
  target_pane: "1.1"
```

Notes:
- `split`: `h` (left/right) or `v` (top/bottom). `horizontal`/`vertical` also work.
- `target_pane`: dot-separated path of `0`/`1` indexes into the layout tree.
  `0` = left/top, `1` = right/bottom. `"1.1"` means right -> bottom.
- If `tmux.layout` is set, `tmux.target_pane` is required.

### Launcher Types

**Full path**: Local Claude Code launcher
```yaml
launcher: ${REPO_ROOT}/projects/claude-code-switch/ccc
launcher_args: ["cp", "--dangerously-skip-permissions"]
```

**Provider name**: CAO provider (optional integration)
```yaml
launcher: droid
launcher_args: []
```

**Provider name**: OpenAI Codex CLI
```yaml
launcher: codex
launcher_args:
  - --model=gpt-5.2
launcher_config:
  model_instructions_file: ${REPO_ROOT}/agents/EMP_0001/prompt/shade-main-model.md
```

`launcher_config` is the generic escape hatch for launcher/provider-specific startup config. Each CLI provider adapts this flat mapping into its own startup flags (for Codex, each entry becomes `-c key=value`).

Reserved `main` agents default to the bundled skill prompt at `agent-manager/.codex/main-codex-model.md` when `launcher: codex` is used and no explicit `launcher_config.model_instructions_file` override is provided in the workspace agent config.

Note: For scheduled jobs, `agent-manager` will best-effort auto-dismiss Codex's first-run/upgrade model selection prompt to keep cron runs non-interactive.

## Commands

All examples below assume you already defined `$CLI` in **Command Path Parity (Docs Baseline)**.

### `list` - List All Agents

Show all configured agents and their status.

```bash
$CLI list              # All agents
$CLI list --running    # Only running
```

Output:
```
📋 Agents:

✅ Running dev (session: agent-dev)
   Description: Dev Agent (project-agnostic)
   Working Dir: /home/user/repo
   Skills: review-pr, bsc-contract-development

⭕ Stopped qa
   Description: QA Agent in a multi-agent system
   Working Dir: /home/user/repo/projects/CloudBank-feat-invite-code

⛔ Disabled old-dev
   Description: Legacy Dev Agent (deprecated)
   Working Dir: /home/user/repo
```

### `start` - Start an Agent

Start an agent in a tmux session.

```bash
$CLI start dev                      # Use default working_dir
$CLI start dev --working-dir /path   # Override working dir
```

- Rejects if already running (one agent, one terminal)
- Rejects if agent is disabled (`enabled: false` in config)
- Loads skills and injects as system prompt
- Session named `agent-{name}`

### `stop` - Stop a Running Agent

Stop (kill) an agent's tmux session.

```bash
$CLI stop dev
```

### `status` - Show Agent Status

Show one agent's runtime snapshot, including running state, runtime state, and the most recent heartbeat marker/event.

```bash
$CLI status dev
```

### `monitor` - Monitor Agent Output

View agent output from tmux session.

```bash
$CLI monitor dev              # Last 100 lines
$CLI monitor dev -n 500       # Last 500 lines
$CLI monitor dev --follow     # Live monitoring (Ctrl+C to stop)
```

### `send` - Send Message to Agent

Send a message/command to a running agent.

```bash
$CLI send dev "Please run tests"
$CLI send dev --no-enter "Draft message only"
```

By default, `send` submits the message immediately (Enter is sent automatically).
Use `--no-enter` to type without submitting.

### `assign` - Assign Task to Agent

Assign a task to an agent (starts if not running).

```bash
# From stdin
$CLI assign dev <<EOF
🎯 Task: Fix the login bug

1. Reproduce the issue
2. Identify root cause
3. Implement fix
4. Add tests
EOF

# From file
$CLI assign dev --task-file task.md
```

`assign` submits automatically (Enter is sent by default), so no manual tmux Enter step is required.

## Disabling Agents

Agents can be temporarily disabled to prevent them from being started (useful for maintenance, testing, or decommissioning).

### Disable an Agent

Add `enabled: false` to the agent's YAML frontmatter:

```yaml
---
name: dev
description: Dev Agent (project-agnostic)
enabled: false  # ← Agent cannot be started
working_directory: ${REPO_ROOT}
launcher: ${REPO_ROOT}/projects/claude-code-switch/ccc
---
```

### Behavior

**When an agent is disabled:**
- ⛔ `list` command shows "Disabled" status
- ⚠️ `start` command is rejected with error message
- `schedule sync` skips all schedules for the disabled agent
- Running sessions are NOT automatically stopped (manual stop required)

**To re-enable:** Set `enabled: true` or remove the field (defaults to `true`)

### Use Cases

- **Maintenance**: Temporarily disable an agent while updating its configuration
- **Testing**: Prevent a scheduled agent from running during testing
- **Decommissioning**: Mark an agent as obsolete before removing its file

## Scheduling

Agents can be configured to run automatically on a schedule using cron expressions.

### Schedule Configuration

Add a `schedules` array to the agent's YAML frontmatter:

```yaml
---
name: dev
description: Dev Agent
working_directory: ${REPO_ROOT}
launcher: ${REPO_ROOT}/projects/claude-code-switch/ccc
launcher_args:
  - cp
  - --dangerously-skip-permissions
skills:
  - bsc-contract-development

schedules:
  - name: daily-standup
    cron: "0 9 * * 1-5"
    task: |
      Review GitHub issues, prioritize today's work
    max_runtime: 30m

  - name: code-review
    cron: "0 14 * * 1-5"
    task_file: ${REPO_ROOT}/tasks/templates/code-review.md
    max_runtime: 2h

  - name: weekly-report
    cron: "0 17 * * 5"
    task: |
      Generate weekly progress report and commit to docs/
    max_runtime: 1h
    enabled: true
---
```

**Schedule Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Unique job identifier |
| `cron` | string | ✓ | Cron expression (e.g., `0 9 * * 1-5`) |
| `task` | string | △ | Inline task description |
| `task_file` | string | △ | Path to task file (supports `${REPO_ROOT}`) |
| `max_runtime` | string | | Maximum runtime (e.g., `30m`, `2h`, `8h`) |
| `enabled` | bool | | Default: `true` |

> **Note**: Either `task` or `task_file` must be provided.

### Schedule Commands

#### `schedule list` - List All Scheduled Jobs

```bash
$CLI schedule list
```

Output:
```
📅 Scheduled Jobs:

dev (EMP_0001):
  ✓ daily-standup         0 9 * * 1-5          (30m)
  ✓ code-review           0 14 * * 1-5         (2h)
  ✓ weekly-report         0 17 * * 5           (1h)

qa (EMP_0002):
  ✓ nightly-tests         0 2 * * *            (4h)
```

#### `schedule sync` - Sync Schedules to Crontab

Synchronize all agent schedules to the system crontab.

```bash
# Preview changes (dry run)
$CLI schedule sync --dry-run

# Apply changes
$CLI schedule sync
```

This generates crontab entries like:
```cron
# === agent-manager schedules (auto-generated) ===
# dev (EMP_0001)
# daily-standup
0 9 * * 1-5 cd /path/to/repo && python3 /absolute/path/to/agent-manager/scripts/main.py schedule run dev --job daily-standup >> /tmp/agent-emp-0001-daily-standup.log 2>&1
# === end agent-manager schedules ===
```

#### `schedule run` - Run a Scheduled Job Manually

Manually trigger a scheduled job (useful for testing).

```bash
$CLI schedule run dev --job daily-standup

# Override timeout
$CLI schedule run dev --job daily-standup --timeout 1h
```

## Heartbeat

Heartbeat is a special type of periodic job that sends a standard check-in message to running agents. Unlike schedules (which can have multiple jobs per agent), each agent can have **0 or 1 heartbeat** configuration.

### Heartbeat Configuration

Add a `heartbeat` dict to the agent's YAML frontmatter:

```yaml
---
name: dev
description: Dev Agent
working_directory: ${REPO_ROOT}
launcher: codex
launcher_args:
  - --model=gpt-4.7
  - --dangerously-bypass-approvals-and-sandbox

heartbeat:
  cron: "*/30 * * * *"  # Every 30 minutes
  max_runtime: 5m
  session_mode: auto     # restore | auto | fresh
  mode: normal           # normal (use `timer` for delayed rescue; `full_speed` is legacy)
  dream:
    enabled: true
    idle_after: 1h       # Optional idle-window trigger after normal HEARTBEAT_OK cycles
    max_runtime: 30m
    fixed_windows:       # During these windows heartbeat dispatch sends DREAM.md tasks
      - timezone: Asia/Shanghai
        start: "23:00"
        end: "08:00"
  enabled: true
---
```

**Heartbeat Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `cron` | string | ✓ | Cron expression (e.g., `*/30 * * * *`) |
| `max_runtime` | string | | Maximum runtime (e.g., `5m`, `10m`) |
| `session_mode` | string | | Session policy: `restore` (default), `auto` (rollover when context <25%), `fresh` (always rollover after handoff) |
| `mode` | string | | Heartbeat trigger mode. `normal` is the only active path. `full_speed` is a deprecated compatibility value that only preserves legacy Codex hook cleanup/readback during `start`; timer-driven follow-up is the supported replacement. |
| `auto_starvation_skip_threshold` | int | | `auto` mode only. Default `3`; set `0` to disable the forced-dispatch starvation bypass after consecutive preflight skips |
| `dream` | dict | | Optional Dream mode policy. `idle_after` preserves the existing post-heartbeat Dream timer behavior; `fixed_windows` switches heartbeat dispatch to a Dream task while any configured window is active. |
| `enabled` | bool | | Default: `true` |

`full_speed` should now be treated as a legacy compatibility marker, not a canonical execution path. If an older Codex Stop hook is still present, `start` will clean it up; new delayed follow-up / rescue flows should use `timer`.

### Fixed Dream Windows

When `heartbeat.dream.enabled` is true and the current wall-clock time is inside
any `heartbeat.dream.fixed_windows` rule, `heartbeat run` sends the standard
Dream prompt instead of the standard heartbeat prompt:

```
Read DREAM.md if it exists ... If nothing worth doing emerges, reply DREAM_OK.
```

Fixed windows support `timezone`, `start`, `end`, `work_days`, `holidays`,
`extra_workdays`, and `when`. Overnight ranges are supported (`23:00` →
`08:00`). If `work_days` is omitted, fixed Dream windows default to all seven
days. Multiple windows are OR rules: the first active window wins.

### Heartbeat vs Schedules

| Feature | Heartbeat | Schedules |
|---------|-----------|-----------|
| **Per agent** | 0-1 heartbeat | 0-N schedules |
| **Task content** | Fixed (standard check-in) | Custom per job |
| **Behavior** | Only checks running agents | Starts agent if needed |
| **Use case** | Periodic health checks | Task automation |

### Heartbeat Commands

#### `heartbeat list` - List All Heartbeat Jobs

```bash
$CLI heartbeat list
```

Output:
```
💓 Heartbeats:

dev (EMP_0001):
  ✓ heartbeat           */30 * * * *         (5m session:auto)
```

#### `heartbeat sync` - Sync Heartbeats to Crontab

Heartbeats and schedules are synced together to the system crontab.

```bash
# Preview changes (dry run)
$CLI heartbeat sync --dry-run

# Apply changes
$CLI heartbeat sync
```

This generates crontab entries like:
```cron
# === agent-manager schedules (auto-generated) ===
# dev (EMP_0001)
# heartbeat [HB]
*/30 * * * * cd /path/to/repo && python3 /absolute/path/to/agent-manager/scripts/main.py heartbeat run EMP_0001 >> /path/to/.crontab_logs/agent-emp-0001-heartbeat.log 2>&1
# === end agent-manager schedules ===
```

#### `heartbeat run` - Run a Heartbeat Manually

Manually trigger a heartbeat (useful for testing).

```bash
$CLI heartbeat run EMP_0001

# Override timeout
$CLI heartbeat run EMP_0001 --timeout 1m
```

**Heartbeat behavior:**
- Skips if agent is disabled
- Skips if agent is not running (does NOT start the agent)
- Sends standard heartbeat message to the agent
- Optional session rollover via `session_mode` (handoff first, then fresh session)
- Waits for response (up to `max_runtime`)
- In `auto` mode, stale pending heartbeats can schedule or trigger rescue via the timer-backed recovery path

### `timer` - Schedule Delayed Actions

Use `timer` for one-shot delayed actions without cron:

```bash
# Run one heartbeat in 5 seconds
$CLI timer heartbeat main --delay 5s

# Schedule one heartbeat rescue in 5 seconds
$CLI timer rescue main --delay 5s --timeout 8m --reason auto_pending_heartbeat_rescue

# Run an arbitrary agent-manager command in 5 seconds
$CLI timer command --delay 5s -- heartbeat run main --timeout 8m

# Inspect recent timers
$CLI timer list
```

Each run appends structured JSONL audit events to:

```
.claude/state/agent-manager/heartbeat-audit/{agent_id}.jsonl
```

Event fields (standardized for observability):

- `timestamp`
- `agent_id`
- `hb_id`
- `stage` (standard stage name, default `heartbeat_attempt`)
- `result` (`success` / `failure` / `pending`)
- `duration` (milliseconds, alias of `duration_ms`)
- `send_status`
- `ack_status`
- `duration_ms`
- `context_left`
- `failure_type`
- `session_mode`
- `reason_code`
- `attempt`
- `recovery_action`
- `reason_code`

Failure classification (`failure_type`) includes:

- `send_fail`
- `no_ack`
- `timeout`
- `blocked`

#### `heartbeat trace` - Query Heartbeat Audit Logs

```bash
# Recent events
$CLI heartbeat trace

# Filter by heartbeat id
$CLI heartbeat trace --hb-id 20260209-120001

# Filter by agent + time range (UTC)
$CLI heartbeat trace   --agent EMP_0001   --since 2026-02-09T00:00:00Z   --until 2026-02-10T00:00:00Z

# Output JSON
$CLI heartbeat trace --agent EMP_0001 --json
```

#### `heartbeat slo` - Daily/Weekly SLO Summary

```bash
# Daily summary (default)
$CLI heartbeat slo

# Weekly summary for one agent
$CLI heartbeat slo --window weekly --agent EMP_0001

# Explicit time window + JSON
$CLI heartbeat slo   --since 2026-02-01T00:00:00Z   --until 2026-02-08T00:00:00Z   --json
```

Built-in SLO checks:

- Success rate target: `>= 99%`
- Timeout rate target: `<= 2%`
- Recovery p95 target: `<= 120000ms`

Standalone summary script (same metrics):

```bash
python3 scripts/heartbeat_slo.py --window daily
python3 scripts/heartbeat_slo.py --window weekly --agent EMP_0001 --json
```

### Standard Heartbeat Message

The heartbeat sends this message to the agent:

```
Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.
```

Agents should respond with `HEARTBEAT_OK` if nothing needs attention, or take action based on their `HEARTBEAT.md` file contents.

## Skills Integration

Agents can reference skills from `.agent/skills/`:

```yaml
skills:
  - review-pr
  - bsc-contract-development
  - cao
```

When the agent starts, skill contents are injected as system prompt:

```
## Available Skills

### review-pr
Code review skill for GitHub PRs and local changes...

### bsc-contract-development
Comprehensive BSC smart contract development expertise...
```

**Available Skills:**
- `bsc-contract-development` - BSC smart contract development
- `cao` - CLI Agent Orchestrator
- `collab-pr-fix-loop` - QA→Dev→QA PR iteration
- `review-pr` - Code review for PRs
- `skill-creator` - Creating new skills

## Architecture

```
.agent/skills/agent-manager/
├── SKILL.md                    # This file
├── scripts/
│   ├── main.py                 # CLI entry point
│   ├── heartbeat_slo.py        # Heartbeat SLO summary script
│   ├── agent_config.py         # Agent file parser
│   ├── tmux_helper.py          # Tmux wrapper
│   └── schedule_helper.py      # Crontab management
├── providers/
│   └── __init__.py             # CLI provider configs
└── references/
    └── task_templates.md       # Optional task templates
```

### Design Principles

1. **Zero CAO Dependency**: Only tmux + Python required
2. **Provider Pattern Inspiration**: Learn from CAO but implement simply
3. **Tmux-Native**: Each agent in its own tmux session
4. **YAML Frontmatter**: Leverage existing agent file format
5. **Environment Variables**: Handle `${REPO_ROOT}` expansion
6. **One Agent, One Terminal**: Reject duplicate starts

## Comparison with CAO

| Feature | CAO | Agent Manager |
|---------|-----|--------------|
| Dependencies | CAO server, uvx, requests | tmux, Python only |
| Complexity | High (HTTP API, providers) | Low (direct tmux) |
| Session Mgmt | CAO server | Native tmux |
| Monitoring | HTTP API calls | Native tmux |
| Extensibility | Provider system | Direct script editing |
| Installation | CAO server setup | No server needed |
| Use Case | Complex workflows | Simple agent management |

## Error Handling

- **tmux not installed**: Clear error with install command
- **Agent not found**: Lists available agents
- **Already running**: Prompts to stop first
- **Not running**: Prompts to start first

## Runbook Checklist

For operations handoff and incident response, use:
- `agent-manager/docs/runbook-checklist.md`

It includes:
- 30-minute newcomer self-check path
- heartbeat no-ack troubleshooting SOP
- stuck-session recovery SOP
- CI/QA merge-gate checklist and evidence template

## Advanced Usage

### Direct Tmux Interaction

```bash
# Attach to agent session (interactive)
tmux attach -t agent-dev

# Detach from session: Ctrl+b, then d

# Capture output manually
tmux capture-pane -p -t agent-dev -S -100

# List all agent sessions
tmux ls | grep ^agent-
```

### Workflow Example

```bash
# Morning: Start agents
$CLI start dev
$CLI start qa

# Assign task to dev
$CLI assign dev <<EOF
Implement the user profile feature:
1. Profile update API
2. Profile view component
3. Integration tests
EOF

# Quick runtime snapshot
$CLI status dev

# Monitor progress
$CLI monitor dev --follow

# Send clarification if needed
$CLI send dev "Please add validation for email format"

# After dev completes, assign to QA
$CLI assign qa <<EOF
Review the user profile feature:
- Security check
- Edge cases
- Test coverage
EOF

# Evening: Stop agents
$CLI stop dev
$CLI stop qa
```
