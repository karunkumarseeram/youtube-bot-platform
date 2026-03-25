"""
Application Configuration Management
Python 3.14.3 Compatible
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application Settings using Pydantic v2"""
    
    # ========== DATABASE ==========
    database_url: str = "postgresql://postgres:password@localhost:5432/youtube_bot"
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_db: str = "youtube_bot"
    database_pool_size: int = 20
    database_max_overflow: int = 40
    database_pool_recycle: int = 3600
    
    # ========== REDIS ==========
    redis_url: str = "redis://localhost:6379"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # ========== YOUTUBE API ==========
    youtube_api_key: str = ""
    
    # ========== JWT ==========
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # ========== BOT CONFIGURATION ==========
    max_workers: int = 10
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    bot_min_delay: float = 0.5
    bot_max_delay: float = 2.0
    
    # ========== PROXY ==========
    use_proxy: bool = False
    proxy_list_url: str = "https://www.proxy-list.download/api/proxy?type=http"
    
    # ========== APPLICATION ==========
    app_name: str = "YouTube Bot Platform"
    app_version: str = "1.0.0"
    debug: bool = True
    env: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        str_strip_whitespace = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get application settings (cached)"""
    settings = Settings()
    logger.info(f"Settings loaded for environment: {settings.env}")
    return settings