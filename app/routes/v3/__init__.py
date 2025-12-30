from .clips import router as clips_router
from .playlists import router as playlists_router
from .profiles import router as profiles_router

__all__ = ["clips_router", "playlists_router", "profiles_router"]