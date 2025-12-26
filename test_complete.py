import requests
import qrcode
import os

BASE_URL = "http://localhost:8000"

EMAIL = "testuser2024@gmail.com"
PASSWORD = "Test@123456"

print("🚀 Testing Emergency Info Card System\n")

# Step 1: Login
print("1️⃣ Logging in...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={
        "username": EMAIL,
        "password": PASSWORD
    }
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print("✅ Login successful!\n")
else:
    print("❌ Login failed")
    exit()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Step 2: Get user
print("2️⃣ Getting user info...")
user = requests.get(f"{BASE_URL}/auth/me", headers=headers).json()
print(f"✅ User: {user['full_name']} ({user['email']})\n")

# Step 3: Create emergency profile
print("3️⃣ Creating emergency profile...")
profile_response = requests.post(
    f"{BASE_URL}/profile",
    headers=headers,
    json={
        "full_name": "Test User",
        "age": 25,
        "blood_group": "O+",
        "allergies": "Penicillin, Peanuts",
        "medical_conditions": "None",
        "medications": "None",
        "doctor_name": "Dr. Smith",
        "doctor_phone": "+919876543210",
        "organ_donor": False,
        "notes": "Test profile"
    }
)

print("✅ Emergency profile ready!\n")

# Step 4: Add contact
print("4️⃣ Adding emergency contact...")
requests.post(
    f"{BASE_URL}/profile/contacts",
    headers=headers,
    json={
        "name": "Emergency Contact",
        "relation": "Family",
        "phone": "+919876543210",
        "email": "contact@example.com",
        "priority": 1
    }
)
print("✅ Emergency contact added!\n")

# Step 5: Generate QR (public URL)
print("5️⃣ Generating QR code...")
qr_response = requests.get(f"{BASE_URL}/profile/qr-code", headers=headers)

qr_data = qr_response.json()
public_url = qr_data["public_url"]
public_id = qr_data["public_id"]

print("✅ QR Code generated!")
print(f"🔗 Public URL: {public_url}\n")

# Step 6: Test public card
print("6️⃣ Testing public emergency card...")
test = requests.get(f"{public_url}/view")
if test.status_code == 200:
    print("✅ Emergency card accessible!\n")

# ==============================
# ⭐ STEP 7: GENERATE QR IMAGE ⭐
# ==============================

print("7️⃣ Creating QR image...")

qr_url = f"{public_url}/view"   # 👈 IMPORTANT
qr = qrcode.make(qr_url)

os.makedirs("qr_codes", exist_ok=True)
file_path = f"qr_codes/emergency_qr_{public_id}.png"
qr.save(file_path)

print("🎉 QR IMAGE CREATED SUCCESSFULLY!")
print("📸 Scan this QR → it will open the emergency card UI")
print(f"🔗 QR points to: {qr_url}\n")

