# Hackathon_0

AI-Powered Task Management Application

## Overview

Hackathon_0 is a full-stack web application that combines task management with AI-powered recommendations. Built with Python/FastAPI backend and React frontend, it helps users organize their tasks and get intelligent suggestions to improve productivity.

## Features

- **User Authentication**: Secure JWT-based authentication
- **Task Management**: Create, read, update, and delete tasks with priorities and due dates
- **AI Recommendations**: Get intelligent task recommendations powered by Claude/Qwen
- **Dashboard**: Visual overview of tasks with statistics
- **Settings**: Customize theme, notifications, and AI preferences
- **Responsive Design**: Works on desktop and mobile devices
- **Docker Support**: Easy deployment with Docker Compose

## Tech Stack

### Backend
- Python 3.13.5
- FastAPI
- SQLAlchemy (ORM)
- SQLite/PostgreSQL
- JWT Authentication
- bcrypt (password hashing)
- structlog (logging)

### Frontend
- React 18
- Vite
- Tailwind CSS
- Zustand (state management)
- React Router
- Axios
- React Hook Form

### DevOps
- Docker
- Docker Compose
- Nginx (production frontend)

## Quick Start

### Prerequisites

- Python 3.13.5 or higher
- Node.js v24.x or higher
- Docker (optional, for containerized deployment)

### Local Development

#### 1. Clone the Repository

```bash
cd hackathon0
```

#### 2. Setup Backend

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

# Copy environment file
cp .env.example .env

# Run the server
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/docs

#### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

### Docker Deployment

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
hackathon0/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # Database setup
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── routes/           # API routes
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utilities
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── pytest.ini
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   ├── store/            # State management
│   │   ├── hooks/            # Custom hooks
│   │   └── utils/            # Utilities
│   ├── package.json
│   ├── Dockerfile
│   └── vite.config.js
├── docker-compose.yml
├── README.md
└── DEPLOYMENT.md
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user
- `PUT /api/v1/auth/password` - Change password
- `POST /api/v1/auth/logout` - Logout

### Tasks
- `GET /api/v1/tasks` - List tasks
- `POST /api/v1/tasks` - Create task
- `GET /api/v1/tasks/{id}` - Get task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `PATCH /api/v1/tasks/{id}/complete` - Mark complete
- `GET /api/v1/tasks/stats` - Get statistics

### Settings
- `GET /api/v1/settings` - Get settings
- `PUT /api/v1/settings` - Update settings

### AI
- `POST /api/v1/ai/recommend` - Get recommendations
- `POST /api/v1/ai/optimize` - Optimize task
- `GET /api/v1/ai/history` - Get history
- `POST /api/v1/ai/history/{id}/accept` - Accept recommendation

## Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Configuration

### Environment Variables

#### Backend (.env)
```
DATABASE_URL=sqlite:///./hackathon.db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
AI_PROVIDER=claude
FRONTEND_URL=http://localhost:5173
```

#### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
```

## AI Integration

The application supports AI-powered task recommendations through:
- **Claude CLI**: Install Claude CLI for recommendations
- **Qwen CLI**: Install Qwen CLI as alternative

To enable AI features:
1. Install the CLI tool of your choice
2. Configure API keys as needed
3. Set `AI_PROVIDER` in backend `.env`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check API documentation at /docs
- Review DEPLOYMENT.md for deployment guide
