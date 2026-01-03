from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from typing import List
import uuid
from config.logging_config import get_logger
from models.entities import *
from config.session import SessionPG

logger = get_logger(__name__)


class PostgresClipDAO:
    def _get_db_session(self):
        try:
            return SessionPG()
        except Exception as e:
            raise HTTPException(status_code=503, detail="PostgreSQL service unavailable")

    def create_clip(self, clip_data: dict):
        db = self._get_db_session()

        try:
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
            db.add(clip)
            db.commit()
            db.refresh(clip)
            return clip
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting clips: {e}")
        finally:
            if db:
                db.close()

    def get_clip_by_id(self, clip_id: str) -> Clip:
        db = self._get_db_session()            
        try:
            return db.query(Clip).filter(Clip.id == clip_id).first()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting clips: {e}")
        finally:
            if db:
                db.close()

    def get_clips_by_user_id(self, user_id: str) -> List[Clip]:
        db = self._get_db_session()
        try:
            return db.query(Clip).filter(Clip.user_id == user_id).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting clips: {e}")
        finally:
            if db:
                db.close()

    def get_all_clips(self, offset: int = 0, limit: int = 25) -> List[Clip]:
        db = self._get_db_session()
        try:
            return db.query(Clip).offset(offset).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting clips: {e}")
        finally:
            if db:
                db.close()


class PostgresPlaylistDAO:
    def _get_db_session(self):
        try:
            return SessionPG()
        except Exception as e:
            raise HTTPException(status_code=503, detail="PostgreSQL service unavailable")


    def create_playlist(self, playlist_data: dict):
        db = self._get_db_session()
            
        try:
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
            db.add(playlist)
            db.commit()
            db.refresh(playlist)
            return playlist
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting Playlist: {e}")
        finally:
            if db:
                db.close()

    def get_playlist_by_id(self, playlist_id: str):
        db = self._get_db_session()
            
        try:
            return db.query(Playlist).options(joinedload(Playlist.clips), joinedload(Playlist.profile)).filter(Playlist.id == playlist_id).first()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting Playlist: {e}")
        finally:
            if db:
                db.close()

    def get_all_playlists(self, skip: int = 0, limit: int = 25) -> List[Playlist]:
        db = self._get_db_session()
            
        try:
            return db.query(Playlist).options(joinedload(Playlist.clips), joinedload(Playlist.profile)).offset(skip).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting Playlist: {e}")
        finally:
            if db:
                db.close()


