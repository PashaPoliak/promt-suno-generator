from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from ...models.database import User, Profile
from ...database.session import get_db
from ...services.services import get_users_list as service_get_users_list

router = APIRouter()

@router.get("/", response_model=List[Dict[str, Any]])
async def get_users_list(db: Session = Depends(get_db)):
    return service_get_users_list(db)

@router.post("/")
async def create_user(
    username: str,
    db: Session = Depends(get_db)
):
    """Create a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = User(
        username=username
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at.isoformat() if user.created_at is not None else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at is not None else None,
    }

@router.get("/{user_id}", response_model=Dict[str, Any])
async def get_user_by_id(user_id: str, db: Session = Depends(get_db)):  # Changed from int to str to match UUID
    """Get user by ID"""
    # First try to find by user ID (UUID)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "created_at": user.created_at.isoformat() if user.created_at is not None else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at is not None else None,
        }
        
        # Add profiles to user data
        profiles = db.query(Profile).filter(Profile.user_id == user.id).all()
        user_dict["profiles"] = [
            {
                "id": profile.id,
                "profile_id": profile.handle,  # Changed from profile_id to handle
                "is_active": profile.is_active,
                "bio": profile.profile_description,  # Changed from bio to profile_description
                "avatar_url": profile.avatar_image_url, # Changed from avatar_url to avatar_image_url
                "created_at": profile.created_at.isoformat() if profile.created_at is not None else None,
            }
            for profile in profiles
        ]
        
        return user_dict

    # If not found by user ID, try to find by profile handle
    profile = db.query(Profile).filter(Profile.handle == user_id).first()
    if profile:
        user = db.query(User).filter(User.id == profile.user_id).first()
        if user:
            user_dict = {
                "id": user.id,
                "username": user.username,
                "created_at": user.created_at.isoformat() if user.created_at is not None else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at is not None else None,
            }
            
            # Add profiles to user data (all profiles for this user)
            profiles = db.query(Profile).filter(Profile.user_id == user.id).all()
            user_dict["profiles"] = [
                {
                    "id": profile.id,
                    "profile_id": profile.handle,  # Changed from profile_id to handle
                    "is_active": profile.is_active,
                    "bio": profile.profile_description,  # Changed from bio to profile_description
                    "avatar_url": profile.avatar_image_url,  # Changed from avatar_url to avatar_image_url
                    "created_at": profile.created_at.isoformat() if profile.created_at is not None else None,
                }
                for profile in profiles
            ]
            
            return user_dict

    raise HTTPException(status_code=404, detail="User not found")