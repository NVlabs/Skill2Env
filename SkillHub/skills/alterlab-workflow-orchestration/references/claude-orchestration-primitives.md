# Claude Code + Agent SDK Orchestration Primitives (verified reference)

All facts below were verified against the official documentation on
**2026-06-08**:

- `code.claude.com/docs/en/sub-agents` (Create custom subagents)
- `code.claude.com/docs/en/agent-teams` (Orchestrate teams of Claude Code sessions)
- `code.claude.com/docs/en/agent-sdk/overview` (Agent SDK overview)

Do not restate orchestration mechanics from memory — load this file and quote it.

## Table of Contents

1. [Subagents — what they are](#1-subagents--what-they-are)
2. [Subagent frontmatter fields](#2-subagent-frontmatter-fields)
3. [Built-in subagents](#3-built-in-subagents)
4. [Invocation, delegation, parallelism, chaining](#4-invocation-delegation-parallelism-chaining)
5. [Foreground vs background](#5-foreground-vs-background)
6. [Forks](#6-forks)
7. [Agent teams (experimental)](#7-agent-teams-experimental)
8. [Claude Agent SDK](#8-claude-agent-sdk)
9. [Key limits and gotchas](#9-key-limits-and-gotchas)

---

## 1. Subagents — what they are

> "Subagents are specialized AI assistants that handle specific types of tasks."

> "Each subagent runs in its own context window with a custom system prompt,
> specific tool access, and independent permissions. When Claude encounters a
> task that matches a subagent's description, it delegates to that subagent,
> which works independently and returns results."

Subagents are defined as Markdown files with YAML frontmatter. Storage by scope
(higher priority wins on name collision):

| Location | Scope | Priority |
|----------|-------|----------|
| Managed settings `.claude/agents/` | Organization-wide | 1 (highest) |
| `--agents` CLI flag (JSON) | Current session | 2 |
| `.claude/agents/` | Current project | 3 |
| `~/.claude/agents/` | All your projects | 4 |
| Plugin's `agents/` directory | Where plugin enabled | 5 (lowest) |

Identity comes only from the `name` frontmatter field; the filename and subfolder
path do not affect how a subagent is invoked. Subagents are loaded at session
start — editing a file on disk requires a restart (the `/agents` interface takes
effect immediately).

## 2. Subagent frontmatter fields

Only `name` and `description` are **required**. Verified optional fields:

| Field | Purpose |
|-------|---------|
| `name` | Unique lowercase-and-hyphens identifier; hooks receive it as `agent_type` |
| `description` | When Claude should delegate to this subagent (the trigger signal) |
| `tools` | Allowlist of tools; inherits all if omitted |
| `disallowedTools` | Denylist; applied before `tools` is resolved |
| `model` | `sonnet`, `opus`, `haiku`, a full id (e.g. `claude-opus-4-8`), or `inherit` (default) |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | Max agentic turns before the subagent stops |
| `skills` | Skills to **preload** (full content injected at startup) |
| `mcpServers` | MCP servers scoped to this subagent |
| `hooks` | Lifecycle hooks scoped to this subagent |
| `memory` | Persistent memory scope: `user`, `project`, or `local` |
| `background` | `true` to always run as a background task (default `false`) |
| `effort` | `low`/`medium`/`high`/`xhigh`/`max` (model-dependent) |
| `isolation` | `worktree` to run in an isolated git worktree |
| `color` | Display color in the task list/transcript |

Minimal valid subagent (from the docs):

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

> "Subagents receive only this system prompt (plus basic environment details like
> working directory), not the full Claude Code system prompt."

## 3. Built-in subagents

| Agent | Model | Tools | Purpose |
|-------|-------|-------|---------|
| **Explore** | Haiku | Read-only (no Write/Edit) | File discovery, code search |
| **Plan** | Inherits | Read-only | Codebase research for plan mode |
| **general-purpose** | Inherits | All tools | Complex multi-step exploration + action |

Explore and Plan skip CLAUDE.md and git status to stay fast/cheap; every other
subagent loads both.

## 4. Invocation, delegation, parallelism, chaining

> "Claude automatically delegates tasks based on the task description in your
> request, the `description` field in subagent configurations, and current
> context. To encourage proactive delegation, include phrases like 'use
> proactively' in your subagent's description field."

Three explicit-invocation patterns: natural language (name the subagent),
@-mention (`@"code-reviewer (agent)"`, guarantees that subagent), and session-wide
(`claude --agent <name>` or the `agent` setting).

**Parallel research** (verbatim doc example):

> "Research the authentication, database, and API modules in parallel using
> separate subagents"

> "Each subagent explores its area independently, then Claude synthesizes the
> findings. This works best when the research paths don't depend on each other."

**Chaining** (verbatim doc example):

> "Use the code-reviewer subagent to find performance issues, then use the
> optimizer subagent to fix them"

> "Each subagent completes its task and returns results to Claude, which then
> passes relevant context to the next subagent."

## 5. Foreground vs background

- **Foreground**: blocks the main conversation; permission prompts pass through.
- **Background**: runs concurrently; runs with permissions already granted and
  **auto-denies** any tool call that would otherwise prompt.

Caution from the docs: "Running many subagents that each return detailed results
can consume significant context." Disable background tasks with
`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`.

## 6. Forks

Forks require Claude Code **v2.1.117+**; from v2.1.161 `/fork` is enabled by
default, otherwise set `CLAUDE_CODE_FORK_SUBAGENT=1`.

> "A fork is a subagent that inherits the entire conversation so far instead of
> starting fresh."

Because the fork's system prompt and tools are identical to the parent, its first
request reuses the parent's prompt cache — cheaper than a fresh subagent for tasks
needing the same context. A fork cannot spawn further forks. Start one with
`/fork <directive>`.

## 7. Agent teams (experimental)

> "Agent teams are experimental and disabled by default. Enable them by adding
> `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`".

Requires Claude Code **v2.1.32+**. Set the env var to `1` (shell or settings.json).

Difference from subagents (verbatim):

> "Unlike subagents, which run within a single session and can only report back to
> the main agent, you can also interact with individual teammates directly without
> going through the lead."

Architecture: a **team lead** (the creating session), **teammates** (separate
Claude Code instances, each own context), a **shared task list**, and a
**mailbox** for inter-agent messaging. Teammates can message each other directly.

**Adversarial / competing-hypotheses example (verbatim):**

> "Users report the app exits after one message instead of staying connected.
> Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
> each other to try to disprove each other's theories, like a scientific debate.
> Update the findings doc with whatever consensus emerges."

Best practices from the docs: start with **3–5 teammates**; ~5–6 tasks per
teammate; agent teams "use significantly more tokens than a single session."
Reuse roles via subagent definitions (the definition's `tools`/`model` apply and
its body is appended to the teammate's prompt; `skills`/`mcpServers` are NOT
applied on the teammate path).

## 8. Claude Agent SDK

> "The Agent SDK gives you the same tools, agent loop, and context management that
> power Claude Code, programmable in Python and TypeScript."

- **Python package**: `claude-agent-sdk` (`pip install claude-agent-sdk`,
  requires Python **3.10+**). Entry point: `query(...)` with `ClaudeAgentOptions`.
- **TypeScript package**: `@anthropic-ai/claude-agent-sdk`
  (`npm install @anthropic-ai/claude-agent-sdk`). Entry point: `query({...})`
  with `options`. Bundles a native Claude Code binary.
- **Subagents in the SDK**: pass an `agents` map of `AgentDefinition`
  (`description`, `prompt`, `tools`) and include `"Agent"` in `allowed_tools` to
  auto-approve delegation. Messages from a subagent carry `parent_tool_use_id`.
- **Sessions**: capture `session_id` from the `init` system message; resume with
  `resume=session_id` to continue with full context. Fork mode is honored via the
  SDK as well (`CLAUDE_CODE_FORK_SUBAGENT`).
- **MCP / hooks / permissions** mirror Claude Code. Loads `.claude/` config by
  default; restrict with `setting_sources` (Python) / `settingSources` (TS).

Minimal Python subagent-orchestration shape (from the docs):

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Use the code-reviewer agent to review this codebase",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Agent"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="Expert code reviewer for quality and security reviews.",
                    prompt="Analyze code quality and suggest improvements.",
                    tools=["Read", "Glob", "Grep"],
                )
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

> Note: from June 15, 2026, Agent SDK and `claude -p` usage on subscription plans
> draws from a separate monthly Agent SDK credit. Branding rule: do not present a
> product as "Claude Code"; "Claude Agent" / "Powered by Claude" are allowed.

## 9. Key limits and gotchas

- **Subagents cannot spawn other subagents** (no nesting). Chain from the main
  conversation or use Skills for nested delegation.
- **Each subagent starts with a fresh, isolated context** (except forks). It does
  not see conversation history, prior skill invocations, or files already read —
  the delegation prompt must carry needed context.
- **Returned results re-enter the main context** — many verbose subagents can
  still flood it; have them "report only" the summary you need.
- **Agent teams**: one team at a time, no nested teams, lead is fixed for the
  team's lifetime, no session resumption for in-process teammates, split panes
  need tmux or iTerm2 (not Ghostty / VS Code terminal / Windows Terminal).
- **Match degrees of freedom to fragility**: prose prompts for open exploration;
  explicit ordered steps + a stop condition for fragile multi-step sequences.
