from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)