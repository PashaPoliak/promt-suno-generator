from fastapi import APIRouter, HTTPException, Depends
from v3.postgres_dao import PostgresClipDAO
from config.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("")
def get_clips_v3():
    try:
        dao = PostgresClipDAO()
        clips = dao.get_all_clips()
        if clips is None:
            return []
        return clips
    except Exception as e:
        logger.error(f"Error retrieving clips: {e}")
        # Return empty list instead of failing if database is unavailable
        return []


@router.get("/{clip_id}")
def get_clip_by_id_v3(clip_id: str):
    try:
        dao = PostgresClipDAO()
        clip = dao.get_clip_by_id(clip_id)
        if clip:
            return clip
        else:
            raise HTTPException(status_code=404, detail=f"Clip {clip_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving clip {clip_id}: {e}")
        # Return 404 instead of 500 if database is unavailable
        raise HTTPException(status_code=404, detail=f"Clip {clip_id} not found or database unavailable")
    