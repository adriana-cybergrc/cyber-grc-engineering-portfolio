
import hashlib
import json
import sqlite3

from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path


# Version 1: persistent finding and remediation lifecycle.
# Version 2: decouple remediation_events from remediation_history.
SCHEMA_VERSION = 2

MIGRATIONS = {
    1: "persistent_finding_and_remediation_lifecycle",
    2: "decouple_remediation_events_from_legacy_history",
}

LIFECYCLE_TABLES = {
    "finding_entities",
    "finding_occurrences",
    "remediation_cases",
    "remediation_events",
}

ALLOWED_CASE_STATUSES = {
    "OPEN",
    "IN_REMEDIATION",
    "PENDING_VALIDATION",
    "RESOLVED",
    "REOPENED",
}

ALLOWED_VERIFICATION_RESULTS = {
    "PENDING",
    "PASS",
    "FAIL",
}


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect_database(db_path):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def _normalize_identity_component(value, field):
    """
    Normalizes one finding identity component.

    Case is preserved because source identifiers may be case-sensitive.
    """

    if value is None:
        raise ValueError(
            f"Missing required finding identity field: {field}"
        )

    normalized = str(value).strip()

    if not normalized:
        raise ValueError(
            f"Missing required finding identity field: {field}"
        )

    return normalized


def _finding_identity_values(finding):
    """
    Returns the canonical identity components used by hashing
    and persistence.
    """

    required_fields = (
        "control_id",
        "finding_type",
        "source_type",
        "source_record_id",
    )

    return tuple(
        _normalize_identity_component(
            finding.get(field),
            field,
        )
        for field in required_fields
    )


def finding_identity(finding):
    """
    Generates a stable SHA-256 identity for a finding.

    Identity:
    control_id | finding_type | source_type | source_record_id

    The original delimiter-based algorithm is retained for
    compatibility with previously persisted finding keys.
    """

    values = _finding_identity_values(finding)
    identity_string = "|".join(values)

    return hashlib.sha256(
        identity_string.encode("utf-8")
    ).hexdigest()


