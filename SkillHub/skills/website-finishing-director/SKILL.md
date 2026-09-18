---
name: website-finishing-director
description: "Run a structured 5-pass finishing audit on any website before launch — scoring visual polish, technical foundation, UX completeness, content quality, and cross-device readiness on 100 points. Use when: **Pre-launch** - Final validation before going live; **Post-redesign** - Verify nothing broke during the overhaul; **Client handoff** - Structured proof that the site is ready; **Quarterly review** - Catch accumulated debt; **Single-pass focus** - Run just Pass 2 after a perf sprint"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Website Finishing Director

> Structured 5-pass website finishing audit — from first impression to launch readiness — scored on 100 points. Like painting: primer, base coat, details, clear coat, final inspection. No site ships without a finishing pass.

## When to Use This Skill

- **Pre-launch gate** — Final validation before DNS goes live or traffic is sent
- **Post-redesign audit** — After a visual overhaul, verify nothing regressed
- **Client handoff** — Generate a structured report proving the site meets quality standards
- **Quarterly maintenance** — Catch accumulated UX debt, broken links, stale content
- **Targeted pass** — Run just one pass (e.g., "Pass 2 only" after a performance sprint)

## Methodology Foundation

**Sources**:
- Nielsen Norman Group — Heuristic evaluation framework (10 usability heuristics)
- Google Web Vitals — LCP, CLS, INP thresholds
- OWASP — Security headers baseline
- Oli Gardner / Unbounce — Landing page conversion best practices
- Don Norman — Emotional Design (visceral/behavioral/reflective layers)
- GUIA production memory — 8 shipped websites, documented gotchas across Next.js, Framer Motion, GSAP, Lenis, Railway, Docker

**Core Principle**: A website that passes Lighthouse and has correct meta tags is technically valid but not *finished*. Finishing is the gap between "it works" and "it's ready." It requires evaluating the site as a visitor experiences it — progressive, emotional, cross-device — not as a checklist of individual metrics.

**Why This Matters**: Existing tools (Lighthouse, Screaming Frog, Awwwards) each audit one dimension. No tool combines visual polish + UX completeness + technical foundation + content quality + brand alignment in a sequential, scored workflow. This skill is that tool.

---

## What Claude Does vs What You Decide

> "Claude runs the audit. You decide what ships."

