# ServiceFlow contributor instructions

This file guides agents; it does **not** grant privileges or enforce security.
Read the README, requirements, SF-ADR-003, threat model and work packet before
making changes.

- Python 3.11+, FastAPI application factory and SQLite demonstration.
- Use uv: `uv sync --extra dev`, `uv run --extra dev pytest -q`,
  `uv run --extra dev ruff check .`
- Work within an approved work packet on a separate branch.
- Reproduce problems, identify the root cause, write negative tests, then fix.
- Never trust identity supplied in request bodies or unauthenticated headers.
- Only a persisted assigned manager can approve; requesters cannot self-approve.
- Never remove or skip tests, disable CI, or weaken authorisation to make checks pass.
- Do not commit credentials, tokens, database files, customer data or caches.
- No external API calls or deployment without explicit human approval.
- Report changed files, requirements, commands actually run, outcomes, limitations,
  residual risks and required human review. Do not fabricate test or agent-session logs.
- Keep explanations straightforward and README concise.

A successful agent response does not replace independent test evidence or review.
