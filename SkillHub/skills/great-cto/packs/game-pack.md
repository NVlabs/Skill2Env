---
name: game-pack
description: Engine decision (Unity/Unreal/Godot/custom), multiplayer netcode patterns (lockstep/rollback/authoritative/P2P), anti-cheat tiers, monetization (IAP/loot box jurisdictions), platform certifications, age ratings (ESRB/PEGI/IARC)
when_to_use: Building single-player or multiplayer games, game engines, game services. Read at architecture time + qa-engineer for performance budgets
applies_to:
  - game
---

# Game Pack

> Extends `game` archetype with engine choice (Unity / Unreal / Godot / custom), multiplayer netcode patterns (rollback / lockstep / authoritative server), anti-cheat, monetization gotchas (loot box / IAP compliance), platform certifications, and age-rating pre-flight.
> Auto-loaded when `archetype: game` is detected in PROJECT.md.
> Also loaded explicitly via `packs: [game-pack]`.

## Why a separate archetype (not `library`)

A game shares almost nothing with a library or SDK:

- **Performance budget**: 60 / 120 / 144 FPS sustained, frame-time variance matters more than throughput
- **Distribution**: Steam / Epic / Xbox / PlayStation / Nintendo / mobile stores — each with its own certification process and rules
- **Multiplayer**: WebSocket / WebRTC / custom UDP at scale, lag compensation, anti-cheat — none of which apply to libraries
- **Monetization**: IAP, loot boxes, battle pass, ads — each with its own legal landmines (Belgium loot-box ban, China gambling rules, COPPA <13)
- **Live-service**: features that break post-launch can lose 80% of DAU in a week
- **Asset pipeline**: textures, models, audio, animations — gigabytes of binary data, version-controlled differently from code

If you're shipping a game, this pack is your reference. If you're shipping a game engine plugin or game-related library, use `library` archetype instead.

## Engine decision

| Engine | Best for | Avoid for |
|--------|----------|-----------|
| **Unity 6** | Indie + AA, mobile, VR, broad platform support, C# | Cutting-edge AAA visuals (Unreal pulls ahead), kernel anti-cheat (Unity has weaker tooling) |
| **Unreal Engine 5** | AAA, photorealism, next-gen consoles, Blueprint+C++ | Lightweight 2D mobile (overkill, big binary size) |
| **Godot 4.x** | 2D, indie, OSS-first, no royalties | Console publishing (limited support; most studios use Unity/Unreal for console) |
| **Custom (Bevy / custom C++)** | Specific perf needs, technical learning | Time-to-market; only justify with a concrete reason |
| **Phaser / PixiJS** (web) | Casual web/HTML5 games, IO games | Anything with serious 3D needs |
| **CocosCreator** | Mobile 2D, China market | Western console publishing |

For new project without strong reason: **Unity 6** if mobile/cross-platform priority, **Unreal 5** if visual fidelity priority, **Godot 4** if OSS / no-royalties priority.

### Team-size sanity check (red flags)

| Team size | Avoid | Why |
|-----------|-------|-----|
| Solo / 2-person | **Unreal 5** | Asset pipeline + C++ ramp eats time-to-prototype; engine fights you alone |
| 3–5 people | **Custom engine** | You will ship the engine, not the game; only justified for a unique tech bet |
| Any size, no console plans | **Console-only engine licenses** (paid Unity Industry, Unreal source access) | Wasted spend |
| Solo / 2-person doing 3D | **AAA-grade 3D in Godot** | Tooling gap is real for 3D; pick Unity 6 or scope down to 2D |

If team size ≤ 5 and target is PC / mobile only, default to Godot 4 (2D) or Unity 6 (3D). Unreal 5 needs ≥ 8 engineers to be net-positive.

## Multiplayer netcode

The hardest engineering problem in games. Pick the model based on your gameplay genre:

### Lockstep (deterministic simulation)

- All clients run same simulation deterministically
- Only inputs are sent over network
- Used by: RTS (StarCraft, Age of Empires), turn-based, fighting games (some)
- **Pros**: tiny bandwidth, fair, replays are free
- **Cons**: any non-determinism (floating point, OS scheduling) breaks it; must wait for slowest player; vulnerable to cheating in revealed-info games

