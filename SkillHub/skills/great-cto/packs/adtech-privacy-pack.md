---
name: adtech-privacy-pack
description: US adtech / web-tracking privacy-litigation overlay. Pairs adtech-privacy-reviewer + us-privacy-reviewer.
when_to_use: Site/app loads third-party advertising or analytics tags (Meta Pixel, GA4, TikTok), uses session-replay/heatmaps, streams/recommends video, or handles consumer-health/precise-location data.
applies_to:
  - web-service
  - commerce
  - cms
  - marketplace
  - ai-system
  - mobile-app
---

# Adtech-Privacy Pack

> Loaded when stack/markup has fbevents/Meta Pixel/GA4/GTM/TikTok pixel/FullStory/Hotjar/LogRocket, or ARCH mentions: pixel, session replay, retargeting, VPPA, CIPA, My Health My Data.

## Reviewers

- **adtech-privacy-reviewer** → `TM-adtech-{slug}.md`
- **us-privacy-reviewer** → state-privacy "sale/share" + GPC

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:tracking-consent` | Pre-implementation — no third-party tag fires before consent | security-officer |
| `gate:ship` | Standard | security-officer |

## Required artefacts

| Artefact | Owner |
|---|---|
| Tag inventory (each tag, data received, page, pre/post-consent) | architect |
| Consent manager gating tag loading + GPC honored | senior-dev |
| Standalone VPPA video-tracking consent (not bundled in ToS) | senior-dev |
| CIPA: session-replay/chat consented + vendor service-provider-only | senior-dev |
| MHMDA/Nevada: separate consent + sale authorization for health data; no health-facility geofencing | architect |
| Privacy policy == actual tags (FTC § 5) | security-officer |
