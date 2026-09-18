---
name: data-pack
description: Data tooling decision tree: dbt for transformation, Dagster/Airflow for orchestration, DuckDB/Polars for compute, Iceberg for table format, lakehouse vs warehouse, data quality patterns
when_to_use: Building data pipelines, warehouses, feature stores, analytics platforms
applies_to:
  - data-platform
---

# Data Domain Pack

> Extends `data-platform` archetype with domain-specific depth for pipelines, warehouses, feature stores, analytics, and time-series systems.
> Loaded when `packs: [data-pack]` is in PROJECT.md or auto-loaded for `data-platform` archetype.

## QA Extras Reference

### `data-lineage` — End-to-End Lineage (data-warehouse, data-pipeline)
- **What**: Trace every output field to its source
- **Tool**: OpenLineage integration or manual lineage doc
- **Threshold**: 100% of output fields traced to source, no orphan transformations
- **Artifact**: Lineage graph in `docs/qa-reports/`

### `pii-classification` — PII Scan (data-warehouse, data-pipeline)
- **What**: Identify and classify PII in all data stores
- **Tool**: Schema scan + regex patterns (email, phone, SSN, credit card)
- **Threshold**: All PII fields tagged with classification level, no unclassified PII
- **Categories**: Public, Internal, Confidential, Restricted

### `schema-diff` — Schema Migration Safety (data-warehouse, db-migration)
- **What**: Compare schema before and after migration
- **Tool**: `schemadiff`, `alembic check`, or `prisma migrate diff`
- **Threshold**: No data loss columns dropped, no type narrowing without explicit migration
- **Report**: Schema diff in `docs/qa-reports/`

### `point-in-time` — Point-in-Time Correctness (feature-store)
- **What**: Verify features are computed using only data available at query time (no future leakage)
- **Tool**: Compare feature values at historical timestamp vs current computation
- **Threshold**: 0 future-leaked features
- **Edge cases**: Late-arriving data, timezone boundaries, DST transitions

### `online-offline-consistency` — Online/Offline Parity (feature-store)
- **What**: Verify online serving values match offline training values for same entity+timestamp
- **Tool**: Sample N entities, compare online API response vs offline table
- **Threshold**: Exact match for categorical features, ≤0.1% relative error for numeric

### `freshness-sla` — Data Freshness (data-pipeline, data-warehouse)
- **What**: Verify data arrives within SLA
- **Tool**: Compare latest partition timestamp vs current time
- **Threshold**: Freshness ≤ PROJECT.md `freshness-sla:` value (default: 1h for streaming, 24h for batch)
- **Alert**: If freshness exceeds 2× SLA, flag as P1

### `snapshot-regression` — Visual/Data Regression (data-visualization)
- **What**: Compare dashboard output before and after change
- **Tool**: Screenshot comparison or data hash comparison
- **Threshold**: 0 unintended visual changes, 0 data discrepancies

### `backtest-validation` — Historical Backtest (time-series-forecasting)
- **What**: Validate model on historical holdout data
- **Tool**: Walk-forward cross-validation (expanding or sliding window)
- **Threshold**: MAPE ≤ PROJECT.md `qa-MAPE-threshold:` value (default: 10%)
- **Anti-leakage**: Verify no future data in feature computation

### `rollback-dry-run` — Migration Rollback (db-migration)
- **What**: Verify down migration executes cleanly
- **Tool**: `alembic downgrade --dry-run` or `flyway undo -dryRun`
- **Threshold**: Exit 0, no data loss, schema returns to previous state
- **Mandatory for**: any production schema change

### `dbt-test` — dbt Model Testing (data-warehouse)
- **What**: Run dbt test suite (schema + data tests)
- **Tool**: `dbt test --select <changed_models>+`
- **Threshold**: 0 test failures, no untested models in changed set
- **Include**: unique, not_null, accepted_values, relationships tests at minimum

### `contract-validation` — Data Contract (data-pipeline)
- **What**: Verify data conforms to published contract (schema, SLA, quality)
- **Tool**: Great Expectations, Soda, or custom contract validator
- **Threshold**: 0 contract violations
- **Contract fields**: schema (types + nullability), freshness SLA, uniqueness constraints, allowed value ranges

## Compliance Extras

### `data-lineage-compliance` — Regulatory Lineage (SOX, GDPR)
- For SOX: every number in financial reports traceable to source system
- For GDPR: every PII field traceable to data subject consent
- Artifact: `docs/compliance/data-lineage-audit.md`

### `retention-policy` — Data Retention
- Document retention period per data category
- Verify automated deletion after retention expiry
- Verify right-to-erasure works end-to-end for PII
- Artifact: `docs/compliance/retention-policy.md`