### Rollback netcode

- Predict opponent inputs, simulate forward, rollback + resimulate when truth arrives
- Used by: fighting games (Street Fighter 6, Mortal Kombat), platform fighters
- **Pros**: feels instant locally, masks latency well
- **Cons**: state must be cheaply rollback-able (every frame), O(N) simulation cost
- Tools: GGPO, custom

### Authoritative server (snapshot interpolation)

- Server holds canonical state, sends snapshots to clients
- Clients interpolate between snapshots, predict locally for own player
- Used by: most FPS, MMOs, battle royales, MOBAs
- **Pros**: anti-cheat-friendly (server is truth), scales horizontally, async player counts
- **Cons**: more bandwidth than lockstep, requires server infrastructure
- Tools: Mirror / FishNet (Unity), Replication (Unreal native), Photon, Nakama, custom UDP

### Peer-to-peer relay

- Players connect via NAT traversal (STUN/TURN), one is host
- Used by: small co-op (4-player), couch co-op streamed
- **Pros**: no server cost
- **Cons**: host advantage, host migration is hard, easily cheated
- Tools: Steam P2P, Epic Online Services P2P

For new project: **authoritative server with snapshot interpolation** for anything with > 4 players or anti-cheat needs. Rollback for fighting games. Lockstep for turn-based or RTS only.

### Decision tree (read top-to-bottom, stop at first match)

| If your game is… | Use |
|------------------|-----|
| Turn-based or RTS, ≤ 8 players | **Lockstep** |
| Fighting / platform fighter, 1v1–4p | **Rollback** |
| Co-op PvE, ≤ 4 players, no leaderboards | **P2P relay (Steam P2P / EOS P2P)** with host-authoritative validation |
| Co-op PvE, 5–8 players | **Authoritative server (cheap dedicated)** |
| PvP shooter / MOBA / battle royale, any count | **Authoritative server** |
| MMO / persistent world | **Authoritative server (sharded)** |

**Common mis-pick**: indie 4-player co-op studios reach for "authoritative server" out of habit, then burn 3 months and $2–5k/month on dedicated infra they don't need. For ≤ 4 co-op PvE, P2P relay is fine — cheating only hurts the cheater's friends.

## Anti-cheat

The game industry runs on cheaters thinking they got away with it. Layer your defenses.

### Server-side validation (always do this)

If your client says "I dealt 10000 damage with a base weapon", the server doesn't believe it. Re-simulate critical actions on server:

- Hit detection (raycast on server with rewind)
- Resource gain / loss (server is the bank)
- Inventory mutations
- Unlock progression

The client is a hostile environment. Treat client input as user input — validate everything.

### Client-side anti-cheat (defense in depth)

| Tool | Type | When |
|------|------|------|
| **Easy Anti-Cheat (EAC)** | Kernel-level | Mainstream FPS, Epic-owned, free | Apex Legends, Fortnite |
| **BattlEye** | Kernel-level | Mainstream FPS | PUBG, Rainbow Six |
| **Vanguard** | Kernel-level + always-on | Most aggressive — Riot's | Valorant only |
| **Hyperion** | Process-level | Lighter | Some Roblox |
| **Server-side ML** | Behavior detection | Catches cheats client-side AC misses | Custom; you build it |

**Trade-off**: kernel-level anti-cheat alienates Linux players, breaks on macOS, and is privacy-controversial. For non-competitive games, server-side validation alone is enough.

### Anti-piracy

For paid games:
- **Denuvo** — most aggressive DRM, used by AAA. Slow load times, sometimes cracked anyway. $$$$
- **Steam DRM** — light wrapper, easily cracked but adequate for most
- **Epic Games Store DRM** — similar
- **Custom checksum / online activation** — many games try this; usually cracked

For multiplayer games: piracy is less of an issue because cheaters need a legit account to play online. Single-player games take the bigger hit.

**Reality**: pirated builds are often cracked within 24-72 hours of release. Plan for it. Don't build your business model on DRM holding.

## Monetization — the legal landmines

Free-to-play (F2P) is a $100B+ market. The legal landscape is messy and getting messier.

