from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid

from app.models.entities import *


class PostgresClipDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_clip(self, clip_data: dict):
        clip = Clip(
            id=clip_data.get("id", str(uuid.uuid4())),
            title=clip_data.get("title", ""),
            audio_url=clip_data.get("audio_url"),
            video_url=clip_data.get("video_url"),
            image_url=clip_data.get("image_url"),
            image_large_url=clip_data.get("image_large_url"),
            caption=clip_data.get("caption"),
            clip_type=clip_data.get("type"),
            duration=clip_data.get("duration"),
            task=clip_data.get("task"),
            user_id=clip_data.get("user_id"),
            display_name=clip_data.get("display_name"),
            handle=clip_data.get("handle"),
            user_avatar_image_url=clip_data.get("user_avatar_image_url"),
            clip_metadata=str(clip_data.get("metadata", {}))
        )
        self.db.add(clip)
        self.db.commit()
        self.db.refresh(clip)
        return clip

    def get_clip_by_id(self, clip_id: str):
        return self.db.query(Clip).filter(Clip.id == clip_id).first()

    def get_clips_by_user_id(self, user_id: str) -> List[Clip]:
        return self.db.query(Clip).filter(Clip.user_id == user_id).all()

    def get_all_clips(self, skip: int = 0, limit: int = 25) -> List[Clip]:
        return self.db.query(Clip).offset(skip).limit(limit).all()


class PostgresPlaylistDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_playlist(self, playlist_data: dict):
        playlist = Playlist(
            id=playlist_data.get("id", str(uuid.uuid4())),
            name=playlist_data.get("name", ""),
            handle=playlist_data.get("handle", ""),
            description=playlist_data.get("description"),
            image_url=playlist_data.get("image_url"),
            upvote_count=playlist_data.get("upvote_count", 0),
            play_count=playlist_data.get("play_count", 0),
            song_count=playlist_data.get("song_count", 0),
            is_public=playlist_data.get("is_public", True)
        )
        self.db.add(playlist)
        self.db.commit()
        self.db.refresh(playlist)
        return playlist

    def get_playlist_by_id(self, playlist_id: str):
        return self.db.query(Playlist).filter(Playlist.id == playlist_id).first()

    def get_all_playlists(self, skip: int = 0, limit: int = 25) -> List[Playlist]:
        return self.db.query(Playlist).offset(skip).limit(limit).all()


class PostgresProfileDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_profile(self, profile_data: dict):
        profile = Profile(
            id=profile_data.get("id", str(uuid.uuid4())),
            handle=profile_data.get("handle", ""),
            display_name=profile_data.get("display_name", ""),
            profile_description=profile_data.get("profile_description"),
            avatar_image_url=profile_data.get("avatar_image_url"),
            is_verified=profile_data.get("is_verified", False),
            stats=str(profile_data.get("stats", {}))
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_profile_by_handle(self, handle: str):
        profile = self.db.query(Profile).options(joinedload(Profile.clips), joinedload(Profile.playlists)).filter(Profile.handle == handle).first()
        return profile

    def get_all_profiles(self, skip: int = 0, limit: int = 25) -> List[Profile]:
        return self.db.query(Profile).options(joinedload(Profile.clips), joinedload(Profile.playlists)).offset(skip).limit(limit).all()
