# Agent memory integration

After a wiki is bootstrapped, add a short stanza to the project's agent-memory file so the AI agent knows about the wiki in future sessions without being re-told. Without this, the agent will often answer from training data instead of reading the wiki, and knowledge stops compounding.

## Which file to use

The memory-file convention varies by agent. Use this table to pick the right one:

| Agent | Memory file | Notes |
|---|---|---|
| Claude Code | `CLAUDE.md` | Project root; Claude walks up to the git root searching for it. |
| Codex (OpenAI) | `AGENTS.md` | Standard `agents.md` convention. |
| Cursor | `AGENTS.md` (or `.cursor/rules/*.mdc`) | AGENTS.md is simpler and portable across other agents. |
| OpenCode | `AGENTS.md` | Also reads `CLAUDE.md`, so either works. |
| Gemini CLI | `GEMINI.md` | Gemini-specific filename. |
| Pi Agent | `AGENTS.md` | Follows the `agents.md` standard. |
| OpenClaw | `AGENTS.md` | Follows the `agents.md` standard. |

If the user runs multiple agents in the same project, prefer `AGENTS.md` as the canonical file and symlink `CLAUDE.md` to it (or duplicate the content). Claude Code will read a symlinked `CLAUDE.md` without issue.

If the user is unsure which agent they use most, default to `AGENTS.md` — it works for the widest set of runtimes.

## The canonical stanza

Append this stanza to the chosen memory file. Keep it tight. Memory files live in the agent's context on every session, so every line has a cost.

```markdown
## LLM Wiki

This project maintains an LLM-curated wiki at `wiki/` following Andrej Karpathy's "LLM Wiki" pattern (https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Before answering questions that rely on knowledge accumulated in this project, read `wiki/index.md` (or the relevant shard under `wiki/indexes/` if the wiki has been sharded) and use its one-line summaries to find the pages you need. Cite with `[[wikilinks]]`. If the index does not surface good candidates, fall back to `wiki_search.py` from the `llm-wiki` skill for BM25-ranked retrieval.

To add a new source, follow the `llm-wiki` skill's ingest workflow: decide placement under `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, or `wiki/synthesis/`; identify touched pages and make surgical `str_replace` updates rather than rewrites; update the index; append a one-line entry to `wiki/log.md`.

Scaling discipline: atomic pages (400-line soft cap, 800-line hard cap), sharded indexes past ~150 pages or 300 index lines, required YAML frontmatter on every page, `[[wikilinks]]` for every cross-reference.

Full conventions live in `wiki/SCHEMA.md`. Treat it as authoritative when it disagrees with this summary.
```

Adjust the path references if the user bootstrapped the wiki into a non-default directory (the schema file and the stanza should always agree with each other).

## The bootstrap conversation

At init time, after the directory structure is in place and the schema walkthrough is done, propose the stanza. Don't silently append. The user owns their memory file.

A good script:

1. Ask the user which agent(s) they run in this project. If they say "Claude Code", target `CLAUDE.md`. If they say "Cursor" or "Codex" or "OpenCode" or "multiple", target `AGENTS.md`. If they say "Gemini CLI", target `GEMINI.md`. If they're unsure, target `AGENTS.md` and mention that Claude Code can still read it via a symlink.
2. Check whether that file already exists.
   - If **not**, offer to create it with just the LLM Wiki stanza as the content.
   - If **yes**, show the proposed stanza and ask whether to append it.
3. Ask whether the user would prefer a shorter stanza. Some users keep their memory files to under 50 lines on principle; the canonical stanza above is already tight, but offer a three-line alternative:

```markdown
## LLM Wiki

This project has an LLM-curated wiki at `wiki/`. Read `wiki/index.md` before answering research questions. Full conventions in `wiki/SCHEMA.md`. Ingest and query workflows live in the `llm-wiki` skill.
```

4. Whatever the user picks, write it, then confirm.

## When the wiki changes shape

The stanza is a pointer, not a playbook. Most evolution of the wiki (new page types, new tags, domain conventions) should happen in `SCHEMA.md`, not in the memory file. The memory file only changes when:

- The wiki moves to a non-standard directory (update the path).
- The wiki shards its index (mention `wiki/indexes/` specifically so the agent starts there).
- The wiki is deprecated (remove the stanza; don't leave a dead pointer).

If you edit the memory file on the user's behalf during a lint or scaling-migration operation, show them the diff and get consent. Silent rewrites of agent-memory files are the fastest way to break user trust.

## Multiple projects, multiple wikis

Each wiki lives inside its own project. The memory-file stanza references `wiki/` as a relative path, so a user with ten projects gets ten independent wikis and ten independent stanzas. Do not write this stanza into a global memory file (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, etc.) — it would apply to projects that have no wiki and create confusing agent behaviour.