### IAP (In-App Purchases)

Standard for mobile / F2P:

- iOS: 30% Apple cut (15% if revenue < $1M/year via Small Business Program)
- Android: 30% Google cut (15% on first $1M/year)
- Steam: 30% (drops to 25% over $10M, 20% over $50M)
- Epic Games Store: 12%
- PlayStation / Xbox / Switch: 30% (negotiable for big publishers)

Use **RevenueCat** or **Adapty** to abstract iOS + Android receipts and handle fraud.

### Loot boxes

The most legally fraught monetization in games. As of 2026:

| Jurisdiction | Status |
|-------------|--------|
| **Belgium** | Banned (since 2018) — must remove or geo-block |
| **Netherlands** | Banned for paid loot boxes; tradeable items considered gambling |
| **China** | Must disclose drop rates; banned for under-18 |
| **Japan** | "Kompu gacha" (combination loot boxes) banned since 2012 |
| **South Korea** | Drop rates must be disclosed (since 2024) |
| **UK** | Investigation ongoing; PEGI labels mandatory |
| **Germany** | USK rating system addresses; PEGI must label "in-game purchases" |
| **Brazil** | Disclosure required since 2025 |
| **US states (e.g. Hawaii, Minnesota)** | Various proposed laws |

**Default**: disclose drop rates in-game (open menu shows %), and **geo-block** Belgium/Netherlands or remove loot boxes entirely from those regions.

### Battle pass

Less legally risky than loot boxes — predictable rewards in exchange for premium currency. Standard now (Fortnite, Call of Duty, Apex). Don't gate ranked / competitive features behind it (skill-pay-to-win is a different problem).

### Ads (rewarded video)

Standard for hyper-casual mobile:
- AdMob (Google), Unity LevelPlay (Unity Ads + mediation), AppLovin MAX
- Rewarded video > interstitial (better LTV)
- Avoid in paid games — players paid not to see ads

### Subscription

Increasingly common (Apple Arcade, Game Pass, EA Play). New games can launch direct subscription at $4.99-$9.99/mo. Or sell into platform subscription deals.

### Anti-pattern: dark UX patterns

The EU Digital Services Act + various national laws are catching up to dark patterns:
- Pre-selected expensive currency packs
- Currency conversion designed to hide $ value
- Forced wait timers that can only be skipped with currency
- "Confirm shaming" to push purchases

These can result in fines AND massive negative press. Your monetization can be aggressive, but it must be transparent.

## Platform certifications

Each console has a certification process. Plan months ahead.

### Sony PlayStation (TRC — Technical Requirements Checklist)

- ~150 requirements covering crashes, memory leaks, save files, achievements, network behaviour
- Submit via Partner Portal
- Cert pass typically 3-4 weeks
- Patches require re-cert (faster for minor fixes)

### Microsoft Xbox (XR — Xbox Requirements)

- Similar scope to TRC
- Smart Delivery (one purchase = all gens) is mandatory now
- Game Pass deals are negotiated separately

### Nintendo Switch (Lotcheck)

- Lotcheck is famously strict on save data behaviour, suspend/resume, error messages
- Cert can take 2-6 weeks
- Patches: cert per patch (no fast-track for hotfixes)

### Steam

- No "certification" but Valve does review for malware, miscategorisation
- Submit via Steamworks; review usually < 5 days
- Steam Deck Verified status separate process — recommended for mass-market PC

### Mobile (Apple App Store / Google Play)

- See `mobile-pack.md` for full submission gotchas
- Game-specific: GameCenter / Play Games Services for achievements / leaderboards
- Mobile games face higher rejection risk than utility apps for "duplicate / spam" rules

### Plan: cert lead time matters

For console launch: lock content 6-8 weeks before launch, leave 2-3 weeks for cert + 1 week buffer for failures. Your release date is "cert-pass + N days marketing", not the day you'd like to ship.

## Age ratings

Required by most platforms before submission. Three ratings agencies cover most markets:

