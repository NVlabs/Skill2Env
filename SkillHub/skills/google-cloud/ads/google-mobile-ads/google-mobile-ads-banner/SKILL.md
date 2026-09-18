---
name: google-mobile-ads-banner
description: Provides instructions to implement, integrate, or configure
  Google Mobile Ads (GMA) banner ads in Android and iOS mobile applications. Use
  when the task involves setting up banner ads in a mobile application.
metadata:
  version: 1.0.0
  category: GoogleAds
---
# Google Mobile Ads SDK - Banner Ads

Banner ads are rectangular image or text ads that occupy a spot within an app's
layout. They remain on screen during user interaction and can refresh
automatically.

### Ad Placement Guidelines

**CRITICAL:** You MUST evaluate and apply the following guidelines before
proceeding with any banner ad implementation.

*   **Determine Ad Placement**:
    *   [ ] **Identify the target file** where the ad should be placed. Ask if
        unsure.
    *   [ ] **Inspect view hierarchy** when the target file is identified.
        Examine the file and determine whether the parent container of the ad is
        a scrollable view (such as a list, scroll view, grid) or a static,
        non-scrollable view.
        *   **Scrollable Content**: Use **Inline Adaptive Banner**.
        *   **Non-Scrollable Content**: Use **Large Anchored Adaptive**.
            *   **Positioning**: If not specified, ask if the ad should be
                anchored to either the **top** or **bottom** of the screen.

## Workflow

1.  **Determine the user's platform**: Identify if the project is Android or
    iOS. If unclear, ask before proceeding.

2.  **Read the platform guide** for implementation details:
    -   Android: `references/android-banner.md`
    -   iOS: `references/ios-banner.md`

3.  **Follow these steps in order**:
    -   [ ] Define the ad view
    -   [ ] Set the ad size
    -   [ ] Register for ad load events
    -   [ ] Load the banner ad
    -   [ ] Verify the implementation

4.  After the banner ad is successfully implemented, remind the user to replace
  the test ad unit ID with their own.