# naming

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for naming products, SaaS tools, brands, and projects.

Metaphor-driven naming that produces memorable, meaningful names — and avoids AI slop.

## What this does

When invoked, this skill guides Claude through a structured naming process:

1. **Naming brief** — establish what the product does, who it's for, what it should feel like
2. **Metaphor exploration** — map conceptual territories before brainstorming names
3. **Candidate generation** — produce names grounded in metaphor, not thesaurus surfing
4. **Filtering** — kill AI slop and anti-patterns
5. **Evaluation** — score and compare finalists with a weighted rubric
6. **Availability checking** — verify domains, handles, and package names
7. **Decision** — present top candidates with origin stories and trade-offs

## Install

### As a project skill (this project only)

Clone or copy the repo contents into your project's `.claude/skills/naming/` directory:

```bash
# From your project root
mkdir -p .claude/skills
git clone https://github.com/glacierphonk/naming.git .claude/skills/naming
```

### As a personal skill (all projects)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/glacierphonk/naming.git ~/.claude/skills/naming
```

## Usage

In Claude Code:

```text
/naming
```

Then describe what you need a name for. Claude will walk you through the full process.

You can also reference the skill naturally in conversation — describe your naming challenge and Claude will pull in the relevant reference files.

### Quick start

You don't need to read any of the reference files before using the skill. Just:

1. Type `/naming`
2. Describe what you're building in one sentence
3. Claude handles the rest — it loads the right references at each step

The 7-step process and 14 reference files are the depth layer. For a quick naming session, Claude compresses the process automatically. The reference files exist so you can dive deeper when needed.

## Files

| File | Purpose |
| ------ | ------- |
| `SKILL.md` | Entry point — process overview and navigation |
| `principles.md` | Core naming principles (metaphor, real words, compounds, length) |
| `phonosemantics.md` | Sound-meaning connections — how sounds convey attributes |
| `anti-patterns.md` | AI name slop, fatal flaws, red flags checklist |
| `metaphor-mapping.md` | How to explore metaphor territories + starter maps |
| `cultural-references.md` | When mythology/literature/science references work vs. fail |
| `brand-architecture.md` | Naming within brand families and product lines |
| `availability.md` | Platform checking workflow and domain landscape |
| `case-studies.md` | Real product name origins and analysis |
| `evaluation.md` | Scoring rubric, comparison framework, decision checklist |
| `language-rules.md` | Working with foreign words — pronunciation, diacritics, transliteration, exoticism trap |
| `scripts/check-availability.sh` | Bundled availability checker for domains, npm, GitHub, PyPI, Telegram, etc. |
| `languages/INDEX.md` | Language-specific naming guides — see [index](languages/INDEX.md) for available languages (Polish, Portuguese, and more) |
| `industries/INDEX.md` | Industry-specific naming guides — see [index](industries/INDEX.md) for available industries |

New language and industry files welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for templates and required sections.

## Philosophy

**Names are compressed stories, not labels.** The best names plant a concrete image that unfolds into understanding — what the product does, what it feels like, where it comes from.

This skill is opinionated:

- **Metaphor over thesaurus.** Don't search for synonyms of your product's category. Explore what else in the world works like your product.
- **Real words over invented words.** Real-word brand names have ~68.8% recall vs ~38.1% for invented names. The brain follows the path of least resistance.
- **Story over sound.** A name with a great origin story and average sound will outperform a name with perfect phonetics and no story.
- **Kill AI slop.** Suffixes like -ly, -ify, -able, meaningless portmanteaus, and thesaurus extraction produce polished-but-interchangeable names. This skill actively filters them out.

## How the skill uses context

- **Always loaded:** Skill name and description (~2% of context budget)
- **Loaded on invoke:** SKILL.md (~180 lines, the process overview)
- **Loaded on demand:** Reference files load only when Claude reaches the relevant step. A simple naming task might only load 2-3 files; a thorough session loads 5-6
- **Never auto-loaded:** Language files, case-studies.md — only when explicitly relevant

Contributors: keep reference files focused. A 500-line file is fine; a 2,000-line file wastes context on content that may not be relevant.

## Development

### Linting

PRs are checked by [markdownlint](https://github.com/DavidAnson/markdownlint) and [lychee](https://github.com/lycheeverse/lychee) (link checker) via GitHub Actions.

Common lint rules to watch:
- **MD040** — fenced code blocks need a language tag (use `text` for plain text, `bash` for shell, `markdown` for markdown examples)
- **MD001** — heading levels must increment by one (`##` → `###`, not `##` → `####`)
- **MD037** — no spaces inside emphasis markers. Use `` `___` `` (code backticks) for placeholders, not `___` (which looks like emphasis)

Run locally before pushing:

```bash
npx markdownlint-cli2 '**/*.md'
```

### Branch protection

`main` is protected — all changes go through pull requests. Direct pushes are blocked.

## Contributing

PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for conventions, file structure, and how to add language files or case studies.

## License

[MIT](LICENSE)
