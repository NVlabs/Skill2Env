---
name: ARCH-game
description: Game ARCH template: Engine choice with team-size sanity check, Multiplayer netcode (lockstep/rollback/authoritative/P2P relay), Anti-cheat tier, Performance budget per platform, Steam Deck Verified, Age rating + IARC, Live-service ops, PC launch milestones
when_to_use: Writing ARCH for game archetype (Unity/Unreal/Godot/Phaser/Cocos)
applies_to:
  - game
---

# ARCH-{slug}.md — Game project template

> **Reader:** the engineer joining mid-project who needs to ship next milestone without breaking the existing live build.
> **Source:** `skills/great_cto/templates/ARCH-game.md`. Mandatory for `archetype: game`.
> Cannot ship to a console / Steam without `## Performance Budget` + `## Age Rating` + `## Live-service Operations` (if multiplayer).

## Decision (one sentence)
{What we're building, target platforms, target launch quarter.}

## Engine
- **Engine + version**: {Unity 6 / Unreal 5.x / Godot 4.x / Phaser 3 / Cocos Creator / custom}
- **Why**: {team-size sanity check from game-pack — solo + Unreal is a red flag; 3D in Godot is a red flag}
- **License terms**: {royalty %, revenue threshold, exemption}
- **Render pipeline**: {URP / HDRP / Lumen / Forward+}
- **Scripting language**: {C# / C++ / GDScript / TypeScript}

## Multiplayer netcode (if multiplayer)
| Property | Value |
|---|---|
| Pattern | {Lockstep / Rollback / Authoritative server / P2P relay} |
| Why this pattern | {Per game-pack decision tree — co-op PvE ≤ 4 → P2P relay; PvP shooter → authoritative; fighting → rollback} |
| Library / framework | {Mirror / FishNet / Photon / Nakama / Unreal Replication / custom UDP} |
| Tick rate | {30 / 60 / 120 Hz} |
| Region routing | {single / multi-region / matchmaker} |
| Estimated server cost | {$/CCU/month} |

## Anti-cheat
| Layer | Implementation | When |
|---|---|---|
| Server-side validation | {hit detection rewind, resource bank, inventory mutations} | always (PvP and PvE) |
| Client AC | {EAC / BattlEye / Vanguard / none} | only for PvP with ladder/economy |
| Telemetry | {Sentry / custom analytics / Helika} | always |

For non-competitive games: server-side validation alone is enough. Don't add EAC if you ship on Steam Deck (alienates Linux/Proton users; Vanguard fully blocks).

## Monetization
- Model: {paid up-front / F2P with IAP / live service / subscription}
- IAP: {none / consumable / non-consumable / subscription}
- Loot boxes: {none / pity-timer disclosed / banned in {jurisdictions}}
- Compliance per jurisdiction (game-pack table):
  - Belgium / Netherlands → no real-money loot boxes if random rewards
  - China / South Korea → drop-rate disclosure mandatory
  - PEGI / USK → "in-game purchases (random items)" label

## Platform certifications
| Platform | Cert process | Lead time |
|---|---|---|
| Steam | review (not certification, ~1 week) | 1 week |
| PlayStation | TRC | 4-8 weeks |
| Xbox | XR | 4-8 weeks |
| Nintendo Switch | Lotcheck | 4-8 weeks |
| iOS | App Store review | 24-48h |
| Android | Play review | 24-72h |
| Steam Deck Verified | submit during EA | 2-4 weeks |

## Age rating
- **Target rating**: {ESRB E10+ / PEGI 7 / USK 12 / CERO B}
- **Process**: IARC questionnaire (one form → ESRB + PEGI + USK + CERO + DJCTQ + GRAC) submitted via Steamworks during store-page setup
- **Online interactions**: pushes ESRB to T+ minimum even for E-rated content; PEGI adds "online" descriptor
- **Loot boxes**: PEGI "in-game purchases (random items)" descriptor required; some jurisdictions geo-block
- **Owner**: {publishing-ops role}

## Performance budget
| Platform | Frame budget (ms) | Memory ceiling | Cold-load time | Network |
|---|---|---|---|---|
| Steam Deck Verified (1280×800) | 16.6 ms (60 FPS) | < 4 GB system RAM | < 30 s | n/a |
| GTX 1650 / RX 6500 (1080p) | 16.6 ms | < 4 GB VRAM | < 20 s | n/a |
| High-end PC (1440p / 144 Hz) | 6.94 ms | < 8 GB VRAM | < 15 s | n/a |
| Mobile baseline (iPhone 12) | 16.6 ms | < 1 GB total | < 10 s | n/a |
| Multiplayer | n/a | n/a | n/a | < 100 ms input lag p95 |

Block-ship rules:
- 60 FPS sustained on baseline device → required
- No memory leaks across 1-hour session → required
- Multiplayer rollback recovers within N frames → required (rollback only)
- Suspend/resume on Steam Deck → required (Verified only)

## Live-service operations (post-launch, if multiplayer or seasonal)
- Feature flags / remote config: {LaunchDarkly / Unity Remote Config / custom}
- Patch cadence: {weekly / bi-weekly / monthly / monthly+hotfix}
- Server scaling: {manual / autoscale / managed (AWS GameLift / PlayFab Multiplayer Servers)}
- Cheating intelligence: {Discord lurking / paid feed / Helika reports}
- Roadmap communication: {public Trello / Steam announcements / Discord}
- Customer support: {Helpshift / Zendesk / in-house}

## PC launch milestones (6–18 month indie timeline)
| Milestone | Target | Block-ship gate |
|---|---|---|
| Vertical slice | T-12 mo | Steam page approved, capsule art locked |
| Steam Next Fest demo | T-9 mo | < 1% crash rate across 1k sessions |
| Closed beta | T-4 mo | IARC questionnaire submitted, all platforms cert-ready |
| Open beta / EA | T-2 mo | Day-one patch tested, refund-rate plan |
| 1.0 launch | T-0 | Steam Deck Verified, no P0 bugs, rollback build pre-staged |
| v1.1 post-launch | T+1 mo | Telemetry shows D7 retention ≥ 25% |

## Out of scope (explicit)
- {e.g. cross-play between PC and console — phase 2}
- {e.g. mod support — too risky pre-1.0}
- {e.g. eSports tournament infrastructure — not for this scope}

## Security (multiplayer / save-cloud / IAP)
- IAP receipt validation server-side (never trust client)
- Save-cloud sync uses signed payloads (HMAC); client cannot inflate currency
- Player chat moderation per online-interactions ESRB rule
- Privacy: minor accounts (under-13) get COPPA-compliant signup if game allows them

## Open questions
- {Items to decide before next ARCH revision}
