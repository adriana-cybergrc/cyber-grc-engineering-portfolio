# ◈ CYBER GRC ENGINEERING

### GOVERNANCE · RISK · SECURITY ENGINEERING · DATA TRUST · RESPONSIBLE AI

**Engineering trust. Governing digital risk. Turning controls into verifiable outcomes.**

An independent engineering portfolio exploring how cybersecurity governance, enterprise risk, data governance, automation, and responsible AI can be translated into practical, measurable, and auditable technical solutions.

[Featured Projects](#-featured-projects) · [Live Demonstrations](#-live-demonstrations) · [Engineering Principles](#-engineering-principles) · [Technology & Frameworks](#-technology--frameworks) · [Master Roadmap](docs/CYBER_GRC_ENGINEERING_MASTER_ROADMAP.md) · [CRISC Architecture](docs/architecture/CRISC-ARCH-001_REFERENCE_ARCHITECTURE_R0.1.md) · [Shared Data Model](docs/architecture/CRISC-DATA-001_SHARED_DATA_MODEL_R0.1.md) · [GRC Field Mapping](docs/architecture/CRISC-MAP-002_GRC_FIELD_TO_CANONICAL_MAPPING_R0.1.md) · [Implementation Roadmap](#-roadmap)

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
| **Data Governance & Data Trust** | Data asset ownership, classification, lineage, quality and control assurance | Planned |
| **DLP & Data Protection Assurance** | Data movement events, policy violations, investigations and governance evidence | Planned |
| **Third-Party Risk Management (TPRM)** | Supplier inventory, CSRA, fourth-party dependencies and remediation assurance | Planned |
| **KPI / KRI / KCI Intelligence** | Shared metric definitions, lineage, thresholds and executive reporting | Planned |
| **ESG Evidence & Risk Assurance Engine** | Sustainability data reliability, evidence traceability, and control assurance | Planned |
| **AI Security Assurance** | AI threat modeling and technical security assurance, separate from AI governance | Planned |
| [**SAP Security Lab**](projects/sap-security-lab/README.md) | SAP access governance and authorization concepts | Planned |
| [**SAP GRC Segregation of Duties Lab**](projects/sap-grc-sod-lab/README.md) | Synthetic SoD conflict detection and review-required findings | Implemented prototype |
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

## ◈ Portfolio Strategy & Master Roadmap

The [Cyber GRC Engineering Master Roadmap](docs/CYBER_GRC_ENGINEERING_MASTER_ROADMAP.md) defines the portfolio's strategic direction, architecture, engineering pillars, implementation phases, and governance principles.

It complements this README's implementation roadmap and the project-specific documentation. Roadmap capabilities remain planned until their implementation and validation are supported by repository evidence.

## ◈ Roadmap

The roadmap is dependency-driven. Existing implementations remain intact; new capabilities are added through versioned specifications, non-destructive changes and reproducible tests.

### Core GRC & Assurance
- [x] Python control evaluation and exception generation.
- [x] SQLite audit persistence and remediation records/history.
- [x] Analytics and executive dashboard generation.
- [x] Automated tests for core GRC behavior and integration paths.
- [ ] Extend cross-domain identifiers/data contracts without replacing existing tables.
- [ ] Complete field-level mapping of current SQLite entities and CSV inputs.
- [ ] Strengthen evidence metadata, lineage and audit-event semantics.

### Vulnerability Management — Scanner-Agnostic
**Current implementation:** standalone HTML/JavaScript dashboard; CSV import/export; browser-side filtering, KPIs, visual summaries and print. No direct scanner API, scheduled ingestion or centralized scanner repository is implemented.

**Target:** accept multiple scanner sources through independent adapters and normalize observations into a shared CRISC model. Tenable is not mandatory; Greenbone/OpenVAS is an explicit candidate.

- [x] Publish CSV-based executive dashboard prototype.
- [x] Document current limitations and preserve the dashboard.
- [ ] VM-P0: validate CSV schema, behavior and synthetic fixtures.
- [ ] VM-P1: implement/test Greenbone/OpenVAS XML parser using sanitized/synthetic reports.
- [ ] VM-P2: add Tenable CSV/JSON adapters against the same canonical model.
- [ ] VM-P3: evaluate Qualys/Rapid7 adapters using validated source contracts.
- [ ] VM-P4: assess other scanners and authorized API integrations.
- [ ] VM-P5: implement cross-scanner correlation, historical observations and risk analytics.
- [ ] Integrate vulnerability observations with asset criticality, business context, remediation and verified closure.

See [CRISC-VM-001](docs/architecture/CRISC-VM-001_SCANNER_AGNOSTIC_VULNERABILITY_MANAGEMENT_R0.1.md).

### Cross-Domain Governance Domains
- [ ] **TPRM / CSRA:** supplier inventory/criticality, due diligence, inherent/residual risk, contractual controls, fourth-party/concentration risk, remediation and assurance.
- [ ] **DLP:** data classification/discovery, movement events, policy violations, investigation and evidence; integrate Data Governance, Privacy and IAM.
- [ ] **Data Governance:** data assets, owners/stewards, classification, lineage, quality rules and accountable remediation.
- [ ] **KPI / KRI / KCI Engine:** shared metric dictionary, formulas, owners, source lineage, period, thresholds, data quality, trends and escalation.
- [ ] **AI Governance:** AI inventory, use cases, business purpose, risk classification, human oversight and governance controls.
- [ ] **AI Security:** technical threat modeling and security assurance, distinct from AI management-system governance.
- [ ] **ESG Assurance:** sustainability methodology, reporting boundary, source evidence, estimation status, traceability and assurance limitations.
- [ ] **Business Resilience:** BIA, process/dependency mapping, continuity, recovery objectives, exercises, incidents and remediation.
- [ ] **IAM / SAP / SoD:** extend synthetic identity and access governance examples; preserve the existing SoD prototype.

### Delivery Priorities

| Priority | Scope | Exit condition |
|---|---|---|
| P0 — Reconcile | Inventory repository, align README/roadmap/status, preserve code/tests | Accurate baseline; no destructive changes |
| P1 — Core model | Shared data model, field mappings, metric dictionary and data quality | Approved logical model and migration plan |
| P2 — Vulnerability + TPRM | Multi-scanner adapters, observations, CSRA and supplier risk | Reproducible fixtures, provenance and tests |
| P3 — DLP + Data + Identity | DLP events/violations, data governance, privacy, IAM/SAP | Clear semantics and traceable remediation |
| P4 — AI Governance + AI Security | AI inventory, governance assessment, technical security assurance | Distinct scopes, evidence and human approval |
| P5 — Resilience + ESG + Intelligence | BCM, ESG assurance, cross-domain analytics and governed AI | Validated metrics and accountable workflows |

### Publication and maturity rules
- A roadmap item is not an implemented feature.
- A connector is not supported until adapter, mapping, tests and security controls exist.
- Scanner severity is not equivalent to business risk.
- A finding disappearing from a later scan is not proof of remediation.
- Public examples use synthetic or sanitized data only.
- Preserve existing files/behavior; review diffs and tests before merge.

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
