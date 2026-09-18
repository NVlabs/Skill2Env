# Technique 25: Glossary / Definition Hub Pages

## What It Is
A centralized collection of short definitions for industry-specific terms, organized alphabetically or by category. Each term gets a concise explanation. Functions as a topical authority signal and internal linking hub.

## When to Use
Informational intent -- user wants quick definitions of industry jargon. Use when your niche has 30+ specialized terms that users search for. The glossary page acts as a hub; high-value terms also get dedicated definition articles.

## Structure Template

```
H1: "[Industry] Woordenlijst: [X] Begrippen Uitgelegd"
    (e.g., "Energie woordenlijst: 80 begrippen over stroom, gas en verduurzaming")

H2: Introduction
    1-2 sentences: what this glossary covers and who it's for
    Anchor link navigation: A-Z or by category

H2: A
    H3: [Term 1]
        2-4 sentence definition
        Link to full article if one exists
    H3: [Term 2]

H2: B
    H3: [Term 3]
    H3: [Term 4]

... (continue alphabetically or by category)

H2: [Category-based alternative]
    H3: Basic concepts
    H3: Technical terms
    H3: Financial terms
    H3: Legal/regulatory terms
```

## Word Count
200-400 words per term (total page length depends on number of terms -- typically 5,000-15,000 words for a full glossary)

## Schema Markup
- **Primary:** DefinedTermSet (with individual DefinedTerm entries)
- **Secondary:** BreadcrumbList

## Featured Snippet Strategy
- **Format:** Paragraph snippet (definition queries trigger paragraph snippets)
- **Target:** Each H3 term heading with its concise definition paragraph
- **Tip:** Start each definition with "[Term] is..." for maximum snippet eligibility

## CTA Placement
- Sticky navigation or sidebar: search/filter functionality for finding terms
- Within definitions: contextual links to related products, tools, or services
- End of page: pillar page CTA or newsletter signup for industry updates

## Internal Linking Strategy
- **Outbound hub:** Every term links to its dedicated definition article (if one exists)
- **Outbound to related:** Terms cross-reference other glossary entries
- **Receive links:** Every article in the cluster links technical terms back to the glossary
- **Anchor links:** Use #term-name anchors so other pages can deep-link to specific definitions

## Key Success Factors
1. **Alphabetical AND searchable:** Provide both A-Z navigation and on-page search/filter
2. **Concise definitions:** 200-400 words maximum per term -- this is a reference, not an article
3. **Link to deep-dives:** High-value terms should have their own dedicated definition article
4. **Cross-reference terms:** Link related terms within definitions (builds internal link web)
5. **Keep it current:** Add new terms as the industry evolves, remove obsolete ones
6. **Anchor links per term:** Enable deep-linking from any page to a specific glossary entry

## Common Mistakes
- Definitions that are too long (turns the glossary into an encyclopedia)
- Definitions that are too short (one-sentence definitions provide no value)
- No navigation system (100+ terms without A-Z anchors is unusable)
- Not linking to dedicated articles for important terms
- Using jargon to define jargon (circular definitions)
- Publishing once and never updating
- Missing DefinedTerm schema (loses rich result opportunity for definitions)

## Anti-AI Focus
Glossary pages are frequently AI-generated because the format is repetitive and the content seems straightforward. To differentiate your glossary from AI-produced alternatives:

- **Write definitions from the practitioner's perspective.** Instead of textbook definitions, explain terms the way you would to a new colleague. Include the practical implications that matter in your specific industry context.
- **Add "why this matters" context.** After the definition, briefly note why this term is relevant to your audience. "This is important because in the Dutch market, salderen rules are changing in 2027" adds value AI glossaries lack.
- **Include common misunderstandings.** For terms that are frequently confused or misused, note the distinction. "Often confused with X, but the key difference is..." demonstrates expertise.
- **Cross-reference with specificity.** When linking related terms, explain the relationship: "See also: teruglevering (which covers the actual process of feeding electricity back to the grid, whereas salderen refers to the financial offsetting)."
- **Update with industry evolution.** Add notes when term definitions shift due to new regulations, technology changes, or market developments, with dates.

## Example Topics by Niche
- Energy: "Energie woordenlijst: van aardwarmte tot zonnepaneel -- 80 begrippen uitgelegd"
- Telecom: "Telecom woordenboek: 60 internetbegrippen eenvoudig uitgelegd"
- SaaS: "Marketing glossary: 100 digital marketing terms defined"
- E-commerce: "E-commerce woordenlijst: 50 begrippen die elke webshop-eigenaar moet kennen"
- Local services: "Bouwterminologie: 70 bouwkundige begrippen voor opdrachtgevers"
