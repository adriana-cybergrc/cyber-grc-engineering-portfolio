"""End-to-end integration tests for the GRC remediation reporting flow."""

import csv
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
        """Run the actual analytics script and render its HTML dashboard."""
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

        build_dashboard(self.analytics_dir)

        dashboard_path = (
            self.analytics_dir / "grc_executive_dashboard.html"
        )
        self.assertTrue(dashboard_path.is_file())

        dashboard_html = dashboard_path.read_text(encoding="utf-8")

        return records[0], dashboard_html

    def test_valid_remediation_is_validated_end_to_end(self):
        """PASS plus evidence and a timezone-aware date must be VALIDATED."""
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
        """A pending remediation must not be reported as VALIDATED."""
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


if __name__ == "__main__":
    unittest.main()
