---
name: mobile-pack
description: Native vs cross-platform decision (iOS/Android native, RN, Flutter, KMM), App Store / Play submission gotchas, MASVS V1-V8 detailed checklist, OTA update patterns (CodePush, EAS Update)
when_to_use: Building iOS, Android, React Native, Flutter, Kotlin Multiplatform, or Electron apps
applies_to:
  - mobile-app
---

# Mobile Pack

> Extends `mobile-app` archetype with framework decision tree, App Store / Play submission gotchas, OWASP MASVS detailed checklist, and OTA update patterns.
> Auto-loaded when `archetype: mobile-app` is detected in PROJECT.md.
> Also loaded explicitly via `packs: [mobile-pack]`.

## Decision tree — cross-platform vs native

| If you need... | Pick | Why |
|---------------|------|-----|
| Best UX, deep platform integration, you have iOS+Android specialists | **Native** (Swift + Kotlin) | No abstraction tax. Full access to platform APIs the day they ship. |
| Single codebase, mature ecosystem, web team transition | **React Native + Expo** | Largest community. Expo Router = file-based navigation like Next.js. |
| Single codebase, native performance feel, design-driven UI | **Flutter 3.x** | Skia/Impeller renders consistently. Best for design-heavy apps. |
| Want to share business logic but keep platform UI | **Kotlin Multiplatform Mobile (KMM)** | Share VM/repo layer in Kotlin, build UI native per platform |
| Cross-platform desktop + mobile from one codebase | **Tauri 2.0** | Rust core, system webview. Tiny binaries. Steeper learning curve. |
| Wrap an existing web app | **Capacitor** (better than Cordova) | OK for content apps. Don't pick for performance-sensitive apps. |
| Internal-only enterprise tool | **PWA** | If iOS isn't required, skip stores entirely. Add to Home Screen. |

**Anti-pattern**: cross-platform for a graphics-intensive game. Use Unity / Unreal / native Metal+Vulkan instead.

**Anti-pattern**: native (Swift + Kotlin × 2 codebases) for a small team building a CRUD app. The 2× engineering cost rarely justifies vs RN or Flutter for typical business apps.

## Build pipelines

| Tool | When |
|------|------|
| **Fastlane** | Native iOS/Android — universal CI/CD pipeline for App Store + Play deploy |
| **EAS Build** (Expo) | React Native via Expo — managed cloud builds, no local Xcode/Android Studio needed |
| **Bitrise** | Multi-framework, hosted CI specifically for mobile |
| **GitHub Actions + Fastlane** | DIY, full control, free for OSS |
| **Codemagic** | Flutter-first hosted CI |

For RN: EAS Build is the path of least resistance unless you have a strong reason to manage your own build infrastructure.

For native: Fastlane in GitHub Actions is the standard. Use Apple's [App Store Connect API](https://developer.apple.com/app-store-connect/api/) for upload, not the deprecated Application Loader.

## App Store rejection patterns (the ones that bite you twice)

Apple's review is not deterministic, but these patterns reliably get rejected:

### Guideline 4.3 — duplicate apps / spam
- App is too similar to your own previous submission, or to a competitor with copied UI
- Multiple apps with same template that only differ in branding (white-label fleet)

**Fix**: each app needs distinct value prop in description, distinct UI, distinct app icon family.

### Guideline 5.1.1 — privacy
- Asking for location/contacts/photos with vague reason
- Tracking users across apps without ATT prompt (iOS 14.5+)
- Missing privacy nutrition label
- Privacy policy URL returns 404 or doesn't cover what app actually collects

**Fix**: every permission has a usage-description string explaining the *specific* user benefit. Run all data collection paths through your privacy lawyer once before first submission.

### Guideline 2.1 — performance bug
- App crashes on launch on a clean device
- Reviewer can't get past login (broken backend, expired test account)
- Slow startup (> 3s on baseline device)

**Fix**: provide reviewer test account with note in App Review Information. Test on the oldest device in your support matrix before every submission.

### Guideline 3.1.1 — payments
- Unlocking digital content via external payment (Stripe, PayPal, web checkout)
- Discount codes that bypass IAP
- "Pay on web for cheaper price" hint

**Fix**: digital goods consumed in-app MUST go through IAP. Physical goods, services rendered outside the app, B2B SaaS subscriptions can use external payment. When in doubt, ask Apple before building.

### Guideline 4.7 — HTML5 / WebView wrappers
- App is essentially a webview pointing at your website
- No iOS-specific UX (just web navigation)

**Fix**: add native iOS features (push, biometric, camera, Apple Pay, sharing) and adapt UI patterns (swipe gestures, pull-to-refresh, native tab bar).

`security-officer` runs the App Store rejection pattern checklist before submit when `archetype: mobile-app`.

## Google Play submission

Less arbitrary than Apple, but has its own minefield:

