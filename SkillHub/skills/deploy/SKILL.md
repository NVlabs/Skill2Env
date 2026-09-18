---
name: harness:deploy
description: "Use when the user is done evolving and wants to finalize, clean up, tag the result, or push the optimized agent."
allowed-tools: [Read, Write, Bash, Glob, AskUserQuestion]
---

# /harness:deploy

Finalize the evolution results. In v3, the best code is already in the main branch (auto-merged during evolve). Deploy is about cleanup, tagging, and pushing.

## What To Do

```bash
TOOLS="${EVOLVER_TOOLS:-$([ -d ".evolver/tools" ] && echo ".evolver/tools" || echo "$HOME/.evolver/tools")}"
EVOLVER_PY="${EVOLVER_PY:-$([ -f "$HOME/.evolver/venv/bin/python" ] && echo "$HOME/.evolver/venv/bin/python" || echo "python3")}"
```

### 1. Show Results

```bash
python3 -c "
import json
c = json.load(open('.evolver.json'))
baseline = c['history'][0]['score'] if c['history'] else 0
best = c['best_score']
improvement = best - baseline
print(f'Baseline: {baseline:.3f}')
print(f'Best: {best:.3f} (+{improvement:.3f}, {improvement/max(baseline,0.001)*100:.0f}% improvement)')
print(f'Iterations: {c[\"iterations\"]}')
print(f'Experiment: {c[\"best_experiment\"]}')
"
```

Show git diff from before evolution started:
```bash
git log --oneline --since="$(python3 -c "import json; print(json.load(open('.evolver.json'))['created_at'][:10])")" | head -20
```

### 2. Ask What To Do (interactive)

```json
{
  "questions": [{
    "question": "Evolution complete. What would you like to do?",
    "header": "Deploy",
    "multiSelect": false,
    "options": [
      {"label": "Tag and push", "description": "Create a git tag with the score and push to remote"},
      {"label": "Just review", "description": "Show the full diff of all changes made during evolution"},
      {"label": "Clean up only", "description": "Remove temporary files (trace_insights.json, etc.) but don't push"},
      {"label": "Promote learnings", "description": "Add proven evolution insights to CLAUDE.md (permanent knowledge)"}
    ]
  }]
}
```

### 3. Execute

**If "Tag and push"**:
```bash
VERSION=$(python3 -c "import json; c=json.load(open('.evolver.json')); print(f'evolver-v{c[\"iterations\"]}')")
SCORE=$(python3 -c "import json; print(f'{json.load(open(\".evolver.json\"))[\"best_score\"]:.3f}')")
git tag -a "$VERSION" -m "Evolver: score $SCORE"
git push origin main --tags
```

**If "Just review"**:
```bash
git diff HEAD~{iterations} HEAD
```

**If "Clean up only"**:
```bash
rm -f trace_insights.json best_results.json comparison.json production_seed.md production_seed.json
```

**If "Promote learnings"**:
```bash
$EVOLVER_PY $TOOLS/promote_learnings.py --memory evolution_memory.md --target CLAUDE.md --threshold 5 --dry-run
```

Show the dry-run output. If the user approves, run without `--dry-run`.

### 4. Report

- What was done
- LangSmith experiment URL for the best result
- Suggest reviewing the changes before deploying to production
