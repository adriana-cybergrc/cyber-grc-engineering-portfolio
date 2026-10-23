
"""Generate a local executive dashboard from GRC analytics CSV files."""

import argparse
import csv
import html
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ANALYTICS_DIR = PROJECT_ROOT / "runtime" / "analytics"


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV file and return its rows."""
    if not path.exists():
        raise FileNotFoundError(f"Required analytics file not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def safe(value: object) -> str:
    """Escape values before inserting them into HTML."""
    return html.escape(str(value if value is not None else ""))


def number(row: dict[str, str], key: str) -> int:
    """Read a numeric CSV field safely."""
    try:
        return int(row.get(key, "0") or "0")
    except (TypeError, ValueError):
        return 0


def make_table(
    headers: list[str],
    rows: list[list[object]],
    empty_message: str,
) -> str:
    """Build an HTML table with escaped values."""
    header_html = "".join(f"<th>{safe(item)}</th>" for item in headers)

    if not rows:
        body_html = (
            f'<tr><td colspan="{len(headers)}">'
            f"{safe(empty_message)}</td></tr>"
        )
    else:
        body_html = "".join(
            "<tr>"
            + "".join(f"<td>{safe(value)}</td>" for value in row)
            + "</tr>"
            for row in rows
        )

    return (
        '<div class="table-wrap"><table><thead><tr>'
        f"{header_html}</tr></thead><tbody>{body_html}</tbody></table></div>"
    )


def severity_bars(run: dict[str, str]) -> str:
    """Render severity distribution for the latest execution."""
    severities = [
        ("Critical", number(run, "critical_count")),
        ("High", number(run, "high_count")),
        ("Medium", number(run, "medium_count")),
        ("Low", number(run, "low_count")),
    ]
    maximum = max((value for _, value in severities), default=0)
    maximum = max(maximum, 1)

    bars = []
    for label, value in severities:
        width = value / maximum * 100
        bars.append(
            '<div class="bar-row">'
            f'<span class="bar-label">{safe(label)}</span>'
            '<div class="bar-track"><div class="bar-fill" '
            f'style="width:{width:.1f}%"></div></div>'
            f'<strong>{value}</strong></div>'
        )
    return "\n".join(bars)


def build_dashboard(analytics_dir: Path) -> Path:
    """Build the executive dashboard HTML file."""
    runs = read_csv(analytics_dir / "execution_summary.csv")
    comparisons = read_csv(analytics_dir / "latest_comparison.csv")
    recurring = read_csv(analytics_dir / "recurring_findings.csv")

    runs.sort(key=lambda row: number(row, "run_id"))
    latest = runs[-1] if runs else {
        "run_id": "N/A",
        "executed_at": "N/A",
        "controls_evaluated": "0",
        "findings_count": "0",
        "critical_count": "0",
        "high_count": "0",
        "medium_count": "0",
        "low_count": "0",
        "distinct_finding_types": "0",
    }

    run_history = [
        [
            row.get("run_id", ""),
            row.get("executed_at", ""),
            row.get("controls_evaluated", ""),
            row.get("findings_count", ""),
            row.get("critical_count", ""),
            row.get("high_count", ""),
            row.get("medium_count", ""),
            row.get("low_count", ""),
        ]
        for row in reversed(runs)
    ]

    comparison_rows = [
        [
            row.get("comparison", ""),
            row.get("status", ""),
            row.get("control_id", ""),
            row.get("finding_type", ""),
            row.get("severity", ""),
            row.get("details", ""),
        ]
        for row in comparisons
    ]

    recurring_rows = [
        [
            row.get("control_id", ""),
            row.get("finding_type", ""),
            row.get("occurrences", ""),
            row.get("latest_run_id", ""),
            row.get("latest_severity", ""),
        ]
        for row in sorted(
            recurring,
            key=lambda item: number(item, "occurrences"),
            reverse=True,
        )
    ]

    status_counts: dict[str, int] = {}
    for row in comparisons:
        status = row.get("status", "UNKNOWN")
        status_counts[status] = status_counts.get(status, 0) + 1

    recurring_count = status_counts.get("RECURRING", 0)
    new_count = status_counts.get("NEW", 0)
    not_present_count = status_counts.get("NOT_PRESENT_IN_LATEST", 0)

    generated_at = __import__("datetime").datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Executive GRC Dashboard</title>
<style>
:root {{
  color-scheme: light;
  font-family: "Segoe UI", Arial, sans-serif;
  color: #182230;
  background: #f3f5f8;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; }}
header {{ background: #172b4d; color: white; padding: 28px 5%; }}
header h1 {{ margin: 0 0 8px; font-size: 28px; }}
header p {{ margin: 4px 0; color: #dbe5f3; }}
main {{ max-width: 1400px; margin: auto; padding: 24px; }}
h2 {{ font-size: 19px; margin: 0 0 16px; }}
section {{ margin-bottom: 26px; }}
.kpis {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));
         gap: 14px; }}
.card, .panel {{ background: white; border: 1px solid #dfe5ed;
                 border-radius: 10px; padding: 18px; }}
.kpi-label {{ color: #596579; font-size: 13px; }}
.kpi-value {{ font-size: 30px; font-weight: 700; margin-top: 8px; }}
.kpi-note {{ color: #68778b; font-size: 12px; margin-top: 6px; }}
.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
.bar-row {{ display: grid; grid-template-columns: 75px 1fr 28px;
            gap: 10px; align-items: center; margin: 15px 0; }}
.bar-label {{ font-size: 13px; }}
.bar-track {{ height: 12px; background: #e8edf3; border-radius: 8px;
              overflow: hidden; }}
.bar-fill {{ height: 100%; background: #4169a1; border-radius: 8px; }}
.table-wrap {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th, td {{ padding: 10px; border-bottom: 1px solid #e6eaf0;
          text-align: left; vertical-align: top; }}
th {{ background: #f6f8fb; white-space: nowrap; }}
td {{ overflow-wrap: anywhere; }}
.note {{ border-left: 4px solid #c18a28; background: #fff8e8;
         padding: 14px; line-height: 1.5; }}
footer {{ color: #68778b; font-size: 12px; padding: 12px 0 28px; }}
@media (max-width: 800px) {{
  .kpis {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .two-col {{ grid-template-columns: 1fr; }}
  main {{ padding: 14px; }}
}}
@media (max-width: 420px) {{
  .kpis {{ grid-template-columns: 1fr 1fr; }}
  .kpi-value {{ font-size: 24px; }}
}}
</style>
</head>
<body>
<header>
  <h1>Executive GRC Dashboard</h1>
  <p>Cybersecurity controls, evidence and remediation oversight</p>
  <p>Latest execution: #{safe(latest["run_id"])} ·
     {safe(latest["executed_at"])}</p>
</header>
<main>
<section class="kpis">
  <div class="card"><div class="kpi-label">Controls evaluated</div>
    <div class="kpi-value">{number(latest, "controls_evaluated")}</div>
    <div class="kpi-note">Latest execution</div></div>
  <div class="card"><div class="kpi-label">Open findings in report</div>
    <div class="kpi-value">{number(latest, "findings_count")}</div>
    <div class="kpi-note">Latest execution</div></div>
  <div class="card"><div class="kpi-label">Recurring findings</div>
    <div class="kpi-value">{recurring_count}</div>
    <div class="kpi-note">In the latest run comparison</div></div>
  <div class="card"><div class="kpi-label">Distinct finding types</div>
    <div class="kpi-value">{number(latest, "distinct_finding_types")}</div>
    <div class="kpi-note">Latest execution</div></div>
</section>

<section class="two-col">
  <div class="panel">
    <h2>Severity distribution — latest execution</h2>
    {severity_bars(latest)}
  </div>
  <div class="panel">
    <h2>Latest comparison status</h2>
    <p><strong>Recurring:</strong> {recurring_count}</p>
    <p><strong>New:</strong> {new_count}</p>
    <p><strong>Not present in latest:</strong> {not_present_count}</p>
    <p class="kpi-note">Comparison statuses are based on the analytics CSV.</p>
  </div>
</section>

<section class="panel">
  <h2>Historical execution summary</h2>
  {make_table(
      ["Run ID", "Executed at", "Controls", "Findings",
       "Critical", "High", "Medium", "Low"],
      run_history,
      "No execution history available."
  )}
</section>

<section class="panel">
  <h2>Recurring findings by control</h2>
  {make_table(
      ["Control", "Finding type", "Occurrences",
       "Latest run", "Severity"],
      recurring_rows,
      "No recurring findings recorded."
  )}
</section>

<section class="panel">
  <h2>Latest run comparison details</h2>
  {make_table(
      ["Comparison", "Status", "Control", "Finding type",
       "Severity", "Details"],
      comparison_rows,
      "No comparison records available."
  )}
</section>

<section class="note">
  <strong>Governance interpretation:</strong>
  A finding marked NOT_PRESENT_IN_LATEST is not proof of remediation.
  Closure requires evidence of corrective action and validation against
  the relevant control. This dashboard summarizes recorded findings;
  it does not independently validate remediation or calculate residual risk.
</section>

<footer>
  Generated locally: {safe(generated_at)} ·
  Source: GRC analytics CSV files · Synthetic portfolio data
</footer>
</main>
</body>
</html>
"""

    output_path = analytics_dir / "grc_executive_dashboard.html"
    output_path.write_text(html_document, encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a local executive GRC dashboard."
    )
    parser.add_argument(
        "--analytics-dir",
        type=Path,
        default=DEFAULT_ANALYTICS_DIR,
        help="Directory containing the analytics CSV files.",
    )
    args = parser.parse_args()

    output_path = build_dashboard(args.analytics_dir)
    print("Executive dashboard generated.")
    print(f"Dashboard: {output_path}")


if __name__ == "__main__":
    main()
