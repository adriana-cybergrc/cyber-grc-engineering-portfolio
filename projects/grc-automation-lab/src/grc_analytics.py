import argparse
import csv
import sqlite3
from collections import Counter
from pathlib import Path


def load_history(db_path):
    with sqlite3.connect(db_path) as connection:
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

    recurring_counts = Counter(
        finding_signature(item) for item in findings
    )
    latest_run_id = runs[-1]["run_id"] if runs else None

    recurring = []
    for signature, count in recurring_counts.most_common():
        if count < 2:
            continue

        control_id, finding_type = signature
        matching = [
            item for item in findings
            if finding_signature(item) == signature
        ]
        recurring.append({
            "control_id": control_id,
            "finding_type": finding_type,
            "occurrences": count,
            "latest_run_id": latest_run_id,
            "latest_severity": next(
                (
                    item["severity"]
                    for item in reversed(matching)
                    if item["run_id"] == latest_run_id
                ),
                "",
            ),
        })

    return summary, latest_comparison, recurring


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
    args = parser.parse_args()

    db_path = Path(args.database)
    output_dir = Path(args.output_dir)

    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    runs, findings = load_history(db_path)
    summary, comparison, recurring = analyze_history(runs, findings)

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
