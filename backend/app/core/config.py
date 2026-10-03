from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Influencer Outreach AI"
    app_env: str = "development"
    debug: bool = True

    mongodb_uri: str = ""
    mongodb_database: str = "influencer_outreach"

    frontend_url: str = "http://localhost:5173"
    api_base_url: str = "http://localhost:8000"

    scraper_headless: bool = True
    scraper_timeout_ms: int = 30000
    scraper_delay_min_ms: int = 1000
    scraper_delay_max_ms: int = 2500
    scraper_max_candidates: int = 150
    scraper_max_queries: int = 10
    scraper_max_results_per_query: int = 15

    llm_provider: str = ""
    llm_api_key: str = ""
    llm_model: str = "gemini-3.8-flash"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    email_mode: str = "simulation"
    smtp_use_tls: bool = Field(
        default=True,
        validation_alias=AliasChoices("SMTP_USE_TLS", "smtp_use_tls"),
    )

    min_followers: int = 5000
    max_followers: int = 100000
    min_engagement_rate: float = 1.5
    min_content_relevance: float = 0.55
    min_brand_fit: float = 0.5

    @property
    def is_smtp_configured(self) -> bool:
        return bool(
            self.smtp_host
            and self.smtp_port
            and self.smtp_username
            and self.smtp_password
            and self.smtp_from_email
        )

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()