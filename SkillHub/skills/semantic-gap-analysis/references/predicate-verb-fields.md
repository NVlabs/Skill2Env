# Predicate Verb Fields by Domain

Predicates are how Google's NLP recognizes that a page actually understands a topic. Domain experts use specific verbs; generalists say "use" and "help" and "leverage." When a language model reads a SERP, the verb density is one of the clearest fingerprints of expertise — and it's also one of the fastest gaps to spot in a competitor audit.

This reference collects verb fields from domains we see often. It's not exhaustive — it's calibration. When you're running the skill on a topic outside your comfort zone, these lists tell you what "expert-written" reads like so you can recognize the gap in your draft.

Koray Tuğberk GÜBÜR's framing: the predicate is the edge in the entity graph. Noun phrases are the nodes. If your page is all nodes and no edges, you haven't said anything the language model can connect.

## 1. Coffee brewing

grind, extract, bloom, tamp, dose, shower, degas, puck, channel, pre-infuse, pull, distribute, level, dial-in, purge, dose-and-weigh

Example of the difference:
- **Generalist:** "Put the coffee in the machine and press the button. The machine will make your espresso."
- **Expert:** "Dose 18g into a 20g VST basket, distribute with a WDT tool, tamp level, lock in, and pull a 36g shot in 28 seconds. Watch for channeling in the first 5 seconds — if you see it, re-dial the grind finer."

Same topic. Different pages. Different SERP positions.

## 2. Espresso machines

tamp, lock, purge, steam, pull, extract, froth, backflush, descale, preinfuse, pre-heat, bleed, gasket-swap, shot-mirror, flush

A machine review that uses zero of these verbs is writing marketing copy. A review that uses eight of them is talking to people who own the machine or are about to.

## 3. Contract law

stipulate, indemnify, warrant, assign, convey, execute, abrogate, covenant, recite, terminate for cause, terminate for convenience, cure, notice, release, novate, reserve rights, incorporate by reference

Note how "terminate" has two specific variants that carry different legal meaning. Generalist content flattens both into "end the contract." Expert content names which kind.

## 4. Financial modeling

forecast, discount, amortize, capitalize, depreciate, reconcile, pivot, scenario-test, sensitize, consolidate, true-up, unlever, relever, normalize, flex, plug, tie out

Finance verbs are unusually compressed — each one stands in for a multi-step operation. A modeling guide that says "we check the numbers" instead of "we tie out the balance sheet" is written by someone who hasn't built a three-statement model.

## 5. Data engineering

ingest, normalize, partition, dedupe, backfill, materialize, cache, index, shard, denormalize, stream, batch, upsert, truncate, vacuum, checkpoint, replay, compact

You can feel the difference just reading the list. A blog post about "data pipelines" that doesn't use backfill or materialize once is almost certainly written by marketing, not by anyone who's been paged at 3am.

## 6. React development

render, hydrate, mount, memoize, throttle, debounce, lift, wrap, compose, suspend, batch, reconcile, portal, unmount, lazy-load, prefetch, rehydrate

The verb "hydrate" alone is a strong signal. If a React performance article never mentions hydration, it was written before Next.js 13 existed or by someone who hasn't shipped an SSR app.

## 7. Distance running

pace, stride, cadence, footstrike, arch, pronate, heel-strike, forefoot, taper, negative-split, fartlek, tempo, threshold, zone-2, pick-up, surge, bank (time)

Compare "run faster on marathon day" to "negative-split the second half after banking no time in the first 10K." Same instruction. One page gets shared in running subreddits; the other doesn't.

## 8. Photography

expose, meter, stop-down, push, pull, develop, stabilize, focus-stack, bracket, dodge, burn, composite, vignette, clip (highlights), crush (shadows), tether

"Push" and "pull" in film development are great examples of verbs that are meaningless without domain context. A generalist writer avoids them because they sound wrong. An expert uses them because they're the correct word.

## 9. Cooking and baking

fold, whip, reduce, emulsify, caramelize, deglaze, proof, blanch, temper, knead, render, sweat, sear, braise, poach, confit, brine, cure, rest

Baking verbs carry particularly high information density. "Fold" and "stir" are not interchangeable. "Proof" and "rise" overlap but signal different stages. Recipe blogs that use the wrong verbs get debunked in the comments.

## 10. Medical diagnosis

present, palpate, auscultate, rule-out, differentiate, exclude, titrate, monitor, stabilize, refer, admit, workup, screen, indicate, contraindicate, r/o (abbreviation), dose

Medical content is where predicate density correlates most strongly with E-E-A-T signals. A physician-authored article uses "present with" and "rule out" naturally. Health-content-farm articles say "have symptoms" and "check for."

## 11. Gardening

prune, stake, mulch, top-dress, side-dress, amend, transplant, harden-off, succession-plant, overwinter, pinch, deadhead, coppice, pollard, graft, bolt, lift, divide

Gardening has a beautiful verb field because it's one of the oldest specialist vocabularies. "Bolt" and "lift" are verbs no generalist would guess, and both are everyday words to a gardener.

## 12. Welding

tack, stringer-bead, weave, root-pass, filler-pass, cap, grind, chamfer, prep, preheat, interpass-cool, purge, gouge, clean, re-strike

A welding article that never uses "root pass" or "filler pass" is describing welding to people who don't weld. That's fine as introductory content — but it will never rank for anything a working welder searches.

## How to extract a domain verb field when you don't already know the domain

When you're running this skill on a topic you're not an expert in, you can build the verb field from the SERP itself:

1. **Pull the top 2–3 expert-authored pieces.** Look for author bylines with credentials, industry publication bylines, or long-form blog posts by practitioners. You can usually tell by the first 200 words.
2. **Highlight every action verb.** Not nouns, not adjectives — verbs. Ignore the common-English verbs (is, has, can, will, get, make, do, go). Keep the rest.
3. **Cross-reference with the generalist competitors.** Run the same pass on a thin aggregator article ranking in position 8–10. The verbs that appear in the expert pieces and not in the generalist are your domain predicate field.
4. **Add them to your content brief as a "verb floor."** You don't need to use all of them, but your draft should read as though the writer knows they exist. If your draft uses "improve" and "help" where the experts use "optimize," "titrate," or "tune," you've got a predicate gap that no amount of keyword density will fix.

Step 3 is the whole trick. The verb field isn't "words experts use" — it's "words experts use that generalists don't." That delta is the gap.

## Cross-reference

The expert-interview skill uses the same verb-field concept in reverse: when extracting expertise from a subject-matter expert, it specifically transcribes their action verbs because that's where the tacit knowledge lives. If you're running a content brief off an SME interview, pipe the transcribed verb field directly into the draft instructions — it's the single fastest way to make generated content read as written by the expert.

And if you're auditing a draft that you or a writer produced after an interview, check it against the expert's verb field. Drafts that lose the verbs lose the expertise.
