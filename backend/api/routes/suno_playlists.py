from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.services.suno_playlist_service import sync_playlist_with_suno, get_playlist_by_id
from backend.models.dtos import PlaylistResponse

router = APIRouter()


@router.get("/suno-playlist/{playlist_id}", response_model=PlaylistResponse)
async def get_suno_playlist(playlist_id: str, db: Session = Depends(get_db)):
    """
    Fetch a playlist from Suno API and save it to the database
    """
    try:
        playlist = sync_playlist_with_suno(db, playlist_id)
        return playlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suno-playlist/{playlist_id}/local", response_model=PlaylistResponse)
async def get_suno_playlist_local(playlist_id: str, db: Session = Depends(get_db)):
    """
    Get a playlist from the local database
    """
    playlist = get_playlist_by_id(db, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found in database")
    return playlist