from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.postgres_dao import PostgresProfileDAO
from services.profile_service import ProfileService
from config.logging_config import get_logger
from database.postgres_connection import get_db
from services.mappers import to_profile_dto, to_clip_dto, to_playlist_dto
from models.profile import ProfileDTO

logger = get_logger(__name__)

router = APIRouter()


@router.get("")
def get_profiles_v3(db: Session = Depends(get_db)) -> list[ProfileDTO]:
    try:
        profiles = PostgresProfileDAO(db).get_all_profiles()
        return [to_profile_dto(profile) for profile in profiles]
    except Exception as e:
        logger.error(f"Error retrieving profiles: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{profile_handle}")
async def get_profile_by_handle_v3(profile_handle: str, db: Session = Depends(get_db)) -> ProfileDTO:
    try:
        profile_service = ProfileService(db)
        profile_dto = profile_service.get_profile_by_handle(profile_handle)
        if not profile_dto:
            raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found")
        
        return profile_dto
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving profile '{profile_handle}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    