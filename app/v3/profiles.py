from fastapi import APIRouter, HTTPException, Depends
from v3.postgres_dao import PostgresProfileDAO
from config.logging_config import get_logger
from services.mappers import to_profile_dto
from models.profile import ProfileDTO

logger = get_logger(__name__)

router = APIRouter()


@router.get("")
def get_profiles_v3() -> list[ProfileDTO]:
    try:
        dao = PostgresProfileDAO()
        profiles = dao.get_all_profiles()
        if profiles is None or (hasattr(profiles, '__len__') and len(profiles) == 0):
            # Return empty list instead of failing if database is unavailable
            return []
        return [to_profile_dto(profile) for profile in profiles]
    except Exception as e:
        logger.error(f"Error retrieving profiles: {e}")
        # Return empty list instead of failing if database is unavailable
        return []


@router.get("/{profile_handle}")
async def get_profile_by_handle_v3(profile_handle: str) -> ProfileDTO:
    try:
        dao = PostgresProfileDAO()
        profile = dao.get_profile_by_handle(profile_handle)
        
        if not profile:
            # Profile doesn't exist, fetch from API and save
            from config.logging_config import get_logger
            logger = get_logger(__name__)
            logger.info(f"Profile {profile_handle} not found in database, fetching from API")
            from services.api import fetch_profile_from_suno
            data = fetch_profile_from_suno(profile_handle)
            if not data:
                raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found")
            profile = dao.save_profile_with_relationships(data)
            if profile:
                return to_profile_dto(profile)
            else:
                raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found")
        else:
            # Profile exists, check if it has clips or playlists
            from config.logging_config import get_logger
            logger = get_logger(__name__)
            clips_count = len(profile.clips) if profile.clips else 0
            playlists_count = len(profile.playlists) if profile.playlists else 0
            
            logger.info(f"Profile exists: {profile.handle}, clips count: {clips_count}, playlists count: {playlists_count}")
            
            # If no clips or playlists, fetch fresh data from API to update relationships
            if clips_count == 0 or playlists_count == 0:
                logger.info(f"Profile {profile_handle} has no clips or playlists, fetching fresh data to update relationships")
                from services.api import fetch_profile_from_suno
                data = fetch_profile_from_suno(profile_handle)
                if data:
                    profile = dao.save_profile_with_relationships(data)
            else:
                logger.info(f"Profile {profile_handle} already has clips and playlists, but reloading with relationships")
                # Even if the profile has clips and playlists, reload it to ensure relationships are properly loaded
                profile = dao.get_profile_by_handle(profile_handle)  # This will reload with joined relationships
        
            if profile:
                return to_profile_dto(profile)
            else:
                raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found")
    
    except HTTPException:
        raise
    except Exception as e:
        from config.logging_config import get_logger
        logger = get_logger(__name__)
        logger.error(f"Error retrieving profile '{profile_handle}': {e}")
        # Return a 404 instead of 500 if database is unavailable
        raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found or database unavailable")
    