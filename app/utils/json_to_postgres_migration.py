import json
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.entities import Base, Clip, Profile, Playlist
from config.settings import settings
from config.logging_config import get_logger
import uuid

logger = get_logger(__name__)

DATABASE_URL = "postgresql://admin:AFttyzTL6nzF7A4myOEFlFMazQ7dVefg@dpg-d5bf6otactks73ft9310-a.oregon-postgres.render.com/suno"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def load_json_data(file_path: Path):
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None


def migrate_clips():
    """Migrate clip data from JSON files to PostgreSQL."""
    clips_dir = Path("json/clips")
    if not clips_dir.exists():
        logger.info("Clips directory does not exist, skipping clip migration")
        return

    db = SessionLocal()
    try:
        clip_count = 0
        for json_file in clips_dir.glob("*.json"):
            data = load_json_data(json_file)
            if data:
                clips_data = data if isinstance(data, list) else [data]
                
                for clip_data in clips_data:
                    try:
                        clip_id = clip_data.get("id", str(uuid.uuid4()))
                        
                        existing_clip = db.query(Clip).filter(Clip.id == clip_id).first()
                        if existing_clip:
                            logger.info(f"Clip with ID {clip_id} already exists, skipping")
                            continue
                        
                        clip = Clip(
                            id=clip_id,
                            profile_id=clip_data.get("profile_id"),
                            title=clip_data.get("title", ""),
                            status=clip_data.get("status"),
                            play_count=clip_data.get("play_count", 0),
                            upvote_count=clip_data.get("upvote_count", 0),
                            audio_url=clip_data.get("audio_url"),
                            video_url=clip_data.get("video_url"),
                            image_url=clip_data.get("image_url"),
                            image_large_url=clip_data.get("image_large_url"),
                            created_at=clip_data.get("created_at"),
                            allow_comments=clip_data.get("allow_comments"),
                            entity_type=clip_data.get("entity_type"),
                            major_model_version=clip_data.get("major_model_version"),
                            model_name=clip_data.get("model_name"),
                            clip_metadata=clip_data.get("metadata") or clip_data.get("clip_metadata"),
                            caption=clip_data.get("caption"),
                            type=clip_data.get("type") or clip_data.get("clip_type"),
                            duration=clip_data.get("duration"),
                            refund_credits=clip_data.get("refund_credits"),
                            stream=clip_data.get("stream"),
                            make_instrumental=clip_data.get("make_instrumental"),
                            can_remix=clip_data.get("can_remix"),
                            is_remix=clip_data.get("is_remix"),
                            priority=clip_data.get("priority", 0),
                            has_stem=clip_data.get("has_stem"),
                            video_is_stale=clip_data.get("video_is_stale"),
                            uses_latest_model=clip_data.get("uses_latest_model"),
                            is_liked=clip_data.get("is_liked"),
                            user_id=clip_data.get("user_id"),
                            display_name=clip_data.get("display_name"),
                            handle=clip_data.get("handle"),
                            is_handle_updated=clip_data.get("is_handle_updated"),
                            avatar_image_url=clip_data.get("avatar_image_url"),
                            is_trashed=clip_data.get("is_trashed"),
                            is_public=clip_data.get("is_public"),
                            explicit=clip_data.get("explicit"),
                            comment_count=clip_data.get("comment_count", 0),
                            flag_count=clip_data.get("flag_count", 0),
                            is_contest_clip=clip_data.get("is_contest_clip"),
                            has_hook=clip_data.get("has_hook"),
                            batch_index=clip_data.get("batch_index", 0),
                            is_pinned=clip_data.get("is_pinned")
                        )
                        
                        db.add(clip)
                        clip_count += 1
                        
                        if clip_count % 100 == 0:
                            db.commit()
                            logger.info(f"Committed {clip_count} clips so far...")
                            
                    except Exception as e:
                        logger.error(f"Error processing clip data from {json_file}: {e}")
                        db.rollback()
        
        db.commit()
        logger.info(f"Successfully migrated {clip_count} clips to PostgreSQL")
        
    except Exception as e:
        logger.error(f"Error during clip migration: {e}")
        db.rollback()
    finally:
        db.close()


