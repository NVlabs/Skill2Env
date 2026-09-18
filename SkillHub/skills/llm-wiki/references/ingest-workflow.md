# Ingest Workflow

When a new source arrives, this is the procedure. The order matters — each step builds context for the next.

## Step 0: Check the schema

Before anything else, read `wiki/SCHEMA.md`. The user may have customized the page-type structure, the tag taxonomy, the naming conventions, or the ingest workflow itself. Schema overrides everything documented here.

## Step 1: Place the raw source

If the source isn't already in `raw/`, place it there. Use a slugified filename: lowercase, hyphens for spaces, no special characters, with the original extension. For web articles, save as `.md` (Obsidian Web Clipper output is ideal). For PDFs, keep the `.pdf`. For transcripts, save as `.md` or `.txt`.

The slug you pick here will become the slug of the source-summary page in `wiki/sources/`, so make it descriptive and stable.

## Step 2: Read the source

For short sources (under ~5,000 words / ~25,000 tokens), read the whole thing in one pass.

For long sources (papers over ~30 pages, book chapters, multi-hour transcripts), **chunk-read**: read the table of contents or section headers first to build a mental map, then read sections sequentially, summarizing each section in working memory before moving to the next. Do not load the entire raw source into context at once if it would consume more than ~25% of your context window — that leaves no room for the rest of the operation.

For PDFs specifically, prefer the `pdf-reading` skill if available (it handles the chunking automatically). Otherwise extract text first with `pdftotext` or `pdfminer` and then chunk-read the extracted text.

For images embedded in the source: read the surrounding text first, then view only the images that the text suggests are load-bearing (a chart referenced in an argument, a diagram of a system, a figure the source explicitly walks through). Don't blindly load every image — many are decorative.

## Step 3: Discuss the takeaways with the user

Briefly — three or four sentences. Surface what struck you as important, what was surprising, what connects to existing wiki content, and what's worth flagging. The user's reaction shapes the next steps. They might say "skip the methodology section, only the results matter for me" or "we already have a page on this — just update it" or "this contradicts the page on X, flag that prominently".

If the user is operating in a hands-off mode (batch ingest, "just process these 20 papers"), skip the discussion but be more conservative on the wiki edits — make smaller, safer updates and surface anything ambiguous in the log.

## Step 4: Identify what's touched

Before writing anything, do a survey pass against the wiki to determine the impact:

