# ServiceFlow Engineering Work Packet: SF-WP-005

**Title:** First Edition Release Readiness, Reproducibility and Repository Governance

**Repository:** https://github.com/justinunderhill/serviceflow-ai-native-playbook

**Status:** Approved for implementation, subject to final human review and release authorisation

**Implementation agent:** Claude Code

**Business and release owner:** Justin Underhill

**Technical reviewer:** ChatGPT (AI-assisted review)

**Release target:** v1.0.0 — ServiceFlow Companion: First Edition

## 1. Objective

Prepare the ServiceFlow companion repository for its first formal public release.

The release must be reproducible, technically verified, clearly documented and consistent with the AI-native engineering principles demonstrated in the accompanying book.

SF-WP-005 follows the successful completion and merge of SF-WP-004.

The scope is repository release readiness. It does not include modifying or publishing the book or developing Justin Underhill's website.

## 2. Publication decisions

The accompanying book, *The AI-Native Software Development Playbook*, will be published as a browser-readable publication on Justin Underhill's personal website:

https://www.justinunderhill.com/

A dedicated page, provisionally `/ai-native-playbook`, is planned. Its final URL has not yet been confirmed.

**Book distribution requirements:**

- The book will be readable directly on the website.
- No PDF, DOCX, EPUB or other complete-book download will be offered at launch.
- The complete book must not be committed to the public ServiceFlow repository.
- The author's personal photograph and publication design assets must not be included in the MIT-licensed software.
- The book retains separate copyright and distribution terms.
- The public repository may contain links to the future book page, but must not advertise an unpublished URL as live.
- The ServiceFlow companion code remains publicly accessible under the existing MIT licence.

The book's website publication is a separate workstream and is not a prerequisite for this repository release.

## 3. Approved scope

### Task A: Repository cleanup

Review the current repository against SF-WP-004's learning report.

Required actions:

1. Identify and close stale draft PR #1 as superseded by merged PR #3. Leave a factual closure comment referencing PR #3, SF-ADR-004 and the changed 403/404 behaviour.
2. Remove `docs/publishing-github.md`, which contains completed internal publishing instructions.
3. Remove the unattributed multi-agent handout reference from `docs/coding-agent-setup.md`.
4. Retain the useful, vendor-neutral agent portability guidance.
5. Add build artefacts such as `*.egg-info/` to `.gitignore`.
6. Review the README for obsolete statements, duplication and excessive disclaimers.
7. Preserve necessary security and educational limitations.

Do not erase historical evidence, rewrite completed commits or remove the SF-WP-004 work packet.

### Task B: Dependency reproducibility

The repository currently uses `uv` without a committed lockfile.

Required actions:

1. Generate and commit `uv.lock` using the existing dependency definitions.
2. Ensure compatibility with the repository's supported Python versions.
3. Update CI to install dependencies using frozen/locked resolution, failing when the lockfile is inconsistent.
4. Document the supported Python version range.
5. Keep dependencies appropriately scoped.
6. Investigate existing third-party deprecation warnings, but do not introduce unrelated framework upgrades merely to silence them.

**Acceptance criteria:**

- A clean checkout can install the locked environment.
- Local development and CI use consistent dependency resolution.
- Existing tests pass.
- Ruff passes.
- No unapproved application behaviour changes are introduced.

### Task C: Automated quality safeguards

Strengthen verification so previously identified issues are less likely to recur.

Required actions:

1. Add a repeatable check for unclosed SQLite connections.
2. Include suitable Python development-mode or `ResourceWarning` validation.
3. Distinguish application resource warnings from pre-existing third-party deprecation warnings.
4. Avoid blanket warning suppression.
5. Update GitHub Actions dependencies to currently supported versions after verifying their compatibility and security implications.
6. Preserve minimal workflow permissions.
7. Keep the required GitHub status check named `validate`.

**Acceptance criteria:**

- All 19 existing tests continue to pass.
- Resource-warning verification passes without masking application leaks.
- Ruff passes.
- GitHub Actions succeeds on the pull request.
- Branch protection continues recognising the required `validate` check.

Do not rename the CI job without explicit approval because the active GitHub ruleset depends on its name.

### Task D: Version and release preparation

Prepare the first stable public companion release.

Required actions:

1. Update project version metadata from `0.3.0` to `1.0.0`.
2. Ensure application and package versions are consistent.
3. Create concise release notes describing the functionality, tests, architecture and educational limitations.
4. Add a release checklist and verification evidence.
5. Review the MIT licence and its explicit exclusion of the independent book and brand assets.
6. Confirm that no credentials, local databases, personal material or sensitive session information are included.
7. Prepare a release description titled:

   **ServiceFlow Companion — First Edition**

**Important:** Do not create or publish the `v1.0.0` Git tag or GitHub Release before the pull request has been reviewed and merged.

The release must point to the verified merge commit on `main`, not an unmerged development branch.

