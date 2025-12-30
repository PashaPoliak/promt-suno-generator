from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from services.api import fetch_clip_from_suno
from services.clip_service import ClipService
from services.mappers import to_clip_dto
from config.session import get_db
from models.clip import ClipDTO
from models.entities import Clip

from config.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("", response_model=List[ClipDTO], response_model_exclude_none=True)
def get_clips(
    page: int = 0,
    size: int = 25,
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching clips with page={page}, size={size}")
    clips = db.query(Clip).offset(page).limit(size).all()
    clip_dtos = [to_clip_dto(clip) for clip in clips]
    logger.info(f"Successfully get {len(clip_dtos)} clips")
    return clip_dtos


@router.get("/{clip_id}", response_model=ClipDTO, response_model_exclude_none=True)
def get_clip(clip_id: str, db: Session = Depends(get_db)):
    clip_service = ClipService(db)
    fetch_clip_from_suno(clip_id)
    clip = clip_service.get_clip_by_id(clip_id)
    if not clip:
        logger.warning(f"Clip not found with ID: {clip_id}")
        raise HTTPException(status_code=404, detail="Clip not found")
    return clip


@router.delete("/{clip_id}")
def delete_clip(clip_id: str, db: Session = Depends(get_db)):
    clip = db.query(Clip).filter(Clip.id == clip_id).first()
    if not clip:
        raise HTTPException(status_code=404, detail="Clip not found")
    
    db.delete(clip)
    db.commit()
    return {"message": "Clip deleted successfully"}