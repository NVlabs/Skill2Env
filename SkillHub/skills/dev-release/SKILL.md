---
name: dev:release
description: "Use when the user wants to release a new version, publish to npm, create a GitHub release, bump version, or tag a release. Also use when the user says 'release', 'publish', 'bump version', 'tag', or 'npm publish'."
argument-hint: "[patch|minor|major]"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---

# /dev:release

Interactive release workflow for harness-evolver. Handles everything: validation, changelog, version bump, git tag, GitHub release, npm publish.

## Step 1: Determine Version Bump

Parse the argument if provided (`patch`, `minor`, `major`). If not provided, ask:

```json
{
  "questions": [
    {
      "question": "Version bump type?",
      "header": "Bump",
      "multiSelect": false,
      "options": [
        {"label": "patch", "description": "Bug fixes, small changes (e.g., 4.0.2 → 4.0.3)"},
        {"label": "minor", "description": "New features, backwards compatible (e.g., 4.0.2 → 4.1.0)"},
        {"label": "major", "description": "Breaking changes (e.g., 4.0.2 → 5.0.0)"}
      ]
    }
  ]
}
```

## Step 2: Read Current State

```bash
# Current version
CURRENT=$(python3 -c "import json; print(json.load(open('package.json'))['version'])")
echo "Current version: $CURRENT"

# Commits since last tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -n "$LAST_TAG" ]; then
    echo "Commits since $LAST_TAG:"
    git log --oneline "$LAST_TAG"..HEAD
else
    echo "No previous tags found"
    git log --oneline -10
fi
```

## Step 3: Compute New Version

Based on the bump type and current version, compute the new version. For example:
- `patch`: 4.0.2 → 4.0.3
- `minor`: 4.0.2 → 4.1.0
- `major`: 4.0.2 → 5.0.0

```bash
python3 -c "
v = '$CURRENT'.split('.')
bump = '$BUMP_TYPE'
if bump == 'major':
    v = [str(int(v[0])+1), '0', '0']
elif bump == 'minor':
    v = [v[0], str(int(v[1])+1), '0']
else:
    v = [v[0], v[1], str(int(v[2])+1)]
print('.'.join(v))
"
```

## Step 4: Generate Changelog Entry

Read the commits since the last tag. Categorize them:
- `feat:` → Added
- `fix:` → Fixed
- `refactor:` → Changed
- `docs:` → (skip unless significant)
- `chore:` → (skip unless version bump)

Write a new `## [NEW_VERSION] - YYYY-MM-DD` section at the top of `CHANGELOG.md` (after the header, before the previous version entry). Follow Keep a Changelog format. Use the commit messages as a starting point but **rewrite them to be user-facing** — explain what changed for the user, not what files were touched.

Show the generated changelog entry to the user before proceeding.

## Step 5: Bump Version

Update version in both files:

```bash
# package.json
python3 -c "
import json
with open('package.json') as f: p = json.load(f)
p['version'] = '$NEW_VERSION'
with open('package.json', 'w') as f: json.dump(p, f, indent=2); f.write('\n')
"

# .claude-plugin/plugin.json
python3 -c "
import json
with open('.claude-plugin/plugin.json') as f: p = json.load(f)
p['version'] = '$NEW_VERSION'
with open('.claude-plugin/plugin.json', 'w') as f: json.dump(p, f, indent=2); f.write('\n')
"
```

## Step 6: Commit, Tag, Push

```bash
git add CHANGELOG.md package.json .claude-plugin/plugin.json
git commit -m "chore: bump version to $NEW_VERSION

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"

git tag -a "v$NEW_VERSION" -m "v$NEW_VERSION"
git push origin main --tags
```

## Step 7: Create GitHub Release

Generate release notes from the changelog entry. Use `gh release create`:

```bash
gh release create "v$NEW_VERSION" \
    --title "v$NEW_VERSION — {short title from changelog}" \
    --notes "{release notes from changelog entry}

Full changelog: https://github.com/raphaelchristi/harness-evolver/blob/main/CHANGELOG.md"
```

## Step 8: Publish to npm

```bash
npm publish
```

Verify the published version:

```bash
npm view harness-evolver version
```

## Step 9: Report

```
Release v{NEW_VERSION} complete:
  - CHANGELOG.md updated
  - package.json + plugin.json bumped
  - Git tag v{NEW_VERSION} created and pushed
  - GitHub release: {release_url}
  - npm: harness-evolver@{NEW_VERSION} published
```
