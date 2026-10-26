# ◈ CYBER GRC ENGINEERING PORTFOLIO

<p align="center">
  <strong>GOVERNANCE · RISK · SECURITY ENGINEERING · RESPONSIBLE AI</strong>
</p>

<p align="center">
  <a href="https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio">
    <img src="https://img.shields.io/badge/Portfolio-Cyber%20GRC-00D9FF?style=for-the-badge&logo=github&logoColor=white" alt="Cyber GRC Portfolio">
  </a>
  <img src="https://img.shields.io/badge/Focus-Risk%20%26%20Governance-8B5CF6?style=for-the-badge" alt="Risk and Governance">
  <img src="https://img.shields.io/badge/Approach-Evidence--Driven-14B8A6?style=for-the-badge" alt="Evidence Driven">
  <img src="https://img.shields.io/badge/AI-Human%20Oversight-EC4899?style=for-the-badge" alt="Responsible AI">
</p>

<p align="center">
  <strong>Transforming cybersecurity governance into measurable, traceable and business-aligned outcomes.</strong>
</p>

<p align="center">
  An independent engineering portfolio exploring how governance, risk management, security controls, automation and responsible AI can work together to improve cybersecurity decision-making.
</p>

<p align="center">
  <a href="#-featured-projects">Projects</a> ·
  <a href="#-live-demonstrations">Live Demos</a> ·
  <a href="#-engineering-principles">Principles</a> ·
  <a href="#-technology--frameworks">Technology</a> ·
  <a href="#-roadmap">Roadmap</a>
</p>

---

## ◈ The Mission

Cybersecurity governance should do more than document requirements. It should help organizations understand exposure, prioritize decisions, demonstrate control effectiveness and establish accountability.

This portfolio explores the engineering practices that connect cybersecurity strategy to measurable execution.

**The objective is to build practical, transparent and auditable examples of Cyber GRC Engineering** — combining risk-based governance, security metrics, evidence management, workflow automation and human oversight.

### The engineering perspective

| Dimension | Engineering objective |
|---|---|
| Governance | Translate policies and requirements into operational controls. |
| Risk | Prioritize exposure according to business impact and context. |
| Assurance | Connect control objectives, evidence, findings and validation. |
| Automation | Reduce manual effort while preserving accountability. |
| Measurement | Convert technical information into decision-useful indicators. |
| Responsible AI | Apply transparency, human oversight and appropriate safeguards. |

---

## ◈ Featured Projects

The portfolio includes working prototypes, developing engineering artifacts and planned research. Each project is identified according to its current maturity.

| Project | Engineering focus | Status |
|---|---|---|
| [GRC Executive Dashboard](projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html) | Executive GRC visibility and management indicators | Published prototype |
| [Vulnerability Management Dashboard](projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html) | Vulnerability exposure, remediation SLAs and CSV analysis | Published prototype |
| [Cyber GRC Risk Register](projects/cyber-grc-risk-register/README.md) | Risk scenarios, scoring and CSV validation | Initial project |
| [GRC Automation Lab](projects/grc-automation-lab/README.md) | Workflow concepts, reporting and auditability | In progress |
| [SAP Security Lab](projects/sap-security-lab/README.md) | SAP access governance and authorization concepts | Planned |
| [SAP GRC Segregation of Duties Lab](projects/sap-grc-sod-lab/README.md) | Segregation of duties and mitigation concepts | Planned |
| [AI Cyber Risk Governance](projects/ai-cyber-risk-governance/README.md) | AI risk controls and human oversight | Planned |
| [Cybersecurity Research](projects/cybersecurity-research/README.md) | Research notes, technical analysis and case studies | Planned |

> **Maturity principle:** a published prototype is not equivalent to a production implementation. Project status reflects the current scope, not a claim of operational readiness.

---

## ◈ Live Demonstrations

### 01 — GRC Executive Dashboard

