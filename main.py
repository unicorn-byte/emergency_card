"""
Main FastAPI application entry point
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from backend.config import settings
from backend.models.database import init_db
from backend.api import auth, profile, public

# =====================================================
# CREATE DB TABLES ON STARTUP
# =====================================================
init_db()

# =====================================================
# FASTAPI APP
# =====================================================
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Emergency Info Card System - Save Lives with Quick Access to Medical Information",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =====================================================
# CORS
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# STATIC FILES (OPTIONAL)
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# =====================================================
# ROUTERS
# =====================================================
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(public.router)

# =====================================================
# ROOT
# =====================================================
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h1>🚨 Emergency Info Card System</h1>
    <p>API is running successfully.</p>
    <ul>
        <li><a href="/docs">Swagger Docs</a></li>
        <li><a href="/redoc">ReDoc</a></li>
    </ul>
    """

# =====================================================
# HEALTH CHECK (RENDER USES THIS)
# =====================================================
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
