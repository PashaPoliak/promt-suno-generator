from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ...database.session import get_db
from ...models import dtos
from ...models.database import Playlist, Clip, playlist_clips

router = APIRouter()


@router.get("/", response_model=List[dtos.PlaylistEntity])
def get_playlists(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    playlists = db.query(Playlist).offset(skip).limit(limit).all()
    return playlists


@router.get("/{playlist_id}", response_model=dtos.PlaylistEntity)
def get_playlist(playlist_id: str, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@router.post("/", response_model=dtos.PlaylistEntity)
def create_playlist(playlist: dtos.PlaylistEntityCreate, db: Session = Depends(get_db)):
    db_playlist = Playlist(**playlist.dict())
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


@router.put("/{playlist_id}", response_model=dtos.PlaylistEntity)
def update_playlist(
    playlist_id: str,
    playlist: dtos.PlaylistEntityCreate,
    db: Session = Depends(get_db)
):
    db_playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not db_playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    for key, value in playlist.dict().items():
        setattr(db_playlist, key, value)
    
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


@router.delete("/{playlist_id}")
def delete_playlist(playlist_id: str, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    db.delete(playlist)
    db.commit()
    return {"message": "Playlist deleted successfully"}


# Playlist clips endpoints
@router.get("/{playlist_id}/clips", response_model=List[dtos.ClipResponse])
def get_playlist_clips(playlist_id: str, db: Session = Depends(get_db)):
    clips = db.query(Clip).join(playlist_clips).filter(playlist_clips.c.playlist_id == playlist_id).all()
    return clips


@router.post("/{playlist_id}/clips", response_model=dtos.PlaylistClipAssociationResponse)
def add_clip_to_playlist(
    playlist_id: str,
    playlist_clip: dtos.PlaylistClipAssociationCreate,
    db: Session = Depends(get_db)
):
    # Verify that the playlist exists
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Verify that the clip exists
    clip = db.query(Clip).filter(Clip.id == playlist_clip.clip_id).first()
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    
    # Check if the clip is already in the playlist
    existing = db.query(playlist_clips).filter(
        playlist_clips.c.playlist_id == playlist_id,
        playlist_clips.c.clip_id == playlist_clip.clip_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Clip already exists in playlist")
    
    # Create association between playlist and clip
    association_data = {
        'playlist_id': playlist_id,
        'clip_id': playlist_clip.clip_id,
        'relative_index': playlist_clip.relative_index
    }
    db.execute(playlist_clips.insert().values(**association_data))
    db.commit()
    
    from datetime import datetime
    # Create a response object with minimal data
    response = dtos.PlaylistClipAssociationResponse(
        id=playlist_clip.clip_id,  # Using clip_id as a placeholder
        playlist_id=playlist_clip.playlist_id,
        clip_id=playlist_clip.clip_id,
        relative_index=playlist_clip.relative_index,
        added_at=datetime.now()  # Use current time
    )
    return response


@router.delete("/{playlist_id}/clips/{clip_id}")
def remove_clip_from_playlist(playlist_id: str, clip_id: str, db: Session = Depends(get_db)):
    playlist_clip = db.query(Playlist).filter(
        Playlist.playlist_id == playlist_id,
        Playlist.clip_id == clip_id
    ).first()
    
    if not playlist_clip:
        raise HTTPException(status_code=404, detail="Clip not found in playlist")
    
    db.delete(playlist_clip)
    db.commit()
    return {"message": "Clip removed from playlist successfully"}