def _table_exists(connection, table_name):
    row = connection.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table'
          AND name = ?
        """,
        (table_name,),
    ).fetchone()

    return row is not None


def _create_legacy_schema(connection):
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


def _create_remediation_events_table(connection, table_name):
    """
    Creates remediation_events.

    source_history_id remains a nullable unique reference to
    legacy history records, without a foreign key dependency.
    """

    if table_name not in {
        "remediation_events",
        "remediation_events_new",
    }:
        raise ValueError(
            "Invalid remediation events table name."
        )

    connection.execute(f"""
        CREATE TABLE {table_name} (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            actor TEXT NOT NULL,
            reason TEXT NOT NULL,
            before_snapshot TEXT NOT NULL,
            after_snapshot TEXT NOT NULL,
            occurred_at TEXT NOT NULL,
            source_history_id INTEGER UNIQUE,
            FOREIGN KEY (case_id)
                REFERENCES remediation_cases(case_id)
        )
    """)


def _migrate_remediation_events_schema(connection):
    """
    Removes the obsolete foreign key from source_history_id.

    Existing event records and event IDs are preserved.

    Must run inside the transaction controlled by initialize_database().
    """

    if not _table_exists(connection, "remediation_events"):
        return

    foreign_keys = connection.execute(
        "PRAGMA foreign_key_list(remediation_events)"
    ).fetchall()

    legacy_history_fk = any(
        row["table"] == "remediation_history"
        and row["from"] == "source_history_id"
        for row in foreign_keys
    )

    if not legacy_history_fk:
        return

    connection.execute(
        "DROP TABLE IF EXISTS remediation_events_new"
    )

    _create_remediation_events_table(
        connection,
        "remediation_events_new",
    )

    connection.execute("""
        INSERT INTO remediation_events_new (
            event_id,
            case_id,
            event_type,
            actor,
            reason,
            before_snapshot,
            after_snapshot,
            occurred_at,
            source_history_id
        )
        SELECT
            event_id,
            case_id,
            event_type,
            actor,
            reason,
            before_snapshot,
            after_snapshot,
            occurred_at,
            source_history_id
        FROM remediation_events
    """)

    connection.execute(
        "DROP TABLE remediation_events"
    )

    connection.execute("""
        ALTER TABLE remediation_events_new
        RENAME TO remediation_events
    """)


def _validate_migration_history(connection):
    """
    Validates migration versions, names and lifecycle tables.

    Rejects unsupported versions, inconsistent migration history,
    and missing lifecycle tables in an already migrated database.
    """

    if not _table_exists(connection, "schema_migrations"):
        existing_lifecycle_tables = {
            table
            for table in LIFECYCLE_TABLES
            if _table_exists(connection, table)
        }

        if existing_lifecycle_tables:
            raise RuntimeError(
                "Inconsistent database schema: lifecycle tables "
                "exist without schema_migrations. "
                f"Detected tables: {sorted(existing_lifecycle_tables)}"
            )

        return {}

    rows = connection.execute("""
        SELECT version, migration_name
        FROM schema_migrations
        ORDER BY version
    """).fetchall()

    recorded = {}

    for row in rows:
        version = row["version"]
        migration_name = row["migration_name"]

        expected_name = MIGRATIONS.get(version)

        if expected_name is None:
            raise RuntimeError(
                f"Unsupported database migration version: {version}. "
                f"Current supported version: {SCHEMA_VERSION}."
            )

        if migration_name != expected_name:
            raise RuntimeError(
                "Migration history mismatch: "
                f"version {version} expects '{expected_name}', "
                f"but the database records '{migration_name}'."
            )

        recorded[version] = migration_name

    if 2 in recorded and 1 not in recorded:
        raise RuntimeError(
            "Inconsistent migration history: version 2 exists "
            "without version 1."
        )

    existing_lifecycle_tables = {
        table
        for table in LIFECYCLE_TABLES
        if _table_exists(connection, table)
    }

    if existing_lifecycle_tables and 1 not in recorded:
        raise RuntimeError(
            "Inconsistent database schema: lifecycle tables exist "
            "without migration version 1. "
            f"Detected tables: {sorted(existing_lifecycle_tables)}"
        )

    if 1 in recorded:
        missing_tables = (
            LIFECYCLE_TABLES - existing_lifecycle_tables
        )

        if missing_tables:
            raise RuntimeError(
                "Inconsistent migrated database: migration version 1 "
                "is recorded, but lifecycle tables are missing. "
                f"Missing tables: {sorted(missing_tables)}"
            )

    return recorded


def _record_migration(connection, version):
    migration_name = MIGRATIONS[version]

    existing = connection.execute(
        """
        SELECT migration_name
        FROM schema_migrations
        WHERE version = ?
        """,
        (version,),
    ).fetchone()

    if existing is not None:
        if existing["migration_name"] != migration_name:
            raise RuntimeError(
                "Migration version/name conflict: "
                f"version {version}."
            )

        return

    connection.execute(
        """
        INSERT INTO schema_migrations (
            version,
            migration_name,
            applied_at
        )
        VALUES (?, ?, ?)
        """,
        (
            version,
            migration_name,
            utc_now(),
        ),
    )


def _create_lifecycle_schema(connection):
    """
    Creates or upgrades the lifecycle schema.

    All operations execute inside the transaction controlled
    by initialize_database().
    """

    recorded_migrations = _validate_migration_history(
        connection
    )

    connection.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            migration_name TEXT NOT NULL,
            applied_at TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS finding_entities (
            finding_key TEXT PRIMARY KEY,
            control_id TEXT NOT NULL,
            finding_type TEXT NOT NULL,
            source_type TEXT NOT NULL,
            source_record_id TEXT NOT NULL,
            severity TEXT NOT NULL,
            first_seen_at TEXT NOT NULL,
            last_seen_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE (
                control_id,
                finding_type,
                source_type,
                source_record_id
            )
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS finding_occurrences (
            occurrence_id INTEGER PRIMARY KEY AUTOINCREMENT,
            finding_key TEXT NOT NULL,
            finding_id INTEGER NOT NULL UNIQUE,
            run_id INTEGER NOT NULL,
            details_snapshot TEXT NOT NULL,
            observed_at TEXT NOT NULL,
            FOREIGN KEY (finding_key)
                REFERENCES finding_entities(finding_key),
            FOREIGN KEY (finding_id)
                REFERENCES audit_findings(finding_id),
            FOREIGN KEY (run_id)
                REFERENCES audit_runs(run_id)
        )
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_finding_occurrences_run
        ON finding_occurrences(run_id)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_finding_occurrences_key
        ON finding_occurrences(finding_key)
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS remediation_cases (
            case_id TEXT PRIMARY KEY,
            finding_key TEXT NOT NULL UNIQUE,
            case_status TEXT NOT NULL CHECK (
                case_status IN (
                    'OPEN',
                    'IN_REMEDIATION',
                    'PENDING_VALIDATION',
                    'RESOLVED',
                    'REOPENED'
                )
            ),
            owner TEXT NOT NULL DEFAULT '',
            corrective_action TEXT NOT NULL DEFAULT '',
            evidence_reference TEXT NOT NULL DEFAULT '',
            validated_at TEXT NOT NULL DEFAULT '',
            verification_result TEXT NOT NULL CHECK (
                verification_result IN (
                    'PENDING',
                    'PASS',
                    'FAIL'
                )
            ),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (finding_key)
                REFERENCES finding_entities(finding_key)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS remediation_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            actor TEXT NOT NULL,
            reason TEXT NOT NULL,
            before_snapshot TEXT NOT NULL,
            after_snapshot TEXT NOT NULL,
            occurred_at TEXT NOT NULL,
            source_history_id INTEGER UNIQUE,
            FOREIGN KEY (case_id)
                REFERENCES remediation_cases(case_id)
        )
    """)

    # Version 1 creates the lifecycle schema.
    if 1 not in recorded_migrations:
        _record_migration(connection, 1)

    # Version 2 removes the legacy history foreign key.
    _migrate_remediation_events_schema(connection)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_remediation_events_case
        ON remediation_events(case_id)
    """)

    foreign_keys = connection.execute(
        "PRAGMA foreign_key_list(remediation_events)"
    ).fetchall()

    legacy_history_fk = any(
        row["table"] == "remediation_history"
        and row["from"] == "source_history_id"
        for row in foreign_keys
    )

    if legacy_history_fk:
        raise RuntimeError(
            "Schema migration failed: remediation_events still "
            "depends on remediation_history."
        )

    _record_migration(connection, 2)

    final_history = _validate_migration_history(
        connection
    )

    if set(final_history) != set(MIGRATIONS):
        raise RuntimeError(
            "Database migration history is incomplete."
        )


def initialize_database(db_path):
    """
    Initializes legacy and lifecycle schemas.

    Schema creation, migration execution and migration history
    updates are transactional.
    """

    with closing(connect_database(db_path)) as connection:
        with connection:
            _create_legacy_schema(connection)
            _create_lifecycle_schema(connection)


def _snapshot_case(row):
    if row is None:
        return {}

    fields = (
        "case_id",
        "finding_key",
        "case_status",
        "owner",
        "corrective_action",
        "evidence_reference",
        "validated_at",
        "verification_result",
        "created_at",
        "updated_at",
    )

    return {
        field: row[field]
        for field in fields
    }


def _insert_remediation_event(
    connection,
    case_id,
    event_type,
    actor,
    reason,
    before_snapshot,
    after_snapshot,
    occurred_at,
    source_history_id=None,
):
    connection.execute(
        """
        INSERT INTO remediation_events (
            case_id,
            event_type,
            actor,
            reason,
            before_snapshot,
            after_snapshot,
            occurred_at,
            source_history_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            case_id,
            event_type,
            actor,
            reason,
            json.dumps(
                before_snapshot,
                ensure_ascii=False,
                sort_keys=True,
            ),
            json.dumps(
                after_snapshot,
                ensure_ascii=False,
                sort_keys=True,
            ),
            occurred_at,
            source_history_id,
        ),
    )