**Purpose:** Explore an executive reporting prototype focused on cybersecurity governance and management visibility.

- [Launch live dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html)
- [View source code](projects/grc-automation-lab/dashboards/grc-executive/grc_executive_dashboard.html)

The dashboard's actual indicators and behaviors should be evaluated directly in the implementation. Its presence in this portfolio does not imply that every GRC workflow or control assurance capability described elsewhere has been implemented.

### 02 — Vulnerability Management Executive Dashboard

**Purpose:** Demonstrate how imported vulnerability records can be transformed into management indicators and filtered operational views.

<p align="center">
  <a href="https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html">
    <img src="https://img.shields.io/badge/LAUNCH-Live%20Dashboard-00D9FF?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Launch Vulnerability Dashboard">
  </a>
  <a href="projects/grc-automation-lab/dashboards/vulnerability-management/README.md">
    <img src="https://img.shields.io/badge/READ-Technical%20Documentation-8B5CF6?style=for-the-badge&logo=readthedocs&logoColor=white" alt="Read Technical Documentation">
  </a>
</p>

**Current capabilities**

- Executive indicators for open vulnerabilities, critical findings, overdue SLAs, SLA compliance and remediated findings.
- Filtering by country, severity, status, responsible party and SLA status.
- CSV import and export for vulnerability records.
- Searchable records and detailed operational views.
- Visual summaries and print-friendly reporting.

**Current boundaries**

- Records are imported from CSV and processed in the browser.
- No direct Tenable API integration or automated scan ingestion is implemented.
- The dashboard does not replace the authoritative vulnerability management platform.
- A persistent remediation register, controlled state transitions and a tamper-resistant audit trail are not yet implemented.
- SLA rules and reporting calculations require validation against the applicable organizational policy before operational use.

**Demonstration:** [Open Vulnerability Management Dashboard](https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/projects/grc-automation-lab/dashboards/vulnerability-management/vulnerability_executive_dashboard.html)

---

## ◈ Engineering Principles

### Risk before activity

Prioritize work according to exposure, business impact, exploitability and applicable obligations — not merely the number of findings closed.

### Traceability by design

Build toward an explicit relationship between:

`Risk → Control → Evidence → Finding → Corrective Action → Validation → Decision`

Traceability is a design objective; each project must document which links are actually implemented.

### Human accountability

Automation can organize evidence, calculate indicators and support recommendations. Accountable people remain responsible for risk acceptance, exceptions and consequential security decisions.

### Evidence over assumptions

Document data sources, calculation rules, test scenarios, limitations and validation results. Do not treat an indicator as reliable without understanding how it was produced.

### Measurable outcomes

Distinguish exposure, remediation progress, SLA performance, exceptions and verified closure. Metrics should support decisions rather than reward activity without context.

### Responsible AI

Apply appropriate human oversight, transparency, access restrictions and risk assessment to AI-assisted processes. AI output is not automatically authoritative evidence.

### Reproducibility and confidentiality

Use synthetic demonstration data, document assumptions and exclude confidential company, customer, supplier and production information from public artifacts.

---

## ◈ Technology & Frameworks

### Engineering technologies

| Technology | Intended application |
|---|---|
| HTML, CSS and JavaScript | Browser-based reporting prototypes |
| Python | Data validation, analysis and automation examples |
| CSV | Portable input and output for selected prototypes |
| Git and GitHub | Version control, documentation and collaboration |
| GitHub Pages | Public demonstration of static projects |
| Automated testing | Repeatable verification where implemented |

The technologies listed describe the portfolio's scope and potential use. They do not imply that every technology is used in every project.

### Governance and security references

