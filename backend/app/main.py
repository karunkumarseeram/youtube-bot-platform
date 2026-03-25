"""
Main FastAPI Application
Python 3.14.3 Compatible
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import router
from app.database import Base, engine, init_db
from app.config import get_settings
from app.utils.logger import get_logger
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/app.log')
    ]
)

logger = get_logger(__name__)
settings = get_settings()

# Initialize database
try:
    init_db()
except Exception as e:
    logger.error(f"Database initialization error: {str(e)}")

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="YouTube Video Watch Time & View Bot Platform - Python 3.14.3",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🎬 YouTube Bot Platform",
        "version": settings.app_version,
        "python_version": sys.version,
        "status": "✅ Running",
        "environment": settings.env
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "✅ Healthy",
        "app": settings.app_name,
        "environment": settings.env
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting YouTube Bot Platform...")
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Environment: {settings.env}")
    logger.info(f"Debug Mode: {settings.debug}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )