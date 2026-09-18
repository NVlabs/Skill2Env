---
title: Keyboard Handling
impact: HIGH
tags: keyboard, text-input, voice-input, remote, tvevent, tv
---

# Keyboard Handling

TV remotes were never meant for typing. Each character takes several arrow presses and a click. Minimize typing and make keyboards work well when needed.

## Quick Reference
- **Rule #1: Minimize input** — Use pre-filled options, voice input, search history, auto-complete
- System keyboards feel natural to users; customize them before building custom
- Map RCU buttons (play/pause) to confirm/cancel actions
- Consider companion apps and QR code auth to eliminate typing entirely

## Input Minimization Strategies

1. **Pre-filled options** — Past searches, popular searches, or both
2. **Voice input** — React Native Voice library
3. **Real-time validation** — Minimize correction needs
4. **Input history** — Let users reuse previous searches
5. **Mobile companion apps** — For authentication, casting, second screen
6. **QR code authentication** — TV displays QR, phone scans it

## Built-In System Keyboards

Trigger the default keyboard with a standard `TextInput`. System keyboards differ by platform but feel natural to users.

### Android TV (GBoard for TV)
Grid-based keyboard, navigate with arrow keys, confirm with "OK" button.

### Apple tvOS
Row-based keyboard, scroll with remote swipe gestures. Supports dictation and iOS Remote app.

### Keyboard Types

Prefer the narrowest `keyboardType` (`numeric`/`number-pad` for PINs) — it swaps the full grid keyboard for a smaller one, cutting D-pad travel. Use `secureTextEntry` for passwords (not a keyboardType).

## Customizing the Built-In Keyboard

Use `useTVEventHandler` to map RCU buttons to actions:

```jsx
import { useTVEventHandler } from 'react-native';

const SearchScreen = () => {
  const inputRef = useRef(null);
  const inputValueRef = useRef('');

  const handleSearch = () => {
    console.log('Search submitted:', inputValueRef.current);
  };

  useTVEventHandler((evt) => {
    if (evt.eventType === 'play') {
      handleSearch();
    }
  });

  return (
    <TextInput
      ref={inputRef}
      placeholder="Search TV shows..."
      onChangeText={(text) => { inputValueRef.current = text; }}
      onSubmitEditing={handleSearch}
    />
  );
};
```

## Custom Keyboards

When the default keyboard is insufficient (YouTube-style search), build your own:

```jsx
const [showKeyboard, setShowKeyboard] = useState(false);
<KeyboardAvoidingView behavior="position" style={{ flex: 1 }}>
  <TextInput
    onFocus={() => setShowKeyboard(true)}
    showSoftInputOnFocus={false}
  />
  {showKeyboard && <CustomKeyboard onKeyPress={handleKeyPress} />}
</KeyboardAvoidingView>
```

**Key considerations:**
- Set `showSoftInputOnFocus={false}` to prevent system keyboard
- Handle two states: focused and selected for each key
- Make discoverable — users should know how to use auto-complete without guessing

## Voice Input

- **System keyboard approach:** Rely on system voice dictation (simplest, most reliable)
- **Custom keyboard:** Write native modules or use `react-native-voice`
- **Important:** Adding voice input requires microphone and speech recognition permissions

## Mobile Companion Apps

Enable communication between mobile and TV apps for:
- Authentication (easiest: QR code scan)
- Media casting
- Second screen experiences (stats, chats, polls)
- Text input from phone keyboard

Communication via local network (Wi-Fi) for media streaming scenarios.

## Related Skills
- [nav-patterns.md](./nav-patterns.md) — Overall navigation structure
- [a11y-implementation.md](./a11y-implementation.md) — Accessible input handling
