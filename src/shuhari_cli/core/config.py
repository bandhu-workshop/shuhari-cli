# SPDX-FileCopyrightText: 2026 Dinabandhu Behera
# SPDX-License-Identifier: MIT

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    app_name: str = "shuhari-cli"
    environment: str = "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
