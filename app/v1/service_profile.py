from typing import List, Optional
from config.session import get_db_sqlite
from v1.dao_sqlite import ProfileDao
from models.profile import ProfileDTO
from services.api import fetch_profile_from_suno
from config.logging_config import get_logger
from services.mappers import to_profile_dto


logger = get_logger(__name__)

class ProfileService:
    def __init__(self, dao: ProfileDao):
        self.dao = dao

    def delete(self, profile_id: str):
        self.dao.delete(profile_id)

    def get_all(self, skip, limit) -> List[ProfileDTO]:
        return [to_profile_dto(profile) for profile in self.dao.get_all(skip, limit)]

    def get_profile_by_handle(self, handle: str) -> Optional[ProfileDTO]:
        profile = self.dao.get_profile_by_handle(handle)
        logger.info(f"Found profile in DAO: {profile is not None}")
        if not profile:
            logger.info(f"Locally profile not found {handle}")
            data = fetch_profile_from_suno(handle)
            logger.info(f"Fetched data from Suno API, clips count: {len(data.get('clips', []))}, playlists count: {len(data.get('playlists', []))}")
            profile = self.dao.save_profile(data)
            logger.info(f"Saved profile with id: {profile.id if profile else 'None'}")
        else:
            clips_count = len(profile.clips) if profile.clips else 0
            playlists_count = len(profile.playlists) if profile.playlists else 0
            logger.info(f"Profile exists: {profile.handle}, clips count: {clips_count}, playlists count: {playlists_count}")
            has_no_clips = clips_count == 0
            has_no_playlists = playlists_count == 0
            logger.info(f"Has no clips: {has_no_clips}, Has no playlists: {has_no_playlists}")
            
            if has_no_clips or has_no_playlists:
                logger.info(f"Profile {handle} has no clips or playlists, fetching fresh data to update relationships")
                data = fetch_profile_from_suno(handle)
                profile = self.dao.save_profile(data)
        
        return to_profile_dto(profile)
