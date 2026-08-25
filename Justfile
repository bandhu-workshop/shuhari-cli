# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

sync:
    uv sync

lint:
    uv run ruff check .

fmt:
    uv run ruff format .

typecheck:
    uv run mypy src

test:
    uv run pytest

ci: lint typecheck test

eval:
    uv run python evals/runners/run.py

run *ARGS:
    uv run shuhari {{ARGS}}
