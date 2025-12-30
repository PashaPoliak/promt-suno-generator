from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from services.playlist_service import PlaylistService
from config.session import get_db
from models.playlist import PlaylistDTO, PlaylistEntity
from models.entities import Playlist, playlist_clips
from services.mappers import to_playlist

from config.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("", response_model=List[PlaylistDTO])
def get_playlists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching playlists with skip={skip}, limit={limit}")
    playlists = db.query(Playlist).options(joinedload(Playlist.profile), joinedload(Playlist.clips)).offset(skip).limit(limit).all()
    logger.info(f"Successfully get {len(playlists)} playlists")
    playlist_dtos = []
    for playlist in playlists:
        logger.info(f"Successfully get {len(playlist.clips)} clips")
        playlist_dtos.append(to_playlist(playlist))
    return playlist_dtos

@router.get("/{playlist_id}", response_model=PlaylistEntity)
def get_playlist_by_id(playlist_id: str, db: Session = Depends(get_db)):
    playlist_service = PlaylistService(db)
    playlist = playlist_service.get_playlist_by_id(playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail=playlist_id + " playlist not found")
    return playlist

@router.delete("/{playlist_id}")
def delete_playlist(playlist_id: str, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    db.delete(playlist)
    db.commit()
    return {"message": "Playlist deleted successfully"}
