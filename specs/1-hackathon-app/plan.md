# Architectural Plan: Hackathon_0 Full-Stack Application

**Feature**: `1-hackathon-app`  
**Version**: 1.0.0  
**Created**: 2026-02-16  
**Status**: Approved  
**References**: [Constitution](../../.specify/memory/constitution.md), [Spec](spec.md)

---

## 1. Executive Summary

This plan provides the technical architecture and implementation roadmap for Hackathon_0, a full-stack web application combining task management with AI-powered recommendations. The system follows a client-server architecture with Python backend (FastAPI), React frontend, and optional containerized deployment.

### 1.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │   Home   │ │Dashboard │ │  Tasks   │ │    Settings      │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │
│                    │ Shared Components (UI Library)             │
└────────────────────┼────────────────────────────────────────────┘
                     │ REST API (JSON/HTTPS)
┌────────────────────┼────────────────────────────────────────────┐
│                   Backend (Python/FastAPI)                      │
│  ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────────┐    │
│  │ Auth Routes  │ │ │ Task Routes  │ │ │  AI Routes       │    │
│  └──────────────┘ │ └──────────────┘ │ └──────────────────┘    │
│         │         │        │         │          │               │
│  ┌──────────────┐ │ ┌──────────────┐ │ ┌──────────────────┐    │
│  │ JWT Service  │ │ │ Task Service │ │ │ AI Recommendation│    │
│  └──────────────┘ │ └──────────────┘ │ │     Service      │    │
│                   │                  │ └──────────────────┘    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Data Access Layer (SQLAlchemy)             │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                     │
┌────────────────────┼────────────────────────────────────────────┐
│              Database (SQLite/PostgreSQL)                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │  Users   │ │  Tasks   │ │Settings  │ │ AIRecommendations│   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Scope and Dependencies

### 2.1 In Scope

| Component | Description | Priority |
|-----------|-------------|----------|
| User Authentication | JWT-based login/logout/register | High |
| Task CRUD | Create, Read, Update, Delete tasks | High |
| Dashboard | Personalized task overview + AI panel | High |
| AI Recommendations | Task suggestions via CLI integration | Medium |
| User Settings | Preferences and AI configuration | Medium |
| REST API | All backend endpoints | High |
| React UI | Responsive frontend | High |
| Docker Support | Containerization for deployment | Low |

### 2.2 Out of Scope

- Mobile native applications (iOS/Android)
- Real-time collaboration features
- Third-party integrations (Calendar, Slack, etc.)
- Advanced AI training/fine-tuning
- Multi-tenant support
- Kubernetes orchestration (optional future phase)

### 2.3 External Dependencies

| Dependency | Purpose | Owner | Status |
|------------|---------|-------|--------|
| Python 3.13.5 | Backend runtime | Python Software Foundation | Required |
| Node.js v24.x | Frontend runtime | OpenJS Foundation | Required |
| FastAPI | Web framework | Sebastián Ramírez (MIT) | Required |
| React 18+ | UI framework | Meta (MIT) | Required |
| SQLAlchemy | ORM | SQLAlchemy Team | Required |
| PyJWT | JWT handling | Jose Padilla (MIT) | Required |
| Docker | Containerization | Docker Inc. | Optional |
| Claude/Qwen CLI | AI integration | Anthropic/Alibaba | Required |

---

## 3. Technology Stack Decisions

### 3.1 Backend Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Framework | **FastAPI** | Async support, auto docs, Python 3.13 compatible, high performance |
| ORM | **SQLAlchemy 2.0** | Type-safe, mature, supports async |
| Database | **SQLite (dev) / PostgreSQL (prod)** | Simple setup, easy migration |
| Auth | **PyJWT + bcrypt** | Industry standard, secure password hashing |
| Validation | **Pydantic** | Built into FastAPI, type validation |
| Logging | **structlog** | Structured logging, JSON output |

### 3.2 Frontend Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Framework | **React 18+** | Spec requirement, large ecosystem |
| State | **Zustand** | Lightweight, simpler than Redux |
| HTTP Client | **Axios** | Interceptors, cancel requests |
| UI Components | **Custom + Tailwind CSS** | Flexibility, no bloat |
| Routing | **React Router v6** | Standard, well-maintained |
| Forms | **React Hook Form** | Performance, minimal re-renders |

