# Task List: Hackathon_0 Full-Stack Application

**Feature**: `1-hackathon-app`  
**Version**: 1.0.0  
**Created**: 2026-02-16  
**Status**: Draft  
**References**: [Constitution](../../.specify/memory/constitution.md), [Spec](spec.md), [Plan](plan.md)

---

## Task Summary

| Phase | Total Tasks | High Priority | Medium Priority | Estimated Effort |
|-------|-------------|---------------|-----------------|------------------|
| Phase 1: Environment Setup | 5 | 5 | 0 | 8 hours |
| Phase 2: Backend Implementation | 24 | 20 | 4 | 24 hours |
| Phase 3: Frontend Implementation | 28 | 22 | 6 | 32 hours |
| Phase 4: AI Integration | 12 | 8 | 4 | 16 hours |
| Phase 5: Testing & QA | 15 | 10 | 5 | 16 hours |
| Phase 6: Deployment | 8 | 6 | 2 | 8 hours |
| **Total** | **92** | **71** | **21** | **104 hours (~13 days)** |

---

## Phase 1: Environment Setup (8 hours)

### Task 1.1: Install Python 3.13.5
- **Description**: Install and configure Python 3.13.5 runtime
- **Subtasks**:
  1. Download Python 3.13.5 from python.org
  2. Run installer with "Add to PATH" option
  3. Verify installation: `python --version`
  4. Verify pip: `pip --version`
- **Dependencies**: None
- **Priority**: High
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] `python --version` returns 3.13.5
  - [ ] `pip --version` works

### Task 1.2: Install Node.js v24.x
- **Description**: Install and configure Node.js v24.x runtime
- **Subtasks**:
  1. Download Node.js v24.x from nodejs.org
  2. Run installer
  3. Verify installation: `node --version`
  4. Verify npm: `npm --version`
- **Dependencies**: None
- **Priority**: High
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] `node --version` returns v24.x
  - [ ] `npm --version` works

### Task 1.3: Setup Python Virtual Environment
- **Description**: Create isolated Python environment for backend
- **Subtasks**:
  1. Navigate to project root
  2. Create venv: `python -m venv venv`
  3. Activate venv: `.\venv\Scripts\Activate` (Windows)
  4. Upgrade pip: `pip install --upgrade pip`
- **Dependencies**: Task 1.1
- **Priority**: High
- **Estimated Effort**: 15 minutes
- **Acceptance Criteria**:
  - [ ] `venv` directory exists
  - [ ] Virtual environment activates successfully

### Task 1.4: Initialize Folder Structure
- **Description**: Create project directory structure per constitution
- **Subtasks**:
  1. Create `backend/` directory with subdirs: `app/`, `tests/`, `migrations/`
  2. Create `frontend/` directory
  3. Create `docs/` directory
  4. Create `specs/` directory (already exists)
  5. Create `history/` directory (already exists)
  6. Create `.env.example` file
  7. Create `.gitignore` file
- **Dependencies**: None
- **Priority**: High
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] All directories created per plan.md structure
  - [ ] `.gitignore` includes venv, node_modules, .env, __pycache__

### Task 1.5: Configure CLI Tools
- **Description**: Setup Claude/Qwen CLI for AI integration
- **Subtasks**:
  1. Install Claude CLI or verify Qwen Code is running
  2. Configure API keys if required
  3. Test CLI: run a simple query
  4. Document CLI setup in README
- **Dependencies**: Task 1.1, Task 1.2
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] CLI tool responds to commands
  - [ ] API keys configured (if required)

### Task 1.6: Install Backend Dependencies
- **Description**: Install Python packages for backend
- **Subtasks**:
  1. Create `backend/requirements.txt` with:
     - fastapi
     - uvicorn[standard]
     - sqlalchemy
     - alembic
     - pyjwt
     - bcrypt
     - pydantic
     - python-dotenv
     - structlog
     - pytest
     - httpx (for testing)
  2. Install: `pip install -r backend/requirements.txt`
  3. Verify installations
- **Dependencies**: Task 1.3
- **Priority**: High
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] All packages installed
  - [ ] `fastapi --version` works

### Task 1.7: Initialize Frontend Project
- **Description**: Create React application with Vite
- **Subtasks**:
  1. Run: `npm create vite@latest frontend -- --template react`
  2. Navigate to frontend: `cd frontend`
  3. Install dependencies: `npm install`
  4. Install additional packages:
     - `npm install axios zustand react-router-dom`
     - `npm install -D tailwindcss postcss autoprefixer`
  5. Initialize Tailwind: `npx tailwindcss init -p`
  6. Test: `npm run dev`
- **Dependencies**: Task 1.2
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Frontend dev server runs
  - [ ] Default Vite page loads in browser

---

## Phase 2: Backend Implementation (24 hours)

### Task 2.1: Setup SQLAlchemy Database Connection
- **Description**: Configure database connection and session management
- **Subtasks**:
  1. Create `backend/app/database.py`
  2. Define DATABASE_URL (SQLite for dev)
  3. Create SQLAlchemy engine
  4. Create SessionLocal class
  5. Create Base class for models
  6. Create `get_db` dependency for FastAPI
- **Dependencies**: Task 1.6
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Database connection works
  - [ ] Session can be created and closed

### Task 2.2: Create User Model
- **Description**: Define User database model
- **Subtasks**:
  1. Create `backend/app/models/user.py`
  2. Define User class with fields:
     - id (UUID, primary key)
     - email (String, unique, not null)
     - password_hash (String, not null)
     - name (String, not null)
     - is_active (Boolean, default True)
     - created_at (DateTime)
     - updated_at (DateTime)
  3. Add `__tablename__ = "users"`
  4. Add relationship to tasks, settings, recommendations
- **Dependencies**: Task 2.1
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] User model defined correctly
  - [ ] Model can be imported without errors

