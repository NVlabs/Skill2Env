# Google Analytics Data API Java Client Library Installation

This guide provides specific instructions for installing and setting up the
Google Analytics Data API (v1beta) client library for Java.

## Prerequisites

*   **Java Development Kit (JDK):** Java 8 or higher (Java 11+ recommended).
*   **Build Tool:** Maven or Gradle.
*   **Authentication:** Application Default Credentials (ADC) configured via
    `gcloud auth application-default login`.

## Installation

Add the official Google Analytics Data client library dependency to your build
file.

> [!NOTE] For complete reference documentation, see the
> [Google Cloud Java Analytics Data Repository](https://github.com/googleapis/google-cloud-java/blob/main/java-analytics-data/README.md).

> [!TIP]
> Always replace `LATEST_LIBRARY_VERSION` with the latest stable version of the
> dependency available on Maven Central.

### Option A: Maven (`pom.xml`)

Add the following dependency inside your `<dependencies>` tag in `pom.xml`:

```xml
<dependency>
  <groupId>com.google.cloud</groupId>
  <artifactId>google-cloud-analytics-data</artifactId>
  <version>LATEST_LIBRARY_VERSION</version>
</dependency>
```

*Why: Using Maven ensures all required gRPC and protobuf message classes are
added to your runtime classpath.*

### Option B: Gradle (`build.gradle`)

Add the following to your `dependencies` block:

```groovy
implementation 'com.google.cloud:google-cloud-analytics-data:LATEST_LIBRARY_VERSION'
```

## Quickstart / Usage

```java
import com.google.analytics.data.v1beta.BetaAnalyticsDataClient;
import com.google.analytics.data.v1beta.RunReportRequest;
import com.google.analytics.data.v1beta.RunReportResponse;
import com.google.analytics.data.v1beta.DateRange;
import com.google.analytics.data.v1beta.Dimension;
import com.google.analytics.data.v1beta.Metric;

public class DataApiDemo {
  public static void main(String[] args) throws Exception {
    // Initialize BetaAnalyticsDataClient within try-with-resources.
    try (BetaAnalyticsDataClient client = BetaAnalyticsDataClient.create()) {
      RunReportRequest request = RunReportRequest.newBuilder()
          .setProperty("properties/1234567")
          .addDimensions(Dimension.newBuilder().setName("city"))
          .addMetrics(Metric.newBuilder().setName("activeUsers"))
          .addDateRanges(DateRange.newBuilder().setStartDate("2026-05-01").setEndDate("today"))
          .build();

      RunReportResponse response = client.runReport(request);
      response.getRowsList().forEach(row -> {
        System.out.printf("%s, %s%n", row.getDimensionValues(0).getValue(), row.getMetricValues(0).getValue());
      });
    }
  }
}
```
