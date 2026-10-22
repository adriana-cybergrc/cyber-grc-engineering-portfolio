"""Validate and score a synthetic cybersecurity risk register.

This is an educational starter, not a calibrated enterprise risk model.
Probability and impact are ordinal values from 1 to 5; score = probability * impact.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

REQUIRED_FIELDS = {
    "risk_id", "scenario", "asset", "probability", "impact",
    "owner", "status", "treatment"
}


def risk_level(score: int) -> str:
    """Map a 1-25 score to a simple illustrative band."""
    if score >= 20:
        return "Critical"
    if score >= 12:
        return "High"
    if score >= 6:
        return "Moderate"
    return "Low"


def load_and_validate(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")
        missing = REQUIRED_FIELDS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

        records = []
        seen_ids: set[str] = set()
        for line_number, row in enumerate(reader, start=2):
            risk_id = (row.get("risk_id") or "").strip()
            if not risk_id:
                raise ValueError(f"Line {line_number}: risk_id is required.")
            if risk_id in seen_ids:
                raise ValueError(f"Line {line_number}: duplicate risk_id '{risk_id}'.")
            seen_ids.add(risk_id)

            for field in ("scenario", "asset", "owner", "status", "treatment"):
                if not (row.get(field) or "").strip():
                    raise ValueError(f"Line {line_number}: {field} is required.")

            try:
                probability = int(row["probability"])
                impact = int(row["impact"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Line {line_number}: probability and impact must be integers."
                ) from exc

            if probability not in range(1, 6):
                raise ValueError(f"Line {line_number}: probability must be between 1 and 5.")
            if impact not in range(1, 6):
                raise ValueError(f"Line {line_number}: impact must be between 1 and 5.")

            row["probability"] = str(probability)
            row["impact"] = str(impact)
            records.append(row)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Path to risk register CSV")
    args = parser.parse_args()

    try:
        records = load_and_validate(args.input)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Validated {len(records)} risk record(s).")
    print("-" * 88)
    print(f"{'ID':<8} {'Score':>5} {'Level':<10} {'Status':<14} Scenario")
    print("-" * 88)
    for record in records:
        score = int(record["probability"]) * int(record["impact"])
        print(
            f"{record['risk_id']:<8} {score:>5} {risk_level(score):<10} "
            f"{record['status']:<14} {record['scenario']}"
        )
    print("\nNote: illustrative scoring only; risk treatment and acceptance require accountable human review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
