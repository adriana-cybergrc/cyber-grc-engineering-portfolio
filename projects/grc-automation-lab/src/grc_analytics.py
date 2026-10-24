import argparse
import csv
from contextlib import closing
import sqlite3
import sys
from datetime import date, datetime
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from remediation_store import load_remediations


def load_history(db_path):
    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row

        runs = [
            dict(row)
            for row in connection.execute("""
                SELECT run_id, executed_at, controls_evaluated,
                       findings_count
                FROM audit_runs
                ORDER BY run_id
            """).fetchall()
        ]

        findings = [
            dict(row)
            for row in connection.execute("""
                SELECT run_id, control_id, finding_type, severity, details
                FROM audit_findings
                ORDER BY run_id, control_id, finding_type
            """).fetchall()
        ]

    return runs, findings


def finding_signature(finding):
    # Stable comparison key; details may change between runs.
    return finding["control_id"], finding["finding_type"]



def analyze_history(runs, findings):
    findings_by_run = {run["run_id"]: [] for run in runs}

    for finding in findings:
        findings_by_run.setdefault(finding["run_id"], []).append(finding)

    summary = []
    for run in runs:
        run_findings = findings_by_run.get(run["run_id"], [])
        severities = Counter(
            item["severity"].upper() for item in run_findings
        )
        types = Counter(item["finding_type"] for item in run_findings)

        summary.append({
            "run_id": run["run_id"],
            "executed_at": run["executed_at"],
            "controls_evaluated": run["controls_evaluated"],
            "findings_count": len(run_findings),
            "critical_count": severities.get("CRITICAL", 0),
            "high_count": severities.get("HIGH", 0),
            "medium_count": severities.get("MEDIUM", 0),
            "low_count": severities.get("LOW", 0),
            "distinct_finding_types": len(types),
        })

    latest_comparison = []

    if len(runs) >= 2:
        previous_id = runs[-2]["run_id"]
        latest_id = runs[-1]["run_id"]

        previous = {
            finding_signature(item): item
            for item in findings_by_run.get(previous_id, [])
        }
        latest = {
            finding_signature(item): item
            for item in findings_by_run.get(latest_id, [])
        }

        for signature in sorted(latest.keys() - previous.keys()):
            item = latest[signature]
            latest_comparison.append({
                "comparison": f"{previous_id}->{latest_id}",
                "status": "NEW",
                "control_id": item["control_id"],
                "finding_type": item["finding_type"],
                "severity": item["severity"],
                "details": item["details"],
            })

        for signature in sorted(previous.keys() - latest.keys()):
            item = previous[signature]
            latest_comparison.append({
                "comparison": f"{previous_id}->{latest_id}",
                "status": "NOT_PRESENT_IN_LATEST",
                "control_id": item["control_id"],
                "finding_type": item["finding_type"],
                "severity": item["severity"],
                "details": item["details"],
            })

        for signature in sorted(latest.keys() & previous.keys()):
            item = latest[signature]
            latest_comparison.append({
                "comparison": f"{previous_id}->{latest_id}",
                "status": "RECURRING",
                "control_id": item["control_id"],
                "finding_type": item["finding_type"],
                "severity": item["severity"],
                "details": item["details"],
            })

    # Count each finding signature once per distinct execution.
    runs_by_signature = {}

    for finding in findings:
        signature = finding_signature(finding)
        runs_by_signature.setdefault(signature, set()).add(
            finding["run_id"]
        )

    latest_run_id = runs[-1]["run_id"] if runs else None
    recurring = []

    for signature, run_ids in sorted(
        runs_by_signature.items(),
        key=lambda entry: (-len(entry[1]), entry[0]),
    ):
        if len(run_ids) < 2:
            continue

        control_id, finding_type = signature

        latest_matches = [
            item
            for item in findings_by_run.get(latest_run_id, [])
            if finding_signature(item) == signature
        ]

        last_observed_run_id = (
            latest_matches[-1]["run_id"] if latest_matches else max(run_ids)
        )
        last_observed_matches = [
            item for item in findings_by_run.get(last_observed_run_id, [])
            if finding_signature(item) == signature
        ]
        latest_severity = (
            last_observed_matches[-1]["severity"]
            if last_observed_matches else ""
        )

        recurring.append({
            "control_id": control_id,
            "finding_type": finding_type,
            "occurrences": len(run_ids),
            "latest_run_id": last_observed_run_id,
            "latest_severity": latest_severity,
        })

    return summary, latest_comparison, recurring



