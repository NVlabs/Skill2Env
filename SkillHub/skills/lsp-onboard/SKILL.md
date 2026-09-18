---
name: lsp-onboard
description: First-session project onboarding. Explores the project structure, detects build system, test runner, entry points, and key architecture patterns. Produces a structured project profile the agent can reference throughout the session.
argument-hint: "[workspace-root-path]"
user-invocable: true
allowed-tools: mcp__lsp__start_lsp mcp__lsp__detect_lsp_servers mcp__lsp__list_symbols mcp__lsp__find_symbol mcp__lsp__blast_radius mcp__lsp__run_build mcp__lsp__run_tests mcp__lsp__get_diagnostics mcp__lsp__get_editing_context
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: documentSymbolProvider
  optional-capabilities: referencesProvider callHierarchyProvider
---

# lsp-onboard

First-session project onboarding. Run this when connecting to a new project
for the first time. Explores the codebase via LSP tools and produces a
structured project profile: languages, build system, test runner, entry
points, key types, and architecture patterns.

The profile helps the agent make better decisions throughout the session
without re-exploring the same ground. Run once per project; skip on
subsequent sessions unless the project structure has changed significantly.

## When to Use

- First time working in a new codebase
- After major structural changes (new packages, build system migration)
- When the agent seems confused about project conventions

Do NOT run this on every session. It's a one-time exploration.

---

## Step 1: Detect languages and servers

```
mcp__lsp__detect_lsp_servers({ "workspace_dir": "<root>" })
```

Record which languages are present and which servers are available.
This tells you what the project is built with.

## Step 2: Initialize and verify

```
mcp__lsp__start_lsp({ "root_dir": "<root>" })
```

Wait for initialization. Call `list_symbols` on one key file to verify
the workspace is indexed.

## Step 3: Identify entry points

Search for common entry point patterns:

```
mcp__lsp__find_symbol({ "query": "main" })
mcp__lsp__find_symbol({ "query": "Run" })
mcp__lsp__find_symbol({ "query": "Handler" })
```

Record entry points with their file paths. These are where execution starts.

## Step 4: Map the package structure

For each top-level directory that contains source files, call `list_symbols`
on one representative file:

```
mcp__lsp__list_symbols({ "file_path": "<dir>/main.go", "format": "outline" })
```

Build a mental map: which packages exist, what they export, how they relate.
Cap at 10 packages to avoid spending too long.

## Step 5: Detect build and test commands

```
mcp__lsp__run_build({ "workspace_dir": "<root>" })
mcp__lsp__run_tests({ "workspace_dir": "<root>" })
```

Record whether build and tests pass, and what language/toolchain was detected.
Note the test count and any failures.

## Step 6: Identify hotspots

Pick the 3-5 files that appear most central (entry points, shared types,
core logic). For each:

```
mcp__lsp__blast_radius({ "changed_files": ["<file>"] })
```

Files with the most non-test callers are the architectural hotspots.
Changes to these files have the widest blast radius.

## Step 7: Check for diagnostics

```
mcp__lsp__get_diagnostics({ "file_path": "<entry-point>" })
```

Note any pre-existing errors or warnings. This sets the baseline
so the agent knows what was broken before it started.

## Step 8: Produce the project profile

Write a structured summary:

```
## Project Profile: <name>

### Languages
- Go (primary), TypeScript (frontend)

### Build & Test
- Build: `go build ./...` (passes)
- Test: `go test ./...` (142 tests, 0 failures)

### Entry Points
- cmd/server/main.go:15 (main)
- cmd/worker/main.go:22 (main)

### Package Map
- cmd/server/     (HTTP server, routing)
- cmd/worker/     (background job processor)
- internal/api/   (handler layer)
- internal/store/ (database access)
- internal/types/ (shared type definitions)

### Hotspots (most referenced)
1. internal/types/models.go: 85 callers across 12 files
2. internal/store/queries.go: 42 callers across 8 files
3. internal/api/handlers.go: 31 callers across 6 files

### Pre-existing Issues
- 0 errors, 2 warnings (unused imports in test files)

### Conventions Observed
- Error wrapping with fmt.Errorf
- Table-driven tests
- Handler functions return (result, error)
```

This profile is for the agent's reference during the session. It does not
need to be saved to disk; it lives in the conversation context.

---

## Notes

- Cap exploration at 10 packages and 5 hotspot files to keep the
  onboarding under 2 minutes
- If `blast_radius` is slow (large files), skip the hotspot step
  and note "hotspot analysis skipped (large codebase)"
- The profile is advisory; update it mentally as you learn more during
  the session