| Claude handles | You provide |
|---------------|-------------|
| Running each pass systematically against the checklist | The live URL or codebase access |
| Scoring each checkpoint with rationale | Context: brand positioning, target audience, launch timeline |
| Classifying issues as P0/P1/P2 | Override decisions (e.g., "P1 is acceptable for MVP") |
| Generating the final report with fix suggestions | Final Go/No-Go judgment |
| Flagging GUIA stack gotchas from production memory | Validation on real devices (Claude can't open Safari) |

**Remember**: This is a centaur workflow. Claude structures the audit rigorously; you validate the verdict with human eyes on real devices.

---

## What This Skill Does

1. **5-Second First Impression Test** — Evaluates clarity, emotional fit, and CTA visibility in the first moments
2. **Technical Foundation Audit** — Performance (Core Web Vitals), SEO basics, security headers, broken links
3. **UX Completeness Check** — Component states, form behavior, animation polish, mobile usability
4. **Content & Brand Validation** — Copy quality, placeholder detection, voice consistency, visual coherence
5. **Cross-Device & Launch Readiness** — Browser testing, OG previews, analytics, 404 page, favicon

## How to Use

### Full website audit before launch
```
I'm about to launch [site URL]. Run a full website-finishing-director audit (all 5 passes).
Brand quadrant: [Warm+Calm / Warm+Active / Cold+Active / Cold+Calm].
Target audience: [who].
```

### Single pass after a specific fix
```
I just optimized performance on [site URL]. Run Pass 2 only (Technical Foundation).
```

### Landing page quick audit
```
Audit this landing page: [URL]. Use the Landing Page profile (passes 1, 2, 4).
```

---

## Instructions

When running this audit, follow the 5 passes in order. Each pass builds on the previous one — foundation before polish. Score each checkpoint, classify issues by priority, then generate the final report.

### Audit Profiles

Not every site needs all 5 passes. Select the profile that matches the project:

| Profile | Passes | When to use |
|---------|--------|-------------|
| **Landing Page** | 1, 2, 4 | Single-page campaign or product page |
| **Full Website** | 1, 2, 3, 4, 5 | Multi-page site with navigation, forms, content |
| **E-commerce** | 2, 3, 5 | Store with cart, checkout, product pages |

Adjust point totals proportionally when using a reduced profile. The Go/No-Go thresholds apply to the percentage score, not raw points.

---

### Pass 1: First Impression (15 points)

*"What does a visitor understand and feel in 5 seconds?"*

Show the homepage (or hero section) for 5 seconds. Answer these 5 questions — 3 points each:

```
## Pass 1 — First Impression (5-Second Test)

### 1. WHAT is this? (3 pts)
Can a visitor identify what the site/product/service IS?
[ ] 3 — Immediately clear, no ambiguity
[ ] 2 — Clear after reading subheadline
[ ] 1 — Vague, requires scrolling to understand
[ ] 0 — No idea what this is

### 2. WHO is it for? (3 pts)
Are there signals identifying the target audience?
[ ] 3 — Obvious demographic/psychographic signals
[ ] 2 — Implied but not explicit
[ ] 1 — Generic ("everyone")
[ ] 0 — Actively confusing (signals wrong audience)

### 3. WHY should I care? (3 pts)
Is the value proposition or benefit visible?
[ ] 3 — Clear benefit, emotionally resonant
[ ] 2 — Feature-focused but understandable
[ ] 1 — Present but buried
[ ] 0 — No value proposition visible

### 4. WHAT do I do next? (3 pts)
Is the primary CTA visible and clear?
[ ] 3 — CTA visible above fold, action-specific text
[ ] 2 — CTA present but generic ("Learn more")
[ ] 1 — CTA below the fold or hard to find
[ ] 0 — No CTA visible

### 5. HOW does it feel? (3 pts)
Does the emotional tone match the brand quadrant?
[ ] 3 — Perfect quadrant match (warm brand = warm design)
[ ] 2 — Mostly aligned, minor dissonance
[ ] 1 — Noticeable mismatch (warm brand + cold design)
[ ] 0 — Opposite quadrant (positioning confusion)

### Pass 1 Score: ___/15

Verdict:
- 12-15: PASS — First impression is clear and emotionally aligned
- 8-11: NEEDS WORK — Visitor gets it, but slowly or with friction
- <8: FAIL — Redesign the above-fold experience
```

**Integration**: Compare the emotional feel against the `web-design-director` quadrant system. If the brand is Warm+Calm but the site feels Cold+Active, that's a P0 regardless of score.

**GUIA gotchas for this pass**:
- Calendly URL hardcoded in CTA instead of `/contact/` page (breaks analytics)
- Mixing warm copy tone with cold UI elements (terracotta palette + monospace font = confusion)

---

### Pass 2: Technical Foundation (25 points)

*"Is the infrastructure solid enough to build on?"*

```
## Pass 2 — Technical Foundation

### Performance (10 pts)

| Metric | Target | Score |
|--------|--------|-------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | 0-3 pts |
| INP (Interaction to Next Paint) | ≤ 200ms | 0-2 pts |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | 0-2 pts |
| Lighthouse Performance score | ≥ 85 | 0-3 pts |

Scoring:
- LCP: 3 = ≤2.5s, 2 = ≤4.0s, 1 = ≤6.0s, 0 = >6.0s
- INP: 2 = ≤200ms, 1 = ≤500ms, 0 = >500ms
- CLS: 2 = ≤0.1, 1 = ≤0.25, 0 = >0.25
- Lighthouse: 3 = ≥90, 2 = ≥85, 1 = ≥70, 0 = <70

### SEO Basics (8 pts)

- [ ] (2 pts) Canonical URLs defined + trailing slash consistent
- [ ] (1 pt) Meta titles unique per page (≤60 chars)
- [ ] (1 pt) Meta descriptions present per page (≤160 chars)
- [ ] (1 pt) Sitemap.xml accessible and valid
- [ ] (1 pt) robots.txt present and correct
- [ ] (1 pt) Structured data present (JSON-LD)
- [ ] (1 pt) Alt text on all images

### Security & Links (7 pts)

- [ ] (2 pts) HTTPS enforced (no mixed content)
- [ ] (2 pts) Security headers present (CSP, X-Frame-Options, HSTS, X-Content-Type-Options)
- [ ] (1 pt) No broken internal links (404s)
- [ ] (1 pt) No broken external links
- [ ] (1 pt) No exposed source maps or debug endpoints in production

### Pass 2 Score: ___/25

Verdict:
- 21-25: SOLID — Ship it
- 16-20: ACCEPTABLE — Fix P0s, ship with P1 backlog
- 11-15: FRAGILE — Significant technical debt
- <11: BROKEN — Do not launch
```

**GUIA gotchas for this pass**:
- `trailingSlash: true` missing in `next.config.js` (caused deindexation on Rental-CRM, Jan 2026)
- `export const metadata` on a `'use client'` component (metadata not rendered server-side)
- Module-level SDK init (Supabase/Stripe) fails at build when env vars missing — lazy-initialize inside functions
- Vercel env vars trailing newline from `echo` — use `printf` instead
- Railway `*.railway.internal` hostnames unreachable during Nixpacks build — use public URLs

---

### Pass 3: UX Completeness (25 points)

*"Does the site handle real-world usage, not just the happy path?"*

```
## Pass 3 — UX Completeness

### Component States (8 pts)

For EACH interactive component (buttons, cards, forms, modals, lists):
- [ ] (2 pts) Loading state — skeleton, spinner, or progressive render
- [ ] (2 pts) Error state — clear message + recovery action
- [ ] (2 pts) Empty state — helpful message, not blank screen
- [ ] (2 pts) Success state — confirmation feedback

Score: deduct per missing state across all components.
8 pts = all states covered. -1 per missing state (cap at 0).

### Forms (6 pts)

- [ ] (1 pt) Client-side validation with clear error messages
- [ ] (1 pt) Server-side validation (not just client)
- [ ] (1 pt) Success feedback after submission (toast, redirect, or inline)
- [ ] (1 pt) Submit button disabled during processing (no double-submit)
- [ ] (1 pt) Spam protection (honeypot, reCAPTCHA, or rate limiting)
- [ ] (1 pt) Privacy policy link near form (GDPR)

### Animation Polish (6 pts)

- [ ] (1 pt) `viewport={{ once: true }}` on scroll animations (no replay on scroll-back)
- [ ] (1 pt) `useGSAP` hook used (not `useEffect`) for GSAP animations
- [ ] (1 pt) `prefers-reduced-motion` respected (disable or reduce animations)
- [ ] (1 pt) No animation blocks content access (content visible even if animation fails)
- [ ] (1 pt) Lenis initialized correctly (not Locomotive Scroll)
- [ ] (1 pt) Exit animations don't cause layout shift

### Mobile Usability (5 pts)

- [ ] (1 pt) Touch targets ≥ 44px (iOS HIG standard)
- [ ] (1 pt) No horizontal overflow / horizontal scroll
- [ ] (1 pt) Font sizes ≥ 16px for body text (prevents iOS zoom)
- [ ] (1 pt) Sticky/fixed elements don't overlap content
- [ ] (1 pt) Scroll behavior works correctly (no scroll-jacking that traps users)

### Pass 3 Score: ___/25

Verdict:
- 21-25: COMPLETE — Real-world usage covered
- 16-20: MOSTLY THERE — Edge cases need attention
- 11-15: INCOMPLETE — Users will hit dead ends
- <11: UNFINISHED — UX not production-ready
```

**GUIA gotchas for this pass**:
- GSAP + React 18 Strict Mode fires animations 2x in dev (use `useGSAP`, not `useEffect`)
- Global CSS `a { color: var(--color-coral) }` overrides Tailwind `text-white` on anchor CTAs — use inline `style={{ color: 'white' }}`
- Framer Motion `AnimatePresence` exit animations break with Next.js App Router
- Too many simultaneous `ScrollTrigger` instances kill mobile performance
- Lenis package name: `npm install lenis` (NOT `@studio-freight/lenis`)

---

### Pass 4: Content & Brand (20 points)

*"Is the content finished, consistent, and on-brand?"*

```
## Pass 4 — Content & Brand

### Copy Quality (8 pts)

- [ ] (2 pts) No placeholder text detected ("Lorem ipsum", "[Your Name]", "Coming soon",
      "example.com", "TODO", empty sections)
- [ ] (1 pt) No spelling or grammar errors
- [ ] (1 pt) Link text is descriptive (not "click here" or naked URLs)
- [ ] (1 pt) CTA copy is specific ("Start free trial" not "Submit")
- [ ] (1 pt) Heading hierarchy is logical (H1 → H2 → H3, one H1 per page)
- [ ] (1 pt) Alt text is descriptive (not "image1.png" or empty)
- [ ] (1 pt) Phone numbers, emails, addresses are real (not placeholder)

### Brand Voice (6 pts)

- [ ] (2 pts) Tone matches brand positioning (warm/cold, formal/casual)
- [ ] (2 pts) Voice is consistent across all pages (same person "speaking")
- [ ] (1 pt) No AI-smoothing markers ("Don't hesitate to contact us",
      "In today's fast-paced world", "It's important to note that")
- [ ] (1 pt) CTAs match the emotional quadrant (warm brand = inviting CTA, not aggressive)

### Visual Consistency (6 pts)

- [ ] (1 pt) Color palette used consistently (no off-brand colors)
- [ ] (1 pt) Typography hierarchy clear (display, heading, body, caption — max 2-3 fonts)
- [ ] (1 pt) Spacing rhythm consistent (not random padding between sections)
- [ ] (1 pt) Icon style uniform (don't mix outline, filled, and emoji)
- [ ] (1 pt) Image treatment consistent (all photos same filter/tone, or all illustrations)
- [ ] (1 pt) Component style consistent (cards, buttons, inputs follow same pattern)

### Pass 4 Score: ___/20

Verdict:
- 17-20: POLISHED — Content is finished and on-brand
- 13-16: GOOD — Minor inconsistencies, shippable
- 9-12: ROUGH — Content needs editing pass
- <9: UNFINISHED — Major content gaps or brand mismatch
```

**GUIA gotchas for this pass**:
- Calendly URL must match the correct professional (Valeria vs Matthieu vs client)
- Mixing warm copy ("We understand your challenges") with cold UI (dark mode, monospace, sharp corners)
- AI-generated copy detection: remove double line breaks before publishing (AI signature on LinkedIn)
- credou.bzh copy direction: mechanism-first, no CV, no parcours/timeline

---

### Pass 5: Cross-Device & Launch (15 points)

*"Does it work everywhere, and is everything ready to go live?"*

```
## Pass 5 — Cross-Device & Launch

### Browser Testing (5 pts)

Test on the 3 major browsers. Score per browser:
- [ ] (2 pts) Safari — renders correctly, animations work, fonts load
- [ ] (2 pts) Chrome — renders correctly, animations work, fonts load
- [ ] (1 pt) Firefox — renders correctly, no major breaks

Per browser, check: layout, animations, fonts, forms, scroll behavior.
Deduct 1 pt per browser with visual bugs. Deduct 2 pts per browser with functional bugs.

### Device Testing (4 pts)

- [ ] (2 pts) Mobile (375px) — full site usable, no content cut off
- [ ] (1 pt) Tablet (768px) — layout adapts, no awkward breakpoints
- [ ] (1 pt) Desktop (1440px) — content doesn't stretch or float in empty space

### Launch Readiness (6 pts)

- [ ] (1 pt) Analytics installed and firing (GA4, Plausible, or equivalent)
- [ ] (1 pt) OG image renders correctly (test with opengraph.xyz or Twitter card validator)
- [ ] (1 pt) 404 page exists and is styled (not default browser/framework error)
- [ ] (1 pt) Favicon present in all sizes (16, 32, 180, 192, 512 — or SVG adaptive)
- [ ] (1 pt) Google Search Console configured (or equivalent)
- [ ] (1 pt) Social preview correct on LinkedIn, Twitter, WhatsApp

### Pass 5 Score: ___/15

Verdict:
- 12-15: LAUNCH READY — Ship it
- 9-11: ALMOST — Fix critical device/browser issues
- <9: NOT READY — Cross-device experience is broken
```

**GUIA gotchas for this pass**:
- Lenis smooth scroll has known issues on Safari — test carefully
- Vercel env vars with trailing newline break OG image URLs
- Docker healthcheck must pass before CI/CD reports success
- `deploy.sh` uses `flock` — no concurrent deploys on VPS
- Resend subdomain DNS: `send.send.<zone>` looks wrong but is correct (Resend adds `send.` prefix)

---

### Step 6: Generate the Final Report

After running all applicable passes, compile the report:

```
## Final Report Template

# Website Finishing Audit: [Site Name]

**URL:** [https://...]
**Date:** [YYYY-MM-DD]
**Profile:** [Landing Page / Full Website / E-commerce]
**Auditor:** [Name] + Claude (website-finishing-director)

---

## Score Summary

| Pass | Name | Score | Max | Status |
|------|------|-------|-----|--------|
| 1 | First Impression | __/15 | 15 | [PASS/NEEDS WORK/FAIL] |
| 2 | Technical Foundation | __/25 | 25 | [SOLID/ACCEPTABLE/FRAGILE/BROKEN] |
| 3 | UX Completeness | __/25 | 25 | [COMPLETE/MOSTLY/INCOMPLETE/UNFINISHED] |
| 4 | Content & Brand | __/20 | 20 | [POLISHED/GOOD/ROUGH/UNFINISHED] |
| 5 | Cross-Device & Launch | __/15 | 15 | [READY/ALMOST/NOT READY] |
| **TOTAL** | | **__/100** | **100** | |

---

## Verdict

| Score Range | Verdict |
|-------------|---------|
| 85-100 | LAUNCH READY |
| 70-84 | CONDITIONAL — fix P0s then ship |
| 50-69 | NEEDS WORK — significant issues |
| <50 | NOT READY — major gaps |

**Override rule:** 1 unresolved P0 = NOT READY, regardless of total score.

**VERDICT: [LAUNCH READY / CONDITIONAL / NEEDS WORK / NOT READY]**

---

## Issues

### P0 — Blockers (must fix before launch)

| # | Pass | Issue | Location | Fix |
|---|------|-------|----------|-----|
| 1 | [1-5] | [Description] | [file:line or URL path] | [Concrete solution] |

### P1 — Important (fix within 1 week of launch)

| # | Pass | Issue | Location | Fix |
|---|------|-------|----------|-----|
| 1 | [1-5] | [Description] | [file:line or URL path] | [Concrete solution] |

### P2 — Nice-to-have (backlog)

| # | Pass | Issue | Location | Fix |
|---|------|-------|----------|-----|
| 1 | [1-5] | [Description] | [file:line or URL path] | [Concrete solution] |

---

## Strengths

- [What the site does well — acknowledge good work]
- [Specific design/technical/content wins]

## Recommendations

1. [Highest-priority improvement]
2. [Second priority]
3. [Strategic suggestion for next iteration]

---

## Sign-off

- [ ] All P0s resolved
- [ ] P0 + P1 resolved (optimal)
- [ ] Stakeholder review completed
- [ ] Go-live date confirmed: ____________
```

---

## Examples

### Example 1: Full Website Audit — credou.bzh

**Context**: Personal brand website for a consultant. Warm+Calm quadrant. Next.js 16, Framer Motion, Lenis. Just completed copy v3 and deployed.

**Input**:
> Run a full website-finishing-director audit on credou.bzh. Brand quadrant: Warm+Calm. Target: decision-makers struggling with AI integration.

**Output**:

# Website Finishing Audit: credou.bzh

**URL:** https://credou.bzh
**Date:** 2026-02-12
**Profile:** Full Website
**Auditor:** Matthieu + Claude (website-finishing-director)

---

## Score Summary

| Pass | Name | Score | Max | Status |
|------|------|-------|-----|--------|
| 1 | First Impression | 13/15 | 15 | PASS |
| 2 | Technical Foundation | 19/25 | 25 | ACCEPTABLE |
| 3 | UX Completeness | 18/25 | 25 | MOSTLY THERE |
| 4 | Content & Brand | 17/20 | 20 | POLISHED |
| 5 | Cross-Device & Launch | 11/15 | 15 | ALMOST |
| **TOTAL** | | **78/100** | **100** | |

---

## Verdict

**CONDITIONAL** — Score 78/100. Fix P0s then ship.

---

## Issues

### P0 — Blockers

| # | Pass | Issue | Location | Fix |
|---|------|-------|----------|-----|
| 1 | 2 | Security headers missing (no CSP, no X-Frame-Options) | `next.config.js` | Add `headers()` config with CSP, X-Frame, HSTS, X-Content-Type |
| 2 | 5 | 404 page is default Next.js error | `/app/not-found.tsx` | Create styled 404 page matching Papier/Encre theme |

### P1 — Important

| # | Pass | Issue | Location | Fix |
|---|------|-------|----------|-----|
| 1 | 2 | eslint.config.js missing | Project root | Add ESLint flat config |
| 2 | 3 | `prefers-reduced-motion` not handled | `globals.css` | Add `@media (prefers-reduced-motion: reduce)` to disable animations |
| 3 | 3 | Skip-to-content link missing | `layout.tsx` | Add visually hidden skip link |
| 4 | 5 | Social preview not tested on WhatsApp | OG image | Verify OG renders on WhatsApp share |

### P2 — Nice-to-have

| # | Pass | Issue | Location | Fix |
|---|------|-------|----------|-----|
| 1 | 4 | "Le plan" section cards could use more varied spacing | `HomeContent.tsx` | Vary vertical padding between card rows |

---

## Strengths

- Copy v3 (articulation bottleneck) is sharp — mechanism-first, no CV padding
- Papier/Encre dual theme is cohesive and on-brand
- Grain texture + borderless cards create genuine warmth (not template-y)
- Edge-rendered OG image is a solid SEO win

## Recommendations

1. Fix security headers (P0) — 15 min task, high security impact
2. Create custom 404 page (P0) — maintain brand experience on dead links
3. Add `prefers-reduced-motion` (P1) — accessibility compliance

---

**Why this works**: The audit catches the gap between "technically deployed" and "actually finished." The site scores well on impression and content but has infrastructure gaps (security headers, 404) that a pure Lighthouse audit would flag separately without prioritization.

---

### Example 2: Landing Page Audit — SaaS Product Launch

**Context**: New SaaS landing page for a productivity tool. Cold+Active quadrant. Single page, no forms, CTA links to waitlist.

**Input**:
> Audit this landing page with the Landing Page profile (passes 1, 2, 4): taskflow.app. Quadrant: Cold+Active. Audience: engineering managers.

**Output**:

# Website Finishing Audit: TaskFlow

**URL:** https://taskflow.app
**Date:** 2026-02-12
**Profile:** Landing Page (Passes 1, 2, 4)
**Auditor:** Product team + Claude (website-finishing-director)

---

## Score Summary

| Pass | Name | Score | Max | Status |
|------|------|-------|-----|--------|
| 1 | First Impression | 9/15 | 15 | NEEDS WORK |
| 2 | Technical Foundation | 22/25 | 25 | SOLID |
| 4 | Content & Brand | 11/20 | 20 | ROUGH |
| **TOTAL** | | **42/60** | **60** | **(70%)** |

---

## Verdict

**CONDITIONAL** — 70% score. P0 in Pass 1 requires attention.

---

## Issues

### P0 — Blockers

| # | Pass | Issue | Location | Fix |
|---|------|-------|----------|-----|
| 1 | 1 | WHAT is this? scored 1/3 — product category unclear in hero | Hero section | Add one line: "Project tracking for engineering teams" above the tagline |
| 2 | 4 | 3 placeholder testimonials with stock photos | Social proof section | Remove section entirely, or replace with real beta user quotes |

### P1 — Important

| # | Pass | Issue | Location | Fix |
|---|------|-------|----------|-----|
| 1 | 1 | CTA says "Get Started" — generic for a waitlist | Hero CTA | Change to "Join the Waitlist" or "Request Early Access" |
| 2 | 4 | AI-smoothing detected: "In today's fast-paced engineering landscape..." | Hero subtitle | Rewrite: direct, specific, no filler |
| 3 | 4 | Feature icons mix filled and outline styles | Features grid | Standardize on one icon style |

### P2 — Nice-to-have

| # | Pass | Issue | Location | Fix |
|---|------|-------|----------|-----|
| 1 | 2 | Structured data missing (no Product or SoftwareApplication schema) | `<head>` | Add JSON-LD SoftwareApplication schema |
| 2 | 4 | Footer copyright says 2025 | Footer | Update to 2026 |

---

## Strengths

- Technical foundation is solid (22/25) — fast, well-optimized
- Dark UI + gradient accents match Cold+Active quadrant perfectly
- Responsive layout works well across breakpoints

## Recommendations

1. Clarify the hero — visitors need to understand the product category in 3 seconds
2. Remove fake testimonials — empty space is better than fake social proof
3. Rewrite CTA to match the actual action (waitlist, not "get started")

---

**Why this works**: The Landing Page profile skips UX completeness (Pass 3) and cross-device (Pass 5), focusing on what matters most for a single page: does it communicate clearly, is the tech solid, and is the content honest? The 70% score flags it as shippable with fixes — the P0s are copy problems, not engineering problems.

---

## Skill Boundaries (Frontier Recognition)

### This skill excels for:
- Pre-launch validation of any website (static, dynamic, SPA, SSR)
- Generating structured audit reports for client handoff
- Catching the "finishing gap" between technically working and truly ready
- Teams using GUIA stack (Next.js, Framer Motion, GSAP, Lenis) — gotchas are baked in

### This skill is NOT ideal for:
- **Deep performance engineering** — Use Lighthouse, WebPageTest, or Chrome DevTools directly
- **Accessibility audit (WCAG compliance)** — This covers basics but isn't a full a11y audit. Use axe-core or WAVE.
- **Security penetration testing** — This checks headers, not vulnerabilities. Use OWASP ZAP.
- **Conversion rate optimization** — Use `landing-page-optimizer` for CRO. This skill checks if the CTA exists, not if it converts.
- **Design direction** — Use `web-design-director` for choosing the visual direction. This skill validates the execution.

### Quality Checkpoints

Before accepting the audit output, verify:
- [ ] All 5 passes (or profile-appropriate passes) have been scored
- [ ] Total points match (15 + 25 + 25 + 20 + 15 = 100 for full audit)
- [ ] Every P0 has a concrete fix (not just "improve this")
- [ ] The verdict respects the override rule (1 P0 = NOT READY)
- [ ] Strengths section acknowledges genuine wins (not just problems)

---

## Iteration Guide

> "First pass catches the obvious. Second pass catches the subtle."

### Recommended Iteration Pattern

| Pass | Focus | Questions to Ask |
|------|-------|------------------|
| **1st audit** | Full sweep | "What's broken? What's missing? What's off-brand?" |
| **2nd audit** (after fixes) | P0 verification | "Are the blockers actually fixed? Did fixes introduce regressions?" |
| **3rd audit** (pre-launch) | Polish | "Would I be proud to share this URL publicly?" |

### Useful Follow-up Prompts

- "Re-run Pass 2 only — I fixed the security headers and 404 page."
- "The brand voice feels inconsistent between the homepage and about page. Deep-dive on Pass 4."
- "Score this against the E-commerce profile — we added a checkout flow."
- "Compare this audit to the previous one and show me what improved."

---

## Learning Curve

| Usage | What You'll Experience |
|-------|----------------------|
| **1st audit** | You discover gaps you didn't know existed (especially states and mobile) |
| **3rd audit** | You start building finishing into your workflow, not just tacking it on |
| **10th audit** | Your sites ship with fewer issues because you internalize the checklist |

**Pro tip**: Run Pass 1 (First Impression) at 50% completion, not just at the end. Catching positioning mismatches early saves redesign time.

---

## Checklists & Templates

### Quick Pre-Launch Checklist (5 min)

```
## Quick Check (non-negotiable minimums)

- [ ] Site loads in < 4s on mobile
- [ ] CTA visible above the fold
- [ ] No placeholder text anywhere
- [ ] No broken links on main pages
- [ ] HTTPS enforced
- [ ] 404 page exists
- [ ] OG image renders

If ALL checked → safe to soft-launch
If ANY unchecked → run full audit
```

### GUIA Stack Checklist (Next.js + Framer + GSAP)

```
## GUIA Stack Finishing Checklist

### Next.js Config
- [ ] trailingSlash: true in next.config.js
- [ ] export const metadata on server components (not 'use client')
- [ ] Lazy SDK init (getSupabase(), getStripe()) — not module-level
- [ ] sitemap.ts + robots.ts present

### Animation
- [ ] useGSAP (not useEffect) for GSAP
- [ ] viewport={{ once: true }} on scroll animations
- [ ] prefers-reduced-motion media query
- [ ] Lenis (not Locomotive Scroll)

### CSS
- [ ] Global a{color} doesn't override CTA text — use inline style if needed
- [ ] No horizontal overflow on mobile
- [ ] Touch targets ≥ 44px

### Deploy
- [ ] Env vars set with printf (no trailing newline)
- [ ] Docker healthcheck passes before success report
- [ ] deploy.sh flock prevents concurrent deploys
```

### Red Flags Checklist

```
## Warning Signs in Your Audit

- [ ] Score is 85+ but something still "feels off" → trust your gut, re-examine Pass 1
- [ ] All passes score well except one pass scores <50% → that pass is a blocker
- [ ] P0 list has more than 3 items → the site isn't ready, period
- [ ] Multiple P2s in the same area → that's actually a P1 (systemic issue)
- [ ] "It works on my machine" for any browser test → test on real devices
```

---

## Integration with Other ClawFu Skills

| Skill | Integration Point |
|-------|------------------|
| **[web-design-director](../web-design-director/)** | Use BEFORE building — determines the emotional quadrant. Pass 1 validates against it. |
| **[design-trends-2026](../design-trends-2026/)** | Pass 4 visual consistency can reference current trend alignment |
| **[minimalist-image-director](../minimalist-image-director/)** | Pass 4 image treatment consistency |
| **[landing-page-optimizer](../../content/landing-page-optimizer/)** | Conversion optimization AFTER this audit passes — CRO assumes the foundation works |
| **[landing-page-copy](../../content/landing-page-copy/)** | Pass 4 copy quality — if copy fails, route to this skill for rewrite |

**Workflow sequence**:
```
web-design-director → [build site] → website-finishing-director → [fix issues] → landing-page-optimizer
(direction)            (code)         (QA/finishing)               (iterate)      (CRO/optimization)
```

---

## References

- Nielsen, Jakob. "10 Usability Heuristics for User Interface Design" (1994, updated 2020) — Foundation for UX completeness checks
- Google. "Web Vitals" — LCP, CLS, INP threshold definitions
- OWASP. "Secure Headers Project" — Security header recommendations
- Gardner, Oli. "101 Landing Page Optimization Tips" (Unbounce) — Pre-launch conversion checklist
- Norman, Don. "Emotional Design" (2004) — Visceral/behavioral/reflective design evaluation
- GUIA Production Memory — `.claude/memory/agents/webdesign.md`, `seo.md`, `devops.md`, `gotchas.md`

## Related Skills

- [web-design-director](../web-design-director/) — Visual direction framework (use BEFORE this skill)
- [design-trends-2026](../design-trends-2026/) — Current visual trends for Pass 4 validation
- [minimalist-image-director](../minimalist-image-director/) — AI photography direction for image consistency
- [landing-page-optimizer](../../content/landing-page-optimizer/) — Conversion optimization (use AFTER this skill)
- [ai-video-qa](../../video/ai-video-qa/) — Sibling QA skill for video content (same scoring philosophy)

---

## Skill Metadata

```yaml
name: website-finishing-director
category: ai-design
subcategory: quality-assurance
version: 1.0
author: GUIA
source_expert: Nielsen Norman Group + Google Web Vitals + OWASP + GUIA Production Memory (8 shipped sites)
source_work: null
difficulty: intermediate
mode: centaur
estimated_value: QA/finishing audit engagement (~1500-3000 EUR per site)
tags: [web-design, qa, audit, finishing, pre-launch, ux, performance, seo, brand, cross-device, scoring]
created: 2026-02-12
updated: 2026-02-12
```

---

*This skill is part of the GUIA Premium Marketing Skills Library — the 201 layer that bridges AI basics and technical implementation.*
