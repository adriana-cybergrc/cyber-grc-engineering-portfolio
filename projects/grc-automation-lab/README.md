# GRC Automation Lab

**Cyber GRC Engineering | Vulnerability Management | Security Metrics | Workflow Automation**

## Overview

This lab explores how cybersecurity governance and engineering practices can improve vulnerability visibility, remediation oversight, and executive decision-making.

The current implementation includes a browser-based executive dashboard prototype that transforms imported vulnerability records into management indicators and filtered operational views.

The project focuses on measurable outcomes, transparent assumptions, and the evolution toward auditable remediation processes.

## Live Demonstration

**[Open the Vulnerability Management Executive Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)**

The dashboard is published through GitHub Pages and uses synthetic data for demonstration.

## Current Capabilities

- Import vulnerability records from CSV files.
- Display executive indicators for open vulnerabilities, critical findings, overdue SLAs, SLA compliance, and remediated findings.
- Filter records by country, severity, status, responsible party, and SLA status.
- Search vulnerability records and inspect detailed entries.
- Export data and generate print-friendly reports.
- Present summarized indicators to support management discussions.

The displayed results depend on the records imported and the dashboard's implemented calculation rules.

## Reference Workflow

The following workflow represents the intended operational context. Only the CSV-based dashboard functionality is currently implemented.

1. **Vulnerability discovery:** scanning and discovery are performed by the organization's vulnerability management process or an authorized service provider.
2. **Data collection:** vulnerability records are exported to a CSV file.
3. **Data analysis:** the dashboard processes the imported records in the browser.
4. **Prioritization:** findings are reviewed according to severity, remediation status, SLA exposure, and ownership information available in the dataset.
5. **Management reporting:** filtered records and summary indicators support operational and executive review.
6. **Remediation verification:** remediation evidence and validation results should be confirmed through an authoritative process.

## Technical Architecture

| Component | Current implementation |
|---|---|
| User interface | HTML |
| Browser-side processing | JavaScript |
| Input format | CSV |
| Reporting | Dashboard indicators, tables, export, and print |
| Hosting | GitHub Pages |
| Vulnerability platform integration | No direct API integration |
| Persistent remediation audit trail | Not yet implemented |

The prototype operates on imported files. It does not directly retrieve scan results from Tenable or other vulnerability management platforms, and it does not replace the source system or the formal remediation workflow.

## Governance and SLA Considerations

An effective vulnerability management process should define:

- Remediation targets by severity and business risk.
- Explicit ownership for internal teams and service providers.
- Due dates, aging, overdue status, and escalation criteria.
- Exceptions, dependencies, and approved remediation plans.
- Evidence of corrective action and independent validation where required.
- Management reporting that distinguishes remediation progress from verified closure.

Critical and high-severity vulnerabilities may be subject to a 48-hour remediation target where that target is formally established by organizational policy. The dashboard's actual SLA calculations and source-data requirements must be verified before relying on it for operational reporting.

## Validation and Test Scenarios

The prototype has been exercised with synthetic CSV scenarios covering:

- Standard English-language headers and records.
- Portuguese-language data and semicolon-delimited files.
- Edge cases and variations in input records.
- CSV import, filtering, indicator updates, export, and print functionality.

These checks represent prototype validation, not comprehensive software assurance. Automated regression testing, malformed-input coverage, browser compatibility testing, and formal acceptance criteria remain areas for further development.

No production or confidential vulnerability data should be used in public demonstrations.

## Current Limitations

- No direct Tenable API connection or automated scan ingestion.
- No scheduled synchronization with a source vulnerability management platform.
- No persistent remediation register with controlled state transitions.
- No formal approval workflow for risk exceptions.
- No independently verified evidence of remediation stored by the dashboard.
- No claim of comprehensive automated test coverage.

The dashboard is a reporting prototype, not a production vulnerability management system.

## Target Evolution

The next engineering iterations should prioritize:

1. **Data quality:** validate required CSV fields, date formats, status values, and duplicate records.
2. **Remediation traceability:** record the finding identifier, accountable owner, corrective action, due date, supporting evidence, and validation result.
3. **Audit history:** preserve timestamps, state transitions, and the identity of the person making each change.
4. **SLA governance:** document calculation rules, exception handling, escalation thresholds, and approved policy mappings.
5. **Automated testing:** establish reproducible test cases for calculations, filters, imports, exports, and edge conditions.
6. **Workflow integration:** evaluate approved integration mechanisms only when access, security requirements, and source-system ownership permit.
7. **Executive reporting:** refine metrics to distinguish exposure, remediation performance, overdue obligations, and verified closure.

## Security and Responsible Use

This project is an independent educational portfolio. It uses synthetic demonstration data and is not affiliated with or endorsed by any employer, vendor, or standards organization.

Validate data quality, calculation logic, security requirements, and governance controls before adapting any component to a real operational environment.
