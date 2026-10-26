# GRC Automation Lab

**Cyber GRC Engineering | Vulnerability Management | Security Metrics | Workflow Automation**

## Overview

This lab explores how cybersecurity governance and engineering practices can improve risk visibility, vulnerability remediation oversight, security metrics, and executive decision-making.

The lab brings together executive reporting prototypes and practical approaches to governance, risk management, control monitoring, and workflow automation. The current implementations are designed to demonstrate measurable outcomes, transparent assumptions, and a path toward more auditable security processes.

## Live Demonstrations

### 1. GRC Executive Dashboard

[Open the GRC Executive Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html)

An executive reporting prototype focused on GRC visibility and management-level indicators.

### 2. Vulnerability Management Executive Dashboard

[Open the Vulnerability Management Executive Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)

A browser-based prototype that transforms imported vulnerability records into management indicators and filtered operational views.

The dashboards are published through GitHub Pages. Use synthetic data for public demonstrations; do not upload confidential or production vulnerability records.

## Current Capabilities

### Vulnerability Management Dashboard

- Import vulnerability records from CSV files.
- Display executive indicators for open vulnerabilities, critical findings, overdue SLAs, SLA compliance, and remediated findings.
- Filter records by country, severity, status, responsible party, and SLA status.
- Search vulnerability records and inspect detailed entries.
- Export data and generate print-friendly reports.
- Present summarized indicators to support management discussions.

Displayed results depend on the imported records and the dashboard's implemented calculation rules.

### GRC Executive Dashboard

The GRC dashboard is a separate executive reporting prototype. Its specific indicators and functionality should be assessed against the published implementation rather than inferred from the vulnerability dashboard.

## Reference Workflow

The following workflow represents the intended operational context for vulnerability management. Only the CSV-based dashboard functionality is currently implemented.

1. **Vulnerability discovery:** Scanning and discovery are performed by the organization's vulnerability management process or an authorized service provider.
2. **Data collection:** Vulnerability records are exported to a CSV file.
3. **Data analysis:** The dashboard processes imported records in the browser.
4. **Prioritization:** Findings are reviewed according to severity, remediation status, SLA exposure, and ownership information available in the dataset.
5. **Management reporting:** Filtered records and summary indicators support operational and executive review.
6. **Remediation verification:** Remediation evidence and validation results must be confirmed through an authoritative process.

## Technical Architecture

| Component | Current implementation |
|---|---|
| User interface | HTML |
| Browser-side processing | JavaScript |
| Vulnerability dashboard input | CSV |
| Reporting | Dashboard indicators, tables, export, and print |
| Hosting | GitHub Pages |
| Direct vulnerability platform API integration | Not implemented |
| Persistent remediation audit trail | Not yet implemented |
| Centralized multi-user remediation register | Not yet implemented |

The vulnerability dashboard operates on imported files. It does not directly retrieve scan results from Tenable or other vulnerability management platforms, and it does not replace the source system or the formal remediation workflow.

## Governance and SLA Considerations

An effective vulnerability management process should define:

- Remediation targets by severity and business risk.
- Explicit ownership for internal teams and service providers.
- Due dates, aging, overdue status, and escalation criteria.
- Exceptions, dependencies, and approved remediation plans.
- Evidence of corrective action and independent validation where required.
- Management reporting that distinguishes remediation progress from verified closure.

Critical and high-severity vulnerabilities may be subject to a 48-hour remediation target where that target is formally established by organizational policy. The dashboard's actual SLA calculations and source-data requirements must be verified before operational use.

## Validation and Test Scenarios

The vulnerability dashboard prototype has been exercised with synthetic CSV scenarios covering:

- Standard English-language headers and records.
- Portuguese-language data and semicolon-delimited files.
- Edge cases and variations in input records.
- CSV import, filtering, indicator updates, export, and print functionality.

These checks represent prototype validation, not comprehensive software assurance. Automated regression testing, malformed-input coverage, browser compatibility testing, and formal acceptance criteria remain areas for further development.

## Current Limitations

- No direct Tenable API connection or automated scan ingestion.
- No scheduled synchronization with a source vulnerability management platform.
- No persistent remediation register with controlled state transitions.
- No formal approval workflow for risk exceptions.
- No independently verified remediation evidence stored by the vulnerability dashboard.
- No claim of comprehensive automated test coverage.
- No claim of production readiness or centralized multi-user operation.

The vulnerability dashboard is a reporting prototype, not a production vulnerability management system.

## Target Evolution

The next engineering iterations should prioritize:

1. **Data quality:** Validate required CSV fields, date formats, status values, and duplicate records.
2. **Remediation traceability:** Record the finding identifier, accountable owner, corrective action, due date, supporting evidence, and validation result.
3. **Audit history:** Preserve timestamps, state transitions, and the identity of the person making each change.
4. **SLA governance:** Document calculation rules, exception handling, escalation thresholds, and approved policy mappings.
5. **Automated testing:** Establish reproducible test cases for calculations, filters, imports, exports, and edge conditions.
6. **Workflow integration:** Evaluate approved integration mechanisms only when access, security requirements, and source-system ownership permit.
7. **Executive reporting:** Refine metrics to distinguish exposure, remediation performance, overdue obligations, and verified closure.
8. **Persistence and recovery:** Evaluate browser-based persistence for the initial prototype and a backend/database architecture for future centralized, multi-user operation.

## Security and Responsible Use

This project is an independent educational portfolio. It uses synthetic demonstration data and is not affiliated with or endorsed by any employer, vendor, or standards organization.

Validate data quality, calculation logic, security requirements, and governance controls before adapting any component to a real operational environment.