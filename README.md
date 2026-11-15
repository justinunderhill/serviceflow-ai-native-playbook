# ServiceFlow — AI-Native Software Development Playbook companion

[![ServiceFlow checks](https://github.com/justinunderhill/serviceflow-ai-native-playbook/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/justinunderhill/serviceflow-ai-native-playbook/actions/workflows/ci.yml)

A small, runnable FastAPI service that accompanies *The AI-Native Software
Development Playbook* by [Justin Underhill](https://www.justinunderhill.com/).
It shows one rule in working code: **authentication is not authorisation**.
Only the assigned manager may approve a request, the requester may never
approve their own, and negative tests prove it.

It is an educational reference, not production software (see
[Limitations](#limitations)).

## Prerequisites

- Python 3.11 or newer (CI tests 3.11, 3.12 and 3.13)
- [uv](https://docs.astral.sh/uv/)

## Install and run

```bash
uv sync --locked --extra dev
uv run uvicorn serviceflow.demo:app --host 127.0.0.1 --reload
```

Open http://127.0.0.1:8000/docs. The disposable local users `alice`, `bob`
and `charlie` share the password `local-demo-only`. Never deploy them.

## Verify

```bash
uv run --locked --extra dev ruff check .
uv run --locked --extra dev python -X dev -m pytest -q
```

Tests fail on any resource leak, such as an unclosed database connection.
The same checks run in CI as the required `validate` check.

## Behaviour

| Situation | Response |
|---|---|
| Not signed in | 401 |
| Request does not exist, or caller is not involved | 404 (identical) |
| Requester tries to approve their own request | 403 |
| Assigned manager approves a pending request | 200 |
| Approving again | 409 |
| Assigning a request to yourself | 422 |

## Design and evidence

- [Requirements](docs/requirements.md) and [threat model](docs/threat-model.md)
- Decisions: [SF-ADR-003](docs/adr/003-approval-authorisation.md) (approval
  authorisation), [SF-ADR-004](docs/adr/004-resource-existence-disclosure.md)
  (existence disclosure)
- Work packets: [SF-WP-004](docs/work-packets/sf-wp-004.md),
  [SF-WP-005](docs/work-packets/sf-wp-005.md); SF-WP-004 evidence is in
  [PR #3](https://github.com/justinunderhill/serviceflow-ai-native-playbook/pull/3)
- Working with coding agents: [AGENTS.md](AGENTS.md),
  [agent setup](docs/coding-agent-setup.md), [CI governance](docs/ci-governance.md)
- [Release notes](docs/releases/v1.0.0.md) and [release checklist](docs/release-checklist.md)

## Limitations

Local HTTP Basic authentication over plain HTTP, disposable demo accounts and
single-process SQLite. There is no identity provider, TLS, rate limiting,
account lifecycle, central audit store, migrations or monitoring, and response
timing is not equalised. Run it on localhost only. Agent instructions guide
behaviour but enforce nothing; the API, tests, CI and branch rules do.

## Licence

Code: [MIT](LICENSE). The book, the author's portrait and brand assets are not
part of this repository or its licence.
