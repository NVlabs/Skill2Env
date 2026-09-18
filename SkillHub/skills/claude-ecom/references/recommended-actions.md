# Recommended Actions Reference

This file provides specific, actionable improvement recommendations for each diagnostic check
in the claude-ecom skill. Each check includes 2-3 prioritized actions with estimated
implementation time and expected improvement range based on industry research and benchmarks.

---

## monthly_revenue_trend: MoM Revenue Growth (Low)

When month-over-month revenue growth is stagnant or declining, the root cause is typically
a combination of weakening acquisition, poor retention, or seasonal patterns not being leveraged.

### Actions

1. **Launch a win-back email campaign targeting lapsed customers**
   - Time: 3-5 days
   - Impact: 5-15% incremental revenue from reactivated customers
   - Details: Segment customers who purchased 60-120 days ago but have not returned.
     Send a 3-email sequence with a personalized incentive (e.g., 10% off their most-browsed
     category). Shopify data shows win-back flows recover 2-5% of lapsed customers.

2. **Implement a monthly promotional calendar aligned to micro-seasons**
   - Time: 2-3 days to plan; ongoing execution
   - Impact: 8-20% revenue lift during promoted periods
   - Details: Map out monthly themes, product highlights, and limited-time offers tied to
     cultural moments, seasonal demand, or new product launches. Consistent promotional
     cadence smooths MoM volatility. Aim for 10-20% MoM growth in early-stage ecommerce
     and 3-5% for mature stores.

3. **Optimize high-traffic landing pages for conversion**
   - Time: 1-2 weeks
   - Impact: 10-30% conversion lift on targeted pages
   - Details: Identify the top 5-10 landing pages by traffic volume. A/B test headlines,
     CTAs, hero images, and social proof placement. Even small CVR improvements on
     high-traffic pages compound into meaningful revenue growth.

### Sources
- Alexander Jarvis, "MoM Growth in Ecommerce" (alexanderjarvis.com)
- Amplitude, "Month-Over-Month Growth Rates" (amplitude.com/blog)
- Shopify, "Win-Back Email Best Practices"

---

## repeat_customer_revenue_share: Repeat Customer Revenue Share (Low)

A low share of revenue from repeat customers (typically below 30%) signals over-reliance
on new customer acquisition, which is 5-7x more expensive than retention.

### Actions

1. **Launch a tiered loyalty/rewards program**
   - Time: 1-2 weeks (using platforms like Smile.io, Yotpo, or Rivo)
   - Impact: 15-25% increase in repeat purchase rate; loyalty members spend 3.1x more
   - Details: Implement a points-based system with 2-3 tiers. Tiered programs achieve
     1.8x higher ROI than flat programs. VIP customers generate 73% higher AOV ($435 vs $291)
     and purchase 3.6x more frequently. Start simple: earn points on purchase, redeem for
     discounts.

2. **Build a post-purchase email automation sequence**
   - Time: 3-5 days
   - Impact: 10-20% increase in second-purchase rate
   - Details: After first purchase, send a sequence: order confirmation with cross-sell,
     product education/tips at day 3, review request at day 7, replenishment or
     complementary product suggestion at day 14-30. Customers who return for a second
     purchase have a 45% chance of buying a third time (Shopify data).

3. **Introduce subscription or auto-replenishment options for consumable products**
   - Time: 1-2 weeks
   - Impact: 20-40% improvement in retention over 6 months
   - Details: Subscription merchants see 45% retention at 6 months vs 20% for standard
     ecommerce (Recharge data). Offer a 5-10% discount for subscribe-and-save to
     incentivize enrollment.

### Sources
- Rivo, "27 VIP Customer Repeat Rate Statistics" (rivo.io)
- Shopify, "Repeat Purchase Rate Benchmarks"
- Recharge, "State of Subscriptions Report"
- The Seventh Sense, "12 Strategies to Increase Repeat Purchase Rate"
- Envive AI, "36 Customer Retention Statistics in eCommerce 2026"

---

## avg_discount_rate_trend: Average Discount Rate (High)

An excessively high average discount rate (typically above 15-20%) erodes margins,
trains customers to wait for sales, and devalues the brand.

### Actions

1. **Shift from percentage discounts to value-added incentives**
   - Time: 1-2 days to plan; ongoing
   - Impact: 5-10 percentage point reduction in average discount rate while maintaining conversion
   - Details: Replace blanket percentage discounts with free shipping thresholds, gift-with-purchase,
     bundle deals, or extended warranties. These preserve perceived value while costing less
     than equivalent percentage discounts. 81% of abandoned cart emails offer percentage discounts;
     differentiate by offering non-discount value.

2. **Implement tiered discount rules with maximum caps**
   - Time: 1-3 days
   - Impact: 3-8 percentage point reduction in average discount depth
   - Details: Set maximum discount caps (e.g., never exceed 20%), prohibit discount stacking,
     and use tiered thresholds (e.g., "Spend $100 get $10 off, spend $200 get $25 off")
     that increase AOV. Track gross margin per promotion, not just conversion.

