# ServiceFlow requirements and acceptance criteria

ServiceFlow is a fictional request-approval service. The reference concentrates
on one bounded workflow, rather than modelling an entire enterprise service desk.

- SF-REQ-001: Authenticated employees can submit requests with title,
  description and an existing assigned manager.
- SF-REQ-002: A requester or assigned manager can view the request.
  Unrelated authenticated users must receive HTTP 403.
- SF-REQ-003: Only the assigned manager can approve a pending request.
  A requester must never self-approve, even when assigned as manager.
- SF-REQ-004: Repeated approval must fail with HTTP 409 and must not
  create a second approval audit event.
- SF-REQ-005: Request creation and approval create audit events that only
  involved actors can read.
- SF-REQ-006: Requests survive application process recreation via SQLite.

The reference must include positive and negative tests, including
other-manager denial, unauthenticated access, self-approval, duplicate approval,
unrelated read access and audit integrity. See SF-ADR-003.
