# Query Format Matching — Expanded

Google picks a snippet format based on query shape. Write the answer in the wrong format and another page will win, even if your content is better. This is the full pattern list.

## The Expanded Table

| Query Pattern | Snippet Format Google Shows | Example Query | Notes |
|---|---|---|---|
| "What is X" | Paragraph, 40-60 words | "what is affiliate marketing" | Most common snippet type. Answer sits directly under an H2 that mirrors the query. |
| "What does X mean" | Paragraph, 30-50 words | "what does SEO mean" | Shorter than "what is X" — Google wants a dictionary-style gloss, not an explainer. |
| "What are X" | Paragraph or unordered list | "what are backlinks" | Splits on subject: single definition → paragraph; plural enumerable → list. |
| "How to X" | Ordered list, 3-8 steps | "how to bake sourdough" | The canonical list-snippet query. Steps must use `<ol>` with `<li>`. |
| "How do I X" | Ordered list, 3-8 steps | "how do I reset my router" | First-person variant, same format. |
| "How do you X" | Ordered list, 3-8 steps | "how do you make cold brew" | Second-person variant. Same rules. |
| "Steps to X" | Ordered list, 5-10 steps | "steps to start an LLC" | Longer lists tolerated here — Google expects procedural depth. |
| "X tutorial" | Ordered list | "python tutorial" | Same as how-to; tutorial implies sequence. |
| "X vs Y" | Table (primary), paragraph (fallback) | "react vs vue" | Table wins when the page uses a real `<table>` element with clear column headers. Without a table, Google falls back to a comparison paragraph. |
| "X or Y" | Paragraph, opinionated | "css grid or flexbox" | Different from "vs" — reads as a decision, not a spec sheet. One-paragraph recommendation format. |
| "Difference between X and Y" | Paragraph or table | "difference between ram and rom" | Paragraph is more common; table only if both entities have multiple parallel attributes. |
| "Types of X" | Unordered list, 5-10 items | "types of cheese" | Each item = one noun phrase, sometimes with a 5-10 word gloss. |
| "X list" | Unordered list | "programming languages list" | Same format as types-of, usually larger (8-12 items). |
| "Best X" | Unordered list with brief descriptors | "best running shoes" | The most AIO-displaced pattern — see reality check below. |
| "Top X" | Unordered list | "top email marketing platforms" | Same as "best X". Often numbered in the source but Google still renders as bullets. |
| "When did X" | Short paragraph, under 40 words | "when did rome fall" | Direct date/year answer with 1-2 sentences of context. |
| "When was X" | Short paragraph | "when was the internet invented" | Similar to "when did X"; includes a date and actor. |
| "Who is X" | Short paragraph, person bio format | "who is elon musk" | 2-4 sentences, usually pulled near a headshot or knowledge panel. |
| "Who invented X" | Short paragraph | "who invented the telephone" | Name + year + one-line context. |
| "Why does X" | Paragraph, explanation format | "why does iron rust" | 40-70 words. Causal structure: mechanism + outcome. |
| "Why is X" | Paragraph | "why is the sky blue" | Same as "why does X". "Why" question words have historically had the highest snippet trigger rate of any question word — optimize as if a snippet is available. |
| "How much does X cost" | Table (ranges) or paragraph (single price) | "how much does a tesla cost" | Price ranges across variants → table. Single product → paragraph with the number up front. |
| "How long does X take" | Short paragraph with specific time | "how long does a passport take" | Answer the duration in the first clause; qualify in the second. |
| "How many X" | Short phrase, single number | "how many bones in the human body" | Sometimes just a number card. Format the answer as "There are N X" in the first sentence. |
| "Where is X" | Short paragraph with location | "where is machu picchu" | Often paired with a map card, not a classic snippet. Still write a paragraph answer under an H2. |
| "X definition" | Paragraph, dictionary format | "paradox definition" | Shorter than "what is X" — 20-40 words, dictionary tone. |
| "X examples" | Unordered list or paragraph with inline examples | "metaphor examples" | List format wins when examples are parallel and short. Paragraph wins when each example needs context. |
| "Is X [adjective]" | Paragraph, direct yes/no | "is coffee bad for you" | Start with "Yes" or "No", then 2-3 sentences of qualification. Google rewards the literal yes/no opener. |
| "Can X Y" | Paragraph, yes/no | "can dogs eat chocolate" | Same rule as "Is X" — commit to a direct answer first word. |
| "X calculator" | Calculator widget, not a snippet | "mortgage calculator" | Not a snippet target at all. Google serves an interactive calculator. Don't chase this. |
| "X meaning in [language]" | Paragraph, translation format | "amigo meaning in english" | Often replaced by a translation card — snippet is secondary. |

