# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

from loguru import logger

from shuhari_cli.core.logging import setup_logging


def test_setup_logging_installs_single_sink():
    setup_logging()
    setup_logging()

    assert len(logger._core.handlers) == 1  # type: ignore[attr-defined]


def test_setup_logging_respects_level():
    setup_logging(level="WARNING")

    sink = next(iter(logger._core.handlers.values()))  # type: ignore[attr-defined]
    assert sink.levelno == logger.level("WARNING").no
