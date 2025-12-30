from sqlalchemy.orm import Session, joinedload
from typing import Optional

from services.dao import PlaylistDao
from models.playlist import PlaylistEntity
from models.entities import Playlist, Clip
from services.api import *
from config.logging_config import get_logger
from services.mappers import to_playlist
from services.dao import PlaylistDao

logger = get_logger(__name__)


class PlaylistService:
    def __init__(self, db: Session):
        self.db = db

    def get_playlist_by_id(self, playlist_id: str) -> Optional[PlaylistEntity]:
        playlist = self.db.query(Playlist).join(Playlist.clips).options(joinedload(Playlist.profile)).filter(Playlist.id == playlist_id).first()
        if not playlist:
            playlist_data = fetch_playlist_from_suno(playlist_id)
            self.save_playlist_clips([playlist_data])
            playlist = self.db.query(Playlist).options(joinedload(Playlist.profile)).filter(Playlist.id == playlist_id).first()
        return to_playlist(playlist) if playlist else None

    def getPlaylistIds(self, profile_data: dict) -> list:
        return [playlist['id'] for playlist in profile_data.get('playlists', []) if 'id' in playlist]

    def getClipsIds(self, playlist_clips: list) -> list:
        clip_ids = []
        for playlist in playlist_clips:
            if 'playlist_clips' in playlist:
                for playlist_clip_entry in playlist['playlist_clips']:
                    clip_data = playlist_clip_entry.get('clip', {})
                    if 'id' in clip_data:
                        clip_ids.append(clip_data['id'])
            elif 'clips' in playlist:
                for clip in playlist['clips']:
                    if 'id' in clip:
                        clip_ids.append(clip['id'])
        return list(set(clip_ids))

    def save_playlist_clips(self, playlist_clips: list):
        for playlist_data in playlist_clips:
            if "id" in playlist_data:
                playlist = self.db.query(Playlist).filter(Playlist.id == playlist_data["id"]).first()
                if not playlist:
                    playlist = PlaylistDao(self.db).create_playlist(playlist_data)
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
                if "clip" in playlist_clip_entry:
                    clip_data = playlist_clip_entry["clip"]
                else:
                    clip_data = playlist_clip_entry
                
                if "id" in clip_data:
                    clip = self.db.query(Clip).filter(Clip.id == clip_data["id"]).first()
                    if not clip:
                        clip = PlaylistDao(self.db).create_clip(clip_data)
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
