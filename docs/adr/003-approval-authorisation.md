# SF-ADR-003: Object-level approval authorisation

**Status:** Accepted for educational use; item 4 amended by
[SF-ADR-004](004-resource-existence-disclosure.md).
**Decision owner:** Fictional ServiceFlow team.

Authentication verifies identity but not the authority to approve a particular
request. A disabled UI button can be bypassed with a direct API call.

Decision:
1. Verify credentials server-side.
2. Read requester and assigned manager from persisted data, not the request body
   of an approval call.
3. Permit approval only when the authenticated actor equals the assigned
   manager and does not equal the requester.
4. Otherwise reject without changing state or adding approval audit: HTTP 404
   for non-participants (identical to a missing request) and HTTP 403 for a
   participant who is not the assigned manager, per SF-ADR-004.
5. Require pending state and perform the transition inside a SQLite write
   transaction, responding HTTP 409 for duplicate approval.
6. Verify with positive and negative automated tests.

Limitations: this educational Basic-auth demonstration is not an enterprise
identity solution and has no production-grade operational safeguards.
