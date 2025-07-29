from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache
import os

class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    Uses Pydantic for automatic type conversion and validation.
    """
    
    # Application settings
    APP_NAME: str = "FastAPI JWT Auth"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # MongoDB settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "fastapi_mvc_db"
    
    # Security settings
    JWT_SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS settings (will be parsed from comma-separated string in .env)
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Additional settings
    TZ: str = "UTC"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated ALLOWED_ORIGINS string to list."""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',') if origin.strip()]
        return self.ALLOWED_ORIGINS


@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache settings instance.
    Using lru_cache to ensure settings are created only once.
    """
    return Settings()

# Create global settings instance
settings = get_settings()
