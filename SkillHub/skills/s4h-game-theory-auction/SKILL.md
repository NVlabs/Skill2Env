---
name: s4h-game-theory-auction
description: "Analyses bidding strategy and auction design — how much to bid, how to avoid the winner's curse, and how to design revenue-maximising or efficient auctions. Triggers: 'bidding strategy', 'auction analysis', 'how much should I bid', 'auction design', 'winner's curse', 'sealed bid', 'how do I avoid overbidding', 'procurement auction', 'design an auction', 'competitive offer'."
---

# Game Theory: Auction Analysis

William Vickrey's 1961 discovery is one of the cleanest results in economics: in a second-price sealed-bid auction, bidding your true value is a *dominant strategy* — the best move regardless of what others bid. The mechanism works because you pay the second-highest bid, not your own. Overbidding your true value doesn't help you (you might win but pay more than the item is worth); underbidding doesn't help you either (you might lose an item worth more than you'd have paid). So you bid your true value and let the second-highest bid determine the price. Vickrey received the Nobel Prize in 1996 for this result and related work.

First-price auctions are strategically different: you pay what you bid, so optimal play requires *shading* your bid below your true value. The optimal shade depends on the number of competitors (shade more with more competitors) and the distribution of their valuations (shade more when competition is intense). In equilibrium, first-price and second-price auctions generate the same expected revenue — the revenue equivalence theorem — under standard conditions.

The winner's curse is the most common failure mode in *common-value* auctions (where the item has an underlying objective value everyone is trying to estimate, rather than a private personal value). Winning means you bid highest, which means your estimate was the most optimistic among all bidders. In expectation, if you bid your unconditional estimate and win, you've overpaid — because winning reveals that you were the most optimistic, not the most accurate. The correct bid is your estimate *conditional on winning*, which is lower than your unconditional estimate.

Paul Milgrom and Robert Wilson (Nobel 2020) developed the modern theory of auction design, including the simultaneous ascending auction used in FCC spectrum allocation — showing how auction design directly affects both revenue and efficient allocation.

---

## Your Process

**Step 1: Auction type identification**
Identify the auction format:
- *First-price sealed bid*: all bidders submit one bid simultaneously; highest bid wins and pays their own bid
- *Second-price sealed bid (Vickrey)*: highest bid wins but pays the second-highest bid
- *Ascending (English)*: price rises until only one bidder remains; winner pays the final price
- *Descending (Dutch)*: price falls from a high start until the first bidder claims the item at the current price
- *Other*: procurement reverse auctions, combinatorial auctions, multi-round formats

**Framing check:** Confirm the auction situation before continuing. State what you've identified — the auction format, whether the user is a bidder or designer, and the key parameters (item, number of competitors, value structure if apparent) — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the auction situation, role, and key parameters]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Private vs. common value**
Determine the value structure:
- *Private value*: each bidder has their own subjective valuation, independent of others. What the item is worth to you doesn't depend on what it's worth to others. Most art auctions, personal property sales.
- *Common value*: the item has an underlying value that is the same for all bidders, but each has an imperfect estimate. Mineral rights, spectrum licenses, antique coins (where the value is objective but uncertain). *Winner's curse applies here.*
- *Affiliated values*: intermediate case — your valuation is positively correlated with others'. Most real situations fall here.

**Step 3: Optimal bidding strategy by type**

*Second-price (Vickrey):*
Bid your true value. This is a dominant strategy — it is best regardless of what others bid. No adjustment needed.

*First-price sealed bid:*
Shade your bid below your true value. As a rough rule with *n* symmetric bidders: bid approximately (n−1)/n × your true value. With 2 bidders, bid 50% of your value; with 4 bidders, 75%; with 10 bidders, 90%. In practice: bid higher when competition is intense (many bidders, strong demand) because the shading needs to be small to remain competitive.

*Ascending (English):*
Stay in the auction until the price exceeds your true value, then drop out. Never bid beyond your valuation. The private-value dominant strategy is identical in structure to the Vickrey auction.

*Descending (Dutch):*
Accept at the price that equals your true value. No advantage to waiting longer (you risk losing), and accepting earlier costs you money.

**Step 4: Winner's curse adjustment** *(common value only)*
In common-value settings, adjust your bid downward to correct for the selection bias of winning. Procedure:
1. Estimate the item's true value using your available information
2. Ask: conditional on winning (i.e., conditional on having submitted the highest bid), what does that tell me about the true value? Winning means everyone else estimated lower — your estimate is the most optimistic
3. Revise your estimate downward by an amount that increases with the number of bidders and the uncertainty in your estimate
4. Bid based on this revised, downward-adjusted estimate, not your initial estimate

**Step 5: Auction design** *(for designers)*
Apply the following principles:
- *Reserve price*: set a floor below which you won't sell. Even in revenue-maximising design, a properly set reserve price increases expected revenue by eliminating sales at too-low prices
- *Revenue equivalence*: under standard conditions, first-price and second-price formats generate equal expected revenue. Choose based on other considerations: second-price is simpler to reason about (dominant strategy bidding); first-price gives more price certainty upfront
- *Efficiency vs. revenue*: second-price with no reserve is most efficient (item goes to highest-value bidder); adding a reserve or using a first-price format trades some efficiency for revenue
- *Multi-unit and combinatorial*: when multiple items are sold and bidders value combinations, use a format that handles complementarities — the Vickrey-Clarke-Groves mechanism generalises the Vickrey auction to multi-item settings

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Specific focus** — Zoom in on one aspect of this analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

### Auction Analysis

**Auction Type**
[Format identified: first-price sealed bid / second-price / ascending / descending / other]

**Value Structure**
[Private value / common value / affiliated values — and the implication for strategy]

**Optimal Bidding Strategy**
[Specific recommended strategy for this auction type — dominant strategy or optimal shade with reasoning]

**Winner's Curse Adjustment** *(common value only)*
[Revised estimate after conditioning on winning, and the magnitude of the adjustment]

**Specific Bid Recommendation**
[If a bidder: the recommended bid with precise reasoning. If asked to evaluate a strategy: assessment of whether it is optimal]

**Designer Recommendations** *(if applicable)*
[Reserve price, format choice, revenue vs. efficiency trade-offs, multi-unit design considerations]

---

## Notes

The revenue equivalence theorem holds under strong assumptions: symmetric bidders, private values, independent valuations, risk-neutral bidders. When these fail — bidders are asymmetric, values are affiliated, bidders are risk-averse — the revenue equivalence breaks down and format choice matters for revenue.

The winner's curse is not irrational behaviour corrected by experience alone. It is a structural consequence of the selection process: winning an auction carries information about the item's value, and that information updates your estimate downward. Even sophisticated bidders overbid in novel common-value contexts.

Auction analysis is a specialised application of mechanism design. For the general framework of designing rules to produce desired behaviour from self-interested players, use `/s4h-game-theory-mechanism-design`. For the equilibrium analysis of the auction (confirming which strategy is actually optimal for each player), use `/s4h-game-theory-equilibrium`.

Pairs with: `/s4h-game-theory-mechanism-design` (the general framework for auction design), `/s4h-game-theory-equilibrium` (equilibrium analysis of specific auction formats), `/s4h-decision-expected-value` (when the bidding decision is primarily about expected value under uncertainty, not strategic interaction).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Auction analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-game-theory-mechanism-design` — Refine the auction mechanism based on findings
  - `/s4h-probability-expected-value-calculation` — Calculate expected value of different bidding strategies
  - `/s4h-strategy-intelligence` — Gather information to improve bidding position
  - **Done** — Wrap up and synthesise what we have so far
