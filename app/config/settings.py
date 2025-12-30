from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    app_name: str = "Suno Prompt Generator"
    app_version: str = "1.0.0"
    app_description: str = "A web application for generating prompts for Suno AI music generation platform"
    secret_key: str = "secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///suno.db")
    postgres_url: str = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost/suno_db")
    mongodb_url: str = os.getenv("MONGODB_URL", "")
    mongodb_database: str = os.getenv("MONGODB_DATABASE", "suno_db")
    
    environment: str = os.getenv("ENVIRONMENT", "local")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "app.log")


settings = Settings()