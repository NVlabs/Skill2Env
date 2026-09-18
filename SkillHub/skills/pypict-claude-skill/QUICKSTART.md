# Quick Start Guide

Get started with PICT Test Designer in 5 minutes!

## Installation (Choose One)

### Option 1: Personal Installation (All Projects)

```bash
# Clone to your personal skills directory
git clone https://github.com/omkamal/pypict-claude-skill.git ~/.claude/skills/pict-test-designer

# Restart Claude Code - the skill is now available in all projects
```

### Option 2: Project-Specific Installation

```bash
# From your project directory
git clone https://github.com/omkamal/pypict-claude-skill.git .claude/skills/pict-test-designer

# Restart Claude Code - the skill is available in this project only
```

### Option 3: Manual Download

1. Download ZIP from: `https://github.com/omkamal/pypict-claude-skill`
2. Extract to `~/.claude/skills/pict-test-designer` (personal) or `.claude/skills/pict-test-designer` (project)
3. Restart Claude Code

## Your First Test Plan (3 Steps)

### Step 1: Start Claude Code

Open your terminal or Claude Code Desktop

### Step 2: Describe Your System

Simply tell Claude what you want to test:

```
I need to test a login function with these requirements:
- Users can login with email and password
- Support for 2FA (enabled/disabled)
- "Remember me" checkbox option
- Rate limiting after 3 failed attempts

Can you design test cases using the pict-test-designer skill?
```

### Step 3: Get Your Test Cases!

Claude will automatically:
1. ✅ Analyze your requirements
2. ✅ Identify test parameters and values
3. ✅ Generate a PICT model with constraints
4. ✅ Create optimized test cases
5. ✅ Provide expected outputs

## Example Output

You'll receive:

### 1. PICT Model
```
Email: Valid, Invalid, Empty
Password: Valid, Invalid, Empty
TwoFactorAuth: Enabled, Disabled
RememberMe: Checked, Unchecked
FailedAttempts: 0, 1, 2, 3

IF [FailedAttempts] = "3" THEN [Email] = "Valid";
```

### 2. Test Cases Table

| Test # | Email | Password | 2FA | Remember | Failed | Expected Output |
|--------|-------|----------|-----|----------|--------|-----------------|
| 1 | Valid | Valid | Enabled | Checked | 0 | Success: Login with 2FA prompt |
| 2 | Valid | Invalid | Disabled | Unchecked | 1 | Error: Incorrect password (2 attempts left) |
| ... | ... | ... | ... | ... | ... | ... |

### 3. Summary
- Total combinations: 432
- PICT test cases: 15
- Reduction: 96.5%

## Real-World Examples

### Try the ATM Example

```
Using the pict-test-designer skill, analyze the ATM specification 
in examples/atm-specification.md and show me the test coverage
```

This demonstrates a complex system with:
- 8 parameters
- 25,920 possible combinations
- Only 31 test cases needed!

## Common Use Cases

### Testing a Web Form
```
Design test cases for a registration form with:
- Name (required, max 50 chars)
- Email (required, must be valid format)
- Phone (optional, 10 digits)
- Country (dropdown with 5 options)
- Terms checkbox (required)
```

### Testing an API Endpoint
```
I need to test a REST API endpoint that:
- Accepts GET, POST, PUT, DELETE methods
- Requires authentication (valid token, invalid token, missing token)
- Returns JSON, XML, or error
- Has rate limiting

Design test cases.
```

### Testing System Configuration
```
Test our application deployment with:
- Environment: Dev, Staging, Production
- Database: MySQL, PostgreSQL, SQLite
- Cache: Enabled/Disabled
- SSL: Enabled/Disabled
- Log Level: Debug, Info, Error

With the constraint: Production must not use SQLite or Debug logging
```

## Tips for Best Results

### ✅ Do This
- Describe your requirements clearly
- Mention any business rules or constraints
- Specify what different values mean
- Ask for specific output formats if needed

### ❌ Avoid This
- Too vague: "test my app"
- No context: "make test cases for login"
- Missing constraints: Not mentioning dependencies between parameters

## Next Steps

1. **Try it with your own system** - Start with a simple feature
2. **Review the examples** - Check out the [ATM example](examples/)
3. **Read the full documentation** - See [SKILL.md](SKILL.md)
4. **Customize for your needs** - Adapt parameters and constraints
5. **Share your results** - Consider contributing examples!

## Getting Help

- **Questions?** Open an [issue on GitHub](https://github.com/yourusername/pypict-claude-skill/issues)
- **Examples?** Check the [examples directory](examples/)
- **Documentation?** Read [SKILL.md](SKILL.md) and [README.md](README.md)

## Advanced Usage

### Generate More Test Cases

Once you have the PICT model, you can:

1. **Use online tools**:
   - https://pairwise.yuuniworks.com/
   - https://pairwise.teremokgames.com/

2. **Install PICT locally**:
   ```bash
   # Windows: Download from GitHub
   # https://github.com/microsoft/pict/releases
   
   # Linux/Mac: Use pypict
   pip install pypict
   ```

3. **Modify the model**:
   - Add more parameters
   - Change constraints
   - Adjust values
   - Re-generate test cases

### Export to Test Management Tools

The generated test cases can be:
- Copied to Excel/CSV
- Imported to JIRA, TestRail, Azure Test Plans
- Converted to automated test scripts
- Used in documentation

## Success Story

> "We were testing a configuration-heavy system with hundreds of possible combinations. Using PICT Test Designer, we reduced our test suite from 500+ tests to just 45 tests while maintaining the same coverage. This saved us weeks of testing time!" - QA Team Lead

## What's Next?

- Add this skill to your regular testing workflow
- Try it on different types of systems
- Share examples with your team
- Contribute improvements back to the project

**Happy Testing! 🚀**
