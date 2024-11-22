import os
from functools import lru_cache
from typing import Literal, Optional

from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Base application settings."""

    API_V1_PREFIX: str = "/api/v1"
    APP_ENV: Literal["local", "development", "production"] = "local"
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    DB_POOL_SIZE: Optional[int] = os.getenv("DB_POOL_SIZE", 3)
    DB_MAX_OVERFLOW: Optional[int] = os.getenv("DB_MAX_OVERFLOW", 3)


class LocalSettings(BaseAppSettings):
    """Local environment settings."""

    DEBUG: bool = True

    class Config:
        env_file = ".env"


class DevelopmentSettings(BaseAppSettings):
    """Development environment settings."""

    APP_ENV: Literal["development"] = "development"
    DEBUG: bool = True


class ProductionSettings(BaseAppSettings):
    """Production environment settings."""

    APP_ENV: Literal["production"] = "production"
    DEBUG: bool = False


@lru_cache()
def get_settings() -> BaseAppSettings:
    """
    Factory function to get the appropriate settings based on the environment.
    """
    app_env = os.getenv("APP_ENV", "local").lower()
    if app_env == "local":
        return LocalSettings()
    elif app_env == "development":
        return DevelopmentSettings()
    elif app_env == "production":
        return ProductionSettings()
    else:
        raise ValueError(f"Invalid APP_ENV: {app_env}")
