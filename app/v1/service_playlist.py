from typing import List, Optional

from app.v1.dao_sqlite import PlaylistDao
from models.playlist import PlaylistDTO
from services.api import *
from config.logging_config import get_logger
from services.mappers import to_playlist
from app.v1.dao_sqlite import PlaylistDao

logger = get_logger(__name__)

class PlaylistService:
    def __init__(self, dao: PlaylistDao):
        self.dao = dao

    def get_all(self, skip, limit) -> List[PlaylistDTO]:
        return self.dao.get_all(skip, limit)

    def get_playlist_by_id(self, playlist_id: str) -> Optional[PlaylistDTO]:
        playlist = self.dao.get_by_id(playlist_id)
        
        if not playlist:
            playlist_data = fetch_playlist_from_suno(playlist_id)
            if playlist_data:
                self.dao.save_playlist_clips([playlist_data])
                playlist = self.dao.get_by_id(playlist_id)
        else:
            if hasattr(playlist, 'clips'):
                if len(playlist.clips) == 0:
                    playlist_data = fetch_playlist_from_suno(playlist_id)
                    if playlist_data:
                        self.dao.save_playlist_clips([playlist_data])
                        playlist = self.dao.get_by_id(playlist_id)
        
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
