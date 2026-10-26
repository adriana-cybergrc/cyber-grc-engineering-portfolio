# Cyber GRC Engineering Portfolio

**Cyber GRC | SAP Security | SAP GRC | Vulnerability Management | AI Governance**

An independent portfolio of cybersecurity governance projects, risk assessment methods, reference architectures, and automation prototypes. The portfolio demonstrates how governance, risk, compliance, and engineering practices can support measurable, auditable, and business-aligned security outcomes.

## Featured Projects

| Project | Focus | Status |
|---|---|---|
| [Vulnerability Management Executive Dashboard](projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html) · [Live Demo](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html) | Executive KPIs, remediation SLAs, risk visibility, CSV analysis | **Published prototype** |
| [Cyber GRC Risk Register](projects/cyber-grc-risk-register/README.md) | Risk scenarios, scoring, and CSV validation | Starter |
| [GRC Automation Lab](projects/grc-automation-lab/README.md) | Workflow automation, monitoring, and reporting | In progress |
| [SAP Security Lab](projects/sap-security-lab/README.md) | Access governance and authorization concepts | Planned |
| [SAP GRC SoD Lab](projects/sap-grc-sod-lab/README.md) | Segregation of Duties and mitigation concepts | Planned |
| [AI Cyber Risk Governance](projects/ai-cyber-risk-governance/README.md) | AI risk controls, oversight, and accountability | Planned |
| [Cybersecurity Research](projects/cybersecurity-research/README.md) | Research notes and cybersecurity case studies | Planned |

## Featured Demonstration: Vulnerability Management

The executive dashboard prototype illustrates how vulnerability data can be transformed into actionable management information.

**Key capabilities**
- Executive indicators for open vulnerabilities, critical findings, overdue remediation, SLA compliance, and remediated items.
- Filtering by country, severity, status, responsible party, SLA status, and search criteria.
- CSV import and export for sample vulnerability records.
- Visual summaries and a detailed vulnerability table.
- Print-friendly reporting for review and discussion.

**Current scope and limitations**
- Processes imported CSV data in the browser.
- Does not connect directly to Tenable or other vulnerability management platforms.
- Does not establish a production integration, automated scanning process, or authoritative remediation workflow.
- Uses synthetic data for demonstration.
- SLA definitions and reporting logic must be validated against the applicable organizational policy before operational use.

[**Open the Live Dashboard →**](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)

## Portfolio Principles

- **Risk-informed security:** prioritize cybersecurity decisions according to business impact and exposure.
- **Traceability:** connect risks, controls, evidence, remediation actions, and decisions.
- **Human accountability:** retain explicit human ownership for risk acceptance and high-impact decisions.
- **Measurable outcomes:** use meaningful indicators to support prioritization, oversight, and continuous improvement.
- **Responsible AI:** apply human oversight, transparency, and appropriate controls to AI-supported activities.
- **Reproducibility:** use synthetic data and documented assumptions in demonstration environments.
- **Confidentiality:** exclude confidential company, customer, supplier, and production information.

## Technology and Frameworks

The portfolio may include examples involving:

- Python and automated validation.
- HTML, JavaScript, and browser-based reporting.
- Git and GitHub Pages.
- SAP Security and SAP GRC concepts.
- Cybersecurity governance, risk assessment, and control mapping.
- NIST Cybersecurity Framework, ISO/IEC 27001, and related standards.
- AI risk governance and human oversight.

Frameworks are referenced for educational and analytical purposes. Each project should identify the specific framework version and control mappings relevant to its scope.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio.git
cd cyber-grc-engineering-portfolio
```

For the vulnerability management dashboard, open the HTML file in a modern browser or use the [published GitHub Pages demonstration](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html).

To run Python-based projects, consult the README and requirements of the specific project before executing commands. Python 3.11 or later is recommended for applicable Python labs.

## Repository Structure

```text
.
├── data/             # Synthetic example data
├── docs/             # Architecture and contribution guidance
├── projects/         # Independent portfolio projects
├── src/              # Shared Python code, where applicable
├── tests/            # Automated tests, where implemented
├── .gitignore
├── README.md
└── requirements.txt
```

Individual projects may have their own requirements, instructions, test coverage, and maturity level.

## Roadmap

- [x] Publish the initial risk register example.
- [x] Publish the vulnerability management executive dashboard prototype.
- [x] Validate the dashboard with synthetic CSV test scenarios.
- [ ] Expand automated test coverage and document test results.
- [ ] Implement persistent remediation traceability, including owner, corrective action, evidence, validation date, and verification outcome.
- [ ] Add a synthetic SAP Segregation of Duties rule matrix.
- [ ] Develop an AI risk assessment example with explicit human review gates.
- [ ] Expand control-to-evidence traceability and audit-ready documentation.

## Disclaimer

This repository is an independent educational portfolio. It is not affiliated with or endorsed by NIST, ISO, SAP, or any employer.

Projects are prototypes and learning artifacts, not representations of production implementations or certifications. Framework references and control mappings must be verified against current official publications. Validate security logic, assumptions, test coverage, and organizational requirements before using any artifact in a real environment.

All demonstration data should be synthetic or appropriately sanitized. No production security decisions should rely solely on these examples.
