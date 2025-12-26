from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from backend.models.database import get_db, User, EmergencyProfile
from backend.api.auth import get_current_user
from backend.models.schemas import EmergencyProfileCreate, EmergencyProfileResponse
from backend.utils.security import encryptor
from backend.utils.qr_generator import generate_qr_code
from backend.config import settings

router = APIRouter(prefix="/profile", tags=["Emergency Profile"])


@router.post("", response_model=EmergencyProfileResponse)
def create_profile(
    data: EmergencyProfileCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    public_id = str(uuid.uuid4())[:8]

    profile = EmergencyProfile(
        user_id=user.id,
        public_id=public_id,
        full_name=data.full_name,
        age=data.age,
        blood_group=data.blood_group,
        allergies=encryptor.encrypt_json(data.allergies or []),
        medical_conditions=encryptor.encrypt_json(data.medical_conditions or []),
        medications=encryptor.encrypt_json(data.medications or [])
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/qr-code")
def get_qr(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(EmergencyProfile).filter_by(user_id=user.id).first()

    url = f"{settings.FRONTEND_URL}/emergency/{profile.public_id}"
    qr, _ = generate_qr_code(url)

    return {"qr_code_base64": qr, "public_url": url}
