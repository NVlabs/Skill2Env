---
title: Testing Strategy for React Native TV Apps
impact: MEDIUM
tags: testing, integration-tests, rntl, focus, remote-input, tv
---

# Testing Strategy for React Native TV Apps

TV testing should prove the remote-controlled paths that break differently from mobile: focus order, Back/Menu behavior, player controls, low-memory carousels, and platform packaging.

## Quick Reference
- Use integration tests for JS-owned focus state, player-control state, and remote event handlers
- Use E2E tests for native focus engine behavior, app launch, routing, playback startup, and Back/Menu behavior
- For agent-run accessibility smoke, load the `agent-device` skill and read `agent-device help workflow`, then inspect labels, roles, states, and focused elements from the accessibility tree
- Use real hardware for overscan, remote latency, memory pressure, video decode, DRM, and display/color checks
- Keep emulators/simulators for fast route, focus, and smoke coverage; do not treat them as final device validation
- Reuse the same user flows for performance baselines where possible

## JS Integration Tests

Prefer a saved or generated app state that includes rows, entitlement state, player state, and modal state:
```jsx
const snapshot = require('my-state.json');
const { Wrapper } = loadStateFromSnapshot(snapshot);
render(<Wrapper><VideoPlayer /></Wrapper>);
```

- Mock native player/focus modules when JS tests cannot load them
- Mock timers for auto-hide controls, debounce, and "are you still watching" flows
- Avoid mocking app state in tests that are meant to prove focus restoration or navigation paths

See [test-javascript.md](./test-javascript.md) for the local `tvRemote` helper pattern.

## CI Scope

- PR checks: static checks, unit tests, integration tests, and changed-platform build checks
- Nightly/release checks: E2E on representative TV devices, playback startup, `agent-device` accessibility-tree smoke, memory-sensitive carousel flows
- Device matrix: at least one Apple TV target, one Android TV/Fire TV target, and any required Vega/Tizen/webOS target

## Related Skills
- [test-javascript.md](./test-javascript.md) — JS test setup and tvRemote helpers
- [test-e2e.md](./test-e2e.md) — E2E testing with Appium and device farms
- [perf-overview.md](./perf-overview.md) — Performance KPIs to test