- **API level requirement**: Play requires apps target latest Android API within 1 year of release. Currently API 34 (Android 14). Old apps get hidden from search.
- **Data Safety form**: Mandatory since 2022. Lying = removal.
- **Permissions justification**: Sensitive permissions (SMS, call log, all-files-access, accessibility) trigger manual review.
- **Pre-launch report**: Play tests your APK on real devices, sends report. Read it. Fix everything before publishing to production track.
- **Internal → Closed → Open → Production**: use the staged tracks. Production rollout: 1% → 10% → 50% → 100%.

## OWASP MASVS — V1-V8 detailed checklist

The MASVS is the mobile equivalent of OWASP Top 10. Eight verticals; `security-officer` runs each when `archetype: mobile-app` + `compliance: [owasp-masvs]`.

### V1 — Architecture, Design, and Threat Modeling
- [ ] Threat model exists, documented
- [ ] All security controls identified for each component
- [ ] Hardware/biometric usage documented

### V2 — Data Storage and Privacy
- [ ] No sensitive data in unencrypted storage (`UserDefaults`, `SharedPreferences` plain)
- [ ] Keychain (iOS) / Keystore (Android) for credentials
- [ ] No sensitive data in logs (especially in production builds)
- [ ] No sensitive data in app backups (exclude from iCloud / Google Backup)
- [ ] Clipboard cleared after use of sensitive data
- [ ] Screenshots disabled in app switcher when sensitive screen visible

### V3 — Cryptography
- [ ] No hardcoded keys in source / Info.plist / strings.xml
- [ ] Modern algorithms only: AES-256-GCM, ChaCha20-Poly1305, Ed25519
- [ ] No DES, 3DES, MD5, SHA-1 for security purposes
- [ ] Key derivation: PBKDF2 (100k+ iterations) or Argon2
- [ ] Secure random: `SecRandomCopyBytes` (iOS) / `SecureRandom` (Android), never `Math.random` / `arc4random`

### V4 — Authentication and Session Management
- [ ] Session tokens HTTP-only, secure, short-lived (~15 min) with refresh
- [ ] Biometric (Face ID / Touch ID / fingerprint) for re-auth, never primary auth
- [ ] Server-side session invalidation on logout
- [ ] Rate limit + lockout on failed auth attempts

### V5 — Network Communication
- [ ] TLS 1.2+ only, certificate validation NEVER disabled
- [ ] Certificate pinning for high-value flows (banking, healthcare)
- [ ] App Transport Security (iOS) configured strictly — no exceptions for HTTP
- [ ] Network Security Config (Android) declares cleartext traffic forbidden

### V6 — Platform Interaction
- [ ] All deep links validated (no command injection, no auth bypass via deep link)
- [ ] WebView: `JavaScriptEnabled` disabled unless needed, no `addJavascriptInterface` exposing dangerous methods
- [ ] WebView: HTTPS only, target origin verified

### V7 — Code Quality and Build Setting Requirements
- [ ] App built with current SDK
- [ ] Debug builds NOT shipped (no `NSLog` / `Log.d` in release, no debug symbols)
- [ ] Code obfuscation for native code (R8/ProGuard for Android, swift-shield for sensitive iOS)
- [ ] No third-party SDK with known CVE in shipped binary

### V8 — Resilience Requirements (defense-in-depth, optional for non-critical apps)
- [ ] Jailbreak / root detection (banking, healthcare apps)
- [ ] Anti-tampering: detect modified binary
- [ ] Anti-debugging: detect debugger attached
- [ ] Runtime application self-protection (RASP) for very high-value apps

## Push notifications

| Platform | Service |
|----------|---------|
| iOS native + RN + Flutter | **APNs** direct OR via Firebase Cloud Messaging (FCM) wrapper |
| Android native + RN + Flutter | **FCM** (replacing GCM since 2018) |
| Cross-platform abstracted | **Pusher Beams**, **OneSignal**, **Notifee** |

