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
