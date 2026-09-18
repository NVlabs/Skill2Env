---
name: lsp-architecture
description: Generate a structural architecture overview of a codebase: languages, package map, entry points, dependency graph, and hotspots. One call for the big picture.
argument-hint: "[workspace-root-path]"
user-invocable: true
allowed-tools: mcp__lsp__start_lsp mcp__lsp__list_symbols mcp__lsp__blast_radius mcp__lsp__detect_lsp_servers mcp__lsp__find_symbol
license: MIT
compatibility: Requires the agent-lsp MCP server (github.com/blackwell-systems/agent-lsp)
metadata:
  required-capabilities: documentSymbolProvider
  optional-capabilities: workspaceSymbolProvider referencesProvider
---

> Requires the agent-lsp MCP server.

# lsp-architecture

Generate a structural architecture overview of any codebase: language
distribution, package hierarchy, entry points, dependency flow, and hotspot
files. One invocation for the big picture.

Read-only; does not modify any files.

**Invocation:** User provides the workspace root path (e.g.
`"/home/user/myproject"`). If omitted, use the current working directory.

---

## Depth Controls (hard limits)

These limits are strict constraints. Never exceed them:

- Package enumeration: **cap at 30 packages**
- Hotspot analysis: **cap at 10 files**
- Workspace symbol queries: **cap at 5 queries**
- Do NOT recurse into `vendor/`, `node_modules/`, `.git/`, or other dependency directories

---

## Step 0 — Initialize

If LSP is not yet running, start it with the workspace root:

```
mcp__lsp__start_lsp({
  "workspace_root": "<workspace-root>"
})
```

Then detect which language servers are available:

```
mcp__lsp__detect_lsp_servers({
  "workspace_root": "<workspace-root>"
})
→ returns: list of detected servers with language names and file patterns
```

Record the available languages and their file globs. This determines which
queries to run in later steps.

---

## Step 1 — Language Detection

Scan the workspace to determine language distribution. Use file extension
counts from the detected servers and supplement with a filesystem scan
(via Glob tool) to count files per language.

For each detected language, report:
- Language name
- File count
- Estimated lines of code (sample 3-5 representative files and extrapolate)

Skip files in `vendor/`, `node_modules/`, `.git/`, `dist/`, `build/`, and
other common dependency or output directories.

---

## Step 2 — Package Structure

Use `find_symbol` with broad queries to discover the package and
module hierarchy. Tailor queries by language:

**Go:**
```
mcp__lsp__find_symbol({
  "query": "",
  "symbol_kind_filter": "Package"
})
```

Also query for top-level types and functions to fill in package-level detail:

```
mcp__lsp__find_symbol({
  "query": "",
  "symbol_kind_filter": "Function"
})
```

**Python:**
```
mcp__lsp__find_symbol({
  "query": "",
  "symbol_kind_filter": "Class"
})
```

**TypeScript/JavaScript:**
```
mcp__lsp__find_symbol({
  "query": "",
  "symbol_kind_filter": "Function"
})
```

From the returned symbols, extract the directory paths and build a tree of
the package hierarchy. Group symbols by their containing directory. For each
package/directory, note:
- Path relative to workspace root
- Brief description (inferred from symbol names and directory name)
- Approximate symbol count

**Cap at 30 packages.** If more than 30 directories contain symbols, keep only
the top 30 by symbol count and note that others were omitted.

**Cap workspace symbol queries at 5 total** across all of Step 2.

---

## Step 3 — Entry Points

Use `find_symbol` to search for common entry point patterns:

```
mcp__lsp__find_symbol({
  "query": "main"
})
```

Also search for other common entry point names (use a single additional query
if needed): `"Run"`, `"Serve"`, `"Handler"`, `"App"`, `"Main"`.

Identify and categorize:
- **CLI entrypoints:** `main` functions, `Run` or `Execute` commands
- **HTTP handlers:** `Handler`, `Serve`, `ListenAndServe` patterns
- **Test suites:** top-level test files (note count only, do not list individually)

List each entry point with `file:line`.

---

## Step 4 — Hotspot Analysis

Identify the files with the highest symbol density (most exports), then
measure their blast radius.

### 4a — Find candidate files

From the symbols discovered in Step 2, count exported symbols per file.
Select the **top 10 files** by exported symbol count.

### 4b — Measure blast radius

For each candidate file, call `blast_radius`:

```
mcp__lsp__blast_radius({
  "changed_files": ["<absolute-path-to-file>"],
  "include_transitive": false
})
→ returns: affected_symbols, test_callers, non_test_callers
```

This tool uses a persistent cache, so repeated calls on the same file are
instant.

### 4c — Rank hotspots

