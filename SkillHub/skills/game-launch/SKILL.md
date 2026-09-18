---
name: "game-launch"
description: >
  Invoke when the user is preparing for game release, needs a launch checklist, store
  submission guidance, go/no-go decision framework, or day-one patch planning. Covers
  Steam, itch.io, Epic, and console submission pipelines. Triggers on: "launch", "release",
  "store submission", "go/no-go", "day-one patch", "launch readiness". Do NOT invoke for
  sprint planning (use game-sprint-plan) or code review (use game-code-review). Part of
  the AlterLab GameForge collection.
argument-hint: "[platform: steam|itch|epic|console]"
model: opus
effort: high
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
version: 1.3.0
---

# AlterLab GameForge -- Pre-Release Launch Pipeline

The distance between "done" and "launched" is longer than most teams expect. And the distance between "launched" and "sustained" is longer still. A game that is feature-complete, bug-free, and fun can still fail because the store page was not optimized, the press kit was missing, the age rating was not filed, or the day-one patch pipeline was not tested. Worse -- a game that launches perfectly can die in week two without a post-launch strategy.

Hades did not become a cultural phenomenon on launch day. It became one through 18 months of Early Access with a meticulously planned patch cadence. Stardew Valley did not stop at 1.0 -- ConcernedApe's free content updates built a community that still plays eight years later. This workflow covers both sides: the exhaustive pre-launch pipeline AND the post-launch operations that determine whether your game survives past the first week.

### Purpose & Triggers

**Invoke this workflow when:**
- The game is entering the final milestone before release and a structured launch plan is needed
- A storefront submission deadline is approaching and the team needs to verify all requirements are met
- Marketing assets need to be prepared and coordinated across platforms
- Legal and compliance requirements (age ratings, privacy policies, licenses) need auditing
- The team needs a go/no-go framework for making the launch decision
- A soft launch or early access release is being planned (same process, adjusted scope)
- Post-launch support infrastructure needs to be established before launch day

**Do NOT use this workflow when:**
- The game is still in active development with significant features incomplete (finish building first)
- You are launching an internal playtest build (use `game-playtest` instead)
- The game is a game jam submission with no commercial intent (streamline to just build validation)

### Critical Rules

1. **Every phase is gated.** Do not advance to the next phase until the current phase is signed off. Skipping a phase to save time is how launches implode. Vampire Survivors launched without a press kit and still succeeded -- but that was 2021 lightning in a bottle, not a replicable strategy.
2. **Storefronts are not optional.** A store page that is missing screenshots, has a vague description, or uses the wrong tags will kill discoverability. The store page IS the game's first impression. Treat it as a design deliverable, not a checkbox.
3. **Legal compliance is not a suggestion.** Missing an age rating or privacy policy can result in the game being pulled post-launch. This is a catastrophic outcome that is entirely preventable.
4. **Plan for failure.** The launch plan must include a rollback strategy. If the answer to "what if launch goes wrong?" is "panic," your launch plan is incomplete.
5. **Day-one patches are expected, not shameful.** Between going gold and launch day, new issues will be found. The question is not "will we need one?" but "how fast can we deploy one?"
6. **Launch day is day one, not the finish line.** Dead Cells shipped its 1.0 and then delivered 6 major content updates over 4 years. Hades had 18 months of Early Access patches before 1.0. Your post-launch strategy matters as much as your pre-launch checklist.
6. **Reference `docs/game-design-theory.md`** for player psychology considerations in storefront presentation and first-time user experience.

### Workflow

**Phase 1: Build Validation**

This is the final technical gate. The game must be provably stable, performant, and complete before any launch activities begin.

**Clean Build Verification:**
- Perform a clean build from source control on a machine that has never built the project before. This catches missing dependencies, local-only files, hardcoded paths, and environment-specific configurations.
- Verify that the build process is documented and reproducible. A build that only one person on the team can create is a single point of failure.
- Confirm the build version string is correct and matches the intended release version.
- If the game has a launcher or auto-updater, verify it points to the correct update servers.

**Automated Test Suite:**
- All unit tests passing: zero failures, zero skipped (unless permanently excluded with documented reason).
- All integration tests passing: game systems interact correctly.
- All platform-specific tests passing: each target platform builds and runs without platform-specific failures.
- Smoke tests for critical paths: new game start, save/load cycle, all main menu options, final boss completion, credits roll.

**Performance Validation:**
- Frame rate meets target on minimum specification hardware. Test on actual min-spec hardware, not a developer workstation set to reduced settings.
- Load times are within budget. First load, level transitions, and respawn times should all be measured and logged.
- Memory usage stays within platform limits across a full play session. Run a 2+ hour continuous play session and track memory allocation. If memory grows monotonically, there is a leak.
- Disk space usage is within platform limits (particularly relevant for console and mobile).
- Network performance (if applicable): latency, bandwidth usage, reconnection handling.

