from fastapi import Depends
from typing import List

from app.config.session import get_db_sqlite
from models.profile import UserDTO
from models.entities import Profile
from config.logging_config import get_logger

logger = get_logger(__name__)


class UserService:
    def get_all_users(self) -> List[UserDTO]:
        from app.config.session import SessionLocal
        db = SessionLocal()
        try:
            profiles = db.query(Profile).all()
            logger.info(profiles)
            result = []
            for profile in profiles:
                profile_dict = {
                    'id': str(profile.id) if profile.id is not None else "",
                    'handle': profile.handle if profile.handle is not None else "",
                    'display_name': profile.display_name if profile.display_name is not None else "",
                    'avatar_image_url': profile.avatar_image_url if profile.avatar_image_url is not None else ""
                }
                result.append(UserDTO(**profile_dict))
            return result
        finally:
            db.close()
