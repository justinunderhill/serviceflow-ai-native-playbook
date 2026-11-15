# Release checklist

Use this for every tagged release. Each line needs evidence a reviewer can
check: a command output, a CI run URL or a commit SHA. The v1.0.0 evidence
is recorded in the SF-WP-005 pull request.

## Before merging the release pull request

- [ ] Work packet approved and committed under `docs/work-packets/`
- [ ] `uv lock --check` passes; CI installs with `uv sync --locked`
- [ ] Clean clone installs the locked environment and passes all tests
- [ ] `ruff check .` passes
- [ ] Tests pass on Python 3.11, 3.12 and 3.13 in development mode,
      with no `ResourceWarning`
- [ ] `validate` check passes on the pull request
- [ ] Version agrees in `pyproject.toml`, `serviceflow.__version__` and the
      API (`tests/test_version.py`)
- [ ] Release notes written under `docs/releases/`
- [ ] No credentials, tokens, `.env` files, databases, personal material,
      book files or brand images are tracked (`git ls-files`)
- [ ] Diff reviewed for scope; AI work, AI review and the human decision
      are recorded separately in the pull request
- [ ] Human decision owner approves the merge in the pull request's
      "Human decision record"

## After merging (separately authorised)

- [ ] `validate` passes on the merge commit on `main`
- [ ] Annotated tag created on that verified merge commit
      (`git tag -a vX.Y.Z <sha>`), never on a branch
- [ ] GitHub Release published from the tag using the release notes
- [ ] Release page, tag and source archive checked
- [ ] Release URL and commit SHA recorded in the learning report
