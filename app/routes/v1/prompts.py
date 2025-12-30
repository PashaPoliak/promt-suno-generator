from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from models.prompt import (
    PromptCreate, PromptResponse,
    GenerateRequest, GenerateResponse
)
from models.template import TemplateResponse
from services.prompt_service import PromptService
from services.template_service import TemplateService
from config.session import get_db

router = APIRouter()


@router.get("/", response_model=List[PromptResponse])
async def get_prompts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all generated prompts with optional filtering and pagination"""
    return await PromptService.get_prompts(db, skip=skip, limit=limit)


@router.post("/", response_model=PromptResponse)
async def create_prompt(
    prompt: PromptCreate,
    db: Session = Depends(get_db)
):
    """Generate and save a new prompt"""
    return await PromptService.create_prompt(db, prompt)


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
    prompt_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific prompt by ID"""
    prompt = await PromptService.get_prompt(db, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.get("/templates/", response_model=List[TemplateResponse])
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
    template_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific template by ID"""
    template = await TemplateService.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


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
    from utils.validators import PromptValidator
    validation_result = PromptValidator.validate_prompt_elements(request.dict())
    return validation_result


@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(
    prompt_id: str,
    prompt: PromptCreate,
    db: Session = Depends(get_db)
):
    """Update an existing prompt"""
    # For now, we'll just return a not implemented error
    # In a real implementation, you would update the prompt in the database
    from services.prompt_service import PromptService
    updated_prompt = await PromptService.update_prompt(db, prompt_id, prompt)
    if not updated_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return updated_prompt


@router.delete("/{prompt_id}")
async def delete_prompt(
    prompt_id: str,
    db: Session = Depends(get_db)
):
    """Delete a prompt"""
    from services.prompt_service import PromptService
    success = await PromptService.delete_prompt(db, prompt_id)
    if not success:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return {"message": "Prompt deleted successfully"}


@router.post("/combine")
async def combine_prompts(request: GenerateRequest):
    """Combine multiple prompt elements"""
    from utils.prompt_generator import PromptGenerator
    combined_prompt = PromptGenerator.generate_fusion_prompt(
        request.genre or "generic",
        request.mood or "neutral",
        style=request.style
    )
    return {"combined_prompt": combined_prompt}


@router.post("/extend")
async def extend_prompt(request: GenerateRequest):
    """Extend an existing prompt"""
    from utils.prompt_generator import PromptGenerator
    extended_prompt = PromptGenerator.generate_prompt_from_request(request)
    return {"extended_prompt": extended_prompt}