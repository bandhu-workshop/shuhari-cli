# GitHub workflow and branch protection

Solo-developer workflow for this repository:

- All changes land on `main` via pull request — no direct pushes.
- 0 approvals required (solo maintainer); CI (`.github/workflows/ci.yml`,
  mirroring `just ci`) is the actual merge gate.
- Squash-merge only. The PR title becomes the squash commit message on
  `main` — write it as a proper commit message (e.g.
  `feat: add hello command`).
- Branch names: `feat/…`, `fix/…`, `refactor/…`, `docs/…`, `chore/…`.
- Never add a `Co-Authored-By: Claude …` (or any AI) trailer to commit
  messages, and never mention Claude/AI authorship in commits or PR
  descriptions. Claude/AI must never appear as a GitHub contributor on this
  repo — commit authorship stays solely with the human developer.
- Use the `git`/`gh` CLI for all GitHub operations.

## Suggested GitHub branch protection settings for `main`

- Require a pull request before merging (0 required approvals).
- Require status checks to pass before merging (the `ci` job).
- Require branches to be up to date before merging.
- Restrict force pushes and deletions.
