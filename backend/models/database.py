"""
Database models for Emergency Info Card System
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    emergency_profile = relationship("EmergencyProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    emergency_contacts = relationship("EmergencyContact", back_populates="user", cascade="all, delete-orphan")
    access_logs = relationship("AccessLog", back_populates="user", cascade="all, delete-orphan")


class EmergencyProfile(Base):
    __tablename__ = "emergency_profiles"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Public identifier for QR code (not revealing actual user ID)
    public_id = Column(String, unique=True, nullable=False, index=True)
    
    # Basic Info
    full_name = Column(String)
    age = Column(Integer, nullable=True)
    blood_group = Column(String(10), nullable=True)
    
    # Medical Information (Encrypted)
    allergies = Column(Text, nullable=True)  # Encrypted JSON
    medical_conditions = Column(Text, nullable=True)  # Encrypted JSON
    medications = Column(Text, nullable=True)  # Encrypted JSON
    doctor_name = Column(String, nullable=True)
    doctor_phone = Column(String, nullable=True)
    
    # Additional Info
    organ_donor = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    
    # Privacy Settings
    show_name = Column(Boolean, default=True)
    show_age = Column(Boolean, default=True)
    show_blood_group = Column(Boolean, default=True)
    show_allergies = Column(Boolean, default=True)
    show_conditions = Column(Boolean, default=True)
    show_medications = Column(Boolean, default=True)
    
    # QR Code
    qr_code_path = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="emergency_profile")


class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    name = Column(String, nullable=False)
    relation = Column(String, nullable=False)  # e.g., "Spouse", "Parent", "Friend"
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    priority = Column(Integer, default=1)  # 1 = Primary, 2 = Secondary, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="emergency_contacts")


class AccessLog(Base):
    __tablename__ = "access_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    accessed_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="access_logs")
