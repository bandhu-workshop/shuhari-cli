# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

import logging

from shuhari_cli.core.logging import setup_logging


def test_setup_logging_adds_handler_once():
    root = logging.getLogger()
    root.handlers.clear()

    setup_logging()
    setup_logging()

    assert len(root.handlers) == 1
