from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from models.profile import UserDTO
from config.session import get_db
from services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=List[UserDTO])
async def get_users_list(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_all_users()
