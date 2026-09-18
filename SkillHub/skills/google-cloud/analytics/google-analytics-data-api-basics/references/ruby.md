# Google Analytics Data API Ruby Client Library Installation

This guide provides specific instructions for installing and setting up the
Google Analytics Data API (v1beta) client library for Ruby.

## Prerequisites

*   **Ruby:** Version 3.0 or higher.
*   **Package Manager:** RubyGems / Bundler.
*   **Authentication:** Application Default Credentials (ADC) configured via
    `gcloud auth application-default login`.

## Installation

Install the official Google Cloud Ruby client gem.

> [!NOTE] For full installation instructions, refer to the
> [Ruby Analytics Data Repository](https://github.com/googleapis/google-cloud-ruby/tree/main/google-analytics-data-v1beta#installation).

Using RubyGems:

```bash
gem install google-analytics-data-v1beta
```

If `gem` is not available, prompt the user to install `Ruby` (and `RubyGems`)
before installing the gem.

Or add to your `Gemfile`:

```ruby
gem "google-analytics-data-v1beta"
```

And run `bundle install`.

## Quickstart / Usage

```ruby
require "google/analytics/data/v1beta"

# Initialize client. Automatically authenticates using ADC.
client = Google::Analytics::Data::V1beta::AnalyticsData::Client.new

request = Google::Analytics::Data::V1beta::RunReportRequest.new(
  property: "properties/1234567",
  dimensions: [Google::Analytics::Data::V1beta::Dimension.new(name: "city")],
  metrics: [Google::Analytics::Data::V1beta::Metric.new(name: "activeUsers")],
  date_ranges: [Google::Analytics::Data::V1beta::DateRange.new(start_date: "2026-05-01", end_date: "today")]
)

response = client.run_report request
response.rows.each do |row|
  puts "#{row.dimension_values.first.value}, #{row.metric_values.first.value}"
end
```
