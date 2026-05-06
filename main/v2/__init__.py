from fastapi import APIRouter
from .playlists import router as v2_playlists_router
from .users import router as v2_users_router
from .profiles import router as v2_profiles_router
from .clips import router as v2_clips_router

router = APIRouter()

router.include_router(v2_playlists_router, prefix="/playlists", tags=["playlist-v2"])
router.include_router(v2_users_router, prefix="/users", tags=["users-v2"])
router.include_router(v2_profiles_router, prefix="/profiles", tags=["profiles-v2"])
router.include_router(v2_clips_router, prefix="/clips", tags=["clip-v2"])

from .clips import router as clips_router
from .playlists import router as playlists_router
from .profiles import router as profiles_router

__all__ = ["clips_router", "playlists_router", "profiles_router"]