def _upsert_finding_entity(
    connection,
    finding,
    finding_key,
    observed_at,
):
    identity_fields = (
        "control_id",
        "finding_type",
        "source_type",
        "source_record_id",
    )

    identity_values = _finding_identity_values(finding)

    expected_key = hashlib.sha256(
        "|".join(identity_values).encode("utf-8")
    ).hexdigest()

    if finding_key != expected_key:
        raise ValueError(
            "Finding key does not match its normalized identity."
        )

    connection.execute(
        """
        INSERT INTO finding_entities (
            finding_key,
            control_id,
            finding_type,
            source_type,
            source_record_id,
            severity,
            first_seen_at,
            last_seen_at,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(finding_key)
        DO UPDATE SET
            severity = excluded.severity,
            last_seen_at = excluded.last_seen_at
        """,
        (
            finding_key,
            *identity_values,
            finding["severity"],
            observed_at,
            observed_at,
            observed_at,
        ),
    )

    stored = connection.execute(
        """
        SELECT
            control_id,
            finding_type,
            source_type,
            source_record_id
        FROM finding_entities
        WHERE finding_key = ?
        """,
        (finding_key,),
    ).fetchone()

    if stored is None:
        raise RuntimeError(
            f"Finding entity was not persisted: {finding_key}"
        )

    stored_identity = tuple(
        stored[field]
        for field in identity_fields
    )

    if stored_identity != identity_values:
        raise ValueError(
            "Finding identity collision or inconsistent identity data "
            f"for finding_key={finding_key}"
        )