def load_operational_metrics(data_dir, reference_date, findings=None, remediation_records=None):
    """Summarize synthetic evidence and task exposure at a fixed reference date."""
    metrics = []
    remediation_lookup = {
        (item["control_id"], item["finding_type"]): item
        for item in (remediation_records or [])
    }

    def status_for(control_id, finding_type):
        record = remediation_lookup.get((control_id, finding_type))
        return record.get("remediation_status", "NOT_TRACKED") if record else "NOT_TRACKED"

    evidence_path = data_dir / "evidence.csv"
    if evidence_path.exists():
        with evidence_path.open("r", encoding="utf-8-sig", newline="") as file:
            for item in csv.DictReader(file):
                status = (item.get("status") or "").strip().lower()
                expiry_text = (item.get("expiry_date") or "").strip()
                days_overdue = 0
                expired = False
                if expiry_text:
                    try:
                        expiry = date.fromisoformat(expiry_text)
                        expired = expiry < reference_date
                        days_overdue = max((reference_date - expiry).days, 0)
                    except ValueError:
                        pass
                if status != "submitted" or expired:
                    if status != "submitted":
                        issue_type = "EVIDENCE_NOT_SUBMITTED"
                    else:
                        issue_type = "EVIDENCE_EXPIRED"
                    metrics.append({
                        "item_type": "EVIDENCE",
                        "item_id": item.get("evidence_id", ""),
                        "control_id": item.get("control_id", ""),
                        "issue_type": issue_type,
                        "status": item.get("status", ""),
                        "due_date": expiry_text,
                        "days_overdue": days_overdue,
                        "owner": "",
                        "remediation_status": status_for(item.get("control_id", ""), issue_type),
                    })

    tasks_path = data_dir / "tasks.csv"
    if tasks_path.exists():
        with tasks_path.open("r", encoding="utf-8-sig", newline="") as file:
            for item in csv.DictReader(file):
                status = (item.get("status") or "").strip().lower()
                due_text = (item.get("due_date") or "").strip()
                if status == "completed" or not due_text:
                    continue
                try:
                    due = date.fromisoformat(due_text)
                except ValueError:
                    continue
                if due < reference_date:
                    metrics.append({
                        "item_type": "TASK",
                        "item_id": item.get("task_id", ""),
                        "control_id": item.get("control_id", ""),
                        "issue_type": "SLA_OVERDUE",
                        "status": item.get("status", ""),
                        "due_date": due_text,
                        "days_overdue": (reference_date - due).days,
                        "owner": item.get("owner", ""),
                        "remediation_status": status_for(item.get("control_id", ""), "SLA_OVERDUE"),
                    })

    # Include controls with a missing-evidence finding even when no evidence
    # row exists in evidence.csv; that absence is itself the exposure.
    existing_evidence_controls = {
        row.get("control_id", "")
        for row in metrics
        if row.get("item_type") == "EVIDENCE"
    }
    for finding in findings or []:
        if (
            finding.get("finding_type") == "MISSING_EVIDENCE"
            and finding.get("control_id") not in existing_evidence_controls
        ):
            metrics.append({
                "item_type": "EVIDENCE",
                "item_id": "NO_RECORD",
                "control_id": finding.get("control_id", ""),
                "issue_type": "MISSING_EVIDENCE",
                "status": "NO_RECORD",
                "due_date": "",
                "days_overdue": 0,
                "owner": "",
                "remediation_status": status_for(finding.get("control_id", ""), "MISSING_EVIDENCE"),
            })
            existing_evidence_controls.add(finding.get("control_id", ""))

    return metrics