**Bug Triage:**
- Zero P0 bugs (game-breaking: crashes, data loss, progression blockers).
- Zero P1 bugs (severe: major features broken, significant visual glitches, frequent soft locks).
- All P2 bugs (moderate) reviewed and either fixed or explicitly accepted as shippable with documented reasoning.
- P3 bugs (minor: cosmetic issues, edge cases) catalogued for day-one patch consideration.

**Save/Load Integrity:**
- Save files created on the release build load correctly.
- Save files from the most recent public build (if applicable, for early access) migrate correctly.
- Corrupted save file handling: the game recovers gracefully, does not crash, and informs the player.
- Cloud save synchronization works across devices (if applicable).

**Extended Play Session:**
- One team member plays the complete game start-to-finish on the release build. This catches issues that only manifest in long play sessions: memory leaks, cumulative state corruption, softlocks from unusual player choices.
- Record the full session and note any anomalies, even minor ones.

**Phase 1 Gate:** All automated tests pass. Zero P0/P1 bugs. Performance within budget on target hardware. Extended play session completed without critical issues.

---

**Phase 2: Storefront Requirements**

Each storefront has specific asset requirements. Missing or non-compliant assets will delay submission or cause rejection.

**Steam:**
- Header capsule image (920x430)
- Small capsule image (462x174)
- Main capsule image (1232x706)
- Vertical capsule image (748x896)
- Hero graphic (3840x1240) for top of store page
- Library capsule artwork (600x900)
- At least 5 screenshots (1280x720 minimum, 1920x1080 recommended). These should be curated moments that communicate the core experience -- not random gameplay captures.
- At least one gameplay trailer (60-90 seconds, embedded or YouTube link)
- Store description: hook paragraph, feature list, system requirements. Write this as marketing copy, not a design document. Lead with the emotional experience, not the feature list.
- Tag selection: choose tags that match your game accurately. Mis-tagging for visibility backfires when players expecting genre X find genre Y.
- System requirements (minimum and recommended): test these on actual hardware that matches the stated specs.
- Review/community settings: configure discussion boards, review visibility, and beta branch settings.
- Steamworks integration: achievements, cloud saves, trading cards (if applicable), Remote Play Together (if applicable).
- Coming Soon page should be live at least 2 weeks before launch for wishlist accumulation.

**itch.io:**
- Page banner image (630x500 recommended)
- At least 3 screenshots
- Cover image for browse pages (315x250)
- Short description (1-2 sentences for browse) and long description (full page)
- Pricing configuration (paid, PWYW, free)
- Download file upload with platform labels (Windows, macOS, Linux)
- Community settings (comments, devlog, forum)

