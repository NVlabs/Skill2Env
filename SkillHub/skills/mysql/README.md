# mysql

Read-only MySQL query skill. Query multiple databases safely with write protection.

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
      "port": 3306,
      "database": "app_prod",
      "user": "readonly",
      "password": "secret",
      "ssl_disabled": false
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

# Run query
python3 scripts/query.py --db prod --query "SELECT * FROM users" --limit 100
```

## Config Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| name | Yes | - | Database identifier |
| description | Yes | - | What data it contains (for auto-selection) |
| host | Yes | - | Hostname |
| port | No | 3306 | Port |
| database | Yes | - | Database name |
| user | Yes | - | Username |
| password | Yes | - | Password |
| ssl_disabled | No | false | Disable SSL connections |
| ssl_ca | No | - | Path to CA certificate |
| ssl_cert | No | - | Path to client certificate |
| ssl_key | No | - | Path to client private key |

## Safety Features

- **Read-only sessions**: MySQL `SET SESSION TRANSACTION READ ONLY` blocks writes at session level
- **Query validation**: Only SELECT, SHOW, DESCRIBE, EXPLAIN, WITH allowed
- **Single statement**: No multi-statement queries (prevents `SELECT 1; DROP TABLE`)
- **Timeouts**: 30s query timeout (max_execution_time), 10s connection timeout
- **Memory cap**: Max 10,000 rows per query
- **Credential protection**: Passwords sanitized from error messages

## Requirements

```bash
pip install mysql-connector-python
```