### Task 2.3: Create Task Model
- **Description**: Define Task database model
- **Subtasks**:
  1. Create `backend/app/models/task.py`
  2. Define Task class with fields:
     - id (UUID, primary key)
     - user_id (UUID, foreign key)
     - title (String(200), not null)
     - description (Text, nullable)
     - status (String(20), default 'pending')
     - priority (String(20), default 'medium')
     - due_date (DateTime, nullable)
     - completed_at (DateTime, nullable)
     - created_at (DateTime)
     - updated_at (DateTime)
  3. Add relationship to User
- **Dependencies**: Task 2.1, Task 2.2
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] Task model defined correctly
  - [ ] Foreign key relationship works

### Task 2.4: Create Setting Model
- **Description**: Define Setting database model for user preferences
- **Subtasks**:
  1. Create `backend/app/models/setting.py`
  2. Define Setting class with fields:
     - id (UUID, primary key)
     - user_id (UUID, foreign key, unique)
     - theme (String(20), default 'light')
     - notifications_enabled (Boolean, default True)
     - ai_assistant_enabled (Boolean, default True)
     - ai_provider (String(50), default 'claude')
     - created_at (DateTime)
     - updated_at (DateTime)
  3. Add relationship to User
- **Dependencies**: Task 2.1, Task 2.2
- **Priority**: Medium
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] Setting model defined correctly
  - [ ] One-to-one relationship with User works

### Task 2.5: Create AI Recommendation Model
- **Description**: Define AIRecommendation database model
- **Subtasks**:
  1. Create `backend/app/models/ai_recommendation.py`
  2. Define AIRecommendation class with fields:
     - id (UUID, primary key)
     - user_id (UUID, foreign key)
     - task_id (UUID, foreign key, nullable)
     - recommendation_text (Text, not null)
     - confidence_score (Decimal)
     - context (JSON)
     - is_accepted (Boolean, default False)
     - created_at (DateTime)
  3. Add relationships to User and Task
- **Dependencies**: Task 2.1, Task 2.2, Task 2.3
- **Priority**: Medium
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] AIRecommendation model defined correctly
  - [ ] Relationships work

### Task 2.6: Setup Alembic Migrations
- **Description**: Configure database migration system
- **Subtasks**:
  1. Initialize Alembic: `alembic init migrations`
  2. Configure `alembic.ini` with DATABASE_URL
  3. Update `migrations/env.py` to import models
  4. Create initial migration: `alembic revision --autogenerate -m "Initial migration"`
  5. Run migration: `alembic upgrade head`
  6. Verify tables created in database
- **Dependencies**: Task 2.2, Task 2.3, Task 2.4, Task 2.5
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Migration runs successfully
  - [ ] All 4 tables created in database

### Task 2.7: Setup Pydantic Schemas - Auth
- **Description**: Create Pydantic schemas for authentication
- **Subtasks**:
  1. Create `backend/app/schemas/auth.py`
  2. Define UserCreate schema (email, password, name)
  3. Define UserLogin schema (email, password)
  4. Define UserResponse schema (id, email, name)
  5. Define Token schema (access_token, token_type, expires_in)
  6. Define PasswordChange schema
- **Dependencies**: Task 1.6
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] All schemas defined
  - [ ] Validation works for test data

### Task 2.8: Setup Pydantic Schemas - Task
- **Description**: Create Pydantic schemas for tasks
- **Subtasks**:
  1. Create `backend/app/schemas/task.py`
  2. Define TaskCreate schema
  3. Define TaskUpdate schema (all fields optional)
  4. Define TaskResponse schema (includes all fields)
  5. Define TaskStatus enum (pending, in_progress, completed)
  6. Define TaskPriority enum (low, medium, high)
- **Dependencies**: Task 1.6
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] All schemas defined
  - [ ] Enums work correctly

### Task 2.9: Setup Pydantic Schemas - Settings & AI
- **Description**: Create Pydantic schemas for settings and AI
- **Subtasks**:
  1. Create `backend/app/schemas/setting.py`
  2. Define SettingCreate schema
  3. Define SettingUpdate schema
  4. Define SettingResponse schema
  5. Create `backend/app/schemas/ai.py`
  6. Define AIRecommendRequest schema
  7. Define AIRecommendResponse schema
- **Dependencies**: Task 1.6
- **Priority**: Medium
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] All schemas defined

### Task 2.10: Implement Password Hashing Utility
- **Description**: Create secure password hashing functions
- **Subtasks**:
  1. Create `backend/app/utils/security.py`
  2. Implement `hash_password(password: str) -> str` using bcrypt
  3. Implement `verify_password(password: str, hashed: str) -> bool`
  4. Test with sample passwords
- **Dependencies**: Task 1.6
- **Priority**: High
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] Passwords hash correctly
  - [ ] Verification works

### Task 2.11: Implement JWT Token Service
- **Description**: Create JWT token generation and verification
- **Subtasks**:
  1. Create `backend/app/services/auth_service.py`
  2. Define SECRET_KEY and ALGORITHM (from env)
  3. Implement `create_access_token(data: dict, expires_delta: int) -> str`
  4. Implement `verify_token(token: str) -> dict`
  5. Implement `get_current_user` dependency for FastAPI
  6. Set token expiry to 1 hour
- **Dependencies**: Task 2.10
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Tokens generate correctly
  - [ ] Tokens verify correctly
  - [ ] Expired tokens rejected

### Task 2.12: Create FastAPI App Structure
- **Description**: Setup main FastAPI application
- **Subtasks**:
  1. Create `backend/app/main.py`
  2. Create FastAPI app instance
  3. Add CORS middleware
  4. Add health check endpoint: `GET /health`
  5. Include routers (placeholder)
  6. Configure uvicorn to run on port 8000
- **Dependencies**: Task 1.6
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] App starts with `uvicorn app.main:app --reload`
  - [ ] `/health` returns 200
  - [ ] `/docs` shows Swagger UI

