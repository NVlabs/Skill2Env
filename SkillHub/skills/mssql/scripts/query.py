#!/usr/bin/env python3
"""
Read-only MSSQL query executor.
Connects to configured databases and executes SELECT queries only.
"""

import json
import os
import re
import stat
import sys
import argparse
from pathlib import Path
from typing import Optional

try:
    import pymssql
except ImportError:
    print("Error: pymssql not installed. Run: pip install pymssql")
    sys.exit(1)

# Constants
SCRIPT_DIR = Path(__file__).parent.parent
CONFIG_LOCATIONS = [
    SCRIPT_DIR / "connections.json",
    Path.home() / ".config" / "claude" / "mssql-connections.json",
]
MAX_ROWS = 10000
MAX_COLUMN_WIDTH = 100
QUERY_TIMEOUT_SEC = 30
CONNECTION_TIMEOUT_SEC = 10
NULL_DISPLAY = "<NULL>"


def is_read_only(query: str) -> bool:
    """Client-side query validation. Since pymssql has no server-side read-only mode,
    this is a critical safety layer. Use a db_datareader role user for defense in depth."""
    query_upper = query.upper().strip()

    # Block WITH...DELETE/UPDATE/INSERT/MERGE (CTE used for writes)
    if query_upper.startswith('WITH'):
        # Extract the action after the CTE: WITH x AS (...) <ACTION>
        # Only allow SELECT after the CTE
        match = re.search(r'\)\s*(\w+)', query_upper)
        if match and match.group(1) != 'SELECT':
            return False
        if not match:
            return False
        return True

    # Exact match for sp_help (not prefix match)
    if re.match(r'^EXEC\s+SP_HELP\b', query_upper) or re.match(r'^SP_HELP\b', query_upper):
        return True

    safe_starts = ('SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN')
    if not any(query_upper.startswith(cmd) for cmd in safe_starts):
        return False

    # Block SELECT INTO (creates tables)
    if re.search(r'\bSELECT\b.*\bINTO\b', query_upper):
        return False

    return True


def validate_single_statement(query: str) -> bool:
    """Check query contains only one statement."""
    clean = query.rstrip().rstrip(';')
    return ';' not in clean


def validate_config_permissions(path: Path) -> None:
    """Warn if config file has insecure permissions (Unix only)."""
    if os.name != 'nt':
        mode = path.stat().st_mode
        if bool(mode & stat.S_IRWXG) or bool(mode & stat.S_IRWXO):
            print(f"WARNING: {path} has insecure permissions!")
            print(f"Config contains credentials. Run: chmod 600 {path}")


def validate_db_config(db: dict) -> None:
    """Validate required fields exist in database config."""
    required = ['name', 'host', 'database', 'user', 'password']
    missing = [f for f in required if f not in db]
    if missing:
        print(f"Error: Database config missing fields: {', '.join(missing)}")
        sys.exit(1)


def find_config() -> Optional[Path]:
    """Find config file in supported locations."""
    for path in CONFIG_LOCATIONS:
        if path.exists():
            return path
    return None


def load_config(config_path: Optional[Path] = None) -> dict:
    """Load database connections from JSON config."""
    path = config_path or find_config()
    if not path:
        print("Config not found. Searched:")
        for loc in CONFIG_LOCATIONS:
            print(f"  - {loc}")
        print("\nCreate connections.json with format:")
        print(json.dumps({
            "databases": [{
                "name": "mydb",
                "description": "Description of database contents",
                "host": "localhost",
                "port": 1433,
                "database": "mydb",
                "user": "user",
                "password": "password",
                "tds_version": "7.3"
            }]
        }, indent=2))
        sys.exit(1)

    validate_config_permissions(path)

    with open(path) as f:
        return json.load(f)


def list_databases(config: dict) -> None:
    """List all configured databases."""
    print("Configured databases:\n")
    for db in config.get("databases", []):
        validate_db_config(db)
        print(f"  [{db['name']}]")
        print(f"    Host: {db['host']}:{db.get('port', 1433)}")
        print(f"    Database: {db['database']}")
        print(f"    Description: {db.get('description', 'No description')}")
        print()


