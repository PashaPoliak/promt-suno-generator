from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from backend.app.models import dtos
from models.database import Clip, ProfileClip

router = APIRouter()


@router.get("/", response_model=List[dtos.ClipResponse])
def get_clips(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    clips = db.query(Clip).offset(skip).limit(limit).all()
    return clips


@router.get("/{clip_id}", response_model=dtos.ClipResponse)
def get_clip(clip_id: str, db: Session = Depends(get_db)):
    clip = db.query(Clip).filter(Clip.id == clip_id).first()
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    return clip


@router.post("/", response_model=dtos.ClipResponse)
def create_clip(clip: dtos.ClipCreate, db: Session = Depends(get_db)):
    db_clip = Clip(**clip.dict())
    db.add(db_clip)
    db.commit()
    db.refresh(db_clip)
    return db_clip


@router.put("/{clip_id}", response_model=dtos.ClipResponse)
def update_clip(
    clip_id: str,
    clip: dtos.ClipCreate,
    db: Session = Depends(get_db)
):
    db_clip = db.query(Clip).filter(Clip.id == clip_id).first()
    if not db_clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    
    for key, value in clip.dict().items():
        setattr(db_clip, key, value)
    
    db.commit()
    db.refresh(db_clip)
    return db_clip


@router.delete("/{clip_id}")
def delete_clip(clip_id: str, db: Session = Depends(get_db)):
    clip = db.query(Clip).filter(Clip.id == clip_id).first()
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    
    db.delete(clip)
    db.commit()
    return {"message": "Clip deleted successfully"}