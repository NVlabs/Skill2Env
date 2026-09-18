---
title: Debugging Video Streams
impact: HIGH
tags: video, debugging, ffmpeg, ffprobe, charles, proxyman, profiling
---

# Debugging Video Streams

## Quick Reference
- Inspect the stream with `ffprobe` before changing React player code
- Verify manifest requests, DRM license exchange, ABR switches, and decoder support separately
- Use a proxy for network/license failures; use RN/React tooling for duplicate UI requests or player state desync
- Correlate client-side player errors with server-side CDN/license telemetry

## Playback Failure Layers

1. **Media package** — Use `ffprobe` for codec, bitrate, resolution, audio tracks, subtitles, and container details.
2. **Manifest validity** — Use platform validators where available, such as `mediastreamvalidator` for Apple HLS.
3. **Network path** — Inspect manifest, segment, and license requests with Charles or Proxyman.
4. **DRM/license** — Verify license URL, headers, entitlement token, and hardware security-level failures before changing UI code.
5. **React/player state** — Use Rozenite, React Native DevTools, or app logs for duplicate play requests, hidden controls, stale state, or JS-generated manifest URL changes.

## Network Traffic Analysis

Install the proxy CA certificate on the simulator, emulator, or device before expecting HTTPS manifests or license requests to decrypt.

## Related Skills
- [video-streaming.md](./video-streaming.md) — Streaming architecture
- [video-players.md](./video-players.md) — Player implementations
- [perf-overview.md](./perf-overview.md) — Overall performance strategy
