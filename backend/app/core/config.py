from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Influencer Outreach AI"
    app_env: str = "development"
    debug: bool = True

    mongodb_uri: str = ""
    mongodb_database: str = "influencer_outreach"

    frontend_url: str = "http://localhost:5173"
    api_base_url: str = "http://localhost:8000"

    youtube_api_key: str = ""
    llm_provider: str = ""
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    email_mode: str = "simulation"

    min_followers: int = 5000
    max_followers: int = 100000
    min_engagement_rate: float = 1.5
    min_content_relevance: float = 0.55
    min_brand_fit: float = 0.5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()