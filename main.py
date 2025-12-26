"""
Main FastAPI application entry point
"""
import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse

from backend.config import settings
from backend.models.database import init_db
from backend.api import auth, profile, public

# =====================================================
# LOGGING SETUP
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
# STARTUP EVENT - Initialize database
# =====================================================
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    try:
        logger.info("🚀 Starting Emergency Info Card System...")
        init_db()
        logger.info("✅ Application started successfully!")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}", exc_info=True)
        # Continue anyway so we can check logs in Render

# =====================================================
# GLOBAL EXCEPTION HANDLER
# =====================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"❌ Error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An error occurred",
            "path": request.url.path
        }
    )

# =====================================================
# CORS
# =====================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for now, configure properly in production
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
    logger.info(f"✅ Static files mounted")

# =====================================================
# ROUTERS
# =====================================================
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(public.router)

logger.info("✅ All API routers registered")

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
        <li><a href="/health">Health Check</a></li>
    </ul>
    """

# =====================================================
# HEALTH CHECK (RENDER USES THIS)
# =====================================================
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    db_status = "unknown"
    
    try:
        from backend.models.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "connected"
        logger.info("✅ Health check passed")
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        db_status = f"error: {str(e)[:50]}"
    
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": db_status
    }
