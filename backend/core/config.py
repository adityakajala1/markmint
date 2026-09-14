from enum import Enum
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    PROJECT_NAME: str = "ExamScope API"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    
    # Must be provided via .env or environment variable
    DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def get_database_url(self) -> str:
        if self.ENVIRONMENT == Environment.PRODUCTION:
            if not self.DATABASE_URL:
                raise ValueError("DATABASE_URL must be explicitly provided in PRODUCTION environment.")
            if self.DATABASE_URL.startswith("sqlite"):
                raise ValueError("SQLite fallback is FORBIDDEN in PRODUCTION environment. Use PostgreSQL.")
            return self.DATABASE_URL
        
        # Fallbacks for dev/test
        if not self.DATABASE_URL:
            if self.ENVIRONMENT == Environment.TEST:
                return "sqlite:///./test.db"
            return "sqlite:///./demo.db"
            
        return self.DATABASE_URL


settings = Settings()
