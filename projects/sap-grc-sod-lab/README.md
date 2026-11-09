# SAP Security & SAP GRC — Segregation of Duties Lab

**Status:** Implemented prototype — synthetic data only  
**Maturity:** Rule-based conflict detection with unit tests; not production SAP integration.

## Objective

Demonstrate identification of potential SoD conflicts using synthetic user access data and configurable business rules.

## Implemented scope

- Synthetic user-to-business-function assignments.
- Configurable SoD conflict rules in CSV.
- Python conflict detection.
- CSV findings with `REQUIRES_REVIEW`.
- Unit tests for conflict and non-conflict scenarios.

## Repository structure

- `data/users_roles.csv` — synthetic user/function assignments.
- `data/sod_rules.csv` — illustrative conflict matrix.
- `src/sod_analyzer.py` — analyzer.
- `tests/test_sod_analyzer.py` — automated tests.
- `sod_findings.csv` — sample output.

## Execution

```powershell
python projects/sap-grc-sod-lab/src/sod_analyzer.py --users projects/sap-grc-sod-lab/data/users_roles.csv --rules projects/sap-grc-sod-lab/data/sod_rules.csv --output projects/sap-grc-sod-lab/sod_findings.csv
```

## Tests

```powershell
python -m unittest discover -s projects/sap-grc-sod-lab/tests -v
```

## Governance and limitations

Findings are indicators requiring review; they do not prove fraud or automatically establish a policy violation. Real-world use requires approved rules, role semantics, business context, compensating-control assessment, ownership and reviewer sign-off.

This lab does not connect to SAP systems, represent SAP GRC Access Control configuration, use an official SAP ruleset or automate mitigation approval. All data is synthetic.
