# Installation Guide

## Prerequisites

Before installing DocuBotAI, ensure you have the following prerequisites:

- Python 3.9 or higher
- pip (Python package installer)
- Redis server
- PostgreSQL database
- Git (for version control)

## Installation Methods

### 1. Using pip (Recommended)

```bash
pip install docubotai
```

### 2. From Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DocuBotAI.git
cd DocuBotAI
```

2. Install in development mode:
```bash
pip install -e ".[dev]"
```

## Configuration

1. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

2. Update the following environment variables:
```env
# API Keys
APIFY_API_KEY=your_apify_key
CLAUDE_API_KEY=your_claude_key
TESTSPRITES_API_KEY=your_testsprites_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/docubotai

# Redis/Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Application Settings
LOG_LEVEL=INFO
MAX_SCRAPING_DEPTH=3
ADMIN_API_KEY=your_admin_key

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4
```

## Running the Application

1. Start the Redis server:
```bash
redis-server
```

2. Start the Celery worker:
```bash
celery -A docubotai.tasks worker --loglevel=info
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the FastAPI server:
```bash
uvicorn docubotai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t docubotai .
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

## Verification

1. Check the API documentation at:
```
http://localhost:8000/docs
```

2. Test the health endpoint:
```bash
curl http://localhost:8000/health
```

## Troubleshooting

### Common Issues

1. Database Connection:
- Ensure PostgreSQL is running
- Verify DATABASE_URL in .env
- Check database user permissions

2. Redis Connection:
- Verify Redis server is running
- Check REDIS_URL in .env
- Ensure port 6379 is available

3. API Key Issues:
- Verify all API keys are correctly set in .env
- Check API key permissions and quotas

### Getting Help

- Check the [GitHub Issues](https://github.com/yourusername/DocuBotAI/issues)
- Join our [Discord Community](https://discord.gg/docubotai)
- Contact support at support@docubotai.com