| Region | Agency | Notes |
|--------|--------|-------|
| US, Canada | **ESRB** | E, E10+, T, M, AO. AO games can't be on Steam (officially). |
| Europe | **PEGI** | 3, 7, 12, 16, 18. PEGI is widely accepted in EU + UK + Israel + Russia. |
| Germany | **USK** | Required separately — has banned games other regions allow |
| Japan | **CERO** | Required for Japanese release |
| Brazil | **DJCTQ** | Required |
| Korea | **GRAC** | Required, has banned games |

**IARC** (International Age Rating Coalition) lets you fill ONE form and get ratings for ESRB, PEGI, USK, CERO, etc. Use this for indie. Big publishers submit individually for more nuance.

Run age-rating pre-flight before submission:
- Violence depicted
- Sexual content
- Drugs / alcohol depicted
- Gambling simulation (loot boxes count!)
- User-generated content (any UGC = 17+ in some regions)
- Online interactions (raises ESRB to T+ minimum)

## Performance budget

```
Frame rate (target):           60 FPS sustained on baseline device, 144+ on high-end
Frame time variance:           < 16% of frame budget (under 2.5ms variance at 60 FPS)
Memory (PC mid-tier):          < 4 GB system, < 4 GB VRAM
Memory (mobile):               < 1 GB total, no leaks across 1h play
Load time (cold):              < 30s on baseline
Load time (level transition):  < 5s, ideally with progress UI
Network (multiplayer):         < 100ms input lag p95, < 1% packet loss tolerable
Bundle size (mobile launch):   < 150 MB initial install, on-demand assets after
Bundle size (PC):              variable, no hard cap, but optimise patches < 5 GB
```

Profile: Unity Profiler / Unreal Insights / RenderDoc / GPA. Run on baseline device (iPhone XS / GTX 1650 / PS4 / Switch) before every cert.

### Steam Deck Verified — the de-facto indie PC baseline (2026)

Steam Deck has become the indie baseline. If your game ships on Steam, plan for Deck Verified from day 1:

| Category | Requirement |
|----------|-------------|
| Performance | 60 FPS sustained at native res (1280×800), 30 FPS minimum on demanding scenes |
| Memory | < 4 GB system RAM (Deck has 16 GB but shares with GPU; budget conservatively) |
| Input | All actions playable with gamepad — keyboard/mouse must be optional |
| Text | Default text size legible at 7" — minimum 9pt at native res |
| Resolution | 1280×800 (16:10) supported and tested |
| Suspend / resume | Must survive Deck sleep cycle without losing progress |
| Anti-cheat | Linux-compatible — EAC and BattlEye both support Proton; Vanguard does not (don't pick Vanguard if you ship on Deck) |

Verification: SteamOS dev kit or Steam Deck retail unit. Submit for Verified status during EA — getting "Playable" instead of "Verified" costs ~30% of indie sales.

## PC launch milestones (6–18 month indie timeline)

If your team is ≤ 5 and target is Steam launch, this is the standard milestone shape. Adapt durations to scope.

| Milestone | Target | Goals | Block-ship gate |
|-----------|--------|-------|-----------------|
| **Vertical slice** | T - 12 mo | One representative level/loop, polished, demoable | Steam page approved, capsule art locked |
| **Steam Next Fest demo** | T - 9 mo | 30-min demo, 1 hub area, online + offline play | < 1% crash rate across 1000 sessions, Discord set up |
| **Closed beta** | T - 4 mo | Feature complete, ~80% content, IARC questionnaire submitted | Age rating returned, all platforms cert-ready |
| **Open beta / EA launch** | T - 2 mo | Early Access on Steam OR final beta to wishlist | Day-one patch tested, refund-rate plan in place |
| **1.0 launch** | T - 0 | Marketing push live, demo still up | Steam Deck Verified, no P0 bugs, rollback build pre-staged |
| **Post-launch v1.1** | T + 1 mo | Day-30 patch addressing top community issues | Telemetry shows D7 retention ≥ 25% |

**Next Fest is non-optional for indie Steam.** Apply 6 months in advance; participation drives ~40% of pre-launch wishlists for the cohort. Plan demo build separately from main game (different config, separate save format) to avoid post-Fest cleanup pain.

**Wishlist target by 1.0**: 50k+ for "broke even" indie, 100k+ for "ramen profitable." Below 25k → consider delaying or pivoting marketing.

## Live service operations (post-launch)

Live games are 50% game development + 50% live ops. Plan from day 1:

- **Feature flags / remote config** — turn off broken features without patch
- **Server scaling** — autoscale matchmaking, instance servers; prepare for launch traffic spike
- **Patch cadence** — weekly to monthly; community expects regular content
- **Customer support** — moderation, ban appeals, restore inventory after server issues
- **Cheating intelligence** — discover cheats early (Discord servers selling them are public)
- **Roadmap communication** — public roadmap, monthly state-of-the-game posts, transparency about delays

## Compliance defaults for `game` archetype

| Trigger | Add to compliance |
|---------|-------------------|
| Always | `age-rating` (ESRB / PEGI / USK / CERO at minimum), `accessibility` (CVAA US, EU EAA) |
| Online interactions | ESRB T+ minimum, COPPA if under-13 access possible |
| IAP | platform-specific receipt validation, anti-fraud |
| Loot boxes | Belgium/Netherlands geo-block, drop rate disclosure (CN/KR), label per PEGI/USK |
| User-generated content | DSA (EU) reporting + moderation, DMCA (US), CSAM scanning |
| Multiplayer chat | content moderation, COPPA chat restrictions for under-13, GDPR for EU |
| Children's game | COPPA (US), GDPR-K (EU children's privacy), App Store kids category rules |

