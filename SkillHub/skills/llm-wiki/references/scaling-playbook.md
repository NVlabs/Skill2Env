# Scaling Playbook

Thresholds at which the wiki's structure needs to evolve, and the migration steps. The goal is to keep the wiki's context cost roughly constant per query as the wiki grows — the LLM should never need to read more pages or larger pages just because the wiki got bigger.

## The bottleneck

Naive LLM Wiki implementations break at scale because of a few specific failure modes, each of which has a structural fix:

- **The index file becomes too large to read cheaply.** Fix: shard the index by category.
- **Pages grow unboundedly as more sources mention them.** Fix: enforce the page size cap; split when violated.
- **Index summaries become too vague to disambiguate candidates.** Fix: tighten summaries; introduce frontmatter filtering via the search script.
- **Brute-force grep over the wiki replaces index-first navigation.** Fix: make the index actually useful and use the search script as the explicit fallback.

## Threshold 1: ~50 pages

Below this scale, you need almost no structure. A flat `wiki/` directory with `index.md` and `log.md` is enough. The categorical subdirectories (`entities/`, `concepts/`, etc.) are still worth using from the start because they're free, but the index doesn't need sharding and the search script is overkill.

## Threshold 2: ~150 pages OR `index.md` over 300 lines

Time to **shard the index**. The migration:

1. Create `wiki/indexes/` directory.
2. Split `index.md` by category into `indexes/sources.md`, `indexes/entities.md`, `indexes/concepts.md`, `indexes/synthesis.md` (and any custom types from the schema). Each shard is a list of pages of that type, with the same one-line summaries.
3. Rewrite the top-level `index.md` to be a directory of shards: each shard linked, with a one-line description of what's in it and a count.
4. Update the schema to document the sharded structure.
5. Update the ingest workflow in your working memory: now you update `indexes/<type>.md`, not `index.md` directly.

The top-level `index.md` should now be tiny — under 50 lines — and the shards are each bounded by the type-specific volume.

If a single shard later exceeds 300 lines (most likely `entities.md` or `concepts.md` if the wiki has a strong topical focus), shard *that* by sub-category: `indexes/entities-people.md`, `indexes/entities-papers.md`, etc. The principle generalizes.

## Threshold 3: ~300 pages

Time to introduce the **search script as a routine fallback**. Index navigation still works for direct lookups ("the page on diffusion models"), but fuzzy queries ("which papers discuss training stability") benefit from BM25 ranking.

`scripts/wiki_search.py` provides:

- `python scripts/wiki_search.py "query terms"` — top-N pages by BM25 score.
- `--type concept` — filter by frontmatter type.
- `--tag <tag>` — filter by tag.
- `--since 2026-01-01` — filter by `updated` date.
- `--backlinks <slug>` — find pages that link to a given page.
- `--top-linked N` — find the N most-linked-to pages (hubs).

Update the schema to declare the search script as a sanctioned fallback, so that future LLM sessions know to reach for it rather than degenerating into recursive grep.

## Threshold 4: ~500 pages

At this scale, two things start to matter:

**Structural lint cadence becomes weekly or per-N-ingests.** Manual oversight stops scaling. Rely on `wiki_lint.py` to surface structural drift and triage with the user.

**The search script may want a real index.** The default `wiki_search.py` rebuilds its BM25 index on every run, which is fine up to a few thousand pages. Beyond that, persist the index to disk (the script supports `--cache .wiki-search-cache.json`).

Also consider whether the wiki has organically split into distinct topic clusters that don't really cross-reference each other. If so, a single wiki may be the wrong shape — splitting into per-topic wikis (each with its own `SCHEMA.md`, `index.md`, etc.) may be cleaner. The user should make this call.

## Threshold 5: ~1,000+ pages

At this scale, the question is whether the LLM Wiki pattern is still the right tool. Markdown + grep + frontmatter scales further than people expect (the gist author reports a wiki of ~100 articles and ~400K words working fine), but at some point a real database with structured queries beats markdown. Signals it's time to consider migrating:

- The user's queries are predominantly relational ("show me all papers from author X cited by papers in topic Y published after date Z"). A graph database serves this better.
- Lint reports are too long to triage even at high cadence.
- The schema has grown to specify dozens of types and hundreds of tags — at that point you've manually built a database schema in markdown.

If the user wants to migrate, the markdown wiki is excellent input for the migration: every page has frontmatter and `[[wikilinks]]` that map cleanly to a property graph.

## When to *not* shard

Sharding is irreversible-ish (you can un-shard, but it's annoying), so don't do it preemptively. Wait for the actual threshold. A wiki of 80 pages with a sharded index has worse usability than the same wiki with a flat index, because the shards add a navigation step without enough volume to justify it.

## When to introduce custom page types

The default types (`source`, `entity`, `concept`, `synthesis`) cover most use cases. Add a custom type only when the user has a clear category of pages that don't fit any default and that benefits from being a distinct subdirectory (queryable, distinct lint rules, distinct templates). Examples that justify it:

- `decision` pages for a team that documents architectural decisions
- `experiment` pages for a research lab logging trial results
- `character` pages for a fan wiki tracking a fictional cast
- `meeting` pages for a team logging meetings

Don't add a type for a one-off — use tags instead. Adding a type is a schema change that affects the index, the lint script, and every future ingest.

## Detecting "we've outgrown our conventions"

Some signals that the schema needs revision rather than just more lint:

- The same kind of frontmatter issue keeps reappearing — the field needs to be optional, or the bootstrap template needs an example.
- Pages keep getting created that don't fit cleanly into any existing type — a new type is wanted.
- The tag list has grown unmanageable — prune, consolidate, or formalize the taxonomy.
- The user keeps overriding the LLM on a particular kind of decision — encode their preference in the schema so it persists across sessions.

Schema revision is healthy. A schema that doesn't change after the first few weeks of a wiki's life is probably not being used.
