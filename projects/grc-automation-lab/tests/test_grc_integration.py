"""End-to-end integration tests for the GRC reporting pipeline."""

import csv
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_DIR / "src"
REPOSITORY_ROOT = PROJECT_DIR.parents[1]

sys.path.insert(0, str(SRC_DIR))

from audit_store import save_audit_run
from grc_dashboard import build_dashboard
from remediation_store import save_remediation


class TestGRCRemediationIntegration(unittest.TestCase):
    """Verify SQLite -> analytics CSV -> executive dashboard."""

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)

        self.temp_path = Path(self.temp_directory.name)
        self.database_path = self.temp_path / "grc_audit.db"
        self.analytics_dir = self.temp_path / "analytics"

        save_audit_run(
            self.database_path,
            controls_evaluated=1,
            findings=[
                {
                    "control_id": "AC-01",
                    "finding_type": "MISSING_EVIDENCE",
                    "severity": "HIGH",
                    "details": "Integration test finding",
                }
            ],
        )

    def run_analytics_and_dashboard(self):
        """Run actual analytics and render its HTML dashboard."""
        result = subprocess.run(
            [
                sys.executable,
                str(SRC_DIR / "grc_analytics.py"),
                "--database",
                str(self.database_path),
                "--output-dir",
                str(self.analytics_dir),
            ],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=(
                "Analytics execution failed.\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
            ),
        )

        register_path = self.analytics_dir / "remediation_register.csv"
        self.assertTrue(register_path.is_file())

        with register_path.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            records = list(csv.DictReader(file))

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["control_id"], "AC-01")

        dashboard_path = build_dashboard(self.analytics_dir)
        self.assertTrue(dashboard_path.is_file())

        dashboard_html = dashboard_path.read_text(encoding="utf-8")
        return records[0], dashboard_html

    def test_valid_remediation_is_validated_end_to_end(self):
        """PASS, evidence and timezone-aware date must be VALIDATED."""
        save_remediation(
            self.database_path,
            control_id="AC-01",
            finding_type="MISSING_EVIDENCE",
            owner="Cybersecurity",
            corrective_action="Provide and verify the required evidence",
            evidence_reference="evidence/AC-01-validation.pdf",
            validated_at=datetime.now(timezone.utc).isoformat(
                timespec="seconds"
            ),
            verification_result="PASS",
        )

        record, dashboard_html = self.run_analytics_and_dashboard()

        self.assertEqual(record["verification_result"], "PASS")
        self.assertEqual(record["remediation_status"], "VALIDATED")
        self.assertIn("VALIDATED", dashboard_html)

    def test_pending_remediation_is_not_validated_end_to_end(self):
        """Pending remediation must not be reported as VALIDATED."""
        save_remediation(
            self.database_path,
            control_id="AC-01",
            finding_type="MISSING_EVIDENCE",
            owner="Cybersecurity",
            corrective_action="Complete the evidence submission",
            evidence_reference="evidence/AC-01-draft.pdf",
            verification_result="PENDING",
        )

        record, dashboard_html = self.run_analytics_and_dashboard()

        self.assertEqual(record["verification_result"], "PENDING")
        self.assertEqual(
            record["remediation_status"], "PENDING_VALIDATION"
        )
        self.assertIn("PENDING_VALIDATION", dashboard_html)
        self.assertNotIn(">VALIDATED<", dashboard_html)


