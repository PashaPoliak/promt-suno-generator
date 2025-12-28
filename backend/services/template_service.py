from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import uuid

from models.database import PromptTemplate
from backend.app.models.dtos import TemplateResponse, TemplateCreate


class TemplateService:
    @staticmethod
    async def get_templates(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        genre: Optional[str] = None,
        mood: Optional[str] = None
    ) -> List[TemplateResponse]:
        query = db.query(PromptTemplate)
        
        if genre:
            query = query.filter(PromptTemplate.genre == genre)
        if mood:
            query = query.filter(PromptTemplate.mood == mood)
        
        templates = query.offset(skip).limit(limit).all()
        
        return [
            TemplateResponse(
                id=template.id,
                name=template.name,
                description=template.description,
                genre=template.genre,
                mood=template.mood,
                style=template.style,
                instruments=template.instruments,
                voice_tags=template.voice_tags,
                lyrics_structure=template.lyrics_structure,
                created_at=template.created_at,
                is_active=template.is_active,
                tags=[]  # In a real implementation, you would fetch associated tags
            )
            for template in templates
        ]

    @staticmethod
    async def get_template(db: Session, template_id: UUID) -> Optional[TemplateResponse]:
        template = db.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
        if template:
            return TemplateResponse(
                id=template.id,
                name=template.name,
                description=template.description,
                genre=template.genre,
                mood=template.mood,
                style=template.style,
                instruments=template.instruments,
                voice_tags=template.voice_tags,
                lyrics_structure=template.lyrics_structure,
                created_at=template.created_at,
                is_active=template.is_active,
                tags=[]  # In a real implementation, you would fetch associated tags
            )
        return None

    @staticmethod
    async def create_template(db: Session, template: TemplateCreate) -> TemplateResponse:
        db_template = PromptTemplate(
            name=template.name,
            description=template.description,
            genre=template.genre,
            mood=template.mood,
            style=template.style,
            instruments=template.instruments,
            voice_tags=template.voice_tags,
            lyrics_structure=template.lyrics_structure,
            is_active=template.is_active
        )
        
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        
        return TemplateResponse(
            id=db_template.id,
            name=db_template.name,
            description=db_template.description,
            genre=db_template.genre,
            mood=db_template.mood,
            style=db_template.style,
            instruments=db_template.instruments,
            voice_tags=db_template.voice_tags,
            lyrics_structure=db_template.lyrics_structure,
            created_at=db_template.created_at,
            is_active=db_template.is_active,
            tags=[]  # In a real implementation, you would fetch associated tags
        )

    @staticmethod
    async def update_template(db: Session, template_id: UUID, template: TemplateCreate) -> Optional[TemplateResponse]:
        db_template = db.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
        if not db_template:
            return None
        
        # Update fields
        db_template.name = template.name
        db_template.description = template.description
        db_template.genre = template.genre
        db_template.mood = template.mood
        db_template.style = template.style
        db_template.instruments = template.instruments
        db_template.voice_tags = template.voice_tags
        db_template.lyrics_structure = template.lyrics_structure
        db_template.is_active = template.is_active
        
        db.commit()
        db.refresh(db_template)
        
        return TemplateResponse(
            id=db_template.id,
            name=db_template.name,
            description=db_template.description,
            genre=db_template.genre,
            mood=db_template.mood,
            style=db_template.style,
            instruments=db_template.instruments,
            voice_tags=db_template.voice_tags,
            lyrics_structure=db_template.lyrics_structure,
            created_at=db_template.created_at,
            is_active=db_template.is_active,
            tags=[]  # In a real implementation, you would fetch associated tags
        )

    @staticmethod
    async def delete_template(db: Session, template_id: UUID) -> bool:
        db_template = db.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
        if not db_template:
            return False
        
        db.delete(db_template)
        db.commit()
        return True