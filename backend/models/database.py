"""
Database models for Emergency Info Card System
"""
import os
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Integer,
    create_engine
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# =====================================================
# DATABASE CONFIG
# =====================================================

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable is not set")

# ⭐ FIX: Render provides postgres:// but SQLAlchemy 2.0+ needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    print(f"✅ Fixed DATABASE_URL format: postgres:// → postgresql://")

print(f"🔗 Connecting to database: {DATABASE_URL[:30]}...")

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        echo=False  # Set to True for SQL debugging
    )
    print("✅ Database engine created successfully")
except Exception as e:
    print(f"❌ Failed to create database engine: {e}")
    raise

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# =====================================================
# DB DEPENDENCY (USED IN auth.py, profile.py, public.py)
# =====================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================
# INIT DB (CALLED IN main.py STARTUP EVENT)
# =====================================================

def init_db():
    """Create all database tables"""
    try:
        print("🔄 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        raise

# =====================================================
# UTILS
# =====================================================

def generate_uuid():
    return str(uuid.uuid4())

# =====================================================
# MODELS
# =====================================================

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
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    emergency_profile = relationship(
        "EmergencyProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    emergency_contacts = relationship(
        "EmergencyContact",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    access_logs = relationship(
        "AccessLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )


class EmergencyProfile(Base):
    __tablename__ = "emergency_profiles"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    public_id = Column(String, unique=True, nullable=False, index=True)

    full_name = Column(String)
    age = Column(Integer)
    blood_group = Column(String(10))

    allergies = Column(Text)
    medical_conditions = Column(Text)
    medications = Column(Text)

    doctor_name = Column(String)
    doctor_phone = Column(String)

    organ_donor = Column(Boolean, default=False)
    notes = Column(Text)

    show_name = Column(Boolean, default=True)
    show_age = Column(Boolean, default=True)
    show_blood_group = Column(Boolean, default=True)
    show_allergies = Column(Boolean, default=True)
    show_conditions = Column(Boolean, default=True)
    show_medications = Column(Boolean, default=True)

    qr_code_path = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="emergency_profile"
    )


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(String, nullable=False)
    relation = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String)
    priority = Column(Integer, default=1)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="emergency_contacts"
    )


class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    accessed_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)
    user_agent = Column(String)

    user = relationship(
        "User",
        back_populates="access_logs"
    )
