from fastapi import APIRouter, HTTPException, Depends
from v3.postgres_dao import PostgresProfileDAO
from config.logging_config import get_logger
from services.mappers import to_profile_dto
from models.profile import ProfileDTO
from services.api import fetch_profile_from_suno


logger = get_logger(__name__)

router = APIRouter()


@router.get("")
def get_profiles_v3() -> list[ProfileDTO]:
    try:
        dao = PostgresProfileDAO()
        profiles = dao.get_all_profiles()
        if profiles is None or (hasattr(profiles, '__len__') and len(profiles) == 0):
            return []
        return [to_profile_dto(profile) for profile in profiles]
    except Exception as e:
        logger.error(f"Error retrieving profiles: {e}")
        return []


@router.get("/{profile_handle}")
def get_profile_by_handle_v3(profile_handle: str) -> ProfileDTO:
    try:
        dao = PostgresProfileDAO()
        profile = dao.get_profile_by_handle(profile_handle)
        
        if not profile:

            data = fetch_profile_from_suno(profile_handle)
            if not data:
                raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found")
            profile = dao.save_profile_with_relationships(data)
            if profile:
                return to_profile_dto(profile)
            else:
                raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found")
        else:
            clips_count = len(profile.clips) if profile.clips else 0
            playlists_count = len(profile.playlists) if profile.playlists else 0
            
            
            if clips_count == 0 or playlists_count == 0:
                data = fetch_profile_from_suno(profile_handle)
                if data:
                    profile = dao.save_profile_with_relationships(data)
                else:
                    profile = dao.get_profile_by_handle(profile_handle)
            else:
                profile = dao.get_profile_by_handle(profile_handle)
        
            if profile:
                return to_profile_dto(profile)
            else:
                raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found")
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found or database unavailable")
