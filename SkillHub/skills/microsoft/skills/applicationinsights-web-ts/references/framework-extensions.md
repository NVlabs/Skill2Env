# Framework Extensions

## React (`@microsoft/applicationinsights-react-js`)

```bash
npm i @microsoft/applicationinsights-react-js history
```

```typescript
// app-insights.ts
import { ApplicationInsights } from "@microsoft/applicationinsights-web";
import { ReactPlugin } from "@microsoft/applicationinsights-react-js";
import { createBrowserHistory } from "history";

export const reactPlugin = new ReactPlugin();
export const browserHistory = createBrowserHistory();

export const appInsights = new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,
    extensions: [reactPlugin],
    extensionConfig: { [reactPlugin.identifier]: { history: browserHistory } },
    enableAutoRouteTracking: false  // ReactPlugin handles routes
  }
});
appInsights.loadAppInsights();
```

### Tracking a component (HOC)

```typescript
import { withAITracking } from "@microsoft/applicationinsights-react-js";
import { reactPlugin } from "./app-insights";

function Checkout() { /* ... */ }
export default withAITracking(reactPlugin, Checkout, "Checkout");
```

`withAITracking` measures the time the component is mounted and emits a metric `React Component Engaged Time (seconds)`.

### Hooks

```typescript
import {
  useTrackEvent, useTrackMetric, useAppInsightsContext
} from "@microsoft/applicationinsights-react-js";

function PayButton() {
  const ai = useAppInsightsContext();
  const trackPay = useTrackEvent(ai, "PayClicked", { /* extra props */ });

  return <button onClick={() => trackPay({ amount: 49.95 })}>Pay</button>;
}
```

### Error boundary

```typescript
import { AppInsightsErrorBoundary } from "@microsoft/applicationinsights-react-js";
import { reactPlugin } from "./app-insights";

<AppInsightsErrorBoundary appInsights={reactPlugin} onError={() => <FallbackUI />}>
  <App />
</AppInsightsErrorBoundary>
```

### React Router v6+ (no `history` prop)

`history v5+` doesn't ship with React Router v6. Bridge manually:

```typescript
import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { appInsights } from "./app-insights";

export function RouteTracker() {
  const loc = useLocation();
  useEffect(() => {
    appInsights.trackPageView({ name: loc.pathname, uri: loc.pathname + loc.search });
  }, [loc.pathname]);
  return null;
}
```

Set `enableAutoRouteTracking: false` so the SDK doesn't double-count.

## React Native (`@microsoft/applicationinsights-react-native`)

```bash
npm i @microsoft/applicationinsights-web @microsoft/applicationinsights-react-native
```

```typescript
import { ApplicationInsights } from "@microsoft/applicationinsights-web";
import { ReactNativePlugin } from "@microsoft/applicationinsights-react-native";

const rnPlugin = new ReactNativePlugin();
export const appInsights = new ApplicationInsights({
  config: {
    connectionString: process.env.EXPO_PUBLIC_APPINSIGHTS_CONNECTION_STRING,
    extensions: [rnPlugin],
    disableFetchTracking: false,
    disableExceptionTracking: false
  }
});
appInsights.loadAppInsights();
```

The plugin auto-collects device metadata (model, OS version, locale, network type) and unhandled JS exceptions. For native crashes, also use App Center / native Crashlytics — App Insights JS only sees the JS layer.

## Angular (`@microsoft/applicationinsights-angularplugin-js`)

```bash
npm i @microsoft/applicationinsights-web @microsoft/applicationinsights-angularplugin-js
```

