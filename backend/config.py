"""
Configuration settings for the Emergency Info Card System
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # =====================================================
    # APPLICATION
    # =====================================================
    APP_NAME: str = "Emergency Info Card System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False   # ❗ Production lo False

    # =====================================================
    # DATABASE
    # (Render lo DATABASE_URL env var automatic ga set avutundi)
    # =====================================================
    DATABASE_URL: str

    # =====================================================
    # SECURITY
    # =====================================================
    SECRET_KEY: str
    ENCRYPTION_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # =====================================================
    # FRONTEND / PUBLIC BASE URL
    # (Mee Render app URL)
    # =====================================================
    FRONTEND_URL: str = "https://emergency-card.onrender.com"

    # =====================================================
    # OPTIONAL: EMAIL
    # =====================================================
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # =====================================================
    # OPTIONAL: SMS (TWILIO)
    # =====================================================
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
