from pydantic_settings import BaseSettings
import os
from typing import Union
from pydantic import field_validator


class Settings(BaseSettings):
    app_name: str = "Suno Prompt Generator"
    app_version: str = "1.0.0"
    app_description: str = "A web application for generating prompts for Suno AI music generation platform"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///suno.db")
    postgres_url: str = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost/suno_db")
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_database: str = os.getenv("MONGODB_DATABASE", "suno_db")
    
    environment: str = os.getenv("ENVIRONMENT", "local")
    debug: Union[bool, str] = os.getenv("DEBUG", "False")
    
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "app.log")
    
    @field_validator('debug', mode='before')
    @classmethod
    def validate_debug(cls, v) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on", "warn", "debug", "info")
        return False


settings = Settings()