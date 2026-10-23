import argparse
import sqlite3
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Display persisted GRC audit history"
    )
    parser.add_argument(
        "--database",
        default="projects/grc-automation-lab/runtime/grc_audit.db",
    )
    args = parser.parse_args()

    db_path = Path(args.database)
    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    with sqlite3.connect(db_path) as connection:
        rows = connection.execute("""
            SELECT run_id, executed_at, controls_evaluated, findings_count
            FROM audit_runs
            ORDER BY run_id DESC
        """).fetchall()

    if not rows:
        print("No audit runs recorded.")
        return

    print("RUN ID | EXECUTED AT | CONTROLS | FINDINGS")
    for run_id, executed_at, controls, findings in rows:
        print(
            f"{run_id} | {executed_at} | {controls} | {findings}"
        )


if __name__ == "__main__":
    main()
