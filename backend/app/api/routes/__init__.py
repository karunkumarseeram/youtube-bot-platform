"""
API Package
Python 3.14.3 Compatible
"""

from fastapi import APIRouter
from app.api.routes import auth, videos, bots, metrics

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(videos.router, prefix="/videos", tags=["videos"])
router.include_router(bots.router, prefix="/bots", tags=["bots"])
router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])