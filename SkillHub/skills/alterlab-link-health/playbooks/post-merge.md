# Playbook — Post-merge cleanup (4-agent)

Use when: the link-health PR is CI-green and mergeable, but some human-decision items from the audit deserve finalization before merge. Converts deferred decisions into verified substitutions, follow-up issues, and durable documentation.

## Shape

```
pre-flight  →  4 parallel subagents  →  patch any cross-agent references  →  single cleanup commit  →  push  →  wait push-CI  →  squash-merge --delete-branch
```

## Pre-flight

1. `cd` to the cloned repo. Confirm current branch.
2. `gh pr view <N>` — confirm state is OPEN, mergeable CLEAN.
3. `git pull --ff-only` — local must be current with origin.
4. `gh auth status` — token must have `repo` scope.

## Parallel agent dispatch (4 subagents)

| Agent | Name | Responsibility |
|-------|------|----------------|
| **agent-A** | `<dead-sub>-substitution` | Take one or more specific dead URLs that were left excluded in Tier 4 and verify alternative targets. Example: replace `github.com/<dead-repo>` with the verified-alive PyPI/npm landing page. **Must `curl -sSI`** or `gh api` before committing. Remove the corresponding exclusion block from `.lycheeignore`. |
| **agent-B** | `followup-issues` | Open GitHub issues for out-of-scope observations from the audit. Each issue needs a title, labels (create missing labels first via `gh label create`), and a body referencing the audit PR. Typical issues: upstream migration tracking, schema drift, deferred substitutions. |
| **agent-C** | `link-debt-doc` | Create `.github/KNOWN_LINK_DEBT.md` populated from the actual `.lycheeignore` plus audit artefacts. Five categories (see `references/known-debt-template.md`). Link any temporary exclusions to agent-B's issue numbers. |
| **agent-D** | `guardrail-in-skill` | Locate the installed link-health skill on the user's system (`~/.claude/skills/`, plugin caches, or an AlterLab skill repo). If present, append the Tier 3 guardrail rule to a `## Guardrails` section. If absent, report and skip. |

All four run in parallel. Agents B, C, D don't modify the skills repo (agent-B opens issues, agent-C writes `.github/KNOWN_LINK_DEBT.md`, agent-D touches an unrelated skill file or reports absent).

## Patch cross-agent references

Agent-C's output references agent-B's issue numbers (tracking-issue cells for the "Upstream migrations" category). After both land:

- Replace the placeholder `<ISSUE_NUMBER_*>` strings in `KNOWN_LINK_DEBT.md` with the real issue numbers from agent-B's output.

## Single cleanup commit

One commit covering everything agents A + C produced (agent-B's work is on the GitHub issue tracker, agent-D's work is in another repo/skill dir):

```
chore(links): finalize <dead-sub> substitution, document link debt
```

Body paragraphs should cover:
- The verified substitution (what was excluded, what replaced it, how you verified).
- The new `KNOWN_LINK_DEBT.md` and what it tracks.
- References to the follow-up issues agent-B opened.

## Push and merge

```bash
git push origin <branch>
# Wait for push-triggered CI (e.g. Validate Skills) to complete.
# Check Links does not auto-trigger on push — only schedule + workflow_dispatch.
gh pr merge <N> --squash --delete-branch
```

Squash-merge gives a clean single commit on `main` with the full audit narrative in the title and the expanded 7+1-commit detail in the squash-merge description (which GitHub pre-populates from the PR body).

## Verify

- `git fetch && git log origin/main --oneline -2` — confirm the merge commit is on main.
- `gh api repos/<owner>/<repo>/branches/<branch>` should return 404 (branch deleted).
- Check `KNOWN_LINK_DEBT.md` exists on `main` and its issue-number placeholders resolved.

## Sanity checks that tend to fail in this playbook

- **Labels don't exist.** `gh issue create --label <x>` fails if the label isn't in the repo. Agent-B should always `gh label list` first and create missing labels.
- **Substitute URL turns out to be archived.** The substitute was 200 when you probed, but if the repo is archived, the URL is still "alive" yet no longer maintained. Prefer `gh api repos/<owner>/<name>` and check `"archived": false`.
- **`.lycheeignore` removal without `KNOWN_LINK_DEBT.md` removal.** If agent-A removes an exclusion, agent-C must not list it under "Dead substitutions." Run a consistency grep before committing.
