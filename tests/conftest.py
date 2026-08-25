# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

import pytest

from shuhari_cli.core.config import get_settings


@pytest.fixture(autouse=True)
def _clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
