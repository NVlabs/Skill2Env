# Google Analytics Data API Node.js Client Library Installation

This guide provides specific instructions for installing and setting up the
Google Analytics Data API (v1beta) client library for Node.js.

## Prerequisites

*   **Node.js:** v14.x or higher (v16+ recommended).
*   **Package Manager:** `npm` or `yarn`.
*   **Authentication:** Application Default Credentials (ADC) configured via
    `gcloud auth application-default login`.

## Installation

Install the official npm package.

> [!NOTE] For complete reference documentation, see the
> [Node.js Analytics Data Reference](https://googleapis.dev/nodejs/analytics-data/latest/index.html#installing-the-client-library).

Run the following command in your project root:

```bash
npm install @google-analytics/data
```

*Why: Installing `@google-analytics/data` provides TypeScript definitions and
JavaScript wrappers for the BetaAnalyticsDataClient.*

## Quickstart / Usage

```javascript
const {BetaAnalyticsDataClient} = require('@google-analytics/data');

async function runReport() {
  // Initialize client. Automatically authenticates using ADC.
  const analyticsDataClient = new BetaAnalyticsDataClient();

  const [response] = await analyticsDataClient.runReport({
    property: 'properties/1234567',
    dateRanges: [{startDate: '2026-05-01', endDate: 'today'}],
    dimensions: [{name: 'city'}],
    metrics: [{name: 'activeUsers'}],
  });

  console.log('Report Rows:');
  response.rows.forEach(row => {
    console.log(`${row.dimensionValues[0].value}, ${row.metricValues[0].value}`);
  });
}

runReport().catch(console.error);
```
