import sqlite3
import tempfile
import unittest
from pathlib import Path

from tools.grc_sqlite_profiler import inspect_database


class TestGrcSqliteProfiler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Path(self.temp_dir.name) / "sample.db"
        with sqlite3.connect(self.database) as connection:
            connection.executescript(
                """
                CREATE TABLE schema_migrations (
                    version INTEGER PRIMARY KEY,
                    migration_name TEXT NOT NULL,
                    applied_at TEXT NOT NULL
                );
                INSERT INTO schema_migrations
                VALUES (1, 'initial', '2026-01-01T00:00:00+00:00');
                CREATE TABLE parent (
                    parent_id INTEGER PRIMARY KEY,
                    label TEXT NOT NULL
                );
                CREATE TABLE child (
                    child_id INTEGER PRIMARY KEY,
                    parent_id INTEGER NOT NULL,
                    FOREIGN KEY(parent_id) REFERENCES parent(parent_id)
                );
                CREATE INDEX idx_child_parent ON child(parent_id);
                INSERT INTO parent(label) VALUES ('SENSITIVE_VALUE_NOT_EXPORTED');
                INSERT INTO child(parent_id) VALUES (1);
                """
            )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_reports_schema_and_counts_without_business_values(self):
        report = inspect_database(self.database)
        objects = {item["name"]: item for item in report["objects"]}

        self.assertEqual(report["inspection_mode"], "read-only")
        self.assertFalse(report["business_data_exported"])
        self.assertEqual(objects["parent"]["row_count"], 1)
        self.assertEqual(objects["child"]["row_count"], 1)
        self.assertEqual(
            objects["child"]["foreign_keys"][0]["referenced_table"],
            "parent",
        )
        self.assertIn(
            "parent_id",
            objects["child"]["indexes"][0]["columns"],
        )
        self.assertEqual(
            report["migration_history"],
            [{"version": 1, "migration_name": "initial"}],
        )
        self.assertNotIn("SENSITIVE_VALUE_NOT_EXPORTED", str(report))

    def test_database_is_not_modified(self):
        before = self.database.read_bytes()
        inspect_database(self.database)
        after = self.database.read_bytes()
        self.assertEqual(before, after)

    def test_missing_database_fails_closed(self):
        missing = self.database.parent / "missing.db"
        with self.assertRaises(FileNotFoundError):
            inspect_database(missing)


if __name__ == "__main__":
    unittest.main()
