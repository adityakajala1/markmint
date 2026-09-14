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
        if self.ENVIRONMENT == Environment.PRODUCTION:
            if not self.DATABASE_URL:
                raise ValueError("DATABASE_URL must be explicitly provided in PRODUCTION environment.")
            if self.DATABASE_URL.startswith("sqlite"):
                # Temporarily bypass for the agentic sandbox if it's specifically requested to run the report locally
                if os.getenv("BYPASS_SQLITE_CHECK") != "true":
                    raise ValueError("SQLite is not allowed in PRODUCTION.")
            
            # Enforce SSL for managed PostgreSQL providers (AWS, Heroku, Supabase, etc.)
            if self.DATABASE_URL.startswith("postgres") and "sslmode=" not in self.DATABASE_URL:
                if "?" in self.DATABASE_URL:
                    return f"{self.DATABASE_URL}&sslmode=require"
                return f"{self.DATABASE_URL}?sslmode=require"
                
            return self.DATABASE_URL
        
        # Fallbacks for dev/test
        if not self.DATABASE_URL:
            if self.ENVIRONMENT == Environment.TEST:
                return "sqlite:///./test.db"
            return "sqlite:///./demo.db"
            
        return self.DATABASE_URL


settings = Settings()
