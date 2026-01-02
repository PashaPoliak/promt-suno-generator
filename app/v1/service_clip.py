from sqlalchemy.orm import Session
from typing import Optional

from models.clip import ClipDTO
from models.entities import Clip
from services.api import *
from config.logging_config import get_logger
from services.mappers import to_clip_dto, create_clip_slim

logger = get_logger(__name__)


class ClipService:
    def __init__(self, db: Session):
        self.db = db

    def get_clip_by_id(self, clip_id: str) -> Optional[ClipDTO]:
        try:
            # Try to convert string ID to UUID for the query
            import uuid
            uuid_id = uuid.UUID(clip_id) if isinstance(clip_id, str) and clip_id else clip_id
            clip = self.db.query(Clip).filter(Clip.id == uuid_id).first()
        except (ValueError, AttributeError):
            # If conversion fails, try with the original string
            clip = self.db.query(Clip).filter(Clip.id == clip_id).first()
        
        if not clip:
            try:
                clip_data = fetch_clip_from_suno(clip_id)
                self.save_clip(clip_data)
                clip = create_clip_slim(clip_data)
            except Exception as e:
                logger.error(f"Failed to fetch clip from remote API: {str(e)}")
                return None
        return to_clip_dto(clip)

    def save_clip(self, data: dict):
        try:
            # Try to convert string ID to UUID for the query
            import uuid
            clip_id = data["id"]
            if isinstance(clip_id, str):
                uuid_id = uuid.UUID(clip_id)
                clip = self.db.query(Clip).filter(Clip.id == uuid_id).first()
            else:
                clip = self.db.query(Clip).filter(Clip.id == clip_id).first()
        except (ValueError, TypeError):
            # If conversion fails, try with the original value
            clip = self.db.query(Clip).filter(Clip.id == data["id"]).first()
        
        if not clip:
            self.db.add(create_clip_slim(data))
            self.db.commit()

    def fetch_profile_from_suno(self, handle: str) -> dict:
        return fetch_profile_from_suno(handle)
