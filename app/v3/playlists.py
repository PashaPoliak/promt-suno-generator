from fastapi import APIRouter, HTTPException
from app.services.mappers import to_playlist_dto
from config.logging_config import get_logger
from models.playlist import PlaylistDTO
from v3.postgres_dao import PostgresPlaylistDAO

logger = get_logger(__name__)

router = APIRouter()

@router.get("")
async def get_playlists_v3():
    try:
        return PostgresPlaylistDAO().get_all_playlists()
    except Exception as e:
        logger.error(f"Error retrieving playlists: {e}")
        return []


@router.get("/{playlist_id}")
async def get_playlist_by_id_v3(playlist_id: str) -> PlaylistDTO:
    try:
        dao = PostgresPlaylistDAO()
        playlist = dao.get_playlist_by_id(playlist_id)
        all_clips = getattr(playlist, 'clips', []) or []
        return to_playlist_dto(playlist, all_clips)
    except Exception as e:
        logger.error(f"Error retrieving playlist {playlist_id}: {e}")
        raise HTTPException(status_code=503, detail=f"Playlist {playlist_id} not found")
