# Ted Sink Law Voice Receptionist AI - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Ted Sink Law Voice Receptionist AI system in various environments, from local development to production.

## Prerequisites

### System Requirements

- **CPU**: 4+ cores recommended
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 50GB+ available space
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **Network**: Stable internet connection for API calls

### Software Requirements

- **Python**: 3.11+
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: Latest version
- **PostgreSQL**: 13+ (if not using Docker)

### API Keys Required

- **OpenAI API Key**: For GPT-4 conversation handling
- **ElevenLabs API Key**: For text-to-speech generation

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ted-sink-law-voice-ai
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file with your API keys:

```bash
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 3. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Run the Application

```bash
# Start the application
python main.py
```

The API will be available at `http://localhost:8000`

### 5. Test the Installation

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test text conversation
curl -X POST http://localhost:8000/conversation/text \
  -H "Content-Type: application/json" \
  -d '{"text_input": "Hello, I need help with a car accident"}'
```

## Docker Deployment

### 1. Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f voice-ai

# Stop services
docker-compose down
```

### 2. Individual Docker Commands

```bash
# Build the image
docker build -t ted-sink-law-voice-ai .

# Run the container
docker run -d \
  --name voice-ai \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e ELEVENLABS_API_KEY=your_key \
  ted-sink-law-voice-ai
```

## Production Deployment

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create application directory
sudo mkdir -p /opt/ted-sink-law-ai
sudo chown $USER:$USER /opt/ted-sink-law-ai
```

### 2. Application Deployment

```bash
# Clone repository
cd /opt/ted-sink-law-ai
git clone <repository-url> .

# Set up environment
cp .env.example .env
# Edit .env with production values

# Create necessary directories
mkdir -p logs audio_files

# Start services
docker-compose up -d
```

### 3. SSL Certificate Setup

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 4. Nginx Configuration

Create `/etc/nginx/sites-available/ted-sink-law-ai`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /audio/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/ted-sink-law-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Database Setup

### 1. PostgreSQL Setup (if not using Docker)

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql

CREATE DATABASE ted_sink_law;
CREATE USER ted_sink_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ted_sink_law TO ted_sink_user;
\q
```

### 2. Database Migrations

```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init migrations

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head
```

## Monitoring and Logging

### 1. Log Management

```bash
# View application logs
docker-compose logs -f voice-ai

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Set up log rotation
sudo nano /etc/logrotate.d/ted-sink-law-ai
```

### 2. Monitoring Setup

```bash
# Access Prometheus
http://your-domain.com:9090

# Access Grafana
http://your-domain.com:3000
# Default credentials: admin/admin123
```

### 3. Health Checks

```bash
# Create health check script
cat > /opt/ted-sink-law-ai/health-check.sh << 'EOF'
#!/bin/bash
curl -f http://localhost:8000/health || exit 1
EOF

chmod +x /opt/ted-sink-law-ai/health-check.sh

# Add to crontab for regular checks
crontab -e
# Add: */5 * * * * /opt/ted-sink-law-ai/health-check.sh
```

## Security Considerations

### 1. Firewall Configuration

```bash
# Configure UFW
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. API Key Security

```bash
# Store API keys securely
sudo mkdir -p /etc/ted-sink-law-ai
sudo chmod 700 /etc/ted-sink-law-ai
sudo nano /etc/ted-sink-law-ai/api-keys.env
```

### 3. Regular Updates

```bash
# Create update script
cat > /opt/ted-sink-law-ai/update.sh << 'EOF'
#!/bin/bash
cd /opt/ted-sink-law-ai
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
EOF

chmod +x /opt/ted-sink-law-ai/update.sh
```

## Backup and Recovery

### 1. Database Backup

```bash
# Create backup script
cat > /opt/ted-sink-law-ai/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/ted-sink-law-ai"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database backup
docker-compose exec -T postgres pg_dump -U ted_sink_user ted_sink_law > $BACKUP_DIR/db_backup_$DATE.sql

# Audio files backup
tar -czf $BACKUP_DIR/audio_backup_$DATE.tar.gz audio_files/

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x /opt/ted-sink-law-ai/backup.sh

# Add to crontab
crontab -e
# Add: 0 2 * * * /opt/ted-sink-law-ai/backup.sh
```

### 2. Disaster Recovery

```bash
# Restore database
docker-compose exec -T postgres psql -U ted_sink_user ted_sink_law < backup_file.sql

# Restore audio files
tar -xzf audio_backup.tar.gz
```

## Performance Optimization

### 1. Resource Limits

```yaml
# Add to docker-compose.yml
services:
  voice-ai:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

### 2. Caching

```bash
# Redis configuration
# Add to docker-compose.yml
services:
  redis:
    command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

### 3. Load Balancing

```nginx
# Nginx upstream configuration
upstream voice_ai_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   ```bash
   # Check environment variables
   docker-compose exec voice-ai env | grep API_KEY
   ```

2. **Database Connection Issues**
   ```bash
   # Test database connection
   docker-compose exec postgres psql -U ted_sink_user -d ted_sink_law -c "SELECT 1;"
   ```

3. **Audio Processing Issues**
   ```bash
   # Check audio file permissions
   ls -la /tmp/audio_files/
   
   # Check ffmpeg installation
   docker-compose exec voice-ai ffmpeg -version
   ```

4. **Memory Issues**
   ```bash
   # Monitor memory usage
   docker stats
   
   # Check system memory
   free -h
   ```

### Log Analysis

```bash
# Search for errors
docker-compose logs voice-ai | grep ERROR

# Monitor real-time logs
docker-compose logs -f --tail=100 voice-ai

# Export logs for analysis
docker-compose logs voice-ai > voice_ai_logs.txt
```

## Maintenance

### Regular Maintenance Tasks

1. **Weekly**
   - Review logs for errors
   - Check disk space usage
   - Verify backup completion

2. **Monthly**
   - Update dependencies
   - Review security patches
   - Analyze performance metrics

3. **Quarterly**
   - Full system backup
   - Performance optimization review
   - Security audit

### Update Procedures

```bash
# Application updates
cd /opt/ted-sink-law-ai
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Database migrations
docker-compose exec voice-ai alembic upgrade head
```

## Support and Documentation

- **API Documentation**: Available at `/docs` when running
- **Logs**: Check application logs for detailed error information
- **Monitoring**: Use Grafana dashboards for system health
- **Backup**: Regular backups stored in `/opt/backups/ted-sink-law-ai`

For additional support, refer to the project documentation or contact the development team.