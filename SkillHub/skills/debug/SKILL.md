---
name: debug
description: Troubleshoot and debug issues. Use when the user reports an error, a test failure, unexpected behavior, or asks to investigate why something isn't working.
allowed-tools: Bash, Read, Grep, Glob
---

# Debug

Help diagnose and troubleshoot the described issue or the most recent error.

## Steps

1. **Understand the problem**
   - Read any error messages or stack traces mentioned
   - Ask clarifying questions if the problem description is vague
   - Check recent git changes that might have caused the issue: `git diff HEAD~3`

2. **Reproduce**
   - If there's a failing test, run it to see the exact error
   - If it's a runtime issue, try to reproduce with minimal steps

3. **Investigate**
   - Find the relevant source files using the stack trace or error message
   - Trace the code path that leads to the error
   - Check for common issues:
     - Typos in variable or function names
     - Wrong types or missing type conversions
     - Missing imports or dependencies
     - Race conditions or async issues
     - Environment differences (missing env vars, wrong paths)
     - Recent changes that broke assumptions

4. **Form a hypothesis and verify**
   - State what you think the root cause is
   - Find evidence in the code that supports or refutes it
   - If needed, add targeted logging to narrow down the issue

5. **Report findings**
   - Root cause explanation (why it broke, not just what broke)
   - Suggested fix with specific code changes
   - How to prevent similar issues in the future

Do NOT make changes unless explicitly asked — diagnose and explain first. The user should decide whether and how to fix it.

$ARGUMENTS