### Task 2.13: Implement Register Endpoint
- **Description**: Create user registration API
- **Subtasks**:
  1. Create `backend/app/routes/auth.py`
  2. Implement `POST /api/v1/auth/register`
  3. Validate input with UserCreate schema
  4. Check if email already exists
  5. Hash password
  6. Create user in database
  7. Return UserResponse (no password)
- **Dependencies**: Task 2.2, Task 2.7, Task 2.10, Task 2.1
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Registration creates user
  - [ ] Duplicate email returns 409
  - [ ] Password not in response

### Task 2.14: Implement Login Endpoint
- **Description**: Create user login API
- **Subtasks**:
  1. Add to `backend/app/routes/auth.py`
  2. Implement `POST /api/v1/auth/login`
  3. Validate credentials
  4. Verify password
  5. Generate JWT token
  6. Return token and user info
- **Dependencies**: Task 2.11, Task 2.13
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Valid credentials return token
  - [ ] Invalid credentials return 401

### Task 2.15: Implement Get Current User Endpoint
- **Description**: Create endpoint to get authenticated user
- **Subtasks**:
  1. Add to `backend/app/routes/auth.py`
  2. Implement `GET /api/v1/auth/me`
  3. Add Depends(get_current_user)
  4. Return current user info
- **Dependencies**: Task 2.11, Task 2.14
- **Priority**: High
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] Valid token returns user
  - [ ] Invalid token returns 401

### Task 2.16: Implement Logout Endpoint
- **Description**: Create logout endpoint (token invalidation)
- **Subtasks**:
  1. Add to `backend/app/routes/auth.py`
  2. Implement `POST /api/v1/auth/logout`
  3. For MVP: return success (client discards token)
  4. Future: add token blacklist
- **Dependencies**: Task 2.14
- **Priority**: Medium
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] Logout returns success

### Task 2.17: Implement Change Password Endpoint
- **Description**: Create password change API
- **Subtasks**:
  1. Add to `backend/app/routes/auth.py`
  2. Implement `PUT /api/v1/auth/password`
  3. Verify current password
  4. Hash new password
  5. Update in database
- **Dependencies**: Task 2.14, Task 2.10
- **Priority**: Medium
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] Correct current password allows change
  - [ ] Wrong current password returns 400

### Task 2.18: Create Task Service
- **Description**: Implement business logic for tasks
- **Subtasks**:
  1. Create `backend/app/services/task_service.py`
  2. Implement `create_task(db, user_id, task_data)`
  3. Implement `get_tasks(db, user_id, skip, limit)`
  4. Implement `get_task(db, task_id, user_id)`
  5. Implement `update_task(db, task_id, user_id, task_data)`
  6. Implement `delete_task(db, task_id, user_id)`
  7. Implement `mark_task_complete(db, task_id, user_id)`
- **Dependencies**: Task 2.3, Task 2.8
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] All CRUD operations work
  - [ ] User can only access own tasks

### Task 2.19: Implement Task Endpoints
- **Description**: Create REST API for tasks
- **Subtasks**:
  1. Create `backend/app/routes/tasks.py`
  2. Implement `GET /api/v1/tasks` (list)
  3. Implement `POST /api/v1/tasks` (create)
  4. Implement `GET /api/v1/tasks/{id}` (get one)
  5. Implement `PUT /api/v1/tasks/{id}` (update)
  6. Implement `DELETE /api/v1/tasks/{id}` (delete)
  7. Implement `PATCH /api/v1/tasks/{id}/complete` (complete)
  8. Add authentication to all endpoints
- **Dependencies**: Task 2.18, Task 2.11
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] All endpoints work
  - [ ] Authentication required
  - [ ] User isolation enforced

### Task 2.20: Implement Settings Endpoints
- **Description**: Create API for user settings
- **Subtasks**:
  1. Create `backend/app/routes/settings.py`
  2. Implement `GET /api/v1/settings`
  3. Implement `PUT /api/v1/settings`
  4. Create default settings if not exist
  5. Add authentication
- **Dependencies**: Task 2.4, Task 2.9, Task 2.11
- **Priority**: Medium
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Settings can be retrieved
  - [ ] Settings can be updated

### Task 2.21: Setup Logging Configuration
- **Description**: Configure structured logging
- **Subtasks**:
  1. Create `backend/app/utils/logging_config.py`
  2. Configure structlog
  3. Set JSON output format
  4. Add request logging middleware
  5. Configure log levels
- **Dependencies**: Task 1.6
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] Logs output in JSON format
  - [ ] Request/response logged

### Task 2.22: Implement Error Handling Middleware
- **Description**: Add global error handling
- **Subtasks**:
  1. Create `backend/app/utils/error_handler.py`
  2. Define custom exception classes
  3. Create exception handlers
  4. Register with FastAPI app
  5. Ensure proper status codes
- **Dependencies**: Task 2.12
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] Errors return proper JSON format
  - [ ] Stack traces not exposed

### Task 2.23: Create AI CLI Wrapper
- **Description**: Implement wrapper for Claude/Qwen CLI
- **Subtasks**:
  1. Create `backend/app/services/ai_cli_wrapper.py`
  2. Implement `call_claude_cli(prompt: str) -> str`
  3. Implement `call_qwen_cli(prompt: str) -> str`
  4. Add error handling
  5. Add timeout (30 seconds)
  6. Parse CLI output
- **Dependencies**: Task 1.5
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] CLI can be called programmatically
  - [ ] Responses parsed correctly
  - [ ] Timeouts handled

### Task 2.24: Create AI Recommendation Service
- **Description**: Implement task recommendation logic
- **Subtasks**:
  1. Create `backend/app/services/ai_service.py`
  2. Implement `get_task_recommendations(user_id, context)`
  3. Implement `optimize_task(task_data)`
  4. Create prompts for AI
  5. Store recommendations in database
  6. Add caching layer
