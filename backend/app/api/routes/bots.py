"""
Bots Routes
Python 3.14.3 Compatible
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.schemas.bot import BotJobCreate, BotJobResponse, BotJobUpdate
from app.models.bot_job import BotJob
from app.services.bot_service import BotService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=BotJobResponse, status_code=status.HTTP_201_CREATED)
def create_bot(
    bot: BotJobCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create new bot job"""
    bot_service = BotService(db)
    db_bot = bot_service.create_bot_job(
        user_id=user_id,
        video_id=bot.video_id,
        target_views=bot.target_views,
        target_likes=bot.target_likes,
        target_comments=bot.target_comments,
        daily_increment=bot.daily_increment,
        watch_time_seconds=bot.watch_time_seconds,
        engagement_ratio=bot.engagement_ratio,
        use_proxy=bot.use_proxy
    )
    
    if not db_bot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Video not found"
        )
    
    return db_bot


@router.get("/{bot_id}", response_model=BotJobResponse)
def get_bot(bot_id: int, db: Session = Depends(get_db)):
    """Get bot job details"""
    bot = db.query(BotJob).filter(BotJob.id == bot_id).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot job not found"
        )
    
    return bot


@router.get("/user/{user_id}", response_model=List[BotJobResponse])
def get_user_bots(user_id: int, db: Session = Depends(get_db)):
    """Get all bot jobs for user"""
    bot_service = BotService(db)
    bots = bot_service.get_user_bot_jobs(user_id)
    return bots


@router.post("/{bot_id}/start")
def start_bot(bot_id: int, db: Session = Depends(get_db)):
    """Start bot job"""
    bot_service = BotService(db)
    bot = bot_service.start_bot(bot_id)
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot job not found"
        )
    
    return {"message": "Bot started", "status": bot.status, "bot_id": bot.id}


@router.post("/{bot_id}/pause")
def pause_bot(bot_id: int, db: Session = Depends(get_db)):
    """Pause bot job"""
    bot_service = BotService(db)
    bot = bot_service.pause_bot(bot_id)
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot job not found"
        )
    
    return {"message": "Bot paused", "status": bot.status}


@router.post("/{bot_id}/stop")
def stop_bot(bot_id: int, db: Session = Depends(get_db)):
    """Stop bot job"""
    bot_service = BotService(db)
    bot = bot_service.stop_bot(bot_id)
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot job not found"
        )
    
    return {"message": "Bot stopped", "status": bot.status}


@router.put("/{bot_id}", response_model=BotJobResponse)
def update_bot(
    bot_id: int,
    bot_update: BotJobUpdate,
    db: Session = Depends(get_db)
):
    """Update bot job"""
    bot = db.query(BotJob).filter(BotJob.id == bot_id).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot job not found"
        )
    
    if bot_update.target_views is not None:
        bot.target_views = bot_update.target_views
    if bot_update.daily_increment is not None:
        bot.daily_increment = bot_update.daily_increment
    if bot_update.watch_time_seconds is not None:
        bot.watch_time_seconds = bot_update.watch_time_seconds
    if bot_update.engagement_ratio is not None:
        bot.engagement_ratio = bot_update.engagement_ratio
    
    try:
        db.commit()
        db.refresh(bot)
        return bot
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating bot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update bot"
        )


@router.delete("/{bot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bot(bot_id: int, db: Session = Depends(get_db)):
    """Delete bot job"""
    bot = db.query(BotJob).filter(BotJob.id == bot_id).first()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bot job not found"
        )
    
    try:
        db.delete(bot)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting bot: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete bot"
        )