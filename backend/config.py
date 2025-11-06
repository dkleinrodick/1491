"""Configuration management for the application."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # Database
    database_url: str = "sqlite:///./gowild.db"

    # Scraper Configuration
    scraper_headless: bool = True
    scraper_timeout: int = 30000
    scraper_max_retries: int = 3

    # Rate Limiting
    rate_limit_requests: int = 10
    rate_limit_window: int = 60

    # CORS
    frontend_url: str = "http://localhost:5173"
    allowed_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    # Optional Redis
    redis_url: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
