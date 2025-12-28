import logging
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from backend.models.dtos import UserDTO
from ..models.database import User, Profile
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self) -> List[UserDTO]:
        users = self.db.query(User).all()
        logger.info(users)
        return [UserDTO(
            id=str(u.id),
            handle=u.handle,
            display_name=u.display_name,
            avatar_image_url=u.avatar_image_url
        ) for u in users]
        

class ProfileService:
    def __init__(self, db: Session):
        self.db = db

    def get_profile_by_id(self, profile_id: str, include_hooks: bool = False,
                         playlists_sort_by: str = "created_at",
                         clips_sort_by: str = "created_at"):
        """Get profile by ID with clips and playlists"""
        # First try to find profile by handle (string) then by id (integer)
        try:
            profile_id_int = int(profile_id)
            profile = self.db.query(Profile).filter(Profile.id == profile_id_int).first()
        except ValueError:
            # If profile_id is not an integer, try to find by handle
            profile = self.db.query(Profile).filter(Profile.handle == profile_id).first()
        
        if not profile:
            return None

        # Convert profile to dict
        profile_dict = {
            "id": profile.id,
            "handle": profile.handle,
            "display_name": profile.display_name,
            "bio": profile.profile_description,
            "avatar_url": profile.avatar_image_url,
            "is_active": profile.is_active,
            "is_verified": profile.is_verified,
            "stats": profile.stats,
            "created_at": profile.created_at.isoformat() if profile.created_at is not None else None,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at is not None else None,
        }

        # Get associated user
        user = self.db.query(User).filter(User.id == profile.user_id).first()
        if user:
            profile_dict["user"] = {
                "id": user.id,
                "username": user.username
            }

        return profile_dict

    def create_profile_from_api_data(self, user_id: int, profile_id: str, api_data: dict):
        """Create profile from API data"""
        # Check if profile already exists
        existing_profile = self.db.query(Profile).filter(Profile.handle == profile_id).first()
        if existing_profile:
            return existing_profile

        # Create new profile
        profile = Profile(
            handle=profile_id,
            user_id=user_id,
            display_name=api_data.get("display_name", ""),
            profile_description=api_data.get("bio", ""),
            avatar_image_url=api_data.get("avatar_url", ""),
            is_verified=api_data.get("is_verified", False),
            stats=api_data.get("stats", {})
        )

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile


def get_users_list(db: Session) -> List[Dict[str, Any]]:
    """
    Retrieve all users with their profiles from the database
    """
    users = db.query(User).all()
    result = []
    for user in users:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "created_at": user.created_at.isoformat() if user.created_at is not None else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at is not None else None,
        }
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
        result.append(user_dict)
    return result