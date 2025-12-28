from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database.session import get_db
from backend.models import dtos
from backend.models.database import UserProfile, Profile

router = APIRouter()


@router.get("/{user_id}/profiles", response_model=List[dtos.ProfileResponse])
def get_user_profiles(user_id: str, db: Session = Depends(get_db)):
    # Get all profiles associated with the user
    user_profile_associations = db.query(UserProfile).filter(UserProfile.user_id == user_id).all()
    profile_ids = [assoc.profile_id for assoc in user_profile_associations]
    profiles = db.query(Profile).filter(Profile.id.in_(profile_ids)).all()
    return profiles


@router.post("/{user_id}/profiles/{profile_id}")
def add_profile_to_user(user_id: str, profile_id: str, db: Session = Depends(get_db)):
    # Verify that both user and profile exist
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Check if the association already exists
    existing = db.query(UserProfile).filter(
        UserProfile.user_id == user_id,
        UserProfile.profile_id == profile_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Profile already associated with user")
    
    user_profile = UserProfile(user_id=user_id, profile_id=profile_id)
    db.add(user_profile)
    db.commit()
    return {"message": "Profile added to user successfully"}


@router.delete("/{user_id}/profiles/{profile_id}")
def remove_profile_from_user(user_id: str, profile_id: str, db: Session = Depends(get_db)):
    user_profile = db.query(UserProfile).filter(
        UserProfile.user_id == user_id,
        UserProfile.profile_id == profile_id
    ).first()
    
    if not user_profile:
        raise HTTPException(status_code=404, detail="Profile not associated with user")
    
    db.delete(user_profile)
    db.commit()
    return {"message": "Profile removed from user successfully"}