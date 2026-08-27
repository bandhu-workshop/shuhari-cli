# shuhari-cli

## About

**shuhari-cli** is a learn-by-building CLI project for agent engineering:
understanding how the Claude and OpenAI APIs actually work — tool calling,
streaming, context/token accounting, evaluation — by building real code
against the raw provider SDKs first, then progressively more capable
agent harnesses, following
[`docs/00_roadmap/agent-engineering-self-study-roadmap.md`](docs/00_roadmap/agent-engineering-self-study-roadmap.md).
It is a CLI tool, not a web product.

This is an early-stage, actively developed project — see
[`CLAUDE.md`](CLAUDE.md) for the current state of the codebase.

## Getting Started

### Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- [direnv](https://direnv.net/) (recommended, for automatic env loading)

### Install

```bash
git clone https://github.com/bandhu-workshop/shuhari-cli.git
cd shuhari-cli
uv sync
```

### Configure

```bash
cp .env.example .env    # fill in local values
direnv allow             # or: eval "$(direnv hook <shell>)" first, if not set up yet
```

Environment variables are loaded via `.envrc` (direnv), which loads `.env`
if present. Full strategy is in
[`docs/environment-variables/environment-variables.md`](docs/environment-variables/environment-variables.md).

### Run

```bash
uv run shuhari --version
```

All frequently used commands are in the `Justfile` — see `CLAUDE.md` for
the project's full command set and conventions.

### Test

```bash
just test    # run the test suite
just ci      # lint + typecheck + test (same gate CI runs)
```

## License

Copyright © 2026 Dinabandhu Behera.

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for details.

Project structure and tooling conventions adapted from
[creditforge](https://github.com/bandhu-workshop/creditforge).
