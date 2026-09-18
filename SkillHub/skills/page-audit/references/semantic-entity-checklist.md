# Semantic Entity Checklist

The page-audit skill loads this when scoring Dimension 2 (Semantic Depth & Topical Completeness). Google's NLP (BERT, MUM) builds a semantic graph of every page. If yours is missing nodes and edges that competitors have, you lose, even when keyword density is identical. This rubric identifies which nodes are missing.

## The four core audit questions

Work through these in order. Each one produces a specific finding.

**1. Which entities from this topic's semantic field are present, and which are missing?**

Entities are the people, companies, products, concepts, locations, and events that make up a topic. For "Kubernetes operators" the core set includes: CRDs, controllers, reconciliation loops, etcd, kubectl, Helm, Prometheus, Operator SDK, KUDO. A page that never mentions CRDs isn't an expert page, it's an outline. Pull the entity list from the top 3 competitors (fetched in Step 3 of the skill) and flag anything they all mention that the audited page omits.

**2. What predicates (verbs / actions) belong to this topic's semantic field, and does this page use them?**

Predicates are the load-bearing signal for expertise depth. A generalist writing about coffee brewing uses "make," "prepare," "put in." Someone who actually brews uses: grind, extract, bloom, tamp, pour, steep, filter, agitate. The predicate vocabulary alone tells Google's NLP whether you're describing the thing or inhabiting it. Audit: list the verbs used in the main body. Fewer than 5 domain-specific predicates = cap Dimension 2 at 5 regardless of word count.

**3. How dense are the Entity-Attribute-Value triples?**

An EAV triple is a fact of the form `[Entity] [has attribute] [with value]`. Example: `[Aeropress] [brew time] [1-2 minutes]` or `[Helm chart] [default timeout] [300 seconds]`. Experts know specific values; generalists describe qualitatively ("Aeropress brews quickly"). That sentence has a relationship but no value, and Google's NLP can't extract a clean triple. Count EAV triples per 500 words. Strong pages hit 15+. Weak pages hit 3 or fewer.

**4. What subtopics do the top 3 competitors cover that this page doesn't?**

Most "content gap" tools surface keyword overlaps instead of conceptual gaps. Do it manually: list the H2s and H3s for each competitor, then compare against the audited page. If two or more competitors have a "common failure modes" section and the audited page doesn't, that's a gap. If all three cover a subtopic the audited page handles in one sentence, that's a gap.

## Worked example: "best coffee brewing method"

**Thin semantic profile (scores ~4)**
- Entities: coffee, water, cup, filter, grinder
- Predicates: make, prepare, pour, add, wait
- EAV triples: "coffee needs hot water" (relationship, no value)
- Subtopics: types of coffee makers, instructions

This reads like a page written by someone who has never actually brewed coffee beyond a drip machine. It covers the *topic* but doesn't inhabit the *domain*. Google's NLP will parse it into a handful of weak triples and rank it below anything with real depth.

**Rich semantic profile (scores ~9)**
- Entities: V60, Chemex, Aeropress, French press, Moka pot, burr grinder, gooseneck kettle, scale, tamper, portafilter, TDS meter, specialty roaster, single origin, blonde roast, natural process, washed process, crema, bloom
- Predicates: grind, extract, bloom, tamp, tare, agitate, pre-infuse, steep, decant, plunge, invert, pour, swirl, filter, pre-wet
- EAV triples: `[V60] [grind size] [medium-fine]`, `[Aeropress] [brew time] [1:30-2:30]`, `[Chemex] [paper filter] [25% thicker than V60]`, `[extraction] [target TDS] [1.15-1.35%]`, `[bloom] [duration] [30-45 seconds]`, `[water temperature] [optimal range] [90-96°C]`
- Subtopics: bean-to-water ratios, grind size per method, water chemistry (TDS target ranges), common extraction mistakes (channeling, under/over-extraction), equipment calibration, bloom timing, agitation techniques, method-specific troubleshooting

The second version reads like an expert because it is one. The EAV density alone (15+ specific values in this snippet) signals domain depth to NLP that no amount of keyword variation can fake.

## 1–10 scoring anchor

**10.** Full entity network. 10+ unique expert verbs. 15+ EAV triples per 500 words. Covers all subtopics the top 3 competitors cover, plus one they don't.

**7–8.** Most entities covered. Domain predicates present but inconsistent. 5–10 EAV triples per 500 words. Misses 1–2 competitor subtopics.

**5–6.** Surface-level entity coverage. Generalist predicates dominate. Few EAV triples. Missing several competitor subtopics. Reads like summary, not expertise.

**3–4.** Thin entities, almost no domain predicates, no EAV triples (all qualitative). Misses most competitor subtopics. Reader learns nothing beyond a Wikipedia excerpt.

**1–2.** Generic wrapper. Target keyword appears, but no domain content underneath. Zero expert verbs, zero specific values. Usually AI generation without grounding or a writer with no domain access.

## Quick checks during the audit

- **Predicate count (30 seconds):** scan the main body for verbs. Fewer than 5 domain-specific ones = Dimension 2 capped at 5.
- **EAV density (1 minute):** pick a 500-word section and count specific values (numbers, measurements, named settings, thresholds). Fewer than 3 = cap at 5.
- **Competitor subtopic diff (2 minutes):** paste the audited page's H2s and each competitor's H2s side by side. Any H2 that appears in 2+ competitors but not the audit target is a named gap.

These three checks will get you 80% of the way to an accurate Dimension 2 score in under 4 minutes.

## Cross-reference

This file is the scoring rubric. For actually closing the gaps (building a semantic brief, running entity extraction against competitors, generating a predicate list), invoke the `semantic-gap-analysis` skill. Use this checklist to *find* the problem; use that skill to *fix* it.
