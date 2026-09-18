---
name: agent-name
description: What this agent specializes in and when to invoke it (third person). Include "PROACTIVELY" for auto-delegation.
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: default
skills: skill1, skill2
---

<!--
Docs: https://code.claude.com/docs/en/sub-agents
NOTE: 'capabilities' is deprecated - use 'tools' instead.
      Agents use short model names (sonnet/opus/haiku/inherit), not full IDs.
-->

# Agent Name

[Brief introduction to the agent's purpose and specialization]

## What This Agent Does

[Detailed description of the agent's responsibilities]

## Capabilities

1. **Capability 1**: [Description]
2. **Capability 2**: [Description]
3. **Capability 3**: [Description]

## When to Use This Agent

Invoke this agent when:
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

## How It Proceeds

[Step-by-step workflow the agent follows]

1. **Analyze**: [What it reads/examines]
2. **Evaluate**: [How it assesses the situation]
3. **Report**: [What it returns to the main conversation]

## Output Format

[What kind of report or recommendations the agent provides]

Example:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (nice to have)
- Summary of findings

## Tool Access

[What tools this agent has access to and why]

## Notes

[Any limitations, constraints, or important considerations]
