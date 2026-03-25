"""
Celery Tasks
Python 3.14.3 Compatible
"""

import time
import random
from app.workers.celery_app import celery_app
from app.database import SessionLocal
from app.models.bot_job import BotJob, BotStatus
from app.models.metrics import Metrics
from app.services.view_engine import ViewSimulationEngine
from app.services.engagement_service import EngagementService
from app.services.bot_service import BotService
from app.utils.logger import get_logger
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


@celery_app.task(name="start_bot_task", bind=True)
def start_bot_task(self, job_id: int):
    """Start bot simulation for a job"""
    db = SessionLocal()
    try:
        job = db.query(BotJob).filter(BotJob.id == job_id).first()
        if not job:
            logger.error(f"Job not found: {job_id}")
            return {"status": "error", "message": "Job not found"}
        
        job.status = BotStatus.RUNNING
        db.commit()
        
        logger.info(f"🤖 Starting bot job {job_id} for video {job.video_id}")
        
        # Simulate views
        view_engine = ViewSimulationEngine(
            watch_time_seconds=job.watch_time_seconds,
            engagement_ratio=job.engagement_ratio
        )
        engagement_service = EngagementService()
        bot_service = BotService(db)
        
        current_views = job.current_views
        current_likes = job.current_likes
        current_comments = job.current_comments
        
        # Simulate views until target reached
        while current_views < job.target_views:
            # Refresh job status
            job = db.query(BotJob).filter(BotJob.id == job_id).first()
            if job.status != BotStatus.RUNNING:
                logger.info(f"🛑 Bot job {job_id} stopped or paused")
                break
            
            # Simulate view
            view_data = view_engine.generate_view()
            current_views += 1
            
            # Generate engagement
            if view_data['like']:
                current_likes += 1
            
            if view_data['comment']:
                current_comments += 1
            
            # Update progress every 10 views
            if current_views % 10 == 0:
                bot_service.update_bot_progress(
                    job_id,
                    current_views,
                    current_likes,
                    current_comments
                )
                
                # Save metrics
                metric = Metrics(
                    video_id=job.video_id,
                    views=current_views,
                    likes=current_likes,
                    comments=current_comments,
                    engagement_rate=(current_likes + current_comments) / current_views if current_views > 0 else 0
                )
                db.add(metric)
                db.commit()
                
                logger.info(f"📊 Bot {job_id} progress: {current_views}/{job.target_views} views ({(current_views/job.target_views*100):.1f}%)")
                
                # Update Celery task state
                self.update_state(
                    state='PROGRESS',
                    meta={'current': current_views, 'total': job.target_views, 'percentage': (current_views/job.target_views*100)}
                )
                
                # Simulate delay between view bursts
                delay = random.uniform(0.1, 0.5)
                time.sleep(delay)
            else:
                # Small delay between views
                time.sleep(random.uniform(0.05, 0.2))
        
        # Mark as completed
        job = db.query(BotJob).filter(BotJob.id == job_id).first()
        job.status = BotStatus.COMPLETED
        job.completed_at = datetime.now(timezone.utc)
        job.current_views = current_views
        job.current_likes = current_likes
        job.current_comments = current_comments
        db.commit()
        
        logger.info(f"✅ Bot job {job_id} completed: {current_views} views, {current_likes} likes, {current_comments} comments")
        return {
            "status": "completed",
            "views": current_views,
            "likes": current_likes,
            "comments": current_comments
        }
    
    except Exception as e:
        logger.error(f"❌ Error in bot task: {str(e)}")
        try:
            job = db.query(BotJob).filter(BotJob.id == job_id).first()
            if job:
                job.status = BotStatus.FAILED
                job.error_message = str(e)
                db.commit()
        except:
            pass
        
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@celery_app.task(name="fetch_youtube_stats")
def fetch_youtube_stats(video_id: int):
    """Fetch real YouTube statistics for a video"""
    db = SessionLocal()
    try:
        from app.models.video import Video
        from app.models.metrics import Metrics
        
        video = db.query(Video).filter(Video.id == video_id).first()
        if not video:
            return {"status": "error", "message": "Video not found"}
        
        logger.info(f"📺 Fetching stats for video {video.video_id}")
        
        # Save metrics snapshot
        metric = Metrics(
            video_id=video_id,
            views=video.current_views,
            likes=video.current_likes,
            comments=video.current_comments
        )
        db.add(metric)
        db.commit()
        
        return {"status": "success", "video_id": video_id}
    
    except Exception as e:
        logger.error(f"❌ Error fetching stats: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()