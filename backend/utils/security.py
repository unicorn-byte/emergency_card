"""
Security utilities for authentication and encryption
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from backend.config import settings
import base64
import json

# =====================
# Password hashing
# =====================
# Using bcrypt_sha256 to avoid 72-byte bcrypt limitation issues on Render

pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


# =====================
# JWT Tokens
# =====================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return email"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None


# =====================
# Data Encryption
# =====================

class DataEncryption:
    """Handle encryption/decryption of sensitive data"""

    def __init__(self):
        key = settings.ENCRYPTION_KEY.encode()

        # Ensure Fernet-compatible key (32 bytes, base64)
        if len(key) < 32:
            key = key.ljust(32, b"0")

        self.key = base64.urlsafe_b64encode(key[:32])
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        if not data:
            return ""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        if not encrypted_data:
            return ""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return ""

    def encrypt_json(self, data) -> str:
        if not data:
            return ""
        return self.encrypt(json.dumps(data))

    def decrypt_json(self, encrypted_data: str):
        if not encrypted_data:
            return []
        try:
            return json.loads(self.decrypt(encrypted_data))
        except Exception:
            return []


# Singleton instance
encryptor = DataEncryption()