```typescript
// app.module.ts
import { NgModule, ErrorHandler } from "@angular/core";
import { Router } from "@angular/router";
import { ApplicationInsights } from "@microsoft/applicationinsights-web";
import {
  AngularPlugin, ApplicationinsightsAngularpluginErrorService
} from "@microsoft/applicationinsights-angularplugin-js";

const angularPlugin = new AngularPlugin();
const appInsights = new ApplicationInsights({
  config: {
    connectionString: environment.appInsightsConnectionString,
    extensions: [angularPlugin],
    extensionConfig: { [angularPlugin.identifier]: { router: undefined /* set in APP_INITIALIZER */ } }
  }
});

@NgModule({
  providers: [
    {
      provide: ErrorHandler,
      useClass: ApplicationinsightsAngularpluginErrorService
    },
    {
      provide: "APP_INSIGHTS_INIT", multi: true,
      useFactory: (router: Router) => () => {
        angularPlugin["_extensionConfig"]!.router = router;
        appInsights.loadAppInsights();
      },
      deps: [Router]
    }
  ]
})
export class AppModule {}
```

Routes emit page views automatically via the `Router` reference; the custom `ErrorHandler` forwards uncaught Angular errors to `trackException`.

## Next.js (App Router, TypeScript)

App Insights JS is browser-only. Initialize in a client component mounted at the root layout.

```typescript
// app/_lib/app-insights.ts
"use client";
import { ApplicationInsights } from "@microsoft/applicationinsights-web";

let _ai: ApplicationInsights | undefined;
export function getAppInsights() {
  if (typeof window === "undefined") return undefined;
  if (_ai) return _ai;
  _ai = new ApplicationInsights({
    config: {
      connectionString: process.env.NEXT_PUBLIC_APPINSIGHTS_CONNECTION_STRING!,
      enableAutoRouteTracking: true
    }
  });
  _ai.loadAppInsights();
  _ai.trackPageView();
  return _ai;
}
```

```typescript
// app/_components/AppInsightsBootstrap.tsx
"use client";
import { useEffect } from "react";
import { getAppInsights } from "@/app/_lib/app-insights";
export function AppInsightsBootstrap() {
  useEffect(() => { getAppInsights(); }, []);
  return null;
}
```

```typescript
// app/layout.tsx
import { AppInsightsBootstrap } from "./_components/AppInsightsBootstrap";
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AppInsightsBootstrap />
        {children}
      </body>
    </html>
  );
}
```

Server-side telemetry in Next.js routes/server actions belongs in `@azure/monitor-opentelemetry` (Node), not here.

## Vite

```bash
npm i @microsoft/applicationinsights-web
```

```typescript
// src/lib/app-insights.ts
import { ApplicationInsights } from "@microsoft/applicationinsights-web";
export const appInsights = new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,
    enableAutoRouteTracking: true
  }
});
appInsights.loadAppInsights();
```

```typescript
// src/main.tsx
import "./lib/app-insights";  // side-effect import — initializes once
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
ReactDOM.createRoot(document.getElementById("root")!).render(<App />);
```

## Click Analytics quick recipe

```bash
npm i @microsoft/applicationinsights-clickanalytics-js
```

```typescript
import { ClickAnalyticsPlugin } from "@microsoft/applicationinsights-clickanalytics-js";

const click = new ClickAnalyticsPlugin();
const appInsights = new ApplicationInsights({
  config: {
    connectionString: import.meta.env.VITE_APPINSIGHTS_CONNECTION_STRING,
    extensions: [click],
    extensionConfig: {
      [click.identifier]: {
        autoCapture: true,
        dataTags: { useDefaultContentNameOrId: true, customDataPrefix: "data-ai-" }
      }
    }
  }
});
appInsights.loadAppInsights();
```

Tag interactive elements:

```html
<button data-ai-name="checkout-pay" data-ai-content-name="Pay $49.95">Pay</button>
```

## Debug plugin (dev only)

```bash
npm i -D @microsoft/applicationinsights-debugplugin-js
```

```typescript
import { DebugPlugin } from "@microsoft/applicationinsights-debugplugin-js";

const extensions = [];
if (import.meta.env.DEV) extensions.push(new DebugPlugin());
new ApplicationInsights({ config: { connectionString, extensions } });
```

Renders an in-page panel listing every telemetry envelope before send.
