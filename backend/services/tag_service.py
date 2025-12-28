from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import uuid

from models.database import Tag
from backend.app.models.dtos import TagCreate, TagResponse


class TagService:
    @staticmethod
    async def get_tags(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        tag_type: Optional[str] = None,
        name: Optional[str] = None
    ) -> List[TagResponse]:
        query = db.query(Tag)
        
        if tag_type:
            query = query.filter(Tag.tag_type == tag_type)
        if name:
            query = query.filter(Tag.name.like(f"%{name}%"))
        
        tags = query.offset(skip).limit(limit).all()
        
        return [
            TagResponse.model_validate(tag)
            for tag in tags
        ]

    @staticmethod
    async def get_tag(db: Session, tag_id: UUID) -> Optional[TagResponse]:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            return TagResponse.model_validate(tag)
        return None

    @staticmethod
    async def create_tag(db: Session, tag_create: TagCreate) -> TagResponse:
        db_tag = Tag(
            name=tag_create.name,  # type: ignore
            description=tag_create.description,  # type: ignore
            tag_type=tag_create.tag_type  # type: ignore
        )
        
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        
        return TagResponse.model_validate(db_tag)

    @staticmethod
    async def update_tag(db: Session, tag_id: UUID, tag_update: TagCreate) -> Optional[TagResponse]:
        db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not db_tag:
            return None
        
        # Update fields
        db_tag.name = tag_update.name  # type: ignore
        db_tag.description = tag_update.description  # type: ignore
        db_tag.tag_type = tag_update.tag_type  # type: ignore
        
        db.commit()
        db.refresh(db_tag)
        
        return TagResponse.model_validate(db_tag)

    @staticmethod
    async def delete_tag(db: Session, tag_id: UUID) -> bool:
        db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if not db_tag:
            return False
        
        db.delete(db_tag)
        db.commit()
        return True

    @staticmethod
    async def search_tags(db: Session, name: str, tag_type: Optional[str] = None) -> List[TagResponse]:
        query = db.query(Tag).filter(Tag.name.like(f"%{name}%"))
        
        if tag_type:
            query = query.filter(Tag.tag_type == tag_type)
        
        tags = query.all()
        
        return [
            TagResponse.model_validate(tag)
            for tag in tags
        ]