- **Dependencies**: Task 2.23, Task 2.5
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Recommendations generated
  - [ ] Results stored in database

### Task 2.25: Implement AI Endpoints
- **Description**: Create REST API for AI features
- **Subtasks**:
  1. Create `backend/app/routes/ai.py`
  2. Implement `POST /api/v1/ai/recommend`
  3. Implement `POST /api/v1/ai/optimize`
  4. Implement `GET /api/v1/ai/history`
  5. Add authentication
  6. Add rate limiting
- **Dependencies**: Task 2.24, Task 2.11
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] All AI endpoints work
  - [ ] Rate limiting prevents abuse

---

## Phase 3: Frontend Implementation (32 hours)

### Task 3.1: Configure Tailwind CSS
- **Description**: Setup Tailwind CSS for styling
- **Subtasks**:
  1. Update `tailwind.config.js` with content paths
  2. Add Tailwind directives to `src/index.css`
  3. Configure PostCSS
  4. Test with sample component
- **Dependencies**: Task 1.7
- **Priority**: High
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] Tailwind classes work in components
  - [ ] Styles apply correctly

### Task 3.2: Create Button Component
- **Description**: Reusable button component
- **Subtasks**:
  1. Create `src/components/shared/Button.jsx`
  2. Add variants: primary, secondary, danger
  3. Add sizes: sm, md, lg
  4. Add disabled state
  5. Add loading state
  6. Add PropTypes or TypeScript
- **Dependencies**: Task 3.1
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] Button renders correctly
  - [ ] All variants work

### Task 3.3: Create Input Component
- **Description**: Reusable input component
- **Subtasks**:
  1. Create `src/components/shared/Input.jsx`
  2. Add text, email, password types
  3. Add label support
  4. Add error message display
  5. Add disabled state
- **Dependencies**: Task 3.1
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] Input works with all types
  - [ ] Error messages display

### Task 3.4: Create Modal Component
- **Description**: Reusable modal/dialog component
- **Subtasks**:
  1. Create `src/components/shared/Modal.jsx`
  2. Add open/close functionality
  3. Add overlay
  4. Add header, body, footer slots
  5. Add close on overlay click
- **Dependencies**: Task 3.2
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Modal opens and closes
  - [ ] Overlay click closes modal

### Task 3.5: Create Loading Component
- **Description**: Loading spinner/indicator
- **Subtasks**:
  1. Create `src/components/shared/Loading.jsx`
  2. Add spinner animation
  3. Add full-screen overlay option
  4. Add inline option
  5. Add customizable text
- **Dependencies**: Task 3.1
- **Priority**: High
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] Spinner animates
  - [ ] Both modes work

### Task 3.6: Create Header Component
- **Description**: Application header with navigation
- **Subtasks**:
  1. Create `src/components/layout/Header.jsx`
  2. Add app logo/title
  3. Add navigation links
  4. Add user menu (when logged in)
  5. Add logout button
  6. Make responsive
- **Dependencies**: Task 3.2
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Header displays correctly
  - [ ] Navigation works
  - [ ] Responsive on mobile

### Task 3.7: Create Sidebar Component
- **Description**: Application sidebar navigation
- **Subtasks**:
  1. Create `src/components/layout/Sidebar.jsx`
  2. Add navigation items
  3. Add active state highlighting
  4. Add collapsible for mobile
  5. Add icons
- **Dependencies**: Task 3.2
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Sidebar displays
  - [ ] Collapses on mobile

### Task 3.8: Setup React Router
- **Description**: Configure routing for application
- **Subtasks**:
  1. Install react-router-dom (already done in 1.7)
  2. Create `src/App.jsx` with routes
  3. Define routes: /, /login, /register, /dashboard, /tasks, /settings
  4. Add ProtectedRoute component
  5. Add redirect logic
- **Dependencies**: Task 1.7
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] All routes defined
  - [ ] Protected routes redirect to login

### Task 3.9: Setup Zustand Store
- **Description**: Configure state management
- **Subtasks**:
  1. Create `src/store/index.js`
  2. Create `src/store/authStore.js`
  3. Define auth state and actions
  4. Create `src/store/taskStore.js`
  5. Define task state and actions
  6. Add persistence (localStorage)
- **Dependencies**: Task 1.7
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Stores created
  - [ ] State persists across reloads

### Task 3.10: Create API Service
- **Description**: Setup Axios for API calls
- **Subtasks**:
  1. Create `src/services/api.js`
  2. Create axios instance with base URL
  3. Add request interceptor (add token)
  4. Add response interceptor (handle errors)
  5. Create `src/services/auth.js`
  6. Create `src/services/tasks.js`
- **Dependencies**: Task 3.9
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] API calls include token
  - [ ] Errors handled globally

### Task 3.11: Create Login Page
- **Description**: User login page
- **Subtasks**:
  1. Create `src/components/auth/Login.jsx`
  2. Add email and password inputs
  3. Add form validation
  4. Call login API
  5. Handle success (redirect to dashboard)
  6. Handle errors (display message)
  7. Add link to register
- **Dependencies**: Task 3.3, Task 3.8, Task 3.10
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Login form works
  - [ ] Errors display correctly
  - [ ] Redirects on success

### Task 3.12: Create Register Page
- **Description**: User registration page
- **Subtasks**:
  1. Create `src/components/auth/Register.jsx`
  2. Add name, email, password inputs
  3. Add password confirmation
  4. Add form validation
  5. Call register API
  6. Handle success (redirect to login)
  7. Handle errors
- **Dependencies**: Task 3.3, Task 3.8, Task 3.10
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Registration works
  - [ ] Validation works

### Task 3.13: Create Dashboard Page
- **Description**: Main dashboard with task overview
- **Subtasks**:
  1. Create `src/components/dashboard/Dashboard.jsx`
  2. Add task summary stats
  3. Add recent tasks list
  4. Add AI panel integration
  5. Add quick add task button
  6. Fetch data from API
