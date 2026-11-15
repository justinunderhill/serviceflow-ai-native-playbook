# ServiceFlow requirements and acceptance criteria

ServiceFlow is a fictional request-approval service. The reference concentrates
on one bounded workflow, rather than modelling an entire enterprise service desk.

- SF-REQ-001: Authenticated employees can submit requests with title,
  description and an existing assigned manager other than themselves
  (self-assignment returns HTTP 422).
- SF-REQ-002: A requester or assigned manager can view the request.
  Unrelated authenticated users must receive HTTP 404, identical to the
  response for a nonexistent request (SF-ADR-004).
- SF-REQ-003: Only the assigned manager can approve a pending request.
  A requester must never self-approve (HTTP 403), including legacy rows
  where they are also the assigned manager. Unrelated users receive HTTP 404.
- SF-REQ-004: Repeated approval must fail with HTTP 409 and must not
  create a second approval audit event.
- SF-REQ-005: Request creation and approval create audit events that only
  involved actors can read.
- SF-REQ-006: Requests survive application process recreation via SQLite.

The reference must include positive and negative tests, including
other-manager denial, unauthenticated access, self-approval, duplicate approval,
unrelated read access, existence non-disclosure, self-assignment and audit
integrity. See SF-ADR-003 and SF-ADR-004.