class TestGRCFullPipelineIntegration(unittest.TestCase):
    """Exercise evaluation, SQLite persistence, analytics and dashboard."""

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)

        self.temp_path = Path(self.temp_directory.name)
        self.data_dir = self.temp_path / "data"
        self.data_dir.mkdir()

        self.database_path = self.temp_path / "grc_audit.db"
        self.findings_path = self.temp_path / "grc_findings.csv"
        self.analytics_dir = self.temp_path / "analytics"

        self.write_csv(
            "controls.csv",
            [
                "control_id",
                "control_name",
                "framework",
                "owner",
                "required_evidence",
                "active",
            ],
            [
                {
                    "control_id": "CTRL-TEST-01",
                    "control_name": "Test access control",
                    "framework": "ISO 27001",
                    "owner": "Cybersecurity",
                    "required_evidence": "Access review report",
                    "active": "true",
                }
            ],
        )

        # No evidence rows: this active control must produce a finding.
        self.write_csv(
            "evidence.csv",
            [
                "evidence_id",
                "control_id",
                "evidence_name",
                "status",
                "submission_date",
                "expiry_date",
            ],
            [],
        )

        # A fixed past due date makes the SLA finding deterministic.
        self.write_csv(
            "tasks.csv",
            [
                "task_id",
                "control_id",
                "task_name",
                "owner",
                "due_date",
                "status",
            ],
            [
                {
                    "task_id": "TASK-TEST-01",
                    "control_id": "CTRL-TEST-01",
                    "task_name": "Complete access review",
                    "owner": "Cybersecurity",
                    "due_date": "2000-01-01",
                    "status": "Open",
                }
            ],
        )

    def write_csv(self, filename, fieldnames, rows):
        """Create an isolated CSV using the project's expected schema."""
        path = self.data_dir / filename

        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def run_script(self, script_name, *arguments):
        """Run a project script and include diagnostics if it fails."""
        result = subprocess.run(
            [
                sys.executable,
                str(SRC_DIR / script_name),
                *map(str, arguments),
            ],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=(
                f"{script_name} failed.\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
            ),
        )

        return result

    def test_full_pipeline_generates_auditable_dashboard(self):
        """Verify evaluation -> SQLite -> analytics -> dashboard."""

        # 1. Run the actual control evaluation with temporary input data.
        evaluation = self.run_script(
            "grc_automation.py",
            "--data-dir",
            self.data_dir,
            "--output",
            self.findings_path,
            "--database",
            self.database_path,
        )

        self.assertIn("Controls evaluated: 1", evaluation.stdout)
        self.assertTrue(self.findings_path.is_file())

        with self.findings_path.open(
            "r", encoding="utf-8-sig", newline=""
        ) as file:
            findings = list(csv.DictReader(file))

        finding_types = {row["finding_type"] for row in findings}

        self.assertIn("MISSING_EVIDENCE", finding_types)
        self.assertIn("SLA_OVERDUE", finding_types)

        # 2. Verify audit history and finding persistence.
        # Explicit close is important for Windows temporary-directory cleanup.
        connection = sqlite3.connect(self.database_path)

        try:
            runs = connection.execute(
                "SELECT controls_evaluated, findings_count FROM audit_runs"
            ).fetchall()

            stored_findings = connection.execute(
                "SELECT finding_type FROM audit_findings"
            ).fetchall()
        finally:
            connection.close()

        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0][0], 1)
        self.assertEqual(runs[0][1], len(findings))
        self.assertEqual(
            {row[0] for row in stored_findings},
            finding_types,
        )

        # 3. Run analytics using only temporary database and input files.
        self.run_script(
            "grc_analytics.py",
            "--database",
            self.database_path,
            "--output-dir",
            self.analytics_dir,
            "--data-dir",
            self.data_dir,
        )

        expected_reports = [
            "remediation_register.csv",
            "operational_metrics.csv",
            "execution_summary.csv",
            "latest_comparison.csv",
            "recurring_findings.csv",
            "grc_analytics_report.md",
        ]

        for filename in expected_reports:
            with self.subTest(report=filename):
                self.assertTrue(
                    (self.analytics_dir / filename).is_file(),
                    f"Expected analytics report was not generated: {filename}",
                )

        # 4. Render the dashboard from the actual analytics output.
        self.run_script(
            "grc_dashboard.py",
            "--analytics-dir",
            self.analytics_dir,
        )

        dashboard_path = (
            self.analytics_dir / "grc_executive_dashboard.html"
        )
        self.assertTrue(dashboard_path.is_file())

        dashboard_html = dashboard_path.read_text(encoding="utf-8")

        self.assertIn("Executive GRC Dashboard", dashboard_html)
        self.assertIn("MISSING_EVIDENCE", dashboard_html)

        # SLA_OVERDUE is asserted in the findings CSV above.
        # The dashboard currently summarizes SLA exposure through operational
        # metrics and does not necessarily render the raw finding type.
        self.assertIn("Evidence and SLA exposure", dashboard_html)


if __name__ == "__main__":
    unittest.main()
