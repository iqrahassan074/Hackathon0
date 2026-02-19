# Railway Deployment Guide

This project can be deployed to Railway as two separate services (recommended) or as a monorepo.

## Option 1: Two Separate Services (Recommended)

### Backend Service

1. **Create New Service** → GitHub Repo → Select your repo
2. **Configure Root Directory**: `backend`
3. **Railway will auto-detect Python**
4. **Set Start Command**:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
5. **Add Environment Variables**:
   - `DATABASE_URL`: `sqlite:///./hackathon.db`
   - `SECRET_KEY`: Generate a random 32+ character string
   - `ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `60`
   - `AI_PROVIDER`: `claude` (or `gemini`, `qwen`)
   - `FRONTEND_URL`: Your frontend Railway URL (add after deploying frontend)
   - `LOG_LEVEL`: `INFO`

### Frontend Service

1. **Create New Service** → GitHub Repo → Select the same repo
2. **Configure Root Directory**: `frontend`
3. **Railway will auto-detect Node.js**
4. **Build Command**: `npm run build`
5. **Start Command**: `npx serve -s dist -l $PORT`
6. **Add Environment Variables**:
   - `VITE_API_URL`: Your backend Railway URL + `/api/v1`
     Example: `https://your-backend.up.railway.app/api/v1`

### Connect the Services

1. After both services are deployed, update the frontend's `VITE_API_URL` to point to the backend's Railway URL
2. Update the backend's `FRONTEND_URL` to point to the frontend's Railway URL (for CORS)

---

## Option 2: Monorepo with Nixpacks

The project includes `nixpacks.toml` files for each service directory.

### Deploy Backend

```bash
cd backend
railway up
```

### Deploy Frontend

```bash
cd frontend
railway up
```

---

## Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./hackathon.db
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
AI_PROVIDER=claude
FRONTEND_URL=https://your-frontend.up.railway.app
LOG_LEVEL=INFO
```

### Frontend (.env)
```
VITE_API_URL=https://your-backend.up.railway.app/api/v1
```

---

## Troubleshooting

### "Cannot find module '/app/index.js'"

This error occurs when Railway tries to run the project as a Node.js app from the root directory.

**Solution**: Set the correct root directory for each service:
- Backend service: `backend`
- Frontend service: `frontend`

### CORS Errors

Make sure the backend's `FRONTEND_URL` matches your frontend's Railway URL exactly.

### Database Persistence

SQLite is used by default. For production, consider using PostgreSQL:
1. Add PostgreSQL database in Railway
2. Update `DATABASE_URL` environment variable

---

## Post-Deployment Checklist

- [ ] Backend health check passes: `https://your-backend.up.railway.app/health`
- [ ] API docs accessible: `https://your-backend.up.railway.app/docs`
- [ ] Frontend loads: `https://your-frontend.up.railway.app`
- [ ] User registration works
- [ ] User login works
- [ ] Frontend can communicate with backend API
- [ ] CORS is properly configured

---

## Useful Commands

### Local Testing Before Deploy

```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

### View Railway Logs

```bash
railway logs
```

### Open Railway Dashboard

```bash
railway open
```
