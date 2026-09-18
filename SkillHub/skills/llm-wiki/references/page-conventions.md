# Page Conventions

The structural rules every wiki page follows. The schema may extend or override these for a particular wiki, but these are the defaults.

## Frontmatter

Every wiki page begins with YAML frontmatter. The required fields:

```yaml
---
type: <source|entity|concept|synthesis|...>
title: "Human-readable title"
tags: [tag1, tag2, tag3]
sources: [source-slug-1, source-slug-2]
created: 2026-04-15
updated: 2026-04-15
---
```

Note that frontmatter list values are **bare slugs**, not `[[wikilinks]]`. The double-bracket syntax is only used in the page body. The bundled scripts treat frontmatter `sources:`, `entities:`, and `concepts:` lists as slug references and resolve them the same way as body wikilinks.

`type` determines the page-type and which subdirectory the page lives in. Standard types are `source`, `entity`, `concept`, `synthesis`. The schema can declare additional types.

`title` is the human-readable name. The filename slug is separate and may be a short version of the title. For pages about people, the convention is `Last, First` for sortability; for everything else, natural casing.

`tags` is a flat list. Tags are how `wiki_search.py` filters and how the user navigates topically in Obsidian. Keep the tag taxonomy small and disciplined — a wiki with 200 tags has effectively no tags. The schema should declare the canonical tag set and the lint script will warn on tags outside it.

`sources` is the list of source-summary pages this page draws from. Always populated for entity/concept/synthesis pages; for source pages themselves, this field is omitted (the source page is the source).

`created` and `updated` are dates in ISO format. `updated` is the load-bearing one — it powers the staleness check in lint and the "what's new" view.

Type-specific fields:
- Source pages add `authors`, `url`, `raw` (path to the raw file), `ingested`.
- Entity pages may add `aliases` (other names for the same entity), `kind` (person, paper, product, etc.).
- Synthesis pages add `question` (the original question, if it was filed back from a query) and `sources_consulted`.

## Wikilinks

Cross-references use the `[[page-slug]]` syntax. The slug is the filename without the `.md` extension and without the directory prefix — Obsidian-style. Aliasing is supported: `[[page-slug|display text]]`.

Every page should have at least one inbound link. New pages without inbound links are orphans and the lint pass will flag them.

The bundled `wiki_search.py --backlinks <slug>` returns inbound links. To find them manually:

```bash
grep -rln "\[\[<slug>\]\]" wiki/
```

## Page sizing

**Soft cap: 400 lines or ~2,000 words.** When a page approaches this, consider whether it should split.

**Hard cap: 800 lines.** Pages over this must split. The lint script flags violations.

Atomicity heuristic: a page is about *one* thing. A page on "Diffusion Models" should not also be the page on "Stable Diffusion" — those are two pages with cross-references. If you find yourself writing "## Variants" with five sub-sections of substantive prose, those sub-sections are probably their own pages.

The reason for the size cap is the context-bottleneck principle: any single page read is bounded, so the LLM can confidently read several pages without exhausting context.

## Naming

Page slugs are lowercase, hyphenated, no special characters. Match the directory: a concept page lives at `wiki/concepts/<slug>.md`.

For entity pages about people: prefer the full name slugified (`andrej-karpathy.md`), not just the surname. Add `aliases:` to frontmatter for common short names.

For source pages: use a slug derived from the source title, possibly with the year for disambiguation (`attention-is-all-you-need-2017.md`). The source page slug should match the raw file slug if possible — that makes the back-pointer trivial.

For synthesis pages: derive from the question or the topic, not the date. `comparing-rag-vs-llm-wiki.md`, not `2026-04-15-question.md`. Date-based names don't surface usefully in the index.

## Body structure

The body has no rigid template — the schema may declare one for specific page types — but a few defaults work well:

**Source pages**: lead paragraph summarizing the source's main contribution. Sections for key claims, methodology (if relevant), conclusions, open questions. End with a "Where this fits" section listing the entity and concept pages this source touches.

**Entity pages**: lead paragraph defining the entity. Sections for relevant attributes (for a paper: authors, venue, key claims; for a person: affiliation, notable work; for a product: what it does, who makes it). A "Mentioned in" section is unnecessary — the backlink discovery handles that.

**Concept pages**: lead paragraph defining the concept clearly. Sections for the key formulation, variants, contested aspects, related concepts. Heavy use of `[[wikilinks]]` is expected — concept pages are the connective tissue of the wiki.

**Synthesis pages**: lead with the question (if filed from a query) or the framing. The body is the answer/analysis. End with the sources consulted as wikilinks.

## Hedging language

When a source claims something that hasn't been corroborated by other sources in the wiki, hedge: "Source X claims Y, though this is not yet corroborated by other sources in the wiki." The lint pass will revisit hedged claims as the wiki accumulates more sources, either upgrading them to confirmed or flagging them as contested.

When two sources contradict, document both: "Source X claims Y; source Z claims not-Y. The contradiction is unresolved." Do not silently pick a side.

## Keeping pages voice-neutral

The wiki is the LLM's voice, not the source author's voice and not the user's voice. Paraphrase rather than quote, except for short load-bearing phrases where the exact wording matters. Maintain a consistent, neutral, encyclopedic tone — close to a Wikipedia article in register, not a chat reply.
