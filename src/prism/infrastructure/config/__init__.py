"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Application
    app_name: str = "Prism Intelligence"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    secret_key: str = Field(min_length=32)
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: PostgresDsn
    database_pool_size: int = 20
    database_max_overflow: int = 10
    database_pool_timeout: int = 30

    # Redis
    redis_url: RedisDsn
    redis_pool_size: int = 20

    # Celery
    celery_broker_url: RedisDsn
    celery_result_backend: RedisDsn
    celery_task_track_started: bool = True
    celery_task_time_limit: int = 300
    celery_worker_prefetch_multiplier: int = 1

    # Security
    jwt_secret_key: str = Field(min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    bcrypt_rounds: int = 12

    # External APIs
    alpha_vantage_api_key: str | None = None
    alpha_vantage_base_url: str = "https://www.alphavantage.co/query"
    polygon_api_key: str | None = None
    polygon_base_url: str = "https://api.polygon.io"
    twelve_data_api_key: str | None = None
    twelve_data_base_url: str = "https://api.twelvedata.com"
    fred_api_key: str | None = None
    fred_base_url: str = "https://api.stlouisfed.org/fred"
    yahoo_finance_enabled: bool = True

    # Market Data
    market_data_cache_ttl: int = 300
    market_data_rate_limit: int = 5
    market_data_timeout: int = 30

    # CORS
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000", "http://localhost:8080"])
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_headers: list[str] = Field(default_factory=lambda: ["*"])

    # Logging
    log_level: str = "INFO"
    log_format: Literal["json", "text"] = "json"
    log_file: str = "logs/app.log"

    # Monitoring
    prometheus_enabled: bool = True
    prometheus_port: int = 9090
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_service_name: str = "prism-intelligence"

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    email_from: str = "noreply@prism-intelligence.com"

    # Storage
    storage_type: Literal["local", "s3"] = "local"
    storage_path: str = "./storage"
    aws_s3_bucket: str | None = None
    aws_s3_region: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    # Feature Flags
    feature_analytics_enabled: bool = True
    feature_risk_analytics_enabled: bool = True
    feature_market_data_enabled: bool = True
    feature_notifications_enabled: bool = False


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()