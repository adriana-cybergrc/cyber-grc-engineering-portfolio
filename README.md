# Cyber GRC Engineering Portfolio

**Cyber GRC | SAP Security | SAP GRC | GRC Engineering | AI Governance**

A public portfolio of independent cybersecurity governance projects, reference architectures, control assessments, and small automation labs.

## Portfolio principles
- Risk-informed and business-aligned cybersecurity.
- Traceable controls, evidence, and decisions.
- Human accountability for risk acceptance and high-impact decisions.
- Reproducible examples using synthetic data only.
- No confidential company, customer, supplier, or production information.

## Featured labs

| Project | Focus | Status |
|---|---|---|
| [Cyber GRC Risk Register](projects/cyber-grc-risk-register/README.md) | Risk scenarios, scoring, CSV validation | Starter |
| [SAP Security Lab](projects/sap-security-lab/README.md) | Access governance and authorization concepts | Planned |
| [SAP GRC SoD Lab](projects/sap-grc-sod-lab/README.md) | Segregation of Duties and mitigation | Planned |
| [GRC Automation Lab](projects/grc-automation-lab/README.md) | Workflow automation and SLA monitoring | Planned |
| [AI Cyber Risk Governance](projects/ai-cyber-risk-governance/README.md) | AI risk controls and human oversight | Planned |
| [Cybersecurity Research](projects/cybersecurity-research/README.md) | Research notes and case studies | Planned |

## Quick start

Requirements: Python 3.11+ recommended and Git.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
python src/risk_register.py --input data/risk_register.csv
```

macOS/Linux:
```bash
source .venv/bin/activate
python src/risk_register.py --input data/risk_register.csv
```

The starter script uses only the Python standard library.

## Repository structure

```text
.
├── data/                 # Synthetic example data only
├── docs/                 # Architecture and contribution guidance
├── projects/             # Independent portfolio labs
├── src/                  # Reusable Python code
├── tests/                # Automated tests
├── .gitignore
├── README.md
└── requirements.txt
```

## Disclaimer

This repository is an independent educational portfolio. It is not affiliated with or endorsed by NIST, ISO, SAP, or any employer. Framework references are used for learning and mapping purposes; verify current official requirements before using them in a real assessment. No production security decisions should rely on this starter implementation without validation.

## Roadmap
- [x] Initial risk register validation and scoring example
- [ ] Add automated unit tests
- [ ] Add a synthetic SAP SoD rule matrix
- [ ] Add control-to-evidence traceability
- [ ] Add AI risk assessment example with human review gates
