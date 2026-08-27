# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

`shuhari-cli` is a **learn-by-building CLI project**, not a product with
external users. It follows
[`docs/00_roadmap/agent-engineering-self-study-roadmap.md`](docs/00_roadmap/agent-engineering-self-study-roadmap.md),
a self-study curriculum for agent engineering. The goal is to understand
how the Claude and OpenAI APIs actually work — request/response payloads,
tool calling, streaming, context/token accounting, evaluation — by building
real code and measuring it, not by reading about it.

Scope decision (see
[`docs/architecture-decisions/0001-cli-only-raw-sdk-first.md`](docs/architecture-decisions/0001-cli-only-raw-sdk-first.md)
for full rationale):

- **CLI only.** The roadmap's own product target is a FastAPI + React web
  app; this project deliberately builds only the CLI, never that web shell.
- **Raw provider SDKs first.** Per the roadmap's R0 step, start with the
  `anthropic` and `openai` SDKs directly, before any agent framework
  (Google ADK, per the roadmap, comes much later — it is not a dependency
  yet).
- **Grow the tree one phase at a time.** Do not pre-create the roadmap's
  full target repository shape (section 6). Add a new top-level package
  only when the roadmap phase that needs it is actually being worked on.

When in doubt about what to build next, check the roadmap's "Final study
order" (section 45) and don't skip ahead.

## Tech Stack

- Python 3.12, managed with `uv`
- Typer (CLI)
- `anthropic`, `openai` (raw provider SDKs — Phase 1)
- Pydantic / pydantic-settings
- Tooling: ruff (lint/format), mypy (types), pytest (tests)

Frameworks/infra intentionally **not** present yet, per the scope decision
above: FastAPI, React, PostgreSQL, Docker Compose, Google ADK. Add any of
these only when a specific roadmap phase requires it, and record that as a
new ADR.

## Project Structure

### `src/shuhari_cli/`

```
src/shuhari_cli/
├── core/                 # Cross-cutting concerns
│   ├── config.py             # Settings (env-driven)
│   ├── logging.py            # setup_logging()
│   └── exceptions.py         # AppError hierarchy + handle_app_error()
└── cli/                  # CLI entry point
    ├── main.py               # create_app() -> Typer app, --version, root callback
    └── commands/               # Domain commands attach here as they're built
```

This is intentionally the whole tree right now. As roadmap phases land,
expect new top-level packages such as a provider-adapter layer, a manual
tool loop/runtime, context building, evals wiring, etc. — follow the
roadmap's section 6 target shape for naming *ideas*, but only materialize
a directory when there's real code to put in it.

One naming deviation from the roadmap, already decided in the ADR: where
the roadmap's section 6 uses `models/` for LLM provider adapters
(`gemini.py`, `anthropic.py`, `openai.py`), use `providers/` instead — a
domain-model connotation for `models/` would be misleading here.

### `docs/` (repo root, committed to Git)

- `00_roadmap/` — the self-study curriculum driving this project. Treat it
  as the source of truth for what to build next and in what order.
- `learning-log.md` — one entry per experiment (hypothesis, change, eval
  set, metrics, result, what failed, decision), per roadmap section 8.
- `architecture-decisions/` — ADRs for scope/technology choices, numbered
  sequentially (`0001-...md`, `0002-...md`, ...).
- `environment-variables/` — env var reference and the add-a-variable
  checklist.
- `github-workflow/`, `licensing/` — repo/process conventions.

Rule of thumb for anything else: if a new contributor (or future you)
needs it to understand or run the project, it belongs in `docs/`, not
`localdev/`.

### `evals/`

Per roadmap section 12 (Phase 4) and section 30 — `datasets/`, `graders/`,
`runners/`, `reports/`, `failures/`. Run with `just eval`. Currently a
placeholder (`evals/runners/run.py`) until Phase 1 produces something
worth evaluating — see `evals/README.md`.

### `localdev/` (gitignored, not shipped)

