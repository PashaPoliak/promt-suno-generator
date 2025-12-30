from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from models import (
    CategoryResponse,
    CategoryCreate
)
from services.category_service import CategoryService
from config.session import get_db

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    name: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all categories with optional filtering and pagination"""
    return await CategoryService.get_categories(
        db,
        skip=skip,
        limit=limit,
        name=name
    )


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific category by ID"""
    category = await CategoryService.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new category"""
    return await CategoryService.create_category(db, category)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """Update an existing category"""
    updated_category = await CategoryService.update_category(db, category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@router.delete("/{category_id}")
async def delete_category(
    category_id: str,
    db: Session = Depends(get_db)
):
    """Delete a category"""
    success = await CategoryService.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}