# ServiceFlow | AI-Native Software Development Playbook companion

**An educational, runnable reference** for the fictional request-approval workflow discussed in *The AI-Native Software Development Playbook* by Justin Underhill (First Edition, November 2026).

The core rule: **authentication is not authorisation**. Only the assigned manager may approve a request, and the requester may not approve their own request. Negative tests enforce this rule.

## Run locally

Use Python 3.11+. Install using `uv sync --extra dev`, then start the local-only demo:

```bash
uv run uvicorn serviceflow.demo:app --host 127.0.0.1 --reload
```

Open http://127.0.0.1:8000/docs. Disposable demo users `alice`, `bob`, and `charlie` all have password `local-demo-only`. Never deploy these credentials.

```bash
uv run pytest -q
uv run ruff check .
```

## What is included

- FastAPI request creation, retrieval, assigned-manager approval, and restricted audit viewing.
- PBKDF2-hashed demo credentials with HTTP Basic authentication (local demonstration only).
- SQLite persistence and atomic approval operations.
- Positive and negative authorisation tests and a GitHub Actions workflow.
- Shared agent instructions in [AGENTS.md](AGENTS.md), [requirements](docs/requirements.md), [ADR SF-ADR-003](docs/adr/003-approval-authorisation.md), [threat model](docs/threat-model.md), [agent setup](docs/coding-agent-setup.md), and [PR evidence template](docs/example-pr-evidence.md).

## Critical limitations

This is **not production ready**. HTTP Basic requires TLS over a network; the app lacks real identity-provider integration, password recovery, rate limits, account lifecycle, distributed audit, production operations and resilience safeguards. Do not expose `serviceflow.demo` publicly. An agent's instructions do not enforce access control: API checks, tests, CI and GitHub rulesets must do that.

The sample PR evidence document is illustrative, **not a recorded autonomous-agent session**. No production performance claims are made.

The code is licensed under MIT. The book, portrait and brand assets are excluded from that licence.
