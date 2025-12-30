from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class TagResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    tag_type: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagCreate(BaseModel):
    name: str
    description: Optional[str] = None
    tag_type: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)