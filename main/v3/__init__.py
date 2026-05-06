from fastapi import APIRouter
from v3.playlists import router as v3_playlists_router
from v3.profiles import router as v3_profiles_router
from v3.clips import router as v3_clips_router

router = APIRouter()

router.include_router(v3_playlists_router, prefix="/playlists", tags=["playlist-v3"])
router.include_router(v3_profiles_router, prefix="/profiles", tags=["profiles-v3"])
router.include_router(v3_clips_router, prefix="/clips", tags=["clip-v3"])

from .clips import router as clips_router
from .playlists import router as playlists_router
from .profiles import router as profiles_router

__all__ = ["clips_router", "playlists_router", "profiles_router"]
