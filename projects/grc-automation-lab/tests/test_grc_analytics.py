import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "grc_analytics.py"
)

SPEC = importlib.util.spec_from_file_location(
    "grc_analytics", MODULE_PATH
)
grc_analytics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(grc_analytics)


class TestGRCAnalytics(unittest.TestCase):

    def setUp(self):
        self.runs = [
            {
                "run_id": 1,
                "executed_at": "2026-10-22T10:00:00",
                "controls_evaluated": 5,
                "findings_count": 3,
            },
            {
                "run_id": 2,
                "executed_at": "2026-10-23T10:00:00",
                "controls_evaluated": 5,
                "findings_count": 2,
            },
        ]

        self.findings = [
            {
                "run_id": 1,
                "control_id": "CTRL001",
                "finding_type": "EVIDENCE_EXPIRED",
                "severity": "HIGH",
                "details": "Evidence expired.",
            },
            {
                "run_id": 1,
                "control_id": "CTRL002",
                "finding_type": "SLA_OVERDUE",
                "severity": "MEDIUM",
                "details": "Task overdue.",
            },
            {
                "run_id": 1,
                "control_id": "CTRL003",
                "finding_type": "MISSING_EVIDENCE",
                "severity": "LOW",
                "details": "Evidence missing.",
            },
            {
                "run_id": 2,
                "control_id": "CTRL001",
                "finding_type": "EVIDENCE_EXPIRED",
                "severity": "HIGH",
                "details": "Evidence remains expired.",
            },
            {
                "run_id": 2,
                "control_id": "CTRL004",
                "finding_type": "SLA_OVERDUE",
                "severity": "CRITICAL",
                "details": "New overdue task.",
            },
        ]

    def test_detects_new_recurring_and_absent_findings(self):
        _, comparison, _ = grc_analytics.analyze_history(
            self.runs, self.findings
        )

        statuses = {
            (
                item["control_id"],
                item["finding_type"],
            ): item["status"]
            for item in comparison
        }

        self.assertEqual(
            statuses[("CTRL004", "SLA_OVERDUE")], "NEW"
        )
        self.assertEqual(
            statuses[("CTRL001", "EVIDENCE_EXPIRED")],
            "RECURRING",
        )
        self.assertEqual(
            statuses[("CTRL002", "SLA_OVERDUE")],
            "NOT_PRESENT_IN_LATEST",
        )
        self.assertEqual(
            statuses[("CTRL003", "MISSING_EVIDENCE")],
            "NOT_PRESENT_IN_LATEST",
        )

    def test_counts_findings_by_severity(self):
        summary, _, _ = grc_analytics.analyze_history(
            self.runs, self.findings
        )

        latest = summary[-1]

        self.assertEqual(latest["findings_count"], 2)
        self.assertEqual(latest["critical_count"], 1)
        self.assertEqual(latest["high_count"], 1)
        self.assertEqual(latest["medium_count"], 0)
        self.assertEqual(latest["low_count"], 0)

    def test_identifies_recurring_findings(self):
        _, _, recurring = grc_analytics.analyze_history(
            self.runs, self.findings
        )

        self.assertEqual(len(recurring), 1)
        self.assertEqual(recurring[0]["control_id"], "CTRL001")
        self.assertEqual(
            recurring[0]["finding_type"], "EVIDENCE_EXPIRED"
        )
        self.assertEqual(recurring[0]["occurrences"], 2)
        self.assertEqual(recurring[0]["latest_run_id"], 2)
        self.assertEqual(recurring[0]["latest_severity"], "HIGH")

    def test_handles_execution_without_findings(self):
        runs = [self.runs[0]]
        summary, comparison, recurring = (
            grc_analytics.analyze_history(runs, [])
        )

        self.assertEqual(summary[0]["findings_count"], 0)
        self.assertEqual(summary[0]["critical_count"], 0)
        self.assertEqual(summary[0]["high_count"], 0)
        self.assertEqual(comparison, [])
        self.assertEqual(recurring, [])

    def test_requires_two_runs_for_comparison(self):
        summary, comparison, recurring = (
            grc_analytics.analyze_history(
                [self.runs[0]],
                self.findings[:3],
            )
        )

        self.assertEqual(len(summary), 1)
        self.assertEqual(comparison, [])
        self.assertEqual(recurring, [])


if __name__ == "__main__":
    unittest.main()