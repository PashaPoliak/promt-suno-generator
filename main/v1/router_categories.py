from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional

from models import (CategoryResponse, CategoryCreate)
from v1.service_category import CategoryService

router = APIRouter()


@router.get("", response_model=List[CategoryResponse])
def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    name: Optional[str] = Query(None)):

    return CategoryService().get_categories(skip=skip, limit=limit, name=name)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str):
    category = CategoryService().get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate):
    return CategoryService().create_category(category)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: str, category: CategoryCreate):
    updated_category = CategoryService().update_category(category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@router.delete("/{category_id}")
def delete_category(category_id: str):
    success = CategoryService().delete_category(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully " + category_id}
