"""
Workers Package
Python 3.14.3 Compatible
"""

from app.workers.celery_app import celery_app

__all__ = ["celery_app"]