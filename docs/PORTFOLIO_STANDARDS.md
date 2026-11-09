# Portfolio Standards

## Definition of done
Every project should contain:
1. Problem statement and intended audience.
2. Scope, assumptions, and explicit limitations.
3. Architecture or process flow.
4. Synthetic data or safe reproducible examples.
5. Validation steps and tests where applicable.
6. Risks, human approval points, and audit trail considerations.
7. References to authoritative public sources.

## Security and privacy rules
- Never commit secrets, tokens, passwords, private keys, or production connection strings.
- Never publish internal audit evidence, company policies, supplier details, personal data, or proprietary diagrams without written authorization.
- Use synthetic identifiers and fictional organizations.
- Review `git diff` before every commit.
- If a secret is committed, revoke/rotate it immediately; deleting it in a later commit does not make it safe.

## Documentation language
Use English for the main README and technical documentation to make the portfolio accessible internationally. Keep a Portuguese summary when it adds value.


## Artifact traceability and maturity

- Assign stable IDs and versions to architecture, data-model and mapping artifacts.
- Preserve prior versions and maintain a change log.
- Link related artifacts and evidence for implementation claims.
- Distinguish Conceptual, Planned, In Progress, Implemented and Validated.
- Implemented means functionality exists in the repository; Validated requires executed tests or verification evidence for the stated scope.
- A roadmap item, diagram or connector specification is not an implementation.

## Non-destructive repository changes

- Inventory files before editing; prefer additive, reviewable diffs.
- Do not replace code, datasets, dashboards, schemas or tests without migration and regression plan.
- Keep existing demonstrations runnable.
- Review complete diff, run tests and record results before merge.
- Do not merge a draft PR without explicit approval.