### Task E: Public repository presentation

Improve the repository's usability without making it promotional or unnecessarily verbose.

Required actions:

1. Add a GitHub Actions status badge to the README.
2. Keep the README concise, explaining the purpose, prerequisites, installation, verification and limitations.
3. Link clearly to requirements, architecture decisions, threat model, work packets and the SF-WP-004 evidence.
4. Suggest suitable GitHub repository topics.
5. Add a link to the personal website where appropriate.
6. Do not link to the proposed book URL until it is live.
7. Avoid presenting the demonstration as production-ready.

Suggested repository topics:

`ai-native-development`, `coding-agents`, `software-engineering`, `fastapi`, `application-security`, `ai-sdlc`

### Task F: Auditability of human decisions

The SF-WP-004 learning report identified an incomplete GitHub audit trail for the human merge decision.

Required actions:

1. Preserve the distinction between Claude Code implementation, AI-assisted review and human release approval.
2. Prepare a factual, retrospective comment for PR #3, explaining that Justin explicitly authorised the merge through ChatGPT before it was performed.
3. Clearly identify the comment as retrospective.
4. Do not fabricate an earlier GitHub approval or present an AI-assisted review as an independent human review.
5. Establish a standard PR template that includes an explicit human decision record for future changes.

A future approving-review requirement may be considered once an eligible independent reviewer is available. Do not modify the existing required approval count in this work packet.

## 4. Existing governance controls

The repository currently has an active **Main Branch Protection** ruleset.

Its verified configuration includes:

- Target: default branch (`main`)
- Pull request required before merging
- Required `validate` status check
- Required checks must be up to date
- Review conversations must be resolved
- Force pushes prohibited
- Branch deletion prohibited
- No bypass actors
- Required approving reviews: 0

Preserve these controls.

Do not disable, weaken or bypass them to complete the work.

## 5. Scope exclusions

The following are not authorised:

- Changing the application's approved 404/403 policy
- Altering approval business rules
- Rewriting SF-WP-004 history
- Disabling tests or CI checks
- Replacing the application architecture
- Adding unrelated features
- Publishing the book or building its website
- Uploading book files to GitHub
- Publishing a release before final approval
- Modifying GitHub branch-protection rules

Escalate any necessary deviation before implementing it.

## 6. Development process

Follow the AI-native engineering workflow documented in the repository:

1. Fetch the current protected `main` branch.
2. Record the exact baseline commit SHA.
3. Create a dedicated `sf-wp-005-release-readiness` branch.
4. Inspect the repository and reproduce any issues being addressed.
5. Implement changes in logically separated commits.
6. Run complete local tests, lint and resource-warning checks.
7. Verify the locked dependency environment from a clean installation.
8. Review the full diff for scope compliance and accidental disclosure.
9. Open a pull request against `main`.
10. Record actual GitHub Actions evidence.
11. Request technical and human review.
12. Stop before merging or tagging the release.

Do not report tests or actions as completed unless they were actually executed.

## 7. Pull request evidence requirements

The pull request must include:

- Baseline and final commit SHAs
- A summary of the completed tasks
- Files changed and reasons
- Dependency lockfile verification
- Python version used
- Test results
- Ruff results
- Resource-warning verification
- GitHub Actions run URL
- Security and licence checks
- Remaining limitations
- The genuine Claude Code session reference, if safe to share
- Explicit confirmation that no release tag has been published

The PR must remain open and unmerged for ChatGPT's technical review and Justin Underhill's final authorisation.

## 8. Definition of Done

SF-WP-005 is ready for human approval when:

- Repository documentation is suitable for public use.
- Superseded draft PR #1 has been closed with an accurate explanation.
- Dependency installation is reproducible.
- All automated tests and lint checks pass.
- Resource-management verification succeeds.
- GitHub Actions passes using the protected `validate` check.
- Application and package versions are consistent at 1.0.0.
- Release notes are prepared.
- No book manuscript or excluded brand assets are published in the repository.
- The review record distinguishes AI work from human decisions.
- No unrelated changes have been introduced.

## 9. Post-merge release procedure

These steps require separate approval after the implementation PR has passed review:

1. Merge the reviewed PR into `main`.
2. Verify GitHub Actions succeeds on the merge commit.
3. Create the annotated `v1.0.0` tag on that verified commit.
4. Publish the GitHub Release using the prepared release notes.
5. Verify the public release page, tag and source contents.
6. Record the release URL and immutable commit SHA.
7. Update the ServiceFlow learning report with the release outcome.

Only after those steps should the book's final edition reference ServiceFlow v1.0.0 as the verified companion release.

## 10. Final instruction

Implement SF-WP-005 on a dedicated branch and open a fully documented pull request.

Do not merge, tag or publish the release.

Stop at the review gate and provide the pull request URL, CI evidence and any outstanding decisions.
