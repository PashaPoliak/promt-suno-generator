from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List
from config.session import get_db
from models.profile import ProfileDTO
from models.entities import Profile
from config.logging_config import get_logger
from services.profile_service import ProfileService
from services.mappers import to_profile_dto

logger = get_logger(__name__)

router = APIRouter()

@router.get("", response_model=List[ProfileDTO])
def get_profiles(
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db)
):
    logger.info(f"Get profiles with skip={skip}, limit={limit}")
    profiles = db.query(Profile).options(joinedload(Profile.clips), joinedload(Profile.playlists)).offset(skip).limit(limit).all()
    return [to_profile_dto(profile) for profile in profiles]

@router.get("/{profile_id}", response_model=ProfileDTO)
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile_dto = ProfileService(db).get_profile_by_handle(profile_id)
    if profile_dto:
        return profile_dto
    logger.warning(f"Profile not found with id/handle: {profile_id}")
    raise HTTPException(status_code=404, detail="Profile not found")


@router.delete("/{profile_id}")
def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db.delete(profile)
    db.commit()
    return {"message": "Profile deleted successfully"}
