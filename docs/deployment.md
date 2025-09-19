# Deployment Guide

## Deployment Options

### 1. Docker Deployment (Recommended)

#### Prerequisites
- Docker
- Docker Compose
- Domain name (optional)
- SSL certificate (optional)

#### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DocuBotAI.git
cd DocuBotAI
```

2. Create and configure `.env`:
```bash
cp .env.example .env
# Edit .env with your production settings
```

3. Build and start services:
```bash
docker-compose up -d
```

4. Run migrations:
```bash
docker-compose exec app alembic upgrade head
```

### 2. Manual Deployment

#### Prerequisites
- Python 3.9+
- PostgreSQL
- Redis
- Nginx
- Supervisor
- SSL certificate

#### Steps

1. Install system dependencies:
```bash
# Ubuntu/Debian
apt-get update
apt-get install python3-pip postgresql redis-server nginx supervisor

# CentOS/RHEL
dnf install python3-pip postgresql redis nginx supervisor
```

2. Create database:
```bash
sudo -u postgres psql
CREATE DATABASE docubotai;
CREATE USER docubotai WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE docubotai TO docubotai;
```

3. Install application:
```bash
pip install docubotai
```

4. Configure Supervisor:
```ini
[program:docubotai]
command=/usr/local/bin/uvicorn docubotai.api.main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/opt/docubotai
user=docubotai
autostart=true
autorestart=true
stderr_logfile=/var/log/docubotai/err.log
stdout_logfile=/var/log/docubotai/out.log

[program:docubotai-worker]
command=/usr/local/bin/celery -A docubotai.tasks worker --loglevel=info
directory=/opt/docubotai
user=docubotai
autostart=true
autorestart=true
stderr_logfile=/var/log/docubotai/celery-err.log
stdout_logfile=/var/log/docubotai/celery-out.log
```

5. Configure Nginx:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Scaling

### Horizontal Scaling

1. Load Balancer Setup:
```nginx
upstream docubotai {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://docubotai;
    }
}
```

2. Session Persistence:
- Use Redis for session storage
- Configure sticky sessions if needed

3. Worker Scaling:
```bash
celery -A docubotai.tasks worker --loglevel=info --concurrency=8
```

### Vertical Scaling

1. Application Server:
- Increase worker count
- Optimize uvicorn settings
- Use PyPy for performance

2. Database:
- Increase connection pool
- Optimize PostgreSQL settings
- Consider read replicas

3. Redis:
- Enable persistence
- Increase maxmemory
- Configure eviction policies

## Monitoring

### 1. Prometheus Setup

```yaml
scrape_configs:
  - job_name: 'docubotai'
    static_configs:
      - targets: ['localhost:8000']
```

### 2. Grafana Dashboard

Import the provided dashboard:
- System metrics
- API endpoints
- Task queues
- Error rates

### 3. Logging

Configure centralized logging:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/docubotai/app.log',
            'maxBytes': 10485760,
            'backupCount': 5,
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    }
}
```

## Backup Strategy

### 1. Database Backup

Daily backup script:
```bash
#!/bin/bash
BACKUP_DIR="/backup/docubotai"
DATE=$(date +%Y%m%d)
pg_dump docubotai > "$BACKUP_DIR/db_$DATE.sql"
```

### 2. Document Storage

Backup embedded documents:
```bash
rsync -av /data/documents/ /backup/documents/
```

### 3. Configuration

Backup environment and config:
```bash
cp /opt/docubotai/.env /backup/config/
cp -r /opt/docubotai/config/ /backup/config/
```

## Security

### 1. SSL Configuration

```nginx
server {
    listen 443 ssl;
    server_name your_domain.com;

    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

### 2. Firewall Rules

```bash
# Allow HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Allow PostgreSQL only from internal network
ufw allow from 10.0.0.0/8 to any port 5432
```

### 3. Security Headers

```nginx
add_header Strict-Transport-Security "max-age=31536000";
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header Content-Security-Policy "default-src 'self'";
```

## Troubleshooting

### Common Issues

1. Connection Errors:
```bash
# Check service status
systemctl status docubotai
systemctl status postgresql
systemctl status redis

# Check logs
tail -f /var/log/docubotai/err.log
```

2. Performance Issues:
```bash
# Monitor resources
top
htop
pg_top

# Check slow queries
SELECT * FROM pg_stat_activity WHERE state = 'active';
```

3. Memory Issues:
```bash
# Monitor memory
free -m
vmstat 1

# Check Redis memory
redis-cli info memory
```

### Support

For additional support:
- Documentation: https://docs.docubotai.com
- Issues: https://github.com/yourusername/DocuBotAI/issues
- Email: support@docubotai.com