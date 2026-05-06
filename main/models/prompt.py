from pydantic import BaseModel, ConfigDict
from typing import Any, Dict, Optional
from datetime import datetime


class PromptResponse(BaseModel):
    id: str
    prompt_text: str
    parameters: Optional[Dict[str, Any]]
    is_favorite: bool
    generation_result: Optional[Dict[str, Any]]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PromptCreate(BaseModel):
    prompt_text: Optional[str] = None
    genre: Optional[str] = None
    mood: Optional[str] = None
    style: Optional[str] = None
    instruments: Optional[str] = None
    voice_tags: Optional[str] = None
    lyrics_structure: Optional[str] = None
    custom_text: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    is_favorite: bool = False
    generation_result: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class GenerateRequest(BaseModel):
    genre: Optional[str] = None
    mood: Optional[str] = None
    style: Optional[str] = None
    instruments: Optional[str] = None
    voice_tags: Optional[str] = None
    lyrics_structure: Optional[str] = None
    custom_text: Optional[str] = None
    custom_elements: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class GenerateResponse(BaseModel):
    id: str
    prompt_text: str
    generated_at: datetime
    parameters_used: dict
    validation_result: dict

    model_config = ConfigDict(from_attributes=True)