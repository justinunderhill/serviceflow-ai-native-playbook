# Portable coding-agent setup

The shared project contract lives in AGENTS.md. CLAUDE.md is a short
Claude Code adapter. Codex and other agents can use AGENTS.md where supported;
check current official documentation for tool/version-specific discovery,
permission and MCP configuration.

No universal instruction filename is a security boundary. Keep tool access
least-privileged and enforce authorisation in the application, CI and GitHub
repository settings.

## Evidence-first exercise

1. Read requirements, SF-ADR-003 and AGENTS.md.
2. Reproduce the issue or define an acceptance test, including a negative case.
3. Change only files authorised by a scoped work packet.
4. Run `uv run --extra dev pytest -q` and `uv run --extra dev ruff check .`.
5. Report actual outputs, changed paths, residual risk and review request.
6. Independently confirm tests in hosted CI and obtain human review.

Avoid committing personal configuration, broad agent tool allowlists, secrets
or speculative tool commands. The supporting multi-agent handout is a
time-sensitive operational reference, not a substitute for official manuals.
