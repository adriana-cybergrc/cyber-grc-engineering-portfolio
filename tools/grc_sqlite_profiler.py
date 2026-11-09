"""Read-only SQLite schema profiler for the Cyber GRC portfolio.

The profiler reports schema metadata and row counts only. It never returns
business records or modifies the inspected database.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def _quote_identifier(value: str) -> str:
    """Safely quote a SQLite identifier for metadata-only COUNT queries."""
    return '"' + value.replace('"', '""') + '"'


def inspect_database(database_path: str | Path) -> dict:
    """Inspect tables, columns, indexes, foreign keys and row counts read-only."""
    path = Path(database_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"SQLite database not found: {path}")

    uri = path.as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row

    try:
        connection.execute("PRAGMA query_only = ON")
        objects = connection.execute(
            """
            SELECT type, name, tbl_name, sql
            FROM sqlite_master
            WHERE type IN ('table', 'view', 'index')
              AND name NOT LIKE 'sqlite_%'
            ORDER BY type, name
            """
        ).fetchall()

        tables = []
        for item in objects:
            if item["type"] not in {"table", "view"}:
                continue

            name = item["name"]
            quoted = _quote_identifier(name)
            columns = [
                {
                    "name": row["name"],
                    "type": row["type"],
                    "not_null": bool(row["notnull"]),
                    "default": row["dflt_value"],
                    "primary_key_position": row["pk"],
                }
                for row in connection.execute(
                    f"PRAGMA table_info({quoted})"
                ).fetchall()
            ]
            foreign_keys = [
                {
                    "id": row["id"],
                    "sequence": row["seq"],
                    "referenced_table": row["table"],
                    "from_column": row["from"],
                    "to_column": row["to"],
                    "on_update": row["on_update"],
                    "on_delete": row["on_delete"],
                }
                for row in connection.execute(
                    f"PRAGMA foreign_key_list({quoted})"
                ).fetchall()
            ]
            indexes = []
            if item["type"] == "table":
                index_rows = connection.execute(
                    f"PRAGMA index_list({quoted})"
                ).fetchall()
                for index in index_rows:
                    index_name = index["name"]
                    index_columns = [
                        row["name"]
                        for row in connection.execute(
                            f"PRAGMA index_info({_quote_identifier(index_name)})"
                        ).fetchall()
                    ]
                    indexes.append({
                        "name": index_name,
                        "unique": bool(index["unique"]),
                        "origin": index["origin"],
                        "columns": index_columns,
                    })
                row_count = connection.execute(
                    f"SELECT COUNT(*) FROM {quoted}"
                ).fetchone()[0]
            else:
                row_count = None

            tables.append({
                "name": name,
                "object_type": item["type"],
                "columns": columns,
                "foreign_keys": foreign_keys,
                "indexes": indexes,
                "row_count": row_count,
            })

        migration_history = []
        if any(t["name"] == "schema_migrations" for t in tables):
            migration_history = [
                dict(row)
                for row in connection.execute(
                    """
                    SELECT version, migration_name
                    FROM schema_migrations
                    ORDER BY version
                    """
                ).fetchall()
            ]

        return {
            "database": path.name,
            "inspection_mode": "read-only",
            "business_data_exported": False,
            "objects": tables,
            "migration_history": migration_history,
        }
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON report path. The inspected database remains read-only.",
    )
    args = parser.parse_args()

    try:
        report = inspect_database(args.database)
    except (OSError, sqlite3.Error) as exc:
        parser.error(str(exc))

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
