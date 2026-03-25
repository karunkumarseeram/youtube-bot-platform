# """
# YouTube Bot Platform - Main Application Package
# Python 3.14.3 Compatible
# """

# __version__ = "1.0.0"
# __author__ = "YouTube Bot Team"

# import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )


"""
API Package
Python 3.14.3 Compatible
"""

from fastapi import APIRouter
from app.api.routes import auth, videos, bots, metrics

# Create main router
router = APIRouter()

# Include all route modules
router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(videos.router, prefix="/videos", tags=["videos"])
router.include_router(bots.router, prefix="/bots", tags=["bots"])
router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])

# Export router
__all__ = ["router"]