### 3.3 AI Integration Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Frontend  │────▶│  Backend API │────▶│  AI Service     │
│   (React)   │◀────│  (FastAPI)   │◀────│  (CLI Wrapper)  │
└─────────────┘     └──────────────┘     └─────────────────┘
                           │                      │
                           │                      ▼
                           │            ┌─────────────────┐
                           │            │ Claude/Qwen CLI │
                           │            └─────────────────┘
                           ▼
                  ┌─────────────────┐
                  │   Database      │
                  └─────────────────┘
```

**Decision**: Backend-mediated AI integration (not direct frontend calls)
- **Rationale**: Security (API keys server-side), rate limiting, caching, logging

---

## 4. API Contracts

### 4.1 Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login, returns JWT | No |
| POST | `/api/v1/auth/logout` | Invalidate token | Yes |
| GET | `/api/v1/auth/me` | Get current user | Yes |
| PUT | `/api/v1/auth/password` | Change password | Yes |

**Request/Response Examples**:

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

### 4.2 Task Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/tasks` | List user's tasks | Yes |
| POST | `/api/v1/tasks` | Create new task | Yes |
| GET | `/api/v1/tasks/{id}` | Get task by ID | Yes |
| PUT | `/api/v1/tasks/{id}` | Update task | Yes |
| DELETE | `/api/v1/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/v1/tasks/{id}/complete` | Mark complete | Yes |

**Task Entity Schema**:

```json
{
  "id": "uuid-string",
  "user_id": "uuid-string",
  "title": "string (max 200 chars)",
  "description": "string (optional)",
  "status": "pending|in_progress|completed",
  "priority": "low|medium|high",
  "due_date": "ISO8601 datetime (optional)",
  "created_at": "ISO8601 datetime",
  "updated_at": "ISO8601 datetime"
}
```

### 4.3 AI Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/ai/recommend` | Get task recommendations | Yes |
| POST | `/api/v1/ai/optimize` | Optimize existing task | Yes |
| GET | `/api/v1/ai/history` | Get AI interaction history | Yes |

### 4.4 Settings Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/settings` | Get user settings | Yes |
| PUT | `/api/v1/settings` | Update user settings | Yes |

### 4.5 Error Taxonomy

| Status Code | Error Type | Response Format |
|-------------|------------|-----------------|
| 400 | Bad Request | `{"error": "invalid_input", "details": [...]}` |
| 401 | Unauthorized | `{"error": "unauthorized", "message": "..."}` |
| 403 | Forbidden | `{"error": "forbidden", "message": "..."}` |
| 404 | Not Found | `{"error": "not_found", "resource": "..."}` |
| 409 | Conflict | `{"error": "conflict", "message": "..."}` |
| 429 | Rate Limited | `{"error": "rate_limited", "retry_after": 60}` |
| 500 | Internal Error | `{"error": "internal_error", "trace_id": "..."}` |
| 503 | Service Unavailable | `{"error": "service_unavailable", "retry_after": 300}` |

---

## 5. Data Management

### 5.1 Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Settings table
CREATE TABLE settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    theme VARCHAR(20) DEFAULT 'light',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    ai_assistant_enabled BOOLEAN DEFAULT TRUE,
    ai_provider VARCHAR(50) DEFAULT 'claude',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI Recommendations table
CREATE TABLE ai_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    recommendation_text TEXT NOT NULL,
    confidence_score DECIMAL(3,2),
    context JSONB,
    is_accepted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_ai_recommendations_user ON ai_recommendations(user_id);
