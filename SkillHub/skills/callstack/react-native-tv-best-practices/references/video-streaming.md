---
title: Video Streaming on TV
impact: HIGH
tags: video, streaming, drm, hls, dash, widevine, fairplay, tv-platforms
---

# Video Streaming on TV

Use this reference to choose the TV platform playback path and to classify playback failures by protocol, DRM, decoder, or memory pressure.

## Quick Reference
- Pick protocol/DRM per target platform; do not assume one stream package covers every TV device
- Verify hardware DRM level and decoder capability before changing React player controls
- Tear down unused preview/player instances before starting another stream
- Keep video buffer sizing conservative on 1-2 GB TV devices

## Pick DRM/Protocol by TV Platform

| Platform | Native player | DRM | Protocol |
|----------|---------------|-----|----------|
| Apple TV (tvOS) | AVPlayer | FairPlay | HLS |
| Android TV / Google TV | ExoPlayer | Widevine | DASH (or HLS) |
| Fire TV | ExoPlayer | Widevine (PlayReady on some SKUs) | DASH |
| webOS / Tizen | platform web player | Widevine / PlayReady | DASH (HLS varies) |

A cross-platform app typically ships an HLS+FairPlay path for Apple and a DASH-based path for other platforms, with Widevine or PlayReady chosen per device support; plan the encode/packaging for both.

## TV Hardware Constraints That Bite
- **Security level is enforced in hardware.** Widevine L1 / FairPlay require hardware-backed decryption for HD/4K; low-end SKUs may only offer L3 (SD-capped). Detect and degrade gracefully rather than failing playback.
- **Decoders are limited and shared.** A TV may decode one 4K stream at a time; trailers + main content can contend. Tear down players you aren't using.
- **Memory is shared with the video buffer** — see [perf-memory.md](./perf-memory.md). Oversized buffers on a 1–2 GB device cause OOM, not just jank.

DRM in any case requires a valid license server, app entitlements/permissions, and sometimes native player configuration (security level, hardware decryption).

## Related Skills
- [video-players.md](./video-players.md) — Player implementations and custom controls
- [video-debugging.md](./video-debugging.md) — Debugging tools for video streams
