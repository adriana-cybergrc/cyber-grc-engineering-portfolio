import unittest
from datetime import date

from pathlib import Path
import importlib.util

MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "src" / "grc_automation.py"
)
spec = importlib.util.spec_from_file_location("grc_automation", MODULE_PATH)
grc_automation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grc_automation)

evaluate_controls = grc_automation.evaluate_controls


class TestGRCAutomation(unittest.TestCase):
    def setUp(self):
        self.controls = [
            {
                "control_id": "CTRL001",
                "control_name": "Access Review",
                "active": "true",
            }
        ]
        self.today = date(2026, 10, 23)

    def test_detects_expired_evidence(self):
        evidence = [{
            "evidence_id": "EV001",
            "control_id": "CTRL001",
            "status": "Submitted",
            "expiry_date": "2026-10-01",
        }]
        findings = evaluate_controls(self.controls, evidence, [], self.today)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["finding_type"], "EVIDENCE_EXPIRED")

    def test_detects_overdue_task(self):
        tasks = [{
            "task_id": "TASK001",
            "control_id": "CTRL001",
            "status": "In Progress",
            "due_date": "2026-10-20",
        }]
        findings = evaluate_controls(self.controls, [], tasks, self.today)

        self.assertEqual(len(findings), 2)
        types = {item["finding_type"] for item in findings}
        self.assertEqual(
            types,
            {"MISSING_EVIDENCE", "SLA_OVERDUE"},
        )

    def test_no_finding_for_current_evidence_and_completed_task(self):
        evidence = [{
            "evidence_id": "EV002",
            "control_id": "CTRL001",
            "status": "Submitted",
            "expiry_date": "2027-01-10",
        }]
        tasks = [{
            "task_id": "TASK002",
            "control_id": "CTRL001",
            "status": "Completed",
            "due_date": "2026-10-20",
        }]
        findings = evaluate_controls(
            self.controls, evidence, tasks, self.today
        )

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
