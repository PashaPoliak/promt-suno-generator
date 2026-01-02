from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.postgres_dao import PostgresClipDAO
from config.logging_config import get_logger
from app.database.postgres_connection import get_db

logger = get_logger(__name__)

router = APIRouter()


def get_clip_dao(db: Session = Depends(get_db)):
    return PostgresClipDAO(db)


@router.get("")
def get_clips_v3(db: Session = Depends(get_db)):
    try:
        clip_dao = PostgresClipDAO(db)
        clips = clip_dao.get_all_clips()
        return clips
    except Exception as e:
        logger.error(f"Error retrieving clips: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{clip_id}")
def get_clip_by_id_v3(clip_id: str, db: Session = Depends(get_db)):
    try:
        clip_dao = PostgresClipDAO(db)
        clip = clip_dao.get_clip_by_id(clip_id)
        if not clip:
            raise HTTPException(status_code=404, detail=f"Clip {clip_id} not found")
        return clip
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving clip {clip_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")