def migrate_profiles():
    """Migrate profile data from JSON files to PostgreSQL."""
    profiles_dir = Path("json/profiles")
    if not profiles_dir.exists():
        logger.info("Profiles directory does not exist, skipping profile migration")
        return

    db = SessionLocal()
    try:
        profile_count = 0
        for json_file in profiles_dir.glob("*.json"):
            data = load_json_data(json_file)
            if data:
                # Handle both single profile objects and lists of profiles
                profiles_data = data if isinstance(data, list) else [data]
                
                for profile_data in profiles_data:
                    try:
                        # Generate ID if not present
                        profile_id = profile_data.get("id", str(uuid.uuid4()))
                        
                        # Check if profile already exists by ID or handle
                        existing_profile_by_id = db.query(Profile).filter(Profile.id == profile_id).first()
                        existing_profile_by_handle = None
                        if profile_data.get("handle"):
                            existing_profile_by_handle = db.query(Profile).filter(Profile.handle == profile_data.get("handle")).first()
                        
                        if existing_profile_by_id or existing_profile_by_handle:
                            logger.info(f"Profile with ID {profile_id} or handle {profile_data.get('handle')} already exists, skipping")
                            continue
                        
                        # Create new profile
                        profile = Profile(
                            id=profile_id,
                            handle=profile_data.get("handle"),
                            display_name=profile_data.get("display_name"),
                            profile_description=profile_data.get("profile_description"),
                            avatar_image_url=profile_data.get("avatar_image_url")
                        )
                        
                        db.add(profile)
                        db.commit()  # Commit each record individually to avoid batch failures
                        profile_count += 1
                        logger.info(f"Successfully migrated profile {profile_id} ({profile_data.get('handle')})")
                        
                    except Exception as e:
                        logger.error(f"Error processing profile data from {json_file}: {e}")
                        db.rollback()
        
        logger.info(f"Successfully migrated {profile_count} profiles to PostgreSQL")
        
    except Exception as e:
        logger.error(f"Error during profile migration: {e}")
        db.rollback()
    finally:
        db.close()


def migrate_playlists():
    """Migrate playlist data from JSON files to PostgreSQL."""
    playlists_dir = Path("json/playlists")
    if not playlists_dir.exists():
        logger.info("Playlists directory does not exist, skipping playlist migration")
        return

    db = SessionLocal()
    try:
        playlist_count = 0
        for json_file in playlists_dir.glob("*.json"):
            data = load_json_data(json_file)
            if data:
                # Handle both single playlist objects and lists of playlists
                playlists_data = data if isinstance(data, list) else [data]
                
                for playlist_data in playlists_data:
                    try:
                        # Generate ID if not present
                        playlist_id = playlist_data.get("id", str(uuid.uuid4()))
                        
                        # Check if playlist already exists
                        existing_playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
                        if existing_playlist:
                            logger.info(f"Playlist with ID {playlist_id} already exists, skipping")
                            continue
                        
                        # Create new playlist
                        playlist = Playlist(
                            id=playlist_id,
                            profile_id=playlist_data.get("profile_id"),
                            name=playlist_data.get("name", ""),
                            description=playlist_data.get("description"),
                            image_url=playlist_data.get("image_url"),
                            upvote_count=playlist_data.get("upvote_count", 0),
                            play_count=playlist_data.get("play_count", 0),
                            song_count=playlist_data.get("song_count", 0),
                            is_public=playlist_data.get("is_public"),
                            entity_type=playlist_data.get("entity_type"),
                            num_total_results=playlist_data.get("num_total_results"),
                            current_page=playlist_data.get("current_page"),
                            is_owned=playlist_data.get("is_owned"),
                            is_trashed=playlist_data.get("is_trashed"),
                            is_hidden=playlist_data.get("is_hidden"),
                            user_display_name=playlist_data.get("user_display_name"),
                            user_handle=playlist_data.get("user_handle"),
                            user_avatar_image_url=playlist_data.get("user_avatar_image_url"),
                            dislike_count=playlist_data.get("dislike_count", 0),
                            flag_count=playlist_data.get("flag_count", 0),
                            skip_count=playlist_data.get("skip_count", 0),
                            is_discover_playlist=playlist_data.get("is_discover_playlist"),
                            next_cursor=playlist_data.get("next_cursor"),
                            handle=playlist_data.get("user_handle") or playlist_data.get("handle") or ""
                        )
                        
                        db.add(playlist)
                        
                        # Process clips in playlist if they exist
                        clips_data = playlist_data.get("clips", [])
                        for idx, clip_data in enumerate(clips_data):
                            clip_id = clip_data.get("id") if isinstance(clip_data, dict) else clip_data
                            if clip_id:
                                # Check if playlist-clip relationship already exists
                                existing_playlist_clip = db.query(Playlist).filter(
                                    Playlist.playlist_id == playlist_id,
                                    Playlist.clip_id == clip_id
                                ).first()
                                
                                if not existing_playlist_clip:
                                    playlist_clip = Playlist(
                                        id=str(uuid.uuid4()),
                                        playlist_id=playlist_id,
                                        clip_id=clip_id,
                                        relative_index=idx
                                    )
                                    db.add(playlist_clip)
                        
                        db.commit()  # Commit each record individually to avoid batch failures
                        playlist_count += 1
                        logger.info(f"Successfully migrated playlist {playlist_id} ({playlist_data.get('name')})")
                        
                    except Exception as e:
                        logger.error(f"Error processing playlist data from {json_file}: {e}")
                        db.rollback()
        
        logger.info(f"Successfully migrated {playlist_count} playlists to PostgreSQL")
        
    except Exception as e:
        logger.error(f"Error during playlist migration: {e}")
        db.rollback()
    finally:
        db.close()


def run_migration():
    logger.info("Starting migration from JSON to PostgreSQL...")
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Ensured database tables exist")
        
        # migrate_clips()
        migrate_profiles()
        migrate_playlists()
        
        logger.info("Migration from JSON to PostgreSQL completed successfully!")
    except Exception as e:
        logger.error(f"Migration failed: {e}")


if __name__ == "__main__":
    run_migration()