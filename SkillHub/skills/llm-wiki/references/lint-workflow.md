# Lint Workflow

A health check on the wiki. Best run on a cadence — after every N ingests, weekly, or when the user explicitly requests it — not on every operation. Lint is split into a structural pass (handled by `wiki_lint.py`) and a semantic pass (handled by the LLM directly).

## Step 0: Check the schema

`wiki/SCHEMA.md` may declare additional lint rules specific to this wiki (e.g. "every entity page must have an `aliases:` field", "no concept page without at least 2 sources"). Read it.

## Step 1: Run the structural lint script

```bash
python scripts/wiki_lint.py wiki/
```

If the wiki has the optional graph layer (`wiki/graph/ontology.yaml` exists), also run:

```bash
python scripts/wiki_graph_lint.py wiki/
```

This catches typed-edge problems independently of the structural lint: unknown predicates, missing evidence, broken object references, alias collisions, invalid `confidence`/`status` values, broken `contradicts`/`supersedes` references. Triage findings the same way as structural lint — propose fixes, don't apply them silently. After approved fixes, run `wiki_graph_extract.py` to refresh the compiled artifacts.

This produces a report covering:

- **Orphan pages** — pages with no inbound `[[wikilinks]]` from anywhere else in the wiki. Orphans are usually a sign that an ingest forgot to update a parent page. They become invisible because the index-first navigation can't surface them.
- **Broken wikilinks** — `[[page-name]]` references pointing to nonexistent pages. Usually a typo or a page that got renamed without updating its referrers.
- **Oversized pages** — anything over the 800-line hard cap (or 400-line soft cap, with a warning).
- **Frontmatter issues** — pages missing required fields (`type`, `tags`, `sources`, `updated`), or with malformed YAML.
- **Stale pages** — pages whose `updated:` date is much older than the most recent ingest that touched their topic. (The script approximates this using the page's tags and the log.)
- **Duplicate slugs** — two pages with the same slug in different subdirectories (a sign of an ingest collision that wasn't resolved).

The script is conservative — it reports findings but doesn't fix them. Present the report to the user.

## Step 2: Triage the structural findings

Walk through the findings with the user and propose a fix for each:

- Orphans: either link them from a sensible parent page (preferred), or determine that the page is genuinely useless and delete it (rare). If many orphans pile up, the index is probably out of date — re-derive the index entries.
- Broken links: rename the link to match the actual page, or create the missing page if it should exist, or remove the link if the concept turned out not to warrant a page.
- Oversized pages: split. Extract sub-concepts into their own pages, link from the parent, update the index.
- Frontmatter issues: add the missing fields. If many pages have the same gap, consider whether the schema should be relaxed or the bootstrap template improved.
- Stale pages: read the recently-touched related pages and the relevant raw sources, update the stale page surgically.
- Duplicate slugs: one is canonical, the other should be merged in and deleted. Pick the better-named one as canonical and migrate inbound links with `grep` + `str_replace`.

Present each proposed fix as an edit, not a fait accompli. The user approves.

## Step 3: Run the semantic pass

The semantic pass is what the script can't do — it requires reading pages and reasoning about content. The good news is that you don't have to read the whole wiki: focus on the pages most likely to have semantic issues.

**Recently updated pages.** Read the last ~10 pages that were modified (sorted by `updated:` frontmatter or by the log). Look for:

- Contradictions with older pages on the same topic. The new claim may have superseded the old one (in which case mark the old as superseded with a note), or both may be true but in different contexts (in which case clarify each), or the new ingest may have been wrong (in which case revert).
- Internal contradictions within a page (an ingest layered on a new claim without reconciling against existing prose).
- Repeated mentions of an entity or concept that doesn't have its own page yet — candidate for promotion.

**Highly-linked pages (hubs).** These are the most likely to drift because every ingest touches them. Use `wiki_search.py --top-linked 10` (or grep `[[wikilinks]]` and count) to find them. Read each hub and check that the prose still hangs together and the cross-references still make sense.

**Pages flagged with explicit uncertainty.** During ingest, the convention is to hedge ("the source claims X, though this is not yet corroborated") rather than assert. The lint pass is when you check whether subsequent ingests have corroborated or contradicted, and update accordingly.

## Step 4: Surface gaps

Look at what's referenced but not pageified. Run:

```bash
python scripts/wiki_lint.py wiki/ --suggest-pages
```

This finds entity-like and concept-like names that appear in many pages but lack their own page. The user can decide which to promote and which to leave as inline mentions.

Also look for what's not covered at all — topics the user has expressed interest in but that haven't been ingested yet. The log can help here ("you ingested 5 sources on diffusion models in March but nothing since; want to refresh?").

## Step 5: Update the index

After lint fixes, the index almost certainly needs updates: new pages, renamed pages, deleted pages, changed summaries. Re-derive the affected index entries surgically.

If `index.md` is over 300 lines and hasn't been sharded yet, this is a good moment to do it. See `scaling-playbook.md`.

## Step 6: Append to the log

One line: `## [YYYY-MM-DD] lint | <N> structural fixes, <M> semantic fixes, <K> proposed gaps`. Optionally a sub-line listing the highest-impact changes.

## Cadence

A reasonable default: structural lint after every 5 ingests, semantic lint weekly or after every 20 ingests, gap-finding monthly. Adjust based on the user's pace and the wiki's volatility. A wiki that's growing fast needs more frequent lint; a stable mature wiki needs less.

The user may also trigger lint explicitly ("clean up the wiki", "what's broken", "lint pass please"). Treat these as priority — the user is asking because they noticed something.

## Anti-patterns to avoid

**Silent rewrites.** Lint findings are proposals. The user approves changes. A wiki that mutates without the user's knowledge stops being trustworthy.

**Treating lint as cleanup-only.** The semantic pass is also where new connections get made. If you read 10 pages and notice that two of them point at the same underlying idea, that's a synthesis-page candidate, not just a lint finding.

**Letting the lint report grow until it's overwhelming.** If the report is too long for the user to triage, the cadence is wrong (lint more often) or the wiki has outgrown its conventions (revisit the schema).

**Skipping lint because everything seems fine.** Silent corruption is the failure mode that's hardest to detect and most damaging. Lint catches it.
