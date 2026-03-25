"""
Metrics Routes
Python 3.14.3 Compatible
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.schemas.metrics import MetricsResponse
from app.models.metrics import Metrics

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/video/{video_id}", response_model=List[MetricsResponse])
def get_video_metrics(
    video_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get metrics for a video"""
    metrics = db.query(Metrics).filter(
        Metrics.video_id == video_id
    ).order_by(Metrics.timestamp.desc()).limit(limit).all()
    
    if not metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No metrics found for video"
        )
    
    return metrics


@router.get("/latest/video/{video_id}", response_model=MetricsResponse)
def get_latest_video_metrics(
    video_id: int,
    db: Session = Depends(get_db)
):
    """Get latest metrics for a video"""
    metric = db.query(Metrics).filter(
        Metrics.video_id == video_id
    ).order_by(Metrics.timestamp.desc()).first()
    
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No metrics found for video"
        )
    
    return metric