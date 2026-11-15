# Example bounded work packet

**Goal:** Verify request approval cannot be performed by another authenticated
manager or by the requester.

**Required context:** SF-REQ-003, SF-ADR-003, serviceflow/app.py,
tests/test_approval.py and threat model.

**Allowed changes:** App and tests only on a separate review branch.
No permission, CI, deployment or credential changes.

**Acceptance evidence:** A negative authorisation test returns 403 without
changing pending state, the assigned manager succeeds, and all tests pass.

**Completion:** List changed files, tests actually run, outcomes, assumptions,
risk and approval needed. Do not claim agent autonomy without a real record.
