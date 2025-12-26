# 🚨 Emergency Info Card System

**A life-saving system that provides instant access to critical medical information during emergencies**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **Emergency Info Card System** is a comprehensive solution designed to save lives by making critical medical information instantly accessible during accidents or medical emergencies. When every second counts, this system ensures that first responders, paramedics, and medical professionals can quickly access vital information about an unconscious or incapacitated person.

### Problem Statement

In medical emergencies:
- Patients are often unconscious or unable to communicate
- Critical information (blood type, allergies, medications) is locked in phones
- Family contacts are inaccessible
- Valuable time is wasted gathering basic medical history

### Solution

This system provides:
- **Digital emergency profile** stored securely in the cloud
- **QR code on lock screen** for instant access without unlocking the phone
- **Physical emergency card** that can be printed and carried in wallets
- **One-tap emergency contacts** for immediate communication
- **Privacy-controlled information** - you decide what to share

---

## ✨ Features

### Core Features

✅ **User Authentication**
- Secure registration and login system
- JWT-based authentication
- Password hashing with bcrypt

✅ **Emergency Profile Management**
- Store blood group, allergies, medical conditions, medications
- Doctor information and emergency notes
- Organ donor status
- Privacy controls for each field

✅ **QR Code Generation**
- Unique QR code for each user
- Can be set as phone lock screen wallpaper
- Links to public emergency page

✅ **Public Emergency Page**
- No authentication required for emergency access
- Beautiful, mobile-responsive design
- One-tap call buttons for emergency contacts
- Access logging for security

✅ **Emergency Contacts**
- Multiple emergency contacts with priority levels
- Store name, relation, phone, email
- Automatically displayed on emergency page

✅ **Physical Card Generation**
- PDF generation for wallet-sized cards
- Full-page printable format
- QR code + basic info on card

✅ **Data Security**
- Medical information encrypted in database
- Secure JWT tokens
- Privacy settings per field

✅ **Access Logging**
- Track when emergency card is accessed
- IP address and timestamp logging
- User can review access history

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database (easily switchable to PostgreSQL)
- **Pydantic** - Data validation using Python type annotations

### Security
- **python-jose** - JWT token creation and verification
- **passlib** - Password hashing
- **cryptography** - Data encryption (Fernet)

### Utilities
- **qrcode** - QR code generation
- **Pillow** - Image processing
- **ReportLab** - PDF generation
- **python-dotenv** - Environment variable management

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Extract the ZIP file**
   ```bash
   unzip emergency-info-card.zip
   cd emergency-info-card
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example .env file
   cp .env.example .env

   # Edit .env with your configuration
   # On Windows: notepad .env
   # On macOS/Linux: nano .env
   ```

---

## ⚙️ Configuration

Edit the `.env` file with your configuration:

```env
# Database Configuration
DATABASE_URL=sqlite:///./emergency_card.db

# Security Keys (IMPORTANT: Change these in production!)
SECRET_KEY=your-super-secret-key-change-this-in-production
ENCRYPTION_KEY=your-encryption-key-change-this-in-production

# Application Settings
APP_NAME=Emergency Info Card System
APP_VERSION=1.0.0
DEBUG=True

# JWT Configuration
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

### Important Security Notes

⚠️ **For Production:**
- Generate strong random keys for `SECRET_KEY` and `ENCRYPTION_KEY`
- Use PostgreSQL instead of SQLite
- Set `DEBUG=False`
- Configure proper CORS origins
- Use HTTPS

To generate secure random keys:
```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## 🚀 Running the Application

### Development Mode

```bash
# Make sure you're in the project directory and virtual environment is activated

# Run the application
python main.py
```

The API will be available at:
- **Main App**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn (Linux/macOS)

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📚 API Documentation

### Authentication Endpoints

