from fastapi import APIRouter
from routes.v2.playlists import router as v2_playlists_router
from routes.v2.users import router as v2_users_router
from routes.v2.profiles import router as v2_profiles_router
from routes.v2.clips import router as v2_clips_router

router = APIRouter()

router.include_router(v2_playlists_router, prefix="/playlist", tags=["playlist-v2"])
router.include_router(v2_users_router, prefix="/users", tags=["users-v2"])
router.include_router(v2_profiles_router, prefix="/profiles", tags=["profiles-v2"])
router.include_router(v2_clips_router, prefix="/clip", tags=["clip-v2"])