**Mobile -- App Store (iOS):**
- App icon (1024x1024, no transparency, no rounded corners -- Apple applies the rounding)
- Screenshots for every supported device size (iPhone 6.7", 6.5", 5.5"; iPad Pro 12.9", 11")
- App preview video (15-30 seconds, optional but strongly recommended)
- App name (30 character limit), subtitle (30 character limit), keywords (100 characters total)
- App description (4000 character limit, first 3 lines are critical since the rest is hidden behind "more")
- Privacy policy URL (mandatory)
- Age rating questionnaire (Apple's proprietary system)
- App Store Connect configuration: pricing, availability, in-app purchases, subscription groups
- **Starting April 28, 2026**: Apps must be built with the iOS/iPadOS 26 SDK. Plan your build pipeline accordingly.
- **Enhanced privacy disclosures**: Must clearly state if personal data is shared with third-party AI services. Explicit user permission required before any AI-related data sharing.
- **Accessibility Nutrition Label**: New feature on App Store product pages. Developers share accessibility support info in App Store Connect. Fill this out accurately -- it improves discoverability for accessibility-conscious players.

**Mobile -- Google Play Store:**
- App icon (512x512 PNG, 32-bit with alpha)
- Feature graphic (1024x500) for store feature placement
- Screenshots: minimum 2, maximum 8, at least one for each supported form factor (phone, tablet)
- Short description (80 characters), full description (4000 characters)
- Content rating questionnaire (IARC-based)
- Privacy policy URL (mandatory)
- Data safety section: declare all data collection, storage, and sharing practices
- Target API level must meet Google's current minimum requirement. **As of August 31, 2025, target API level 35 (Android 15) is required.** Non-compliant apps are hidden from users on newer Android versions. Check annually -- this changes.

**Console -- First-Party Certification:**
- **PlayStation (TRC)**: Technical Requirements Checklist. Covers controller behavior, system software interaction, trophy implementation, save data handling, network features. Allow 2-4 weeks for Sony QA review.
- **Xbox (XR)**: Xbox Requirements. Covers achievement implementation, rich presence, controller input, accessibility features. Allow 2-4 weeks for Microsoft certification.
- **Nintendo Switch (Lotcheck)**: Nintendo's compliance testing. Covers button prompts matching controller layout, handheld/docked mode switching, sleep mode handling. Allow 2-4 weeks for Nintendo review.
- All console submissions should be preceded by a pre-certification internal audit against the published requirements checklist.

**Phase 2 Gate:** All storefront assets prepared and reviewed. All submission requirements met per platform. Store pages drafted and reviewed by at least two people (one for accuracy, one for marketing effectiveness).

---

**Phase 3: Marketing Asset Checklist**

These assets should be prepared in parallel with Phase 2 but are tracked separately because they serve different distribution channels.

**Press Kit:**
- Fact sheet: game title, developer, publisher (if applicable), release date, platforms, price, one-sentence description, 100-word description, key features (5-7 bullet points)
- Key art: at minimum the game's primary promotional image at the highest resolution available (300 DPI for print, 72 DPI for web, both versions)
- Screenshot pack: 10-15 curated screenshots showing variety (gameplay, exploration, combat, narrative, environments). Organize by theme. Include both HUD-on and HUD-off versions.
- GIF captures: 3-5 short loops (5-10 seconds each) showing satisfying game moments. These are critical for social media and messaging platforms where video autoplay is unreliable.
- Logo pack: game logo in full color, white, and black versions. SVG or high-res PNG with transparency. Include the developer/studio logo.
- Team bio: short description of the studio, team size, notable previous work, contact information for press inquiries
- All assets should be downloadable from a single URL (Google Drive, Dropbox, or a dedicated press page on the studio website)

**Trailer Production:**
- **Gameplay trailer** (60-90 seconds): shows actual gameplay, not cinematic renders. Players want to see what they will experience. Lead with the most visually impressive or mechanically unique moment. End with a clear call-to-action (release date, platforms, wishlist/pre-order link).
- **Launch trailer** (30-60 seconds): shorter, more emotionally impactful, designed for social media. Can use a mix of gameplay and cinematic moments. Optimized for autoplay-without-audio (use text overlays for key messages).
- **Platform-specific trailers**: some platforms (Steam, App Store, Nintendo eShop) have specific requirements for trailer format, resolution, and content restrictions. Verify before uploading.

**Social Media Launch Assets:**
- Launch announcement posts drafted for each platform (Twitter/X, Instagram, TikTok, Reddit, Discord, YouTube Community)
- Hashtag strategy: primary game hashtag, genre hashtag, event hashtags (if launching during a festival)
- Community notification plan: Discord announcement, mailing list, Steam update post
- Launch day posting schedule: coordinate timing across platforms for maximum reach

**Press Outreach:**
- Press/media list: minimum 50 relevant outlets, YouTubers, streamers, and journalists. Prioritize those who cover your genre.
- Review code distribution: prepare Steam keys, console codes, or direct builds for press. Use a key management service (Keymailer, Woovit, or manual spreadsheet tracking).
- Embargo management: set a clear embargo date and communicate it explicitly. Standard practice is to lift the embargo 1-3 days before launch to allow reviews to publish and drive wishlists.
- Press outreach email: personalized (not mass-blast), concise, includes a press kit link, key/code, and embargo date. Send 2-3 weeks before launch.

**Phase 3 Gate:** Press kit complete and hosted. All trailers produced and uploaded. Social media posts drafted and scheduled. Press outreach initiated with embargo communicated.

---

**Phase 4: Compliance and Legal**

This phase is non-negotiable. Skipping or deferring compliance tasks creates legal liability and storefront removal risk.

**Age Rating:**
- **ESRB** (North America): submit content questionnaire through ESRB's online tool. Processing time: typically 1-3 business days for digital-only releases. Required for major storefronts selling in the US.
- **PEGI** (Europe): submit through the IARC (International Age Rating Coalition) portal. Most digital storefronts use IARC for automated PEGI ratings.
- **CERO** (Japan): required for any release in Japan. Longer processing time (2-4 weeks). Submit well in advance.
- **USK** (Germany): handled through IARC for digital releases.
- Retain rating certificates for all regions where the game will be sold.

**Accessibility Statement:**
- Document the accessibility features the game supports: remappable controls, colorblind modes, subtitle options, screen reader support, difficulty options, motor accessibility settings.
- Reference WCAG 2.1 AA guidelines and the Game Accessibility Guidelines (gameaccessibilityguidelines.com).
- Be honest about what is NOT supported. An incomplete but honest accessibility statement is far better than a fabricated comprehensive one.

**Privacy Policy:**
- Mandatory for any game that collects ANY data (including analytics, crash reports, cloud saves, or account creation).
- Must specify: what data is collected, how it is used, who it is shared with, how long it is retained, and how players can request deletion (GDPR right to erasure).
- Must be accessible from within the game (typically linked from the settings or main menu).
- If the game targets players under 13 (ESRB E or E10+), COPPA compliance is mandatory (parental consent for data collection).

**EULA / Terms of Service:**
- Required for online-enabled games. Recommended for all commercial releases.
- Cover: license grant, restrictions, limitation of liability, dispute resolution, termination conditions.
- If the game has user-generated content, the EULA must address content ownership and moderation rights.

**Copyright and License Verification:**
- Audit ALL third-party assets: music, sound effects, fonts, middleware, textures, models.
- Verify license terms for every asset: is commercial use permitted? Is attribution required? Are there revenue thresholds?
- Check all middleware licenses: physics engines, networking libraries, UI frameworks, analytics SDKs. Some have per-title or revenue-based licensing.
- Open-source license compliance: if the game uses any open-source code, verify license obligations. MIT and BSD are permissive. GPL requires source code disclosure. Apache 2.0 requires a NOTICE file.
- Create a credits screen or text file that includes all required attributions.

**Phase 4 Gate:** All age ratings obtained. Privacy policy published and accessible in-game. EULA reviewed by someone with legal knowledge (ideally a lawyer). All third-party assets verified for license compliance. Credits complete.

---

**📊 Market Context**

Understanding the competitive landscape is essential for setting realistic launch expectations and calibrating your marketing effort. These numbers are sobering but necessary:

- **20,017 games** were released on Steam in 2025 alone. Your game is competing for attention with roughly 55 new releases every single day.
- **83% of those games earned less than $10,000** in their first year. The long tail is extremely long.
- **40% did not recoup the $100 Steam Direct listing fee.** Nearly half of all releases are effectively invisible to the market.
- **Minimum 7,000-10,000 wishlists** are needed for meaningful algorithmic visibility on launch day. Steam's algorithm rewards momentum -- games that sell quickly in the first 48 hours get promoted to more storefronts and recommendation feeds. Below this wishlist threshold, the algorithm largely ignores your game.
- **Top 1% of indie titles earn 90% of total indie revenue.** The distribution is winner-take-most, not winner-take-all, but the concentration is extreme.
- **70% indie financial failure rate.** Seven out of ten commercial indie games do not earn enough to fund the next project. This is not a reason to quit -- it is a reason to plan marketing as seriously as development.

These numbers are not meant to discourage. They are meant to ensure that your launch plan includes sufficient marketing effort, realistic revenue projections, and a clear understanding of what "success" means for YOUR project. A game that sells 500 copies and funds a game jam follow-up is a success by one measure. A game that sells 5,000 copies but needed to sell 50,000 to break even is a failure by another. Define your success threshold before launch day.

---

**⚖️ Regulatory Compliance Checkpoint**

Beyond age ratings and privacy policies, the regulatory landscape for games is expanding rapidly. Review each of these for applicability to your title:

- **EAA (European Accessibility Act)**: Enforceable since June 2025. Applies to games with communication features (chat, voice) or e-commerce features (in-game purchases) sold in the EU. Requires accessible alternatives for core interactions. Non-compliance can result in market access restrictions within the EU.
- **CVAA (21st Century Communications and Video Accessibility Act)**: Text and voice chat features must be accessible to players with disabilities. Applies to games distributed in the US with communication functionality. Fines up to $1.4M per violation. Covers real-time text, captioning, and UI navigability for communication features.
- **COPPA (Children's Online Privacy Protection Act)**: **CRITICAL -- Compliance deadline April 22, 2026 (IMMINENT).** The FTC's final COPPA Rule amendments expand "personal information" to include biometric identifiers. New requirements: a formal information security program is now mandatory, and separate parental consent is required for third-party data disclosures not "integral" to the service. If your game could reasonably attract children (E or E10+ rating, cartoon art style, educational content), COPPA compliance is mandatory. Review your data collection practices against the updated rule immediately.
- **PEGI 2026 Update**: Effective June 2026. Applies to newly submitted games only. Games containing loot box mechanics receive a minimum PEGI 16 rating. Games containing NFT or blockchain integration receive an automatic PEGI 18 rating. Additionally: time-limited offers (battle passes, seasonal items) receive a minimum PEGI 12 rating. Daily quests and login streaks receive a minimum PEGI 7 with a new engagement mechanics descriptor. Unrestricted communication features (no block/report system) receive an automatic PEGI 18 rating. Plan your monetization model and social features with these rating implications in mind. **Note:** ESRB has explicitly rejected adopting PEGI's interactive risk category approach, stating it "could be confusing if non-content related features influence rating category assignments." North American ratings remain content-only.
- **ESA Accessible Games Initiative**: 24 standardized accessibility tags now live on Xbox storefronts (console, PC, mobile, web). Founding members: EA, Google, Microsoft, Nintendo of America, Ubisoft. Additional members: Amazon Games, Riot, Square Enix, Warner Bros. Filling these tags accurately improves discoverability among accessibility-conscious players and demonstrates good faith compliance with emerging accessibility standards. Other storefronts are expected to follow Xbox's implementation.
- **Steam AI Disclosure (January 2026 Three-Tier Framework)**:
  - **Pre-generated AI content**: AI assets baked into game files (textures, art, voice lines, lore text). Must be flagged in the store page content descriptor.
  - **Live-generated AI content**: AI creating content at runtime (dynamic NPC dialogue, procedural quests). Must have safety guardrails preventing illegal/offensive output AND a player reporting mechanism.
  - **Developer tools**: Code assistants, debugging tools, internal pipeline AI. **Explicitly exempt from disclosure.** Using AI for development workflow does not require storefront disclosure.
  - Document your AI usage tier in `@templates/ai-content-policy.md` to ensure correct disclosure per storefront.
- **itch.io AI Disclosure**: Generative AI content must be tagged explicitly -- this includes hand-edited AI outputs (editing AI-generated art does not exempt it from disclosure). Non-tagged AI content is delisted from browse and search. AI-tagged projects appear on a segregated "AI Assisted" browse page, which effectively reduces discoverability. Mass-produced AI pages are treated as spam. Tag requirements apply to both the game page metadata and the game description.
- **Console Certification**: Each first-party platform (Sony, Microsoft, Nintendo) requires a dedicated certification pass that takes 2-4 weeks. Plan your submission timeline to include at least one rejection-and-resubmission cycle. First submissions rarely pass on the first attempt. Budget 4-8 weeks total for console certification in your launch timeline.

Review this checklist with your team (or yourself, for solo devs) at least 8 weeks before your target launch date. Regulatory requirements that surface at the last minute are the most common cause of preventable launch delays.

---

**Phase 5: Day-One Patch Planning**

The build you submit for certification or storefront review is almost never the build players will experience on day one. Between submission and launch, issues will be found. Plan for this.

**Known Issues List:**
- Compile a list of every known issue that shipped in the gold build. Categorize by severity and player visibility.
- Mark which issues will be addressed in the day-one patch and which are accepted as-is (with reasoning).
- This list is also valuable for community management -- if players report a known issue on launch day, the support team can respond immediately with "We're aware of this and a fix is included in the day-one patch."

**Day-One Patch Scope:**
- Define the patch contents BEFORE launch, not reactively on launch day.
- Typical day-one patch scope: bug fixes found during certification period, final balance tuning based on late playtests, localization corrections, last-minute performance optimizations.
- Do NOT use the day-one patch to add features. Feature additions belong in a post-launch update, not a patch.
- Test the day-one patch through the same validation process as the gold build (Phase 1, abbreviated). A day-one patch that introduces new bugs is worse than no patch.

**Hotfix Process:**
- Establish the emergency hotfix pipeline: code fix, build, test, deploy. What is the minimum time from "critical bug reported" to "fix live on all platforms"?
- For PC (Steam): hotfixes can typically be deployed within hours. Document the process for pushing a Steam build update.
- For console: hotfixes must go through certification (abbreviated fast-track process if the issue is severe). Know each platform's expedited certification process and contact.
- For mobile: App Store review can take 24-48 hours. Google Play is typically faster (hours). Factor this into your response time estimates.
- Designate who has authority to approve an emergency hotfix deployment. This should not require a full team meeting -- one decision-maker with 24/7 availability on launch week.

**Monitoring Infrastructure:**
- Crash reporting: integrate a crash reporting service (Sentry, Backtrace, Crashlytics, or engine-native). Verify it is active in the release build.
- Analytics: basic telemetry for player progression, session length, and drop-off points. This data is invaluable for post-launch balance tuning and content planning.
- Community sentiment tracking: monitor Steam reviews, social media mentions, Discord activity, and Reddit posts. Assign a community manager or team member to this role for launch week.
- Server monitoring (if applicable): dashboard for player count, server load, error rates, and latency. Alert thresholds configured for anomalous behavior.

**Phase 5 Gate:** Known issues list complete. Day-one patch scoped and tested. Hotfix pipeline tested end-to-end (deploy a test patch to a staging environment). Monitoring infrastructure active and verified.

---

**Phase 6: Go/No-Go Decision**

This is the final gate. The launch decision is made collectively with full visibility into the state of every prior phase.

**Checklist Review:**
- Each phase owner presents their completion status: fully complete, complete with exceptions (list them), or incomplete (list blockers).
- All exceptions are reviewed and explicitly accepted or escalated.
- Any incomplete phase is a potential launch blocker. The team must agree that the risk of launching with the incomplete item is acceptable.

**Risk Assessment:**
Evaluate the following risk categories:

| Risk Category | Question | Impact if Realized |
|--------------|----------|-------------------|
| Technical | Could the game crash on common hardware configurations? | Reviews destroyed. Refund spike. |
| Performance | Could frame rate drop below acceptable on min-spec? | Negative first impressions. Steam review bombing. |
| Content | Is there offensive, misleading, or missing content? | PR crisis. Storefront removal. |
| Legal | Are there unresolved licensing or compliance issues? | DMCA takedown. Legal liability. |
| Server (if applicable) | Could launch-day traffic overwhelm infrastructure? | Players unable to play. Refund requests. |
| Marketing | Is the game discoverable on the storefront? | Low sales despite game quality. |

For each risk, assign likelihood (Low/Medium/High) and impact (Low/Medium/High). Any High-High risk should be a launch blocker unless explicitly accepted by the team lead.

**Rollback Plan:**
Define what happens if launch goes catastrophically wrong:
- Can the storefront listing be taken down temporarily? What is the process?
- Can a broken build be reverted to the previous version? How quickly?
- Who communicates with players? What is the messaging? Draft a template post for "we are aware of issues and are working on a fix."
- At what point is a launch "aborted" versus "rough but proceeding"? Define the threshold.

**Launch Day War Room:**
- Designate who is on-call for launch day and the 48 hours following. Cover all time zones if the team is distributed.
- Establish communication channels: primary (Slack/Discord channel), escalation (phone calls), and public (social media, community forums).
- Define the escalation path: who makes the call to deploy a hotfix? Who makes the call to pull the build?
- Schedule check-in points: launch +1 hour, +4 hours, +12 hours, +24 hours, +48 hours. At each check-in, review crash reports, player feedback, sales data, and server health.

**The Decision:**
- **GO**: All phases complete (or complete with explicitly accepted exceptions). No High-High risks. Rollback plan in place. War room staffed.
- **CONDITIONAL GO**: Launch proceeds but with specific conditions. Example: "GO, contingent on the day-one patch deploying successfully by 6 AM launch day." Define what happens if the condition is not met.
- **NO-GO**: One or more launch blockers remain unresolved. Identify the new target date and the path to resolution. Communicate the delay transparently -- a delayed game that launches well is remembered more fondly than a rushed game that launches broken.

---

**Phase 7: Post-Launch Operations**

Launch day is the beginning, not the end. The first 30 days after release determine whether your game builds momentum or fades into the Steam graveyard. This phase covers the operational cadence that sustains a live game.

**Patch Cadence Planning**

Define three distinct update tiers with different release cycles:

```
PATCH CADENCE MODEL
-------------------------------------------------
HOTFIXES (days 1-7 post-launch, then as needed):
  Scope: Crash fixes, progression blockers, data loss bugs, critical
  balance breaks (one weapon doing 10x intended damage)
  Turnaround: 24-72 hours from report to live
  Process: Fix → abbreviated QA → deploy → verify
  Communication: "We are aware. Fix incoming." posted within 2 hours
  of confirmed report. Players tolerate bugs. They do not tolerate silence.

CONTENT PATCHES (every 2-4 weeks for first 3 months):
  Scope: Balance tuning based on live data, quality-of-life improvements,
  bug fixes batched from the tracker, minor content additions (new items,
  cosmetics, challenges)
  Turnaround: 1-2 sprint cycles
  Process: Plan → build → QA → staging → deploy → monitor
  Communication: Patch notes published 24 hours before deployment.
  Write patch notes for players, not developers. "Sword damage reduced
  15%" means nothing. "The Iron Sword was trivializing mid-game bosses,
  so we brought its damage closer to other tier-2 weapons" tells a story.

  Dead Cells' patch cadence: biweekly during Early Access, monthly after
  1.0, with each update clearly themed (the "Rise of the Giant" DLC,
  the "Bad Seed" expansion). Every patch had a narrative identity.

MAJOR UPDATES (every 3-6 months):
  Scope: New content (areas, enemies, bosses, mechanics), system overhauls,
  seasonal events, paid DLC
  Turnaround: Full milestone planning cycle
  Process: Design → prototype → build → extended QA → marketing push → deploy
  Communication: Announce 2-4 weeks in advance with trailer or dev blog.
  Time major updates with Steam sales for maximum visibility.

  Stardew Valley model: free major updates as community-building investment.
  ConcernedApe shipped 1.1, 1.2, 1.3, 1.4, and 1.5 as free updates over
  5 years, each one reigniting press coverage and sales. The free updates
  generated more revenue through base game sales than paid DLC would have.
-------------------------------------------------
```

**Community Management Strategy**

Your community is your most powerful marketing channel and your most dangerous risk vector. Manage it deliberately.

```
COMMUNITY CHANNELS (priority order for most indie games)
-------------------------------------------------
Discord:
  Set up BEFORE launch. Have channels for: announcements, bug reports,
  feedback, general discussion, fan art/content. Assign moderators.
  Respond to bug reports within 4 hours during launch week.
  Run a "known issues" pinned post updated in real-time on launch day.

Steam Forums:
  Monitor daily for the first month. Steam forum sentiment directly
  influences store page visibility. Respond to negative posts with
  empathy and specifics -- "We hear you. This is on our radar for
  the next patch" turns a detractor into a watcher.

Reddit:
  Post launch announcement in relevant subreddits (r/indiegaming,
  genre-specific subs). Be present in comments. Do NOT astroturf.
  Reddit detects and punishes corporate-feeling engagement instantly.

Twitter/Social:
  Share GIFs of satisfying moments, patch previews, player
  achievements. The Vampire Survivors social strategy was almost
  entirely player-generated content retweets -- free, authentic,
  and more effective than any marketing campaign.
-------------------------------------------------
```

**Metrics Monitoring Dashboard**

Track these metrics daily for the first 30 days, weekly after:

```
POST-LAUNCH METRICS
-------------------------------------------------
Retention:
  D1 retention (% who play again within 24 hours): Target 40%+
  D7 retention: Target 20%+
  D30 retention: Target 10%+
  If D1 < 30%, the first-time experience has a critical problem.
  If D7 drops sharply from D1, mid-game content is failing.

Engagement:
  Median session length: Compare to your design target
  Sessions per week per active player
  Completion rate: % who reach credits (for narrative games)
  Compare to Hades benchmarks: ~20 hours median to first clear

Revenue (if commercial):
  Daily revenue and 7-day moving average
  Revenue per user (RPU) by acquisition source
  Refund rate: above 10% is a red flag, above 20% is a crisis
  Wishlist conversion rate on launch day: industry average ~15-20%

Sentiment:
  Steam review score: track daily. Below 70% "Mixed" threshold
  triggers a community response plan.
  Review keyword frequency: what are players praising/complaining about?
  Net Promoter Score from in-game surveys (if implemented)

Stability:
  Crash rate: target < 0.5% of sessions
  Average FPS across hardware tiers
  Error log volume (trending up = new bugs introduced by patches)
-------------------------------------------------
```

**Post-Launch Content Roadmap Template**

Draft this BEFORE launch. It keeps the team focused and gives the community something to look forward to.

```
POST-LAUNCH ROADMAP
-------------------------------------------------
Month 1: Stability & Balance
  - Hotfixes for launch issues
  - Balance pass based on live data (not dev intuition)
  - Quality-of-life improvements from community feedback
  - "Thank you" patch with 1-2 small community-requested features

Month 2-3: First Content Update
  - [Themed content addition: new area/mode/characters]
  - Major balance overhaul if needed
  - Accessibility improvements from player feedback

Month 4-6: Major Content Drop
  - [Significant expansion: new mechanics, story content, or game mode]
  - Align with a Steam sale or seasonal event for visibility
  - Press outreach for "now with [new feature]" coverage

Month 6-12: Sustained Operations or Sunset
  Decision point: Is the game growing, stable, or declining?
  - Growing: Plan next content year, consider DLC or expansion
  - Stable: Maintain with quarterly patches, shift team to next project
  - Declining: Ship a final "definitive edition" patch, communicate
    honestly with community, redirect resources

The Hades model: 10 major content updates during Early Access,
each one adding weapons, characters, story content, and systems.
Each update had a themed identity and generated fresh press coverage.
By 1.0, the game had 18 months of community investment behind it.
-------------------------------------------------
```

---

### Output Format

```
## Launch Readiness Report: [Game Title]
## Target Launch Date: [YYYY-MM-DD]
## Report Date: [YYYY-MM-DD]
## Report Author: [Name/Role]

### Executive Summary
[3 sentences: Overall readiness state, biggest remaining risk, recommendation (GO/CONDITIONAL GO/NO-GO)]

### Phase Completion Status

| Phase | Status | Exceptions | Owner |
|-------|--------|-----------|-------|
| 1. Build Validation | Complete / With Exceptions / Incomplete | [list] | [name] |
| 2. Storefront Requirements | Complete / With Exceptions / Incomplete | [list] | [name] |
| 3. Marketing Assets | Complete / With Exceptions / Incomplete | [list] | [name] |
| 4. Compliance & Legal | Complete / With Exceptions / Incomplete | [list] | [name] |
| 5. Day-One Patch | Complete / With Exceptions / Incomplete | [list] | [name] |

### Blocking Issues
| ID | Issue | Phase | Severity | Resolution Path | ETA |
|----|-------|-------|----------|----------------|-----|
| L1 | [desc] | [phase] | Blocker | [plan] | [date] |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation | Accepted? |
|------|-----------|--------|-----------|-----------|
| [risk] | H/M/L | H/M/L | [plan] | Y/N |

### Rollback Plan
- Build reversion process: [description]
- Storefront takedown process: [description]
- Public communication template: [drafted message]
- Abort threshold: [criteria]

### War Room Configuration
- On-call team: [names and roles]
- Communication channels: [primary, escalation, public]
- Check-in schedule: [times]
- Escalation path: [who decides what]

### Post-Launch Operations Plan
- Patch cadence: [hotfix/content/major schedule]
- Community channels: [platform list with owners]
- Metrics dashboard: [tool and key metric targets]
- Content roadmap: [month-by-month plan]

### Decision: [GO / CONDITIONAL GO / NO-GO]
**Conditions (if CONDITIONAL GO):** [list]
**Reasoning:** [2-3 sentences]
**Next Steps:** [immediate action items]
```

### Quality Criteria

- **Phase completeness**: Every phase has been addressed, even if the conclusion is "not applicable to this project" (with reasoning).
- **No hand-waving**: Every exception and every accepted risk is explicitly documented with reasoning. "We'll figure it out" is not a valid entry in a launch readiness report.
- **Rollback plan tested**: The rollback plan is not theoretical -- it has been tested in a staging environment. A rollback plan that has never been executed is a hope, not a plan.
- **War room staffed**: Every critical function (engineering, community management, platform relations) has a named individual on-call with confirmed availability.
- **Legal verification complete**: No third-party asset remains unverified. No compliance requirement remains unmet. Zero ambiguity in this area.
- **Post-launch plan exists**: Patch cadence defined, community channels established, metrics dashboard configured, content roadmap drafted. A launch without a post-launch plan is a game with a one-week lifespan.
- **Decision traceability**: The go/no-go decision can be traced back to specific completion states and risk assessments. A future post-mortem should be able to reconstruct exactly what was known at decision time.

## MCP Integration

The launch workflow connects to MCP servers for release management, marketing asset creation, press outreach, and deployment -- enabling a coordinated launch pipeline from a single session.

### Connected MCP Servers

| MCP Server | Launch Use | How It Helps |
|---|---|---|
| **GitHub** (connected) | Release management | Create release tags and GitHub Releases with changelogs, manage the day-one patch branch, track launch-blocking issues with milestone labels, coordinate the hotfix pipeline through PR workflow |
| **Gmail** (connected) | Press outreach | Draft and send personalized press outreach emails with press kit links, embargo dates, and review codes. Manage follow-up threads with journalists and streamers. |
| **Canva** (connected) | Marketing assets | Generate store page graphics, social media launch announcements, press kit key art variations, and launch day countdown assets |
| **Vercel** (connected) | Web deployment | Deploy the game's marketing site, press kit page, or web game builds. Useful for companion apps, community portals, and web demo deployments. |
| **Cloudflare** (connected) | CDN and storage | Configure R2 storage for downloadable builds and press kits, set up D1 databases for leaderboards or community features, manage CDN caching for game assets served via web |
| **Slack** (connected) | War room coordination | Post launch status updates to the team channel, coordinate the war room check-in schedule, distribute crash report alerts and sentiment monitoring summaries |
| **Notion** (connected) | Launch checklist tracking | Maintain the launch readiness report as a structured Notion page with phase completion status, blocking issues, and risk assessments queryable by the team |

### Example Workflows

**Release Tagging and Changelog:**
1. Use GitHub MCP to create a release tag from the gold build commit
2. Generate a changelog from merged PR descriptions since the last release
3. Create a GitHub Release with the changelog, linking to known issues and day-one patch scope
4. After the day-one patch deploys, update the release notes with patch contents

**Press Kit Distribution:**
1. Use Canva to generate store page capsule images and social media announcement graphics
2. Draft personalized press outreach emails via Gmail MCP with press kit download links and embargo dates
3. Deploy the press kit page to Vercel for a clean, branded download experience
4. Track responses and follow up with interested outlets through Gmail threads

**Launch Day War Room:**
1. Post the launch status template to Slack at launch +0 hours
2. Monitor GitHub for incoming bug reports tagged as P0/P1
3. At each check-in interval (+1h, +4h, +12h, +24h, +48h), compile crash report summaries and sentiment data
4. Post updated status to Slack and Notion with current risk assessment
5. If a hotfix is needed, manage the PR and deployment through GitHub MCP

### Example Use Cases

1. "Our indie game is feature-complete and we want to launch on Steam in 6 weeks. Walk me through the full launch pipeline and help me build a timeline."
2. "We're submitting to the App Store for the first time. What are the specific requirements we need to meet, and what are the common rejection reasons to avoid?"
3. "Our game launches next Friday and we just found a significant bug. Help me evaluate whether this is a launch blocker or a day-one patch item."
4. "We need to prepare a press kit for our upcoming release. What should be in it and how should it be organized?"
5. "We're debating whether to delay our launch by two weeks to fix remaining bugs or ship on time with a day-one patch. Help me frame this as a go/no-go decision with a proper risk assessment."
6. "We launched last week and reviews are mixed. Help me build a post-launch operations plan with patch cadence, community response strategy, and a content roadmap to turn the reviews around."
