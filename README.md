# ◈ CYBER GRC ENGINEERING

### GOVERNANCE · RISK · SECURITY ENGINEERING · DATA TRUST · RESPONSIBLE AI

**Engineering trust. Governing digital risk. Turning controls into verifiable outcomes.**

An independent engineering portfolio exploring how cybersecurity governance, enterprise risk, data governance, automation, and responsible AI can be translated into practical, measurable, and auditable technical solutions.

[Featured Projects](#-featured-projects) · [Live Demonstrations](#-live-demonstrations) · [Engineering Principles](#-engineering-principles) · [Technology & Frameworks](#-technology--frameworks) · [Roadmap](#-roadmap)

---

## ◈ Mission

Cybersecurity and enterprise governance should go beyond documenting requirements. They should help organizations understand exposure, prioritize decisions, establish accountability, and demonstrate that controls are operating as intended.

This portfolio explores how governance requirements can become **executable rules, traceable evidence, reproducible tests, and decision-useful indicators**.

The engineering focus connects five dimensions:

| Dimension | Engineering objective |
|---|---|
| **Cyber GRC** | Translate governance requirements into actionable controls. |
| **Risk Engineering** | Prioritize exposure based on business context and impact. |
| **Data Governance** | Improve data quality, ownership, lineage, and accountability. |
| **ESG Assurance** | Strengthen the traceability and reliability of sustainability information. |
| **AI & Digital Risk** | Support responsible technology adoption through risk assessment and human oversight. |

---

## ◈ Featured Projects

Explore the current engineering labs, demonstrations, and research initiatives.

| Project | Focus | Status |
|---|---|---|
| [**GRC Automation Lab**](projects/grc-automation-lab/README.md) | Remediation records, evidence, validation, audit history, and GRC analytics | Active |
| [**GRC Executive Dashboard**](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html) | Executive visibility and governance indicators | Published prototype |
| [**Vulnerability Management Dashboard**](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html) | Vulnerability exposure, remediation SLAs, and CSV analysis | Published prototype |
| [**Cyber GRC Risk Register**](projects/cyber-grc-risk-register/README.md) | Risk scenarios, scoring, and input validation | Initial project |
| **Data Trust & Control Graph** | Data quality, ownership, lineage, and governance controls | Planned |
| **ESG Evidence & Risk Assurance Engine** | Sustainability data reliability, evidence traceability, and control assurance | Planned |
| [**SAP Security Lab**](projects/sap-security-lab/README.md) | SAP access governance and authorization concepts | Planned |
| [**SAP GRC Segregation of Duties Lab**](projects/sap-grc-sod-lab/README.md) | Segregation of duties and mitigation concepts | Planned |
| [**AI Cyber Risk Governance**](projects/ai-cyber-risk-governance/README.md) | AI risk controls and human oversight | Planned |
| [**Cybersecurity Research**](projects/cybersecurity-research/README.md) | Research notes, technical analysis, and case studies | Planned |

**Maturity principle:** a published prototype is not equivalent to a production implementation. Planned initiatives are research directions, not completed capabilities. Each project must document its current scope, limitations, and validation status.

---

## ◈ Live Demonstrations

### 01 · GRC Executive Dashboard

Explore an executive reporting prototype focused on cybersecurity governance and management visibility.

- [**Open the live dashboard**](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html)
- [View the dashboard source](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html)

Review the implementation to understand the indicators and behavior actually provided by the prototype.

### 02 · Vulnerability Management Executive Dashboard

Explore how imported vulnerability records can be transformed into management indicators and operational views.

- [**Open the live dashboard**](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)
- [Read the GRC Automation Lab documentation](projects/grc-automation-lab/README.md)

**Current capabilities**
- Executive indicators for vulnerability exposure, severity, overdue remediation, SLA compliance, and remediated findings.
- Filtering by country, severity, status, owner, and SLA status.
- CSV import and export.
- Searchable records, visual summaries, and print-oriented reporting.

**Current limitations**
- Records are imported from CSV and processed in the browser.
- Direct Tenable API integration and automated scan ingestion are not implemented.
- The dashboard does not replace an official vulnerability management platform.
- Dashboard processing is distinct from the persistent remediation register implemented in the Python GRC Automation Lab.
- SLA calculations must be validated against the applicable organizational policy before operational use.

Use synthetic demonstration data for public demonstrations. Never upload confidential, personal, or production vulnerability records.

---

## ◈ Engineering Principles

### Risk before activity

Prioritize exposure according to business impact, exploitability, criticality, and applicable obligations — not merely by the number of findings processed.

### Traceability by design

Build explicit relationships between:

**Risk → Control → Evidence → Finding → Corrective Action → Validation → Decision**

The relationship must be supported by actual implementation and documented tests, not just by diagrams or descriptions.

### Human accountability

Automation can organize evidence, calculate indicators, and support recommendations. Accountable people remain responsible for risk acceptance, exceptions, and consequential security decisions.

### Evidence over assumptions

Document data sources, calculation rules, test scenarios, limitations, and validation results. An indicator should not be treated as trustworthy without understanding how it was produced.

### Measurable outcomes

Distinguish exposure, remediation progress, SLA performance, exceptions, and verified closure. Metrics should support decisions rather than reward activity without context.

### Responsible AI

Apply appropriate human oversight, transparency, access restrictions, and risk assessment to AI-assisted processes. AI outputs are not automatically definitive evidence.

### Reproducibility and confidentiality

Use synthetic demonstration data, document assumptions, and exclude confidential company, customer, supplier, and production information from public artifacts.

---

## ◈ Technology & Frameworks

### Engineering technologies

| Technology | Application |
|---|---|
| **Python** | Data validation, analytics, persistence, and automation |
| **SQLite** | Structured storage for selected GRC records and audit history |
| **HTML, CSS & JavaScript** | Browser-based reporting prototypes |
| **CSV** | Portable input and output for selected demonstrations |
| **Git & GitHub** | Version control, documentation, and collaboration |
| **GitHub Actions** | Automated workflows where configured |
| **Automated testing** | Repeatable verification of implemented behavior |

Technologies are listed according to their use across the portfolio. Not every project uses every technology.

### Governance and security references

| Reference | Application area |
|---|---|
| **NIST Cybersecurity Framework 2.0** | Cybersecurity governance and risk outcomes |
| **NIST SP 800-30** | Risk assessment |
| **NIST SP 800-53** | Security and privacy control references |
| **ISO/IEC 27001** | Information security management systems |
| **ISO/IEC 27002** | Information security controls |
| **ISO/IEC 27005** | Information security risk management |
| **ISO/IEC 27701** | Privacy information management |
| **ISO/IEC 42001** | AI management systems |
| **NIST AI RMF** | AI risk management |
| **COBIT 2019** | Enterprise IT governance and management |
| **DAMA-DMBOK** | Data management and data governance concepts |
| **ESRS and GRI** | Sustainability reporting and related information requirements |

Frameworks are selected according to each project's scope. References do not imply certification, complete compliance, or verified control effectiveness. Applicable versions and requirements must be confirmed during implementation.

---

## ◈ Roadmap

The roadmap prioritizes verifiable engineering progress, clear requirements, and reproducible results over feature count.

### GRC Automation & Remediation Assurance

- [x] Implement persistent remediation records.
- [x] Record remediation metadata and validation outcomes.
- [x] Preserve before-and-after snapshots in remediation history.
- [x] Add backward-compatible handling for legacy audit-history schemas.
- [x] Validate the implementation with the automated test suite.
- [ ] Expand automated tests for additional edge cases and audit-history integrity.
- [ ] Document the remediation data model and event semantics.
- [ ] Assess integrity protections, access controls, and production deployment requirements.

### Data Governance

- [ ] Specify the Data Trust & Control Graph architecture.
- [ ] Define data asset ownership, stewardship, classification, and lineage models.
- [ ] Implement synthetic data quality rules and validation results.
- [ ] Link data quality findings to controls, accountable owners, and remediation actions.
- [ ] Produce traceable governance indicators and technical documentation.

### ESG Governance & Assurance

- [ ] Define the ESG Evidence & Risk Assurance Engine scope.
- [ ] Model sustainability indicators, source data, methodologies, and evidence references.
- [ ] Implement validation for completeness, consistency, traceability, and reporting periods.
- [ ] Identify unsupported, estimated, or inconsistent indicators.
- [ ] Connect findings to risk, control, and remediation records.
- [ ] Document assurance limitations and applicable reporting requirements.

### AI, Digital Risk & Enterprise Governance

- [ ] Develop an AI cyber risk assessment example with explicit human review.
- [ ] Explore reusable control-to-evidence mappings.
- [ ] Develop SAP segregation-of-duties rules and mitigation scenarios.
- [ ] Investigate integration patterns across cyber risk, data governance, and ESG assurance.

Roadmap items remain planned until implementation and relevant validation have been completed.

---

## ◈ Repository Structure

```text
cyber-grc-engineering-portfolio/
├── projects/
│   ├── grc-automation-lab/
│   ├── cyber-grc-risk-register/
│   ├── sap-security-lab/
│   ├── sap-grc-sod-lab/
│   ├── ai-cyber-risk-governance/
│   └── cybersecurity-research/
├── docs/
├── tests/
├── README.md
└── requirements.txt
```

This is a logical overview, not a guarantee that every directory exists or is complete. New projects will be added as their specifications and implementations mature.

---

## ◈ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio.git
cd cyber-grc-engineering-portfolio
```

### 2. Explore the demonstrations

- [GRC Executive Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html)
- [Vulnerability Management Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)

### 3. Explore the Python projects

Read the relevant project README before installing dependencies or executing commands. Follow the Python version and setup instructions specified by the individual project.

### 4. Review maturity and limitations

Before adapting an artifact, review its prerequisites, supported inputs, calculation rules, test coverage, validation status, and known limitations.

---

## ◈ Quality & Validation

Where applicable, projects should progressively demonstrate:

- **Functional correctness:** behavior matches documented rules.
- **Input validation:** malformed, missing, duplicate, or unexpected values are handled safely.
- **Test reproducibility:** scenarios can be repeated with known inputs and expected outcomes.
- **Data integrity:** exports and persistent records retain the intended information.
- **Auditability:** significant changes can be attributed and reconstructed.
- **Security:** access assumptions, data handling, and implementation boundaries are explicit.
- **Transparency:** unsupported integrations and unverified claims are clearly identified.

Test status must reflect tests that have actually been executed. A manually tested prototype must not be described as fully tested or production-ready.

---

## ◈ Security & Responsible Use

This repository is an independent educational and engineering portfolio. It is not affiliated with or endorsed by NIST, ISO, SAP, or any employer.

- Use synthetic or appropriately anonymized data in public demonstrations.
- Do not publish credentials, secrets, confidential architecture details, or production vulnerability information.
- Validate calculation logic, control mappings, and governance assumptions before real-world adaptation.
- Do not treat prototype outputs as definitive risk decisions or proof of compliance.
- Do not rely on these examples as the sole basis for production security decisions.
- Verify framework references and mappings against applicable official publications.

---

<div align="center">

### Governance that guides decisions.
### Engineering that makes controls actionable.
### Evidence that makes outcomes verifiable.

[Explore the Repository](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio) · [Open GRC Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html) · [Open Vulnerability Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)

*Cyber GRC Engineering Portfolio · Learn · Build · Validate · Improve*
</div>
