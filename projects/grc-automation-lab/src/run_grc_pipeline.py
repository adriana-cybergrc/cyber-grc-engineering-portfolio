
"""Run the complete synthetic GRC audit and reporting pipeline."""

import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
REPOSITORY_ROOT = PROJECT_DIR.parent.parent

PIPELINE_STEPS = [
    (
        "GRC control evaluation",
        PROJECT_DIR / "src" / "grc_automation.py",
    ),
    (
        "Historical analytics",
        PROJECT_DIR / "src" / "grc_analytics.py",
    ),
    (
        "Executive dashboard",
        PROJECT_DIR / "src" / "grc_dashboard.py",
    ),
]


def main() -> int:
    print("=" * 60)
    print("GRC AUTOMATION PIPELINE")
    print("=" * 60)

    for step_name, script_path in PIPELINE_STEPS:
        print(f"\n[START] {step_name}")

        if not script_path.is_file():
            print(f"[ERROR] Script not found: {script_path}")
            return 1

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=REPOSITORY_ROOT,
            check=False,
        )

        if result.returncode != 0:
            print(
                f"\n[FAILED] {step_name}. "
                "Pipeline stopped; later steps were not executed."
            )
            return result.returncode or 1

        print(f"[SUCCESS] {step_name}")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(
        "Dashboard: projects/grc-automation-lab/"
        "runtime/analytics/grc_executive_dashboard.html"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
