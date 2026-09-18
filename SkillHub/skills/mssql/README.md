# mssql

Read-only Microsoft SQL Server query skill. Query multiple databases safely with write protection.

## Setup

1. Copy the example config:
```bash
cp connections.example.json connections.json
```

2. Add your database credentials:
```json
{
  "databases": [
    {
      "name": "prod",
      "description": "Production - users, orders, transactions",
      "host": "db.example.com",
      "port": 1433,
      "database": "app_prod",
      "user": "readonly",
      "password": "secret",
      "encrypt": true,
      "tds_version": "7.3"
    }
  ]
}
```

3. Secure the config:
```bash
chmod 600 connections.json
```

## Usage

```bash
# List configured databases
python3 scripts/query.py --list

# List tables
python3 scripts/query.py --db prod --tables

# Show schema
python3 scripts/query.py --db prod --schema

# Run query (MSSQL uses TOP instead of LIMIT)
python3 scripts/query.py --db prod --query "SELECT TOP 10 * FROM users"

# Or use --limit flag (auto-converts to TOP N)
python3 scripts/query.py --db prod --query "SELECT * FROM users" --limit 100
```

## Config Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| name | Yes | - | Database identifier |
| description | Yes | - | What data it contains (for auto-selection) |
| host | Yes | - | Hostname |
| port | No | 1433 | Port |
| database | Yes | - | Database name |
| user | Yes | - | Username |
| password | Yes | - | Password |
| encrypt | No | false | Enable TLS encryption |
| tds_version | No | auto | TDS protocol version (7.0, 7.1, 7.2, 7.3, 7.4) |

## Safety Features

- **Read-only transaction**: `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED` for read-only access
- **Query validation**: Only SELECT, SHOW, EXPLAIN, WITH, SP_HELP allowed
- **Single statement**: No multi-statement queries (prevents `SELECT 1; DROP TABLE`)
- **Timeouts**: 30s query timeout, 10s login timeout
- **Memory cap**: Max 10,000 rows per query
- **Credential protection**: Passwords sanitized from error messages

## Requirements

```bash
pip install pymssql
```
