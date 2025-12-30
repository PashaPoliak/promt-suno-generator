from sqlalchemy.orm import Session
from typing import Optional

from services.dao import ProfileDao
from models.profile import ProfileDTO
from models.entities import Profile, Clip, Playlist
from services.api import *
from config.logging_config import get_logger
from services.mappers import to_profile_dto

logger = get_logger(__name__)

class ProfileService:
    def __init__(self, db: Session):
        self.db = db


    def create_profile_from_api_data(self, profile_id: str, api_data: dict):
        existing_profile = self.db.query(Profile).filter(Profile.handle == profile_id).first()
        if existing_profile:
            return existing_profile
        
        profile = Profile(
            id=profile_id,
            handle=profile_id,
            display_name=api_data.get("display_name", ""),
            profile_description=api_data.get("bio", ""),
            avatar_image_url=api_data.get("avatar_url", ""),
            is_verified=api_data.get("is_verified", False),
            stats=api_data.get("stats", {})
        )

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile

    def get_profile_by_handle(self, handle: str) -> Optional[ProfileDTO]:
        profile = self.db.query(Profile).filter(Profile.handle == handle).first()
        if not profile:
            logger.info(f"Locally profile not found fetching {handle}")
            data = fetch_profile_from_suno(handle)
            self.save_profile(data)
            profile = self.db.query(Profile).filter(Profile.handle == handle).first()
        return to_profile_dto(profile) if profile else None

    def get_profile_by_id_dto(self, profile_id: str) -> Optional[ProfileDTO]:
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return None
        return to_profile_dto(profile)

    def save_profile(self, data: dict):
        profile = self.db.query(Profile).filter(Profile.handle == data["handle"]).first()
        if not profile:
            profile = ProfileDao(self.db).create_profile(data)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        logger.info(f"Fetched clips: {len(data.get('clips', []))}")
        for c in data.get("clips", []):
            if not c.get("id"):
                continue
            clip = self.db.query(Clip).filter(Clip.id == c["id"]).first()
            if not clip:
                clip = Clip(
                    id=c["id"],
                    profile=profile,
                    title=c.get("title"),
                    status=c.get("status"),
                    play_count=c.get("play_count", 0),
                    upvote_count=c.get("upvote_count", 0),
                    audio_url=c.get("audio_url"),
                    video_url=c.get("video_url"),
                    image_url=c.get("image_url"),
                    image_large_url=c.get("image_large_url"),
                    allow_comments=c.get("allow_comments"),
                    entity_type=c.get("entity_type"),
                    major_model_version=c.get("major_model_version"),
                    model_name=c.get("model_name"),
                    clip_metadata=c.get("metadata"),
                    caption=c.get("caption"),
                    type=c.get("type"),
                    duration=str(c.get("duration")) if c.get("duration") is not None else None,
                    refund_credits=c.get("refund_credits"),
                    stream=c.get("stream"),
                    make_instrumental=c.get("make_instrumental"),
                    can_remix=c.get("can_remix"),
                    is_remix=c.get("is_remix"),
                    priority=c.get("priority"),
                    has_stem=c.get("has_stem"),
                    video_is_stale=c.get("video_is_stale"),
                    uses_latest_model=c.get("uses_latest_model"),
                    is_liked=c.get("is_liked"),
                    user_id=c.get("user_id"),
                    display_name=c.get("display_name"),
                    handle=c.get("handle"),
                    is_handle_updated=c.get("is_handle_updated"),
                    avatar_image_url=c.get("avatar_image_url"),
                    is_trashed=c.get("is_trashed"),
                    is_public=c.get("is_public"),
                    explicit=c.get("explicit"),
                    comment_count=c.get("comment_count"),
                    flag_count=c.get("flag_count"),
                    is_contest_clip=c.get("is_contest_clip"),
                    has_hook=c.get("has_hook"),
                    batch_index=c.get("batch_index"),
                    is_pinned=c.get("is_pinned")
                )
                self.db.add(clip)

        playlist_ids = []

        logger.info(f"Fetched playlists: {len(data.get('playlists', []))}")
        for p in data.get("playlists", []):
            playlist_ids.append(p["id"])
            playlist = self.db.query(Playlist).filter(Playlist.id == p["id"]).first()
            if not playlist:
                playlist = Playlist(
                    id=p["id"],
                    profile_id=profile.id,
                    name=p.get("name"),
                    description=p.get("description"),
                    image_url=p.get("image_url"),
                    upvote_count=p.get("upvote_count", 0),
                    play_count=p.get("play_count", 0),
                    song_count=p.get("song_count", 0),
                    is_public=p.get("is_public", True),
                    entity_type=p.get("entity_type"),
                    num_total_results=p.get("num_total_results"),
                    current_page=p.get("current_page"),
                    is_owned=p.get("is_owned"),
                    is_trashed=p.get("is_trashed"),
                    is_hidden=p.get("is_hidden"),
                    user_display_name=p.get("user_display_name"),
                    user_handle=p.get("user_handle"),
                    user_avatar_image_url=p.get("user_avatar_image_url"),
                    dislike_count=p.get("dislike_count"),
                    flag_count=p.get("flag_count"),
                    skip_count=p.get("skip_count"),
                    is_discover_playlist=p.get("is_discover_playlist"),
                    next_cursor=p.get("next_cursor")
                )
                self.db.add(playlist)
                # Commit after adding each playlist to ensure relationships are established
                self.db.commit()
                # Refresh to ensure the object is in the session
                self.db.refresh(playlist)
            else:
                # If playlist already exists, ensure it has the correct profile relationship
                if playlist.profile_id is None:
                    playlist.profile_id = profile.id
                    self.db.commit()

        self.db.commit()
