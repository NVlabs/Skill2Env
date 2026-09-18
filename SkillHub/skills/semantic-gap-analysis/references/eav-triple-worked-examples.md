# EAV Triple Worked Examples

EAV modeling is hard to learn abstractly. What follows is a set of worked examples across domains — each one showing the thin-keyword version of a topic alongside the rich semantic version a domain expert would write. The contrast is the point. When you run Step 5 of the skill (Map Entity Relationships), these are the shapes you're aiming for.

The framework is Koray Tuğberk GÜBÜR's: every entity on a page should carry attributes and relations to other entities in the same topic space. Subject, predicate, object. A page that lists entities without attributes reads to a language model the same way a glossary reads to a human — flat. A page with EAV coverage reads like someone who actually knows the topic.

## Example 1 — Espresso machines

**Thin coverage (keywords only):**
> espresso machine, coffee machine, best espresso machine, $5000 espresso machine, commercial espresso machine

**Rich coverage (EAV):**
- **Entity:** La Marzocco Linea Mini
- **Attributes:** brew pressure (9 bar), boiler configuration (dual boiler, saturated group), price point (~EUR 5,800), heat-up time (~20 min), PID temperature stability (±0.5°C), E61-derived group head with saturated design
- **Relations:** competes with Rocket R58 and ECM Synchronika in the prosumer tier; successor to the La Marzocco GS3 in Home-use positioning; uses the same group head philosophy as the commercial Linea Classic; preferred by third-wave cafes like Blue Bottle for staff training machines; pairs commonly with the Eureka Atom 75 or Niche Zero grinders

The thin version ranks for "espresso machine." The rich version ranks for "best home espresso machine under 6000," "la marzocco linea mini vs rocket r58," "dual boiler home espresso," and drags PAA boxes with it. It also signals to Google that this page knows the third-wave coffee entity graph, not just the shopping keywords.

## Example 2 — SaaS payment infrastructure

**Thin coverage:**
> stripe, stripe pricing, payment processing fees, online payments

**Rich coverage (EAV):**
- **Entity:** Stripe Connect
- **Attributes:** transaction fee structure (2.9% + 30¢ for cards, 0.8% capped at $5 for ACH), platform revenue share model (Application Fee API), account types (Standard, Express, Custom), 1099-K issuance handled by Stripe for US Custom accounts, supports 135+ currencies
- **Relations:** competes with Adyen MarketPay for enterprise marketplaces and with Paddle Merchant-of-Record for simpler SaaS cases; powers Shopify Payments under the hood; used by Substack for creator payouts and Lyft for driver disbursements; built on top of core Stripe Payments primitives (Charges, PaymentIntents); alternative to building PCI-DSS compliance in-house

The thin version is a pricing page. The rich version is a piece that a fintech PM at a marketplace startup would actually cite when choosing a payments stack.

## Example 3 — Refractive surgery

**Thin coverage:**
> lasik, laser eye surgery, lasik cost, is lasik safe

**Rich coverage (EAV):**
- **Entity:** LASIK (Laser-Assisted In Situ Keratomileusis)
- **Attributes:** recovery window (24–48 hours to functional vision, 3–6 months to fully stabilized), ideal candidate age range (21–40), corneal thickness requirement (~500 microns minimum), refractive error range (up to -12D myopia, +6D hyperopia, 6D astigmatism), FDA approval date (1999 for myopia), typical cost (USD 2,000–3,000 per eye in the US)
- **Relations:** alternatives include PRK (better for thin corneas, longer recovery), SMILE (small-incision, flapless, newer), and ICL (implantable collamer lens, for extreme prescriptions); shares the femtosecond-laser flap creation step with Femto-LASIK; reported side effects include dry eye symptoms, halos and starbursts at night, and rare ectasia; contraindicated for keratoconus patients and during pregnancy

Notice how the relations encode medical decision-making. A reader searching "LASIK vs PRK" doesn't get served a keyword match — they get served the page that understands why you'd choose one over the other.

## Example 4 — Dutch corporate law

**Thin coverage:**
> BV oprichten, BV kosten, nederlandse BV

**Rich coverage (EAV):**
- **Entity:** Besloten Vennootschap (BV) oprichten
- **Attributes:** minimum share capital (EUR 0.01 since Flex-BV reform 2012), notary requirement (verplicht — notariële akte), deed language (Nederlands, met optionele Engelse vertaling), registration timeline (typically 1–5 business days after akte), VPB (corporate income tax) rate (19% first EUR 200K, 25.8% above), DGA minimum salary rule (EUR 56,000 in 2026)
- **Relations:** alternatives for solo entrepreneurs include Eenmanszaak (unlimited liability, simpler) and VOF (for partnerships); filed at the Kamer van Koophandel (KvK); governed by Boek 2 Burgerlijk Wetboek; often used as a holding structure above a werk-BV for dividend-routing and liability shielding; contrasts with the German GmbH (EUR 25,000 minimum) and the UK Ltd (GBP 1 minimum, no notary)

