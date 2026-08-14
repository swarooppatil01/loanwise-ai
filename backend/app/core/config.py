from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LoanWise AI API"
    app_version: str = "0.1.0"
    environment: str = "production"
    debug: bool = False

    database_url: str = Field(
        default="postgresql+psycopg://loanwise:loanwise@localhost:5432/loanwise"
    )

    jwt_secret_key: str = Field(
        default="CHANGE_ME_IN_ENV",
        validation_alias="SECRET_KEY",
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    cors_origins: str = Field(
        default="http://localhost:5173",
        validation_alias="CORS_ORIGINS",
    )

    ai_provider: str = "gemini"
    ai_model: str = "gemini-2.5-flash"
    gemini_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
