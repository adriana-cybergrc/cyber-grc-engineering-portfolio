"""Persistent, auditable remediation register backed by SQLite.

A remediation is considered VALIDATED only when:
- verification_result is PASS;
- an evidence reference is supplied;
- validated_at is a valid ISO 8601 timestamp with a timezone.

The history table records each successful save operation. It is an audit
trail, but it is not immutable against direct database modification.
"""

import argparse
import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_DATABASE = Path(
    "projects/grc-automation-lab/runtime/grc_audit.db"
)

VALID_RESULTS = {"PENDING", "PASS", "FAIL"}


def _is_timezone_aware_iso(value):
    """Return True only for ISO 8601 timestamps with a timezone."""
    if not isinstance(value, str) or not value.strip():
        return False

    try:
        parsed = datetime.fromisoformat(
            value.strip().replace("Z", "+00:00")
        )
    except ValueError:
        return False

    return (
        parsed.tzinfo is not None
        and parsed.utcoffset() is not None
    )


def _ensure_columns(connection, table_name, columns):
    """Add missing columns without deleting existing records."""
    existing_columns = {
        row[1]
        for row in connection.execute(
            f"PRAGMA table_info({table_name})"
        ).fetchall()
    }

    for column_name, definition in columns.items():
        if column_name not in existing_columns:
            connection.execute(
                f"ALTER TABLE {table_name} "
                f"ADD COLUMN {column_name} {definition}"
            )


