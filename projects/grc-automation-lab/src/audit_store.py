
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect_database(db_path):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path):
    with closing(connect_database(db_path)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS audit_runs (
                    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    executed_at TEXT NOT NULL,
                    controls_evaluated INTEGER NOT NULL,
                    findings_count INTEGER NOT NULL
                )
            """)
            connection.execute("""
                CREATE TABLE IF NOT EXISTS audit_findings (
                    finding_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INTEGER NOT NULL,
                    control_id TEXT NOT NULL,
                    finding_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    details TEXT NOT NULL,
                    FOREIGN KEY (run_id)
                        REFERENCES audit_runs(run_id)
                )
            """)


def save_audit_run(db_path, controls_evaluated, findings):
    initialize_database(db_path)

    with closing(connect_database(db_path)) as connection:
        with connection:
            cursor = connection.execute(
                """
                INSERT INTO audit_runs
                    (executed_at, controls_evaluated, findings_count)
                VALUES (?, ?, ?)
                """,
                (utc_now(), controls_evaluated, len(findings)),
            )
            run_id = cursor.lastrowid

            connection.executemany(
                """
                INSERT INTO audit_findings
                    (run_id, control_id, finding_type, severity, details)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        run_id,
                        finding["control_id"],
                        finding["finding_type"],
                        finding["severity"],
                        finding["details"],
                    )
                    for finding in findings
                ],
            )

    return run_id


def get_audit_history(db_path):
    initialize_database(db_path)

    with closing(connect_database(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("""
            SELECT run_id, executed_at, controls_evaluated, findings_count
            FROM audit_runs
            ORDER BY run_id
        """).fetchall()

    return [dict(row) for row in rows]


def get_findings_for_run(db_path, run_id):
    initialize_database(db_path)

    with closing(connect_database(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT finding_id, run_id, control_id, finding_type,
                   severity, details
            FROM audit_findings
            WHERE run_id = ?
            ORDER BY finding_id
            """,
            (run_id,),
        ).fetchall()

    return [dict(row) for row in rows]
