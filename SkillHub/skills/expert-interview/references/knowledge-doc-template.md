# Knowledge Document Template: Worked Example

This is what a good interview output looks like. Use it to calibrate the final step of the skill: how to organize the user's answers into something `write-content` or `improve-content` can actually use. Pattern-match against this example, don't copy the topic.

## The four-section structure

Every knowledge document the skill produces should have these four sections, in this order:

1. **Key insight / contrarian take**: the one thing the user knows that most people don't
2. **Specific examples and data points**: named clients, real numbers, actual projects, dates
3. **Experience details**: what worked, what failed, what surprised them
4. **Scope and limitations**: who this applies to, who it doesn't, when it breaks down

That's it. No executive summary, no intro, no "further reading" section, no fluff. This document gets fed to a writing skill; it's not published anywhere. Compression is the goal.

## Worked example

Topic: bootstrapping a B2B tool to $100K ARR. The user interviewed is a founder who did this between 2023 and 2025.

---

**Expert Knowledge: bootstrapping a B2B tool to $100K ARR**

### Key insight / contrarian take

Cold outbound works in year one and then stops working, but not because of deliverability. It stops because the founder runs out of interesting things to say. Most advice tells you to scale outbound to 500 emails a day. The real constraint after month six is that your own product usage doesn't produce enough new angles for a second email to the same prospect. The founders who plateau at $40-60K ARR are usually the ones still writing generic outbound. The ones who break past $100K started publishing case studies instead and letting warm inbound replace cold around month eight.

*Why this section matters for downstream writing: this gives the article a thesis. The writer can now lead with "cold outbound works until it doesn't, and it stops working for a specific reason nobody talks about" instead of yet another generic "here's how I got to $100K" post. The contrarian take sets the angle for every other paragraph in the eventual article.*

### Specific examples and data points

- First ten customers came from a single Reddit post in r/smallbusiness (March 2023), 38 upvotes, 400 clicks to landing page, 11 trial signups, 9 converted at €49/mo
- Cold outbound ran from May 2023 to January 2024, peaked at 280 emails/week, hit-rate dropped from 4.2% reply rate in month one to 0.6% in month eight
- Pivoted to publishing one customer case study every two weeks starting Feb 2024. First case study about a Dutch accounting firm drove 14 signups in a week, which was more than the previous month of outbound combined
- $100K ARR crossed in November 2024, 20 months after launch, 183 paying customers, blended ACV €546/year
- CAC in outbound phase: €118. CAC once content took over: €31
- Biggest wasted spend: €3,400 on a Facebook ads experiment in summer 2023 that produced zero paying customers

*Why this section matters for downstream writing: named subreddits, specific date ranges, euro amounts, and conversion percentages are Tier 1 information gain. A generic AI can't invent "€3,400 on Facebook ads in summer 2023" convincingly, and if it does, it's wrong. The writer should weave these numbers into arguments, not dump them into a "my results" box at the bottom. Every one of these data points can anchor a section.*

### Experience details

- Tried Lemlist, Instantly, and Smartlead for outbound. Lemlist was the worst because of deliverability issues in month three (blacklisted two sending domains). Smartlead was the best because of the shared IP rotation, but switching mid-campaign lost two weeks.
- The thing that actually worked on outbound wasn't the email copy, it was the subject line format: "{first name}, question about {their tool} → {our tool}". Ugly but hit-rate doubled.
- Biggest surprise: the top three customers by revenue all came from content, not outbound. The outbound customers churned at 3x the rate. By month 18, outbound had become a net loss if you properly attributed churn.
- Failure story: spent two months in mid-2024 trying to build an annual plan discount flow because a consultant said it would raise ACV. It did, by 18%, but also doubled the refund rate because customers signed up annually without understanding the product. Killed it in September.
- Unexpected lesson: the founder's personal LinkedIn drove more demo requests than the company LinkedIn by a factor of roughly six, even at similar follower counts. Company pages are noise; personal pages are signal.

*Why this section matters for downstream writing: the "failure story" and "unexpected lesson" bullets are exactly what the write-content skill will turn into the "what went wrong" paragraphs that build EEAT trust. A specific named tool (Lemlist) with a specific named problem (deliverability in month three, two blacklisted domains) is more believable and more rankable than "we tried a cold outreach tool and it didn't work out". The failure story about the annual plan consultant is gold because it has a direction nobody else writes about: "raising ACV made refunds worse."*

### Scope and limitations

- This approach only works for products priced €30-€80/month. Below €30 the content-driven CAC math doesn't work. Above €80 you actually do need sales and outbound becomes important again.
- Assumes the founder can write. The pivot from outbound to content assumes the user is capable of writing case studies that convert, and maybe three founders in ten actually are. The others should probably stay on outbound and hire a copywriter before scaling.
- Assumes a single-founder or two-person team. A five-person team burning salary has a different math problem and probably needs to raise, not bootstrap.
- The Reddit launch trick is almost certainly dead by 2026. Worked in 2023 because r/smallbusiness was less aggressive about promotional posts. Don't replicate it literally. Replicate the principle (one high-signal organic post in the right community) in whichever community is currently viable.
- Everything above is B2B only. B2C bootstrapping at this price point has different dynamics, especially around refunds and support volume.

*Why this section matters for downstream writing: this is the "who should NOT follow this advice" section, and it's what turns a generic success story into actual thought leadership. Most $100K ARR posts leave readers thinking "will this work for me?" and never answer. The scope section answers that directly. The writer should not bury this at the end of the article; it should be near the top, so readers who aren't the right fit self-select out.*

---

## What makes this document good vs bad

**Good** means the document passes the 30% Rule: at least 30% of any article written from it could not be produced by a generic AI. The test is simple. Strip out the named tools, the euro amounts, the dated events, the specific failure stories, and the scope conditions. What's left? If what's left is an article, the human input wasn't doing any work. If what's left is obviously broken, the human input was doing the work.

**Bad** looks like this:

> Key insight: cold outbound is harder than people think. You need good copy, good targeting, and good follow-up. Many founders underestimate how much effort goes into it.

This is the LinkedIn thought leader version. No numbers, no names, no dates, no scope. Every sentence could have been produced by an LLM, and probably has been, many times. If your interview output looks like this, the interview wasn't good enough. Go back and ask follow-ups. Ask for a number. Ask for a named tool. Ask for a date. Ask what broke.

**The test you should run on the document before handing it off:**

1. Pick any paragraph. Could the words "many", "some", "often", "usually" be deleted without loss? If yes, the paragraph is generic.
2. Is there at least one proper noun per bullet (a tool, a client, a subreddit, a country, a month)?
3. Are there numbers with units, or just vibes?
4. Does the scope section answer "who is this wrong for?", and not just "here's who it's right for"?

If all four answers are yes, hand it off. If any answer is no, you have one more follow-up question to ask before the interview is done.

## Cross-reference

See `information-gain-writing.md` in this references folder for the theory behind why specificity is what makes this document valuable. The short version: Google's Information Gain patent scores content against what the searcher has already seen on the same topic. Named tools, real dates, specific failures, scope limits: those are the things that by definition can't be on the other pages, because nobody else has them. Everything else in the article can be AI-generated. This document is the part that can't be.
