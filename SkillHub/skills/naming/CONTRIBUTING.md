# Contributing

This project is a collection of markdown reference files that teach an AI assistant how to name products. Contributions are content, not code — you're writing naming guidance, case studies, and linguistic analysis.

## What we're looking for

- **New language files** — naming guides for languages not yet covered (see [Adding a Language File](#adding-a-language-file))
- **Case studies** — real product name origins with verifiable sources
- **Factual corrections** — wrong stats, outdated claims, incorrect origin stories
- **Cross-reference fixes** — files that should link to each other but don't
- **Anti-pattern examples** — real products that demonstrate naming failures
- **Metaphor territory maps** — new product categories for metaphor-mapping.md
- **Phonosemantics research** — academic citations backing sound-meaning claims

Not looking for: subjective opinions without evidence, AI-generated filler, marketing copy.

## How to contribute

**Small fixes** (typos, broken links, one-line corrections): edit directly on GitHub and submit a PR.

**Larger changes** (new sections, new language files, case study batches):

1. Check [open issues](https://github.com/glacierphonk/naming/issues) — many have detailed descriptions of exactly what's needed
2. Comment on the issue to claim it
3. Fork the repo and create a branch (`fix/issue-44-scoring-max`, `add/language-de`)
4. Make your changes following the conventions below
5. Submit a PR referencing the issue (`Closes #44`)

## File structure

```text
SKILL.md                  ← Entry point. Defines the 7-step process.
                             Only change this for process flow updates.

principles.md             ← Foundational naming rules (metaphor, real words, etc.)
phonosemantics.md         ← Sound-meaning associations (English-centric)
anti-patterns.md          ← What kills names (AI slop, fatal flaws)
metaphor-mapping.md       ← Metaphor exploration technique + territory maps
cultural-references.md    ← When mythology/literature/science references work
brand-architecture.md     ← Naming within brand families
language-rules.md         ← Working with foreign words (pronunciation, diacritics, transliteration)
availability.md           ← Platform checking workflow
case-studies.md           ← Real product name origins
evaluation.md             ← Scoring rubric and comparison framework

scripts/
  check-availability.sh   ← Bundled availability checker (domain, npm, GitHub, etc.)

languages/
  pl.md                   ← Polish naming guide
  pt-PT.md                ← European Portuguese naming guide
  pt-BR.md                ← Brazilian Portuguese naming guide
```

Files are loaded on demand during the naming process — not all at once. SKILL.md tells the AI when to load each file.

**When your change in one file affects another**, update the cross-references. For example, adding a new anti-pattern to `anti-patterns.md` that has a real-world example should also add a reference in `case-studies.md`.

## Context budget and file sizes

The skill's reference files are loaded into Claude's context window on demand — each file consumes tokens. Contributors should understand the cost model:

**Loading tiers:**

| Tier | What loads | Context cost |
| ---- | ---------- | ------------ |
| **Always** | Skill name and description (from frontmatter) | ~2% of budget |
| **On invoke** | SKILL.md (~200 lines, process overview) | ~3-4% of budget |
| **On demand** | Reference files, one at a time as Claude reaches the relevant step | ~2-4% each |
| **Never auto-loaded** | Language files, industry files, case-studies.md — only when explicitly relevant | 0% unless needed |

**Typical session costs:**

- **Simple naming** (Steps 1-3-7, skip thorough evaluation): loads 2-3 reference files
- **Full process** (all 7 steps): loads 5-6 reference files
- **Multilingual naming**: adds 1-2 language files on top

**Guidelines for contributors:**

- Keep reference files under 300 lines where possible. A 500-line file is acceptable; a 2,000-line file wastes context on content that may not apply to the current naming task
- When adding content, consider whether it belongs in the file that's loaded early (high visibility) or one loaded later (lower cost)
- Split large files rather than growing them — SKILL.md already directs Claude to load files at specific steps, so splitting a file in two doesn't break the workflow
- New reference files are free until loaded — adding a file to the repo costs nothing if SKILL.md only loads it when relevant

## Adding a language file

Use `languages/pl.md` as the template. Every language file needs these sections:

| Section | What to cover |
| ------- | ------------- |
| **Phonosemantics** | How sounds carry meaning in this language — which sounds feel technical, warm, aggressive, premium. Where this DIFFERS from English. |
| **Word Formation** | Compounding rules, productive prefixes/suffixes, diminutives/augmentatives. How the language builds new words. |
| **Cultural Naming Conventions** | What makes a brand name feel premium, cheap, modern, or dated in this culture. Local cultural territories (mythology, history, nature). |
| **Alphabet / Script** | Diacritics, character sets, how the name looks when written. Domain and handle implications. |
| **Anti-Patterns** | Language-specific naming failures. What constitutes slop in THIS language. |
| **Cross-Language Pitfalls** | Words that cause problems internationally. False friends, offensive meanings in neighboring languages. |
| **Rhythm and Stress** | Stress patterns, syllable count sweet spots, how the language's rhythm affects brand name perception. |

File naming: `languages/<ISO 639-1 code>.md` (e.g., `de.md`, `ja.md`, `fr.md`). Use region codes only when the language has significant regional variation that warrants separate files (e.g., `pt-PT.md` vs `pt-BR.md`).

**Quality bar:** Write from knowledge of the language and culture, not from a quick Wikipedia skim. If you're not confident about a section, mark it with `<!-- TODO: needs native speaker review -->` and we'll find a reviewer.

## Adding an industry file

Industry files live in `industries/` and cover naming constraints for specific niches. Each file needs these sections:

| Section | What to cover |
| ------- | ------------- |
| **Platform constraints** | Character limits, slug formats, store/registry requirements |
| **Audience expectations** | What sounds premium, trustworthy, or appropriate in this industry |
| **Naming conventions** | Existing patterns and which are saturated |
| **Trademark / regulatory** | Industry-specific IP or regulatory naming rules |
| **Case studies** | 3-5 real names analyzed — what works and why |
| **Anti-patterns** | What constitutes slop in this specific industry |
| **Territory map** | Metaphor territories especially relevant to this industry |

File naming: `industries/<industry>.md` (e.g., `saas.md`, `fintech.md`, `developer-tools.md`). Lowercase, hyphens for multi-word names.

After creating the file, add it to `industries/INDEX.md`.

## Adding case studies

Case studies go in `case-studies.md`, organized by naming technique (Metaphor, Common Word, Compound, Invented, Cultural Reference).

Requirements:

- **Verifiable origin story** — link to a primary source: founder interview, blog post, podcast, company documentation. "I think the name comes from..." is not a case study.
- **Follow the existing table format:**
  ```markdown
  | **Name** | Product category | Origin story | Why it works |
  ```
- **"Why it works" must reference specific principles** from the skill — which principles does this name satisfy? What makes the metaphor strong?
- **Failed names** go in the "Names That Teach By Failing" section with the same format.

## Style conventions

- **Tables** for structured data, prose for explanations
- **Real product names** as examples, not hypothetical ones
- **Direct, technical tone** — "this pattern fails because..." not "you might want to consider whether perhaps..."
- **No emojis**
- Heading hierarchy: `##` for main sections, `###` for subsections, `####` sparingly
- When referencing another file, use a relative markdown link: `[principles.md](principles.md)`

## Linting

PRs are automatically checked by [markdownlint](https://github.com/DavidAnson/markdownlint) and a link checker. Your PR won't merge if lint fails.

**Run locally before pushing:**

```bash
npx markdownlint-cli2 '**/*.md'
```

**Common issues:**

- Fenced code blocks need a language tag — use `` ```text ``, `` ```bash ``, `` ```markdown ``, not bare `` ``` ``
- Heading levels must increment by one — `##` → `###`, not `##` → `####`
- Don't use bare `___` as placeholders in prose — the linter reads them as broken emphasis. Use `` `___` `` (backtick-wrapped) instead
- No bare URLs — wrap in angle brackets (`<https://example.com>`) or markdown links

See [.markdownlint.yml](.markdownlint.yml) for the full config and disabled rules.

## What reviewers check

- **Accuracy** — are facts verifiable? Are origin stories sourced?
- **Consistency** — does the contribution match the existing tone and format?
- **Cross-references** — if your change connects to other files, did you update those too?
- **Scope** — does the PR match the issue it claims to close? No scope creep.

## Review timeline

This is a solo-maintainer project. PRs are reviewed when feasible — expect a response within 1-2 weeks. Small, focused PRs get reviewed faster than large ones.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).
