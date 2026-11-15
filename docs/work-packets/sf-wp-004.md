# ServiceFlow Engineering Work Packet: SF-WP-004

**Title:** Database Resource Management, Authorisation Disclosure and Workflow Validation

**Repository:** https://github.com/justinunderhill/serviceflow-ai-native-playbook

**Status:** Approved for implementation

**Implementation agent:** Claude Code

**Human decision owner:** Justin Underhill

**Technical review:** ChatGPT, with final human approval by Justin Underhill

## 1. Objective

Resolve three identified engineering defects while preserving ServiceFlow's existing security guarantees and providing a verifiable, evidence-backed development record.

This work should demonstrate the AI-native delivery principles described in the accompanying playbook.

## 2. Approved business and security decisions

### SF-DEC-004A: Resource existence disclosure

Unauthorised users must not be able to distinguish an existing request they are not permitted to discover from a nonexistent request through HTTP response status or body.

Implement these rules consistently:

| Scenario | Expected HTTP status |
|---|---|
| Unauthenticated actor | 401 |
| Nonexistent request | 404 |
| Unrelated authenticated actor accessing request, audit or approval endpoint | 404 |
| Requester attempting to approve their own existing request | 403 |
| Assigned manager approving pending request | 200 |
| Repeated approval by assigned manager | 409 |

For unrelated users, the response body must match the response for a nonexistent request.

Create **SF-ADR-004: Resource Existence Disclosure and Authorisation Responses**, documenting the reasoning, affected endpoints, trade-offs and expected behaviour.

Retain SF-ADR-003 and update its cross-references where necessary.

The implementation must not weaken authentication or object-level authorisation.

### SF-DEC-004B: Self-assignment

The system must reject creation of a request when the assigned manager is the requester.

Return HTTP 422.

Retain the existing defensive self-approval check in the approval endpoint to protect against invalid legacy data or future implementation errors.

## 3. Engineering tasks

### Task A: SQLite connection lifecycle

**Problem:** Database connections are not explicitly closed.

**Required change:**
- Ensure database connections are closed on all execution paths, including exceptions.
- Preserve existing transaction guarantees.
- Do not weaken atomic approval behaviour.
- Prefer a consistent connection-management abstraction.

**Acceptance criteria:**
- Existing tests pass.
- No unclosed SQLite connection warnings when tests execute in Python development mode.
- Transactions preserve correct rollback behaviour on errors.
- Connection cleanup is demonstrably verified.

### Task B: Resource existence disclosure

**Problem:** Unrelated users can distinguish existing from nonexistent request identifiers through API responses.

**Required change:**
- Apply SF-DEC-004A consistently to request retrieval, audit retrieval and approval.
- Preserve the different responses for authenticated participants where appropriate.
- Ensure rejected operations do not change request state or create approval audit events.
- Rename any tests whose names misrepresent their assertions.

**Acceptance criteria:**
- Negative tests verify all three affected endpoints.
- Responses to unrelated users do not disclose resource existence through status or body.
- Existing positive authorisation behaviour remains correct.
- Audit integrity remains intact.

### Task C: Invalid self-assignment

**Problem:** The system accepts requests that cannot complete their approval workflow.

**Required change:**
- Reject requester/assigned-manager equality during creation.
- Return 422.
- Preserve the approval endpoint's defensive self-approval check.

**Acceptance criteria:**
- A self-assigned request cannot be created.
- Failed creation produces no request or audit record.
- Existing valid request creation and approval workflows continue to work.
- A regression test confirms the defensive approval check still functions for legacy invalid data.

## 4. Scope boundaries

**Permitted:**
- Application code relevant to these defects
- Automated tests
- SF-ADR-004 and necessary updates to SF-ADR-003
- Work-packet evidence and directly related documentation

**Not permitted without separate approval:**
- Disabling or bypassing tests
- Weakening authentication or authorisation
- Changing unrelated application features
- Changing deployment configuration
- Introducing unnecessary dependencies
- Modifying branch protection or CI requirements
- Merging into `main`

Investigate root causes before implementing fixes. Keep the changes focused.

## 5. Development workflow

1. Create a dedicated feature branch from the latest `main`.
2. Record the baseline commit SHA.
3. Reproduce and document the defects.
4. Add or update failing regression tests.
5. Implement the minimum necessary corrections.
6. Run the complete test suite and lint checks using the repository's `uv` conventions.
7. Verify connection warnings in Python development mode.
8. Review the diff for unrelated changes and security regressions.
9. Open a GitHub pull request against `main`.
10. Record the actual test output, commit references, GitHub Actions results and remaining limitations.

Do not manufacture evidence or report commands as executed unless they were actually run.

## 6. Pull request requirements

Include:

- Summary of each defect and its root cause
- Business/security decisions implemented
- Files changed and rationale
- Regression tests added
- Local test and lint evidence
- GitHub Actions evidence
- SF-ADR-004 reference
- Known limitations and residual risks
- Link to the genuine Claude Code development session, if sharing is enabled and the session has been checked for secrets
- Explicit request for human review

Keep the pull request unmerged.

## 7. Definition of Done

The implementation is ready for review when:

- All acceptance criteria are satisfied.
- All existing and newly added tests pass.
- Lint checks pass.
- GitHub Actions checks succeed.
- No unclosed database-connection warnings remain.
- Changes are traceable to the approved work packet.
- Architecture decisions reflect the implemented behaviour.
- The pull request contains sufficient evidence for independent technical inspection.

**Passing CI does not constitute human approval.**

## 8. Learning report

After implementation and review, produce a concise learning report covering:

- The original engineering problems
- Human-owned decisions versus agent-made implementation choices
- Root causes and corrections
- Testing and verification evidence
- Review findings and resulting amendments
- Lessons for AI-native engineering workflows

Use verified session records, commits and CI artifacts.

This report may inform a future ServiceFlow case-study update in *The AI-Native Software Development Playbook*.

**Final instruction:** Implement the approved scope, provide verifiable evidence, and stop at the pull-request stage for review. Do not merge or release.
