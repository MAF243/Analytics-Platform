from typing import Any, Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Environment specific configuration settings.
    """

    app_name: str = "Enterprise Analytics Platform"
    version: str = "v1.0.0"
    env: Literal["development", "testing", "production"] = "development"

    # API Settings
    api_v1_prefix: str = "/api/v1"

    # Storage Settings
    storage_base_path: str = "data"

    # Logging
    log_level: str = "INFO"

    # Security / CORS
    cors_origins: list[str] = ["http://localhost:5173"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> Any:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
