from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import uuid

from models.database import Category
from backend.app.models.dtos import CategoryCreate, CategoryResponse


class CategoryService:
    @staticmethod
    async def get_categories(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        name: Optional[str] = None
    ) -> List[CategoryResponse]:
        query = db.query(Category)
        
        if name:
            query = query.filter(Category.name.ilike(f"%{name}%"))
        
        categories = query.offset(skip).limit(limit).all()
        
        return [
            CategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                created_at=category.created_at
            )
            for category in categories
        ]

    @staticmethod
    async def get_category(db: Session, category_id: UUID) -> Optional[CategoryResponse]:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            return CategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                created_at=category.created_at
            )
        return None

    @staticmethod
    async def create_category(db: Session, category: CategoryCreate) -> CategoryResponse:
        db_category = Category(
            name=category.name,
            description=category.description
        )
        
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        
        return CategoryResponse(
            id=db_category.id,
            name=db_category.name,
            description=db_category.description,
            created_at=db_category.created_at
        )

    @staticmethod
    async def update_category(db: Session, category_id: UUID, category: CategoryCreate) -> Optional[CategoryResponse]:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return None
        
        # Update fields
        db_category.name = category.name
        db_category.description = category.description
        
        db.commit()
        db.refresh(db_category)
        
        return CategoryResponse(
            id=db_category.id,
            name=db_category.name,
            description=db_category.description,
            created_at=db_category.created_at
        )

    @staticmethod
    async def delete_category(db: Session, category_id: UUID) -> bool:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return False
        
        db.delete(db_category)
        db.commit()
        return True