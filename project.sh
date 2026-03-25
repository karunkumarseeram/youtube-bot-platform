#!/bin/bash

echo "🚀 Setting up youtube-bot-platform structure..."

# Create directories
mkdir -p backend/app/{models,schemas,api/routes,services,workers,utils}
mkdir -p backend/migrations/versions
mkdir -p backend/tests
mkdir -p frontend/{public,src}
mkdir -p docs

# Backend core
touch backend/app/__init__.py
touch backend/app/main.py
touch backend/app/config.py
touch backend/app/database.py

# Models
touch backend/app/models/__init__.py
touch backend/app/models/user.py
touch backend/app/models/video.py
touch backend/app/models/bot_job.py
touch backend/app/models/metrics.py
touch backend/app/models/proxy.py

# Schemas
touch backend/app/schemas/__init__.py
touch backend/app/schemas/user.py
touch backend/app/schemas/video.py
touch backend/app/schemas/bot.py
touch backend/app/schemas/metrics.py

# API
touch backend/app/api/__init__.py
touch backend/app/api/routes/__init__.py
touch backend/app/api/routes/auth.py
touch backend/app/api/routes/videos.py
touch backend/app/api/routes/bots.py
touch backend/app/api/routes/metrics.py

# Services
touch backend/app/services/__init__.py
touch backend/app/services/youtube_service.py
touch backend/app/services/bot_service.py
touch backend/app/services/view_engine.py
touch backend/app/services/engagement_service.py

# Workers
touch backend/app/workers/__init__.py
touch backend/app/workers/celery_app.py
touch backend/app/workers/tasks.py

# Utils
touch backend/app/utils/__init__.py
touch backend/app/utils/logger.py
touch backend/app/utils/security.py
touch backend/app/utils/youtube_utils.py
touch backend/app/utils/proxies.py
touch backend/app/utils/http_utils.py

# Migrations
touch backend/migrations/alembic.ini
touch backend/migrations/env.py
touch backend/migrations/script.py.mako

# Tests
touch backend/tests/__init__.py
touch backend/tests/conftest.py
touch backend/tests/test_auth.py
touch backend/tests/test_videos.py
touch backend/tests/test_bots.py
touch backend/tests/test_services.py

# Backend root files (skip README, .gitignore, LICENSE)
touch backend/requirements.txt
touch backend/.env
touch backend/.env.example
touch backend/Dockerfile
touch backend/docker-compose.yml

# Frontend
touch frontend/package.json
touch frontend/Dockerfile

# Docs
touch docs/API.md
touch docs/SETUP.md
touch docs/ARCHITECTURE.md

echo "✅ Project structure created successfully!"