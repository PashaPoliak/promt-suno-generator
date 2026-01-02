from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.config.session import get_db_sqlite
from models.entities import Category
from models.category import CategoryCreate, CategoryResponse


class CategoryService:
    def __init__(self):
        self.db = Depends(get_db_sqlite)
            
    async def get_categories(self,
        skip: int = 0, 
        limit: int = 100,
        name: Optional[str] = None
    ) -> List[CategoryResponse]:
        query = self.db.query(Category)
        
        if name:
            query = query.filter(Category.name.ilike(f"%{name}%"))
        
        categories = query.offset(skip).limit(limit).all()
        
        return [
            CategoryResponse.model_validate(category)
            for category in categories
        ]

    def get_category(self, category_id: str) -> Optional[CategoryResponse]:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if category:
            return CategoryResponse.model_validate(category)
        return None


    def create_category(self, category: CategoryCreate) -> CategoryResponse:
        db_category = Category()
        setattr(db_category, 'name', category.name)
        setattr(db_category, 'description', category.description)
        
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        
        return CategoryResponse.model_validate(db_category)

    def update_category(self, category_id: str, category: CategoryCreate) -> Optional[CategoryResponse]:
        db_category = self.db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return None
        
        setattr(db_category, 'name', category.name)
        setattr(db_category, 'description', category.description)
        
        self.db.commit()
        self.db.refresh(db_category)
        
        return CategoryResponse.model_validate(db_category)

    def delete_category(self, category_id: str) -> bool:
        db_category = self.db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return False
        
        self.db.delete(db_category)
        self.db.commit()
        return True
