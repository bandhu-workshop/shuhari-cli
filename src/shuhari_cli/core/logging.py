# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

import sys

from loguru import logger

_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} {level: <8} {name}: {message}"


def setup_logging(level: str = "INFO") -> None:
    """Configure loguru's global logger with a single stdout sink.

    Idempotent: repeated calls replace the sink rather than stacking them.
    """
    logger.remove()
    logger.add(sys.stdout, level=level, format=_FORMAT)
