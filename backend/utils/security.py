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

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return email"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None


# Data Encryption
class DataEncryption:
    """Handle encryption/decryption of sensitive data"""
    
    def __init__(self):
        # Generate or use existing encryption key
        key = settings.ENCRYPTION_KEY.encode()
        # Ensure key is base64 encoded and proper length for Fernet
        if len(key) < 32:
            # Pad key to 32 bytes
            key = key.ljust(32, b'0')
        self.key = base64.urlsafe_b64encode(key[:32])
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        if not data:
            return ""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        if not encrypted_data:
            return ""
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            return ""
    
    def encrypt_json(self, data: list) -> str:
        """Encrypt list/dict as JSON"""
        if not data:
            return ""
        json_str = json.dumps(data)
        return self.encrypt(json_str)
    
    def decrypt_json(self, encrypted_data: str) -> list:
        """Decrypt JSON data back to list/dict"""
        if not encrypted_data:
            return []
        try:
            json_str = self.decrypt(encrypted_data)
            if json_str:
                return json.loads(json_str)
        except Exception as e:
            print(f"JSON decryption error: {e}")
        return []


# Singleton instance
encryptor = DataEncryption()
