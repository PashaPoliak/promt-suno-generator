from fastapi import APIRouter, HTTPException
from services.mongo_dao import MongoPlaylistDAO
from config.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


def get_playlist_dao():
    """Lazy initialization of playlist DAO to avoid immediate MongoDB connection"""
    return MongoPlaylistDAO()


@router.get("")
async def get_playlists_v3():
    try:
        playlist_dao = get_playlist_dao()
        playlists = await playlist_dao.get_all_playlists()
        return playlists
    except Exception as e:
        logger.error(f"Error retrieving playlists: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{playlist_id}")
async def get_playlist_by_id_v3(playlist_id: str):
    try:
        playlist_dao = get_playlist_dao()
        playlist = await playlist_dao.get_playlist_by_id(playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail=f"Playlist {playlist_id} not found")
        return playlist
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving playlist {playlist_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")