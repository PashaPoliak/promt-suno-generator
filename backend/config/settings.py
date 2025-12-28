from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Suno Prompt Generator"
    app_version: str = "1.0.0"
    app_description: str = "A web application for generating prompts for Suno AI music generation platform"
    database_url: str = "sqlite:///./suno_prompts.db"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()