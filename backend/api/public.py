# -*- coding: utf-8 -*-
"""
Public Emergency Card API - No authentication required
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from sqlalchemy.orm import Session

from backend.models.database import (
    get_db,
    EmergencyProfile,
    EmergencyContact,
    AccessLog
)
from backend.models.schemas import PublicEmergencyCard
from backend.utils.security import encryptor
from backend.utils.pdf_generator import generate_full_page_card
from backend.config import settings

router = APIRouter(tags=["Public Emergency Access"])

# -----------------------------------------------------
# Helper: Log access
# -----------------------------------------------------
def log_access(public_id: str, request: Request, db: Session):
    try:
        profile = db.query(EmergencyProfile).filter(
            EmergencyProfile.public_id == public_id
        ).first()

        if profile:
            access_log = AccessLog(
                user_id=profile.user_id,
                ip_address=request.client.host if request.client else "unknown",
                user_agent=request.headers.get("user-agent", "unknown")
            )
            db.add(access_log)
            db.commit()
    except Exception as e:
        print(f"Access log error: {e}")

# =====================================================
# 🔁 PUBLIC ENTRY (QR ALWAYS HITS THIS)
# =====================================================
@router.get("/emergency/{public_id}")
def redirect_to_emergency_view(public_id: str):
    return RedirectResponse(
        url=f"/emergency/{public_id}/view",
        status_code=302
    )

# =====================================================
# 🧠 JSON API (PROGRAMMATIC USE)
# =====================================================
@router.get("/api/emergency/{public_id}", response_model=PublicEmergencyCard)
def get_public_emergency_card_json(
    public_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.public_id == public_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Emergency card not found"
        )

    log_access(public_id, request, db)

    contacts = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == profile.user_id
    ).order_by(EmergencyContact.priority).all()

    return {
        "full_name": profile.full_name if profile.show_name else None,
        "age": profile.age if profile.show_age else None,
        "blood_group": profile.blood_group if profile.show_blood_group else None,
        "allergies": encryptor.decrypt_json(profile.allergies)
        if profile.show_allergies else None,
        "medical_conditions": encryptor.decrypt_json(profile.medical_conditions)
        if profile.show_conditions else None,
        "medications": encryptor.decrypt_json(profile.medications)
        if profile.show_medications else None,
        "organ_donor": profile.organ_donor,
        "emergency_contacts": [
            {
                "name": c.name,
                "relation": c.relation,
                "phone": c.phone,
                "priority": c.priority
            } for c in contacts
        ]
    }

# =====================================================
# 🖥️ UI VIEW (MOBILE + FIRST RESPONDER FRIENDLY)
# =====================================================
@router.get("/emergency/{public_id}/view", response_class=HTMLResponse)
def view_emergency_card_html(
    public_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.public_id == public_id
    ).first()

    if not profile:
        return HTMLResponse(
            "<h1>Emergency Card Not Found</h1>",
            status_code=404
        )

    log_access(public_id, request, db)

    contacts = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == profile.user_id
    ).order_by(EmergencyContact.priority).all()

    allergies = encryptor.decrypt_json(profile.allergies) if profile.show_allergies else []
    conditions = encryptor.decrypt_json(profile.medical_conditions) if profile.show_conditions else []
    medications = encryptor.decrypt_json(profile.medications) if profile.show_medications else []

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Emergency Medical Card</title>

<style>
body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.card {{
    background: #fff;
    width: 100%;
    max-width: 420px;
    border-radius: 22px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.35);
    overflow: hidden;
}}

.header {{
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
    color: white;
    text-align: center;
    padding: 25px;
}}

.header h1 {{
    font-size: 22px;
}}

.content {{
    padding: 22px;
}}

.section {{
    margin-bottom: 18px;
}}

.section-title {{
    font-weight: 700;
    margin-bottom: 8px;
}}

.info {{
    background: #f7f9fc;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 6px;
}}

.blood {{
    background: #e63946;
    color: white;
    font-size: 26px;
    font-weight: bold;
    padding: 8px 22px;
    border-radius: 30px;
    display: inline-block;
}}

.contact {{
    background: #e8f5e9;
    padding: 12px;
    border-radius: 10px;
    border-left: 5px solid #28a745;
    margin-bottom: 10px;
}}

.call {{
    display: block;
    margin-top: 8px;
    background: #28a745;
    color: white;
    padding: 10px;
    text-align: center;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
}}

.footer {{
    text-align: center;
    font-size: 12px;
    color: #777;
    padding: 12px;
    background: #fafafa;
}}
</style>
</head>

<body>
<div class="card">
    <div class="header">
        <h1>EMERGENCY MEDICAL INFO</h1>
        <p>For first responders</p>
    </div>

    <div class="content">

        <div class="section">
            <div class="section-title">Personal Details</div>
            <div class="info">Name: {profile.full_name}</div>
            <div class="info">Age: {profile.age}</div>
        </div>

        <div class="section">
            <div class="section-title">Blood Group</div>
            <div style="text-align:center;">
                <span class="blood">{profile.blood_group}</span>
            </div>
        </div>

        <div class="section">
            <div class="section-title">Allergies</div>
            <div>{", ".join(allergies) if allergies else "None"}</div>
        </div>

        <div class="section">
            <div class="section-title">Medical Conditions</div>
            <div>{", ".join(conditions) if conditions else "None"}</div>
        </div>

        <div class="section">
            <div class="section-title">Medications</div>
            <div>{", ".join(medications) if medications else "None"}</div>
        </div>

        <div class="section">
            <div class="section-title">Emergency Contacts</div>
            {"".join([f"<div class='contact'><b>{c.name}</b> ({c.relation})<a class='call' href='tel:{c.phone}'>Call {c.phone}</a></div>" for c in contacts])}
        </div>

    </div>

    <div class="footer">
        Emergency Info Card • Powered by QR Access
    </div>
</div>
</body>
</html>
"""
    return HTMLResponse(content=html_content)

# =====================================================
# 📄 PDF DOWNLOAD (PROD URL FIX)
# =====================================================
@router.get("/emergency/{public_id}/pdf")
def download_emergency_card_pdf(
    public_id: str,
    db: Session = Depends(get_db)
):
    profile = db.query(EmergencyProfile).filter(
        EmergencyProfile.public_id == public_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Emergency card not found"
        )

    primary_contact = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == profile.user_id,
        EmergencyContact.priority == 1
    ).first()

    user_data = {
        "name": profile.full_name,
        "blood_group": profile.blood_group,
        "age": profile.age,
        "emergency_contact": {
            "name": primary_contact.name if primary_contact else "N/A",
            "phone": primary_contact.phone if primary_contact else "N/A"
        }
    }

    # ✅ IMPORTANT: Render URL (NOT localhost)
    qr_url = f"{settings.FRONTEND_URL}/emergency/{public_id}"

    pdf_bytes = generate_full_page_card(user_data, qr_url)

    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    return FileResponse(
        tmp_path,
        filename=f"emergency_card_{public_id}.pdf",
        media_type="application/pdf"
    )
