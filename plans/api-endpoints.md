# API Endpoints for Suno Prompt Generator

## Overview
This document outlines the comprehensive API endpoints for the Suno Prompt Generator application, following RESTful principles and supporting all required functionality for the prompt generation system.

## Prompt Management Endpoints

### Generated Prompts
```
GET    /api/v1/prompts         - Get all generated prompts (with pagination/filtering)
POST   /api/v1/prompts         - Generate a new prompt
GET    /api/v1/prompts/{id}    - Get specific prompt
```

### Request/Response Examples
```json
// POST /api/v1/prompts
{
  "genre": "pop",
  "mood": "energetic",
  "style": "vibrant",
  "instruments": "piano, guitar",
  "voice_tags": "smooth, powerful",
  "lyrics_structure": "verse-chorus-bridge",
  "custom_text": "Additional custom elements"
}

// Response
{
  "id": "uuid-here",
  "prompt_text": "pop, energetic, vibrant, piano, guitar, smooth, powerful, verse-chorus-bridge, Additional custom elements",
  "parameters": {
    "genre": "pop",
    "mood": "energetic",
    "style": "vibrant"
  },
  "created_at": "2023-10-01T12:00:00Z",
 "generation_result": {
    "validation": {
      "is_valid": true,
      "errors": [],
      "warnings": [],
      "suggestions": []
    }
 }
}
```

## Template Management Endpoints

### Prompt Templates
```
GET    /api/v1/templates       - Get all prompt templates (with pagination/filtering)
GET    /api/v1/templates/{id}  - Get specific template
GET    /api/v1/templates/search - Search templates by criteria
```

## Category Management Endpoints

### Categories
```
GET    /api/v1/categories      - Get all categories
POST   /api/v1/categories      - Create a new category
GET    /api/v1/categories/{id} - Get specific category
PUT    /api/v1/categories/{id} - Update a category
DELETE /api/v1/categories/{id} - Delete a category
```

## Tag Management Endpoints

### Tags
```
GET    /api/v1/tags            - Get all tags
POST   /api/v1/tags            - Create a new tag
GET    /api/v1/tags/{id}       - Get specific tag
PUT    /api/v1/tags/{id}       - Update a tag
DELETE /api/v1/tags/{id}       - Delete a tag
GET    /api/v1/tags/search     - Search tags by type/name
```

## Prompt Generation Endpoints

### Advanced Generation Features
```
POST   /api/v1/generate        - Generate a new prompt using parameters
POST   /api/v1/generate/batch  - Generate multiple prompts in batch
POST   /api/v1/generate/combine - Combine multiple prompt elements
POST   /api/v1/generate/extend - Extend an existing prompt
POST   /api/v1/validate        - Validate a prompt without generating
```

### Request/Response Examples
```json
// POST /api/v1/generate
{
  "genre": "electronic",
  "mood": "energetic",
  "style": "dynamic",
  "instruments": "synthesizer, drums",
  "voice_tags": "robotic, futuristic",
  "lyrics_structure": "verse-chorus",
  "template_id": "template-uuid-here",
  "custom_elements": {
    "tempo": "120 BPM",
    "key": "C Major"
  }
}

// Response
{
  "id": "generated-uuid-here",
  "prompt_text": "electronic, energetic, dynamic, synthesizer, drums, robotic, futuristic, verse-chorus",
  "generated_at": "2023-10-01T12:00:00Z",
  "parameters_used": {
    "genre": "electronic",
    "mood": "energetic"
  },
  "validation_result": {
    "is_valid": true,
    "errors": [],
    "warnings": ["No specific instruments mentioned"],
    "suggestions": ["Consider adding specific instruments like piano or guitar"]
  }
}
```

## API Implementation Details

### FastAPI Router Example
```python
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from models.schemas import (
    PromptCreate, PromptResponse,
    TemplateResponse,
    GenerateRequest, GenerateResponse
)
from services.prompt_service import PromptService
from services.template_service import TemplateService
from database.session import get_db

router = APIRouter(prefix="/api/v1", tags=["prompts"])

# Prompt Management Endpoints
@router.get("/prompts", response_model=List[PromptResponse])
async def get_prompts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all generated prompts with optional filtering and pagination"""
    return await PromptService.get_prompts(db, skip=skip, limit=limit)

@router.post("/prompts", response_model=PromptResponse)
async def create_prompt(
    prompt: PromptCreate,
    db: Session = Depends(get_db)
):
    """Generate and save a new prompt"""
    return await PromptService.create_prompt(db, prompt)

@router.get("/prompts/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific prompt by ID"""
    prompt = await PromptService.get_prompt(db, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

# Template Management Endpoints
@router.get("/templates", response_model=List[TemplateResponse])
async def get_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    genre: Optional[str] = Query(None),
    mood: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all prompt templates with optional filtering and pagination"""
    return await TemplateService.get_templates(
        db,
        skip=skip,
        limit=limit,
        genre=genre,
        mood=mood
    )

@router.get("/templates/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific template by ID"""
    template = await TemplateService.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

# Prompt Generation Endpoints
@router.post("/generate", response_model=GenerateResponse)
async def generate_prompt(
    request: GenerateRequest,
    db: Session = Depends(get_db)
):
    """Generate a new prompt based on parameters"""
    return await PromptService.generate_prompt(db, request)

@router.post("/generate/batch", response_model=List[GenerateResponse])
async def generate_prompts_batch(
    requests: List[GenerateRequest],
    db: Session = Depends(get_db)
):
    """Generate multiple prompts in batch"""
    return await PromptService.generate_prompts_batch(db, requests)

@router.post("/validate")
async def validate_prompt(request: GenerateRequest):
    """Validate a prompt without generating it"""
    validation_result = PromptValidator.validate_prompt_elements(request.dict())
    return validation_result
```

## Request/Response Models

### Pydantic Models
```python
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

# Prompt Models
class PromptCreate(BaseModel):
    genre: Optional[str]
    mood: Optional[str]
    style: Optional[str]
    instruments: Optional[str]
    voice_tags: Optional[str]
    lyrics_structure: Optional[str]
    custom_text: Optional[str]

class PromptResponse(BaseModel):
    id: UUID
    prompt_text: str
    parameters: Optional[dict]
    created_at: datetime
    generation_result: Optional[dict]

    class Config:
        from_attributes = True

# Template Models
class TemplateResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    genre: Optional[str]
    mood: Optional[str]
    style: Optional[str]
    instruments: Optional[str]
    voice_tags: Optional[str]
    lyrics_structure: Optional[str]
    created_at: datetime
    is_active: bool
    tags: List[str] = []

    class Config:
        from_attributes = True

# Generation Request/Response
class GenerateRequest(BaseModel):
    genre: Optional[str]
    mood: Optional[str]
    style: Optional[str]
    instruments: Optional[str]
    voice_tags: Optional[str]
    lyrics_structure: Optional[str]
    custom_elements: Optional[dict]

class GenerateResponse(BaseModel):
    id: UUID
    prompt_text: str
    generated_at: datetime
    parameters_used: dict
    validation_result: dict
```

## Security and Access Control

### Rate Limiting
- API endpoints have rate limiting to prevent abuse
- Different limits for different types of requests
- Special limits for generation endpoints due to computational cost

This API design provides comprehensive functionality for managing Suno prompts with proper validation and error handling while following RESTful conventions.