---
name: dev:validate
description: "Use when the user wants to validate the plugin, check integrity, verify cross-references, or before a release. Also use when the user says 'validate', 'check plugin', or 'verify'."
allowed-tools: [Read, Bash, Glob, Grep]
---

# /dev:validate

Check plugin integrity: skill/agent frontmatter, cross-references, Python tool syntax, version sync, hook script executability.

## Checks

### 1. Version Sync

```bash
PKG_V=$(python3 -c "import json; print(json.load(open('package.json'))['version'])")
PLUGIN_V=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
if [ "$PKG_V" = "$PLUGIN_V" ]; then
    echo "OK: versions match ($PKG_V)"
else
    echo "FAIL: package.json=$PKG_V, plugin.json=$PLUGIN_V"
fi
```

### 2. Skill Frontmatter

For each `skills/*/SKILL.md`:
- Must have `name:` in frontmatter
- Must have `description:` in frontmatter
- Must have `allowed-tools:` in frontmatter

```bash
for f in skills/*/SKILL.md; do
    NAME=$(grep -m1 "^name:" "$f" | cut -d: -f2- | xargs)
    DESC=$(grep -m1 "^description:" "$f")
    TOOLS=$(grep -m1 "^allowed-tools:" "$f")
    if [ -z "$NAME" ] || [ -z "$DESC" ] || [ -z "$TOOLS" ]; then
        echo "FAIL: $f missing frontmatter fields"
    else
        echo "OK: $f ($NAME)"
    fi
done
```

### 3. Agent Frontmatter

For each `agents/*.md`:
- Must have `name:` in frontmatter
- Must have `description:` in frontmatter
- Must have `tools:` in frontmatter
- Must have `color:` in frontmatter

```bash
for f in agents/*.md; do
    NAME=$(grep -m1 "^name:" "$f" | cut -d: -f2- | xargs)
    COLOR=$(grep -m1 "^color:" "$f" | cut -d: -f2- | xargs)
    if [ -z "$NAME" ] || [ -z "$COLOR" ]; then
        echo "FAIL: $f missing name or color"
    else
        echo "OK: $f ($NAME, $COLOR)"
    fi
done
```

### 4. Agent Cross-References

Check that every `subagent_type:` referenced in skills exists as an agent file:

```bash
for AGENT in $(grep -roh 'subagent_type: "[^"]*"' skills/ | sed 's/subagent_type: "//;s/"//' | sort -u); do
    if [ ! -f "agents/$AGENT.md" ]; then
        echo "FAIL: subagent_type '$AGENT' referenced in skills but agents/$AGENT.md not found"
    else
        echo "OK: $AGENT agent exists"
    fi
done
```

### 5. Python Tool Syntax

```bash
ERRORS=0
for f in tools/*.py; do
    python3 -c "import ast; ast.parse(open('$f').read())" 2>&1
    if [ $? -ne 0 ]; then
        echo "FAIL: $f has syntax errors"
        ERRORS=$((ERRORS+1))
    else
        echo "OK: $f"
    fi
done
echo "Python tools: $ERRORS errors"
```

### 6. Hook Script

```bash
if [ -f "hooks/session-start.sh" ]; then
    if [ -x "hooks/session-start.sh" ]; then
        echo "OK: hooks/session-start.sh is executable"
    else
        echo "FAIL: hooks/session-start.sh not executable"
    fi
    if [ -f "hooks/hooks.json" ]; then
        python3 -c "import json; json.load(open('hooks/hooks.json'))" 2>&1
        if [ $? -eq 0 ]; then echo "OK: hooks.json valid JSON"; else echo "FAIL: hooks.json invalid"; fi
    fi
else
    echo "WARN: no hooks/session-start.sh"
fi
```

### 7. CLAUDE.md Accuracy

Check that tool count and agent count in CLAUDE.md match reality:

```bash
TOOL_COUNT=$(ls tools/*.py 2>/dev/null | wc -l)
AGENT_COUNT=$(ls agents/*.md 2>/dev/null | wc -l)
echo "Tools: $TOOL_COUNT Python files"
echo "Agents: $AGENT_COUNT agent definitions"
```

## Report

Print a summary:
```
Plugin Validation:
  Versions: {OK/FAIL}
  Skills: {N} checked, {N} passed
  Agents: {N} checked, {N} passed
  Cross-refs: {N} checked, {N} passed
  Python tools: {N} checked, {N} syntax errors
  Hooks: {OK/FAIL}

Result: {PASS/FAIL}
```
