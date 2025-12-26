# 🚀 Quick Start Guide

## Get Up and Running in 5 Minutes!

### Step 1: Setup Environment

```bash
# Extract the project
unzip emergency-info-card.zip
cd emergency-info-card

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure

```bash
# Copy environment file
cp .env.example .env

# Edit .env if needed (optional for quick start)
# Default settings work fine for development
```

### Step 3: Run the Application

```bash
# Start the server
python main.py
```

You should see:
```
✅ Database initialized successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Test the API

Open your browser and go to:
- **Landing Page**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Step 5: Create Your First Emergency Card

#### Using the Interactive API Docs:

1. Go to http://localhost:8000/docs
2. Click on **POST /auth/register**
3. Click "Try it out"
4. Fill in the form:
   ```json
   {
     "email": "test@example.com",
     "username": "testuser",
     "password": "Test123!",
     "full_name": "Test User",
     "phone": "+1234567890"
   }
   ```
5. Click "Execute"

6. Now **POST /auth/login** to get your token:
   - username: `test@example.com`
   - password: `Test123!`
   - Copy the `access_token` from the response

7. Click the **Authorize** button at the top
   - Paste your token
   - Click "Authorize"

8. Create your emergency profile using **POST /profile**:
   ```json
   {
     "full_name": "Test User",
     "age": 30,
     "blood_group": "O+",
     "allergies": "Penicillin, Peanuts",
     "medical_conditions": "None",
     "medications": "None",
     "organ_donor": false
   }
   ```

9. Add emergency contact using **POST /profile/contacts**:
   ```json
   {
     "name": "Jane Doe",
     "relation": "Spouse",
     "phone": "+1234567890",
     "priority": 1
   }
   ```

10. Generate QR code using **GET /profile/qr-code**
    - Copy the `public_url` from the response

11. Open the public URL in a new browser tab to see your emergency card!

### Step 6: View Your Emergency Card

Visit the URL you got from step 10 (it will look like):
```
http://localhost:8000/emergency/abc12345
```

You should see a beautiful emergency card with:
- Your name and age
- Blood group
- Allergies and medical conditions
- Emergency contact with call button

### Step 7: Download PDF Card

Add `/pdf` to your emergency URL:
```
http://localhost:8000/emergency/abc12345/pdf
```

This will download a printable PDF card!

---

## 🎉 Congratulations!

You now have a fully functional Emergency Info Card System!

### What's Next?

- **Customize your profile** with more details
- **Add multiple emergency contacts** with different priorities
- **Set the QR code as your phone wallpaper** for lock screen access
- **Print the PDF card** and keep it in your wallet
- **Share with family and friends** - it could save lives!

### Need Help?

- Check the full **README.md** for detailed documentation
- Visit http://localhost:8000/docs for interactive API testing
- Review the code in the `backend/` directory

---

## 📱 Mobile App Setup (Optional)

The current version is a backend API. To use it on mobile:

**Option 1: Use Browser**
- Set QR code as lock screen wallpaper
- QR leads to mobile-responsive web page

**Option 2: Build Flutter App** (future)
- A mobile app can be built using Flutter
- Connect to this backend API

---

## 🛑 Troubleshooting

### Port Already in Use
```bash
# Kill the process using port 8000
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Module Not Found Error
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Database Error
```bash
# Delete the database and restart
rm emergency_card.db
python main.py
```

---

## 🎯 Quick API Testing with cURL

### Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"test","password":"Test123!","full_name":"Test User"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -d "username=test@example.com&password=Test123!"
```

### Create Profile (replace TOKEN)
```bash
curl -X POST http://localhost:8000/profile \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"blood_group":"O+","age":30}'
```

---

**Happy Building! 🚀**
