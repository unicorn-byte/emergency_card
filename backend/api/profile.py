"""
Emergency Profile API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from backend.models.database import (
    get_db,
    User,
    EmergencyProfile,
    EmergencyContact
)
from backend.api.auth import get_current_user
from backend.models.schemas import (
    EmergencyProfileCreate,
    EmergencyProfileUpdate,
    EmergencyProfileResponse,
    EmergencyContactCreate,
    EmergencyContactResponse,
    QRCodeResponse
)
from backend.utils.security import encryptor
from backend.utils.qr_generator import generate_qr_code
from backend.config import settings

router = APIRouter(prefix="/profile", tags=["Emergency Profile"])

# =====================================================
# CREATE EMERGENCY PROFILE
# =====================================================
@router.post(
    "",
    response_model=EmergencyProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_emergency_profile(
    profile_data: EmergencyProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Emergency profile already exists"
        )

    public_id = str(uuid.uuid4())[:8]

    profile = EmergencyProfile(
        user_id=current_user.id,
        public_id=public_id,
        full_name=profile_data.full_name or current_user.full_name,
        age=profile_data.age,
        blood_group=profile_data.blood_group,
        allergies=encryptor.encrypt_json(
            profile_data.allergies.split(",") if profile_data.allergies else []
        ),
        medical_conditions=encryptor.encrypt_json(
            profile_data.medical_conditions.split(",") if profile_data.medical_conditions else []
        ),
        medications=encryptor.encrypt_json(
            profile_data.medications.split(",") if profile_data.medications else []
        ),
        doctor_name=profile_data.doctor_name,
        doctor_phone=profile_data.doctor_phone,
        organ_donor=profile_data.organ_donor,
        notes=profile_data.notes
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

# =====================================================
# GET MY PROFILE
# =====================================================
@router.get("", response_model=EmergencyProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(404, "Profile not found")

    return profile

# =====================================================
# UPDATE PROFILE
# =====================================================
@router.put("", response_model=EmergencyProfileResponse)
def update_profile(
    data: EmergencyProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(404, "Profile not found")

    updates = data.model_dump(exclude_unset=True)

    if "allergies" in updates:
        updates["allergies"] = encryptor.encrypt_json(
            updates["allergies"].split(",")
        )

    if "medical_conditions" in updates:
        updates["medical_conditions"] = encryptor.encrypt_json(
            updates["medical_conditions"].split(",")
        )

    if "medications" in updates:
        updates["medications"] = encryptor.encrypt_json(
            updates["medications"].split(",")
        )

    for k, v in updates.items():
        setattr(profile, k, v)

    db.commit()
    db.refresh(profile)
    return profile

# =====================================================
# DELETE PROFILE
# =====================================================
@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(404, "Profile not found")

    db.delete(profile)
    db.commit()
    return None

# =====================================================
# QR CODE GENERATION
# =====================================================
@router.get("/qr-code", response_model=QRCodeResponse)
def generate_qr(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(404, "Profile not found")

    public_url = f"{settings.FRONTEND_URL}/emergency/{profile.public_id}"
    qr_base64, _ = generate_qr_code(public_url)

    return {
        "qr_code_base64": qr_base64,
        "public_url": public_url,
        "public_id": profile.public_id
    }

# =====================================================
# ADD EMERGENCY CONTACT
# =====================================================
@router.post(
    "/contacts",
    response_model=EmergencyContactResponse,
    status_code=status.HTTP_201_CREATED
)
def add_contact(
    contact: EmergencyContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exists = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == current_user.id,
        EmergencyContact.phone == contact.phone
    ).first()

    if exists:
        raise HTTPException(400, "Contact already exists")

    new_contact = EmergencyContact(
        user_id=current_user.id,
        **contact.model_dump()
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

# =====================================================
# GET CONTACTS
# =====================================================
@router.get(
    "/contacts",
    response_model=List[EmergencyContactResponse]
)
def get_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(EmergencyContact).filter(
        EmergencyContact.user_id == current_user.id
    ).order_by(EmergencyContact.priority).all()

# =====================================================
# DELETE CONTACT
# =====================================================
@router.delete(
    "/contacts/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_contact(
    contact_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contact = db.query(EmergencyContact).filter(
        EmergencyContact.id == contact_id,
        EmergencyContact.user_id == current_user.id
    ).first()

    if not contact:
        raise HTTPException(404, "Contact not found")

    db.delete(contact)
    db.commit()
    return None