#### Register New User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "phone": "+1234567890"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=SecurePass123!
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer {token}
```

### Emergency Profile Endpoints

#### Create Emergency Profile
```http
POST /profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "full_name": "John Doe",
  "age": 30,
  "blood_group": "O+",
  "allergies": "Penicillin, Peanuts",
  "medical_conditions": "Diabetes Type 2, Hypertension",
  "medications": "Metformin 500mg, Lisinopril 10mg",
  "doctor_name": "Dr. Jane Smith",
  "doctor_phone": "+1234567890",
  "organ_donor": true,
  "notes": "Wears contact lenses"
}
```

#### Get My Profile
```http
GET /profile
Authorization: Bearer {token}
```

#### Update Profile
```http
PUT /profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "blood_group": "AB+",
  "show_allergies": true,
  "show_medications": false
}
```

#### Generate QR Code
```http
GET /profile/qr-code
Authorization: Bearer {token}
```

Response:
```json
{
  "qr_code_base64": "iVBORw0KGgoAAAANS...",
  "public_url": "http://localhost:8000/emergency/abc123",
  "public_id": "abc123"
}
```

### Emergency Contact Endpoints

#### Add Emergency Contact
```http
POST /profile/contacts
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Jane Doe",
  "relation": "Spouse",
  "phone": "+1234567890",
  "email": "jane@example.com",
  "priority": 1
}
```

#### Get All Contacts
```http
GET /profile/contacts
Authorization: Bearer {token}
```

#### Delete Contact
```http
DELETE /profile/contacts/{contact_id}
Authorization: Bearer {token}
```

### Public Emergency Access (No Authentication)

#### Get Emergency Card (JSON)
```http
GET /emergency/{public_id}
```

#### View Emergency Card (HTML)
```http
GET /emergency/{public_id}/view
```

#### Download Emergency Card PDF
```http
GET /emergency/{public_id}/pdf
```

---

## 💡 Usage Examples

### Complete Workflow Example

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Register a new user
register_data = {
    "email": "john@example.com",
    "username": "johndoe",
    "password": "SecurePass123!",
    "full_name": "John Doe",
    "phone": "+1234567890"
}
response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
print("User registered:", response.json())

# 2. Login
login_data = {
    "username": "john@example.com",
    "password": "SecurePass123!"
}
response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 3. Create emergency profile
profile_data = {
    "full_name": "John Doe",
    "age": 30,
    "blood_group": "O+",
    "allergies": "Penicillin, Peanuts",
    "medical_conditions": "Diabetes Type 2",
    "medications": "Metformin 500mg",
    "organ_donor": True
}
response = requests.post(f"{BASE_URL}/profile", json=profile_data, headers=headers)
print("Profile created:", response.json())

# 4. Add emergency contact
contact_data = {
    "name": "Jane Doe",
    "relation": "Spouse",
    "phone": "+1234567890",
    "priority": 1
}
response = requests.post(f"{BASE_URL}/profile/contacts", json=contact_data, headers=headers)
print("Contact added:", response.json())

# 5. Generate QR code
response = requests.get(f"{BASE_URL}/profile/qr-code", headers=headers)
qr_data = response.json()
print("QR Code URL:", qr_data["public_url"])

# 6. Access emergency card (public - no authentication)
public_id = qr_data["public_id"]
response = requests.get(f"{BASE_URL}/emergency/{public_id}")
print("Emergency card data:", response.json())
```

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user","password":"pass123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -d "username=user@example.com&password=pass123"

# Get profile (replace TOKEN with your actual token)
curl -X GET http://localhost:8000/profile \
  -H "Authorization: Bearer TOKEN"

