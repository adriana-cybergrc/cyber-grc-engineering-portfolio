# Cyber GRC Engineering — Dashboards

This directory contains dashboard demonstrations for cybersecurity governance, risk oversight, and vulnerability management.

## Available Dashboards

### 1. Vulnerability Management — VulnOps

**Path:** `vulnerability-management/vulnerability_executive_dashboard.html`

An interactive, standalone dashboard for vulnerability management oversight.

Features include:
- KPIs for open vulnerabilities, critical findings, overdue SLAs, SLA compliance, and fixed items.
- Filtering by country, severity, remediation status, owner, and deadline.
- Visual analysis of severity, country distribution, remediation responsibility, and operational status.
- Searchable vulnerability inventory.
- CSV import and filtered CSV export.
- Print-friendly reporting.

[Open the Vulnerability Management Dashboard](vulnerability-management/vulnerability_executive_dashboard.html)

See the [Vulnerability Management README](vulnerability-management/README.md) for usage instructions, limitations, and governance considerations.

### 2. Executive GRC Dashboard

**Path:**### 2. Executive GRC Dashboard

**Access the [Executive GRC Dashboard](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html).**

An executive dashboard for monitoring Governance, Risk, and Compliance (GRC) indicators, with a focus on management visibility, traceability, and informed decision-making.

**Key Features**

- Consolidation of evaluated controls and reported findings.
- Analysis of recurring findings and severity distribution.
- Monitoring of evidence issues and overdue remediation tasks.
- Tracking of formal remediation validation status.
- Execution history and comparison of analytical results.

**Architecture and Data Updates**

The dashboard is delivered as a standalone HTML file. Analytical processing is performed by `src/grc_dashboard.py`, using CSV files as input sources. The displayed information depends on the available input data and the analytical execution used to generate the published version.

**Limitations and Governance Controls**

This demonstration uses synthetic data. Operational indicators must not be interpreted as formally validated remediation records unless supporting evidence, verification results, and traceable records are available. The dashboard supports monitoring and management analysis but does not replace a controlled remediation workflow or formal audit mechanisms.
## Governance and Security

These dashboards support monitoring and decision-making; they do not replace a vulnerability management platform, formal risk acceptance, or a controlled remediation workflow.

A production implementation should establish:
- Risk-based remediation SLAs and escalation criteria.
- Accountable remediation owners.
- Evidence retention and independent validation of remediation.
- Data quality checks, traceability, and audit logging.
- Appropriate access controls and protection of confidential information.

No direct Tenable API integration is implemented in the vulnerability dashboard. Do not publish credentials, internal hostnames, IP addresses, exploitable vulnerability details, or confidential organizational data.

Use sanitized datasets in public portfolio demonstrations.
