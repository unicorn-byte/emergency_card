"""
Database models for Emergency Info Card System
"""
import os
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Boolean, DateTime, Text,
    ForeignKey, Integer, create_engine
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# =======================
# DATABASE CONFIG
# =======================

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# =======================
# DB DEPENDENCY
# =======================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =======================
# INIT DB (CALLED IN main.py)
# =======================

def init_db():
    Base.metadata.create_all(bind=engine)

# =======================
# UTILS
# =======================

def generate_uuid():
    return str(uuid.uuid4())

# =======================
# MODELS
# =======================

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    phone = Column(String)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    emergency_profile = relationship(
        "EmergencyProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class EmergencyProfile(Base):
    __tablename__ = "emergency_profiles"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    public_id = Column(String, unique=True, nullable=False, index=True)

    full_name = Column(String)
    age = Column(Integer)
    blood_group = Column(String(10))

    allergies = Column(Text)
    medical_conditions = Column(Text)
    medications = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="emergency_profile")
