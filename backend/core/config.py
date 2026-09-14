from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "ExamScope API"
    # Default to the docker-compose setup
    DATABASE_URL: str = "postgresql://exam_user:exam_password@localhost:5432/exam_db"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
