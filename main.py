"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

from backend.config import settings
from backend.models import init_db
from backend.api import auth, profile, public

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Emergency Info Card System - Save Lives with Quick Access to Medical Information",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(public.router)


@app.get("/", response_class=HTMLResponse)
def root():
    """Landing page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Emergency Info Card System</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                max-width: 800px;
                padding: 50px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
            }
            h1 {
                font-size: 48px;
                color: #333;
                margin-bottom: 20px;
            }
            .emoji {
                font-size: 80px;
                margin-bottom: 20px;
            }
            p {
                font-size: 18px;
                color: #666;
                margin-bottom: 30px;
                line-height: 1.6;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 40px 0;
                text-align: left;
            }
            .feature {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            .feature-icon {
                font-size: 30px;
                margin-bottom: 10px;
            }
            .feature h3 {
                font-size: 16px;
                color: #333;
                margin-bottom: 8px;
            }
            .feature p {
                font-size: 14px;
                color: #777;
                margin: 0;
            }
            .btn-group {
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .btn {
                padding: 15px 40px;
                font-size: 16px;
                font-weight: bold;
                text-decoration: none;
                border-radius: 10px;
                transition: all 0.3s;
                display: inline-block;
            }
            .btn-primary {
                background: #667eea;
                color: white;
            }
            .btn-primary:hover {
                background: #5568d3;
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            .btn-secondary {
                background: #f8f9fa;
                color: #333;
                border: 2px solid #ddd;
            }
            .btn-secondary:hover {
                background: #e9ecef;
            }
            .stats {
                margin-top: 40px;
                padding-top: 40px;
                border-top: 2px solid #f0f0f0;
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
            }
            .stat {
                text-align: center;
            }
            .stat-number {
                font-size: 36px;
                font-weight: bold;
                color: #667eea;
            }
            .stat-label {
                font-size: 14px;
                color: #666;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="emoji">🚨</div>
            <h1>Emergency Info Card System</h1>
            <p>
                Save lives by making critical medical information instantly accessible 
                during emergencies. Your medical details, always available when seconds matter.
            </p>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">📱</div>
                    <h3>QR Code Access</h3>
                    <p>Instant access via QR code on your phone's lock screen</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">💳</div>
                    <h3>Physical Card</h3>
                    <p>Print and carry in your wallet for offline access</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🔒</div>
                    <h3>Secure & Private</h3>
                    <p>Your data is encrypted and privacy-controlled</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">📞</div>
                    <h3>One-Tap Contact</h3>
                    <p>Emergency contacts with instant call buttons</p>
                </div>
            </div>
            
            <div class="btn-group">
                <a href="/docs" class="btn btn-primary">📚 API Documentation</a>
                <a href="/redoc" class="btn btn-secondary">📖 API Reference</a>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">⚡</div>
                    <div class="stat-label">Instant Access</div>
                </div>
                <div class="stat">
                    <div class="stat-number">🔐</div>
                    <div class="stat-label">Encrypted Data</div>
                </div>
                <div class="stat">
                    <div class="stat-number">🌍</div>
                    <div class="stat-label">Works Anywhere</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
