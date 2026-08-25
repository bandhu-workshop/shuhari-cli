# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

from shuhari_cli.core.config import Settings, get_settings


def test_defaults():
    settings = Settings()
    assert settings.app_name == "shuhari-cli"
    assert settings.environment == "development"


def test_get_settings_is_cached():
    assert get_settings() is get_settings()
