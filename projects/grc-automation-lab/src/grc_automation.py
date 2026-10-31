

import argparse
import csv
import importlib.util

from datetime import date
from pathlib import Path


# Load audit_store.py from the same directory, including when this
# module is loaded dynamically by the existing unit tests.
AUDIT_STORE_PATH = Path(__file__).resolve().with_name("audit_store.py")

AUDIT_STORE_SPEC = importlib.util.spec_from_file_location(
    "audit_store",
    AUDIT_STORE_PATH,
)

if AUDIT_STORE_SPEC is None or AUDIT_STORE_SPEC.loader is None:
    raise ImportError(f"Cannot load audit store: {AUDIT_STORE_PATH}")

audit_store = importlib.util.module_from_spec(AUDIT_STORE_SPEC)
AUDIT_STORE_SPEC.loader.exec_module(audit_store)


def load_csv(path):
    with open(
        path,
        mode="r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def evaluate_controls(controls, evidence_records, tasks, today=None):
    """
    Evaluate active controls against evidence records and remediation tasks.

    Findings include structured source identity fields for persistent
    lifecycle tracking in SQLite.
    """

    today = today or date.today()
    findings = []

    evidence_by_control = {}

    for evidence in evidence_records:
        evidence_by_control.setdefault(
            evidence["control_id"],
            [],
        ).append(evidence)

    tasks_by_control = {}

    for task in tasks:
        tasks_by_control.setdefault(
            task["control_id"],
            [],
        ).append(task)

    def append_finding(
        control_id,
        control_name,
        finding_type,
        severity,
        details,
        source_type,
        source_record_id,
    ):
        findings.append({
            "control_id": control_id,
            "control_name": control_name,
            "finding_type": finding_type,
            "severity": severity,
            "details": details,
            "source_type": source_type,
            "source_record_id": source_record_id,
        })

    for control in controls:
        if control["active"].strip().lower() != "true":
            continue

        control_id = control["control_id"]
        control_name = control["control_name"]

        evidence_items = evidence_by_control.get(
            control_id,
            [],
        )

        # No evidence record exists for the control.
        if not evidence_items:
            append_finding(
                control_id=control_id,
                control_name=control_name,
                finding_type="MISSING_EVIDENCE",
                severity="HIGH",
                details="No evidence record exists for this control.",
                source_type="CONTROL_REQUIREMENT",
                source_record_id=control_id,
            )

        else:
            for evidence in evidence_items:
                evidence_id = evidence["evidence_id"]
                status = evidence["status"].strip().lower()

                # Evidence has not been submitted.
                if status != "submitted":
                    append_finding(
                        control_id=control_id,
                        control_name=control_name,
                        finding_type="EVIDENCE_NOT_SUBMITTED",
                        severity="HIGH",
                        details=(
                            f"Evidence {evidence_id} status "
                            f"is {evidence['status']}."
                        ),
                        source_type="EVIDENCE",
                        source_record_id=evidence_id,
                    )
                    continue

                expiry = evidence["expiry_date"].strip()

                # Evidence has no expiry date.
                if not expiry:
                    append_finding(
                        control_id=control_id,
                        control_name=control_name,
                        finding_type="EXPIRY_DATE_MISSING",
                        severity="MEDIUM",
                        details=(
                            f"Evidence {evidence_id} "
                            "has no expiry date."
                        ),
                        source_type="EVIDENCE",
                        source_record_id=evidence_id,
                    )

                # Evidence has expired.
                elif date.fromisoformat(expiry) < today:
                    append_finding(
                        control_id=control_id,
                        control_name=control_name,
                        finding_type="EVIDENCE_EXPIRED",
                        severity="HIGH",
                        details=(
                            f"Evidence {evidence_id} "
                            f"expired on {expiry}."
                        ),
                        source_type="EVIDENCE",
                        source_record_id=evidence_id,
                    )

        # Evaluate overdue tasks independently of evidence findings.
        for task in tasks_by_control.get(control_id, []):
            if task["status"].strip().lower() == "completed":
                continue

            due_date = date.fromisoformat(task["due_date"])

            if due_date < today:
                task_id = task["task_id"]

                append_finding(
                    control_id=control_id,
                    control_name=control_name,
                    finding_type="SLA_OVERDUE",
                    severity="HIGH",
                    details=(
                        f"Task {task_id} is {task['status']} "
                        f"and was due on {task['due_date']}."
                    ),
                    source_type="TASK",
                    source_record_id=task_id,
                )

    return findings


def export_findings_csv(findings, output_path):
    """
    Export findings using the original five-column CSV contract.

    Structured lifecycle identity fields remain available in the
    finding dictionaries and SQLite, but are intentionally excluded
    from the existing CSV report.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "control_id",
        "control_name",
        "finding_type",
        "severity",
        "details",
    ]

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=columns,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(findings)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="GRC control, evidence and SLA automation"
    )

    parser.add_argument(
        "--data-dir",
        default="projects/grc-automation-lab/data",
    )

    parser.add_argument(
        "--output",
        default="projects/grc-automation-lab/grc_findings.csv",
    )

    parser.add_argument(
        "--database",
        default="projects/grc-automation-lab/runtime/grc_audit.db",
        help="SQLite database path for persistent audit history",
    )

    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    database_path = Path(args.database)

    # Load input datasets.
    controls = load_csv(data_dir / "controls.csv")
    evidence = load_csv(data_dir / "evidence.csv")
    tasks = load_csv(data_dir / "tasks.csv")

    # Evaluate controls and generate structured findings.
    findings = evaluate_controls(
        controls=controls,
        evidence_records=evidence,
        tasks=tasks,
    )

    # Count only active controls.
    controls_evaluated = sum(
        1
        for control in controls
        if control["active"].strip().lower() == "true"
    )

    # Export the original CSV format.
    output_path = export_findings_csv(
        findings=findings,
        output_path=args.output,
    )

    # Persist the audit execution and lifecycle records.
    run_id = audit_store.save_audit_run(
        database_path,
        controls_evaluated,
        findings,
    )

    print(f"Controls evaluated: {controls_evaluated}")
    print(f"Findings generated: {len(findings)}")
    print(f"Report saved to: {output_path}")
    print(f"Audit database: {database_path}")
    print(f"Audit run ID: {run_id}")


if __name__ == "__main__":
    main()
