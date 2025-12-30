from sqlalchemy.orm import Session
from typing import List, Optional

from models.entities import Category
from models.category import CategoryCreate, CategoryResponse


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
            CategoryResponse.model_validate(category)
            for category in categories
        ]

    @staticmethod
    async def get_category(db: Session, category_id: str) -> Optional[CategoryResponse]:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            return CategoryResponse.model_validate(category)
        return None

    @staticmethod
    async def create_category(db: Session, category: CategoryCreate) -> CategoryResponse:
        db_category = Category()
        setattr(db_category, 'name', category.name)
        setattr(db_category, 'description', category.description)
        
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        
        return CategoryResponse.model_validate(db_category)

    @staticmethod
    async def update_category(db: Session, category_id: str, category: CategoryCreate) -> Optional[CategoryResponse]:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return None
        
        setattr(db_category, 'name', category.name)
        setattr(db_category, 'description', category.description)
        
        db.commit()
        db.refresh(db_category)
        
        return CategoryResponse.model_validate(db_category)

    @staticmethod
    async def delete_category(db: Session, category_id: str) -> bool:
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return False
        
        db.delete(db_category)
        db.commit()
        return True