This is what a Dutch tax advisor's blog looks like when they're actually writing for fellow professionals. Everything else on the SERP is a repackaged KvK brochure.

## Example 5 — Local service (HVAC)

**Thin coverage:**
> ac repair, air conditioning repair near me, broken ac

**Rich coverage (EAV):**
- **Entity:** Residential AC compressor failure
- **Attributes:** typical symptoms (warm air at vents, hard-start clicking, outside unit humming but not spinning, tripped breaker), diagnostic steps (capacitor test, contactor inspection, amp draw reading, refrigerant pressure check), common root causes (failed run capacitor ~70% of cases, seized bearings, locked rotor, low refrigerant charge starving the compressor), repair vs replace threshold ($1,500+ on a system over 10 years old = replace)
- **Relations:** capacitor failures are the single most common false-alarm "compressor is dead" call; contactors are a $15 part that mimics compressor failure when pitted; R-22 systems (pre-2010) face refrigerant phase-out making major repairs uneconomic; the compressor sits inside the outdoor condenser unit alongside the condenser coil and fan motor

A local HVAC page with this content reads as a real technician talking. A generic "call us for AC repair!" page reads as AI slop, even if it was written by a human.

## Example 6 — Running shoes

**Thin coverage:**
> best running shoes, running shoes for beginners, marathon shoes

**Rich coverage (EAV):**
- **Entity:** Nike Vaporfly 3
- **Attributes:** stack height (40mm heel / 32mm forefoot), carbon plate (full-length ZoomX Flyplate), midsole foam (ZoomX PEBA-based), drop (8mm), weight (~196g men's US 10), outsole (partial rubber, exposed foam for weight savings), durability (~250 km before noticeable foam compression)
- **Relations:** competes directly with Adidas Adios Pro 3 and Asics Metaspeed Sky Paris in the super-shoe tier; successor to the Vaporfly Next% 2; shares the ZoomX foam platform with the Alphafly 3 (which adds Air Zoom pods and more stack); banned briefly in 2020 discussions before World Athletics set the 40mm stack-height rule that the Vaporfly 3 complies with exactly; trainer equivalent in the Nike lineup is the Pegasus Plus

The attributes here aren't trivia — they're the exact things a runner comparing shoes searches for. Stack height, drop, foam type, weight, plate configuration. A generic review that says "it feels springy and fast" ranks for nothing.

## Example 7 — Cooking technique

**Thin coverage:**
> how to sear a steak, best way to cook steak, steak recipe

**Rich coverage (EAV):**
- **Entity:** Reverse-sear method for thick-cut steaks
- **Attributes:** ideal cut thickness (1.5–2.5 inches), oven temperature (225–275°F / 110–135°C), target internal temperature before searing (10–15°F below final doneness), finishing sear temperature (screaming-hot cast iron or carbon steel, 450°F+ surface), total cook time for a 2-inch ribeye (35–50 min + 2 min sear), rest time (minimal — the slow cook acts as the rest)
- **Relations:** contrasts with the traditional sear-first-then-roast method (which produces a gray band under the crust); pairs naturally with dry-brining 24–48 hours ahead; developed and popularized by J. Kenji López-Alt for Serious Eats; works best on ribeye, strip, and thick porterhouse and poorly on thin flat-iron or skirt; competes with sous-vide + sear on results but requires no equipment beyond an oven thermometer

Same topic, completely different semantic density. The thin version gets crowded out by AllRecipes. The rich version ranks because it understands the technique well enough to contrast it against its alternatives.

## How to extract EAV triples from a SERP

When you're doing this for a real page, you're reverse-engineering the triples your competitors already encode. Four steps:

1. **Read the top 3 in full, not just the headings.** Scroll. Read the tables and captions and pull-quotes. This is where the attributes live — headings give you topics, body text gives you values.
2. **List the entities each page names.** Be generous — include products, people, places, standards, dates, technical terms. Sort the entities by how many of the top 3 mention them. Anything 3/3 is mandatory for your page.
3. **For each shared entity, list the attributes the competitors attach to it.** Numerical specs, ranges, thresholds, approvals, dates, comparisons. This is the attribute column of your EAV inventory.
4. **List the relations — the predicates connecting entities.** "Competes with," "is a successor to," "is governed by," "contraindicated in," "powered by." Relations are what tell Google you understand the graph, not just the nodes.

Once you have this inventory, your gap list writes itself. Any entity, attribute, or relation in the competitor set but absent from your page is a gap. Classify it using `gap-classification-rubric.md` and write it into your brief.

## What this unlocks

Pages built with EAV coverage read as domain-expert to NLP models (BERT, MUM, Gemini) and to humans simultaneously. They rank not just for the primary keyword but for the long tail of comparison, spec, and decision queries that cluster around the entity. They're resistant to commodification because the depth is in the relationships, not in phrases you can swap out. And they build topical authority at the site level because every entity you properly encode strengthens the graph for every other page that references it.

This is the payoff of the EAV discipline: you stop writing pages, and start adding nodes and edges to your site's knowledge graph.
