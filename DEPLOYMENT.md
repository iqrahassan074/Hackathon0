# Deployment Guide

This guide covers deployment options for Hackathon_0, from local development to production.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites

- **Python**: 3.13.5 or higher
- **Node.js**: v24.x or higher
- **npm**: Latest (comes with Node.js)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify backend: http://localhost:8000/health

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

Verify frontend: http://localhost:5173

---

## Docker Deployment

### Prerequisites

- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher

### Quick Start

```bash
# From project root
docker-compose up --build
```

This starts:
- Backend on http://localhost:8000
- Frontend on http://localhost:3000

### Docker Commands

```bash
# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Stop and remove volumes (resets database)
docker-compose down -v

# Rebuild and restart
docker-compose up -d --build

# Run tests in container
docker-compose exec backend pytest
```

### Production Docker Build

```bash
# Build with production optimizations
docker-compose -f docker-compose.yml build --no-cache

# Tag for registry
docker tag hackathon0-backend:latest your-registry/hackathon0-backend:1.0.0
docker tag hackathon0-frontend:latest your-registry/hackathon0-frontend:1.0.0
```

---

## Production Deployment

### Environment Variables for Production

#### Backend

```bash
# .env.production
DATABASE_URL=postgresql://user:password@host:5432/hackathon0
SECRET_KEY=<generate-strong-random-key-64-chars>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
AI_PROVIDER=claude
AI_CLI_TIMEOUT=30
LOG_LEVEL=WARNING
FRONTEND_URL=https://your-domain.com
```

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

#### Frontend

```bash
# .env.production
VITE_API_URL=https://api.your-domain.com/api/v1
```

### Nginx Reverse Proxy

For production, use Nginx as reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Kubernetes Deployment (Optional)

See `k8s/` directory for Kubernetes manifests.

```bash
# Deploy to Minikube
minikube start
kubectl apply -f k8s/

# Deploy to production cluster
kubectl apply -f k8s/ -n hackathon0
```

---

## Environment Configuration

### Complete Backend Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| DATABASE_URL | Database connection string | sqlite:///./hackathon.db | No |
| SECRET_KEY | JWT signing key | (development key) | Yes (prod) |
| ALGORITHM | JWT algorithm | HS256 | No |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiry | 60 | No |
| AI_PROVIDER | AI provider (claude/qwen) | claude | No |
| AI_CLI_TIMEOUT | AI timeout seconds | 30 | No |
| AI_RATE_LIMIT_PER_MINUTE | Rate limit | 10 | No |
| FRONTEND_URL | CORS allowed origin | http://localhost:5173 | No |
| LOG_LEVEL | Logging level | INFO | No |

### Complete Frontend Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| VITE_API_URL | Backend API URL | http://localhost:8000/api/v1 | Yes |

---

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
# Linux/Mac:
lsof -i :8000

# Kill the process
# Windows:
taskkill /PID <PID> /F
# Linux/Mac:
kill -9 <PID>
```

**Database errors:**
```bash
# Reset SQLite database
rm hackathon.db
# Restart server to recreate
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Port already in use:**
```bash
# Change port in vite.config.js
server: { port: 5174 }
```

**API connection errors:**
```bash
# Check VITE_API_URL in .env
# Ensure backend is running
curl http://localhost:8000/health
```

**Build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs backend

# Verify Dockerfile
docker-compose build --no-cache backend
```

**Volume permission errors:**
```bash
# Remove volumes and recreate
docker-compose down -v
docker-compose up -d
```

**Network issues:**
```bash
# Reset network
docker-compose down
docker network prune
docker-compose up -d
```

### Performance Issues

**Slow API responses:**
1. Check database query performance
2. Enable query logging
3. Consider adding indexes
4. Use PostgreSQL for production

**Frontend slow loading:**
1. Build with optimizations: `npm run build`
2. Enable gzip compression
3. Use CDN for static assets
4. Implement code splitting

---

## Health Checks

### Backend Health
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","version":"1.0.0"}
```

### Frontend Health
```bash
curl http://localhost:3000
# Expected: HTML content
```

### Docker Health
```bash
docker-compose ps
# All services should show "healthy"
```

---

## Backup and Restore

### Database Backup (SQLite)
```bash
# Backup
cp backend/hackathon.db backup-$(date +%Y%m%d).db

# Restore
cp backup-20260216.db backend/hackathon.db
```

### Database Backup (PostgreSQL)
```bash
# Backup
pg_dump hackathon0 > backup.sql

# Restore
psql hackathon0 < backup.sql
```

---

## Security Checklist

- [ ] Change SECRET_KEY to strong random value
- [ ] Use HTTPS in production
- [ ] Set secure database credentials
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Remove debug endpoints
- [ ] Set LOG_LEVEL to WARNING or ERROR
- [ ] Regular dependency updates
- [ ] Enable firewall rules
- [ ] Set up monitoring/alerting

---

## Monitoring

### Application Logs

Backend logs are in JSON format:
```bash
# View logs
docker-compose logs backend

# Export logs
docker-compose logs backend > logs.json
```

### Metrics to Monitor

- API response times (target: < 200ms p95)
- Error rates (target: < 1%)
- Active users
- Task creation rate
- AI recommendation usage

---

## Support

For additional help:
1. Check README.md for general documentation
2. Review API docs at /docs endpoint
3. Check GitHub issues
4. Contact development team