3. **Create urgency through scarcity rather than discounts**
   - Time: 2-5 days
   - Impact: Maintain conversion rates while reducing discount dependency by 15-30%
   - Details: Use limited-edition products, countdown timers on flash sales, low-stock
     indicators, and early-access for loyalty members. These psychological triggers drive
     conversion without margin erosion. Reserve deep discounts for clearance of end-of-life SKUs only.

### Sources
- ReferralCandy, "The Complete Ecommerce Discount Strategy Guide for 2026"
- Email Vendor Selection, "Cart Abandonment Rate Statistics 2026"
- Pitney Bowes, "6 Ideas for Improving eCommerce Profit Margins"

---

## large_order_dependency: Large Order Dependency (High)

When a small number of large orders account for a disproportionate share of revenue
(>5-10%), the business faces fragility risk — losing those customers or orders
would materially impact performance.

### Actions

1. **Analyze large-order customers and diversify revenue sources**
   - Time: 1-3 days for analysis; ongoing for execution
   - Impact: Reduce single-order concentration below 5% of period revenue
   - Details: Identify orders exceeding 5% of period revenue. Determine if they are
     recurring (B2B accounts, wholesale) or one-off. For recurring large accounts,
     build relationship management but also actively grow the mid-tier customer base.
     For one-off spikes, discount them from trend analysis to avoid false signals.

2. **Grow the mid-tier customer base to reduce concentration**
   - Time: 2-4 weeks
   - Impact: 10-20% increase in order count from diversified sources
   - Details: Shift acquisition spend toward channels that attract higher volumes of
     mid-value customers rather than fewer high-value ones. Introduce tiered pricing
     or product bundles that appeal to a broader audience. A healthy revenue
     distribution has no single order exceeding 5% of monthly revenue.

3. **Implement revenue monitoring alerts for concentration risk**
   - Time: 1-2 days
   - Impact: Early warning when dependency thresholds are breached
   - Details: Set up automated alerts when any single order exceeds 5% of trailing-30d
     revenue, or when the top 3 orders exceed 15%. This enables proactive response
     before concentration becomes structural.

### Sources
- Revenue concentration risk management best practices
- Customer diversification strategies for D2C ecommerce

---

## top20_revenue_concentration: Top 20% SKU Revenue Concentration (Too High)

When the top 20% of SKUs account for >80% of revenue (extreme Pareto), the business
is overly dependent on a narrow product range, creating risk and limiting growth.

### Actions

1. **Create discovery merchandising for mid-tier products**
   - Time: 3-7 days
   - Impact: 10-20% revenue shift toward the mid-tier over 3-6 months
   - Details: Feature "hidden gems," "staff picks," or "rising products" collections
     on the homepage and in email campaigns. Use product recommendations to cross-sell
     mid-tier items alongside bestsellers. Bundle top sellers with lesser-known products
     to introduce them to customers.

2. **Invest in content marketing and SEO for long-tail product categories**
   - Time: 2-4 weeks; ongoing
   - Impact: 15-30% increase in organic traffic to non-hero product pages
   - Details: Create buying guides, comparison articles, and how-to content targeting
     long-tail keywords related to underperforming categories. Each piece of content
     acts as a new entry point to the catalog. Internal linking from top-selling
     product pages to related mid-tier products distributes link equity.

3. **Review and optimize pricing/positioning of mid-tier products**
   - Time: 3-5 days for analysis; ongoing for testing
   - Impact: 5-15% conversion improvement on repositioned products
   - Details: Analyze why mid-tier products underperform. Common issues: poor product
     photography, weak descriptions, uncompetitive pricing, or low review counts.
     Prioritize the top 20 mid-tier products with the best margin potential and
     systematically fix their product pages.

### Sources
- IBSW, "SKU Rationalization in E-Commerce: Strategic Approach to Growth"
- ThoughtSpot, "How to Use Data to Optimize Your SKU Rationalization Process"
- Onramp Funds, "9 Ways to Improve eCommerce Profit Margins"

---

## converting_sku_rate: Converting SKU Rate (Low)

A low converting SKU rate (below 50-70%) indicates catalog bloat — too many SKUs
with zero or negligible sales. This increases carrying costs, dilutes marketing
resources, and degrades the customer browsing experience.

### Actions

1. **Conduct SKU rationalization: discontinue or archive non-converting SKUs**
   - Time: 1-2 weeks for analysis and decision; ongoing
   - Impact: 5-15% reduction in inventory carrying costs; improved site navigation
   - Details: Flag all SKUs with zero sales in the past 90 days. Categorize as:
     (a) new launches (keep, promote), (b) seasonal (archive until season),
     (c) truly dead stock (clearance or discontinue). Removing dead SKUs reduces
     storage costs, simplifies operations, and makes the catalog easier to browse.
     SKU rationalization typically improves profit margins by focusing resources
     on high-performers.

2. **Bundle or promote non-converting SKUs with bestsellers before discontinuing**
   - Time: 3-5 days
   - Impact: Recover 10-30% of dead stock investment
   - Details: Create "complete the set" bundles pairing slow movers with popular
     items. Run a targeted clearance campaign with email and social promotion.
     Offer non-converting items as gifts-with-purchase above a spend threshold.
     If products still do not sell after a 30-day promotional push, proceed with
     discontinuation.

