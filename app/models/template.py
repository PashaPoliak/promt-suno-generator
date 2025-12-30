from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class TemplateResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    genre: Optional[str]
    mood: Optional[str]
    style: Optional[str]
    instruments: Optional[str]
    voice_tags: Optional[str]
    lyrics_structure: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    category_id: Optional[str] = None
    tags: Optional[List[str]] = []

    model_config = ConfigDict(from_attributes=True)


class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    mood: Optional[str] = None
    style: Optional[str] = None
    instruments: Optional[str] = None
    voice_tags: Optional[str] = None
    lyrics_structure: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)