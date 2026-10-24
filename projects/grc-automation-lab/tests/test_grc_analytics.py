
import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "grc_analytics.py"
)

SPEC = importlib.util.spec_from_file_location(
    "grc_analytics", SCRIPT_PATH
)
analytics = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analytics)


class TestGRCAnalytics(unittest.TestCase):

    def setUp(self):
        self.runs = [
            {
                "run_id": 1,
                "executed_at": "2026-10-22T10:00:00+00:00",
                "controls_evaluated": 5,
            },
            {
                "run_id": 2,
                "executed_at": "2026-10-23T10:00:00+00:00",
                "controls_evaluated": 5,
            },
        ]

        self.findings = [
            {
                "run_id": 1,
                "control_id": "CTRL001",
                "finding_type": "EVIDENCE_EXPIRED",
                "severity": "HIGH",
                "details": "Evidence expired",
            },
            {
                "run_id": 1,
                "control_id": "CTRL002",
                "finding_type": "SLA_OVERDUE",
                "severity": "MEDIUM",
                "details": "Task overdue",
            },
            {
                "run_id": 2,
                "control_id": "CTRL001",
                "finding_type": "EVIDENCE_EXPIRED",
                "severity": "HIGH",
                "details": "Evidence expired",
            },
            {
                "run_id": 2,
                "control_id": "CTRL003",
                "finding_type": "MISSING_EVIDENCE",
                "severity": "CRITICAL",
                "details": "Evidence missing",
            },
        ]

    def test_detects_new_recurring_and_absent_findings(self):
        _, comparison, _ = analytics.analyze_history(
            self.runs, self.findings
        )

        statuses = {
            (item["control_id"], item["finding_type"]): item["status"]
            for item in comparison
        }

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
            "NEW",
        )

    def test_counts_findings_by_severity(self):
        summary, _, _ = analytics.analyze_history(
            self.runs, self.findings
        )

        first_run = summary[0]
        self.assertEqual(first_run["findings_count"], 2)
        self.assertEqual(first_run["high_count"], 1)
        self.assertEqual(first_run["medium_count"], 1)
        self.assertEqual(first_run["critical_count"], 0)

        second_run = summary[1]
        self.assertEqual(second_run["findings_count"], 2)
        self.assertEqual(second_run["critical_count"], 1)
        self.assertEqual(second_run["high_count"], 1)

    def test_identifies_recurring_findings(self):
        _, _, recurring = analytics.analyze_history(
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

        summary, comparison, recurring = analytics.analyze_history(
            runs, []
        )

        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["findings_count"], 0)
        self.assertEqual(summary[0]["distinct_finding_types"], 0)
        self.assertEqual(comparison, [])
        self.assertEqual(recurring, [])

    def test_requires_two_runs_for_comparison(self):
        runs = [self.runs[0]]

        _, comparison, _ = analytics.analyze_history(
            runs, self.findings
        )

        self.assertEqual(comparison, [])

    def test_operational_metrics_calculate_overdue_days(self):
        import tempfile
        from datetime import date

        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            (data_dir / "evidence.csv").write_text(
                "evidence_id,control_id,evidence_name,status,submission_date,expiry_date\n"
                "EV002,CTRL002,Scan,Submitted,2026-07-01,2026-10-01\n"
                "EV003,CTRL003,Training,Pending,,\n"
                "EV004,CTRL004,Backup,Submitted,2026-09-15,2027-09-15\n",
                encoding="utf-8",
            )
            (data_dir / "tasks.csv").write_text(
                "task_id,control_id,task_name,owner,due_date,status\n"
                "TASK002,CTRL002,Remediate,Security,2026-10-22,In Progress\n"
                "TASK003,CTRL003,Training,HR,2026-10-20,Pending\n"
                "TASK001,CTRL001,Review,Security,2026-10-20,Completed\n",
                encoding="utf-8",
            )
            latest_findings = [
                {
                    "control_id": "CTRL005",
                    "finding_type": "MISSING_EVIDENCE",
                }
            ]

            metrics = analytics.load_operational_metrics(
                data_dir, date(2026, 10, 23), latest_findings
            )

        by_id = {row["item_id"]: row for row in metrics}
        self.assertEqual(by_id["EV002"]["days_overdue"], 22)
        self.assertEqual(by_id["TASK002"]["days_overdue"], 1)
        self.assertEqual(by_id["TASK003"]["days_overdue"], 3)
        self.assertEqual(by_id["NO_RECORD"]["issue_type"], "MISSING_EVIDENCE")
        self.assertEqual(by_id["NO_RECORD"]["remediation_status"], "NOT_TRACKED")

    def test_recurring_finding_absent_from_latest_reports_last_observed_run(self):
        runs = [
            {"run_id": 1, "executed_at": "2026-10-20T10:00:00+00:00", "controls_evaluated": 5},
            {"run_id": 2, "executed_at": "2026-10-21T10:00:00+00:00", "controls_evaluated": 5},
            {"run_id": 3, "executed_at": "2026-10-22T10:00:00+00:00", "controls_evaluated": 5},
        ]
        findings = [
            {"run_id": 1, "control_id": "CTRL009", "finding_type": "SLA_OVERDUE", "severity": "HIGH", "details": "Overdue"},
            {"run_id": 2, "control_id": "CTRL009", "finding_type": "SLA_OVERDUE", "severity": "HIGH", "details": "Overdue"},
        ]
        _, _, recurring = analytics.analyze_history(runs, findings)
        self.assertEqual(len(recurring), 1)
        self.assertEqual(recurring[0]["occurrences"], 2)
        self.assertEqual(recurring[0]["latest_run_id"], 2)
        self.assertEqual(recurring[0]["latest_severity"], "HIGH")

    def test_recurring_findings_count_distinct_runs(self):
        runs = [
            {
                "run_id": 1,
                "executed_at": "2026-10-22T10:00:00+00:00",
                "controls_evaluated": 5,
            },
            {
                "run_id": 2,
                "executed_at": "2026-10-23T10:00:00+00:00",
                "controls_evaluated": 5,
            },
        ]

        base_finding = {
            "control_id": "CTRL002",
            "finding_type": "EVIDENCE_EXPIRED",
            "severity": "HIGH",
            "details": "Evidence expired",
        }

        findings = [
            {**base_finding, "run_id": 1},
            {**base_finding, "run_id": 1},
            {**base_finding, "run_id": 2},
        ]

        _, _, recurring = analytics.analyze_history(runs, findings)

        self.assertEqual(len(recurring), 1)
        self.assertEqual(recurring[0]["occurrences"], 2)
        self.assertEqual(recurring[0]["latest_run_id"], 2)
        self.assertEqual(recurring[0]["latest_severity"], "HIGH")


if __name__ == "__main__":
    unittest.main()
