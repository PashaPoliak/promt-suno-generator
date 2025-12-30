from sqlalchemy.orm import Session
from typing import List

from models.profile import UserDTO
from models.entities import Profile
from config.logging_config import get_logger

logger = get_logger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self) -> List[UserDTO]:
        profiles = self.db.query(Profile).all()
        logger.info(profiles)
        result = []
        for profile in profiles:
            # Create a dictionary representation of the profile
            profile_dict = {
                'id': str(profile.id) if profile.id is not None else "",
                'handle': profile.handle if profile.handle is not None else "",
                'display_name': profile.display_name if profile.display_name is not None else "",
                'avatar_image_url': profile.avatar_image_url if profile.avatar_image_url is not None else ""
            }
            result.append(UserDTO(**profile_dict))
        return result