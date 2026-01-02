from fastapi import APIRouter
from app.v1.router_playlists import router as playlists_router
from app.v1.router_users import router as users_router
from app.v1.router_profiles import router as profiles_router
from app.v1.router_clips import router as clips_router

router = APIRouter()

router.include_router(playlists_router, prefix="/playlists", tags=["playlist"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(profiles_router, prefix="/profiles", tags=["profiles"])
router.include_router(clips_router, prefix="/clips", tags=["clip"])

from .router_clips import router as clips_router
from .router_playlists import router as playlists_router
from .router_profiles import router as profiles_router

__all__ = ["clips_router", "playlists_router", "profiles_router"]