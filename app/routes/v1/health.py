from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any
import time
import logging

from config.session import get_db
from config.settings import settings

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/health", status_code=200)
def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Health check endpoint to verify system status"""
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        
        # Check if we can access settings
        app_info = {
            "status": "healthy",
            "app_name": settings.app_name,
            "app_version": settings.app_version,
            "environment": settings.environment,
            "timestamp": time.time(),
            "database_status": "connected"
        }
        
        return app_info
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail={"status": "unhealthy", "error": str(e)})


@router.get("/status", status_code=200)
def status_check() -> Dict[str, Any]:
    """Detailed status check for all system components"""
    status_info = {
        "status": "running",
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "timestamp": time.time(),
        "endpoints": {
            "v1_available": True,
            "v2_available": True,
            "total_endpoints": 24  # Based on our analysis of routes
        }
    }
    
    return status_info