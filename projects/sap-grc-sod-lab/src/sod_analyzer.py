import argparse
import csv
from pathlib import Path


def load_csv(path):
    with open(path, mode="r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def analyze_sod(users, rules):
    findings = []

    functions_by_user = {}
    for row in users:
        functions_by_user.setdefault(row["user_id"], set()).add(
            row["business_function"]
        )

    for rule in rules:
        function_a = rule["function_a"]
        function_b = rule["function_b"]

        for user_id, functions in functions_by_user.items():
            if function_a in functions and function_b in functions:
                findings.append({
                    "user_id": user_id,
                    "rule_id": rule["rule_id"],
                    "rule_name": rule["rule_name"],
                    "risk_level": rule["risk_level"],
                    "function_a": function_a,
                    "function_b": function_b,
                    "status": "REQUIRES_REVIEW",
                })

    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Synthetic SAP GRC SoD conflict analyzer"
    )
    parser.add_argument("--users", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    users = load_csv(args.users)
    rules = load_csv(args.rules)
    findings = analyze_sod(users, rules)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "user_id", "rule_id", "rule_name", "risk_level",
        "function_a", "function_b", "status"
    ]

    with open(output_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(findings)

    print(f"Analysis complete. Findings: {len(findings)}")
    print(f"Report saved to: {output_path}")


if __name__ == "__main__":
    main()