- **Dependencies**: Task 3.6, Task 3.8, Task 3.10
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Dashboard loads
  - [ ] Data displays correctly

### Task 3.14: Create TaskList Component
- **Description**: Component to display list of tasks
- **Subtasks**:
  1. Create `src/components/dashboard/TaskList.jsx`
  2. Add filtering (by status, priority)
  3. Add sorting
  4. Add pagination (if needed)
  5. Integrate TaskCard
  6. Add empty state
- **Dependencies**: Task 3.15
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Tasks display in list
  - [ ] Filtering works

### Task 3.15: Create TaskCard Component
- **Description**: Individual task card
- **Subtasks**:
  1. Create `src/components/tasks/TaskCard.jsx`
  2. Display title, description, status, priority
  3. Add due date display
  4. Add quick actions (edit, delete, complete)
  5. Add priority color coding
  6. Add status badge
- **Dependencies**: Task 3.2
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Card displays all info
  - [ ] Actions work

### Task 3.16: Create AIPanel Component
- **Description**: AI assistant panel for recommendations
- **Subtasks**:
  1. Create `src/components/dashboard/AIPanel.jsx`
  2. Add chat-like interface
  3. Add input for user queries
  4. Display AI recommendations
  5. Add accept/reject actions
  6. Add loading states
  7. Connect to AI API
- **Dependencies**: Task 3.3, Task 3.5, Task 3.10
- **Priority**: High
- **Estimated Effort**: 2.5 hours
- **Acceptance Criteria**:
  - [ ] Panel displays
  - [ ] Can send queries
  - [ ] Recommendations display

### Task 3.17: Create TaskForm Component
- **Description**: Form for creating/editing tasks
- **Subtasks**:
  1. Create `src/components/tasks/TaskForm.jsx`
  2. Add title input
  3. Add description textarea
  4. Add priority select
  5. Add due date picker
  6. Add status select
  7. Add validation
  8. Handle create and update modes
- **Dependencies**: Task 3.3, Task 3.4
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Form validates input
  - [ ] Create works
  - [ ] Update works

### Task 3.18: Create TaskDetail Page
- **Description**: Detailed view of single task
- **Subtasks**:
  1. Create `src/components/tasks/TaskDetail.jsx`
  2. Display all task fields
  3. Add edit button
  4. Add delete button with confirmation
  5. Add complete toggle
  6. Add back navigation
- **Dependencies**: Task 3.15, Task 3.8
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Task details display
  - [ ] Actions work

### Task 3.19: Create Settings Page
- **Description**: User settings and preferences
- **Subtasks**:
  1. Create `src/components/settings/Settings.jsx`
  2. Add theme preference (light/dark)
  3. Add notification toggle
  4. Add AI assistant toggle
  5. Add AI provider select
  6. Fetch current settings
  7. Save changes
- **Dependencies**: Task 3.3, Task 3.8, Task 3.10
- **Priority**: Medium
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Settings load
  - [ ] Changes save

### Task 3.20: Create Home Page
- **Description**: Landing page (public)
- **Subtasks**:
  1. Create `src/components/Home.jsx`
  2. Add hero section
  3. Add feature highlights
  4. Add login/register CTAs
  5. Redirect if logged in
- **Dependencies**: Task 3.6, Task 3.8
- **Priority**: Medium
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Home page displays
  - [ ] Redirects when logged in

### Task 3.21: Add Custom Hooks
- **Description**: Create reusable React hooks
- **Subtasks**:
  1. Create `src/hooks/useAuth.js`
  2. Add login, logout, register functions
  3. Create `src/hooks/useTasks.js`
  4. Add CRUD functions for tasks
  5. Add error handling
- **Dependencies**: Task 3.9, Task 3.10
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Hooks work correctly
  - [ ] Can be used in components

### Task 3.22: Add Responsive Design
- **Description**: Ensure mobile responsiveness
- **Subtasks**:
  1. Test all pages on mobile viewport
  2. Fix layout issues
  3. Add mobile menu
  4. Optimize touch targets
  5. Test on actual device
- **Dependencies**: All Phase 3 tasks
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] All pages work on mobile
  - [ ] No horizontal scroll

### Task 3.23: Add Error Boundaries
- **Description**: React error boundaries for graceful failures
- **Subtasks**:
  1. Create ErrorBoundary component
  2. Wrap app routes
  3. Add fallback UI
  4. Log errors
- **Dependencies**: Task 3.8
- **Priority**: Medium
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] Errors caught gracefully
  - [ ] Fallback displays

### Task 3.24: Add Loading States
- **Description**: Add loading indicators throughout app
- **Subtasks**:
  1. Add loading to all async operations
  2. Add skeleton loaders where appropriate
  3. Add button loading states
  4. Test all flows
- **Dependencies**: Task 3.5
- **Priority**: Medium
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Loading states visible
  - [ ] No infinite loaders

### Task 3.25: Add Form Validation
- **Description**: Client-side form validation
- **Subtasks**:
  1. Add validation to login form
  2. Add validation to register form
  3. Add validation to task form
  4. Add error messages
  5. Add real-time validation
- **Dependencies**: Task 3.11, Task 3.12, Task 3.17
- **Priority**: Medium
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Forms validate
  - [ ] Errors display

### Task 3.26: Add Toast Notifications
- **Description**: Toast/notification system
- **Subtasks**:
  1. Create Toast component
  2. Add success, error, warning types
  3. Add auto-dismiss
  4. Integrate with API errors
  5. Add to auth flows
  6. Add to task CRUD
- **Dependencies**: Task 3.4
- **Priority**: Medium
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Toasts display
  - [ ] Auto-dismiss works

