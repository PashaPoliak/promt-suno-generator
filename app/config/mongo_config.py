from pydantic_settings import BaseSettings
import os
from config.settings import settings


class MongoSettings(BaseSettings):
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_database: str = os.getenv("MONGODB_DATABASE", "suno_db")
    mongodb_clips_collection: str = os.getenv("MONGODB_CLIPS_COLLECTION", "clips")
    mongodb_playlists_collection: str = os.getenv("MONGODB_PLAYLISTS_COLLECTION", "playlists")
    mongodb_profiles_collection: str = os.getenv("MONGODB_PROFILES_COLLECTION", "profiles")


mongo_settings = MongoSettings()