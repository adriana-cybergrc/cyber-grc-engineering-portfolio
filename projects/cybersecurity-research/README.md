# Cybersecurity Research

**Status:** Active — research coordination  
**Portfolio:** [Cyber GRC Engineering](../../README.md)  
**Research program:** ISO/IEC 27090 — AI Security Research Program  
**Program governance:** [Notion research program](https://app.notion.com/p/418c04145c668173820ad66f7cc338c2)

## Purpose

This directory is the central catalog for independent cybersecurity research initiatives associated with the Cyber GRC Engineering portfolio.

It provides an executive-level view of research questions, scope, maturity, and repository locations. It is not the authoritative location for detailed scientific records: each independent research repository is intended to hold its own literature review, prior-art analysis, formal foundations, experimental protocols, code, results, and reproducibility materials.

Research coordination does not imply that a scientific contribution has been established or validated.

## Research Program — ISO/IEC 27090

**Program objective:** investigate scientific and engineering challenges in AI system security through independently assessable research tracks.

The program is organized into three priority research tracks and one cross-track investigation.

| ID | Research track | Core investigation | Research repository | Current status |
|---|---|---|---|---|
| R1 | AI Security Evidence Validity | Conditions under which security evidence remains valid after changes to AI models, data, configurations, and dependencies; selective revalidation | `ai-security-evidence-validity` — planned | Research charter defined; prior-art assessment pending |
| R2 | AI Model Provenance & Integrity | Verifiable continuity between model artifacts that are sourced, transformed, evaluated, and deployed | `ai-model-provenance-integrity` — planned | Research charter defined; prior-art assessment pending |
| R3 | AI Model–Infrastructure Security | Propagation of compromise across models, agents, tools, identities, APIs, connectors, and infrastructure | `ai-model-infrastructure-security` — planned | Research charter defined; prior-art assessment pending |
| R4 | Lifecycle Security Assurance | Whether security assurance can be preserved, invalidated, or selectively renewed across lifecycle changes | Cross-track investigation; no separate repository yet | Exploratory; independence not established |

### Research charters

- [R1 — AI Security Evidence Validity](https://app.notion.com/p/418c04145c6681d98e40de08552d5283)
- [R2 — AI Model Provenance & Integrity](https://app.notion.com/p/418c04145c668176a790f5e17417e9f6)
- [R3 — AI Model–Infrastructure Security](https://app.notion.com/p/418c04145c6681d08bf8ef4eb887f6cd)
- [R4 — Lifecycle Security Assurance](https://app.notion.com/p/418c04145c6681309df0d4b991cd8ceb)

## Research Method

Each track is expected to follow a common evidence-driven process:

1. Define the research problem, scope, research question, and falsifiable hypotheses.
2. Search and review relevant literature, standards, technical specifications, and competing approaches.
3. Build a traceable prior-art matrix covering problem, assumptions, definitions, formal results, methods, evidence, and limitations.
4. Identify the closest competing work and test whether the proposed contribution reduces to, or is already covered by, that work.
5. Formalize definitions, assumptions, properties, and candidate propositions before broad implementation.
6. Develop counterexamples and explicit rejection criteria.
7. Design reproducible experiments against credible baselines.
8. Record negative, inconclusive, and positive results with equal traceability.

## Scientific Maturity and Decision Gates

Research status must reflect evidence actually obtained.

| Status | Meaning |
|---|---|
| Proposed | Problem and candidate research direction have been articulated. |
| Under review | Literature, prior art, assumptions, and scope are being assessed. |
| Experimental | A defined model or prototype is being tested. |
| Validated | Stated claims have passed documented formal and/or empirical validation within explicit limits. |
| Rejected | Evidence shows the hypothesis is false, not novel, or not sufficiently distinguishable from prior work. |
| Inconclusive | Available evidence is insufficient to accept or reject the claim. |

A research track must not be described as original, novel, or validated solely because a literature search returned few results or because a prototype works.

The decision process uses explicit gates:

- **G0 — Scope:** bounded problem and terminology.
- **G1 — Prior art:** reproducible search and closest-work review.
- **G2 — Research gap:** demonstrable difference from existing methods.
- **G3 — Formalization:** explicit model, assumptions, and properties.
- **G4 — Falsification:** counterexamples and competing explanations assessed.
- **G5 — Feasibility:** data, implementation, and experimental design are viable.
- **G6 — Validation:** claims supported by reproducible results and stated limitations.

Originality and non-equivalence to prior art are mandatory conditions; strengths in other dimensions cannot compensate for failure on either condition.

## Repository and Artifact Governance

Each independent research repository should preserve:

- Research charter, questions, and hypotheses.
- Search protocol, bibliography, and prior-art matrix.
- Definitions, assumptions, propositions, and proofs or proof attempts.
- Experimental protocols, baselines, parameters, seeds, and environment.
- Source code, tests, logs, datasets or synthetic fixtures, and generated results.
- Threats to validity, limitations, negative findings, and decision records.
- Version history and reproducibility instructions.

The Cyber GRC Engineering repository remains the portfolio-level catalog. Detailed research artifacts belong in their respective research repositories to avoid divergent copies.

## Scope Boundaries

These research tracks are distinct from the portfolio's implementation projects, including GRC Automation Lab and AI Cyber Risk Governance. Research outputs may inform engineering projects in the future, but no implementation or governance control should be represented as scientifically validated merely because it references a research track.

R4 remains a cross-track investigation until it demonstrates an independent research question, formal object, prior-art gap, and validation path. A separate repository should be created only after that independence is established.

## Related Portfolio Resources

- [Cyber GRC Engineering — main README](../../README.md)
- [Cyber GRC Engineering Master Roadmap](../../docs/CYBER_GRC_ENGINEERING_MASTER_ROADMAP.md)
- [ISO/IEC 27090 — AI Security Research Program in Notion](https://app.notion.com/p/418c04145c668173820ad66f7cc338c2)

## Confidentiality and Responsible Research

Use public sources, synthetic data, or appropriately sanitized material. Do not publish employer, customer, supplier, personal, or production security information. Document source provenance, licensing constraints, assumptions, and limitations. Do not disclose vulnerabilities or sensitive implementation details without appropriate authorization and coordinated handling.
