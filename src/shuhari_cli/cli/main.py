# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

from typing import Annotated

import typer

from shuhari_cli.core.config import get_settings
from shuhari_cli.core.logging import setup_logging

# Domain commands (typer.Typer() sub-apps or @app.command() functions) are
# registered here with app.add_typer(...) / app.command(...) as they are built.


def _version_callback(value: bool) -> None:
    if value:
        settings = get_settings()
        typer.echo(f"{settings.app_name} {settings.environment}")
        raise typer.Exit()


def create_app() -> typer.Typer:
    setup_logging()
    cli_app = typer.Typer(name="shuhari", no_args_is_help=True)

    @cli_app.callback()
    def main(
        version: Annotated[
            bool,
            typer.Option("--version", callback=_version_callback, is_eager=True),
        ] = False,
    ) -> None:
        pass

    return cli_app


app = create_app()

if __name__ == "__main__":
    app()