def initialize_remediation_store(database_path=DEFAULT_DATABASE):
    """Create the remediation tables and migrate older schemas safely."""
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(path)) as connection, connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS remediation_records (
                control_id TEXT NOT NULL,
                finding_type TEXT NOT NULL,
                owner TEXT NOT NULL,
                corrective_action TEXT NOT NULL,
                evidence_reference TEXT NOT NULL DEFAULT '',
                validated_at TEXT NOT NULL DEFAULT '',
                verification_result TEXT NOT NULL DEFAULT 'PENDING'
                    CHECK (
                        verification_result IN ('PENDING', 'PASS', 'FAIL')
                    ),
                updated_at TEXT NOT NULL,
                PRIMARY KEY (control_id, finding_type)
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS remediation_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                control_id TEXT NOT NULL,
                finding_type TEXT NOT NULL,
                owner TEXT NOT NULL,
                corrective_action TEXT NOT NULL,
                evidence_reference TEXT NOT NULL,
                validated_at TEXT NOT NULL,
                verification_result TEXT NOT NULL,
                recorded_at TEXT NOT NULL
            )
            """
        )

        _ensure_columns(
            connection,
            "remediation_records",
            {
                "recorded_by": "TEXT NOT NULL DEFAULT ''",
                "validated_by": "TEXT NOT NULL DEFAULT ''",
                "change_reason": "TEXT NOT NULL DEFAULT ''",
            },
        )

        _ensure_columns(
            connection,
            "remediation_history",
            {
                "recorded_by": "TEXT NOT NULL DEFAULT ''",
                "validated_by": "TEXT NOT NULL DEFAULT ''",
                "change_reason": "TEXT NOT NULL DEFAULT ''",
                "event_type": "TEXT NOT NULL DEFAULT 'UPSERT'",
                "before_snapshot": "TEXT",
                "after_snapshot": "TEXT",
            },
        )


def remediation_status(record):
    """Calculate the formal status from the underlying record fields."""
    if not record:
        return "NOT_TRACKED"

    result = str(
        record.get("verification_result") or "PENDING"
    ).strip().upper()

    evidence = str(
        record.get("evidence_reference") or ""
    ).strip()

    validated_at = str(
        record.get("validated_at") or ""
    ).strip()

    if result == "PASS":
        if evidence and _is_timezone_aware_iso(validated_at):
            return "VALIDATED"
        return "PENDING_VALIDATION"

    if result == "FAIL":
        return "REJECTED"

    if evidence:
        return "PENDING_VALIDATION"

    return "IN_REMEDIATION"


def _classify_event(previous_result, result):
    """Classify a save operation based on the previous and new results."""
    if previous_result is None:
        return "VALIDATION" if result == "PASS" else "CREATED"

    if previous_result == result:
        return "UPDATED"

    if result == "PASS":
        return "VALIDATION"

    if result == "FAIL":
        return "REJECTED"

    if result == "PENDING":
        return "REOPENED"

    return "UPDATED"


def save_remediation(
    database_path,
    *,
    control_id,
    finding_type,
    owner,
    corrective_action,
    evidence_reference="",
    validated_at="",
    verification_result="PENDING",
    recorded_by="",
    validated_by="",
    change_reason="",
):
    """Save the current remediation state and append an audit event.

    Actor and change metadata are optional for backward compatibility.
    The current record update and history insert share one transaction.
    """
    control_id = str(control_id or "").strip()
    finding_type = str(finding_type or "").strip()
    owner = str(owner or "").strip()
    corrective_action = str(corrective_action or "").strip()
    evidence_reference = str(evidence_reference or "").strip()
    validated_at = str(validated_at or "").strip()
    result = str(verification_result or "").strip().upper()
    recorded_by = str(recorded_by or "").strip()
    validated_by = str(validated_by or "").strip()
    change_reason = str(change_reason or "").strip()

    if not all(
        (control_id, finding_type, owner, corrective_action)
    ):
        raise ValueError(
            "control_id, finding_type, owner and corrective_action "
            "are required"
        )

    if result not in VALID_RESULTS:
        raise ValueError(
            f"verification_result must be one of {sorted(VALID_RESULTS)}"
        )

    if result == "PASS":
        if not evidence_reference or not validated_at:
            raise ValueError(
                "PASS requires evidence_reference and validated_at"
            )

        if not _is_timezone_aware_iso(validated_at):
            raise ValueError(
                "validated_at must be ISO 8601 with a timezone"
            )
    else:
        # Do not retain a previous validation timestamp after reopening
        # a remediation or rejecting the verification.
        validated_at = ""

    initialize_remediation_store(database_path)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with closing(sqlite3.connect(database_path)) as connection, connection:
        connection.row_factory = sqlite3.Row
        previous = connection.execute(
            """
            SELECT
                control_id, finding_type, owner, corrective_action,
                evidence_reference, validated_at, verification_result,
                updated_at, recorded_by, validated_by, change_reason
            FROM remediation_records
            WHERE control_id = ? AND finding_type = ?
            """,
            (control_id, finding_type),
        ).fetchone()

        previous_snapshot = (
            json.dumps(dict(previous), sort_keys=True, ensure_ascii=False)
            if previous else None
        )
        previous_result = previous["verification_result"] if previous else None
        event_type = _classify_event(previous_result, result)

        connection.execute(
            """
            INSERT INTO remediation_records (
                control_id,
                finding_type,
                owner,
                corrective_action,
                evidence_reference,
                validated_at,
                verification_result,
                updated_at,
                recorded_by,
                validated_by,
                change_reason
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(control_id, finding_type) DO UPDATE SET
                owner = excluded.owner,
                corrective_action = excluded.corrective_action,
                evidence_reference = excluded.evidence_reference,
                validated_at = excluded.validated_at,
                verification_result = excluded.verification_result,
                updated_at = excluded.updated_at,
                recorded_by = excluded.recorded_by,
                validated_by = excluded.validated_by,
                change_reason = excluded.change_reason
            """,
            (
                control_id,
                finding_type,
                owner,
                corrective_action,
                evidence_reference,
                validated_at,
                result,
                now,
                recorded_by,
                validated_by,
                change_reason,
            ),
        )

        current = connection.execute(
            """
            SELECT
                control_id, finding_type, owner, corrective_action,
                evidence_reference, validated_at, verification_result,
                updated_at, recorded_by, validated_by, change_reason
            FROM remediation_records
            WHERE control_id = ? AND finding_type = ?
            """,
            (control_id, finding_type),
        ).fetchone()

        current_snapshot = json.dumps(
            dict(current), sort_keys=True, ensure_ascii=False
        )

        connection.execute(
            """
            INSERT INTO remediation_history (
                control_id,
                finding_type,
                owner,
                corrective_action,
                evidence_reference,
                validated_at,
                verification_result,
                recorded_at,
                recorded_by,
                validated_by,
                change_reason,
                event_type,
                before_snapshot,
                after_snapshot
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                control_id,
                finding_type,
                owner,
                corrective_action,
                evidence_reference,
                validated_at,
                result,
                now,
                recorded_by,
                validated_by,
                change_reason,
                event_type,
                previous_snapshot,
                current_snapshot,
            ),
        )


