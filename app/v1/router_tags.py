from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from config.session import get_db_sqlite

from models import (
    TagResponse,
    TagCreate
)
from v1.service_tag import TagService

router = APIRouter()


@router.get("/", response_model=List[TagResponse])
async def get_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tag_type: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    db: Session = Depends(get_db_sqlite)
):
    return await TagService.get_tags(
        db,
        skip=skip,
        limit=limit,
        tag_type=tag_type,
        name=name
    )


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: str,
    db: Session = Depends(get_db_sqlite)
):
    """Get a specific tag by ID"""
    tag = await TagService.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("/", response_model=TagResponse)
async def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db_sqlite)
):
    return await TagService.create_tag(db, tag)


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: str,
    tag: TagCreate,
    db: Session = Depends(get_db_sqlite)
):
    updated_tag = await TagService.update_tag(db, tag_id, tag)
    if not updated_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated_tag


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: str,
    db: Session = Depends(get_db_sqlite)
):
    """Delete a tag"""
    success = await TagService.delete_tag(db, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}


@router.get("/search", response_model=List[TagResponse])
async def search_tags(
    name: str = Query(..., min_length=1),
    tag_type: Optional[str] = Query(None),
    db: Session = Depends(get_db_sqlite)
):
    return await TagService.search_tags(db, name, tag_type)