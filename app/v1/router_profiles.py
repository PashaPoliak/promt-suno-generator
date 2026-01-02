from fastapi import APIRouter, Depends
from typing import List
from models.profile import ProfileDTO
from config.logging_config import get_logger
from app.v1.service_profile import ProfileService
from app.v1.dao_sqlite import ProfileDao
from app.config.session import get_db_sqlite

logger = get_logger(__name__)

router = APIRouter()

@router.get("", response_model=List[ProfileDTO])
def get_profiles(skip: int = 0, limit: int = 100, db=Depends(get_db_sqlite)):
    logger.info(f"Get profiles from page={skip}, size={limit}")
    return ProfileService(ProfileDao(db)).get_all(skip, limit)

@router.get("/{handle}", response_model=ProfileDTO)
def get_profile(handle: str, db=Depends(get_db_sqlite)):
    logger.info(f"Get {handle} profile")
    return ProfileService(ProfileDao(db)).get_profile_by_handle(handle)


@router.delete("/{handle}")
def delete_profile(handle: str, db=Depends(get_db_sqlite)):
    ProfileService(ProfileDao(db)).delete(handle)
    return {"message": f"Profile {handle} deleted successfully"}
