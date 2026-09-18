# Architecture

This document explains the three-layer / three-operation architecture in detail. The main `SKILL.md` summarises it; this is the reference you reach for when you need to know *why* a design decision exists or how to handle an edge case.

## The three layers

### Raw sources

Raw sources are the user's curated input material. They live in `raw/` (or wherever the project's `SCHEMA.md` declares). They are **immutable** — the LLM reads from them but never modifies them. This immutability is load-bearing: it means the wiki can always be re-derived from the raw sources if it gets corrupted, and it gives the user a stable ground truth they can audit independently.

What goes in `raw/`: PDFs, web articles converted to markdown (the Obsidian Web Clipper is one popular path), transcripts, code repos, dataset descriptions, screenshots, hand-typed notes the user wants the wiki to incorporate. What does *not* go in `raw/`: anything the LLM generated — that all belongs in the wiki layer.

A useful convention is one source per file (or per directory if the source has multiple pieces, e.g. a paper plus its appendix), with a slugified filename that ends up matching the wiki's source-summary page name. This makes the back-pointer from the wiki to the raw source trivial.

### The wiki

The wiki is a directory of LLM-generated markdown files. The LLM owns this layer entirely — it creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. The user reads it (typically through Obsidian, but any markdown viewer works); the LLM writes it.

The wiki directory is conventionally split into subdirectories by **page type**:

- `wiki/sources/` — one summary page per ingested source. Captures what the source said, in the LLM's words, with a citation back to the raw file. These are append-mostly: you write one when you ingest a source and rarely modify it after.
- `wiki/entities/` — pages about specific things: people, products, papers, places, companies, events. Anything that has a proper noun or could plausibly be a Wikipedia article subject. These accumulate updates as new sources mention the entity.
- `wiki/concepts/` — pages about ideas, methods, frameworks, abstractions. These are the most heavily cross-referenced pages and the ones most likely to evolve as understanding deepens.
- `wiki/synthesis/` — cross-cutting analyses, comparisons, query answers filed back. This is where exploration compounds: a comparison the user asked for becomes a page the next query can build on.

`SCHEMA.md` may declare additional types (e.g. `wiki/decisions/` for an engineering team, `wiki/characters/` for a fan wiki, `wiki/experiments/` for a research lab). Adding a new type costs nothing — make the directory, document it in the schema, update the index template.

### The schema

`SCHEMA.md` lives at the wiki root and is **the configuration file** that turns a generic LLM into a disciplined wiki maintainer for *this specific* knowledge base. It documents the page types in use, the tag taxonomy, the naming conventions, any custom workflow steps, and the user's stylistic preferences (e.g. "always include a 'Why this matters' section on concept pages", "never use bullet lists in summaries").

The schema is **co-evolved** with the user. On bootstrap it starts from the default template in `assets/SCHEMA.md.template`, but every user will customize it as they discover what fits their domain. When you notice a recurring pattern in the user's edits or feedback that isn't in the schema, propose adding it. When the schema starts contradicting itself or growing unwieldy, propose pruning it.

The schema is the first file you read when entering an existing wiki. Its conventions override the defaults documented in the skill.

### The graph (optional, compiled)

The wiki may carry a fourth layer at `wiki/graph/`: a compiled, queryable view of the typed `graph:` metadata in page frontmatter and the body wikilinks. It contains a hand-edited `ontology.yaml` (the contract: which node types and predicates exist) plus generated artifacts (`nodes.jsonl`, `edges.jsonl`, `graph.sqlite`, `graph.graphml`) produced by `wiki_graph_extract.py`. **Markdown is canonical**; the graph can be deleted and regenerated from the markdown without losing knowledge.

Its purpose is to make typed, provenance-backed relationships machine-queryable — "who founded what", "what does Konvy depend on", "shortest path from A to B" — without giving up the editability and human-legibility of markdown. Typed edges require an explicit `source` (a source-page slug) and `evidence` quote; the extractor never invents them. Plain `[[wikilinks]]` in the body produce low-confidence `mentions` edges, which are useful for navigation but not for evidence.

