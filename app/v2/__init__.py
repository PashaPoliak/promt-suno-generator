from fastapi import APIRouter
from v2.playlists import router as v2_playlists_router
from v2.users import router as v2_users_router
from v2.profiles import router as v2_profiles_router
from v2.clips import router as v2_clips_router

router = APIRouter()

router.include_router(v2_playlists_router, prefix="/playlists", tags=["playlist-v2"])
router.include_router(v2_users_router, prefix="/users", tags=["users-v2"])
router.include_router(v2_profiles_router, prefix="/profiles", tags=["profiles-v2"])
router.include_router(v2_clips_router, prefix="/clips", tags=["clip-v2"])

from .clips import router as clips_router
from .playlists import router as playlists_router
from .profiles import router as profiles_router

__all__ = ["clips_router", "playlists_router", "profiles_router"]
