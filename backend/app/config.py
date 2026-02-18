"""
Application configuration
Loads environment variables and provides settings
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str = "sqlite:///./hackathon.db"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production-min-32-chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # AI Settings
    ai_provider: str = "claude"
    gemini_api_key: str = ""
    ai_cli_timeout: int = 30
    ai_rate_limit_per_minute: int = 10
    
    # CORS
    frontend_url: str = "http://localhost:5173"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
