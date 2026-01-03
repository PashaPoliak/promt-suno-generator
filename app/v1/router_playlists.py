from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from config.session import get_db_sqlite
from v1.dao_sqlite import PlaylistDao
from v1.service_playlist import PlaylistService
from models.playlist import PlaylistDTO, PlaylistDTO
from models.entities import Playlist

from config.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("", response_model=List[PlaylistDTO])
def get_playlists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_sqlite)
):
    logger.info(f"Fetching playlists with skip={skip}, limit={limit}")
    return PlaylistService(PlaylistDao(db)).get_all(skip, limit)

@router.get("/{playlist_id}", response_model=PlaylistDTO)
def get_playlist_by_id(playlist_id: str, db: Session = Depends(get_db_sqlite)):
    playlist = PlaylistService(PlaylistDao(db)).get_playlist_by_id(playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail=playlist_id + " playlist not found")
    return playlist

@router.delete("/{playlist_id}")
def delete_playlist(playlist_id: str, db: Session = Depends(get_db_sqlite)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    db.delete(playlist)
    db.commit()
    return {"message": "Playlist deleted successfully"}