def _ensure_remediation_case(
    connection,
    finding_key,
    observed_at,
):
    existing = connection.execute(
        """
        SELECT *
        FROM remediation_cases
        WHERE finding_key = ?
        """,
        (finding_key,),
    ).fetchone()

    if existing is None:
        case_id = finding_key

        connection.execute(
            """
            INSERT INTO remediation_cases (
                case_id,
                finding_key,
                case_status,
                owner,
                corrective_action,
                evidence_reference,
                validated_at,
                verification_result,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                case_id,
                finding_key,
                "OPEN",
                "",
                "",
                "",
                "",
                "PENDING",
                observed_at,
                observed_at,
            ),
        )

        created_case = connection.execute(
            """
            SELECT *
            FROM remediation_cases
            WHERE case_id = ?
            """,
            (case_id,),
        ).fetchone()

        _insert_remediation_event(
            connection=connection,
            case_id=case_id,
            event_type="CASE_CREATED",
            actor="SYSTEM",
            reason=(
                "Remediation case automatically created "
                "for a new finding."
            ),
            before_snapshot={},
            after_snapshot=_snapshot_case(created_case),
            occurred_at=observed_at,
        )

        return

    # Preserve remediation data when a finding recurs.
    if existing["case_status"] == "RESOLVED":
        before_snapshot = _snapshot_case(existing)

        connection.execute(
            """
            UPDATE remediation_cases
            SET
                case_status = 'REOPENED',
                verification_result = 'PENDING',
                validated_at = '',
                updated_at = ?
            WHERE case_id = ?
            """,
            (
                observed_at,
                existing["case_id"],
            ),
        )

        reopened_case = connection.execute(
            """
            SELECT *
            FROM remediation_cases
            WHERE case_id = ?
            """,
            (existing["case_id"],),
        ).fetchone()

        _insert_remediation_event(
            connection=connection,
            case_id=existing["case_id"],
            event_type="CASE_REOPENED",
            actor="SYSTEM",
            reason=(
                "Finding reappeared in a subsequent audit run after "
                "the remediation case had been resolved."
            ),
            before_snapshot=before_snapshot,
            after_snapshot=_snapshot_case(reopened_case),
            occurred_at=observed_at,
        )


def _insert_audit_findings(
    connection,
    run_id,
    findings,
    observed_at,
):
    for finding in findings:
        # Corrected INSERT: five columns, five placeholders,
        # and five corresponding values, including run_id.
        cursor = connection.execute(
            """
            INSERT INTO audit_findings (
                run_id,
                control_id,
                finding_type,
                severity,
                details
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                run_id,
                finding["control_id"],
                finding["finding_type"],
                finding["severity"],
                finding["details"],
            ),
        )

        finding_id = cursor.lastrowid

        has_source_type = bool(
            str(finding.get("source_type") or "").strip()
        )

        has_source_record_id = bool(
            str(finding.get("source_record_id") or "").strip()
        )

        # Legacy findings without structured identity remain
        # in audit_findings but are not mapped to lifecycle tables.
        if not has_source_type and not has_source_record_id:
            continue

        # Partial identity is invalid and rolls back the audit run.
        if has_source_type != has_source_record_id:
            raise ValueError(
                "Both source_type and source_record_id are required "
                "to register a finding in the lifecycle tables."
            )

        finding_key = finding_identity(finding)

        _upsert_finding_entity(
            connection=connection,
            finding=finding,
            finding_key=finding_key,
            observed_at=observed_at,
        )

        connection.execute(
            """
            INSERT INTO finding_occurrences (
                finding_key,
                finding_id,
                run_id,
                details_snapshot,
                observed_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                finding_key,
                finding_id,
                run_id,
                finding["details"],
                observed_at,
            ),
        )

        _ensure_remediation_case(
            connection=connection,
            finding_key=finding_key,
            observed_at=observed_at,
        )


def save_audit_run(db_path, controls_evaluated, findings):
    """
    Saves an audit run and all associated findings.

    Audit and lifecycle records are committed atomically.
    If any operation fails, the entire run is rolled back.
    """

    initialize_database(db_path)

    observed_at = utc_now()

    with closing(connect_database(db_path)) as connection:
        with connection:
            cursor = connection.execute(
                """
                INSERT INTO audit_runs (
                    executed_at,
                    controls_evaluated,
                    findings_count
                )
                VALUES (?, ?, ?)
                """,
                (
                    observed_at,
                    controls_evaluated,
                    len(findings),
                ),
            )

            run_id = cursor.lastrowid

            _insert_audit_findings(
                connection=connection,
                run_id=run_id,
                findings=findings,
                observed_at=observed_at,
            )

    return run_id


def get_audit_history(db_path):
    initialize_database(db_path)

    with closing(connect_database(db_path)) as connection:
        rows = connection.execute(
            """
            SELECT
                run_id,
                executed_at,
                controls_evaluated,
                findings_count
            FROM audit_runs
            ORDER BY run_id
            """
        ).fetchall()

    return [dict(row) for row in rows]


def get_findings_for_run(db_path, run_id):
    initialize_database(db_path)

    with closing(connect_database(db_path)) as connection:
        rows = connection.execute(
            """
            SELECT
                finding_id,
                run_id,
                control_id,
                finding_type,
                severity,
                details
            FROM audit_findings
            WHERE run_id = ?
            ORDER BY finding_id
            """,
            (run_id,),
        ).fetchall()

    return [dict(row) for row in rows]