## Ambiguous and Edge Cases

- **"How much X"** (no "cost", no "take") — Google reads intent on a case-by-case basis. "How much sleep do I need" shows a paragraph. "How much is a Tesla" shows a table. When in doubt, write both: a paragraph block directly under the H2 and a table further down. Google picks.
- **"Best X for Y"** — the sub-qualification ("for beginners", "for small business") sometimes shifts Google to a substructured list with named categories ("Best overall: X. Best budget: Y. Best for beginners: Z."). Target this format when the sub-qualifier adds a dimension that splits the list cleanly.
- **Comparison queries with 3+ options** — "react vs vue vs angular" theoretically wants a table, but Google frequently rejects the snippet entirely and shows an AI Overview instead because the comparison surface is too wide for a clean snippet. When you see an AIO on a 3-way comparison, stop chasing the snippet and optimize for the AIO citation instead.
- **Questions with an implicit list** — "what are the ingredients in coca cola" reads as a what-is query but Google often shows an unordered list. Test the SERP; don't trust the query stem.
- **"X near me"** — local intent, never a classic snippet. Local pack only. Skip.

## 2026 Reality Check

Featured snippet prevalence dropped from 15.4% of queries to 5.5% as AI Overviews expanded ([Ahrefs, Goodbye Featured Snippets](https://ahrefs.com/blog/how-serp-features-have-evolved-in-the-ai-era/)). A large-scale Ahrefs study recorded a 64% drop in featured snippet visibility between January and June 2025 alone, correlating 0.9 with AI Overview growth. The takeaway: many query patterns in the table above no longer trigger a snippet at all.

Which query types still reliably show featured snippets in 2026:

- **Short factual/definitional queries** — "what is X", "when did X", "how many X", "who invented X". These still show snippets because AIO is overkill for a one-line answer.
- **How-to queries with concrete tasks** — "how to change a flat tire", "how to reset X". Procedural content holds up; AIO is less aggressive here.
- **Specific numeric questions** — "how long does X take", "how much does X cost" for a single item. Single-number answers resist AIO replacement.

Which query types have been absorbed by AI Overviews:

- **"Best X" and "top X"** — these shifted almost entirely to AIO by mid-2025 because they benefit from multi-source synthesis.
- **"Why" questions** — reason queries trigger AIO 59.8% of the time (Ahrefs), the highest rate of any category. The snippet you used to see is probably now an AIO.
- **Comparison queries** — "X vs Y" with 3+ options or complex dimensions usually show AIO instead of a table.
- **Long-tail informational queries** — the longer and more synthesis-heavy the query, the more likely AIO replaces the snippet. Rule of thumb: past 6-8 words with multiple clauses, assume AIO.

Rule of thumb: if the query is longer than 6 words or demands synthesis across sources, assume AIO. If the answer fits in a tweet, the snippet is still in play.

## How to Use This Table

1. Look at the target query.
2. Find the closest row in the table.
3. Write the answer in that exact format, under an H2 that mirrors the query.
4. Before committing, Google the query and check if a snippet actually shows. If it's an AIO instead, re-scope — see `aio-vs-snippet-decision.md`.
