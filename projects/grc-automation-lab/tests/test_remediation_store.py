

import importlib.util
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "remediation_store.py"
)

SPEC = importlib.util.spec_from_file_location(
    "remediation_store", MODULE_PATH
)
store = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(store)


class TestRemediationStore(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Path(self.temp_dir.name) / "audit.db"

    def tearDown(self):
        self.temp_dir.cleanup()

    def save(self, **overrides):
        values = {
            "control_id": "CTRL002",
            "finding_type": "EVIDENCE_EXPIRED",
            "owner": "Security Governance",
            "corrective_action": (
                "Obtain a current vulnerability scan report"
            ),
            "evidence_reference": "evidence/EV002-2026.pdf",
            "validated_at": "2026-10-23T10:00:00+00:00",
            "verification_result": "PASS",
        }
        values.update(overrides)
        store.save_remediation(self.database, **values)

    def test_validated_requires_pass_date_and_evidence(self):
        self.save()

        rows = store.load_remediations(self.database)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["remediation_status"], "VALIDATED")

    def test_pass_without_evidence_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save(evidence_reference="")

    def test_pass_without_validation_timestamp_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save(validated_at="")

    def test_pass_with_timestamp_without_timezone_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save(validated_at="2026-10-23T10:00:00")

    def test_pass_with_invalid_timestamp_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save(validated_at="not-a-date")

    def test_required_fields_reject_whitespace(self):
        for field in (
            "owner",
            "control_id",
            "corrective_action",
            "finding_type",
        ):
            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    self.save(**{field: "   "})

    def test_pending_record_is_not_validated(self):
        self.save(
            evidence_reference="",
            validated_at="",
            verification_result="PENDING",
        )

        rows = store.load_remediations(self.database)

        self.assertEqual(
            rows[0]["remediation_status"],
            "IN_REMEDIATION",
        )
        self.assertEqual(rows[0]["validated_at"], "")

    def test_pass_to_pending_clears_current_validation_date(self):
        self.save()
        self.save(
            verification_result="PENDING",
            evidence_reference="",
            validated_at="",
        )

        rows = store.load_remediations(self.database)

        self.assertEqual(rows[0]["verification_result"], "PENDING")
        self.assertEqual(rows[0]["validated_at"], "")
        self.assertEqual(
            rows[0]["remediation_status"],
            "IN_REMEDIATION",
        )

    def test_pass_to_fail_clears_current_validation_date(self):
        self.save()
        self.save(
            verification_result="FAIL",
            evidence_reference="evidence/retest.txt",
        )

        rows = store.load_remediations(self.database)

        self.assertEqual(rows[0]["verification_result"], "FAIL")
        self.assertEqual(rows[0]["validated_at"], "")
        self.assertEqual(
            rows[0]["remediation_status"],
            "REJECTED",
        )

    def test_fail_is_rejected_and_history_records_each_save(self):
        self.save(
            verification_result="FAIL",
            validated_at="",
            evidence_reference="evidence/retest.txt",
        )
        self.save(
            verification_result="PENDING",
            validated_at="",
            evidence_reference="",
        )

        rows = store.load_remediations(self.database)

        self.assertEqual(
            rows[0]["remediation_status"],
            "IN_REMEDIATION",
        )

        with closing(sqlite3.connect(self.database)) as connection:
            history = connection.execute(
                """
                SELECT verification_result, validated_at
                FROM remediation_history
                ORDER BY history_id
                """
            ).fetchall()

        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], ("FAIL", ""))
        self.assertEqual(history[1], ("PENDING", ""))

    def test_invalid_result_is_rejected(self):
        with self.assertRaises(ValueError):
            self.save(verification_result="UNKNOWN")

    def test_status_requires_evidence_and_timezone_aware_timestamp(self):
        self.assertEqual(
            store.remediation_status({
                "verification_result": "PASS",
                "evidence_reference": "",
                "validated_at": "2026-10-23T10:00:00+00:00",
            }),
            "PENDING_VALIDATION",
        )

        self.assertEqual(
            store.remediation_status({
                "verification_result": "PASS",
                "evidence_reference": "evidence/report.pdf",
                "validated_at": "2026-10-23T10:00:00",
            }),
            "PENDING_VALIDATION",
        )

    def test_failed_save_does_not_persist_record_or_history(self):
        self.save()

        with closing(sqlite3.connect(self.database)) as connection:
            before_record = connection.execute(
                """
                SELECT
                    control_id,
                    finding_type,
                    owner,
                    corrective_action,
                    evidence_reference,
                    validated_at,
                    verification_result,
                    updated_at
                FROM remediation_records
                """
            ).fetchall()

            before_history = connection.execute(
                "SELECT COUNT(*) FROM remediation_history"
            ).fetchone()[0]

        with closing(sqlite3.connect(self.database)) as connection:
            connection.execute(
                """
                CREATE TRIGGER reject_history_insert
                BEFORE INSERT ON remediation_history
                BEGIN
                    SELECT RAISE(ABORT, 'simulated history failure');
                END
                """
            )

        with self.assertRaises(sqlite3.IntegrityError):
            self.save(
                verification_result="PENDING",
                evidence_reference="",
                validated_at="",
                corrective_action="Updated corrective action",
            )

        with closing(sqlite3.connect(self.database)) as connection:
            after_record = connection.execute(
                """
                SELECT
                    control_id,
                    finding_type,
                    owner,
                    corrective_action,
                    evidence_reference,
                    validated_at,
                    verification_result,
                    updated_at
                FROM remediation_records
                """
            ).fetchall()

            after_history = connection.execute(
                "SELECT COUNT(*) FROM remediation_history"
            ).fetchone()[0]

        self.assertEqual(after_record, before_record)
        self.assertEqual(after_history, before_history)

    def test_first_pending_save_is_classified_as_created(self):
        self.save(
            verification_result="PENDING",
            evidence_reference="",
            validated_at="",
        )

        with closing(sqlite3.connect(self.database)) as connection:
            event = connection.execute(
                "SELECT event_type FROM remediation_history"
            ).fetchone()[0]

        self.assertEqual(event, "CREATED")

    def test_same_result_update_is_classified_as_updated(self):
        self.save()
        self.save(change_reason="Updated corrective action")

        with closing(sqlite3.connect(self.database)) as connection:
            events = connection.execute(
                """
                SELECT event_type
                FROM remediation_history
                ORDER BY history_id
                """
            ).fetchall()

        self.assertEqual(
            [event[0] for event in events],
            ["VALIDATION", "UPDATED"],
        )

    def test_pass_to_pending_is_classified_as_reopened(self):
        self.save()
        self.save(
            verification_result="PENDING",
            evidence_reference="",
            validated_at="",
        )

        with closing(sqlite3.connect(self.database)) as connection:
            event = connection.execute(
                """
                SELECT event_type
                FROM remediation_history
                ORDER BY history_id DESC
                """
            ).fetchone()[0]

        self.assertEqual(event, "REOPENED")

    def test_pending_to_fail_is_classified_as_rejected(self):
        self.save(
            verification_result="PENDING",
            evidence_reference="",
            validated_at="",
        )
        self.save(
            verification_result="FAIL",
            evidence_reference="evidence/retest.txt",
            validated_at="",
        )

        with closing(sqlite3.connect(self.database)) as connection:
            event = connection.execute(
                """
                SELECT event_type
                FROM remediation_history
                ORDER BY history_id DESC
                """
            ).fetchone()[0]

        self.assertEqual(event, "REJECTED")

    def test_metadata_is_saved_to_current_record_and_history(self):
        self.save(
            recorded_by="analyst@example.com",
            validated_by="reviewer@example.com",
            change_reason="Retest evidence reviewed",
        )

        rows = store.load_remediations(self.database)

        self.assertEqual(
            rows[0]["recorded_by"],
            "analyst@example.com",
        )
        self.assertEqual(
            rows[0]["validated_by"],
            "reviewer@example.com",
        )
        self.assertEqual(
            rows[0]["change_reason"],
            "Retest evidence reviewed",
        )

        with closing(sqlite3.connect(self.database)) as connection:
            event = connection.execute(
                """
                SELECT
                    recorded_by,
                    validated_by,
                    change_reason,
                    event_type
                FROM remediation_history
                """
            ).fetchone()

        self.assertEqual(
            event,
            (
                "analyst@example.com",
                "reviewer@example.com",
                "Retest evidence reviewed",
                "VALIDATION",
            ),
        )

    def test_migrates_legacy_database_without_losing_rows(self):
        with closing(sqlite3.connect(self.database)) as connection, connection:
            connection.execute("""
                CREATE TABLE remediation_records (
                    control_id TEXT NOT NULL,
                    finding_type TEXT NOT NULL,
                    owner TEXT NOT NULL,
                    corrective_action TEXT NOT NULL,
                    evidence_reference TEXT NOT NULL DEFAULT '',
                    validated_at TEXT NOT NULL DEFAULT '',
                    verification_result TEXT NOT NULL DEFAULT 'PENDING',
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (control_id, finding_type)
                )
            """)

            connection.execute("""
                CREATE TABLE remediation_history (
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
            """)

            connection.execute(
                """
                INSERT INTO remediation_records
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "CTRL001",
                    "MISSING_EVIDENCE",
                    "Team",
                    "Collect evidence",
                    "",
                    "",
                    "PENDING",
                    "2026-10-01T00:00:00+00:00",
                ),
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
                    recorded_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "CTRL001",
                    "MISSING_EVIDENCE",
                    "Team",
                    "Collect evidence",
                    "",
                    "",
                    "PENDING",
                    "2026-10-01T00:00:00+00:00",
                ),
            )

        store.initialize_remediation_store(self.database)
        rows = store.load_remediations(self.database)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["control_id"], "CTRL001")
        self.assertEqual(rows[0]["recorded_by"], "")

        with closing(sqlite3.connect(self.database)) as connection:
            self.assertEqual(
                connection.execute(
                    "SELECT COUNT(*) FROM remediation_history"
                ).fetchone()[0],
                1,
            )

            record_columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(remediation_records)"
                )
            }
            history_columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(remediation_history)"
                )
            }

        self.assertTrue(
            {"recorded_by", "validated_by", "change_reason"}
            .issubset(record_columns)
        )
        self.assertTrue(
            {
                "recorded_by",
                "validated_by",
                "change_reason",
                "event_type",
            }.issubset(history_columns)
        )

    def test_missing_database_returns_empty_list(self):
        missing_database = Path(self.temp_dir.name) / "missing.db"

        self.assertEqual(
            store.load_remediations(missing_database),
            [],
        )


if __name__ == "__main__":
    unittest.main()
