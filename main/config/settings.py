from pydantic_settings import BaseSettings
import os
from typing import Union
from pydantic import field_validator


class Settings(BaseSettings):
    app_name: str = "Suno Prompt Generator"
    app_version: str = "1.0.0"
    app_description: str = "A web application for generating prompts for Suno music generation platform"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///suno.db")
    postgres_url: str = os.getenv("POSTGRES_URL", "postgresql://admin:AFttyzTL6nzF7A4myOEFlFMazQ7dVefg@dpg-d5bf6otactks73ft9310-a.oregon-postgres.render.com/suno")
    
    @property
    def postgresql_enabled(self) -> bool:
        """Check if PostgreSQL is enabled by testing if we can connect"""
        import psycopg2
        from urllib.parse import urlparse
        
        try:
            # Parse the PostgreSQL URL
            result = urlparse(self.postgres_url)
            # Extract connection parameters
            host = result.hostname
            port = result.port or 5432
            database = result.path[1:]  # Remove leading slash
            username = result.username
            password = result.password
            
            # Attempt to connect to PostgreSQL
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=username,
                password=password
            )
            conn.close()
            return True
        except Exception:
            return False
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
