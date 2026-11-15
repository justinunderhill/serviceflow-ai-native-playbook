# SF-ADR-004: Resource existence disclosure and authorisation responses

**Status:** Accepted for educational use (SF-DEC-004A, SF-DEC-004B in work packet SF-WP-004).
**Decision owner:** Justin Underhill (human decision owner for ServiceFlow).
**Amends:** SF-ADR-003, item 4 (response code for non-participants).

## Context

Before this decision, request retrieval, audit retrieval and approval answered 404
for an unknown request ID but 403 for an existing request the caller was not part of.
Any authenticated user could therefore confirm that a given request ID exists. Random
UUIDs make guessing hard, but IDs can still leak through logs, links or screenshots,
and the playbook teaches that authorisation responses are part of the security design.

## Decision

A *participant* is the request's requester or its assigned manager.

| Scenario | Response |
|---|---|
| Unauthenticated actor | 401 |
| Nonexistent request | 404 `{"detail": "Request not found"}` |
| Authenticated non-participant, on read, audit or approve | 404, identical body to a nonexistent request |
| Requester attempting to approve their own request | 403 |
| Assigned manager approving a pending request | 200 |
| Assigned manager approving again | 409 |
| Creating a request assigned to oneself | 422 (SF-DEC-004B) |

Participants already know the request exists, so a 403 tells them nothing new and
keeps the error meaningful. Both cases are produced by one helper,
`load_for_participant`, so the three endpoints cannot drift apart.

Self-assignment is rejected at creation because such a request could never be
approved. The approval endpoint keeps its `who == requester` check as a defence
against rows created before this validation or by future defects.

## Consequences

- Non-participants cannot distinguish "exists but not yours" from "does not exist"
  by status or body. Response timing was not measured or equalised; the two paths
  run the same single-row lookup, but this is not a timing guarantee.
- Clients and operators see 404 for some authorisation failures, which can make
  support diagnosis harder; server-side logging would be the place to record the
  real reason (not implemented in this teaching reference).
- Tests that previously expected 403 for unrelated actors now expect 404.
  The playbook text describing the 403 for an unrelated manager must be updated.
- Rejected operations still change no state and write no audit event.

## Alternatives considered

- **Keep 403 for non-participants** and accept the existence oracle. Rejected by the
  decision owner: the playbook should demonstrate the stricter behaviour.
- **Return 404 to the requester as well.** Rejected: the requester can already see the
  request, so hiding it would only make the error misleading.