# Access public emergency card
curl -X GET http://localhost:8000/emergency/abc123
```

---

## 📁 Project Structure

```
emergency-info-card/
│
├── backend/                    # Backend application
│   ├── api/                    # API endpoints
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── profile.py         # Emergency profile endpoints
│   │   └── public.py          # Public emergency access
│   │
│   ├── models/                 # Database models
│   │   ├── __init__.py        # Database connection
│   │   ├── database.py        # SQLAlchemy models
│   │   └── schemas.py         # Pydantic schemas
│   │
│   ├── services/               # Business logic (future)
│   │
│   ├── utils/                  # Utility functions
│   │   ├── security.py        # Password hashing, JWT, encryption
│   │   ├── qr_generator.py    # QR code generation
│   │   └── pdf_generator.py   # PDF creation
│   │
│   ├── templates/              # HTML templates (future)
│   ├── static/                 # Static files (CSS, JS, images)
│   └── config.py              # Configuration settings
│
├── frontend/                   # Frontend (future mobile app)
├── tests/                      # Unit and integration tests (future)
├── docs/                       # Documentation
│
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

---

## 🔒 Security

### Data Protection

1. **Password Hashing**
   - Passwords are hashed using bcrypt
   - Never stored in plain text

2. **Data Encryption**
   - Sensitive medical data encrypted using Fernet (symmetric encryption)
   - Encryption key stored in environment variables

3. **JWT Authentication**
   - Secure token-based authentication
   - Token expiration after configurable time

4. **Privacy Controls**
   - Users control visibility of each field
   - Public emergency page respects privacy settings

5. **Access Logging**
   - All emergency card accesses are logged
   - IP address and timestamp recorded

### Best Practices

- Use strong passwords (minimum 8 characters)
- Change default SECRET_KEY and ENCRYPTION_KEY
- Use HTTPS in production
- Regularly update dependencies
- Review access logs periodically
- Set appropriate CORS origins

---

## 🧪 Testing

### Manual Testing Using API Docs

1. Start the application
2. Open http://localhost:8000/docs
3. Use the interactive Swagger UI to test endpoints

### Test Scenarios

1. **User Registration & Login**
   - Register a new user
   - Login with credentials
   - Get current user info

2. **Profile Management**
   - Create emergency profile
   - Update profile with medical info
   - Add emergency contacts
   - Generate QR code

3. **Public Access**
   - Access emergency card via public URL
   - View HTML emergency page
   - Download PDF card

4. **Privacy Controls**
   - Update privacy settings
   - Verify public page respects settings

---

## 🎨 Customization

### Changing Colors/Styles

Edit the inline CSS in:
- `backend/api/public.py` (for emergency card HTML)
- `main.py` (for landing page)

### Adding Features

1. **Email Notifications**
   - Uncomment email configuration in `.env`
   - Implement email service in `backend/services/email_service.py`

2. **SMS Alerts**
   - Add Twilio credentials to `.env`
   - Implement SMS service using Twilio API

3. **Live Location Sharing**
   - Add geolocation endpoint
   - Implement SOS button functionality

---

## 🚢 Deployment

### Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create new app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ENCRYPTION_KEY=your-encryption-key

# Deploy
git push heroku main
```

### Deploy to Railway

1. Push code to GitHub
2. Connect Railway to GitHub repo
3. Set environment variables in Railway dashboard
4. Deploy automatically

### Deploy to AWS/DigitalOcean

Use Docker:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📖 Documentation

- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Nithin**
- Final Year B.Tech CSE Student
- Project: Emergency Info Card System

---

## 🙏 Acknowledgments

- FastAPI team for the excellent framework
- SQLAlchemy for the robust ORM
- All open-source contributors

---

## 📞 Support

For support or questions:
- Open an issue on GitHub
- Contact: [Your Email]

---

## 🎯 Future Enhancements

- [ ] Mobile app (Flutter/React Native)
- [ ] Multi-language support
- [ ] Voice assistant integration
- [ ] Wearable device support
- [ ] Hospital integration API
- [ ] Medical document uploads
- [ ] Allergy scanner (barcode)
- [ ] Medication reminder
- [ ] Family sharing features

---

**⚡ Remember: This system could save your life or someone else's. Share it with your loved ones! ⚡**
