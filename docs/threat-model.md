# Threat model and boundaries

Assets: requests, assigned-manager authority, request status, approval audit,
account credentials and repository integrity.

Risks and controls:
- Impersonation: passwords are checked server-side against salted PBKDF2 hashes
  in the local reference. HTTPS and an identity provider are still missing.
- Broken object-level authorisation: the API loads assignment from persisted
  request data and tests that unrelated actors are refused.
- Existence disclosure: non-participants receive the same 404 status and body
  for an existing request as for a missing one (SF-ADR-004). Response timing is
  not equalised or measured.
- Self-approval: self-assigned requests are rejected at creation (HTTP 422), and
  the approval endpoint keeps an explicit requester != actor check for legacy data.
- Duplicate writes: SQLite BEGIN IMMEDIATE and pending-status condition.
- Audit exposure: only request participants can fetch that request's events.
- Malicious agent behaviour: agent guidance is advisory; repository rulesets,
  branch protections, permissions and separate human review enforce controls.

Not addressed: account provisioning/recovery, expiry and revocation, production
secret management, TLS termination, rate limiting, CSRF/session security,
centralised audit, migrations, resilience and production threat modelling.

Never deploy the bundled demo app or its disposable passwords publicly.