```

### 5.2 Migration Strategy

- **Tool**: Alembic (SQLAlchemy's migration tool)
- **Location**: `backend/migrations/`
- **Strategy**: 
  - Auto-generate migrations from models
  - Review and commit migration files
  - Rollback support for every migration

### 5.3 Data Retention

| Data Type | Retention Policy |
|-----------|------------------|
| User accounts | Until user deletion |
| Tasks | Until user deletion (soft delete option future) |
| AI history | 90 days rolling |
| Logs | 30 days |
| Sessions | 7 days inactive |

---

## 6. Non-Functional Requirements

### 6.1 Performance Budgets

| Metric | Target | Measurement |
|--------|--------|-------------|
| API p95 latency | < 200ms | Backend monitoring |
| Frontend FCP | < 1.5s | Lighthouse |
| Frontend LCP | < 2.5s | Lighthouse |
| Dashboard load | < 3s | E2E tests |
| Task CRUD | < 2s (p95) | API monitoring |
| AI response | < 5s (p95) | API monitoring |
| Concurrent users | 100+ | Load testing |

### 6.2 Reliability

| Metric | Target | Strategy |
|--------|--------|----------|
| Uptime | 99% (business hours) | Health checks, monitoring |
| Error rate | < 1% | Error tracking, alerts |
| Recovery time | < 15 minutes | Runbooks, automated recovery |

### 6.3 Security

| Area | Implementation |
|------|----------------|
| Authentication | JWT with 1-hour expiry, refresh tokens |
| Password storage | bcrypt with cost factor 12 |
| API security | Rate limiting, CORS, input validation |
| Data in transit | HTTPS/TLS required |
| Secrets management | Environment variables, `.env` files |
| SQL injection | Parameterized queries (SQLAlchemy) |
| XSS | React auto-escaping, CSP headers |

### 6.4 Observability

| Component | Tool | Purpose |
|-----------|------|---------|
| Logging | structlog (JSON) | Structured logs |
| Metrics | Prometheus (future) | Performance tracking |
| Tracing | OpenTelemetry (future) | Request tracing |
| Error tracking | Console + logs (MVP) | Error capture |

**Log Format**:
```json
{
  "timestamp": "2026-02-16T10:30:00Z",
  "level": "INFO",
  "service": "hackathon-backend",
  "trace_id": "abc123",
  "user_id": "uuid",
  "event": "task_created",
  "task_id": "uuid"
}
```

---

## 7. Implementation Phases

### Phase 1: Environment Setup (1 day)

**Goal**: Development environment ready

| Task | Subtasks | Priority |
|------|----------|----------|
| 1.1 Install runtimes | Python 3.13.5, Node v24.x | High |
| 1.2 Setup virtualenv | `python -m venv venv` | High |
| 1.3 Initialize backend | `pip install fastapi uvicorn sqlalchemy` | High |
| 1.4 Initialize frontend | `npx create-react-app` or Vite | High |
| 1.5 Configure CLI tools | Claude/Qwen CLI setup | High |
| 1.6 Create folder structure | As per constitution | High |

**Deliverables**:
- [ ] Working Python environment
- [ ] Working Node environment
- [ ] Basic folder structure

### Phase 2: Backend Implementation (2-3 days)

**Goal**: Functional REST API with auth and task management

| Module | Files | Priority | Dependencies |
|--------|-------|----------|--------------|
| Database | `models/`, `database.py` | High | Phase 1 |
| Auth | `routes/auth.py`, `services/auth.py` | High | Database |
| Tasks | `routes/tasks.py`, `services/tasks.py` | High | Auth |
| Settings | `routes/settings.py` | Medium | Auth |
| AI Service | `services/ai_service.py` | Medium | Phase 1 |
| Utils | `logging_config.py`, `middleware.py` | High | None |

**Deliverables**:
- [ ] All API endpoints functional
- [ ] Authentication working
- [ ] Database migrations
- [ ] API documentation (`/docs`)

### Phase 3: Frontend Implementation (3-4 days)

**Goal**: Complete React UI connected to backend

| Module | Components | Priority | Dependencies |
|--------|------------|----------|--------------|
| Auth Pages | Login, Register | High | Backend Auth |
| Dashboard | Dashboard, TaskList, AIPanel | High | Backend Tasks |
| Tasks | TaskForm, TaskDetail, TaskCard | High | Backend Tasks |
| Settings | SettingsForm, Preferences | Medium | Backend Settings |
| Shared | Button, Input, Modal, Loading | High | None |
| Layout | Header, Sidebar, Footer | High | None |

**Deliverables**:
- [ ] All pages implemented
- [ ] API integration complete
- [ ] Responsive design
- [ ] Error handling

### Phase 4: AI Integration (2-3 days)

**Goal**: AI-powered task recommendations

| Module | Implementation | Priority |
|--------|----------------|----------|
| CLI Wrapper | `services/ai_cli_wrapper.py` | High |
| Recommendation Engine | `services/task_recommendation.py` | High |
| API Endpoints | `/api/v1/ai/*` | High |
| Frontend Integration | AIPanel component | Medium |

**Deliverables**:
- [ ] AI recommendations working
- [ ] CLI integration functional
- [ ] Frontend displays AI suggestions

### Phase 5: Testing & QA (1-2 days)

**Goal**: Verified, bug-free application

| Test Type | Scope | Tools |
|-----------|-------|-------|
| Unit Tests | Backend services, utils | pytest |
| API Tests | All endpoints | pytest + httpx |
| Component Tests | React components | React Testing Library |
| E2E Tests | Critical user flows | Playwright (optional) |
| Manual QA | All acceptance scenarios | Checklist |

**Deliverables**:
- [ ] 80%+ code coverage
- [ ] All acceptance scenarios pass
- [ ] Performance benchmarks met

### Phase 6: Deployment (1 day)

**Goal**: Containerized, deployable application

| Task | Files | Priority |
|------|-------|----------|
| Docker Backend | `backend/Dockerfile` | High |
| Docker Frontend | `frontend/Dockerfile` | High |
| Docker Compose | `docker-compose.yml` | High |
| Environment Config | `.env.example` | High |
| Documentation | `README.md`, `DEPLOYMENT.md` | High |

**Deliverables**:
- [ ] Docker containers build successfully
- [ ] `docker-compose up` runs full stack
- [ ] Deployment documentation

---

## 8. Risk Analysis

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| AI service unavailable | High | Medium | Graceful degradation, cached responses |
| Database corruption | High | Low | Regular backups, transactions |
| Security vulnerability | High | Medium | Input validation, dependency updates |
| Performance degradation | Medium | Medium | Load testing, monitoring |
| Scope creep | Medium | High | Strict adherence to spec |
| Timeline overrun | Medium | Medium | Prioritize MVP features |

### Kill Switches

- AI integration: Feature flag to disable AI features
- Rate limiting: Emergency increase limits
- Database: Read-only mode for maintenance

---

## 9. Definition of Done

A feature/task is considered complete when:

- [ ] Code implemented per spec
- [ ] Unit tests passing (80%+ coverage)
- [ ] Integration tests passing
- [ ] API documented
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Security reviewed
- [ ] Performance within budget
- [ ] Documentation updated

---

## 10. File Structure

```
hackathon0/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── setting.py
│   │   │   └── ai_recommendation.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   │   ├── settings.py
│   │   │   └── ai.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── task_service.py
│   │   │   ├── ai_service.py
│   │   │   └── ai_cli_wrapper.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── task.py
│   │   │   ├── setting.py
│   │   │   └── ai.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── logging_config.py
│   │       └── security.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_tasks.py
│   │   └── test_ai.py
│   ├── migrations/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── pytest.ini
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── shared/
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Input.jsx
│   │   │   │   ├── Modal.jsx
│   │   │   │   └── Loading.jsx
│   │   │   ├── auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   └── Register.jsx
│   │   │   ├── dashboard/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── TaskList.jsx
│   │   │   │   └── AIPanel.jsx
│   │   │   ├── tasks/
│   │   │   │   ├── TaskForm.jsx
│   │   │   │   ├── TaskCard.jsx
│   │   │   │   └── TaskDetail.jsx
│   │   │   └── settings/
│   │   │       └── Settings.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   └── useTasks.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   └── tasks.js
│   │   ├── store/
│   │   │   ├── index.js
│   │   │   ├── authStore.js
│   │   │   └── taskStore.js
│   │   └── utils/
│   │       └── helpers.js
│   ├── package.json
│   ├── vite.config.js (or craco.config.js)
│   ├── Dockerfile
│   └── tailwind.config.js
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── DEPLOYMENT.md
├── specs/
│   └── 1-hackathon-app/
│       ├── spec.md
│       ├── plan.md (this file)
│       ├── tasks.md
│       └── checklists/
├── history/
│   ├── prompts/
│   └── adr/
└── docs/
    └── api.md
```

---

## 11. Next Steps

1. **Create PHR** for this planning session
2. **Generate `sp.tasks`** with detailed, testable tasks
3. **Begin Phase 1** (Environment Setup)

---

**Version**: 1.0.0  
**Approved**: Pending  
**Last Updated**: 2026-02-16
