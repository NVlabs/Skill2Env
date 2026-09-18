---
title: End-to-End Testing for TV Apps
impact: MEDIUM
tags: e2e, appium, webdriverio, device-farms, tvos, android-tv
---

# End-to-End Testing for TV Apps

For full behavioral testing, Appium is the best option for React Native TV. It supports Android TV and Apple TV via UIAutomator and XCUITest. Web-based platforms test through browser automation.

## Quick Reference
- Use Appium + WebdriverIO for native TV platforms
- Use `driver.pressKeyCode` to simulate D-pad navigation
- Use accessibility labels as selectors (`~home-button`)
- Device farms (AWS, BrowserStack, Sauce Labs) for real hardware testing

## Appium Setup — Android TV

```typescript
// wdio.conf.ts
capabilities: [{
  platformName: 'Android',
  automationName: 'UiAutomator2',
  deviceName: 'Android TV Emulator',
  appPackage: 'com.mycompany.tvapp',
  appActivity: 'com.mycompany.tvapp.MainActivity',
  newCommandTimeout: 300,
}]
```

## Appium Setup — Apple TV

```typescript
capabilities: [{
  platformName: 'iOS',
  platformVersion: '17.0',
  deviceName: 'Apple TV',
  automationName: 'XCUITest',
  udid: 'auto',
  app: '/path/to/your/TVApp.app',
  newCommandTimeout: 300,
}]
```

## Example Test

```typescript
describe('TV App Navigation', () => {
  it('navigates to Home and selects an item', async () => {
    const homeButton = await $('~home-button');
    await homeButton.click();
    await driver.pressKeyCode(20); // DPAD_DOWN
    await driver.pressKeyCode(23); // DPAD_CENTER
    const detailsSection = await $('~details-section');
    await expect(detailsSection).toBeDisplayed();
  });
});
```

Make components accessible for selectors:
```jsx
<Pressable accessibilityLabel="home-button" onPress={goHome}>
  <Text>Home</Text>
</Pressable>
```

## Web-Based TV Platforms (Tizen, webOS)

Use WebdriverIO with browser capabilities:

```typescript
capabilities: [{
  browserName: 'chrome',
  'goog:chromeOptions': {
    args: ['--window-size=1920,1080'],
  },
}],
services: ['chromedriver'],
```

```typescript
describe('Web TV App (webOS)', () => {
  it('navigates with keyboard and selects item', async () => {
    await browser.url('http://localhost:1234/index.html');
    const homeButton = await $('aria/Home');
    await homeButton.click();
    await browser.keys(['ArrowDown', 'Enter']);
    const details = await $('[data-testid="details"]');
    await expect(details).toBeDisplayed();
  });
});
```

## Device Farms

Real-device testing is essential — emulators can't replicate remote input, performance, or display quirks.

| Service | Supported | Integration |
|---------|-----------|-------------|
| AWS Device Farm | Android, iOS, custom | Upload APK/IPA, use ARN refs |
| BrowserStack | Android, iOS, web | `bs://` app IDs, wdio service |
| Sauce Labs | Android, iOS, web | `storage:` app refs |

### Running on Device Farms

1. Upload binary (APK/IPA) via API
2. Get app ID (ARN, bs://, storage:)
3. Update capabilities with real device names
4. Run: `npx wdio run wdio.browserstack.conf.ts`

### AWS Device Farm
```bash
aws devicefarm schedule-run \
  --project-arn arn:... \
  --app-arn arn:... \
  --device-pool-arn arn:... \
  --name "MyApp TV Run" \
  --test type=APPIUM_NODE,testPackageArn=arn:...
```

## Limitations

- **Maestro and Detox** are not helpful for TV environments
- Web-based TVs run custom browser forks — never exact match in automated tests
- For platform-specific quirks, real devices are the only reliable test

## Related Skills
- [test-strategy.md](./test-strategy.md) — Overall testing approach
- [test-javascript.md](./test-javascript.md) — JS-level tests with tvRemote helpers
- [release-cicd.md](./release-cicd.md) — CI/CD pipeline integration