Use the graph layer when the user's questions are predominantly relational and the cost of maintaining typed metadata is paying for itself. Skip it for purely textual wikis. Full reference: `graph-workflow.md`.

## The three operations

### Ingest

A new source has arrived. The user has dropped a file in `raw/` (or pasted content and asked you to file it). The job is to integrate this source into the wiki such that future queries can benefit from it.

The shape of an ingest: read the source (chunked if large), discuss the key takeaways with the user briefly, write a summary page in `wiki/sources/`, identify which existing pages are touched, surgically update those pages, create new pages for any new entities or concepts, update the relevant index, and append to the log.

The temptation to skip the discussion step is strong, but resist it — the user's reaction to the takeaways often reveals what should be emphasized in the wiki versus left out. Ingest is not a batch import; it's a collaborative reading.

For the full procedure, see `ingest-workflow.md`.

### Query

The user asks a question. The job is to answer it from the wiki, with citations, and to file the answer back if it represents new synthesis.

The shape of a query: read the index to identify candidate pages; read those pages; if needed, follow `[[wikilinks]]` from those pages or grep for backlinks; synthesize the answer with `[[wikilink]]` citations; offer to file the answer into `wiki/synthesis/` if it's substantive enough to be worth keeping.

The compounding effect of the wiki only works if good answers get filed back. A comparison you generated, a connection you discovered, an analysis you produced — these should not evaporate into chat history. Default to offering to file; let the user decline if the answer was too trivial or too transient.

For the full procedure, see `query-workflow.md`.

### Lint

Periodic health check. The job is to find structural and semantic problems before they compound.

Structural problems are mechanical and the bundled `wiki_lint.py` script catches them: orphan pages with no inbound links, broken `[[wikilinks]]` to nonexistent pages, oversized pages that need splitting, missing or malformed frontmatter, suspicious staleness (a page that hasn't been updated despite many recent ingests touching its topic).

Semantic problems need the LLM: contradictions between pages, claims that newer sources have superseded, concepts mentioned in many pages but lacking their own page, cross-references that should exist but don't, knowledge gaps the user might want to fill.

Lint findings are presented as proposed edits, not silent rewrites. The user approves changes. This is essential for trust — a wiki that mutates under the user is not a wiki the user can rely on.

For the full procedure, see `lint-workflow.md`.

## Why this architecture

A few load-bearing design choices and the reasoning behind them.

**Why markdown files instead of a database.** Markdown is portable (no proprietary format), version-controllable (the wiki is a git repo for free), human-editable (the user can fix things directly when needed), and natively legible to LLMs (no schema translation overhead). The downsides — no true relational queries, no transaction guarantees, no constraint enforcement — are acceptable for a personal/team knowledge base because the LLM enforces conventions through linting rather than the storage layer. For domains where these tradeoffs invert (e.g. tracking 100,000 customer records with strict referential integrity), use an actual database; this pattern is wrong for that.

**Why the LLM owns the wiki layer.** Splitting ownership creates merge conflicts. If both the user and the LLM edit pages, the LLM's mental model of the wiki goes stale and it starts producing inconsistent updates. The user owns sources (they decide what to ingest) and questions (they decide what to ask). The LLM owns the wiki (it does the bookkeeping). The user *can* edit the wiki when they spot something wrong, but those edits should be the exception, not the workflow, and they should be communicated to the LLM ("I cleaned up the page on X, please proceed accordingly").

**Why an explicit schema file.** Without it, conventions drift. Two ingests a week apart produce slightly differently-shaped pages, and a month later the wiki is internally inconsistent. The schema is the contract that makes the LLM's bookkeeping disciplined. It also makes the wiki portable — a different LLM, or a different conversation with the same LLM, can pick up where the last one left off because the conventions are documented rather than implicit in chat history.

**Why filing answers back matters.** A query is an act of synthesis. The LLM read N pages and produced an answer that connects them. That synthesis is itself valuable knowledge — the next query that touches the same topic shouldn't have to re-derive it. Filing back is what turns the wiki from a passive archive into a compounding artifact.
