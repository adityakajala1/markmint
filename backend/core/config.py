import os
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
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def get_database_url(self) -> str:
        url = self.DATABASE_URL
        if url and url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
            
        if self.ENVIRONMENT == Environment.PRODUCTION:
            if not url:
                raise ValueError("DATABASE_URL must be explicitly provided in PRODUCTION environment.")
            if url.startswith("sqlite"):
                # Temporarily bypass for the agentic sandbox if it's specifically requested to run the report locally
                if os.getenv("BYPASS_SQLITE_CHECK") != "true":
                    raise ValueError("SQLite is not allowed in PRODUCTION.")
            
            # Enforce SSL for managed PostgreSQL providers (AWS, Heroku, Supabase, etc.)
            if url.startswith("postgres") and "sslmode=" not in url:
                if "?" in url:
                    return f"{url}&sslmode=require"
                return f"{url}?sslmode=require"
                
            return url
        
        # Fallbacks for dev/test
        if not url:
            if self.ENVIRONMENT == Environment.TEST:
                return "sqlite:///./test.db"
            return "sqlite:///./demo.db"
            
        return url


settings = Settings()
