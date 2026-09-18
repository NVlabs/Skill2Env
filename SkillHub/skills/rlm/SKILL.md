---
name: rlm
description: "Process large codebases (>100 files) using the Recursive Language Model pattern. Orchestrates parallel sub-agents to map-reduce across files without context rot. Use when: analyzing large repositories; auditing security or auth across many files; finding patterns across 50+ files; processing large log files or data dumps"
license: MIT
metadata:
  author: ClawFu
  version: 2.1.0
  mcp-server: "@clawfu/mcp-skills"
---

# Recursive Language Model (RLM)

**"Context is an external resource, not a local variable."**

You are the **Root Node**. Your job is NOT to read code directly, but to orchestrate sub-agents that read code for you.

## The RLM Loop

### Phase 1: Index & Filter
Identify relevant files without loading them into context.

```bash
# Find candidate files
grep -rl "pattern" src/ --include="*.ts"
find . -name "*.py" -newer last_check
```

### Phase 2: Parallel Map
Split work into atomic units, spawn parallel agents.

- Launch **3-5+ agents** in parallel for broad tasks
- Give each agent **ONE specific file or chunk**
- Each agent returns a structured summary

Example spawn:
```
Agent 1: "Read src/api/routes.ts. List all endpoints with their auth decorators."
Agent 2: "Read src/api/users.ts. List all endpoints with their auth decorators."
...
```

### Phase 3: Reduce & Synthesize
Collect all agent outputs, find patterns, compile into a coherent answer.

If incomplete, recurse: run a second RLM pass on the specific gaps.

## Critical Rules

1. **NEVER** read more than 3-5 files into your main context
2. **ALWAYS** use parallel agents when file count > 5
3. **Write Python scripts** for state tracking across 50+ files — let the script scan and summarize
4. If parallel agents are unavailable, fall back to iterative Python scripting

## Example: "Find all API endpoints, check for Auth"

**Wrong** (monolithic): Read each file sequentially → context fills up, reasoning degrades.

**RLM Way**:
1. `grep -l "@Controller" src/**/*.ts` → 20 files
2. Spawn 20 agents, each extracts endpoints + auth status
3. Collect outputs, compile table, identify missing auth

## Output Format

Return a structured summary:
- **Findings table** (file, pattern, status)
- **Gaps identified** (what needs deeper investigation)
- **Confidence level** (how complete the scan was)

## Skill Boundaries

**Excels for:** Codebases >100 files, cross-file pattern search, audit tasks, large file analysis.

**Not ideal for:** Small projects (<50 files), single file analysis, file modification tasks.