3. **Implement a new product launch checklist to prevent future non-converting additions**
   - Time: 2-3 days to create process
   - Impact: 20-40% fewer non-converting SKUs added over time
   - Details: Before adding a new SKU, require: demand signal validation (search
     data, customer requests), minimum viable product page (6+ images, complete
     description, competitive price analysis), and a 30-day launch marketing plan.
     Set a 60-day review gate: if a new SKU has zero sales by day 60, trigger
     a mandatory review.

### Sources
- Toolio, "SKU Rationalization: What It Is and How to Optimize It"
- Brightpearl, "How to Perform SKU Rationalization to Improve Product Management"
- ThoughtSpot, "How to Use Data to Optimize Your SKU Rationalization Process"
- IBSW, "SKU Rationalization in E-Commerce: Strategic Approach to Growth"

---

## repeat_purchase_rate: Repeat Purchase Rate (Low)

A low returning customer ratio (below 20-30%) means most revenue comes from one-time
buyers, indicating weak post-purchase engagement and retention.

### Actions

1. **Deploy a post-purchase engagement sequence across email and SMS**
   - Time: 3-5 days
   - Impact: 10-20% increase in second-purchase rate within 90 days
   - Details: Send targeted communications: thank-you + order tracking (day 0),
     product tips/care guide (day 3), review request (day 7), cross-sell recommendation
     based on purchase (day 14), replenishment reminder or new arrival alert (day 30).
     56% of shoppers become repeat buyers following personalized experiences.

2. **Implement a referral program with dual incentives**
   - Time: 3-7 days (using tools like ReferralCandy, Yotpo, or native platform features)
   - Impact: 5-10% increase in returning customer rate; referred customers have 16% higher LTV
   - Details: Offer rewards to both the referrer and the new customer (e.g., "$10 off
     for you and your friend"). Referral programs create a re-engagement touchpoint for
     existing customers while acquiring high-quality new customers who are pre-disposed
     to loyalty.

3. **Create a VIP or membership program for top customers**
   - Time: 1-2 weeks
   - Impact: 15-25% increase in purchase frequency among enrolled customers
   - Details: The top 5% of customers generate 35% of ecommerce revenue.
     Identify these customers and offer exclusive benefits: early access to sales,
     free shipping, birthday rewards, or members-only products. VIP customers show
     73% higher AOV and 3.6x purchase frequency. Even simple recognition (handwritten
     notes, surprise gifts) drives emotional loyalty.

### Sources
- Envive AI, "36 Customer Retention Statistics in eCommerce 2026"
- Amplience, "5 Proven Ecommerce Customer Retention Strategies"
- Recharge, "6 Ecommerce Retention Strategies to Maximize Repeat Business"
- Rivo, "VIP Customer Repeat Rate Statistics"

---

## Cross-Cutting Recommendations

Several actions reinforce multiple metrics simultaneously:

| Action | Checks Improved |
|--------|----------------|
| Loyalty/rewards program | repeat_customer_revenue_share, repeat_purchase_rate, monthly_revenue_trend |
| Post-purchase email automation | repeat_customer_revenue_share, repeat_purchase_rate, monthly_revenue_trend |
| SKU rationalization | top20_revenue_concentration, converting_sku_rate |
| Shift from % discounts to value-added incentives | avg_discount_rate_trend |

---

## Implementation Priority Framework

When multiple checks are flagged, prioritize actions by:

1. **Quick wins** (< 3 days, high impact): Post-purchase email sequences,
   free-shipping threshold adjustment, discount cap rules
2. **Medium effort** (1-2 weeks, high impact): Loyalty program launch,
   SKU rationalization, product page optimization
3. **Strategic initiatives** (2-8 weeks, transformational): Private-label
   development, supplier renegotiation, subscription model

Focus on the highest-impact items first, typically retention automation (repeat_customer_revenue_share, repeat_purchase_rate)
and discount governance (avg_discount_rate_trend), as these have the fastest payback period.

---

## Vertical-Specific Strategy Playbooks

When the business vertical is identified, apply the corresponding strategy playbook
from [`benchmarks.md`](benchmarks.md) to prioritize actions.

| Vertical | Top Priority Action | Reference |
|----------|--------------------|-----------|
| Fashion & Apparel | Build fit-confidence layer to reduce preventable returns | `benchmarks.md` |
| Beauty & Cosmetics | Implement guided selling (shade finders, quizzes) | `benchmarks.md` |
| Food & Beverage | Make subscription-first for consumable staples | `benchmarks.md` |
| Electronics & Gadgets | Make PDPs decision-complete (specs, compatibility) | `benchmarks.md` |
| Home & Living | Upgrade confidence merchandising (dimensions, UGC) | `benchmarks.md` |
| Health & Wellness | Build trust stack (certifications, claim review) | `benchmarks.md` |

See also: [`finding-clusters.md`](finding-clusters.md) for how clusters inform action prioritization.