def write_csv(path, rows, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path, runs, summary, comparison, recurring):
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# GRC Historical Analytics",
        "",
        f"Total executions: {len(runs)}",
        "",
    ]

    if not runs:
        lines.append("No audit executions found.")
    else:
        latest = summary[-1]
        lines.extend([
            "## Latest execution",
            "",
            f"- Run ID: {latest['run_id']}",
            f"- Executed at (UTC): {latest['executed_at']}",
            f"- Controls evaluated: {latest['controls_evaluated']}",
            f"- Findings: {latest['findings_count']}",
            f"- Critical: {latest['critical_count']}",
            f"- High: {latest['high_count']}",
            f"- Medium: {latest['medium_count']}",
            f"- Low: {latest['low_count']}",
            "",
            "## Execution trend",
            "",
            "| Run | Executed at (UTC) | Controls | Findings | Critical | High | Medium | Low |",
            "|---:|---|---:|---:|---:|---:|---:|---:|",
        ])

        for item in summary:
            lines.append(
                f"| {item['run_id']} | {item['executed_at']} "
                f"| {item['controls_evaluated']} | {item['findings_count']} "
                f"| {item['critical_count']} | {item['high_count']} "
                f"| {item['medium_count']} | {item['low_count']} |"
            )

        if len(summary) >= 2:
            change = (
                summary[-1]["findings_count"]
                - summary[-2]["findings_count"]
            )
            lines.extend([
                "",
                f"Change in finding count between the latest two runs: {change:+d}.",
                "This is a count comparison, not proof of remediation.",
            ])

        lines.extend(["", "## Latest run comparison", ""])
        if comparison:
            lines.extend([
                "| Status | Control | Finding type | Severity |",
                "|---|---|---|---|",
            ])
            for item in comparison:
                lines.append(
                    f"| {item['status']} | {item['control_id']} "
                    f"| {item['finding_type']} | {item['severity']} |"
                )
        else:
            lines.append(
                "At least two executions are required for comparison."
            )

        lines.extend(["", "## Recurring findings", ""])
        if recurring:
            lines.extend([
                "| Control | Finding type | Occurrences | Latest severity |",
                "|---|---|---:|---|",
            ])
            for item in recurring:
                lines.append(
                    f"| {item['control_id']} | {item['finding_type']} "
                    f"| {item['occurrences']} | {item['latest_severity']} |"
                )
        else:
            lines.append("No recurring findings identified across executions.")

        lines.extend([
            "",
            "## Interpretation note",
            "",
            "`NOT_PRESENT_IN_LATEST` means the finding signature was not "
            "observed in the latest run. It does not establish that the "
            "issue was remediated or independently verified.",
            "",
        ])

    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Historical analytics for GRC audit executions"
    )
    parser.add_argument(
        "--database",
        default="projects/grc-automation-lab/runtime/grc_audit.db",
    )
    parser.add_argument(
        "--output-dir",
        default="projects/grc-automation-lab/runtime/analytics",
    )
    parser.add_argument(
        "--data-dir",
        default="projects/grc-automation-lab/data",
        help="Directory containing operational evidence and task CSV files",
    )
    args = parser.parse_args()

    db_path = Path(args.database)
    output_dir = Path(args.output_dir)
    data_dir = Path(args.data_dir)

    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    runs, findings = load_history(db_path)
    summary, comparison, recurring = analyze_history(runs, findings)

    reference_date = date.today()
    if runs:
        try:
            reference_date = datetime.fromisoformat(
                runs[-1]["executed_at"].replace("Z", "+00:00")
            ).date()
        except (ValueError, TypeError):
            pass

    project_dir = Path(__file__).resolve().parents[1]
    latest_run_id = runs[-1]["run_id"] if runs else None
    latest_findings = [
        item for item in findings if item.get("run_id") == latest_run_id
    ]
    remediation_records = load_remediations(db_path)
    operational_metrics = load_operational_metrics(
        data_dir,
        reference_date,
        latest_findings,
        remediation_records,
    )

    write_csv(
        output_dir / "remediation_register.csv",
        remediation_records,
        ["control_id", "finding_type", "owner", "corrective_action",
         "evidence_reference", "validated_at", "verification_result",
         "remediation_status", "updated_at"],
    )

    write_csv(
        output_dir / "operational_metrics.csv",
        operational_metrics,
        [
            "item_type", "item_id", "control_id", "issue_type", "status",
            "due_date", "days_overdue", "owner", "remediation_status",
        ],
    )

    write_csv(
        output_dir / "execution_summary.csv",
        summary,
        [
            "run_id", "executed_at", "controls_evaluated",
            "findings_count", "critical_count", "high_count",
            "medium_count", "low_count", "distinct_finding_types",
        ],
    )
    write_csv(
        output_dir / "latest_comparison.csv",
        comparison,
        [
            "comparison", "status", "control_id", "finding_type",
            "severity", "details",
        ],
    )
    write_csv(
        output_dir / "recurring_findings.csv",
        recurring,
        [
            "control_id", "finding_type", "occurrences",
            "latest_run_id", "latest_severity",
        ],
    )

    report_path = output_dir / "grc_analytics_report.md"
    write_markdown(
        report_path, runs, summary, comparison, recurring
    )

    print(f"Executions analyzed: {len(runs)}")
    print(f"Findings analyzed: {len(findings)}")
    print(f"Analytics directory: {output_dir}")
    print(f"Executive report: {report_path}")


if __name__ == "__main__":
    main()
