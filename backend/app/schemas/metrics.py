"""
Metrics Schemas (Pydantic Models)
Python 3.14.3 Compatible
"""

from pydantic import BaseModel, Field
from datetime import datetime


class MetricsResponse(BaseModel):
    """Metrics Response Schema"""
    id: int
    video_id: int
    views: int
    likes: int
    comments: int
    shares: int
    watch_time: float
    average_view_duration: float
    engagement_rate: float
    timestamp: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "video_id": 1,
                "views": 5000,
                "likes": 250,
                "comments": 50,
                "shares": 10,
                "watch_time": 100.5,
                "average_view_duration": 45.2,
                "engagement_rate": 0.06,
                "timestamp": "2024-01-15T10:30:00"
            }
        }