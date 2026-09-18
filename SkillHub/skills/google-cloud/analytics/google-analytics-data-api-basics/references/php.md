# Google Analytics Data API PHP Client Library Installation

This guide provides specific instructions for installing and setting up the
Google Analytics Data API (v1beta) client library for PHP.

## Prerequisites

*   **PHP:** Version 8.0 or higher.
*   **Package Manager:** Composer.
*   **Authentication:** Application Default Credentials (ADC) configured via
    `gcloud auth application-default login`.

## Installation

Install the library using Composer.

> [!NOTE] For complete instructions, see the
> [PHP Analytics Data Repository](https://github.com/googleapis/php-analytics-data#installation).

Run the following command in your project root:

```bash
composer require google/analytics-data
```

If `composer` is not available, prompt the user to install `Composer` before
installing the package.

*Why: Composer downloads `google/analytics-data`, its dependencies, and sets up
autoloading.*

## Quickstart / Usage

```php
require_once __DIR__ . '/vendor/autoload.php';

use Google\Analytics\Data\V1beta\Client\BetaAnalyticsDataClient;
use Google\Analytics\Data\V1beta\DateRange;
use Google\Analytics\Data\V1beta\Dimension;
use Google\Analytics\Data\V1beta\Metric;
use Google\Analytics\Data\V1beta\RunReportRequest;

$client = new BetaAnalyticsDataClient();

$request = (new RunReportRequest())
    ->setProperty('properties/1234567')
    ->setDimensions([new Dimension(['name' => 'city'])])
    ->setMetrics([new Metric(['name' => 'activeUsers'])])
    ->setDateRanges([new DateRange(['start_date' => '2026-05-01', 'end_date' => 'today'])]);

$response = $client->runReport($request);

foreach ($response->getRows() as $row) {
    printf("%s, %s\n", $row->getDimensionValues()[0]->getValue(), $row->getMetricValues()[0]->getValue());
}
```
