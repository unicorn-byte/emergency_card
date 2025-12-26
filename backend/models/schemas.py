"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    # ⭐ FIX: Added max_length=72
    password: str = Field(..., min_length=8, max_length=72)
    
    # ⭐ FIX: Added validator to check byte length
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long (max 72 bytes)')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# Emergency Profile Schemas
class EmergencyProfileBase(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=150)
    blood_group: Optional[str] = Field(None, pattern="^(A|B|AB|O)[+-]$")
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    medications: Optional[str] = None
    doctor_name: Optional[str] = None
    doctor_phone: Optional[str] = None
    organ_donor: bool = False
    notes: Optional[str] = None


class EmergencyProfileCreate(EmergencyProfileBase):
    pass


class EmergencyProfileUpdate(EmergencyProfileBase):
    show_name: Optional[bool] = True
    show_age: Optional[bool] = True
    show_blood_group: Optional[bool] = True
    show_allergies: Optional[bool] = True
    show_conditions: Optional[bool] = True
    show_medications: Optional[bool] = True


class EmergencyProfileResponse(EmergencyProfileBase):
    id: str
    public_id: str
    qr_code_url: Optional[str] = None
    show_name: bool
    show_age: bool
    show_blood_group: bool
    show_allergies: bool
    show_conditions: bool
    show_medications: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Public Emergency Card (Read-only, limited info)
class PublicEmergencyCard(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    blood_group: Optional[str] = None
    allergies: Optional[List[str]] = None
    medical_conditions: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    organ_donor: bool = False
    emergency_contacts: List[dict] = []


# Emergency Contact Schemas
class EmergencyContactBase(BaseModel):
    name: str
    relation: str
    phone: str
    email: Optional[EmailStr] = None
    priority: int = Field(1, ge=1, le=5)


class EmergencyContactCreate(EmergencyContactBase):
    pass


class EmergencyContactUpdate(EmergencyContactBase):
    pass


class EmergencyContactResponse(EmergencyContactBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# QR Code Generation
class QRCodeResponse(BaseModel):
    qr_code_base64: str
    public_url: str
    public_id: str


# PDF Generation
class PDFCardRequest(BaseModel):
    include_photo: bool = False
    card_size: str = Field("credit", pattern="^(credit|business)$")


# Access Log
class AccessLogResponse(BaseModel):
    id: str
    accessed_at: datetime
    ip_address: Optional[str]
    
    class Config:
        from_attributes = True