Scratch space used while developing. Nothing here is visible to anyone
else who clones the repo — never put anything here that's needed to
understand or run the project (that belongs in `docs/`).

Suggested subfolders and their purpose (create as needed):

- `debug/` — one subfolder per issue under investigation.
- `docs/` — one subfolder per piece of analysis/brainstorming/planning.
- `experiments/` — one subfolder per proof-of-concept.
- `features/` — one subfolder per feature being built; holds Superpowers-
  skill artifacts for that feature.
- `temp/` — throwaway code and files.
- `logs/` — local run logs.

## Environment

- Python `>=3.12`, pinned via `.python-version`.
- Dependencies and the virtual environment are managed with `uv`
  (`uv.lock` is committed).

### Environment variables

The canonical guide is `docs/environment-variables/environment-variables.md`.
When adding or changing configuration:

- Put local values and secrets in `.env`. Never commit `.env`.
- Update `.env.example` whenever a variable is added, renamed, or removed.
- Use `.envrc` only for direnv shell setup and non-secret developer
  tooling. It is committed to Git, so never place credentials, tokens,
  passwords, or API keys in it.
- Application code must read configuration from the process environment
  (see `Settings` in `src/shuhari_cli/core/config.py`) and must not depend
  on `.env` or `.envrc` existing.
- Require variables via `Settings` fields with no default; never log
  secret values. `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` will be the first
  real secrets, wired up when Phase 1 starts.

## Common Commands

All frequently used commands are kept in the `Justfile` — use it rather
than retyping raw commands. Run `just ci` before considering any change
done; it's the same gate the `CI` GitHub Actions workflow runs.

- `just sync` — install/update dependencies from `uv.lock`.
- `just lint` / `just fmt` / `just typecheck` / `just test` / `just ci`
- `just eval` — run the eval suite (`evals/runners/run.py`).
- `just run --version` — run the CLI (`uv run shuhari ...` under the hood).

## Testing

- `tests/unit/` mirrors `src/shuhari_cli/`'s layout 1:1 (`tests/unit/core/`
  tests `src/shuhari_cli/core/`, `tests/unit/cli/` tests
  `src/shuhari_cli/cli/`, and so on) — put a new test next to its sibling,
  not in whichever file is open.
- `tests/integration/` is for cross-module tests exercising real CLI
  invocations end-to-end; create it when that becomes worth doing.
- `tests/conftest.py`'s autouse fixture clears the `Settings` `lru_cache`
  before and after every test — if a new cached singleton is added
  anywhere, clear it there too, or tests will silently leak state across
  each other.
- CLI commands are tested with Typer's `CliRunner` (see
  `tests/unit/cli/test_main.py`) rather than mocked — prefer invoking the
  real Typer app.
- Do not add an import-skeleton test (`test_package_structure.py`-style)
  for a package that doesn't exist yet — that pattern only makes sense
  once a package actually holds real skeleton modules, and one was removed
  here for exactly that reason.

## Workflow Rules

### Git and GitHub

- Always use the `git`/`gh` CLI.
- The repo lives at `bandhu-workshop/shuhari-cli` and is public, with a
  solo-developer workflow: pull requests are required into `main`, 0
  approvals are required, CI is the merge gate. Squash- or rebase-merge
  only (merge commits are disabled; `main` keeps a linear history).
- Branch names: `feat/…`, `fix/…`, `refactor/…`, `docs/…`, `chore/…`.
- For a squash merge the PR title becomes the commit message on `main` —
  write it as a proper commit message (e.g. `feat: add hello command`).
- Full rationale and setup checklist:
  `docs/github-workflow/repo-branch-protection.md`.
- Never add a `Co-Authored-By: Claude …` (or any AI) trailer to commit
  messages, and never mention Claude/AI authorship in commits or PR
  descriptions. Claude/AI must never appear as a GitHub contributor on
  this repo — commit authorship stays solely with the human developer.

### Licensing

Project is MIT. SPDX header convention and rationale:
`docs/licensing/mit-setup.md`.