Best practice: server sends to FCM/APNs via your backend, never bundle the secret key in the app. Use [`apns2`](https://github.com/sideshow/apns2) (Go) or [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) (Node/Python).

Token rotation: store APNs/FCM tokens server-side per user. Rotate on app reinstall, on user logout, on token expiry (FCM tokens can change).

## In-app purchases

| Tool | When |
|------|------|
| **RevenueCat** | Default for any IAP product. Abstracts iOS+Android, gives you analytics + experimentation. |
| **Adapty** | Alternative to RevenueCat, more pricing experimentation features |
| Native StoreKit 2 (iOS) + BillingClient v6 (Android) | When you need full control or RevenueCat is too expensive |

RevenueCat free tier covers most early-stage apps. Pricing scales with revenue. Worth the cost for the receipt validation, fraud handling, and platform abstraction alone.

## Crash reporting

| Service | Best for |
|---------|---------|
| **Sentry** | Cross-platform, also covers backend. Best UI for grouping. |
| **Firebase Crashlytics** | Free, integrates with Google Analytics, mobile-only |
| **Bugsnag** | Detailed breadcrumbs, good for complex flows |

For new project: Sentry. Single tool covers mobile + web + backend with consistent UX.

## OTA updates

| Stack | Tool |
|-------|------|
| React Native | **EAS Update** (Expo) — bundled, no extra service |
| RN without Expo | **Microsoft App Center CodePush** — being deprecated, migrate |
| Flutter | **Shorebird** — code-push for Flutter |
| Native | Not really possible without going through stores (hot-reload of UI assets only) |

Rules:
- Only ship JS/Dart bundle changes via OTA. Native code changes require store submission.
- Apple's guideline 3.3.2 forbids hot-patching native logic. RevenueCat is *fine*. Bypassing IAP via OTA is *not*.
- Stage rollouts (1% → 100%) on OTA same as native.
- Have a rollback plan: previous bundle available in 30 seconds.

## Mobile auth

Modern stack (2026):

- **Passkeys** (FIDO2 / WebAuthn): primary recommended auth for new apps. Native APIs on iOS 16+ and Android 14+. RN has libraries.
- **Sign in with Apple**: required by Apple if you offer any third-party social login (Google, Facebook, etc.)
- **Sign in with Google**: Google's One Tap UI on Android is excellent
- **Biometric (Face ID / Touch ID / fingerprint)**: re-auth for sensitive actions, NEVER primary auth (someone can use your face while you sleep)
- **Magic links**: friendly fallback, but susceptible to phishing — pair with email verification
- **MFA**: TOTP (Google Authenticator) or push-based (Duo, Authy) for high-value apps

**Anti-pattern**: SMS as primary 2FA. SIM swap attacks make it the weakest factor. Only acceptable as recovery method.

## Performance budget (default for `mobile-app`)

```
Cold start (cold launch):       < 2.0s on baseline device
Warm start:                     < 800ms
Memory (steady state):          < 200 MB
Crash-free users (DAU):         ≥ 99.9%
ANR rate (Android):             ≤ 0.47% (Play Console threshold)
Frame rate (UI thread):         60 FPS sustained
APK / IPA size (initial):       < 50 MB compressed
```

For React Native specifically:
- JS bundle (initial):          < 1 MB minified
- TTI (time to interactive):    < 3s

For Flutter:
- App size (release):           < 30 MB compressed
- 60 FPS sustained, especially during scrolling

Test on the **oldest device** in your support matrix. iPhone 13 / Pixel 6 is NOT a baseline device — millions of users still have iPhone XS / Pixel 4a.

## Compliance defaults for `mobile-app`

| Trigger | Add to compliance |
|---------|-------------------|
| Always | `owasp-masvs` |
| Apple required | `att` (App Tracking Transparency) — needed for any cross-app tracking |
| Apple required | `play-api-34` (target API level 34+) |
| Stores credentials/PII | `gdpr` if EU users, `ccpa` if California users |
| Health data | `hipaa` (US), `gdpr-health` (EU) |
| Financial | `pci-dss` (if storing card data — usually you shouldn't, use Apple Pay/Google Pay) |
| Children (under 13) | `coppa` (US) |
| EU users + ads | `eu-cookie` (consent before ad tracking) |

## Anti-patterns specific to `mobile-app`

| Pattern | Why it fails | Fix |
|---------|-------------|-----|
| Hardcoded API keys in app bundle | Reverse engineering trivial — keys leak in 24h | Server-side proxy, ephemeral session tokens |
| Trusting client-side validation only | Anyone can MITM and skip checks | Validate server-side; client validation is UX only |
| Logging tokens / PII to crash reporter | Crash reports go to Sentry/Crashlytics in plaintext | Strip from logs, use scrubbing rules |
| Skipping cert pinning for "convenience" | MITM attacks succeed on public WiFi | Pin certs for high-value flows |
| Shipping debug builds to TestFlight | Users find dev tools, file false bug reports | Distinct configs for debug/staging/prod |
| In-app browser without sandbox | Phishing risk | Use SFSafariViewController (iOS) / Custom Tabs (Android), not raw WKWebView |
| Forcing app update on launch | Users abandon if update is large or slow | Soft-prompt, allow skip for non-critical updates |

## QA extras provided by this pack

When `archetype: mobile-app`, `qa-engineer` automatically runs:

- **Unit tests** (Jest/Vitest for RN, XCTest for iOS, JUnit/Espresso for Android, flutter_test for Flutter)
- **UI test on device matrix** (oldest supported + latest, both platforms)
- **Accessibility audit** (VoiceOver / TalkBack basic flow)
- **Crash rate baseline** (compare with last release on TestFlight / Internal track)
- **Bundle size diff** vs main branch (fail if > 10% increase)
- **MASVS V1-V5 checklist** (always)
- **MASVS V6-V8** if `qa-extras: [masvs-resilience]`

## Recommended `PROJECT.md` for new mobile-app

```yaml
primary: mobile
archetype: mobile-app
project_size: medium
stack: [react-native, expo, typescript]
team-size: 2
compliance: [owasp-masvs, att, play-api-34, gdpr]
performance-sla: cold-start < 2s, crash-free ≥ 99.9%
qa-extras: [device-matrix, accessibility]
packs: [mobile-pack]
```
