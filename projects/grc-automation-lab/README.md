# GRC Automation Lab — Control Assurance & Evidence Monitoring

## Overview

A Python-based Governance, Risk and Compliance (GRC) automation lab that evaluates synthetic control records, evidence validity and remediation deadlines.

The solution identifies potential control exceptions and produces a structured CSV report to support auditability and risk-based decision-making.

## Objectives

- Automate control evidence validation.
- Identify missing, pending and expired evidence.
- Detect overdue remediation tasks.
- Generate structured findings for review.
- Validate business rules through automated unit tests.

## Architecture

- `data/controls.csv` — control inventory and evidence requirements.
- `data/evidence.csv` — evidence records and validity dates.
- `data/tasks.csv` — remediation activities and deadlines.
- `src/grc_automation.py` — evaluation engine.
- `tests/test_grc_automation.py` — automated unit tests.
- `grc_findings.csv` — generated exception report.

## Execution

Run from the repository root:

```powershell
python projects/grc-automation-lab/src/grc_automation.py
```

The program evaluates the control inventory and generates `grc_findings.csv`.

## Automated tests

```powershell
python -m unittest discover -s projects/grc-automation-lab/tests -v
```

The current test suite validates expired evidence, overdue tasks, missing evidence and a scenario with valid evidence and a completed task.

## Example finding types

| Finding | Description |
|---|---|
| `MISSING_EVIDENCE` | No evidence record exists for an active control. |
| `EVIDENCE_NOT_SUBMITTED` | Evidence is pending or has not been submitted. |
| `EVIDENCE_EXPIRED` | Submitted evidence is past its expiry date. |
| `SLA_OVERDUE` | An incomplete task has passed its due date. |
| `EXPIRY_DATE_MISSING` | Submitted evidence has no expiry date. |

## Governance and limitations

Findings are indicators requiring validation, not automatic declarations of non-compliance. The current prototype uses simplified rules and synthetic data.

Production implementation would require approved control applicability, evidence acceptance criteria, SLA definitions, exception ownership, audit logging and human review.

## Data protection

All records are synthetic. No confidential corporate data, production evidence or real user information is included.

## Roadmap

- Add configurable severity and SLA rules.
- Add persistent audit logging.
- Introduce evidence acceptance criteria.
- Add exception aging and ownership.
- Integrate with approved GRC workflows through controlled interfaces.

## Skills demonstrated

GRC Engineering · Control Assurance · Evidence Management · SLA Monitoring · Python · CSV Data Processing · Automated Testing · Auditability