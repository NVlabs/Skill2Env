# Technique 21: FAQ Pages

## What It Is
Structured question-and-answer content that addresses the most common questions around a topic, product, or service. Captures long-tail "question" queries and People Also Ask opportunities.

## When to Use
Informational intent -- user has specific questions and wants direct answers. Use when PAA data shows a cluster of related questions, or when a topic has many common questions that do not justify individual articles.

## Structure Template

```
H1: "[Topic] FAQ: Veelgestelde vragen over [topic]"
    (e.g., "Zonnepanelen FAQ: 25 veelgestelde vragen beantwoord")

H2: Short intro
    1-2 sentences explaining what this page covers
    Link to pillar page for full overview

H2: [Question category 1]
    H3: [Question 1]?
        2-4 sentence answer, front-load the key fact
    H3: [Question 2]?
        Same pattern
    H3: [Question 3-5]?

H2: [Question category 2]
    H3: [Question 6]?
    H3: [Question 7-10]?

H2: [Question category 3]
    H3: [Question 11-15]?

H2: [Question category 4: Costs/Pricing questions]
    H3: [Cost question 1]?
    H3: [Cost question 2]?

H2: Still have questions?
    CTA to contact, consultation, or community
```

## Word Count
1,500-2,500 words (15-25 questions at 60-120 words per answer)

## Schema Markup
- **Primary:** FAQPage (with Question and acceptedAnswer pairs)
- **Secondary:** BreadcrumbList

## Featured Snippet Strategy
- **Format:** Paragraph snippet (FAQ queries trigger paragraph snippets)
- **Target:** Each H3 question with its concise answer paragraph
- **Tip:** Start each answer with the direct answer in the first sentence, then elaborate

## CTA Placement
- After each question category: contextual link to relevant deeper content
- End of page: contact form, consultation CTA, or chat prompt
- Inline within answers: link to products/services when naturally relevant

## Internal Linking Strategy
- Link from answers to detailed articles that cover the topic in depth
- Link to definition articles for technical terms mentioned in answers
- Link to how-to articles for process-related questions
- Link to comparison/review pages for product-related questions
- Receive links from pillar pages and service pages

## Key Success Factors
1. **Real questions from real data:** Use PAA, search console queries, and customer support data
2. **Answer-first format:** Every answer starts with the direct answer, then adds context
3. **Group by category:** Do not list 25 random questions -- organize by theme
4. **Keep answers concise:** 60-120 words per answer. Link to deeper content for complex topics
5. **Update regularly:** Add new questions based on fresh PAA and support ticket data
6. **Use the exact question phrasing:** Match how users actually search, not how you would phrase it

## Common Mistakes
- Using made-up questions instead of real search queries
- Answers that are too long (200+ words) -- defeats the purpose of an FAQ
- Answers that are too short (one sentence) -- provides no value and looks thin
- No logical grouping of questions (random order confuses readers)
- Missing FAQPage schema markup (loses AI Overview citation lift — ~3x per vendor studies; Google still uses it for entity understanding)
- Duplicating content from other pages instead of summarizing and linking
- Not updating after launch (FAQ pages go stale quickly)

## Anti-AI Focus
FAQ pages are a common target for AI generation because the Q&A format is easy to produce at scale. To ensure your FAQ pages signal genuine expertise:

- **Source questions from real user data.** Pull questions directly from Google Search Console queries, customer support tickets, live chat logs, and sales call transcripts. AI-generated FAQs tend to use obvious, generic questions.
- **Include answers that reflect actual customer interactions.** Reference specific situations, edge cases, or follow-up questions that real customers have raised. "We get asked this a lot after customers try X and find that Y happens" is a pattern AI cannot fabricate.
- **Add specificity to answers.** Instead of "prices vary," state "as of March 2026, prices range from X to Y depending on Z." Concrete numbers, dates, and conditions are strong authenticity signals.
- **Update with real frequency data.** Note which questions are most common ("this is our #1 support question") or trending ("we started getting this question after the 2026 regulation change").

## Example Topics by Niche
- Energy: "Veelgestelde vragen over overstappen van energieleverancier"
- Telecom: "Glasvezel FAQ: alles wat je wilt weten over glasvezel internet"
- SaaS: "Frequently asked questions about CRM implementation"
- E-commerce: "FAQ retourneren en ruilen: alles over ons retourbeleid"
- Local services: "Verhuizen FAQ: veelgestelde vragen over verhuisservice"
