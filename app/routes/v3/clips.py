from fastapi import APIRouter, HTTPException
from services.mongo_dao import MongoClipDAO
from config.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()


def get_clip_dao():
    """Lazy initialization of clip DAO to avoid immediate MongoDB connection"""
    return MongoClipDAO()


@router.get("")
async def get_clips_v3():
    try:
        clip_dao = get_clip_dao()
        clips = await clip_dao.get_all_clips()
        return clips
    except Exception as e:
        logger.error(f"Error retrieving clips: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{clip_id}")
async def get_clip_by_id_v3(clip_id: str):
    try:
        clip_dao = get_clip_dao()
        clip = await clip_dao.get_clip_by_id(clip_id)
        if not clip:
            raise HTTPException(status_code=404, detail=f"Clip {clip_id} not found")
        return clip
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving clip {clip_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")