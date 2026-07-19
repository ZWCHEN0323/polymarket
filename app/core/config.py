"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import DEFAULT_LOG_LEVEL, AppEnvironment


class Settings(BaseSettings):
    """Runtime settings sourced from environment variables or `.env` file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="Polymarket Trading Bot", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    environment: AppEnvironment = Field(
        default=AppEnvironment.DEVELOPMENT,
        alias="ENVIRONMENT",
    )
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default=DEFAULT_LOG_LEVEL, alias="LOG_LEVEL")

    supabase_url: str | None = Field(default=None, alias="SUPABASE_URL")
    supabase_key: str | None = Field(default=None, alias="SUPABASE_KEY")

    @property
    def is_database_configured(self) -> bool:
        """Return whether database connection settings are present."""
        return bool(self.supabase_url and self.supabase_key)


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()
