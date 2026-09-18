# Configuration Reference

Complete reference for `IConfiguration` / `IConfig` passed to `new ApplicationInsights({ config })`.

## Identity & Endpoints

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `connectionString` | string | — | **Required.** Includes ingestion + live-metrics endpoints. Public — never reuse with backend secrets. |
| `instrumentationKey` | string | — | Legacy. Prefer `connectionString`. |
| `endpointUrl` | string | regional | Override ingestion endpoint (sovereign clouds, proxies). |
| `userOverrideEndpointUrl` | string | — | Force a specific ingestion URL bypassing connection-string parsing. |
| `appId` | string | — | App identifier for cross-component correlation. |

## Auto-Collection

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `disableAjaxTracking` | bool | `false` | Stops XHR auto-instrumentation. |
| `disableFetchTracking` | bool | `false` | Stops `fetch` auto-instrumentation. |
| `disableExceptionTracking` | bool | `false` | Stops `window.onerror` / unhandled-rejection capture. |
| `autoTrackPageVisitTime` | bool | `false` | Emit time-on-page when leaving. |
| `enableAutoRouteTracking` | bool | `false` | Hook `history.pushState/replaceState`. SPA only. |
| `enableUnhandledPromiseRejectionTracking` | bool | `false` | Emits `unhandledRejection` as exceptions. |
| `excludeRequestFromAutoTrackingPatterns` | RegExp[] | — | Skip URLs (e.g. health checks, telemetry endpoints). |

## Distributed Tracing

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `distributedTracingMode` | enum | `AI` (1) | `AI_AND_W3C` (2) is required for OTel-instrumented backends. |
| `enableCorsCorrelation` | bool | `false` | Add correlation headers on cross-origin requests (requires server CORS allow-list). |
| `correlationHeaderExcludePatterns` | RegExp[] | — | Skip correlation for matching URLs (e.g. third-party CDNs that reject unknown headers). |
| `correlationHeaderDomains` | string[] | — | Limit correlation to specific domains. |
| `correlationHeaderExcludedDomains` | string[] | — | Hard-exclude domains. |
| `enableRequestHeaderTracking` | bool | `false` | Capture outbound request headers (PII risk). |
| `enableResponseHeaderTracking` | bool | `false` | Capture inbound response headers. |
| `enableAjaxErrorStatusText` | bool | `false` | Include `statusText` on failed AJAX. |
| `enableAjaxPerfTracking` | bool | `false` | Use `PerformanceResourceTiming` for richer AJAX timing. |
| `maxAjaxCallsPerView` | number | 500 | Limit AJAX deps per page view (-1 = unlimited). |

## Sampling & Throttling

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `samplingPercentage` | number | 100 | Client-side ingestion sampling. Whole numbers only. |
| `maxBatchSizeInBytes` | number | 102400 | Batch send threshold. |
| `maxBatchInterval` | number | 15000 | ms between sends. |

## Cookies & Storage

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `isCookieUseDisabled` | bool | `false` | Hard-disable cookies (no `ai_user`/`ai_session`). |
| `cookieCfg` | object | — | `{ enabled, domain, path, expiry, secure, ... }`. |
| `isStorageUseDisabled` | bool | `false` | Disable `localStorage` for buffer/retry. |
| `disableUserInitMessage` | bool | `false` | Suppress noisy diagnostic init message. |

## Send Behaviour

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `onunloadDisableBeacon` | bool | `false` | If `true`, do not use `sendBeacon` on unload. |
| `disableXhr` | bool | `false` | Force-disable XHR transport (sendBeacon/fetch only). |
| `disableFlushOnBeforeUnload` | bool | `false` | Skip auto-flush on `beforeunload`. |
| `disableFlushOnUnload` | bool | `false` | Skip auto-flush on `unload`/`pagehide`. |
| `enableSessionStorageBuffer` | bool | `true` | Persist queued telemetry across reloads. |

## Retry & Failover

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `maxRetries` | number | 10 | Per-batch retry budget. |
| `disableInstrumentationKeyValidation` | bool | `false` | Skip GUID validation (sovereign clouds). |
| `loggingLevelConsole` | 0–2 | 0 | 0=off, 1=critical, 2=warn+critical. |
| `loggingLevelTelemetry` | 0–2 | 1 | Same scale; sends SDK self-diagnostics as Trace. |

## Plugins

| Key | Type | Default | Notes |
| --- | --- | --- | --- |
| `extensions` | `ITelemetryPlugin[]` | `[]` | E.g. `ReactPlugin`, `ClickAnalyticsPlugin`. |
| `extensionConfig` | `Record<string, any>` | `{}` | Keyed by `plugin.identifier`. |
| `disableTelemetry` | bool | `false` | Master kill-switch (set after consent flow). |

## Recommended Production Config

```typescript
import { ApplicationInsights, DistributedTracingModes } from "@microsoft/applicationinsights-web";

new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,

    // Auto-collection
    enableAutoRouteTracking: true,
    autoTrackPageVisitTime: true,
    enableUnhandledPromiseRejectionTracking: true,
    excludeRequestFromAutoTrackingPatterns: [
      /\/healthz$/i,
      /dc\.services\.visualstudio\.com/i,
      /js\.monitor\.azure\.com/i
    ],

    // Distributed tracing
    distributedTracingMode: DistributedTracingModes.AI_AND_W3C,
    enableCorsCorrelation: true,
    correlationHeaderExcludedDomains: ["*.googleapis.com", "*.facebook.com"],

    // Privacy
    isCookieUseDisabled: false,
    cookieCfg: { domain: ".example.com" },

    // Throughput
    samplingPercentage: 100,        // tune down if egress is high
    maxBatchInterval: 5000,

    // Diagnostics (set 0 in prod after stable)
    loggingLevelConsole: 0,
    loggingLevelTelemetry: 1
  }
});
```

## Tuning notes

- **Mobile networks:** lower `maxBatchInterval` to 3–5 s and `maxBatchSizeInBytes` to 32 KB so unload flushes are smaller.
- **High-traffic SPAs:** turn on `samplingPercentage` (e.g. 25) before paying for ingestion overage. Server-side ingestion sampling on the App Insights resource is preferred when available.
- **Strict CSP:** Loader Script needs `script-src https://js.monitor.azure.com 'self'`. The npm import path requires no extra CSP.
- **Tracking opt-out:** set `disableTelemetry = true` and call `getCookieMgr().setEnabled(false)` after the user revokes consent. Do not destroy the SDK instance — re-enable by toggling `disableTelemetry = false`.

## See also

- Microsoft Learn — JavaScript SDK configuration: <https://learn.microsoft.com/azure/azure-monitor/app/javascript-sdk-configuration>
- IConfiguration source: <https://github.com/microsoft/ApplicationInsights-JS/blob/main/shared/AppInsightsCommon/src/Interfaces/IConfig.ts>
