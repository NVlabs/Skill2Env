# Google Analytics Data API .NET Client Library Installation

This guide provides specific instructions for installing and setting up the
Google Analytics Data API (v1beta) client library for .NET / C#.

## Prerequisites

*   **.NET SDK:** .NET Core 3.1, .NET Standard 2.0, or .NET 6.0+.
*   **Package Manager:** NuGet / `dotnet` CLI.
*   **Authentication:** Application Default Credentials (ADC) configured via
    `gcloud auth application-default login`.

## Installation

Install the official NuGet package.

> [!NOTE] For package management options, see the
> [NuGet Google.Analytics.Data.V1Beta Page](https://www.nuget.org/packages/Google.Analytics.Data.V1Beta#package-manager).

Run the following command using the .NET CLI:

```bash
dotnet add package Google.Analytics.Data.V1Beta
```

If `dotnet` is not available, prompt the user to install the `.NET CLI` before
installing the package.

Or via Package Manager Console in Visual Studio:

```powershell
Install-Package Google.Analytics.Data.V1Beta
```

*Why: The NuGet package provides asynchronous service client wrappers and
protobuf types for calling the Data API.*

## Quickstart / Usage

```csharp
using System;
using System.Threading.Tasks;
using Google.Analytics.Data.V1Beta;

class Program
{
    static async Task Main()
    {
        // Initialize client. Uses Application Default Credentials.
        BetaAnalyticsDataClient client = await BetaAnalyticsDataClient.CreateAsync();

        RunReportRequest request = new RunReportRequest
        {
            Property = "properties/1234567",
            Dimensions = { new Dimension { Name = "city" } },
            Metrics = { new Metric { Name = "activeUsers" } },
            DateRanges = { new DateRange { StartDate = "2026-05-01", EndDate = "today" } }
        };

        RunReportResponse response = await client.RunReportAsync(request);
        foreach (Row row in response.Rows)
        {
            Console.WriteLine($"{row.DimensionValues[0].Value}, {row.MetricValues[0].Value}");
        }
    }
}
```
