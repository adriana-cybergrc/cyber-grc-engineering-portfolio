# CRISC-MAP-001 — Existing Repository-to-Target Data Model Mapping

**Version:** R0.1 | **Status:** Draft — Component Inventory / Field-Level Mapping Pending  
**Related:** CRISC-ARCH-001, CRISC-DATA-001, CRISC-VM-001

## Purpose and inspected baseline

Map observed repository components to the CRISC target without claiming all entities are implemented.

Repository: `adriana-cybergrc/cyber-grc-engineering-portfolio`  
Branch: `main` | Observed head: `51234930d5305bb88835235d7ad3bf5610b0eedb`  
Recursive tree: 66 paths; not truncated.

| Component | Evidence | Observed capability | Target mapping | Status |
|---|---|---|---|---|
| GRC Automation Lab | `projects/grc-automation-lab/src/`, `tests/`, `data/` | Python control evaluation, SQLite audit/remediation records/history, analytics, dashboard generation, tests | Control, Evidence, Finding, Remediation, AuditEvent, Metric | Implemented prototype |
| GRC executive dashboard | `projects/grc-automation-lab/dashboards/grc-executive/` | Static HTML visualization | Reporting | Published prototype |
| Vulnerability dashboard | `projects/grc-automation-lab/dashboards/vulnerability-management/` | HTML/JS, CSV import/export, browser analysis, filters, charts, print | Vulnerability reporting/UI | CSV-only prototype |
| Risk Register | `src/risk_register.py`, `data/risk_register.csv`, `tests/test_risk_register.py` | CSV validation and illustrative probability × impact score | Risk/RiskAssessment starter | Initial |
| SAP GRC SoD | `projects/sap-grc-sod-lab/src/sod_analyzer.py`, `data/`, `tests/` | Synthetic assignments, rule matching, review-required findings | Identity/control/finding review | Implemented prototype |
| AI Cyber Risk Governance | `projects/ai-cyber-risk-governance/README.md` | Scope only; no implementation files | AI inventory/governance | Planned |
| SAP Security | `projects/sap-security-lab/README.md` | Scope only; no implementation files | IAM/IGA/PAM | Planned |
| Cybersecurity Research | `projects/cybersecurity-research/README.md` | Placeholder README | Research/threat intelligence | Planned |

## Implementation boundaries

GRC Automation Lab has separate modules for control automation, audit persistence, remediation persistence, analytics, dashboard rendering and pipeline execution. Preserve SQLite migrations, backward compatibility, tests and data contracts. Map existing tables before schema changes.

Vulnerability dashboard processes imported CSV in the browser; supports KPIs, filters, visual summaries, search, export and print. No Tenable API or automated scan ingestion is implemented. It is not a scanner connector, normalized vulnerability repository, centralized remediation register or production audit system.

Risk Register validates required fields, duplicate IDs and probability/impact ranges; score is illustrative, not calibrated residual risk/appetite/acceptance.

SAP SoD analyzer reads synthetic user/function assignments and conflict matrix, emits `REQUIRES_REVIEW`; it is not SAP production integration, official SAP ruleset or automated fraud/policy conclusion.

## Documentation inconsistencies found

1. SAP GRC SoD README mixes implemented execution instructions with contradictory Planned status.
2. Vulnerability dashboard README overstates remediation tracking/local persistence; inspected HTML has CSV import/export and does not contain a localStorage/IndexedDB remediation store.
3. Root README lists `requirements.txt`, absent from inspected tree.
4. Architecture document is a simple conceptual flow, not the five-layer CRISC target.
5. CI runs GRC Automation Lab tests only; Risk Register and SAP SoD tests are omitted.
6. CRISC artifacts were not present in inspected `main` tree at observed head. Confirm intended repository/branch/path before treating them as previously published there.

## Target gaps

| Area | Existing coverage | Next work |
|---|---|---|
| Organization/BusinessUnit/BusinessProcess | Partial labels/context | Stable IDs, scope, ownership |
| Asset/DataAsset | No shared inventory | Inventory, IDs, classification, owner |
| Risk/RiskAssessment | Starter register | Methodology versioning, inherent/residual risk, decisions |
| Requirement/Control/ControlAssessment | GRC controls/synthetic rules | Applicability and assessment period |
| Finding/Evidence/Remediation | Strongest in GRC Lab | Canonical IDs and cross-domain links |
| Vulnerability/Observation/ScannerSource | CSV dashboard only | Multi-scanner adapters/history |
| Supplier/Assessment/FourthParty | No dedicated implementation | TPRM inventory and CSRA |
| DLPEvent/PolicyViolation/Investigation | No dedicated implementation | Event/policy model |
| AI_System/AIUseCase/AIThreat | Governance README only | Inventory and separate AI security assurance |
| Metric/Observation/Threshold | Dashboard/analytics indicators | Shared dictionary, formulas, lineage, thresholds, owners |
| Decision/Approval/AuditEvent | Partial audit/remediation history | Cross-domain decision semantics |

## Mapping procedure and sequencing

For each table/CSV: inventory exact field names, types, nullability, keys and allowed values; map to canonical entity/attribute; define transformation/defaults; preserve raw values/source; assign confidence; record open questions; add positive/negative/boundary/migration tests; verify no existing records or behavior are lost.

- MAP-P0: inspect SQLite tables, migrations, CSV headers and fixtures.
- MAP-P1: field-level mappings for GRC Automation Lab and Risk Register.
- MAP-P2: scanner observation schema and sanitized OpenVAS/current Tenable CSV mapping.
- MAP-P3: map SAP SoD synthetic users/functions/rules/findings.
- MAP-P4: design TPRM, DLP, Data Governance, AI Security and ESG entities; do not create empty folders.
- MAP-P5: approve physical schema/migration only after backward-compatibility tests.

Do not replace code, CSVs, dashboards, SQLite migrations or tests as part of mapping. Add documentation first; any schema/code change must be isolated, tested, diff-reviewed and approved.

**Change log:** R0.1 records repository baseline, implementation boundaries, inconsistencies, gaps and mapping procedure.
