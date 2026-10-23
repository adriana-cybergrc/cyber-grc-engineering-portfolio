
import argparse
import csv
import importlib.util
from datetime import date
from pathlib import Path


# Load audit_store.py from the same directory, including when this
# module is loaded dynamically by the existing unit tests.
AUDIT_STORE_PATH = Path(__file__).resolve().with_name("audit_store.py")
AUDIT_STORE_SPEC = importlib.util.spec_from_file_location(
    "audit_store", AUDIT_STORE_PATH
)

if AUDIT_STORE_SPEC is None or AUDIT_STORE_SPEC.loader is None:
    raise ImportError(f"Cannot load audit store: {AUDIT_STORE_PATH}")

audit_store = importlib.util.module_from_spec(AUDIT_STORE_SPEC)
AUDIT_STORE_SPEC.loader.exec_module(audit_store)


def load_csv(path):
    with open(path, mode="r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def evaluate_controls(controls, evidence_records, tasks, today=None):
    today = today or date.today()
    findings = []

    evidence_by_control = {}
    for evidence in evidence_records:
        evidence_by_control.setdefault(
            evidence["control_id"], []
        ).append(evidence)

    tasks_by_control = {}
    for task in tasks:
        tasks_by_control.setdefault(
            task["control_id"], []
        ).append(task)

    for control in controls:
        if control["active"].strip().lower() != "true":
            continue

        control_id = control["control_id"]
        evidence_items = evidence_by_control.get(control_id, [])

        if not evidence_items:
            findings.append({
                "control_id": control_id,
                "control_name": control["control_name"],
                "finding_type": "MISSING_EVIDENCE",
                "severity": "HIGH",
                "details": "No evidence record exists for this control.",
            })
        else:
            for evidence in evidence_items:
                status = evidence["status"].strip().lower()

                if status != "submitted":
                    findings.append({
                        "control_id": control_id,
                        "control_name": control["control_name"],
                        "finding_type": "EVIDENCE_NOT_SUBMITTED",
                        "severity": "HIGH",
                        "details": (
                            f"Evidence {evidence['evidence_id']} status "
                            f"is {evidence['status']}."
                        ),
                    })
                    continue

                expiry = evidence["expiry_date"].strip()
                if not expiry:
                    findings.append({
                        "control_id": control_id,
                        "control_name": control["control_name"],
                        "finding_type": "EXPIRY_DATE_MISSING",
                        "severity": "MEDIUM",
                        "details": (
                            f"Evidence {evidence['evidence_id']} "
                            "has no expiry date."
                        ),
                    })
                elif date.fromisoformat(expiry) < today:
                    findings.append({
                        "control_id": control_id,
                        "control_name": control["control_name"],
                        "finding_type": "EVIDENCE_EXPIRED",
                        "severity": "HIGH",
                        "details": (
                            f"Evidence {evidence['evidence_id']} "
                            f"expired on {expiry}."
                        ),
                    })

        for task in tasks_by_control.get(control_id, []):
            if task["status"].strip().lower() == "completed":
                continue

            due_date = date.fromisoformat(task["due_date"])
            if due_date < today:
                findings.append({
                    "control_id": control_id,
                    "control_name": control["control_name"],
                    "finding_type": "SLA_OVERDUE",
                    "severity": "HIGH",
                    "details": (
                        f"Task {task['task_id']} is {task['status']} "
                        f"and was due on {task['due_date']}."
                    ),
                })

    return findings


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

    controls = load_csv(data_dir / "controls.csv")
    evidence = load_csv(data_dir / "evidence.csv")
    tasks = load_csv(data_dir / "tasks.csv")

    findings = evaluate_controls(controls, evidence, tasks)

    # Count only active controls, which are the controls actually evaluated.
    controls_evaluated = sum(
        1
        for control in controls
        if control["active"].strip().lower() == "true"
    )

    # Preserve the existing CSV schema and output behavior.
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "control_id",
        "control_name",
        "finding_type",
        "severity",
        "details",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(findings)

    # Persist this execution and its findings in SQLite.
    # audit_store creates the database and its tables if needed.
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
