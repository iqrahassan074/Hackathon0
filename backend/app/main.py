"""
Hackathon_0 Backend Application
Main entry point and app configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import os

from app.routes import auth, tasks, settings, ai
from app.utils.logging_config import setup_logging
from app.database import engine, Base
from app.utils.error_handler import (
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
    AppException
)

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Hackathon_0 API",
    description="Full-stack application with AI-powered task recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(settings.router, prefix="/api/v1/settings", tags=["Settings"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Hackathon_0 API",
        "docs": "/docs",
        "health": "/health"
    }
