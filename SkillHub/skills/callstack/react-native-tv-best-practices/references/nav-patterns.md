---
title: Navigation Patterns
impact: CRITICAL
tags: navigation, drawer, tabs, modals, back-navigation, focus-restoration, tv
---

# Navigation Patterns

TV navigation uses two layers: global navigation (between sections) and local navigation (within sections). The goal is predictable navigation — users should reach content with minimal button presses and no confusion.

## Quick Reference
- Use drawer for global navigation, tabs for local navigation
- Always restore focus when returning from modals/overlays
- Keep the back button behavior consistent: each press = one layer back
- Trap focus inside modals and overlays until dismissed

## Drawer Navigation (Global)

The main menu, typically on the left edge:
- Opens when user presses left from leftmost area (or menu/back button)
- Rest of screen dims slightly to signal context shift
- Focus is trapped inside until user exits or selects

```jsx
<Drawer isOpen={open}>
  <MenuItem label="Home" onPress={() => navigate('home')} />
  <MenuItem label="Movies" onPress={() => navigate('movies')} />
  <MenuItem label="Settings" onPress={() => navigate('settings')} />
</Drawer>
```

**Best practices:**
- Limit to 5-7 items
- Use clear labels (icons + text)
- Restore focus to previously active element when drawer closes
- Transitions under 200ms — should feel like infrastructure, not a feature

## Tab Navigation (Local)

Organizes content within a single section:
- Typically beneath hero banner or above first row
- 3-5 tabs maximum
- Left/right to switch tabs, down to enter content rows

```jsx
<Tabs>
  <Tab label="Popular" onFocus={() => setCategory('popular')} />
  <Tab label="New" onFocus={() => setCategory('new')} />
  <Tab label="Favorites" onFocus={() => setCategory('favorites')} />
</Tabs>
```

Horizontal tabs as primary navigation work for simple apps. Complex apps benefit from drawer-based approach.

## Modal Navigation

Modals are temporary, focused interruptions:

```jsx
<Modal visible={showDetails}>
  <Text>Are you sure you want to remove this item?</Text>
  <Button label="Cancel" onPress={() => setShowDetails(false)} />
  <Button label="Confirm" onPress={handleConfirm} />
</Modal>
```

**Guidelines:**
- Trap focus inside — dim/blur background
- Transitions ~150ms
- Never stack multiple modals
- Consistent placement (center fade/scale typically works)
- When modal closes, restore focus to element that triggered it

## Back Navigation & Focus Restoration

When users press back, they expect:
1. Return to the same screen
2. Focus on the element they were using before

### Remembering Last Focused Element

`TVFocusGuideView` manages this internally — each guide maintains the last element that held focus. When user returns, the same element is refocused.

```jsx
function ConfirmModal({ visible, onClose, returnRef }) {
  return visible ? (
    <TVFocusGuideView trapFocusUp trapFocusDown>
      <Pressable hasTVPreferredFocus onPress={onClose}>
        Confirm
      </Pressable>
      <Pressable onPress={() => {
        onClose();
        returnRef?.current?.focus();
      }}>
        Cancel
      </Pressable>
    </TVFocusGuideView>
  ) : null;
}
```

### Keeping Back Flow Consistent

Each back press should move back one layer and restore previous focus state. This sequence must be the same everywhere in your app.

## Navigation Predictability

- Always provide a visible focus state
- Never move focus off-screen without scrolling into view
- Keep focusable elements reasonable — users shouldn't press buttons excessively
- Use consistent directional logic: if left opens drawer on one screen, it should do the same on all screens

## Implementation with React Navigation

### Drawer
```jsx
const Drawer = createDrawerNavigator();
<Drawer.Navigator screenOptions={{
  drawerType: 'permanent',
  drawerStyle: { width: 240 },
}}>
  <Drawer.Screen name="Home" component={HomeScreen} />
  <Drawer.Screen name="Movies" component={MoviesScreen} />
</Drawer.Navigator>
```

### Tabs
```jsx
const Tab = createBottomTabNavigator();
<Tab.Navigator screenOptions={{
  tabBarStyle: { height: 80 },
  tabBarLabelStyle: { fontSize: 18 },
}}>
  <Tab.Screen name="Home" component={HomeScreen} />
  <Tab.Screen name="Movies" component={MoviesScreen} />
</Tab.Navigator>
```

## Related Skills
- [focus-management.md](./focus-management.md) — TVFocusGuideView, focus traps
- [nav-directional.md](./nav-directional.md) — How focus engines work
- [nav-keyboard.md](./nav-keyboard.md) — Keyboard handling on TV
