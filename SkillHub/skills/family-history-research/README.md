# Family History Research Planning Skill for Claude

Claude Skill to provide assistance with planning family history and genealogy research projects.

## ⚠️ Privacy and Responsible AI Use

**Protect Private Information:** When using AI tools for genealogy research, take reasonable measures to safeguard private and sensitive information about living individuals and recently deceased persons.

### Best Practices:
- **DO NOT** share personal identifying information (Social Security Numbers, birth certificates, addresses of living people, medical records, or other sensitive data) with AI systems
- **DO NOT** upload documents containing information about living individuals or recently deceased persons (generally within the last 75-100 years)
- **DO** remove or redact private information before sharing research materials with AI
- **DO** focus on historical records and deceased individuals when using AI assistance
- **DO** verify all AI-generated information with primary sources
- **DO** comply with applicable privacy laws, terms of service, and ethical genealogical standards

This skill follows the principles of the [Coalition for Responsible AI in Genealogy (CRAIGEN)](https://craigen.org), which promotes accuracy, privacy protection, disclosure, education, and compliance in genealogical AI use.

**Remember:** AI systems may retain and learn from information you provide. Always prioritize privacy and use discretion when sharing genealogical data.

## Overview

This skill provides Claude with specialized knowledge and workflows for family history and genealogy research following the Genealogical Proof Standard (GPS) and Evidence Explained citation methodology.

## Skill Structure

```
genealogy-research-skill/
├── SKILL.md                              # Main skill file (loaded when skill triggers)
├── references/                           # Reference documentation (loaded as needed)
│   ├── citation-templates.md            # Citation formats for 14+ source types
│   ├── evidence-evaluation.md           # Conflict resolution frameworks
│   ├── gps-guidelines.md                # Genealogical Proof Standard details
│   └── research-strategies.md           # Advanced research methodologies
└── assets/                               # Templates for output documents
    └── templates/
        ├── research-plan-template.md    # Simplified research project planning (practical)
        ├── research-plan-guidance.md    # Detailed guidance and best practices
        ├── citation-template.md         # Citation library entry
        ├── evidence-analysis-template.md # Evidence analysis report
        └── research-log-template.md     # Research session documentation
```

## What This Skill Does

### 1. Research Planning
Guides users through creating structured family history research plans with:
- Specific research questions
- Source identification
- Search strategies
- GPS framework integration
- Timeline and milestones

**Templates:**
- `research-plan-template.md` - Simplified, practical template for day-to-day research work
- `research-plan-guidance.md` - Comprehensive guidance with examples, checklists, and best practices

### 2. Citation Creation
Generates properly formatted genealogical citations for:
- Census records
- Vital records (birth, marriage, death)
- Church records
- Land and probate records
- Military records
- Immigration records
- Newspapers
- Online databases
- Published books and manuscripts

### 3. Evidence Analysis
Systematically analyzes conflicting genealogical evidence:
- Individual source evaluation
- Reliability assessment
- Conflict identification
- Resolution frameworks
- Preponderance of evidence analysis
- GPS compliance checking
- Proof argument construction

### 4. Research Documentation
Creates professional research logs documenting:
- Sources searched (positive and negative results)
- Search strategies
- Findings and discoveries
- Evidence quality assessment
- Next steps

## When Claude Uses This Skill

Claude automatically loads this skill when users:
- Ask about family history or genealogy research
- Mention family history, genealogy or ancestry
- Need help with genealogical citations
- Have conflicting information from multiple sources
- Ask about research planning methods or strategies
- Reference census records, vital records, or historical documents
- Need help analyzing evidence quality

## Key Features

### Professional Standards
- Built on Genealogical Proof Standard (GPS)
- Evidence Explained citation methodology
- Board for Certification of Genealogists (BCG) standards

### Progressive Disclosure
- Core instructions in SKILL.md (~4k words)
- Detailed reference material loaded as needed
- Templates available for document creation

### Comprehensive Coverage
- 14+ citation templates
- Detailed conflict resolution frameworks
- Advanced research strategies
- Complete GPS guidelines

## Installation

### Quick Start (Experienced Users)

1. Download the latest release from [Releases](https://github.com/emaynard/genealogy-research-skill/releases)
2. **Claude.ai users**: Enable Skills in Settings > Capabilities, then upload the skill folder
3. **Claude Code users**: Extract the ZIP file
4. **Claude Code users**: Move the `family-history-planning` folder to `~/.claude/skills/`
5. Start using: Just ask Claude about family history research!

### Detailed Installation Instructions

#### Prerequisites

**For Claude.ai:**
- Claude Pro, Max, Team, or Enterprise plan
- Skills feature enabled (Settings > Capabilities)
- Code execution enabled (Settings > Capabilities)

**For Claude Code:**
- Claude Code installed
- Access to your home directory

#### Step-by-Step Installation

**Option 1: Install on Claude.ai**

1. **Download the Skill**
   - Go to the [Releases page](https://github.com/emaynard/genealogy-research-skill/releases)
   - Download the latest `family-history-planning-vX.X.X.zip` file
   - Extract the ZIP file to a location on your computer

2. **Enable Skills in Claude**
   - Open [Claude.ai](https://claude.ai)
   - Click on your profile/settings (bottom left)
   - Navigate to **Settings > Capabilities**
   - Toggle **Skills** to ON
   - Toggle **Code execution** to ON (required for Skills)

3. **Upload the Skill**
   - In Claude.ai, go to **Settings > Skills**
   - Click **"Add Skill"** or **"Upload Skill"**
   - Select the downloaded `family-history-planning-vX.X.X.zip` ZIP file   
   - The skill will be uploaded and enabled automatically
   - Your skill will appear in your Skills list and can be toggled on or off

4. **Verify Installation**
   - Start a new conversation with Claude
   - Ask: "What version of the family history skill are you using?"
   - Claude should recognize and load the skill

**Option 2: Install on Claude Code**

1. **Download the Skill**
   - Go to the [Releases page](https://github.com/emaynard/genealogy-research-skill/releases)
   - Download the latest `family-history-planning-vX.X.X.zip` file
   - Extract the ZIP file

2. **Locate Your Skills Directory**
   - Open your terminal
   - Navigate to your home directory: `cd ~`
   - Create the skills directory if it doesn't exist:
     ```bash
     mkdir -p ~/.claude/skills
     ```

3. **Install the Skill**
   - Move the extracted skill folder to the skills directory:
     ```bash
     mv /path/to/extracted/family-history-planning ~/.claude/skills/
     ```
   - Or copy if you want to keep the original:
     ```bash
     cp -r /path/to/extracted/family-history-planning ~/.claude/skills/
     ```

4. **Verify Installation**
   - Your skills directory structure should look like:
     ```
     ~/.claude/skills/
     └── family-history-planning/
         ├── SKILL.md
         ├── references/
         └── assets/
     ```
   - Restart Claude Code if it's currently running
   - Ask Claude: "What version of the family history skill are you using?"

#### Troubleshooting

**Skill not loading?**
- Ensure Skills are enabled in Settings > Capabilities
- Verify code execution is enabled
- Check that the skill folder contains SKILL.md with proper frontmatter
- Try restarting Claude or Claude Code

**Permission issues (Claude Code)?**
- Check folder permissions: `ls -la ~/.claude/skills/`
- Ensure you have read access: `chmod -R 755 ~/.claude/skills/family-history-planning/`

**Skill not recognized?**
- Verify the skill name matches the frontmatter in SKILL.md
- Check that all required files are present (SKILL.md, references/, assets/)

## How to Use This Skill

### As a User
Simply ask Claude for help with family history research:
- "Help me plan research on my great-grandfather"
- "Create a citation for this census record"
- "I have conflicting birth dates - help me figure out which is right"
- "How do I systematically research this ancestor?"

Claude will automatically detect your request and load the skill—no need to manually invoke it.

### As Claude
When family history or genealogy research is detected:
1. Load SKILL.md for procedural guidance
2. Load specific reference files as needed:
   - `references/citation-templates.md` for citation help
   - `references/evidence-evaluation.md` for conflict resolution
   - `references/gps-guidelines.md` for GPS compliance
   - `references/research-strategies.md` for advanced techniques
3. Use templates from `assets/templates/` to create output documents
4. Follow workflows systematically
5. Apply professional standards throughout


## Professional Standards Compliance

This skill ensures research follows:

### Genealogical Proof Standard (GPS)
- Reasonably exhaustive research
- Complete and accurate citations
- Analysis and correlation
- Conflict resolution
- Soundly reasoned conclusions

### Evidence Explained
- Proper citation format
- Original vs. derivative distinction
- Complete source documentation

### BCG Standards
- Professional genealogical methodology
- Ethical research practices
- Peer-reviewable work

## Output Documents

Claude can create four types of genealogy documents using this skill:

1. **Research Plans** - Strategic planning documents
2. **Citations** - Properly formatted source citations
3. **Evidence Analysis Reports** - Systematic conflict resolution
4. **Research Logs** - Session documentation

All outputs follow professional genealogical standards and are ready for:
- Personal research management
- Professional genealogy work
- Publication
- Sharing with other researchers
- GPS compliance review

## Version

**Version:** 1.0
**Created:** October 2025
**Source:** BMAD Method genealogy-assistant module
**Converted by:** Claude with skill-creator guidance

## License

This skill was created from a genealogy research project. Please respect professional genealogical standards and properly attribute sources when using the workflows and methodologies contained herein.

## Support

For questions about:
- **Genealogy methodology**: Refer to professional resources (BCG, NGS, Evidence Explained)
- **Skill usage**: Ask Claude for help - the skill is designed to guide you
- **Professional standards**: See references/ files for detailed guidelines

---

**Ready to start your family history research? Just ask Claude!**
