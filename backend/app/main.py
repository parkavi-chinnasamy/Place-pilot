
"""
PlacePilot - FastAPI Application Entry Point
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import engine, Base
from .routes import (
    auth,
    student,
    assessment,
    readiness,
    interview,
    resume,
    leetcode,
    jobroles,
    admin,
    recommendations,
    skill_dictionary,
    coding,
)
from .database import SessionLocal
from .routes.coding import ensure_coding_problems_seeded
from .services.leetcode_service import ensure_leetcode_progress_columns

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="PlacePilot API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
os.makedirs(settings.upload_dir, exist_ok=True)


@app.on_event("startup")
def startup_event():
    """Initialize the LeetCode database columns and seed initial coding problems."""
    ensure_leetcode_progress_columns()
    try:
        db = SessionLocal()
        ensure_coding_problems_seeded(db)
        db.close()
    except Exception as e:
        print(f"Warning: Could not seed coding problems: {e}")


# Register API routers
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(assessment.router)
app.include_router(readiness.router)
app.include_router(interview.router)
app.include_router(resume.router)
app.include_router(leetcode.router)
app.include_router(jobroles.router)
app.include_router(admin.router)
app.include_router(recommendations.router)
app.include_router(skill_dictionary.router)
app.include_router(coding.router)


@app.get("/")
def root():
    return {
        "app": "PlacePilot API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "placepilot-api",
    }
