# Publishing and verification checklist

1. Check repository visibility, ownership and default branch.
2. Commit source, tests, agent guidance, ADR, threat model and CI workflow.
3. Verify the GitHub Actions run on the pushed commit.
4. Fix failing checks; never suppress or bypass lint/tests for a green badge.
5. Configure a main-branch ruleset with required checks and independent review,
   if supported by the GitHub plan and available reviewers.
6. Record whether the ruleset is **active**; a workflow is not branch protection.
7. Create a real scoped follow-up change as a pull request, capture commit,
   CI evidence and reviewer decision; do not invent an agent execution.
8. Update the book with the verified repository and concrete evidence links.

This is a demonstration, not a production security certification.
