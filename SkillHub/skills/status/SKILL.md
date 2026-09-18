---
name: harness:status
description: "Use when the user asks about evolution progress, current scores, best version, how many iterations ran, or whether the loop is stagnating."
allowed-tools: [Read, Bash]
---

# /harness:status

Show current evolution progress.

## What To Do

### Resolve Tool Path

```bash
TOOLS="${EVOLVER_TOOLS:-$([ -d ".evolver/tools" ] && echo ".evolver/tools" || echo "$HOME/.evolver/tools")}"
EVOLVER_PY="${EVOLVER_PY:-$([ -f "$HOME/.evolver/venv/bin/python" ] && echo "$HOME/.evolver/venv/bin/python" || echo "python3")}"
```

### Display Chart

```bash
$EVOLVER_PY $TOOLS/evolution_chart.py --config .evolver.json
```

### Additional Analysis

After displaying the chart:

- Detect stagnation: if last 3 scores within 1% of each other, warn and suggest `/harness:evolve` with architect trigger.
- Detect regression: if current best is lower than a previous best, warn.
- Print LangSmith experiment URL for the best experiment if available.