1. Read `wiki/index.md` (or the relevant shard under `wiki/indexes/`) to identify existing pages this source touches. Look for entity names, concept names, and topical overlap.
2. For each potentially-touched page, read the page to confirm. (Read, don't grep — the index summaries can mislead.)
3. List, in working memory: existing pages to update, new pages to create, contradictions to flag.

This survey is what prevents duplication. Without it, you'll create a new page on a topic that already has one under a slightly different name.

## Step 5: Write the source-summary page

Create `wiki/sources/<source-slug>.md`. Use the page template (`assets/page.md.template`) as a starting point. Frontmatter should include at minimum:

```yaml
---
type: source
title: "Original title of the source"
authors: ["Author Name"]
url: "https://..." # if applicable
raw: "raw/<source-slug>.<ext>"
ingested: 2026-04-15
tags: [tag1, tag2]
entities: [entity-page-1, entity-page-2]
concepts: [concept-page-1, concept-page-2]
---
```

Frontmatter list values are bare slugs — the `[[wikilink]]` syntax goes in the body, not in YAML.

The body should be the LLM's summary of the source — the key claims, the methodology if relevant, the conclusions, the open questions. Do not paraphrase the entire source; that defeats the purpose. Aim for a summary that captures what a future query would need to know without re-reading the raw file.

Keep the page atomic — under the 400-line soft cap. If the source is so dense that a single summary page can't capture it, split: one page per major section, each linking to the others, with a parent page that gives the overview.

End the body with a "Where this fits" section listing `[[wikilinks]]` to the entity and concept pages this source touches. This is the bidirectional link from source → existing structure.

## Step 6: Update touched pages

For each existing page identified in Step 4, surgically edit it to incorporate what the new source adds. Use `str_replace`, not full rewrites. The goal is to add a sentence or paragraph in the relevant section, with a `[[wikilinks]]` citation to the new source-summary page.

Common update patterns:

- A new source corroborates an existing claim → add a citation: `..., as established in [[paper-X]] and now corroborated by [[paper-Y]]`.
- A new source contradicts an existing claim → flag prominently: add a "## Contradictions" section if it doesn't exist, and document the contradiction with both sources cited. Do not silently overwrite the older claim.
- A new source adds a new dimension to an existing topic → add a new sub-section, don't dilute the existing prose.
- A new source mentions an entity or concept the page already discusses → update the `sources:` frontmatter and add the cross-reference where relevant in the body.

If updating a page would push it over the 800-line hard cap, that's the signal to split the page (extract the new dimension into its own page, link from the parent). Do that as part of the ingest, not as a deferred lint task.

## Step 7: Create new pages for new entities and concepts

For each new entity or concept the source introduces that doesn't have a page yet, decide whether it warrants its own page. Heuristic: if the source mentions it in passing and no other source is likely to expand on it, just mention it inline on a related page. If the source treats it as a first-class topic or you can foresee future sources building on it, create a page.

New pages need:
- Frontmatter with `type`, `tags`, `sources: [[[<source-slug>]]]`, `created`, `updated`.
- A body that introduces the entity/concept with what this source said about it.
- Inbound links — at least one existing page should `[[wikilink]]` to the new page, otherwise it's an instant orphan. Update the existing page to add the link.

A new page that nothing links to is a bug in the ingest, not just a lint finding.

## Step 8: Update the index

Add entries for any new pages to `wiki/index.md` (or the appropriate shard). Each entry is one line: a wikilink to the page and a one-sentence summary. Keep the summary tight — the index is engineered to be cheap to read, and a fat index defeats the index-first navigation principle.

If `index.md` exceeds 300 lines after this update, that's the signal to shard. Do it now while the structure is fresh — see `scaling-playbook.md` for the procedure.

## Step 8b: Refresh the graph layer (only if `wiki/graph/ontology.yaml` exists)

If the wiki has the optional graph layer:

1. Add typed `graph.relationships[]` only when the source explicitly supports them (predicate, source-page slug, evidence quote, confidence, status). When uncertain, prefer a plain `[[wikilink]]` in the body — the body wikilink already produces a `mentions` edge.
2. Run `python scripts/wiki_graph_lint.py wiki/`. Triage findings with the user before extracting; do not silently rewrite typed edges.
3. Run `python scripts/wiki_graph_extract.py wiki/` to regenerate `nodes.jsonl`, `edges.jsonl`, `graph.sqlite`, `graph.graphml`.

Skip this entire step if the ingest added no `graph:` metadata and created no new pages — the compiled artifacts are unchanged. Full reference: `references/graph-workflow.md`.

## Step 9: Append to the log

One line in `wiki/log.md`, with the prefix `## [YYYY-MM-DD] ingest | <source-title>`. Optionally add a sub-line listing the pages touched. If the graph layer was refreshed, add a second sub-line: `   graph: +N nodes, +M typed edges`. The log is parsed by simple unix tools (`grep "^## \[" log.md | tail -10`), so the prefix matters.

## Step 10: Close the loop with the user

Tell the user what you did, briefly: "Ingested. Created the source page and a new entity page for X; updated the concept pages for Y and Z. Flagged a contradiction with [[paper-A]] regarding the claim about W."

If the source revealed something worth following up on (an obvious gap, a question the source raised but didn't answer, a candidate next source to ingest), say so — this is where the wiki's compounding effect comes from.

## Anti-patterns to avoid

**Loading the whole source into context at once when it's large.** This is the most common scaling failure. Chunk-read.

**Rewriting whole pages instead of surgical edits.** This burns tokens, risks losing nuance, and erodes diff quality if the wiki is in git.

**Creating pages with no inbound links.** Orphans accumulate fast and become invisible. Always link.

**Ingesting silently in batch mode without surfacing surprises.** Batch ingest is fine, but a one-line "ingested 5 sources, 2 new entity pages, 1 contradiction with [[X]]" summary is the minimum.

**Treating prior wiki pages as ground truth instead of the raw sources.** When updating an existing claim, re-read the raw source for that claim before merging the new one. Don't compound on the wiki's own paraphrase.

**Letting the page split decision drift to a future lint pass.** If a page crossed the size cap during this ingest, split it during this ingest.