## Anti-patterns specific to `game` archetype

| Pattern | Why it fails | Fix |
|---------|-------------|-----|
| Trusting client damage / position / inventory | Cheaters trivially exploit | Server-authoritative simulation for everything that affects gameplay |
| Loot boxes shipped to Belgium / NL | Illegal, fines | Geo-block at IP level + payment country, soft-fallback to alternate progression |
| No drop-rate disclosure | Bad faith UX, illegal in CN/KR | Show % in shop UI for all randomised content |
| Hardcoded server IP | Can't migrate / scale / regional fail-over | Service discovery, region routing |
| Save file in cleartext local file | Easy cheating + can corrupt + can't sync to cloud | Encrypted save format, cloud-sync via platform service |
| All assets in one giant bundle | Slow patches, slow downloads | Asset bundles per region / language / DLC, on-demand download |
| Weekly hotfix without rollback plan | Patch breaks live game = revenue + reputation damage | Stage hotfix on internal branch, public beta, then prod; have last-known-good ready |
| Ignoring CCU forecast | Launch day server crash → Twitter disaster | Load test 5× expected peak; have queue / capacity-shed UX ready |
| Dark monetization patterns | EU DSA + national laws, public backlash | Transparent pricing, no forced loops, easy refund flow |
| No accessibility options | EU EAA fines from 2025; CVAA US already in effect | Subtitles, colorblind modes, remappable controls, motion-reduce |

## QA extras provided by this pack

When `archetype: game`, `qa-engineer` automatically runs:

- **FPS / frame-time benchmark** on baseline device
- **Memory profile** across 1h play (no leaks, no growth)
- **Multiplayer netcode test** — latency injection (50ms / 150ms / 300ms / packet loss 5%)
- **Save/load corruption test** — kill process at random, restart, verify save valid
- **Cert pre-flight** — checks platform requirements (TRC / XR / Lotcheck) per declared platform
- **Age-rating self-assessment** — flags content categories for IARC / ESRB / PEGI
- **Geo-compliance scan** — loot boxes off in BE/NL, drop rates disclosed for CN/KR
- **Accessibility audit** — subtitles, colorblind, remappable, motion-reduce

## Recommended `PROJECT.md` for new game project

```yaml
primary: game
archetype: game
project_size: large    # most games are large or enterprise
stack: [unity-6, csharp, multiplayer-mirror, postgres]
team-size: 8
compliance: [age-rating-iarc, esrb, pegi, accessibility-cvaa, accessibility-eaa, coppa]
performance-sla: 60-fps-baseline, multiplayer-input-lag < 100ms p95
qa-extras: [fps-benchmark, memory-leak, multiplayer-latency-injection, cert-preflight, geo-compliance]
packs: [game-pack]
```
