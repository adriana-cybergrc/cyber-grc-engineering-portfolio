<div align="center">

# ◈ CYBER GRC ENGINEERING

### GOVERNANCE · RISK · SECURITY ENGINEERING · RESPONSIBLE AI

**Turning cybersecurity governance into measurable, traceable, and business-aligned outcomes.**

An independent engineering portfolio exploring how governance, risk management, security controls, automation, and responsible AI can work together to improve cybersecurity decision-making.

[Featured Projects](#-featured-projects) · [Live Demonstrations](#-live-demonstrations) · [Engineering Principles](#-engineering-principles) · [Technology & Frameworks](#-technology--frameworks) · [Roadmap](#-roadmap)

</div>

---

## ◈ Mission

Cybersecurity governance should go beyond documenting requirements. It should help organizations understand exposure, prioritize decisions, demonstrate control effectiveness, and establish accountability.

This portfolio explores engineering practices that connect cybersecurity strategy with measurable execution.

The goal is to build practical, transparent, and auditable examples of **Cyber GRC Engineering** by combining risk-based governance, security metrics, evidence management, workflow automation, and human oversight.

### The engineering perspective

| Dimension | Engineering objective |
|---|---|
| **Governance** | Translate policies and requirements into actionable controls. |
| **Risk** | Prioritize exposure based on business impact and context. |
| **Assurance** | Connect control objectives, evidence, findings, and validation. |
| **Automation** | Reduce manual effort without removing accountability. |
| **Measurement** | Turn technical information into decision-useful indicators. |
| **Responsible AI** | Apply transparency, human oversight, and appropriate safeguards. |

---

## ◈ Featured Projects

The portfolio includes functional prototypes, engineering artifacts under development, and planned research. Each project is labeled according to its current maturity.

| Project | Engineering focus | Status |
|---|---|---|
| [**GRC Executive Dashboard**](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html) | Executive visibility and GRC management indicators | Published prototype |
| [**Vulnerability Management Dashboard**](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html) | Vulnerability exposure, remediation SLAs, and CSV analysis | Published prototype |
| [**Cyber GRC Risk Register**](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/cyber-grc-risk-register/README.md) | Risk scenarios, scoring, and CSV validation | Initial project |
| [**GRC Automation Lab**](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/grc-automation-lab/README.md) | Workflow concepts, reporting, and auditability | In progress |
| [**SAP Security Lab**](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/sap-security-lab/README.md) | SAP access governance and authorization concepts | Planned |
| [**SAP GRC Segregation of Duties Lab**](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/sap-grc-sod-lab/README.md) | Segregation of duties and mitigation concepts | Planned |
| [**AI Cyber Risk Governance**](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/ai-cyber-risk-governance/README.md) | AI risk controls and human oversight | Planned |
| [**Cybersecurity Research**](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/cybersecurity-research/README.md) | Research notes, technical analysis, and case studies | Planned |

> **Maturity principle:** A published prototype is not equivalent to a production implementation. Project status reflects current scope, not operational readiness.

---

## ◈ Live Demonstrations

### 01 — GRC Executive Dashboard

**Purpose:** Explore an executive reporting prototype focused on cybersecurity governance and management visibility.

- [**Open the live GRC Executive Dashboard**](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html)
- [View source code](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html)

Evaluate the dashboard's actual indicators and behavior directly in the implementation. Its presence in this portfolio does not imply that every GRC workflow or control-assurance capability described elsewhere has been implemented.

### 02 — Vulnerability Management Executive Dashboard

**Purpose:** Demonstrate how imported vulnerability records can be transformed into management indicators and filtered operational views.

- [**Open the live Vulnerability Management Dashboard**](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)
- [Read the technical documentation](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio/blob/main/projects/grc-automation-lab/README.md)

#### Current capabilities

- Executive indicators for open vulnerabilities, critical findings, overdue SLAs, SLA compliance, and remediated findings.
- Filtering by country, severity, status, owner, and SLA status.
- CSV import and export for vulnerability records.
- Searchable records and filtered operational views.
- Visual summaries and print-oriented reporting.

#### Current limitations

- Records are imported from CSV and processed in the browser.
- Direct Tenable API integration and automated scan ingestion are not implemented.
- The dashboard does not replace the official vulnerability management platform.
- A persistent remediation register, controlled state transitions, and a tamper-evident audit trail have not been implemented.
- SLA rules and report calculations require validation against the applicable organizational policy before operational use.

> Use synthetic demonstration data for public demonstrations. Do not upload confidential, personal, or production vulnerability data.

---

## ◈ Engineering Principles

### Risk before activity

Prioritize work according to exposure, business impact, exploitability, and applicable obligations—not merely by the number of findings processed.

### Traceability by design

Build an explicit relationship between:

**Risk → Control → Evidence → Finding → Corrective Action → Validation → Decision**

Traceability is a design objective. Each project must document which connections have actually been implemented.

### Human accountability

Automation can organize evidence, calculate indicators, and support recommendations. Accountable people remain responsible for risk acceptance, exceptions, and consequential security decisions.

### Evidence over assumptions

Document data sources, calculation rules, test scenarios, limitations, and validation results. Do not treat an indicator as trustworthy without understanding how it was produced.

### Measurable outcomes

Distinguish exposure, remediation progress, SLA performance, exceptions, and verified closure. Metrics should support decisions rather than reward activity without context.

### Responsible AI

Apply appropriate human oversight, transparency, access restrictions, and risk assessment to AI-assisted processes. AI outputs are not automatically definitive evidence.

### Reproducibility and confidentiality

Use synthetic demonstration data, document assumptions, and exclude confidential company, customer, supplier, and production information from public artifacts.

---

## ◈ Technology & Frameworks

### Engineering technologies

| Technology | Intended application |
|---|---|
| HTML, CSS, and JavaScript | Browser-based reporting prototypes |
| Python | Data validation, analysis, and automation examples |
| CSV | Portable input and output for selected prototypes |
| Git and GitHub | Version control, documentation, and collaboration |
| GitHub Pages | Public demonstrations of static projects |
| Automated tests | Repeatable verification where implemented |

The technologies listed describe the portfolio's scope and potential use. They do not imply that every technology is used in every project.

### Governance and security references

| Reference | Application area |
|---|---|
| **NIST Cybersecurity Framework 2.0** | Cybersecurity governance and risk outcomes |
| **NIST SP 800-30** | Risk assessment methodology |
| **NIST SP 800-53** | Security and privacy control references |
| **ISO/IEC 27001** | Information security management systems |
| **ISO/IEC 27002** | Information security controls |
| **ISO/IEC 27005** | Information security risk management |
| **ISO/IEC 27701** | Privacy information management |
| **ISO/IEC 42001** | AI management systems |
| **NIST AI RMF** | AI risk management |
| **COBIT 2019** | Enterprise IT governance and management |
| **SAP Security and SAP GRC concepts** | Access governance and segregation of duties |

Framework mappings should identify the relevant version, scope, and source. A conceptual mapping does not establish compliance, certification, or control effectiveness.

---

## ◈ Roadmap

The roadmap prioritizes verifiable engineering progress over feature count.

### Vulnerability management and assurance

- [x] Publish the vulnerability management dashboard prototype.
- [x] Document its CSV-based operating model and current limitations.
- [ ] Expand reproducible test coverage and publish test results.
- [ ] Improve CSV validation, normalization, and duplicate detection.
- [ ] Implement a structured remediation record.
- [ ] Record the accountable owner, corrective action, due date, and evidence reference.
- [ ] Add validation date, verifier, and verification outcome.
- [ ] Preserve remediation status history and timestamps.
- [ ] Implement and test browser-based persistence and recovery for the initial prototype.
- [ ] Assess a backend and database for centralized, multi-user operation.

### Broader portfolio

- [ ] Develop a synthetic SAP segregation-of-duties ruleset.
- [ ] Develop an AI cyber risk assessment example with explicit human review.
- [ ] Extend control-to-evidence traceability and audit-ready documentation.

Roadmap items are planned improvements, not claims of completed functionality. Completion should be recorded only after the relevant implementation and tests have been performed.

---

## ◈ Repository Structure

```text
.
├── data/               # Synthetic example data
├── docs/               # Architecture and contribution guidance
├── projects/
│   ├── grc-automation-lab/
│   │   └── dashboards/
│   │       ├── grc-executive/
│   │       └── vulnerability-management/
│   ├── cyber-grc-risk-register/
│   ├── sap-security-lab/
│   ├── sap-grc-sod-lab/
│   ├── ai-cyber-risk-governance/
│   └── cybersecurity-research/
├── src/                # Shared Python code, where applicable
├── tests/              # Automated tests, where implemented
├── .gitignore
├── README.md
└── requirements.txt
```

This is a logical overview of the repository's intended organization. Individual directories and files may be added as projects evolve.

---

## ◈ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio.git
cd cyber-grc-engineering-portfolio
```

### 2. Explore the dashboards

Open the HTML files in a modern browser or use the published demonstrations:

- [GRC Executive Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html)
- [Vulnerability Management Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)

Use synthetic data for public demonstrations.

### 3. Explore Python projects

Read the relevant project README and requirements before installing dependencies or running commands. Python 3.11 or later is a suggested minimum for applicable Python projects; individual projects may require a different version.

### 4. Review project-specific maturity

Before using an artifact, check its documentation for prerequisites, supported inputs, known limitations, test coverage, and validation status.

---

## ◈ Quality & Validation

Engineering quality requires more than a successful demonstration.

Where applicable, projects should progressively document:

- **Functional correctness:** calculations and state changes match documented rules.
- **Input validation:** malformed, missing, duplicate, or unexpected values are handled safely.
- **Test reproducibility:** scenarios can be repeated with known inputs and expected outcomes.
- **Data integrity:** exports and persistent records retain the intended information.
- **Auditability:** significant changes can be attributed and reconstructed.
- **Security:** access assumptions, data handling, and implementation boundaries are explicit.
- **Limitations:** unsupported integrations and unverified claims are clearly identified.

Test status must reflect tests that have actually been executed. A manually tested prototype should not be described as fully tested or production-ready.

---

## ◈ Security & Responsible Use

This repository is an independent educational portfolio. It is not affiliated with or endorsed by NIST, ISO, SAP, or any employer.

- Use synthetic or properly anonymized data in public demonstrations.
- Do not publish credentials, secrets, internal architecture details, or confidential vulnerability information.
- Validate calculation logic, control mappings, security requirements, and governance assumptions before adapting an artifact to a real environment.
- Do not treat prototype outputs as definitive risk decisions or proof of compliance.
- Do not rely on these examples as the sole basis for production security decisions.
- Verify all framework references and control mappings against the applicable official publications.

---

## ◈ The Standard

<div align="center">

**Governance that guides decisions.**  
**Engineering that makes controls actionable.**  
**Evidence that makes outcomes verifiable.**

[Explore the Repository](https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio) · [Open GRC Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html) · [Open Vulnerability Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)

*Cyber GRC Engineering Portfolio · Learn · Build · Validate · Improve*

</div>