### Task 3.27: Setup Environment Configuration
- **Description**: Configure environment variables for frontend
- **Subtasks**:
  1. Create `.env` file
  2. Add VITE_API_URL
  3. Create `.env.example`
  4. Update API service to use env
- **Dependencies**: Task 3.10
- **Priority**: High
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] Env vars load correctly
  - [ ] API URL configurable

### Task 3.28: Frontend Integration Testing
- **Description**: Test frontend integration with backend
- **Subtasks**:
  1. Test login flow end-to-end
  2. Test task CRUD end-to-end
  3. Test AI recommendations
  4. Test settings
  5. Fix any integration issues
- **Dependencies**: Phase 2 complete, Phase 3 complete
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] All flows work end-to-end
  - [ ] No console errors

---

## Phase 4: AI Integration (16 hours)

### Task 4.1: Test CLI Integration
- **Description**: Verify CLI wrapper works with actual AI
- **Subtasks**:
  1. Test Claude CLI call
  2. Test Qwen CLI call
  3. Verify response format
  4. Handle errors
  5. Document which CLI works best
- **Dependencies**: Task 2.23
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] CLI responds
  - [ ] Responses parse correctly

### Task 4.2: Create AI Prompts
- **Description**: Design prompts for AI recommendations
- **Subtasks**:
  1. Create task analysis prompt
  2. Create task optimization prompt
  3. Create task recommendation prompt
  4. Test prompts with sample data
  5. Refine for best results
- **Dependencies**: Task 4.1
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Prompts generate useful output
  - [ ] Output is consistent

### Task 4.3: Implement Recommendation Generation
- **Description**: Build recommendation engine
- **Subtasks**:
  1. Update `ai_service.py`
  2. Fetch user tasks
  3. Build context for AI
  4. Call AI with prompt
  5. Parse response
  6. Extract recommendations
  7. Add confidence scoring
- **Dependencies**: Task 4.2, Task 2.18
- **Priority**: High
- **Estimated Effort**: 2.5 hours
- **Acceptance Criteria**:
  - [ ] Recommendations generated
  - [ ] Confidence scores assigned

### Task 4.4: Add Caching Layer
- **Description**: Cache AI responses to reduce API calls
- **Subtasks**:
  1. Add cache table or in-memory cache
  2. Cache key: user_id + context_hash
  3. Set TTL (e.g., 1 hour)
  4. Check cache before calling AI
  5. Invalidate on task changes
- **Dependencies**: Task 4.3
- **Priority**: Medium
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Cache works
  - [ ] Reduces AI calls

### Task 4.5: Implement Task Optimization
- **Description**: AI-powered task optimization
- **Subtasks**:
  1. Create optimize endpoint
  2. Send task details to AI
  3. Get optimization suggestions
  4. Return structured suggestions
  5. Test with various tasks
- **Dependencies**: Task 4.2
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Optimization works
  - [ ] Suggestions are actionable

### Task 4.6: Add AI History Tracking
- **Description**: Track AI interactions
- **Subtasks**:
  1. Implement history endpoint
  2. Query AIRecommendations table
  3. Filter by user
  4. Add pagination
  5. Include accept/reject status
- **Dependencies**: Task 2.5
- **Priority**: Medium
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] History retrieves correctly
  - [ ] Pagination works

### Task 4.7: Integrate AI Panel with Backend
- **Description**: Connect frontend AI panel to API
- **Subtasks**:
  1. Update AIPanel component
  2. Add API call to recommend endpoint
  3. Display loading state
  4. Display recommendations
  5. Add accept/reject handlers
  6. Update recommendation status
- **Dependencies**: Task 3.16, Task 2.25
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Panel connects to API
  - [ ] Recommendations display
  - [ ] Accept/reject works

### Task 4.8: Add AI Error Handling
- **Description**: Graceful degradation when AI unavailable
- **Subtasks**:
  1. Add timeout handling
  2. Add retry logic
  3. Add fallback message
  4. Disable AI features gracefully
  5. Show user-friendly errors
- **Dependencies**: Task 4.1
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Errors handled gracefully
  - [ ] App still usable

### Task 4.9: Test AI Recommendations
- **Description**: Manual testing of AI features
- **Subtasks**:
  1. Create test tasks
  2. Request recommendations
  3. Verify relevance
  4. Test optimization
  5. Test edge cases
  6. Document results
- **Dependencies**: Task 4.3, Task 4.5
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Recommendations are relevant
  - [ ] Edge cases handled

### Task 4.10: Optimize AI Performance
- **Description**: Improve AI response times
- **Subtasks**:
  1. Measure current response times
  2. Optimize prompts
  3. Improve caching
  4. Add streaming if possible
  5. Verify improvements
- **Dependencies**: Task 4.3, Task 4.4
- **Priority**: Medium
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Response time < 5 seconds
  - [ ] Caching effective

### Task 4.11: Add AI Rate Limiting
- **Description**: Prevent AI API abuse
- **Subtasks**:
  1. Add rate limit middleware
  2. Limit: 10 requests per minute per user
  3. Return 429 on exceed
  4. Add retry-after header
  5. Test rate limiting
- **Dependencies**: Task 2.25
- **Priority**: Medium
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Rate limiting works
  - [ ] Proper errors returned

### Task 4.12: Document AI Integration
- **Description**: Document AI features and usage
- **Subtasks**:
  1. Write AI feature documentation
  2. Document prompt engineering
  3. Add usage examples
  4. Document limitations
  5. Add to README
- **Dependencies**: All AI tasks
- **Priority**: Low
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Documentation complete
  - [ ] Examples work

---

## Phase 5: Testing & QA (16 hours)

### Task 5.1: Setup Pytest
- **Description**: Configure pytest for backend testing
- **Subtasks**:
  1. Create `backend/pytest.ini`
  2. Create `backend/tests/conftest.py`
  3. Add test database fixture
  4. Add client fixture
  5. Add auth fixtures