| Reference | Area of application |
|---|---|
| NIST Cybersecurity Framework 2.0 | Cybersecurity governance and risk outcomes |
| NIST SP 800-30 | Risk assessment methodology |
| NIST SP 800-53 | Security and privacy control references |
| ISO/IEC 27001 | Information security management systems |
| ISO/IEC 27002 | Information security controls |
| ISO/IEC 27005 | Information security risk management |
| ISO/IEC 27701 | Privacy information management |
| ISO/IEC 42001 | AI management systems |
| NIST AI RMF | AI risk management |
| COBIT 2019 | Governance and management of enterprise IT |
| SAP security and SAP GRC concepts | Access governance and segregation of duties |

Framework mappings must identify the relevant version, scope and source. A conceptual mapping is not proof of compliance, certification or control effectiveness.

---

## ◈ Roadmap

The roadmap prioritizes verifiable engineering progress over feature count.

- [x] Publish the vulnerability management dashboard prototype.
- [x] Document its CSV-based operating model and current limitations.
- [ ] Expand reproducible test coverage and publish test results.
- [ ] Strengthen CSV validation, normalization and duplicate detection.
- [ ] Implement a structured remediation register.
- [ ] Record accountable owner, corrective action, due date and evidence reference.
- [ ] Add validation date, verifier and verification result.
- [ ] Preserve remediation status history and timestamps.
- [ ] Implement and test browser-based persistence and data recovery for the initial prototype.
- [ ] Evaluate a backend and database for centralized, multi-user operation.
- [ ] Develop a synthetic SAP segregation-of-duties ruleset.
- [ ] Build an AI cyber risk assessment example with explicit human review.
- [ ] Expand control-to-evidence traceability and audit-ready documentation.

Roadmap items are planned improvements, not claims of completed functionality. Completion should be recorded only after implementation and relevant tests.

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

This is a logical overview of the intended repository organization. Individual directories and files may be added as projects evolve.

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

Read the README and requirements for the specific project before installing dependencies or running commands. Python 3.11 or later is a suggested baseline for applicable Python projects; individual projects may require a different version.

### 4. Review project-specific maturity

Before relying on an artifact, check its documentation for prerequisites, supported inputs, known limitations, test coverage and validation status.

---

## ◈ Quality & Validation

Engineering quality requires more than a successful demonstration.

Where applicable, projects should progressively document:

- **Functional correctness:** calculations and state changes match documented rules.
- **Input validation:** malformed, missing, duplicate or unexpected values are handled safely.
- **Test reproducibility:** scenarios can be repeated with known inputs and expected outcomes.
- **Data integrity:** exports and persisted records retain the intended information.
- **Auditability:** important changes can be attributed and reconstructed.
- **Security:** access, data handling and deployment assumptions are explicit.
- **Limitations:** unsupported integrations and unverified claims are clearly identified.

Test status must reflect tests actually executed. A manually exercised prototype must not be described as comprehensively tested or production-ready.

---

## ◈ Security & Responsible Use

This repository is an independent educational portfolio. It is not affiliated with or endorsed by NIST, ISO, SAP, or any employer.

- Use synthetic or appropriately anonymized data in public demonstrations.
- Do not publish credentials, secrets, internal architecture details or confidential vulnerability information.
- Validate calculation logic, control mappings, security requirements and governance assumptions before adapting any artifact to a real environment.
- Do not treat prototype outputs as authoritative risk decisions or proof of compliance.
- Do not use these examples as the sole basis for production security decisions.

All framework references and control mappings must be verified against the applicable official publications.

---

## ◈ The Standard

<p align="center">
  <strong>Governance that guides decisions.</strong><br>
  <strong>Engineering that makes controls actionable.</strong><br>
  <strong>Evidence that makes outcomes verifiable.</strong>
</p>

<p align="center">
  <a href="https://github.com/adriana-cybergrc/cyber-grc-engineering-portfolio">Explore the Repository</a>
  &nbsp; · &nbsp;
  <a href="https://adriana-cybergrc.github.io/cyber-grc-engineering-portfolio/">Visit the Portfolio Site</a>
</p>

<p align="center">
  <sub>Cyber GRC Engineering Portfolio · Learn · Build · Validate · Improve</sub>
</p>