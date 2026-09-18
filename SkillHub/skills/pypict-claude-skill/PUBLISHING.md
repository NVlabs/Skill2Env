# Publishing Guide

This guide will walk you through publishing the pypict-claude-skill repository to GitHub.

## Prerequisites

Before you begin, make sure you have:
- [ ] A GitHub account
- [ ] Git installed on your computer
- [ ] The pypict-claude-skill directory on your local machine

## Step-by-Step Publishing Process

### Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and log in
2. Click the "+" icon in the top-right corner
3. Select "New repository"
4. Configure your repository:
   - **Repository name:** `pypict-claude-skill`
   - **Description:** "A Claude skill for designing comprehensive test cases using PICT (Pairwise Independent Combinatorial Testing)"
   - **Visibility:** Public (so others can use it)
   - **Initialize:** DO NOT add README, .gitignore, or license (we already have these)
5. Click "Create repository"

### Step 2: Initialize Local Git Repository

Open your terminal and navigate to the pypict-claude-skill directory:

```bash
cd /path/to/pypict-claude-skill

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: PICT Test Designer skill v1.0.0"
```

### Step 3: Connect to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/pypict-claude-skill.git

# Verify remote is set correctly
git remote -v
```

### Step 4: Push to GitHub

```bash
# Push to main branch (or master if using older git)
git branch -M main
git push -u origin main
```

### Step 5: Verify on GitHub

1. Go to your repository: `https://github.com/YOUR_USERNAME/pypict-claude-skill`
2. Verify all files are present:
   - README.md
   - SKILL.md
   - LICENSE
   - examples/
   - .github/
   - And all other files

### Step 6: Configure Repository Settings

#### Enable Issues
1. Go to Settings → General
2. Under "Features", ensure "Issues" is checked

#### Enable Discussions (Optional)
1. Go to Settings → General
2. Under "Features", check "Discussions"
3. This allows users to ask questions and share experiences

#### Set Up Branch Protection (Optional but Recommended)
1. Go to Settings → Branches
2. Add branch protection rule for `main`
3. Recommended settings:
   - Require pull request reviews before merging
   - Require status checks to pass

### Step 7: Create a Release

1. Go to your repository on GitHub
2. Click "Releases" (right sidebar)
3. Click "Create a new release"
4. Configure the release:
   - **Tag:** `v1.0.0`
   - **Release title:** `v1.0.0 - Initial Release`
   - **Description:**
     ```markdown
     ## 🎉 Initial Release
     
     First public release of the PICT Test Designer skill for Claude!
     
     ### Features
     - Complete PICT-based test case generation
     - Comprehensive ATM system example
     - Installation guides for Claude Code CLI and Desktop
     - Full documentation and examples
     
     ### Highlights
     - Reduces test cases by 99%+ while maintaining coverage
     - Easy integration with Claude Code
     - Real-world examples included
     
     ### Credits
     Built on Microsoft PICT and pypict by Kenichi Maehashi
     ```
5. Click "Publish release"

### Step 8: Update README URLs

Now that you know your GitHub username, update the placeholder URLs in README.md:

```bash
# Edit README.md and replace all instances of:
# "yourusername" with your actual GitHub username

# For example, change:
# https://github.com/yourusername/pypict-claude-skill
# to:
# https://github.com/YOUR_ACTUAL_USERNAME/pypict-claude-skill
```

Then commit and push:

```bash
git add README.md
git commit -m "Update URLs with actual GitHub username"
git push origin main
```

### Step 9: Test the Installation

Test that others can install your skill:

#### For Claude Code CLI:
```bash
claude code config add-skill \
  --name pict-test-designer \
  --source github \
  --repo YOUR_USERNAME/pypict-claude-skill
```

#### For Claude Code Desktop:
1. Settings → Skills
2. Add Skill from GitHub
3. URL: `https://github.com/YOUR_USERNAME/pypict-claude-skill`

### Step 10: Share Your Skill!

Now that it's published, share it with:

1. **Social Media**
   - Post on Twitter/X with hashtags #ClaudeAI #Testing #PICT
   - Share on LinkedIn
   - Post in relevant Reddit communities (r/softwaredevelopment, r/QualityAssurance)

2. **Communities**
   - Claude AI Discord
   - Software testing forums
   - QA communities

3. **Your Team**
   - Share with colleagues
   - Add to team documentation
   - Include in onboarding materials

## Maintaining Your Repository

### When Making Updates

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main

# For new releases
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin v1.1.0
```

### Update CHANGELOG.md

Keep track of changes in CHANGELOG.md for each release.

### Respond to Issues and PRs

- Check GitHub regularly for new issues
- Review pull requests promptly
- Thank contributors
- Keep discussions friendly and helpful

## Promoting Your Skill

### 1. Add Topics to Your Repository

On GitHub, add relevant topics:
- claude
- claude-ai
- pict
- testing
- test-automation
- combinatorial-testing
- pairwise-testing
- qa
- quality-assurance

### 2. Create a Blog Post

Write about:
- Why you created this skill
- How it helps with testing
- Real-world use cases
- Tutorial on using it

### 3. Make a Video Tutorial

Create a quick video showing:
- Installation process
- Basic usage
- The ATM example
- Tips and tricks

### 4. Submit to Directories

- Add to awesome lists (awesome-claude, awesome-testing)
- Submit to skill directories
- List on your portfolio

## Getting Help

If you encounter issues:

1. Check [GitHub's documentation](https://docs.github.com)
2. Ask in GitHub Discussions (if enabled)
3. Search for similar issues
4. Ask in Claude AI community

## Congratulations! 🎉

Your skill is now public and ready to help the community!

Next steps:
- Monitor for issues and feedback
- Plan improvements based on user needs
- Consider adding more examples
- Keep documentation up to date

---

**Remember:** You're now maintaining an open-source project. Be patient, be kind, and enjoy helping others improve their testing!