- **Dependencies**: Task 2.12
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Pytest runs
  - [ ] Fixtures work

### Task 5.2: Write Auth Tests
- **Description**: Unit tests for authentication
- **Subtasks**:
  1. Create `backend/tests/test_auth.py`
  2. Test register endpoint
  3. Test login endpoint
  4. Test get current user
  5. Test invalid credentials
  6. Test token expiration
- **Dependencies**: Task 5.1, Task 2.13, Task 2.14
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] All auth tests pass
  - [ ] Coverage > 80%

### Task 5.3: Write Task Tests
- **Description**: Unit tests for task endpoints
- **Subtasks**:
  1. Create `backend/tests/test_tasks.py`
  2. Test create task
  3. Test list tasks
  4. Test get task
  5. Test update task
  6. Test delete task
  7. Test user isolation
  8. Test complete task
- **Dependencies**: Task 5.1, Task 2.19
- **Priority**: High
- **Estimated Effort**: 2.5 hours
- **Acceptance Criteria**:
  - [ ] All task tests pass
  - [ ] User isolation verified

### Task 5.4: Write AI Tests
- **Description**: Unit tests for AI endpoints
- **Subtasks**:
  1. Create `backend/tests/test_ai.py`
  2. Test recommend endpoint
  3. Test optimize endpoint
  4. Test history endpoint
  5. Mock AI CLI calls
  6. Test rate limiting
- **Dependencies**: Task 5.1, Task 2.25
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] All AI tests pass
  - [ ] Mocks work correctly

### Task 5.5: Write Service Tests
- **Description**: Tests for service layer
- **Subtasks**:
  1. Test auth_service.py
  2. Test task_service.py
  3. Test ai_service.py
  4. Test security utilities
  5. Achieve coverage
- **Dependencies**: Task 5.1
- **Priority**: Medium
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Service tests pass
  - [ ] Coverage improved

### Task 5.6: Setup React Testing Library
- **Description**: Configure frontend testing
- **Subtasks**:
  1. Install testing dependencies
  2. Create test setup file
  3. Add custom renders
  4. Configure mocks
- **Dependencies**: Task 1.7
- **Priority**: Medium
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] Tests can run
  - [ ] RTL configured

### Task 5.7: Write Component Tests
- **Description**: Test React components
- **Subtasks**:
  1. Test Button component
  2. Test Input component
  3. Test TaskCard component
  4. Test TaskForm component
  5. Test AIPanel component
- **Dependencies**: Task 5.6
- **Priority**: Medium
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Component tests pass
  - [ ] Interactions tested

### Task 5.8: Write Hook Tests
- **Description**: Test custom hooks
- **Subtasks**:
  1. Test useAuth hook
  2. Test useTasks hook
  3. Mock API calls
  4. Test error states
- **Dependencies**: Task 5.6
- **Priority**: Medium
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Hook tests pass

### Task 5.9: Run Manual QA - Auth Flow
- **Description**: Manual testing of authentication
- **Subtasks**:
  1. Test registration
  2. Test login
  3. Test logout
  4. Test password change
  5. Test error states
  6. Document results
- **Dependencies**: Phase 3 complete
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] All scenarios pass
  - [ ] No bugs found

### Task 5.10: Run Manual QA - Task Flow
- **Description**: Manual testing of task management
- **Subtasks**:
  1. Test create task
  2. Test view tasks
  3. Test update task
  4. Test delete task
  5. Test filter/sort
  6. Test complete task
- **Dependencies**: Phase 3 complete
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] All scenarios pass

### Task 5.11: Run Manual QA - AI Features
- **Description**: Manual testing of AI recommendations
- **Subtasks**:
  1. Test AI panel
  2. Test recommendations
  3. Test optimization
  4. Test accept/reject
  5. Test error states
- **Dependencies**: Phase 4 complete
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] AI features work
  - [ ] Recommendations useful

### Task 5.12: Run Manual QA - Settings
- **Description**: Manual testing of settings
- **Subtasks**:
  1. Test view settings
  2. Test update settings
  3. Test all toggles
  4. Test persistence
- **Dependencies**: Phase 3 complete
- **Priority**: Medium
- **Estimated Effort**: 30 minutes
- **Acceptance Criteria**:
  - [ ] Settings work

### Task 5.13: Performance Testing
- **Description**: Test application performance
- **Subtasks**:
  1. Test API response times
  2. Test frontend load times
  3. Test with multiple users
  4. Identify bottlenecks
  5. Document results
- **Dependencies**: All features complete
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Performance within budgets
  - [ ] No major bottlenecks

### Task 5.14: Bug Fixing
- **Description**: Fix bugs found during testing
- **Subtasks**:
  1. Triage bugs by severity
  2. Fix critical bugs
  3. Fix major bugs
  4. Re-test fixes
  5. Document fixes
- **Dependencies**: All testing tasks
- **Priority**: High
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Critical bugs fixed
  - [ ] Major bugs fixed

### Task 5.15: Code Coverage Report
- **Description**: Generate and review coverage
- **Subtasks**:
  1. Run coverage for backend
  2. Run coverage for frontend
  3. Generate reports
  4. Review gaps
  5. Add missing tests if needed
  6. Ensure > 80% coverage
- **Dependencies**: All test tasks
- **Priority**: Medium
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Coverage > 80%
  - [ ] Report generated

---

## Phase 6: Deployment (8 hours)

### Task 6.1: Create Backend Dockerfile
- **Description**: Dockerize backend application
- **Subtasks**:
  1. Create `backend/Dockerfile`
  2. Use Python 3.13.5 base image
  3. Copy requirements and install
  4. Copy application code
  5. Set entrypoint to uvicorn
  6. Expose port 8000
  7. Test build
- **Dependencies**: Phase 2 complete
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Docker image builds
  - [ ] Container runs
  - [ ] API accessible

