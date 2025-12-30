import asyncio
import json
from pathlib import Path
from database.mongo_connection import mongodb
from database.mongo_models import MongoClip, MongoPlaylist, MongoProfile
from config.logging_config import get_logger

logger = get_logger(__name__)


async def load_json_data(file_path: Path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None


async def migrate_clips():
    """Migrate clip data from JSON files to MongoDB."""
    clips_dir = Path("app/json/clips")
    if not clips_dir.exists():
        logger.info("Clips directory does not exist, skipping clip migration")
        return

    clips = []
    for json_file in clips_dir.glob("*.json"):
        data = await load_json_data(json_file)
        if data:
            # Convert the JSON data to the MongoClip model
            try:
                # Handle both single clip objects and lists of clips
                if isinstance(data, list):
                    for clip_data in data:
                        clip = MongoClip(**clip_data)
                        clips.append(clip.model_dump())
                else:
                    clip = MongoClip(**data)
                    clips.append(clip.model_dump())
            except Exception as e:
                logger.error(f"Error processing clip data from {json_file}: {e}")

    if clips:
        try:
            result = await mongodb.clips_collection.insert_many(clips)
            logger.info(f"Successfully migrated {len(result.inserted_ids)} clips to MongoDB")
        except Exception as e:
            logger.error(f"Error inserting clips into MongoDB: {e}")


async def migrate_playlists():
    """Migrate playlist data from JSON files to MongoDB."""
    playlists_dir = Path("app/json/playlists")
    if not playlists_dir.exists():
        logger.info("Playlists directory does not exist, skipping playlist migration")
        return

    playlists = []
    for json_file in playlists_dir.glob("*.json"):
        data = await load_json_data(json_file)
        if data:
            # Convert the JSON data to the MongoPlaylist model
            try:
                # Handle both single playlist objects and lists of playlists
                if isinstance(data, list):
                    for playlist_data in data:
                        playlist = MongoPlaylist(**playlist_data)
                        playlists.append(playlist.model_dump())
                else:
                    playlist = MongoPlaylist(**data)
                    playlists.append(playlist.model_dump())
            except Exception as e:
                logger.error(f"Error processing playlist data from {json_file}: {e}")

    if playlists:
        try:
            result = await mongodb.playlists_collection.insert_many(playlists)
            logger.info(f"Successfully migrated {len(result.inserted_ids)} playlists to MongoDB")
        except Exception as e:
            logger.error(f"Error inserting playlists into MongoDB: {e}")


async def migrate_profiles():
    """Migrate profile data from JSON files to MongoDB."""
    profiles_dir = Path("app/json/profiles")
    if not profiles_dir.exists():
        logger.info("Profiles directory does not exist, skipping profile migration")
        return

    profiles = []
    for json_file in profiles_dir.glob("*.json"):
        data = await load_json_data(json_file)
        if data:
            # Convert the JSON data to the MongoProfile model
            try:
                # Handle both single profile objects and lists of profiles
                if isinstance(data, list):
                    for profile_data in data:
                        # Set id from user_id or handle if id is not present
                        if 'id' not in profile_data:
                            profile_data['id'] = profile_data.get('user_id', profile_data.get('handle', ''))
                        profile = MongoProfile(**profile_data)
                        profiles.append(profile.model_dump())
                else:
                    # Set id from user_id or handle if id is not present
                    if 'id' not in data:
                        data['id'] = data.get('user_id', data.get('handle', ''))
                    profile = MongoProfile(**data)
                    profiles.append(profile.model_dump())
            except Exception as e:
                logger.error(f"Error processing profile data from {json_file}: {e}")

    if profiles:
        try:
            result = await mongodb.profiles_collection.insert_many(profiles)
            logger.info(f"Successfully migrated {len(result.inserted_ids)} profiles to MongoDB")
        except Exception as e:
            logger.error(f"Error inserting profiles into MongoDB: {e}")


async def run_migration():
    """Run the complete migration process."""
    logger.info("Starting migration from JSON to MongoDB...")
    
    # Connect to MongoDB
    mongodb.connect()
    
    try:
        # Clear existing collections if needed
        await mongodb.clips_collection.delete_many({})
        await mongodb.playlists_collection.delete_many({})
        await mongodb.profiles_collection.delete_many({})
        logger.info("Cleared existing data from collections")
        
        # Run migrations
        await migrate_clips()
        await migrate_playlists()
        await migrate_profiles()
        
        logger.info("Migration completed successfully!")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
    finally:
        # Disconnect from MongoDB
        mongodb.disconnect()


if __name__ == "__main__":
    asyncio.run(run_migration())