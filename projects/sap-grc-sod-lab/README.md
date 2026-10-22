# SAP Security & SAP GRC — Segregation of Duties Lab

## Objective

Demonstrate automated identification of potential Segregation of Duties (SoD) conflicts using synthetic user access data and configurable business rules.

## Scope

- Synthetic user-to-function assignments
- Configurable SoD conflict rules
- Python-based conflict detection
- CSV findings report
- Automated unit tests

## Execution

Run from the repository root:

```powershell
python projects/sap-grc-sod-lab/src/sod_analyzer.py --users projects/sap-grc-sod-lab/data/users_roles.csv --rules projects/sap-grc-sod-lab/data/sod_rules.csv --output projects/sap-grc-sod-lab/sod_findings.csv
```

## Tests

```powershell
python -m unittest discover -s projects/sap-grc-sod-lab/tests -v
```

## Governance note

Findings are risk indicators that require review. They do not prove fraud or automatically establish a policy violation. Real-world use requires approved conflict rules, role semantics, business context, and assessment of compensating controls.

All data in this lab is synthetic.
# SAP GRC Segregation of Duties (SoD) Lab

**Status:** Planned

## Intended scope
- Synthetic business functions and conflicting permissions.
- Rule matrix for illustrative SoD conflicts.
- Risk severity, mitigating controls, and reviewer sign-off.
- Test cases for rule matching and false-positive review.

This is a learning lab, not a representation of SAP GRC Access Control configuration or an official SAP ruleset.
