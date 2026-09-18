# Testing Plugin Authoring Skill

**Purpose**: Validate that plugin-authoring instructions produce working plugins and that guidance is unambiguous.

## When to Use

Test this skill when:
- Adding new instructions to plugin-authoring
- Observing agents make repeated mistakes
- Users report confusion about instructions
- Updating schemas or templates

## Testing Approach

Unlike discipline-enforcing skills (TDD, verification), plugin-authoring is a **reference skill**. Testing focuses on:

| Focus Area | Question |
|------------|----------|
| **Clarity** | Are instructions unambiguous? |
| **Completeness** | Do instructions cover the happy path? |
| **Error recovery** | Can agents debug when something goes wrong? |
| **Discoverability** | Can agents find relevant information quickly? |

## Test Scenarios

### Scenario 1: New Plugin Creation (Happy Path)

```markdown
TASK: Create a new plugin called "my-test-plugin" with:
- One command: "greet" that says hello
- Validate and test it locally

TRACK:
- Did agent use /plugin-development:init?
- Did agent put plugin.json in .claude-plugin/ (not components)?
- Did agent validate before testing?
- Did agent create dev marketplace correctly?
```

**Expected behavior**: Agent follows the "Creating a New Plugin" workflow exactly.

### Scenario 2: Common Mistake Recovery

```markdown
TASK: You created a plugin but /plugin-name:command doesn't appear.
Debug and fix it.

TRACK:
- Did agent check plugin.json location first?
- Did agent check component directories exist at plugin root?
- Did agent run /plugin-development:validate?
- Did agent check if commands have .md extension?
```

**Expected behavior**: Agent follows troubleshooting checklist systematically.

### Scenario 3: Hook Script Configuration

```markdown
TASK: Add a PostToolUse hook that runs a formatting script after Write/Edit.

TRACK:
- Did agent use ${CLAUDE_PLUGIN_ROOT} for paths?
- Did agent make script executable (chmod +x)?
- Did agent set appropriate timeout?
- Did agent use correct matcher pattern?
```

**Expected behavior**: Agent produces working hook with portable paths.

### Scenario 4: Skill Creation

```markdown
TASK: Add a skill called "code-quality" to your plugin that provides
guidance on code review.

TRACK:
- Did agent create skills/code-quality/SKILL.md structure?
- Did agent use kebab-case matching directory name?
- Did agent include both name and description in frontmatter?
- Did agent keep SKILL.md under 500 lines?
```

**Expected behavior**: Agent follows skill template and naming conventions.

### Scenario 5: Marketplace Publishing

```markdown
TASK: Add your plugin to a marketplace for distribution.

TRACK:
- Did agent create marketplace.json in .claude-plugin/?
- Did agent match plugin name between marketplace and plugin.json?
- Did agent use relative source paths?
- Did agent test with /plugin marketplace add?
```

**Expected behavior**: Agent follows marketplace schema correctly.

## Pressure Scenarios

Test under realistic constraints:

### Time Pressure
```markdown
TASK: Quick - add a validation hook to block writes to .env files.
You have 2 minutes before the meeting.

TRACK:
- Did agent still use ${CLAUDE_PLUGIN_ROOT}?
- Did agent still validate?
- Did shortcuts cause failures?
```

### Iteration Pressure
```markdown
TASK: The hook isn't working. This is the 4th attempt.
Just make it work somehow.

TRACK:
- Did agent resort to absolute paths?
- Did agent skip validation steps?
- Did agent read error messages carefully?
```

## Validation Checklist

After testing, verify:

```
□ Agent found correct information in skill
□ Agent followed workflow without confusion
□ Resulting plugin validates cleanly
□ Agent knew how to debug when stuck
□ Agent used provided commands (/plugin-development:*)
□ Agent didn't need external documentation
```

## Common Failure Modes

| Failure | Indicates | Fix |
|---------|-----------|-----|
| Agent puts components in .claude-plugin/ | Warning not prominent enough | Strengthen warning, add to red flags |
| Agent adds commands field with standard path | Anti-pattern not visible | Add to main SKILL.md anti-patterns |
| Agent uses relative paths in hooks | ${CLAUDE_PLUGIN_ROOT} instruction unclear | Add explicit example, add consequence |
| Agent skips validation | Validation not framed as required | Add authority language, consequences |
| Agent uses wrong skill name format | Naming rules buried | Surface rules earlier in workflow |
| Agent creates deeply nested skill refs | Progressive disclosure not explained | Add warning about nesting depth |

## Iteration Process

1. **Run scenario** without skill loaded → Document baseline behavior
2. **Run scenario** with skill loaded → Compare to baseline
3. **Identify gaps** → Where did instructions fail?
4. **Update skill** → Add clarifications, examples, warnings
5. **Re-test** → Verify improvement
6. **Capture rationalizations** → Add to Common Mistakes if agent found workaround

## Meta-Testing

After an agent makes a mistake despite having the skill:

```markdown
You read the plugin-authoring skill and still [made mistake X].

How could that skill have been written differently to make it
crystal clear that [correct approach] was required?
```

**Three possible responses:**

1. **"The skill WAS clear, I chose to ignore it"**
   - Need stronger authority language
   - Add to Red Flags section

2. **"The skill should have said X"**
   - Documentation gap
   - Add their suggestion

3. **"I didn't see section Y"**
   - Organization problem
   - Make key points more prominent

## Success Criteria

**Skill is effective when:**
- Agent creates valid plugin on first attempt
- Agent finds troubleshooting info without external help
- Agent uses provided commands and workflows
- Agent doesn't rationalize shortcuts under pressure

**Skill needs work when:**
- Agent makes mistakes the skill should prevent
- Agent asks questions answered in the skill
- Agent uses patterns explicitly marked as anti-patterns
- Agent skips validation despite warnings
