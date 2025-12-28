from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from backend.app.models.dtos import (
    TemplateResponse,
    TemplateCreate
)
from services.template_service import TemplateService
from database.session import get_db

router = APIRouter()


@router.get("/", response_model=List[TemplateResponse])
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


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific template by ID"""
    template = await TemplateService.get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.post("/", response_model=TemplateResponse)
async def create_template(
    template: TemplateCreate,
    db: Session = Depends(get_db)
):
    """Create a new prompt template"""
    return await TemplateService.create_template(db, template)


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: UUID,
    template: TemplateCreate,
    db: Session = Depends(get_db)
):
    """Update an existing template"""
    updated_template = await TemplateService.update_template(db, template_id, template)
    if not updated_template:
        raise HTTPException(status_code=404, detail="Template not found")
    return updated_template


@router.delete("/{template_id}")
async def delete_template(
    template_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a template"""
    success = await TemplateService.delete_template(db, template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template deleted successfully"}