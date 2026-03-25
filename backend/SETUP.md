# YouTube Bot Platform - Setup Guide (Python 3.14.3)

## Prerequisites
- Python 3.14.3
- Docker & Docker Compose (optional)
- PostgreSQL 15+ (if not using Docker)
- Redis 7+ (if not using Docker)
- Git

## Installation Methods

### Method 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone <your-repo-url>
cd youtube-bot-platform/backend

# Copy environment file
cp .env.example .env

# Build and start containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f fastapi

# Stop services
docker-compose down