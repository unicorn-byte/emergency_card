"""
Simple test script to verify the Emergency Info Card System is working
Run this after starting the server to test all endpoints
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def test_health():
    """Test health check endpoint"""
    print_section("1. Testing Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success("Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Could not connect to server: {e}")
        print("   Make sure the server is running: python main.py")
        return False

def test_registration():
    """Test user registration"""
    print_section("2. Testing User Registration")
    user_data = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "full_name": "Test User",
        "phone": "+1234567890"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code in [201, 400]:  # 400 if user already exists
            if response.status_code == 201:
                print_success("User registered successfully")
            else:
                print_success("User already exists (continuing with tests)")
            print(f"   Email: {user_data['email']}")
            return True
        else:
            print_error(f"Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Registration error: {e}")
        return False

def test_login():
    """Test user login and return token"""
    print_section("3. Testing User Login")
    login_data = {
        "username": "testuser@example.com",
        "password": "TestPass123!"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print_success("Login successful")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print_error(f"Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Login error: {e}")
        return None

def test_get_user(token):
    """Test getting current user info"""
    print_section("4. Testing Get Current User")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print_success("Retrieved user information")
            print(f"   Username: {user_data['username']}")
            print(f"   Email: {user_data['email']}")
            return True
        else:
            print_error(f"Get user failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get user error: {e}")
        return False

def test_create_profile(token):
    """Test creating emergency profile"""
    print_section("5. Testing Emergency Profile Creation")
    profile_data = {
        "full_name": "Test User",
        "age": 30,
        "blood_group": "O+",
        "allergies": "Penicillin, Peanuts",
        "medical_conditions": "None",
        "medications": "None",
        "doctor_name": "Dr. Smith",
        "doctor_phone": "+1234567890",
        "organ_donor": True,
        "notes": "Test profile"
    }
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{BASE_URL}/profile", json=profile_data, headers=headers)
        if response.status_code in [201, 400]:  # 400 if profile exists
            if response.status_code == 201:
                print_success("Emergency profile created")
            else:
                print_success("Profile already exists (continuing)")
            return True
        else:
            print_error(f"Profile creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Profile creation error: {e}")
        return False

def test_add_contact(token):
    """Test adding emergency contact"""
    print_section("6. Testing Emergency Contact Addition")
    contact_data = {
        "name": "Jane Doe",
        "relation": "Spouse",
        "phone": "+1234567890",
        "email": "jane@example.com",
        "priority": 1
    }
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{BASE_URL}/profile/contacts", json=contact_data, headers=headers)
        if response.status_code in [201, 400]:
            print_success("Emergency contact added")
            return True
        else:
            print_error(f"Contact addition failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Contact addition error: {e}")
        return False

def test_qr_code(token):
    """Test QR code generation"""
    print_section("7. Testing QR Code Generation")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{BASE_URL}/profile/qr-code", headers=headers)
        if response.status_code == 200:
            qr_data = response.json()
            print_success("QR code generated")
            print(f"   Public ID: {qr_data['public_id']}")
            print(f"   Public URL: {qr_data['public_url']}")
            return qr_data['public_id']
        else:
            print_error(f"QR code generation failed: {response.status_code}")
            return None
    except Exception as e:
        print_error(f"QR code generation error: {e}")
        return None

def test_public_access(public_id):
    """Test public emergency card access"""
    print_section("8. Testing Public Emergency Card Access")
    try:
        response = requests.get(f"{BASE_URL}/emergency/{public_id}")
        if response.status_code == 200:
            card_data = response.json()
            print_success("Public emergency card accessed")
            print(f"   Name: {card_data.get('full_name', 'N/A')}")
            print(f"   Blood Group: {card_data.get('blood_group', 'N/A')}")
            print(f"   Emergency Contacts: {len(card_data.get('emergency_contacts', []))}")
            return True
        else:
            print_error(f"Public access failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Public access error: {e}")
        return False

def test_public_html(public_id):
    """Test public emergency card HTML view"""
    print_section("9. Testing Public Emergency Card HTML View")
    try:
        response = requests.get(f"{BASE_URL}/emergency/{public_id}/view")
        if response.status_code == 200:
            print_success("Public HTML page generated")
            print(f"   URL: {BASE_URL}/emergency/{public_id}/view")
            print("   Open this URL in your browser to see the emergency card!")
            return True
        else:
            print_error(f"HTML view failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"HTML view error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🚨"*30)
    print("  EMERGENCY INFO CARD SYSTEM - API TEST SUITE")
    print("🚨"*30)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Server is not running. Please start it with: python main.py")
        sys.exit(1)
    
    # Test 2: Registration
    if not test_registration():
        print("\n❌ Registration test failed")
        sys.exit(1)
    
    # Test 3: Login
    token = test_login()
    if not token:
        print("\n❌ Login test failed")
        sys.exit(1)
    
    # Test 4: Get user
    if not test_get_user(token):
        print("\n❌ Get user test failed")
        sys.exit(1)
    
    # Test 5: Create profile
    if not test_create_profile(token):
        print("\n❌ Profile creation test failed")
        sys.exit(1)
    
    # Test 6: Add contact
    if not test_add_contact(token):
        print("\n❌ Contact addition test failed")
        sys.exit(1)
    
    # Test 7: QR code
    public_id = test_qr_code(token)
    if not public_id:
        print("\n❌ QR code test failed")
        sys.exit(1)
    
    # Test 8: Public access
    if not test_public_access(public_id):
        print("\n❌ Public access test failed")
        sys.exit(1)
    
    # Test 9: HTML view
    if not test_public_html(public_id):
        print("\n❌ HTML view test failed")
        sys.exit(1)
    
    # Success summary
    print_section("✅ ALL TESTS PASSED!")
    print("\n🎉 Your Emergency Info Card System is working perfectly!")
    print("\n📱 Next Steps:")
    print(f"   1. Visit: {BASE_URL}/emergency/{public_id}/view")
    print("   2. Save the QR code as your phone wallpaper")
    print("   3. Download the PDF card for your wallet")
    print(f"   4. API Documentation: {BASE_URL}/docs")
    print("\n💡 Tip: Open the emergency card URL on your phone to see the mobile view!\n")

if __name__ == "__main__":
    main()
