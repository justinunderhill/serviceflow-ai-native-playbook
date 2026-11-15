# CI and review governance

The GitHub Actions workflow runs on pushes and pull requests. Its single job,
`validate`, installs the locked dependencies, runs lint, runs the tests on the
oldest and newest supported Python versions, and fails on any application
resource leak.

**A workflow alone is not a merge gate.** `main` is protected by the active
"Main Branch Protection" ruleset, enabled on 15 November 2026:

- a pull request is required to change `main`;
- the `validate` check must pass on a branch that is up to date with `main`;
- review conversations must be resolved;
- force pushes and branch deletion are blocked;
- no actor may bypass the ruleset.

Required approving reviews are set to 0 because the repository has one
maintainer, and a maintainer cannot approve their own pull request. The human
decision is therefore recorded in each pull request's "Human decision record"
section (see `.github/pull_request_template.md`). An approval requirement can
be added once an independent reviewer is available.

**Do not rename the `validate` job.** The ruleset requires a check with that
exact name; renaming it, or turning it into a matrix, would block every merge.

Never use skip flags or `continue-on-error` to make a failed check appear
successful.
