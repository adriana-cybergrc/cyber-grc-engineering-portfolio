
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

    def test_displays_operational_exposure_and_remediation_caveat(self):
        self.write_csv(
            "operational_metrics.csv",
            [
                "item_type", "item_id", "control_id", "issue_type",
                "status", "due_date", "days_overdue", "owner",
                "remediation_status",
            ],
            [
                [
                    "TASK", "TASK003", "CTRL003", "SLA_OVERDUE",
                    "Pending", "2026-10-20", "3", "HR", "NOT_TRACKED",
                ],
                [
                    "EVIDENCE", "EV002", "CTRL002", "EVIDENCE_EXPIRED",
                    "Submitted", "2026-10-01", "22", "", "NOT_TRACKED",
                ],
            ],
        )

        output = dashboard.build_dashboard(self.analytics_dir)
        content = output.read_text(encoding="utf-8")

        self.assertIn("Evidence issues", content)
        self.assertIn("Overdue tasks", content)
        self.assertIn("Days overdue", content)
        self.assertIn("NOT_TRACKED", content)
        self.assertIn("does not independently validate remediation", content)

    def test_displays_formal_remediation_register_and_validated_count(self):
        self.write_csv(
            "remediation_register.csv",
            [
                "control_id", "finding_type", "owner", "corrective_action",
                "evidence_reference", "validated_at", "verification_result",
                "remediation_status", "updated_at",
            ],
            [
                [
                    "CTRL002", "EVIDENCE_EXPIRED", "Security Governance",
                    "Replace expired report", "evidence/EV002.pdf",
                    "2026-10-23T10:00:00+00:00", "PASS", "VALIDATED",
                    "2026-10-23T10:01:00+00:00",
                ],
            ],
        )

        output = dashboard.build_dashboard(self.analytics_dir)
        content = output.read_text(encoding="utf-8")

        self.assertIn("Formal remediation register", content)
        self.assertIn("Security Governance", content)
        self.assertIn("Validated remediations", content)
        self.assertIn("evidence/EV002.pdf", content)

    def test_rejects_validated_claim_when_verification_fails(self):
        row = {
            "verification_result": "FAIL",
            "evidence_reference": "evidence/EV002.pdf",
            "validated_at": "2026-10-23T10:00:00+00:00",
            "remediation_status": "VALIDATED",
        }

        status = dashboard.formal_remediation_status(row)

        self.assertEqual(status, "REJECTED")

    def test_pass_without_evidence_is_not_validated(self):
        row = {
            "verification_result": "PASS",
            "evidence_reference": "",
            "validated_at": "2026-10-23T10:00:00+00:00",
            "remediation_status": "VALIDATED",
        }

        status = dashboard.formal_remediation_status(row)

        self.assertEqual(status, "PENDING_VALIDATION")

    def test_pass_without_timezone_aware_timestamp_is_not_validated(self):
        row = {
            "verification_result": "PASS",
            "evidence_reference": "evidence/EV002.pdf",
            "validated_at": "2026-10-23T10:00:00",
            "remediation_status": "VALIDATED",
        }

        status = dashboard.formal_remediation_status(row)

        self.assertEqual(status, "PENDING_VALIDATION")

    def test_missing_operational_metrics_are_reported_as_unavailable(self):
        metrics_file = self.analytics_dir / "operational_metrics.csv"
        self.assertFalse(metrics_file.exists())

        output = dashboard.build_dashboard(self.analytics_dir)
        content = output.read_text(encoding="utf-8")

        self.assertIn("N/A", content)

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
