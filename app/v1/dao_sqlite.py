from typing import List
from fastapi import Depends, HTTPException
from app.config.session import get_db_sqlite
from app.services.mappers import to_playlist
from models.entities import Profile, Clip, Playlist
from sqlalchemy.orm import joinedload
from config.logging_config import get_logger
from uuid import UUID
import uuid

logger = get_logger(__name__)


class PlaylistDao:
    def __init__(self, db_session=None):
        self.db = db_session

    def get_all(self, skip, limit):
        if self.db is None:
            raise HTTPException(status_code=500, detail="Database session not available")

        playlists = self.db.query(Playlist).options(joinedload(Playlist.profile), joinedload(Playlist.clips)).offset(skip).limit(limit).all()
        playlist_dtos = []
        for playlist in playlists:
            playlist_dtos.append(to_playlist(playlist))
        return playlist_dtos

    def get_by_id(self, playlist_id):
        if self.db is None:
            raise HTTPException(status_code=500, detail="Database session not available")

        if not playlist_id or isinstance(playlist_id, dict):
            logger.warning(f"Invalid playlist_id: {playlist_id}")
            return None

        if isinstance(playlist_id, str):
            try:
                uuid_obj = UUID(playlist_id)
            except ValueError as e:
                logger.warning(f"Invalid UUID string '{playlist_id}': {e}")
                return None
            playlist_id = uuid_obj

        return self.db.query(Playlist).options(joinedload(Playlist.profile), joinedload(Playlist.clips)).filter(Playlist.id == playlist_id).first()

    def save_playlist_clips(self, playlist_clips: list):
        if self.db is None:
            raise HTTPException(status_code=500, detail="Database session not available")

        for playlist_data in playlist_clips:
            if not isinstance(playlist_data, dict):
                continue

            if "id" in playlist_data:
                playlist_id = playlist_data["id"]
                if isinstance(playlist_id, str):
                    try:
                        playlist_id = UUID(playlist_id)
                    except ValueError as e:
                        logger.warning(f"Invalid UUID string '{playlist_id}': {e}")
                        continue
                elif hasattr(playlist_id, 'hex'):
                    logger.info(f"playlist_id is already a UUID object: {playlist_id}")
                else:
                    logger.warning(f"Unexpected playlist_id type: {type(playlist_id)}, value: {playlist_id}")
                    continue

                playlist = self.db.query(Playlist).filter(Playlist.id == playlist_id).first()
                if not playlist:
                    playlist = create_playlist(playlist_data)
                    self.db.add(playlist)
                    self.db.commit()
                    self.db.refresh(playlist)
            else:
                continue

            self.set_playlist(playlist, playlist_data)

            playlist_clips_data = playlist_data.get("playlist_clips", [])
            if not playlist_clips_data:
                playlist_clips_data = playlist_data.get("clips", [])

            for playlist_clip_entry in playlist_clips_data:

                if not isinstance(playlist_clip_entry, dict):
                    continue

                if "clip" in playlist_clip_entry:
                    clip_data = playlist_clip_entry["clip"]
                else:
                    clip_data = playlist_clip_entry

                if "id" in clip_data:
                    clip_id = clip_data["id"]
                    if not clip_id or isinstance(clip_id, dict):
                        logger.warning(f"Invalid clip_id: {clip_id}")
                        continue

                    if isinstance(clip_id, str):
                        try:
                            clip_id = UUID(clip_id)
                        except ValueError as e:
                            logger.warning(f"Invalid clip UUID string '{clip_id}': {e}")
                            continue
                    elif hasattr(clip_id, 'hex'):
                        logger.info(f"clip_id is already a UUID object: {clip_id}")
                    else:
                        logger.warning(f"Unexpected clip_id type: {type(clip_id)}, value: {clip_id}")
                        continue

                    clip = self.db.query(Clip).filter(Clip.id == clip_id).first()
                    if not clip:
                        clip = create_clip(clip_data)
                        self.db.add(clip)
                        self.db.commit()
                        self.db.refresh(clip)

                    if playlist and clip not in playlist.clips:
                        playlist.clips.append(clip)

        self.db.commit()


    def set_playlist(self, playlist, playlist_data):
        if playlist:
            original_profile_id = playlist.profile_id
            playlist.name = playlist_data.get("name", playlist.name)
            playlist.description = playlist_data.get("description", playlist.description)
            playlist.image_url = playlist_data.get("image_url", playlist.image_url)
            playlist.upvote_count = playlist_data.get("upvote_count", playlist.upvote_count)
            playlist.play_count = playlist_data.get("play_count", playlist.play_count)
            playlist.song_count = playlist_data.get("song_count", playlist.song_count)
            playlist.is_public = playlist_data.get("is_public", playlist.is_public)
            playlist.entity_type = playlist_data.get("entity_type", playlist.entity_type)
            playlist.num_total_results = playlist_data.get("num_total_results", playlist.num_total_results)
            playlist.current_page = playlist_data.get("current_page", playlist.current_page)
            playlist.is_owned = playlist_data.get("is_owned", playlist.is_owned)
            playlist.is_trashed = playlist_data.get("is_trashed", playlist.is_trashed)
            playlist.is_hidden = playlist_data.get("is_hidden", playlist.is_hidden)
            playlist.user_display_name = playlist_data.get("user_display_name", playlist.user_display_name)
            playlist.user_handle = playlist_data.get("user_handle", playlist.user_handle)
            playlist.user_avatar_image_url = playlist_data.get("user_avatar_image_url",
                                                               playlist.user_avatar_image_url)
            playlist.dislike_count = playlist_data.get("dislike_count", playlist.dislike_count)
            playlist.flag_count = playlist_data.get("flag_count", playlist.flag_count)
            playlist.skip_count = playlist_data.get("skip_count", playlist.skip_count)
            playlist.is_discover_playlist = playlist_data.get("is_discover_playlist", playlist.is_discover_playlist)
            playlist.next_cursor = playlist_data.get("next_cursor", playlist.next_cursor)

            playlist.profile_id = original_profile_id

