---
title: JavaScript Tests for TV Apps
impact: MEDIUM
tags: testing, rntl, tvremote, focus, hardware-key-events, tv
---

# JavaScript Tests for TV Apps

TV tests use the same React Native Testing Library but need custom helpers for remote-controlled navigation — you can't emulate D-pad with click events.

## Quick Reference
- Create a local `tvRemote` helper for focus/blur/press events owned by JS
- Focus movement must be explicit; RNTL does not run the native TV focus engine
- Test native focus-engine behavior in E2E, not in JS-only tests
- Add platform-specific event-emitter coverage only when app code subscribes to those events

## Example Test

`tvRemote` is a project-specific helper, not a library export.

```jsx
import { render, screen, fireEvent } from '@testing-library/react-native';
import { tvRemote } from './testUtils/tvRemote';

it('navigates and selects the play button', () => {
  const onPressMock = jest.fn();
  render(<MyComponent onPress={onPressMock} />);

  const infoButton = screen.getByRole('button', { name: 'Info' });
  const playButton = screen.getByRole('button', { name: 'Play' });

  fireEvent(infoButton, 'focus');
  tvRemote.right({ elementToFocus: playButton, elementToBlur: infoButton });
  tvRemote.select({ elementToSelect: playButton });

  expect(onPressMock).toHaveBeenCalled();
});
```

## Building the tvRemote Helper

Start with the smallest helper that matches what React Native Testing Library can actually test: JS focus/blur handlers and press handlers. Keep native focus-engine assertions in E2E.

```jsx
import { fireEvent } from '@testing-library/react-native';

export const tvRemote = {
  move({ elementToBlur, elementToFocus } = {}) {
    if (elementToBlur) {
      fireEvent(elementToBlur, 'blur');
    }
    if (elementToFocus) {
      fireEvent(elementToFocus, 'focus');
    }
  },
  right(args) {
    this.move(args);
  },
  left(args) {
    this.move(args);
  },
  up(args) {
    this.move(args);
  },
  down(args) {
    this.move(args);
  },
  select({ elementToSelect } = {}) {
    if (!elementToSelect) return;
    fireEvent(elementToSelect, 'pressIn');
    fireEvent.press(elementToSelect);
    fireEvent(elementToSelect, 'pressOut');
  },
};
```

## Testing Native Remote Event Subscribers

If app code subscribes to `TVEventHandler`, `useTVEventHandler`, `DeviceEventEmitter`, or a Vega/Kepler equivalent, add a second helper that emits the event payload shape used by that app. Keep this helper local because payload names differ by platform and RN fork.

```jsx
import { act } from '@testing-library/react-native';
import { DeviceEventEmitter, Platform } from 'react-native';

export function emitRemoteEvent(eventType) {
  const payload = Platform.isTVOS
    ? { eventType }
    : { eventType, eventKeyAction: 1 };

  act(() => {
    DeviceEventEmitter.emit('onHWKeyEvent', payload);
  });
}
```

> `Platform.isTVOS` is specific to `react-native-tvos`. For Vega/Kepler, use that stack's documented platform flags and event payloads instead of copying this branch.

## Why Focus Must Be Explicit

The native focus engine handles actual focus movement. In JavaScript tests, there is no real focus search, so specify `elementToFocus` and `elementToBlur` manually. Use E2E to validate that a physical remote press moves focus to the expected element.

## Performance Testing with Reassure

Reuse integration test scenarios to measure render characteristics:
```jsx
// Same RNTL tests, but Reassure measures render times
// Compare results against a stable baseline
```

## Related Skills
- [test-strategy.md](./test-strategy.md) — Overall testing approach
- [test-e2e.md](./test-e2e.md) — End-to-end testing with Appium
- [focus-management.md](./focus-management.md) — Focus APIs being tested
