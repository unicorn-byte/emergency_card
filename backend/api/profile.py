"""
Emergency Profile API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from backend.models import get_db
from backend.models.database import User, EmergencyProfile, EmergencyContact
from backend.models.schemas import (
    EmergencyProfileCreate,
    EmergencyProfileUpdate,
    EmergencyProfileResponse,
    EmergencyContactCreate,
    EmergencyContactResponse,
    QRCodeResponse
)
from backend.api.auth import get_current_user
from backend.utils.security import encryptor
from backend.utils.qr_generator import generate_qr_code
from backend.config import settings

router = APIRouter(prefix="/profile", tags=["Emergency Profile"])


@router.post("", response_model=EmergencyProfileResponse, status_code=status.HTTP_201_CREATED)
def create_emergency_profile(
    profile_data: EmergencyProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create emergency profile for current user"""
    
    # Check if profile already exists
    existing_profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emergency profile already exists. Use PUT to update."
        )
    
    # Generate unique public ID for QR code
    public_id = str(uuid.uuid4())[:8]  # Short unique ID
    
    # Encrypt sensitive data
    allergies_encrypted = encryptor.encrypt_json(
        profile_data.allergies.split(',') if profile_data.allergies else []
    )
    conditions_encrypted = encryptor.encrypt_json(
        profile_data.medical_conditions.split(',') if profile_data.medical_conditions else []
    )
    medications_encrypted = encryptor.encrypt_json(
        profile_data.medications.split(',') if profile_data.medications else []
    )
    
    # Create profile
    new_profile = EmergencyProfile(
        user_id=current_user.id,
        public_id=public_id,
        full_name=profile_data.full_name or current_user.full_name,
        age=profile_data.age,
        blood_group=profile_data.blood_group,
        allergies=allergies_encrypted,
        medical_conditions=conditions_encrypted,
        medications=medications_encrypted,
        doctor_name=profile_data.doctor_name,
        doctor_phone=profile_data.doctor_phone,
        organ_donor=profile_data.organ_donor,
        notes=profile_data.notes
    )
    
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    
    return new_profile


@router.get("", response_model=EmergencyProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's emergency profile"""
    
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency profile not found. Please create one first."
        )
    
    return profile


@router.put("", response_model=EmergencyProfileResponse)
def update_emergency_profile(
    profile_data: EmergencyProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update emergency profile"""
    
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency profile not found."
        )
    
    # Update fields
    update_data = profile_data.model_dump(exclude_unset=True)
    
    # Handle encrypted fields
    if 'allergies' in update_data and update_data['allergies']:
        update_data['allergies'] = encryptor.encrypt_json(
            update_data['allergies'].split(',')
        )
    if 'medical_conditions' in update_data and update_data['medical_conditions']:
        update_data['medical_conditions'] = encryptor.encrypt_json(
            update_data['medical_conditions'].split(',')
        )
    if 'medications' in update_data and update_data['medications']:
        update_data['medications'] = encryptor.encrypt_json(
            update_data['medications'].split(',')
        )
    
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    
    return profile


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_emergency_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete emergency profile"""
    
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency profile not found."
        )
    
    db.delete(profile)
    db.commit()
    
    return None


@router.get("/qr-code", response_model=QRCodeResponse)
def get_qr_code(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate QR code for emergency profile"""

    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency profile not found."
        )

    # ✅ IMPORTANT: Point QR to UI view
    emergency_url = f"http://localhost:8000/emergency/{profile.public_id}"


    qr_base64, _ = generate_qr_code(emergency_url)

    return {
        "qr_code_base64": qr_base64,
        "public_url": emergency_url,
        "public_id": profile.public_id
    }

# Emergency Contacts Management
@router.post("/contacts", response_model=EmergencyContactResponse, status_code=status.HTTP_201_CREATED)
def add_emergency_contact(
    contact_data: EmergencyContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add emergency contact (no duplicates allowed)"""

    # 🔒 DUPLICATE CHECK (IMPORTANT)
    existing_contact = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == current_user.id,
        EmergencyContact.phone == contact_data.phone
    ).first()

    if existing_contact:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emergency contact with this phone number already exists"
        )

    new_contact = EmergencyContact(
        user_id=current_user.id,
        **contact_data.model_dump()
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact



@router.get("/contacts", response_model=List[EmergencyContactResponse])
def get_emergency_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all emergency contacts"""
    
    contacts = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == current_user.id
    ).order_by(EmergencyContact.priority).all()
    
    return contacts


@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_emergency_contact(
    contact_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete emergency contact"""
    
    contact = db.query(EmergencyContact).filter(
        EmergencyContact.id == contact_id,
        EmergencyContact.user_id == current_user.id
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emergency contact not found."
        )
    
    db.delete(contact)
    db.commit()
    
    return None