class ProfileDao:
    def __init__(self, db):
        self.db = db

    def get_profile_by_handle(self, handle):
        if self.db is None:
            raise HTTPException(status_code=500, detail="Database session not available")
        return self.db.query(Profile).options(joinedload(Profile.clips), joinedload(Profile.playlists)).filter(Profile.handle == handle).first()

    def get_all(self, skip: int = 0, limit: int = 200) -> List[Profile]:
        if self.db is None:
            raise HTTPException(status_code=500, detail="Database session not available")
        return self.db.query(Profile).options(joinedload(Profile.clips), joinedload(Profile.playlists)).offset(skip).limit(limit).all()

    def delete(self, profile_id: str) -> None:
        if self.db is None:
            raise HTTPException(status_code=500, detail="Database session not available")
        profile = self.db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        self.db.delete(profile)
        self.db.commit()

    def save_profile(self, data: dict):
        if self.db is None:
            raise HTTPException(status_code=500, detail="Database session not available")
        profile = self.db.query(Profile).filter(Profile.handle == data["handle"]).first()
        if not profile:
            profile = create_profile(data)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)

        for c in data.get("clips", []):
            if not c.get("id"):
                continue
            clip_id = uuid.UUID(c["id"]) if isinstance(c["id"], str) else c["id"]
            clip = self.db.query(Clip).filter(Clip.id == clip_id).first()
            if not clip:
                clip = create_clip_profile(c=c, profile=profile)
                self.db.add(clip)
            else:
                if clip.profile_id is None:
                    clip.profile_id = profile.id
                    self.db.flush()

        for p in data.get("playlists", []):
            if not p.get("id"):
                continue
            playlist_id = UUID(p["id"]) if isinstance(p["id"], str) else p["id"]
            playlist = self.db.query(Playlist).filter(Playlist.id == playlist_id).first()
            if not playlist:
                playlist_id = UUID(p["id"]) if isinstance(p["id"], str) else p["id"]

                playlist = Playlist(
                    id=playlist_id,
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
                self.db.flush() # Use flush instead of commit for better performance
            else:
                if playlist.profile_id is None:
                    playlist.profile_id = profile.id
                    self.db.flush()

            playlist_clips_data = p.get("playlist_clips", [])
            if playlist_clips_data:
                for playlist_clip_entry in playlist_clips_data:
                    if "clip" in playlist_clip_entry:
                        clip_data = playlist_clip_entry["clip"]
                    else:
                        clip_data = playlist_clip_entry

                    if "id" in clip_data and clip_data["id"]:
                        clip_id = UUID(clip_data["id"]) if isinstance(clip_data["id"], str) else clip_data["id"]
                        clip = self.db.query(Clip).filter(Clip.id == clip_id).first()
                        if not clip:
                            clip = create_clip_profile(c=clip_data, profile=profile)
                            self.db.add(clip)
                            self.db.flush()

                        if clip not in playlist.clips:
                            playlist.clips.append(clip)
                            self.db.flush()

        self.db.commit()
        self.db.refresh(profile)
        profile_with_relationships = self.db.query(Profile).options(joinedload(Profile.clips), joinedload(Profile.playlists)).filter(Profile.handle == data["handle"]).first()

        if profile_with_relationships:
            return profile_with_relationships
        raise HTTPException(status_code=404, detail=f"Profile not saved: {data}")

def create_profile(data) -> Profile:
        id_value = data.get("id", data.get("user_id", data["handle"]))
        if isinstance(id_value, str):
            id_value = uuid.UUID(id_value)
        return Profile(
            id=id_value,
            handle=data["handle"],
            display_name=data["display_name"],
            profile_description=data.get("profile_description"),
            avatar_image_url=data.get("avatar_image_url")
        )

def create_playlist(playlist_data):
        playlist_id = uuid.UUID(playlist_data["id"]) if isinstance(playlist_data["id"], str) else playlist_data["id"]
        return Playlist(
            id=playlist_id,
            name=playlist_data.get("name"),
            description=playlist_data.get("description"),
            image_url=playlist_data.get("image_url"),
            upvote_count=playlist_data.get("upvote_count", 0),
            play_count=playlist_data.get("play_count", 0),
            song_count=playlist_data.get("song_count", 0),
            is_public=playlist_data.get("is_public", True),
            entity_type=playlist_data.get("entity_type"),
            num_total_results=playlist_data.get("num_total_results"),
            current_page=playlist_data.get("current_page"),
            is_owned=playlist_data.get("is_owned"),
            is_trashed=playlist_data.get("is_trashed"),
            is_hidden=playlist_data.get("is_hidden"),
            user_display_name=playlist_data.get("user_display_name"),
            user_handle=playlist_data.get("user_handle"),
            user_avatar_image_url=playlist_data.get("user_avatar_image_url"),
            dislike_count=playlist_data.get("dislike_count"),
            flag_count=playlist_data.get("flag_count"),
            skip_count=playlist_data.get("skip_count"),
            is_discover_playlist=playlist_data.get("is_discover_playlist"),
            next_cursor=playlist_data.get("next_cursor")
        )


def create_playlist_profile(p, profile):
        playlist_id = UUID(p["id"]) if isinstance(p["id"], str) else p["id"]
        return Playlist(
            id=playlist_id,
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

def create_clip_profile(c, profile):
        import uuid
        clip_id = uuid.UUID(c["id"]) if isinstance(c["id"], str) else c["id"]
        user_id = uuid.UUID(c["user_id"]) if c.get("user_id") and isinstance(c["user_id"], str) else c.get("user_id")

        profile_id = profile.id if hasattr(profile, 'id') and profile.id else None

        return Clip(
            id=clip_id,
            profile_id=profile_id,  # Use profile_id instead of profile object to avoid issues
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
            user_id=user_id,
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

def create_clip(clip_data):
        clip_id = UUID(clip_data["id"]) if isinstance(clip_data["id"], str) else clip_data["id"]
        user_id = UUID(clip_data["user_id"]) if clip_data.get("user_id") and isinstance(clip_data["user_id"], str) else clip_data.get("user_id")

        return Clip(
            id=clip_id,
            title=clip_data.get("title"),
            status=clip_data.get("status"),
            play_count=clip_data.get("play_count", 0),
            upvote_count=clip_data.get("upvote_count", 0),
            audio_url=clip_data.get("audio_url"),
            video_url=clip_data.get("video_url"),
            image_url=clip_data.get("image_url"),
            image_large_url=clip_data.get("image_large_url"),
            allow_comments=clip_data.get("allow_comments"),
            entity_type=clip_data.get("entity_type"),
            major_model_version=clip_data.get("major_model_version"),
            model_name=clip_data.get("model_name"),
            clip_metadata=clip_data.get("metadata"),
            caption=clip_data.get("caption"),
            type=clip_data.get("type"),
            duration=str(clip_data.get("duration")) if clip_data.get("duration") is not None else None,
            refund_credits=clip_data.get("refund_credits"),
            stream=clip_data.get("stream"),
            make_instrumental=clip_data.get("make_instrumental"),
            can_remix=clip_data.get("can_remix"),
            is_remix=clip_data.get("is_remix"),
            priority=clip_data.get("priority"),
            has_stem=clip_data.get("has_stem"),
            video_is_stale=clip_data.get("video_is_stale"),
            uses_latest_model=clip_data.get("uses_latest_model"),
            is_liked=clip_data.get("is_liked"),
            user_id=user_id,
            display_name=clip_data.get("display_name"),
            handle=clip_data.get("handle"),
            is_handle_updated=clip_data.get("is_handle_updated"),
            avatar_image_url=clip_data.get("avatar_image_url"),
            is_trashed=clip_data.get("is_trashed"),
            is_public=clip_data.get("is_public"),
            explicit=clip_data.get("explicit"),
            comment_count=clip_data.get("comment_count"),
            flag_count=clip_data.get("flag_count"),
            is_contest_clip=clip_data.get("is_contest_clip"),
            has_hook=clip_data.get("has_hook"),
            batch_index=clip_data.get("batch_index"),
            is_pinned=clip_data.get("is_pinned")
        )


def get_profile_dao(db=Depends(get_db_sqlite)):
   return ProfileDao(db)


def get_playlist_dao(db=Depends(get_db_sqlite)):
   return PlaylistDao(db)