def execute_query(db_config: dict, query: str, limit: Optional[int] = None) -> None:
    """Execute a read-only query against the specified database."""
    if not is_read_only(query):
        print("Error: Only read-only queries (SELECT, SHOW, EXPLAIN, WITH) are allowed.")
        sys.exit(1)

    if not validate_single_statement(query):
        print("Error: Multiple statements not allowed. Execute queries separately.")
        sys.exit(1)

    # Apply TOP limit for MSSQL (uses TOP instead of LIMIT)
    if limit and not re.search(r'\bTOP\s+\d+', query, re.IGNORECASE):
        query = query.rstrip(';')
        if query.upper().strip().startswith('WITH'):
            # CTE: insert TOP after the outer SELECT (after CTE closing paren)
            match = re.search(r'\)\s*(SELECT(?:\s+DISTINCT)?)\b', query, re.IGNORECASE)
            if match:
                pos = match.start(1)
                original = match.group(1)
                query = query[:pos] + f'{original} TOP {limit}' + query[pos + len(original):]
        else:
            # Handle SELECT DISTINCT and plain SELECT; use re.MULTILINE for leading whitespace
            query = re.sub(
                r'(SELECT(?:\s+DISTINCT)?)\b',
                rf'\1 TOP {limit}',
                query, count=1, flags=re.IGNORECASE | re.MULTILINE
            )

    conn = None
    try:
        conn_kwargs = {
            'server': db_config['host'],
            'port': str(db_config.get('port', 1433)),
            'database': db_config['database'],
            'user': db_config['user'],
            'password': db_config['password'],
            'login_timeout': CONNECTION_TIMEOUT_SEC,
            'timeout': QUERY_TIMEOUT_SEC,
            'as_dict': False,
        }

        # TDS version configuration
        if db_config.get('tds_version'):
            conn_kwargs['tds_version'] = db_config['tds_version']

        # Encryption support
        if db_config.get('encrypt', False):
            conn_kwargs['encryption'] = 'require'

        conn = pymssql.connect(**conn_kwargs)

        conn.autocommit(True)
        # Note: pymssql has no native read-only session mode like PostgreSQL/MySQL.
        # Protection relies on client-side is_read_only() validation above.
        # For production use, configure the database user with db_datareader role only.

        with conn.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchmany(MAX_ROWS)
                truncated = len(rows) == MAX_ROWS

                # Calculate column widths with cap
                widths = [min(len(col), MAX_COLUMN_WIDTH) for col in columns]
                for row in rows:
                    for i, val in enumerate(row):
                        val_str = str(val) if val is not None else NULL_DISPLAY
                        widths[i] = min(max(widths[i], len(val_str)), MAX_COLUMN_WIDTH)

                # Print header
                header = " | ".join(col[:MAX_COLUMN_WIDTH].ljust(widths[i]) for i, col in enumerate(columns))
                print(header)
                print("-" * len(header))

                # Print rows
                for row in rows:
                    cells = []
                    for i, val in enumerate(row):
                        val_str = str(val) if val is not None else NULL_DISPLAY
                        if len(val_str) > MAX_COLUMN_WIDTH:
                            val_str = val_str[:MAX_COLUMN_WIDTH-3] + "..."
                        cells.append(val_str.ljust(widths[i]))
                    print(" | ".join(cells))

                msg = f"\n({len(rows)} rows)"
                if truncated:
                    msg += f" [truncated at {MAX_ROWS}]"
                print(msg)
            else:
                print("Query executed (no result set returned)")

    except pymssql.Error as e:
        error_msg = str(e)
        if 'password' in error_msg.lower() or 'login failed' in error_msg.lower():
            error_msg = "Authentication failed. Check credentials in connections.json"
        print(f"Database error: {error_msg}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()


def find_database(config: dict, name: str) -> dict:
    """Find database config by name (case-insensitive)."""
    for db in config.get("databases", []):
        if db.get('name', '').lower() == name.lower():
            validate_db_config(db)
            return db
    available = [db.get('name', 'unnamed') for db in config.get("databases", [])]
    print(f"Database '{name}' not found.")
    print(f"Available: {', '.join(available)}")
    sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Execute read-only MSSQL queries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list
  %(prog)s --db mydb --tables
  %(prog)s --db mydb --query "SELECT TOP 10 * FROM users"
  %(prog)s --db mydb --query "SELECT * FROM users" --limit 100
        """
    )
    parser.add_argument("--config", "-c", type=Path, help="Path to config JSON")
    parser.add_argument("--db", "-d", help="Database name to query")
    parser.add_argument("--query", "-q", help="SQL query to execute")
    parser.add_argument("--limit", "-l", type=int, help="Limit rows returned (uses TOP N)")
    parser.add_argument("--list", action="store_true", help="List configured databases")
    parser.add_argument("--schema", "-s", action="store_true", help="Show database schema")
    parser.add_argument("--tables", "-t", action="store_true", help="List tables")

    args = parser.parse_args()
    config = load_config(args.config)

    if args.list:
        list_databases(config)
        return

    if not args.db:
        print("Error: --db required. Use --list to see available databases.")
        sys.exit(1)

    db_config = find_database(config, args.db)

    if args.tables:
        query = """
            SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA NOT IN ('sys', 'INFORMATION_SCHEMA', 'guest')
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """
        execute_query(db_config, query, args.limit)
    elif args.schema:
        query = """
            SELECT c.TABLE_SCHEMA, c.TABLE_NAME, c.COLUMN_NAME, c.DATA_TYPE, c.IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS c
            JOIN INFORMATION_SCHEMA.TABLES t
                ON c.TABLE_NAME = t.TABLE_NAME AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
            WHERE c.TABLE_SCHEMA NOT IN ('sys', 'INFORMATION_SCHEMA', 'guest')
            ORDER BY c.TABLE_SCHEMA, c.TABLE_NAME, c.ORDINAL_POSITION
        """
        execute_query(db_config, query, args.limit)
    elif args.query:
        execute_query(db_config, args.query, args.limit)
    else:
        print("Error: --query, --tables, or --schema required")
        sys.exit(1)


if __name__ == "__main__":
    main()
