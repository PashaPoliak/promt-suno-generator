from fastapi import APIRouter
from routes.v1.playlists import router as playlists_router
from routes.v1.users import router as users_router
from routes.v1.profiles import router as profiles_router
from routes.v1.clips import router as clips_router
from routes.v1.health import router as health_router
from routes.v1.categories import router as categories_router
from routes.v1.tags import router as tags_router
from routes.v1.templates import router as templates_router
from routes.v1.prompts import router as prompts_router
from config.logging_config import setup_logging

router = APIRouter()

router.include_router(playlists_router, prefix="/playlist", tags=["playlist"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(profiles_router, prefix="/profiles", tags=["profiles"])
router.include_router(clips_router, prefix="/clip", tags=["clip"])

router.include_router(categories_router, prefix="/categories", tags=["categories"])
router.include_router(tags_router, prefix="/tags", tags=["tags"])
router.include_router(templates_router, prefix="/templates", tags=["templates"])
router.include_router(prompts_router, prefix="/prompts", tags=["prompts"])
router.include_router(health_router, prefix="/system", tags=["system"])

setup_logging()
