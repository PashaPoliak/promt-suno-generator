from fastapi import APIRouter, Depends
from typing import List

from models.profile import UserDTO
from v1.service_user import UserService

router = APIRouter()

@router.get("", response_model=List[UserDTO])
async def get_users_list():
    return UserService().get_all_users()
