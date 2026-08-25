# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

import typer

from shuhari_cli.core.exceptions import AppError, NotFoundError, handle_app_error


def test_app_error_default_detail():
    exc = AppError()
    assert exc.detail == "Something went wrong"
    assert exc.exit_code == 1


def test_not_found_error_overrides():
    exc = NotFoundError()
    assert exc.detail == "Resource not found"
    assert exc.exit_code == 4


def test_handle_app_error_returns_typer_exit():
    result = handle_app_error(AppError("custom detail"))
    assert isinstance(result, typer.Exit)
    assert result.exit_code == 1
