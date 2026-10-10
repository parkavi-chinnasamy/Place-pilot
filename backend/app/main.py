"""
PlacePilot – FastAPI Application Entry Point
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import get_settings
from .database import engine, Base
from .routes import auth, student, assessment, readiness, interview, resume, leetcode, jobroles, admin, recommendations

settings = get_settings()

# Create tables (dev only – use Alembic for production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PlacePilot API",
    description="Smart Placement Preparation Platform – Backend API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File uploads directory
os.makedirs(settings.upload_dir, exist_ok=True)

# Include all routers
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
    return {"status": "healthy"}
