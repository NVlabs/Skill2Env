---
name: harness:health
description: "Use when the user wants to check dataset quality, diagnose eval issues, or before running evolve. Checks size, difficulty distribution, dead examples, coverage, and splits. Auto-corrects issues found."
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, Agent, AskUserQuestion]
---

# /harness:health

Check eval dataset quality and auto-correct issues. Can be run independently or is invoked by `/harness:evolve` before the iteration loop.

## Prerequisites

`.evolver.json` must exist. If not, tell user to run `/harness:setup`.

## Resolve Tool Path and Python

```bash
TOOLS="${EVOLVER_TOOLS:-$([ -d ".evolver/tools" ] && echo ".evolver/tools" || echo "$HOME/.evolver/tools")}"
EVOLVER_PY="${EVOLVER_PY:-$([ -f "$HOME/.evolver/venv/bin/python" ] && echo "$HOME/.evolver/venv/bin/python" || echo "python3")}"
```

## 1. Run Health Diagnostic

```bash
$EVOLVER_PY $TOOLS/dataset_health.py \
    --config .evolver.json \
    --production-seed production_seed.json \
    --output health_report.json 2>/dev/null
```

Print summary:
```bash
python3 -c "
import json, os
if os.path.exists('health_report.json'):
    r = json.load(open('health_report.json'))
    print(f'Dataset Health: {r[\"health_score\"]}/10 ({r[\"example_count\"]} examples)')
    for issue in r.get('issues', []):
        print(f'  [{issue[\"severity\"]}] {issue[\"message\"]}')
    if not r.get('issues'):
        print('  No issues found.')
"
```

## 2. Auto-Correct Issues

If `health_report.json` has corrections, apply them automatically:

```bash
CORRECTIONS=$(python3 -c "
import json, os
if os.path.exists('health_report.json'):
    r = json.load(open('health_report.json'))
    for c in r.get('corrections', []):
        print(c['action'])
" 2>/dev/null)
```

For each correction:

**If `create_splits`**: Assign 70/30 train/held_out splits:
```bash
$EVOLVER_PY -c "
from langsmith import Client
import json, random
client = Client()
config = json.load(open('.evolver.json'))
examples = list(client.list_examples(dataset_name=config['dataset']))
random.shuffle(examples)
sp = int(len(examples) * 0.7)
for ex in examples[:sp]:
    client.update_example(ex.id, split='train')
for ex in examples[sp:]:
    client.update_example(ex.id, split='held_out')
print(f'Assigned splits: {sp} train, {len(examples)-sp} held_out')
"
```

**If `generate_hard`**: Spawn testgen agent to generate hard examples:
```
Agent(
  subagent_type: "harness-testgen",
  description: "Generate hard examples to rebalance dataset",
  prompt: "The dataset is skewed toward easy examples. Generate {count} HARD examples that the current agent is likely to fail on. Focus on edge cases, adversarial inputs, and complex multi-step queries. Read .evolver.json and production_seed.json for context."
)
```

**If `fill_coverage`**: Spawn testgen agent for missing categories:
```
Agent(
  subagent_type: "harness-testgen",
  description: "Generate examples for missing categories",
  prompt: "The dataset is missing these production categories: {categories}. Generate 5 examples per missing category. Read .evolver.json and production_seed.json for context."
)
```

**If `retire_dead`**: Move dead examples to retired split:
```bash
$EVOLVER_PY -c "
from langsmith import Client
import json
client = Client()
report = json.load(open('health_report.json'))
dead_ids = report.get('dead_examples', {}).get('ids', [])
config = json.load(open('.evolver.json'))
examples = {str(e.id): e for e in client.list_examples(dataset_name=config['dataset'])}
retired = 0
for eid in dead_ids:
    if eid in examples:
        client.update_example(examples[eid].id, split='retired')
        retired += 1
print(f'Retired {retired} dead examples')
"
```

After corrections, log what was done.

## 3. Report

Print final health status. If critical issues remain that couldn't be auto-corrected, warn the user.