Rank files by total `non_test_callers` count (descending). Files with the
most non-test callers are the architectural hotspots: changing them has the
widest blast radius.

---

## Step 5 — Output

Produce the architecture report in this format:

```
## Architecture Overview: <project-name>

### Languages
- Go: 150 files (~15K lines)
- TypeScript: 30 files (~3K lines)

### Package Map
cmd/agent-lsp/     (entrypoint, CLI routing)
internal/lsp/      (LSP client, process management)
internal/tools/    (MCP tool handlers)
internal/session/  (speculative execution sessions)
...

### Entry Points
- cmd/agent-lsp/main.go:55 (main)
- cmd/agent-lsp/server.go:276 (Run)

### Hotspots (most referenced files)
1. internal/lsp/client.go: 150+ callers across 30 files
2. internal/tools/helpers.go: 80 callers across 20 files
...

### Dependency Flow
cmd/ -> internal/tools/ -> internal/lsp/ -> (gopls subprocess)
         |-> internal/session/ -> internal/lsp/
```

### Report sections

**Languages:** One line per language with file count and estimated LOC.

**Package Map:** Directory tree with a parenthetical description of each
package's role. Cap at 30 entries.

**Entry Points:** Each with `file:line` and a parenthetical label (e.g.
`(main)`, `(HTTP handler)`, `(CLI command)`).

**Hotspots:** Ranked list of the most-referenced files. For each, show the
total non-test caller count and the number of distinct files containing
callers.

**Dependency Flow:** A simple ASCII arrow diagram showing how the top-level
packages depend on each other. Infer this from the hotspot caller data and
package structure. Keep it concise: show the primary flow paths, not every
edge.

---

## Example

```
Goal: architecture overview of /home/user/agent-lsp

Step 0 — Initialize
  start_lsp: workspace_root="/home/user/agent-lsp"
  detect_lsp_servers:
  → Go (gopls): *.go
  → detected 1 language server

Step 1 — Language Detection
  Glob: **/*.go (excluding vendor/) → 85 files
  Sample 5 files, average 180 lines → estimate ~15K total lines
  → Go: 85 files (~15K lines)

Step 2 — Package Structure
  find_symbol: query="", symbol_kind_filter="Package"
  → 12 packages found

  find_symbol: query="", symbol_kind_filter="Function"
  → 240 functions across 12 packages

  Package map:
    cmd/agent-lsp/       (entrypoint, CLI routing, 15 symbols)
    internal/lsp/        (LSP client lifecycle, 45 symbols)
    internal/tools/      (MCP tool handlers, 60 symbols)
    internal/session/    (speculative execution, 25 symbols)
    internal/protocol/   (LSP protocol types, 30 symbols)
    skills/              (embedded skill definitions, 5 symbols)

Step 3 — Entry Points
  find_symbol: query="main"
  → cmd/agent-lsp/main.go:55 main()

  find_symbol: query="Run"
  → cmd/agent-lsp/server.go:276 Run()
  → cmd/agent-lsp/daemon.go:40 RunDaemon()

  Entry points:
  - cmd/agent-lsp/main.go:55 (main)
  - cmd/agent-lsp/server.go:276 (Run, server lifecycle)
  - cmd/agent-lsp/daemon.go:40 (RunDaemon, background mode)

Step 4 — Hotspot Analysis
  Top files by symbol count:
    1. internal/lsp/client.go (22 exported symbols)
    2. internal/tools/helpers.go (18 exported symbols)
    3. internal/protocol/types.go (15 exported symbols)

  blast_radius on each:
    internal/lsp/client.go → 150 non-test callers across 30 files
    internal/tools/helpers.go → 80 non-test callers across 20 files
    internal/protocol/types.go → 60 non-test callers across 15 files

Step 5 — Output

## Architecture Overview: agent-lsp

### Languages
- Go: 85 files (~15K lines)

### Package Map
cmd/agent-lsp/       (entrypoint, CLI routing)
internal/lsp/        (LSP client, process management)
internal/tools/      (MCP tool handlers)
internal/session/    (speculative execution sessions)
internal/protocol/   (LSP protocol types)
skills/              (embedded skill definitions)

### Entry Points
- cmd/agent-lsp/main.go:55 (main)
- cmd/agent-lsp/server.go:276 (Run)
- cmd/agent-lsp/daemon.go:40 (RunDaemon)

### Hotspots (most referenced files)
1. internal/lsp/client.go: 150 callers across 30 files
2. internal/tools/helpers.go: 80 callers across 20 files
3. internal/protocol/types.go: 60 callers across 15 files

### Dependency Flow
cmd/agent-lsp/ -> internal/tools/ -> internal/lsp/ -> (gopls subprocess)
                    |-> internal/session/ -> internal/lsp/
                    |-> internal/protocol/
```
