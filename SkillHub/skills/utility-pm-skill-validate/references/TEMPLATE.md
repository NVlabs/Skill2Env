# Validation Report: {skill-name}
Date: {YYYY-MM-DD}
Skill version: {version from frontmatter}
Validator version: 1.0.0
Report schema: v1
Result: {PASS | WARN | FAIL}

## Summary

{1-2 sentence overall assessment of the skill's compliance with structural
conventions and quality criteria.}

Errors: {n} | Warnings: {n} | Info: {n}

> Tier 2 findings are heuristic quality assessments and may require human review.

## Structural Checks

{One line per Tier 1 check. Use pipe-delimited format:}

- {STATUS} | structural | {check-id} | {message}

{Include all checks from the Tier 1 table in SKILL.md Step 3.
STATUS is PASS or FAIL.}

## Quality Checks

{One line per Tier 2 check. Use pipe-delimited format:}

- {STATUS} | quality | {check-id} | {message}

{Include all checks from the Tier 2 table in SKILL.md Step 4.
STATUS is PASS, WARN, or INFO. Tier 2 findings capped at WARN unless
objectively grounded (placeholder-leakage can FAIL).}

## Recommendations

{Only include checks that did NOT pass. Each recommendation includes
the check ID, target file path, and a specific action.}

1. {STATUS} | {check-id} | Target: {file-path}
   Action: {what to do to resolve this finding}

{If all checks pass, write: "No issues found."}
