---
title: Video Players for React Native TV
impact: HIGH
tags: video, players, react-native-video, exoplayer, avplayer, shaka, drm
---

# Video Players for React Native TV

## Quick Reference
- Choose the player after the target platform and DRM/protocol path are known
- Native TV targets usually end at AVPlayer/ExoPlayer through a wrapper or native module
- Web-based TV targets can use Shaka, hls.js, or dash.js in the browser context
- For seek thumbnails, prefer BIF or another indexed single-file format over many image requests

## Available Players

| Player | Platform | Best For |
|--------|----------|----------|
| AVPlayer | iOS, tvOS | Native Apple playback, FairPlay DRM |
| ExoPlayer | Android TV, Fire TV | Wide format support, Widevine DRM |
| react-native-video | Cross-platform | Wraps AVPlayer + ExoPlayer; easiest setup |
| react-native-theoplayer | Cross-platform | THEOplayer SDK wrapper |
| Shaka Player | JS (all platforms) | DASH + HLS, advanced ABR, multiple DRMs |
| hls.js | Web-based TVs | HLS playback in browsers |
| dash.js | Web-based TVs | MPEG-DASH reference player |

## Player-Control Checks

- Do not mount multiple hidden player instances for preview + main playback unless the target device can decode them concurrently.
- Keep player controls remote-focusable even when video is buffering or DRM is negotiating.
- Separate seekbar focus state from playback progress state so rapid scrubbing does not fight `onProgress`.
- Tear down preview playback before starting protected main content on memory-constrained devices.

## Thumbnail Generation — BIF Format

The Broadcast Image Format bundles all thumbnails in one indexed binary file:
- Single network request (vs. individual image downloads)
- Indexed structure for instant lookup by timestamp
- `thumbIndex = Math.floor(videoTime / interval)`

For large videos (2+ hours), use a native module for BIF parsing. Cache BIF files locally.

## Focus During Scrubbing

- **Debounce thumbnail updates** (100-200ms) during rapid scrubbing
- **Preload adjacent thumbnails** during idle moments
- **Lazy load** distant timeline parts to optimize memory

## Shaka Player for Enterprise

For complex streaming (live sports, multi-DRM, custom ABR), choose the architecture explicitly:

- **Web-based TV targets:** Run Shaka in the TV browser/webview context and render controls in the web UI.
- **Native React Native targets:** Prefer AVPlayer/ExoPlayer through `react-native-video`, THEOplayer, or a custom native module. If Shaka is required for packaging/ABR logic, treat it as an orchestration layer and bridge the native playback surface deliberately; do not assume browser Shaka drops into a native RN view unchanged.

## When to Use What

| Scenario | Recommendation |
|----------|---------------|
| Basic HLS/MP4 playback | react-native-video |
| Simple DRM (single platform) | react-native-video with DRM config |
| Enterprise multi-DRM, live sports | Shaka Player or native players |
| Web-based TVs (Tizen, webOS) | Shaka Player, hls.js, or dash.js |

## Related Skills
- [video-streaming.md](./video-streaming.md) — Streaming architecture and protocols
- [video-debugging.md](./video-debugging.md) — Debugging tools
- [focus-management.md](./focus-management.md) — Focus handling during playback
