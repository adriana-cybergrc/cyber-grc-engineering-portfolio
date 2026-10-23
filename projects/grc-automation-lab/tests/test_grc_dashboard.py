
import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "grc_dashboard.py"
)

SPEC = importlib.util.spec_from_file_location(
    "grc_dashboard", SCRIPT_PATH
)
dashboard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard)


class TestGRCDashboard(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.analytics_dir = Path(self.temp_dir.name)

        self.write_csv(
            "execution_summary.csv",
            [
                "run_id", "executed_at", "controls_evaluated",
                "findings_count", "critical_count", "high_count",
                "medium_count", "low_count",
                "distinct_finding_types",
            ],
            [
                [
                    "1", "2026-10-23T10:00:00+00:00", "5",
                    "6", "0", "6", "0", "0", "4",
                ],
            ],
        )

        self.write_csv(
            "latest_comparison.csv",
            [
                "comparison", "status", "control_id",
                "finding_type", "severity", "details",
            ],
            [
                [
                    "1->2", "RECURRING", "CTRL002",
                    "EVIDENCE_EXPIRED", "HIGH",
                    "Evidence expired",
                ],
            ],
        )

        self.write_csv(
            "recurring_findings.csv",
            [
                "control_id", "finding_type", "occurrences",
                "latest_run_id", "latest_severity",
            ],
            [
                ["CTRL002", "EVIDENCE_EXPIRED", "2", "1", "HIGH"],
            ],
        )

    def write_csv(self, filename, headers, rows):
        with (self.analytics_dir / filename).open(
            "w", encoding="utf-8", newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_generates_dashboard_with_expected_metrics(self):
        output = dashboard.build_dashboard(self.analytics_dir)

        self.assertTrue(output.exists())
        content = output.read_text(encoding="utf-8")

        self.assertIn("Executive GRC Dashboard", content)
        self.assertIn("Controls evaluated", content)
        self.assertIn("CTRL002", content)
        self.assertIn("EVIDENCE_EXPIRED", content)
        self.assertIn("NOT_PRESENT_IN_LATEST", content)

    def test_escapes_untrusted_csv_content(self):
        self.write_csv(
            "latest_comparison.csv",
            [
                "comparison", "status", "control_id",
                "finding_type", "severity", "details",
            ],
            [
                [
                    "1->2", "NEW", "CTRL999",
                    "TEST", "HIGH", "<script>alert(1)</script>",
                ],
            ],
        )

        output = dashboard.build_dashboard(self.analytics_dir)
        content = output.read_text(encoding="utf-8")

        self.assertNotIn("<script>alert(1)</script>", content)
        self.assertIn("&lt;script&gt;", content)

    def test_fails_when_required_csv_is_missing(self):
        (self.analytics_dir / "recurring_findings.csv").unlink()

        with self.assertRaises(FileNotFoundError):
            dashboard.build_dashboard(self.analytics_dir)


if __name__ == "__main__":
    unittest.main()
