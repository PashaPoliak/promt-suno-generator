from sqlalchemy.orm import Session
from typing import List, Optional

from models.entities import PromptTemplate
from models import TemplateResponse, TemplateCreate


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
            TemplateResponse.model_validate({
                **{k: v for k, v in template.__dict__.items() if not k.startswith('_sa_')},
                'tags': []
            })
            for template in templates
        ]

    @staticmethod
    async def get_template(db: Session, template_id: str) -> Optional[TemplateResponse]:
        template = db.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
        if template:
            return TemplateResponse.model_validate({
                **{k: v for k, v in template.__dict__.items() if not k.startswith('_sa_')},
                'tags': []
            })
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
        
        return TemplateResponse.model_validate({
            **{k: v for k, v in db_template.__dict__.items() if not k.startswith('_sa_')},
            'tags': []
        })

    @staticmethod
    async def update_template(db: Session, template_id: str, template: TemplateCreate) -> Optional[TemplateResponse]:
        db_template = db.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
        if not db_template:
            return None
        
        # Update fields
        db_template.name = template.name  # type: ignore
        db_template.description = template.description  # type: ignore
        db_template.genre = template.genre  # type: ignore
        db_template.mood = template.mood  # type: ignore
        db_template.style = template.style  # type: ignore
        db_template.instruments = template.instruments  # type: ignore
        db_template.voice_tags = template.voice_tags  # type: ignore
        db_template.lyrics_structure = template.lyrics_structure  # type: ignore
        db_template.is_active = template.is_active  # type: ignore
        
        db.commit()
        db.refresh(db_template)
        
        return TemplateResponse.model_validate({
            **{k: v for k, v in db_template.__dict__.items() if not k.startswith('_sa_')},
            'tags': []
        })

    @staticmethod
    async def delete_template(db: Session, template_id: str) -> bool:
        db_template = db.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
        if not db_template:
            return False
        
        db.delete(db_template)
        db.commit()
        return True