### Task 6.2: Create Frontend Dockerfile
- **Description**: Dockerize frontend application
- **Subtasks**:
  1. Create `frontend/Dockerfile`
  2. Use Node v24 base image
  3. Install dependencies
  4. Build application
  5. Serve with nginx (multi-stage)
  6. Expose port 80
  7. Test build
- **Dependencies**: Phase 3 complete
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Docker image builds
  - [ ] Container runs
  - [ ] Frontend accessible

### Task 6.3: Create Docker Compose
- **Description**: Orchestrate multi-container setup
- **Subtasks**:
  1. Create `docker-compose.yml`
  2. Define backend service
  3. Define frontend service
  4. Define database service (if PostgreSQL)
  5. Add networking
  6. Add volume mounts
  7. Add environment variables
- **Dependencies**: Task 6.1, Task 6.2
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] `docker-compose up` works
  - [ ] All services start
  - [ ] Services communicate

### Task 6.4: Create Environment Configuration
- **Description**: Setup environment variables for deployment
- **Subtasks**:
  1. Update `.env.example`
  2. Add all required variables
  3. Document each variable
  4. Add security notes
  5. Create production example
- **Dependencies**: All phases
- **Priority**: High
- **Estimated Effort**: 45 minutes
- **Acceptance Criteria**:
  - [ ] All variables documented
  - [ ] Example is usable

### Task 6.5: Write README
- **Description**: Create comprehensive README
- **Subtasks**:
  1. Add project description
  2. Add features list
  3. Add tech stack
  4. Add setup instructions
  5. Add usage instructions
  6. Add API documentation link
  7. Add contributing guidelines
- **Dependencies**: All phases
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] README complete
  - [ ] Setup instructions work

### Task 6.6: Write Deployment Guide
- **Description**: Create deployment documentation
- **Subtasks**:
  1. Create `DEPLOYMENT.md`
  2. Document Docker deployment
  3. Document environment setup
  4. Document production considerations
  5. Add troubleshooting
- **Dependencies**: Task 6.3
- **Priority**: High
- **Estimated Effort**: 1 hour
- **Acceptance Criteria**:
  - [ ] Guide complete
  - [ ] Steps are clear

### Task 6.7: Final Verification
- **Description**: End-to-end verification of deployment
- **Subtasks**:
  1. Clean environment
  2. Run `docker-compose up`
  3. Test all features
  4. Verify persistence
  5. Test restart
  6. Document any issues
- **Dependencies**: All deployment tasks
- **Priority**: High
- **Estimated Effort**: 1.5 hours
- **Acceptance Criteria**:
  - [ ] Fresh deploy works
  - [ ] All features functional

### Task 6.8: Optional Kubernetes Manifests
- **Description**: Create K8s deployment files (optional)
- **Subtasks**:
  1. Create `k8s/` directory
  2. Create backend deployment
  3. Create frontend deployment
  4. Create services
  5. Create configmaps
  6. Create secrets template
  7. Document K8s deployment
- **Dependencies**: Task 6.3
- **Priority**: Low
- **Estimated Effort**: 2 hours
- **Acceptance Criteria**:
  - [ ] Manifests created
  - [ ] Can deploy to Minikube

---

## Appendix: Task Dependencies Graph

```
Phase 1 (Environment)
├── 1.1 Python ──┬──> 1.3 venv ──> 1.6 Backend deps ──> Phase 2
│                └──> 1.5 CLI tools ──> 2.23 AI CLI wrapper
└── 1.2 Node ────> 1.7 Frontend ──> Phase 3

Phase 2 (Backend)
├── 2.1 Database ──> 2.2-2.5 Models ──> 2.6 Migrations
├── 2.10 Security ──> 2.11 JWT ──> 2.13-2.17 Auth routes
├── 2.18 Task service ──> 2.19 Task routes
├── 2.23 AI CLI ──> 2.24 AI service ──> 2.25 AI routes
└── All routes ──> Phase 3 integration

Phase 3 (Frontend)
├── 3.1 Tailwind ──> 3.2-3.5 Shared components
├── 3.2-3.5 ──> 3.6-3.7 Layout
├── 3.8 Router ──> 3.11-3.20 Pages
├── 3.9 Store ──> 3.10 API ──> All pages
└── All pages ──> 3.22 Responsive ──> 3.28 Integration

Phase 4 (AI)
├── 4.1 CLI test ──> 4.2 Prompts ──> 4.3 Recommendations
├── 4.3 ──> 4.4 Caching ──> 4.10 Optimization
├── 3.16 AIPanel ──> 4.7 Integration
└── 4.9 Testing ──> Phase 5

Phase 5 (Testing)
├── 5.1-5.5 Backend tests
├── 5.6-5.8 Frontend tests
├── 5.9-5.12 Manual QA
├── 5.13 Performance
└── 5.14 Bug fixes

Phase 6 (Deployment)
├── 6.1 Backend Docker ──┬──> 6.3 Docker compose ──> 6.7 Verification
├── 6.2 Frontend Docker ─┘
├── 6.4 Env config ──> 6.5 README ──> 6.6 Deployment guide
└── 6.8 K8s (optional)
```

---

## Task Priority Summary

### High Priority (71 tasks)
- All Phase 1 tasks (5)
- Core backend: Database, Models, Auth, Tasks (16)
- Core frontend: Components, Pages, State (18)
- AI integration: Core features (8)
- Testing: Critical tests (10)
- Deployment: Docker, docs (14)

### Medium Priority (18 tasks)
- Settings features (4)
- Additional frontend polish (6)
- AI enhancements (4)
- Additional tests (4)

### Low Priority (3 tasks)
- AI documentation (1)
- Kubernetes manifests (1)
- Optional enhancements (1)

---

**Version**: 1.0.0  
**Status**: Ready for Implementation  
**Next Step**: Begin Phase 1, Task 1.1
