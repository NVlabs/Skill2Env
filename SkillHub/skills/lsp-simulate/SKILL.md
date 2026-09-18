---
name: lsp-simulate
description: Speculative code editing session — simulate changes in memory before touching disk. Use when planning edits that might break things, exploring refactors across multiple files, or verifying an edit is safe before applying.
user-invocable: true
allowed-tools: mcp__lsp__start_lsp mcp__lsp__create_simulation_session mcp__lsp__simulate_edit mcp__lsp__simulate_chain mcp__lsp__evaluate_session mcp__lsp__commit_session mcp__lsp__discard_session mcp__lsp__destroy_session mcp__lsp__preview_edit
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata: {}
---

> Requires the agent-lsp MCP server.

# lsp-simulate

Simulate code edits in memory before writing to disk. The LSP server applies
your changes to an in-memory overlay, runs diagnostics, and reports whether
the edit is safe — without touching any files.

## Prerequisites

LSP must be running for the target workspace. If not yet initialized, call
`start_lsp` before any simulation tool.

```
mcp__lsp__start_lsp(root_dir: "/your/workspace")
```

Auto-init note: agent-lsp supports workspace auto-inference from file paths.
Explicit `start_lsp` is only needed when switching workspace roots.

## Quick Start (single edit)

For a single what-if check, use `preview_edit` — it creates a session,
applies the edit, evaluates, and destroys the session in one call:

```
mcp__lsp__preview_edit(
  workspace_root: "/your/workspace",
  language: "go",
  file_path: "/abs/path/to/file.go",
  start_line: 42, start_column: 1,
  end_line: 42, end_column: 20,
  new_text: "replacement text"
)
```

Result:

```
{ net_delta: 0 }   -- safe to apply
{ net_delta: 2 }   -- 2 new errors introduced; do NOT apply
```

`net_delta: 0` means no new errors were introduced. Positive values mean
errors were introduced — inspect `errors_introduced` before deciding.

## Full Session Workflow (multiple edits)

Use a full session when applying several edits that build on each other, or
when you want to inspect the patch before deciding whether to write to disk.

**Step 1 — Create a simulation session**

```
mcp__lsp__create_simulation_session(
  workspace_root: "/your/workspace",
  language: "go"
)
→ { session_id: "abc123" }
```

**Step 2 — Apply edits in-memory**

Call `simulate_edit` one or more times. All edits are in-memory only.
Positions are 1-indexed (matching editor line numbers and `cat -n` output).

```
mcp__lsp__simulate_edit(
  session_id: "abc123",
  file_path: "/abs/path/to/file.go",
  start_line: 10, start_column: 1,
  end_line: 10, end_column: 30,
  new_text: "func NewClient(cfg Config) *Client {"
)
→ { session_id: "abc123", edit_applied: true, version_after: 1 }
```

Repeat for additional edits as needed.

**Step 3 — Evaluate the session**

```
mcp__lsp__evaluate_session(
  session_id: "abc123",
  scope: "file"
)
→ {
    net_delta: 0,
    confidence: "high",
    errors_introduced: [],
    errors_resolved: [],
    edit_risk_score: 0.0,
    affected_symbols: []
  }
```

`scope: "file"` (default) is faster and returns `confidence: "high"`.
`scope: "workspace"` catches cross-file type errors but returns
`confidence: "eventual"` (results may not be fully settled).

**Step 4 — Decision gate**

If `net_delta == 0`, proceed to commit. Otherwise, discard:

```
mcp__lsp__discard_session(session_id: "abc123")
```

**Step 5 — Commit the session**

```
-- Preview patch only (no disk write):
mcp__lsp__commit_session(session_id: "abc123", apply: false)

-- Write to disk:
mcp__lsp__commit_session(session_id: "abc123", apply: true)
```

**Step 6 — Destroy the session (always)**

```
mcp__lsp__destroy_session(session_id: "abc123")
```

Always call `destroy_session` after commit or discard to release server
resources. See [Cleanup Rule](#cleanup-rule) below.

## Chained Mutations (simulate_chain)

Use `simulate_chain` when you have a sequence of edits and want to find
how far through the sequence is safe to apply. Unlike multiple `simulate_edit`
calls, `simulate_chain` evaluates diagnostics after each step.

```
mcp__lsp__simulate_chain(
  session_id: "abc123",
  edits: [
    { file_path: "/abs/file.go", start_line: 5, start_column: 1,
      end_line: 5, end_column: 40, new_text: "type Foo struct { Bar int }" },
    { file_path: "/abs/file.go", start_line: 20, start_column: 1,
      end_line: 20, end_column: 10, new_text: "f.Bar" },
    { file_path: "/abs/other.go", start_line: 8, start_column: 1,
      end_line: 8, end_column: 10, new_text: "x.Bar" }
  ]
)
→ {
    steps: [
      { step: 1, net_delta: 0, errors_introduced: [] },
      { step: 2, net_delta: 0, errors_introduced: [] },
      { step: 3, net_delta: 1, errors_introduced: [...] }
    ],
    safe_to_apply_through_step: 2,
    cumulative_delta: 1
  }
```

`safe_to_apply_through_step: 2` means steps 1 and 2 are safe; step 3
introduced errors. Commit the session after reviewing to apply steps 1–2,
or discard to cancel everything.

## Decision Guide

| net_delta | confidence  | Action                                                             |
|-----------|-------------|-------------------------------------------------------------------|
| 0         | high        | Safe. Commit or apply.                                            |
| 0         | eventual    | Likely safe. Workspace scope — re-evaluate if risk matters.       |
| > 0       | any         | Do NOT apply. Inspect `errors_introduced`. Discard session.       |
| > 0       | partial     | Timeout. Results incomplete. Discard and retry with smaller scope.|

## Session States

| State     | Meaning                                                       | Next step              |
|-----------|---------------------------------------------------------------|------------------------|
| created   | Session initialized, no edits yet                             | simulate_edit          |
| mutated   | One or more edits applied in-memory                           | evaluate_session       |
| evaluated | Diagnostics collected                                         | commit or discard      |
| committed | Patch returned (and optionally written to disk)               | destroy_session        |
| discarded | In-memory edits reverted, no disk write                       | destroy_session        |
| dirty     | Revert failed or version mismatch; session is inconsistent    | destroy_session only   |

A session in `dirty` state cannot be recovered — call `destroy_session` immediately.

## Cleanup Rule

Always call `destroy_session` after finishing a session, even on error paths:

```
-- After commit:
mcp__lsp__commit_session(session_id: "abc123", apply: true)
mcp__lsp__destroy_session(session_id: "abc123")

-- After discard:
mcp__lsp__discard_session(session_id: "abc123")
mcp__lsp__destroy_session(session_id: "abc123")
```

**MCP server restart:** Sessions are ephemeral — they live in server memory
only. If the MCP server restarts, all session IDs become invalid. To preserve
work across a restart, call `commit_session(apply: false)` first to get a
portable patch, then re-apply it after the server restarts.

See [references/patterns.md](references/patterns.md) for detailed field
descriptions and confidence interpretation.
