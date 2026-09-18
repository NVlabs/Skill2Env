# Technique 08: Fact-Checking & Verification

## What It Is
A systematic process to verify every factual claim, statistic, quote, and attribution in AI-assisted content — because AI models confidently fabricate data, invent sources, and present plausible-sounding but incorrect information.

## Why It Works
One fabricated statistic destroys an article's credibility. Google's EEAT framework heavily weights Trustworthiness, and factual accuracy is its foundation. More practically: if a reader fact-checks ONE claim and it's wrong, they dismiss the entire article — and bounce back to search results (NavBoost penalty).

AI hallucination rates for factual claims vary by model and domain, but even the best models fabricate 5-15% of specific statistics and quotes. For an article with 20 factual claims, that's 1-3 fabricated "facts" by default.

## Step-by-Step Process

### Step 1: Claim Extraction
1. Read the draft and highlight every factual claim:
   - Statistics ("63% of marketers...")
   - Quotes ("According to [name]...")
   - Named studies or reports
   - Historical facts ("Founded in 2019...")
   - Tool capabilities ("Supports up to 100 users...")
   - Comparisons ("3x faster than...")
2. Create a verification checklist with each claim

### Step 2: Source Verification
3. For each statistic:
   - Can you find the ORIGINAL source (not another blog citing it)?
   - Is the source reputable (academic, government, major research firm)?
   - Is the year current? (Statistics from 2020 may not apply in 2026)
   - Does the exact number match? (AI often rounds or inverts percentages)
4. For each quote:
   - Did this person actually say this?
   - Is it attributed to the right person?
   - Is it in context? (AI often paraphrases and presents as direct quotes)
5. For each named study:
   - Does the study exist?
   - Does it say what the article claims it says?
   - Is the author/organization correct?

### Step 3: Claim Classification
6. Classify each claim:
   - **Verified**: Source found, claim matches
   - **Partially correct**: Source exists but numbers/context differ
   - **Fabricated**: No source found, likely hallucinated
   - **Unverifiable**: First-party data that only the author can confirm
7. Fix or remove all fabricated claims
8. Correct all partially correct claims to match actual sources
9. Flag unverifiable claims for human verification

### Step 4: Attribution Standards
10. Replace all vague attributions:
    - "Studies show..." -> "[Organization]'s [year] study of [N subjects] found..."
    - "Experts agree..." -> "[Name], [title] at [organization], states..."
    - "Research suggests..." -> "A [year] paper in [journal] by [author] found..."
    - "According to industry data..." -> "According to [specific report name]..."
11. Every statistic must have: source name, year, and ideally a link

### Step 5: Currency Check
12. Flag statistics older than 2 years for review
13. Note when data was last updated
14. Add "as of [date]" qualifiers for time-sensitive data
15. Check if more recent data is available

## Tips

- **The "Google Scholar" test**: If you can't find a study on Google Scholar, it probably doesn't exist. AI loves citing plausible-sounding studies that were never published.
- **Reverse-search quotes**: Paste any direct quote into Google with quotation marks. If it only appears in AI-generated content, it's fabricated.
- **Watch for "statistic laundering"**: AI often cites a real organization but invents the specific number. "According to HubSpot, 78% of..." — HubSpot exists, but they never published that 78% figure.
- **Common AI fabrication patterns**:
  - Round numbers (AI loves 67%, 83%, 91% — exact round numbers)
  - Recent years (AI often cites "[current year - 1]" studies that don't exist)
  - Well-known organizations (AI cites McKinsey, HubSpot, Forrester with invented numbers)

## Common Mistakes

1. **Trusting AI citations**: Even when AI provides a URL, the page often doesn't exist or doesn't contain the cited information
2. **Skipping first-party data verification**: When the human provides data, still verify it makes sense (basic sanity checks)
3. **Verifying against other AI content**: If your "source" is another AI-generated article that cites the same fake statistic, you've verified nothing
4. **Removing instead of fixing**: Sometimes the claim is directionally correct but the specific number is wrong. Find the real number rather than cutting valuable data points
