---
name: harness:certify
description: "Use when the user wants to verify that the evolved agent's score is stable and reliable. Runs evaluation multiple times and reports mean ± std."
allowed-tools: [Read, Bash, Glob]
---

# /harness:certify

Verify score stability by running evaluation multiple times and reporting statistical confidence.

## Resolve Tool Path

```bash
TOOLS="${EVOLVER_TOOLS:-$([ -d ".evolver/tools" ] && echo ".evolver/tools" || echo "$HOME/.evolver/tools")}"
EVOLVER_PY="${EVOLVER_PY:-$([ -f "$HOME/.evolver/venv/bin/python" ] && echo "$HOME/.evolver/venv/bin/python" || echo "python3")}"
```

## What To Do

Read `.evolver.json` to get the best experiment and dataset.

Run evaluation 3 times on the current code (not a worktree — the best code is already merged):

```bash
for i in 1 2 3; do
    $EVOLVER_PY $TOOLS/run_eval.py \
        --config .evolver.json \
        --worktree-path "." \
        --experiment-prefix "certify-run-$i"
done
```

After all 3 runs complete, read results and compute statistics:

```bash
$EVOLVER_PY $TOOLS/read_results.py --experiments "certify-run-1-{suffix},certify-run-2-{suffix},certify-run-3-{suffix}" --config .evolver.json --format summary
```

Calculate mean and standard deviation from the 3 combined_scores.

## Report

```
CERTIFICATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Runs:  3
Mean:  {mean:.3f}
Std:   {std:.3f}
Range: {min:.3f} — {max:.3f}

Verdict: {STABLE|UNSTABLE}
```

**STABLE** (std < 0.05): Score is reliable. The agent performs consistently.

**MARGINAL** (0.05 <= std < 0.10): Score varies moderately. Consider adding rubrics to reduce judge variance.

**UNSTABLE** (std >= 0.10): Score is unreliable. The LLM judge interprets criteria differently across runs. Add few-shot examples or tighter rubrics.

## After Certification

If STABLE: suggest `/harness:deploy` to finalize.
If UNSTABLE: suggest adding rubrics to dataset examples, or running `/harness:evolve` with `heavy` mode for more thorough evaluation.
