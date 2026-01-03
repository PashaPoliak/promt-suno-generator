from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from services.mappers import to_clip_dto
from models.clip import ClipDTO
from v3.postgres_dao import PostgresClipDAO
from config.logging_config import get_logger
from typing import List, Optional

logger = get_logger(__name__)

router = APIRouter()

@router.get("")
def get_clips_v3(
    page: int = Query(1, description="Page number", ge=1),
    size: int = Query(20, description="Items per page", ge=1, le=100)
) -> List[ClipDTO]:
    try:
        offset = (page - 1) * size
        clips = PostgresClipDAO().get_all_clips(offset=offset, limit=size)
        return [to_clip_dto(clip) for clip in clips]
    except Exception as e:
        logger.error(f"Error retrieving clips: {e}")
        return []


@router.get("/{clip_id}")
def get_clip_by_id_v3(clip_id: str) -> Optional[ClipDTO]:
    try:
        return to_clip_dto(PostgresClipDAO().get_clip_by_id(clip_id))
    except Exception as e:
        logger.error(f"Error retrieving clip {clip_id}: {e}")
        raise HTTPException(status_code=404, detail=f"Clip {clip_id} not found")
    