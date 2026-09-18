# PICT Test Designer - Claude Skill

A Claude skill for designing comprehensive test cases using PICT (Pairwise Independent Combinatorial Testing). This skill enables systematic test case design with minimal test cases while maintaining high coverage through pairwise combinatorial testing.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude](https://img.shields.io/badge/Claude-Skill-blue.svg)](https://claude.ai)

## 🎯 What is PICT?

PICT (Pairwise Independent Combinatorial Testing) is a combinatorial testing tool developed by Microsoft. It generates test cases that efficiently cover all pairwise combinations of parameters while drastically reducing the total number of tests compared to exhaustive testing.

**Example:** Testing a system with 8 parameters and 3-5 values each:
- Exhaustive testing: **25,920 test cases**
- PICT pairwise testing: **~30 test cases** (99.88% reduction!)

## 🚀 Features

- **Automated Test Case Generation**: Converts requirements into structured PICT models
- **Constraint-Based Testing**: Applies business rules to eliminate invalid combinations
- **Expected Output Generation**: Automatically determines expected results for each test case
- **Comprehensive Coverage**: Ensures all pairwise parameter interactions are tested
- **Multiple Domains**: Works for software functions, APIs, web forms, configurations, and more

## 📋 Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installing in Claude Code CLI](#installing-in-claude-code-cli)
  - [Installing in Claude Code Desktop](#installing-in-claude-code-desktop)
- [Quick Start](#quick-start)
- [Example: ATM System Testing](#example-atm-system-testing)
- [How It Works](#how-it-works)
- [Use Cases](#use-cases)
- [Credits](#credits)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Installation

### Prerequisites

- Claude Code CLI or Claude Code Desktop
- (Optional) Python 3.7+ with `pypict` for advanced usage

### Installation Methods

Claude Code skills can be installed via the plugin marketplace or manually by placing them in the `.claude/skills/` directory.

### Method 1: Install via Claude Code Plugin Marketplace (Easiest) 🌟

Install directly through Claude Code's plugin system:

```bash
# Add the marketplace
/plugin marketplace add omkamal/pypict-claude-skill

# Install the plugin
/plugin install pict-test-designer@pypict-claude-skill
```

This automatically installs the skill and keeps it updated. The skill will be available across all your projects.

### Method 2: Install from GitHub (Manual)

**For Personal Use (All Projects):**

```bash
# Clone the repository to your personal skills directory
git clone https://github.com/omkamal/pypict-claude-skill.git ~/.claude/skills/pict-test-designer

# Restart Claude Code to load the skill
# The skill will now be available in all your projects
```

**For Project-Specific Use:**

```bash
# From your project directory
git clone https://github.com/omkamal/pypict-claude-skill.git .claude/skills/pict-test-designer

# Add to .gitignore if you don't want to commit it
echo ".claude/skills/" >> .gitignore

# Or commit it to share with your team
git add .claude/skills/pict-test-designer
git commit -m "Add PICT test designer skill"
```

### Method 3: Install via Git Submodule (Team Sharing)

If you want to share this skill with your team via version control:

```bash
# From your project directory
git submodule add https://github.com/omkamal/pypict-claude-skill.git .claude/skills/pict-test-designer
git commit -m "Add PICT test designer skill as submodule"

# Team members clone with:
git clone --recurse-submodules <your-repo-url>

# Or if already cloned:
git submodule update --init --recursive
```

### Method 4: Download Minimal Package from Releases

Download the pre-packaged minimal installation from [GitHub Releases](https://github.com/omkamal/pypict-claude-skill/releases):

```bash
# Download the latest minimal package from releases
wget https://github.com/omkamal/pypict-claude-skill/releases/latest/download/pict-test-designer-minimal.zip

# Extract and install for personal use
unzip pict-test-designer-minimal.zip
mv pict-test-designer-minimal ~/.claude/skills/pict-test-designer

# Or for project-specific use
unzip pict-test-designer-minimal.zip
mv pict-test-designer-minimal .claude/skills/pict-test-designer
```

**What's included:** SKILL.md, LICENSE, references/ (syntax and examples)
**What's excluded:** Full examples, helper scripts, extended documentation
**Size:** ~9 KB | **Latest Version:** [See Releases](https://github.com/omkamal/pypict-claude-skill/releases)

### Method 5: Download Full Repository

1. **Download the repository** as a ZIP from GitHub
2. **Extract to the skills directory**:

```bash
# For personal use (all projects)
unzip pypict-claude-skill-main.zip
mv pypict-claude-skill-main ~/.claude/skills/pict-test-designer

# For project-specific use
unzip pypict-claude-skill-main.zip
mv pypict-claude-skill-main .claude/skills/pict-test-designer
```

### Verify Installation

After installation, restart Claude Code. The skill will load automatically when relevant. You can verify by asking Claude:

```
Do you have access to the pict-test-designer skill?
```

Or simply start using it:

```
Design test cases for a login function with username, password, and remember me checkbox.
```

## 🚀 Quick Start

Once installed, you can use the skill in Claude by simply asking:

```
Design test cases for a login function with username, password, and remember me checkbox.
```

Claude will:
1. Analyze the requirements
2. Identify parameters and values
3. Generate a PICT model with constraints
4. Create test cases with expected outputs
5. Present results in a formatted table

## 📊 Example: ATM System Testing

This repository includes a complete real-world example of testing an ATM system. See the [examples](examples/) directory for:

- **[ATM Specification](examples/atm-specification.md)**: Complete ATM system specification with 11 sections covering hardware, software, security, and functional requirements
- **[ATM Test Plan](examples/atm-test-plan.md)**: Comprehensive test plan generated using PICT methodology with 31 test cases (reduced from 25,920 possible combinations)

### ATM Example Summary

**System Parameters:**
- Transaction Types (5): Withdrawal, Deposit, Balance Inquiry, Transfer, PIN Change
- Card Types (3): EMV Chip, Magnetic Stripe, Invalid
- PIN Status (4): Valid, Invalid attempts 1-3
- Account Types (3): Checking, Savings, Both
- Transaction Amounts (4): Within limits, at max, exceeds transaction, exceeds daily
- Cash Availability (3): Sufficient, Insufficient, Empty
- Network Status (3): Primary, Backup, Disconnected
- Card Condition (3): Good, Damaged, Expired

**Test Results:**
- Total possible combinations: **25,920**
- PICT test cases generated: **31**
- **Reduction: 99.88%**
- Coverage: All pairwise (2-way) interactions
- Test execution time: Reduced from weeks to hours

### Running the ATM Example

```bash
# In Claude Code
Ask: "Use the pict-test-designer skill to analyze the ATM specification 
in examples/atm-specification.md and generate test cases"
```

## 🔍 How It Works

### 1. Requirements Analysis

Claude analyzes your requirements to identify:
- **Parameters**: Input variables, configuration options, environmental factors
- **Values**: Possible values using equivalence partitioning
- **Constraints**: Business rules and dependencies
- **Expected Outcomes**: What should happen for different combinations

### 2. PICT Model Generation

Creates a structured model:

```
# Parameters
Browser: Chrome, Firefox, Safari
OS: Windows, MacOS, Linux
Memory: 4GB, 8GB, 16GB

# Constraints
IF [OS] = "MacOS" THEN [Browser] <> "IE";
IF [Memory] = "4GB" THEN [OS] <> "MacOS";
```

### 3. Test Case Generation

Generates minimal test cases covering all pairwise combinations:

| Test # | Browser | OS | Memory | Expected Output |
|--------|---------|----|---------|-----------------------------|
| 1 | Chrome | Windows | 4GB | Success |
| 2 | Firefox | MacOS | 8GB | Success |
| 3 | Safari | Linux | 16GB | Success |
| ... | ... | ... | ... | ... |

### 4. Expected Output Determination

For each test case, Claude determines the expected outcome based on:
- Business requirements
- Code logic
- Valid/invalid combinations

## 🎯 Use Cases

### Software Testing
- Function testing with multiple parameters
- API endpoint testing
- Database query testing
- Algorithm validation

### Configuration Testing
- System configuration combinations
- Feature flag testing
- Environment setup validation
- Browser compatibility testing

### Web Application Testing
- Form validation
- User authentication flows
- E-commerce checkout processes
- Shopping cart functionality

### Mobile Testing
- Device and OS combinations
- Screen size and orientation
- Network conditions
- App permissions

### Hardware Testing
- Device compatibility
- Interface testing
- Protocol validation
- Performance under different conditions

## 📚 Documentation

- **[SKILL.md](SKILL.md)**: Complete skill documentation with workflow and best practices
- **[PICT Syntax Reference](references/pict_syntax.md)**: Complete syntax guide (to be created)
- **[Examples](references/examples.md)**: Real-world examples across domains (to be created)
- **[Helper Scripts](scripts/pict_helper.py)**: Python utilities for PICT (to be created)

## 💡 Tips for Best Results

### Good Parameter Names
✅ Use descriptive names: `AuthMethod`, `UserRole`, `PaymentType`
✅ Apply equivalence partitioning: `FileSize: Small, Medium, Large`
✅ Include boundary values: `Age: 0, 17, 18, 65, 66`
✅ Add negative values: `Amount: ~-1, 0, 100, ~999999`

### Writing Constraints
✅ Document rationale: `# Safari only available on MacOS`
✅ Start simple, add incrementally
✅ Test constraints work as expected

### Expected Outputs
✅ Be specific: "Login succeeds, user redirected to dashboard"
❌ Not vague: "Works" or "Success"

## 🙏 Credits

This skill is built upon the excellent work of:

- **[Microsoft PICT](https://github.com/microsoft/pict)**: The original Pairwise Independent Combinatorial Testing tool developed by Microsoft Research
- **[pypict](https://github.com/kmaehashi/pypict)**: Python binding for PICT by Kenichi Maehashi
- **Community Contributors**: All contributors who have helped improve PICT tools

### About PICT

PICT was developed by Jacek Czerwonka at Microsoft Research. It's a powerful combinatorial testing tool that has been used extensively within Microsoft for testing complex systems with multiple interacting parameters.

**References:**
- [PICT: Pairwise Independent Combinatorial Testing](https://github.com/microsoft/pict)
- [Pairwise Testing Methodology](https://www.pairwisetesting.com/)
- [Combinatorial Test Design](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Add examples or documentation**
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Areas for Contribution

- Additional real-world examples
- Enhanced constraint patterns
- Support for more testing domains
- Improved documentation
- Bug fixes and improvements

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The underlying PICT tool by Microsoft is also licensed under the MIT License.

## 🔗 Links

- **Claude AI**: https://claude.ai
- **Claude Documentation**: https://docs.claude.com
- **Microsoft PICT**: https://github.com/microsoft/pict
- **pypict**: https://github.com/kmaehashi/pypict
- **Online PICT Tools**: 
  - https://pairwise.yuuniworks.com/
  - https://pairwise.teremokgames.com/

## 📧 Support

If you encounter issues or have questions:

1. Check the [examples](examples/) directory for reference
2. Review the [SKILL.md](SKILL.md) documentation
3. Open an issue on GitHub
4. Join discussions in the Issues section

## 🌟 Star This Repository

If you find this skill useful, please star the repository to help others discover it!

---

**Made with ❤️ for the Claude and testing community**

**Powered by Microsoft PICT and pypict**