class PostgresProfileDAO:
    def _get_db_session(self):
        try:
            return SessionPG()
        except Exception as e:
            raise HTTPException(status_code=503, detail="PostgreSQL service unavailable")

    def create_profile(self, profile_data: dict):
        db = self._get_db_session()

        try:
            profile = Profile(
                id=profile_data.get("id", str(uuid.uuid4())),
                handle=profile_data.get("handle", ""),
                display_name=profile_data.get("display_name", ""),
                profile_description=profile_data.get("profile_description"),
                avatar_image_url=profile_data.get("avatar_image_url"),
                is_verified=profile_data.get("is_verified", False),
                stats=str(profile_data.get("stats", {}))
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
            return profile
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting profile: {e}")
        finally:
            if db:
                db.close()

    def get_profile_by_handle(self, handle: str):
        db = self._get_db_session()

        try:
            return db.query(Profile).options(
                joinedload(Profile.clips),
                joinedload(Profile.playlists).options(joinedload(Playlist.clips), joinedload(Playlist.profile))
                ).filter(Profile.handle == handle).first()

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting profile: {e}")
        finally:
            if db:
                db.close()

    def save_profile_with_relationships(self, data: dict):
        db = self._get_db_session()
            
        try:
            profile = db.query(Profile).filter(Profile.handle == data["handle"]).first()
            if not profile:
                profile = self._create_profile_entity(data)
                db.add(profile)
                db.commit()
                db.refresh(profile)

            for c in data.get("clips", []):
                if not c.get("id"):
                    continue
                clip_id = uuid.UUID(c["id"]) if isinstance(c["id"], str) else c["id"]
                clip = db.query(Clip).filter(Clip.id == clip_id).first()
                if not clip:
                    clip = self._create_clip_entity(c, profile)
                    db.add(clip)
                else:
                    if clip.profile_id is None:
                        clip.profile_id = profile.id
                        db.flush()
                
                if clip not in profile.clips:
                    profile.clips.append(clip)
                    db.flush()

            for p in data.get("playlists", []):
                if not p.get("id"):
                    continue
                playlist_id = uuid.UUID(p["id"]) if isinstance(p["id"], str) else p["id"]
                playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
                if not playlist:
                    playlist_handle = p.get("handle", data.get("handle", ""))
                    playlist = self._create_playlist_entity(p, profile)
                    playlist.handle = playlist_handle
                    db.add(playlist)
                    db.flush()
                else:
                    if playlist.profile_id is None:
                        playlist.profile_id = profile.id
                        db.flush()
                
                if playlist not in profile.playlists:
                    profile.playlists.append(playlist)
                    db.flush()

                playlist_clips_data = p.get("clips", [])
                if playlist_clips_data:
                    for clip_data in playlist_clips_data:
                        if "id" in clip_data and clip_data["id"]:
                            clip_id = uuid.UUID(clip_data["id"]) if isinstance(clip_data["id"], str) else clip_data["id"]
                            clip = db.query(Clip).filter(Clip.id == clip_id).first()
                            if not clip:
                                clip = self._create_clip_entity(clip_data, profile)
                                db.add(clip)
                                db.flush()

                            if clip not in playlist.clips:
                                playlist.clips.append(clip)
                                db.flush()

            db.commit()
            db.refresh(profile)
            
            return db.query(Profile).options(joinedload(Profile.clips), joinedload(Profile.playlists).options(joinedload(Playlist.clips), joinedload(Playlist.profile))).filter(Profile.handle == data["handle"]).first()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Error getting profile: {e}")
        finally:
            if db:
                db.close()

    def _create_profile_entity(self, data: dict):
        id_value = data.get("id", data.get("user_id", str(uuid.uuid4())))
        if isinstance(id_value, str):
            try:
                id_value = uuid.UUID(id_value)
            except ValueError:
                id_value = uuid.uuid4()
        return Profile(
            id=id_value,
            handle=data["handle"],
            display_name=data["display_name"],
            profile_description=data.get("profile_description"),
            avatar_image_url=data.get("avatar_image_url")
        )

    def _create_clip_entity(self, clip_data: dict, profile):
        import uuid
        clip_id = uuid.UUID(clip_data["id"]) if isinstance(clip_data["id"], str) else clip_data["id"]
        user_id = uuid.UUID(clip_data["user_id"]) if clip_data.get("user_id") and isinstance(clip_data["user_id"], str) else clip_data.get("user_id")

        profile_id = profile.id if hasattr(profile, 'id') and profile.id else None

        return Clip(
            id=clip_id,
            profile_id=profile_id,
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

    def _create_playlist_entity(self, playlist_data: dict, profile):
        playlist_id = uuid.UUID(playlist_data["id"]) if isinstance(playlist_data["id"], str) else playlist_data["id"]
        return Playlist(
            id=playlist_id,
            profile_id=profile.id,
            name=playlist_data.get("name", ""),
            description=playlist_data.get("description", ""),
            image_url=playlist_data.get("image_url"),
            upvote_count=playlist_data.get("upvote_count", 0),
            play_count=playlist_data.get("play_count", 0),
            song_count=playlist_data.get("song_count", 0),
            is_public=playlist_data.get("is_public", True),
            handle=playlist_data.get("handle", ""),
            entity_type=playlist_data.get("entity_type"),
            num_total_results=playlist_data.get("num_total_results"),
            current_page=playlist_data.get("current_page"),
            is_owned=playlist_data.get("is_owned"),
            is_trashed=playlist_data.get("is_trashed"),
            is_hidden=playlist_data.get("is_hidden"),
            user_display_name=playlist_data.get("user_display_name", ""),
            user_handle=playlist_data.get("user_handle", ""),
            user_avatar_image_url=playlist_data.get("user_avatar_image_url"),
            dislike_count=playlist_data.get("dislike_count"),
            flag_count=playlist_data.get("flag_count"),
            skip_count=playlist_data.get("skip_count"),
            is_discover_playlist=playlist_data.get("is_discover_playlist"),
            next_cursor=playlist_data.get("next_cursor")
        )

    def get_all_profiles(self, skip: int = 0, limit: int = 25) -> List[Profile]:
        db = self._get_db_session()
            
        try:
            return db.query(Profile).options(joinedload(Profile.clips), joinedload(Profile.playlists).options(joinedload(Playlist.clips), joinedload(Playlist.profile))).offset(skip).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error getting profile: {e}")

        finally:
            if db:
                db.close()
