from fastapi import APIRouter, HTTPException
from config.logging_config import get_logger
from v3.postgres_dao import PostgresPlaylistDAO

logger = get_logger(__name__)

router = APIRouter()

@router.get("")
async def get_playlists_v3():
    try:
        dao = PostgresPlaylistDAO()
        playlists = dao.get_all_playlists()
        if playlists is None:
            return []
        return playlists
    except Exception as e:
        logger.error(f"Error retrieving playlists: {e}")
        # Return empty list instead of failing if both databases are unavailable
        return []


@router.get("/{playlist_id}")
async def get_playlist_by_id_v3(playlist_id: str):
    try:
        dao = PostgresPlaylistDAO()
        playlist = dao.get_playlist_by_id(playlist_id)
        if playlist:
            return playlist
        else:
            raise HTTPException(status_code=404, detail=f"Playlist {playlist_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving playlist {playlist_id}: {e}")
        # Return 404 instead of 500 if both databases are unavailable
        raise HTTPException(status_code=404, detail=f"Playlist {playlist_id} not found or database unavailable")
