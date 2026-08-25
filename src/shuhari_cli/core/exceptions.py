# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

import typer


class AppError(Exception):
    exit_code: int = 1
    detail: str = "Something went wrong"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class NotFoundError(AppError):
    exit_code = 4
    detail = "Resource not found"


def handle_app_error(exc: AppError) -> typer.Exit:
    typer.secho(exc.detail, fg=typer.colors.RED, err=True)
    return typer.Exit(code=exc.exit_code)