### `data-residency` — Geographic Data Residency
- Identify data storage locations per dataset
- Verify compliance with geographic restrictions (EU data stays in EU, etc.)
- Document cross-border transfer mechanisms (SCCs, BCRs)
- Artifact: `docs/compliance/data-residency.md`

## Tooling Reference (2026 stack)

The data tooling landscape consolidated significantly between 2023-2026. Here's what to default to:

### Transformation

| Tool | When |
|------|------|
| **dbt Core / dbt Cloud** | SQL-first transformation, defines models + tests + docs together. Default for warehouse work. |
| **SQLMesh** | dbt alternative with virtual environments, easier dev workflow |
| **Spark** (Databricks) | Big data + ML workloads, when SQL alone isn't enough |
| **Polars** | Pandas replacement, 10-100× faster, Rust core | Default for in-process analysis (replaces pandas in 2026) |
| **DuckDB** | Embedded analytical DB, blazing on local files (Parquet, CSV, JSON) | Default for local exploratory analysis + ETL |

For new project: dbt + DuckDB for dev, dbt + Snowflake/BigQuery for production. Polars for any custom Python transformation logic.

### Orchestration

| Tool | When |
|------|------|
| **Dagster** | Asset-based, type-checked, modern. Best DX of any orchestrator. | Default for new projects |
| **Airflow 3.x** | Industry standard, vast operator library, mature | Pick if team has Airflow experience |
| **Prefect** | Pythonic, dynamic DAGs, hosted option | Lighter alternative to Airflow |
| **Mage** | Notebook-first, fast iteration | For experimentation-heavy teams |
| **Temporal** | Workflow engine with durable execution | For event-driven workflows, not pure ETL |

For new project without strong opinion: **Dagster** in 2026. Software engineering best practices baked in (typed assets, asset-level tests, declarative scheduling, partitions, backfills as a first-class concept).

### Data warehouse / lakehouse

| Tool | When |
|------|------|
| **Snowflake** | Industry default, mature, multi-cloud | Pick when budget allows |
| **BigQuery** | GCP-native, serverless, generous free tier | Pick if already on GCP |
| **Databricks** | Lakehouse, deep Spark + ML integration | Pick for AI/ML-heavy workloads |
| **ClickHouse** | OLAP, blazing fast, self-hostable | Pick for high-throughput analytics, time-series |
| **DuckDB** + **Iceberg** | Lakehouse pattern without compute layer | New: emerging "small data" lakehouse |

### Lakehouse (Iceberg)

Apache Iceberg has become the de-facto open lakehouse format in 2026 (winning over Delta and Hudi for new projects):

- **Storage**: Parquet files in S3/GCS/Azure Blob
- **Catalog**: AWS Glue, Snowflake Polaris, Tabular, or self-hosted via REST catalog
- **Compute**: Spark, Trino, DuckDB, Snowflake, BigQuery — all read Iceberg natively
- **Why**: time travel (snapshot-based), schema evolution, hidden partitioning, ACID transactions on object storage

For new lakehouse: Iceberg + DuckDB for small/dev, Iceberg + Snowflake or Spark for production.

### Streaming

| Tool | When |
|------|------|
| **Kafka** + **Flink** | Standard for high-volume event streaming |
| **Confluent Cloud** | Managed Kafka, lower operational burden |
| **Redpanda** | Kafka-compatible, single binary, lower latency |
| **Materialize** | Streaming SQL, incremental views |
| **RisingWave** | Open-source streaming DB, Postgres-wire-compatible |

### Data quality

| Tool | When |
|------|------|
| **Great Expectations** | Pythonic, comprehensive, Python ecosystem | Default if you're Python-shop |
| **Soda Core** | YAML-driven, lightweight, multi-language | Default if you want config-driven |
| **dbt tests** | If on dbt anyway, start here, add specialised tools as needed |
| **Monte Carlo** / **Bigeye** | Hosted observability, incident detection | When data outages cost money |

### Catalog & discovery

| Tool | When |
|------|------|
| **DataHub** | Open-source, LinkedIn-built, mature | Default for new self-hosted |
| **OpenMetadata** | Alternative, more polished UI | Same role as DataHub |
| **Atlan** / **Alation** | Hosted, enterprise focus | Pick when budget allows |

### Vector data (when crossing into AI)

See `ai-pack.md` § Vector databases. For pure data-platform: **pgvector** if you need it; otherwise Pinecone/Qdrant/Weaviate.

### Recommended `PROJECT.md` for new data-platform project

```yaml
primary: data-pipeline
archetype: data-platform
project_size: medium
stack: [python, dbt, dagster, snowflake, polars]
team-size: 2
compliance: [pii-classification, data-lineage]
qa-extras: [data-lineage, dbt-test, freshness-sla, contract-validation]
packs: [data-pack]
```
