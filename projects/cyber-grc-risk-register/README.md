# Cyber GRC Risk Register

## Objective
Demonstrate how a structured risk register can be validated and scored consistently using synthetic cybersecurity scenarios.

## Included
- Synthetic CSV risk register.
- Python validation for mandatory fields, duplicate IDs, and score ranges.
- Illustrative probability × impact scoring and risk bands.

## Run
From the repository root:

```powershell
python src/risk_register.py --input data/risk_register.csv
```

Run tests:
```powershell
python -m unittest discover -s tests -v
```

## Important limitations
The scoring bands are illustrative, not a calibrated risk methodology. The example does not calculate residual risk, determine risk appetite, or accept risk. Those decisions require an approved methodology and an accountable human decision-maker.