def load_remediations(database_path=DEFAULT_DATABASE):
    """Load current remediation records with calculated statuses."""
    path = Path(database_path)

    if not path.exists():
        return []

    with closing(sqlite3.connect(path)) as connection:
        connection.row_factory = sqlite3.Row

        try:
            rows = connection.execute(
                """
                SELECT
                    control_id,
                    finding_type,
                    owner,
                    corrective_action,
                    evidence_reference,
                    validated_at,
                    verification_result,
                    updated_at,
                    recorded_by,
                    validated_by,
                    change_reason
                FROM remediation_records
                ORDER BY control_id, finding_type
                """
            ).fetchall()
        except sqlite3.OperationalError:
            # The database exists but lacks the expected table.
            return []

    results = []

    for row in rows:
        record = dict(row)
        record["remediation_status"] = remediation_status(record)
        results.append(record)

    return results






def load_remediation_history(database_path=DEFAULT_DATABASE):
    """Load remediation audit events with backward-compatible schema support."""
    path = Path(database_path)

    if not path.exists():
        return []

    with closing(sqlite3.connect(path)) as connection:
        connection.row_factory = sqlite3.Row

        try:
            existing_tables = {
                row["name"]
                for row in connection.execute(
                    """
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table'
                    """
                ).fetchall()
            }

            if "remediation_history" not in existing_tables:
                return []

            existing_columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(remediation_history)"
                ).fetchall()
            }

            required_columns = [
                "history_id",
                "recorded_at",
                "control_id",
                "finding_type",
                "owner",
                "corrective_action",
                "evidence_reference",
                "validated_at",
                "verification_result",
            ]

            if not set(required_columns).issubset(existing_columns):
                return []

            optional_columns = [
                "event_type",
                "recorded_by",
                "validated_by",
                "change_reason",
                "before_snapshot",
                "after_snapshot",
            ]

            selected_columns = required_columns + [
                column
                for column in optional_columns
                if column in existing_columns
            ]

            rows = connection.execute(
                f"""
                SELECT {", ".join(selected_columns)}
                FROM remediation_history
                ORDER BY recorded_at DESC, history_id DESC
                """
            ).fetchall()

        except sqlite3.OperationalError:
            return []

    results = []

    for row in rows:
        record = dict(row)

        record.setdefault("recorded_by", "")
        record.setdefault("validated_by", "")
        record.setdefault("change_reason", "")
        record.setdefault("before_snapshot", None)
        record.setdefault("after_snapshot", None)

        if not record.get("event_type"):
            record["event_type"] = (
                "VALIDATION"
                if record.get("validated_at")
                or record.get("verification_result")
                not in ("", "PENDING", None)
                else "REMEDIATION_UPDATE"
            )

        results.append(record)

    return results




def main():
    parser = argparse.ArgumentParser(
        description="Record a GRC remediation status"
    )
    parser.add_argument(
        "--database",
        default=str(DEFAULT_DATABASE),
    )
    parser.add_argument("--control-id", required=True)
    parser.add_argument("--finding-type", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--corrective-action", required=True)
    parser.add_argument("--evidence-reference", default="")
    parser.add_argument("--validated-at", default="")
    parser.add_argument(
        "--verification-result",
        choices=sorted(VALID_RESULTS),
        default="PENDING",
    )
    parser.add_argument("--recorded-by", default="")
    parser.add_argument("--validated-by", default="")
    parser.add_argument("--change-reason", default="")

    args = parser.parse_args()

    save_remediation(
        args.database,
        control_id=args.control_id,
        finding_type=args.finding_type,
        owner=args.owner,
        corrective_action=args.corrective_action,
        evidence_reference=args.evidence_reference,
        validated_at=args.validated_at,
        verification_result=args.verification_result,
        recorded_by=args.recorded_by,
        validated_by=args.validated_by,
        change_reason=args.change_reason,
    )

    record = {
        "verification_result": args.verification_result,
        "evidence_reference": args.evidence_reference,
        "validated_at": (
            args.validated_at
            if args.verification_result == "PASS"
            else ""
        ),
    }

    print(
        "Remediation record saved: "
        f"{args.control_id} / {args.finding_type}"
    )
    print(f"Status: {remediation_status(record)}")


if __name__ == "__main__":
    main()
