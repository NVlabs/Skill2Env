# Google Analytics Data API Go Client Library Installation

This guide provides specific instructions for installing and setting up the
Google Analytics Data API (v1beta) client library for Go.

## Prerequisites

*   **Go:** Version 1.19 or higher.
*   **Modules:** Go modules enabled.
*   **Authentication:** Application Default Credentials (ADC) configured via
    `gcloud auth application-default login`.

## Installation

Install the official Go client library using `go get`.

Run the following command in your module directory:

```bash
go get cloud.google.com/go/analytics/data/apiv1beta
```

If `go` is not available, prompt the user to install `Go` before installing the
package.

*Why: This command adds the Google Analytics Data API package and its gRPC
transport layers to your Go project.*

## Quickstart / Usage

```go
package main

import (
    "context"
    "fmt"
    "log"

    data "cloud.google.com/go/analytics/data/apiv1beta"
    "cloud.google.com/go/analytics/data/apiv1beta/datapb"
)

func main() {
    ctx := context.Background()

    // Initialize client. Uses ADC from environment.
    client, err := data.NewBetaAnalyticsDataClient(ctx)
    if err != nil {
        log.Fatalf("Failed to create client: %v", err)
    }
    defer client.Close()

    req := &datapb.RunReportRequest{
        Property:   "properties/1234567",
        Dimensions: []*datapb.Dimension{{Name: "city"}},
        Metrics:    []*datapb.Metric{{Name: "activeUsers"}},
        DateRanges: []*datapb.DateRange{{StartDate: "2026-05-01", EndDate: "today"}},
    }

    resp, err := client.RunReport(ctx, req)
    if err != nil {
        log.Fatalf("RunReport failed: %v", err)
    }

    for _, row := range resp.Rows {
        fmt.Printf("%s, %s\n", row.DimensionValues[0].Value, row.MetricValues[0].Value)
    }
}
```
