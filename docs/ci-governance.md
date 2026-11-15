# CI and review governance

The GitHub Actions workflow runs lint and tests on pushes and pull requests.

**A workflow alone is not a merge gate.** A maintainer should configure a
ruleset for the default branch that requires the `validate` check and
independent pull-request review where account plan/features permit.
Do not require self-approval; a repository owner cannot independently
approve their own changes.

Check required status names after the first hosted workflow run.
If rulesets or required review cannot be enabled, document the limitation
rather than claim branch protection is active. Never use skip flags or
`continue-on-error` to make a failed check appear successful.
