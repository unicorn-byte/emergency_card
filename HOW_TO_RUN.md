# 🚀 How to Run the Emergency Info Card System

## Quick Start (3 Simple Steps!)

### For Windows Users:

1. **Extract the ZIP file** to a folder (e.g., `C:\Projects\emergency-info-card`)

2. **Double-click `run.bat`** in the project folder
   - This will automatically:
     - Create a virtual environment
     - Install all dependencies
     - Start the server

3. **Open your browser** and go to:
   - http://localhost:8000 (Main page)
   - http://localhost:8000/docs (API Documentation)

That's it! 🎉

---

### For Mac/Linux Users:

1. **Extract the ZIP file** to a folder

2. **Open Terminal** in the project folder and run:
   ```bash
   ./run.sh
   ```
   Or:
   ```bash
   bash run.sh
   ```

3. **Open your browser** and go to:
   - http://localhost:8000 (Main page)
   - http://localhost:8000/docs (API Documentation)

---

## Manual Installation (If Automated Script Doesn't Work)

### Step 1: Install Python

**Check if Python is installed:**
```bash
python --version
# or
python3 --version
```

You need Python 3.9 or higher.

**If Python is not installed:**
- **Windows**: Download from https://www.python.org/downloads/
  - ⚠️ Important: Check "Add Python to PATH" during installation!
- **Mac**: Use Homebrew: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip` (Ubuntu/Debian)

---

### Step 2: Set Up Virtual Environment

**Windows:**
```cmd
cd emergency-info-card
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
cd emergency-info-card
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI
- Uvicorn
- SQLAlchemy
- And all other required packages

Wait for installation to complete (may take 2-3 minutes).

---

### Step 4: Configure Environment (Optional)

The project comes with a `.env` file with default settings. You can use it as-is for development.

**To customize:**
```bash
# Open .env file in any text editor
notepad .env      # Windows
nano .env         # Mac/Linux
```

**Important settings:**
- `DATABASE_URL`: Database connection (default: SQLite)
- `SECRET_KEY`: Change this in production!
- `ENCRYPTION_KEY`: Change this in production!

---

### Step 5: Run the Application

```bash
python main.py
```

You should see:
```
✅ Database initialized successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Testing the Installation

### Method 1: Use the Test Script

In a **new terminal** (keep the server running):

**Activate venv first:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**Run test script:**
```bash
python test_api.py
```

This will test all endpoints and show you if everything is working!

---

### Method 2: Manual Testing

1. **Open browser**: http://localhost:8000
   - You should see a beautiful landing page

2. **Open API Docs**: http://localhost:8000/docs
   - Interactive API documentation

3. **Test registration**:
   - Click on `POST /auth/register`
   - Click "Try it out"
   - Fill in the form and click "Execute"

---

## Common Issues & Solutions

### Issue 1: "Python is not recognized"

**Solution:**
- Windows: Reinstall Python and check "Add Python to PATH"
- Verify installation: `python --version`

---

### Issue 2: "Port 8000 is already in use"

**Solution:**

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Mac/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

Or change the port in `main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8080)  # Changed to 8080
```

---

### Issue 3: "pip: command not found"

**Solution:**
```bash
# Try pip3 instead
pip3 install -r requirements.txt

# Or use python -m pip
python -m pip install -r requirements.txt
```

---

### Issue 4: "ModuleNotFoundError"

**Solution:**
Make sure virtual environment is activated:
```bash
# You should see (venv) in your terminal
# If not, activate it:

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

---

### Issue 5: Virtual environment won't activate (Windows)

**Solution:**
Enable script execution:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
venv\Scripts\activate
```

---

## Project Structure Quick Reference

```
emergency-info-card/
│
├── main.py                 ← START HERE (Run this file)
├── requirements.txt        ← Dependencies
├── .env                    ← Configuration
├── run.bat                 ← Windows auto-run script
├── run.sh                  ← Mac/Linux auto-run script
├── test_api.py            ← Test script
│
├── backend/
│   ├── api/               ← API endpoints
│   ├── models/            ← Database models
│   ├── utils/             ← Utilities
│   └── config.py          ← Settings
│
├── README.md              ← Full documentation
├── QUICKSTART.md          ← Quick guide
└── docs/
    └── PRESENTATION_GUIDE.md  ← Project presentation guide
```

---

## What to Do After Installation

### 1. Explore the API Documentation
Visit: http://localhost:8000/docs

This interactive documentation lets you:
- See all available endpoints
- Test each endpoint directly from browser
- View request/response schemas

### 2. Create Your First User
Use the API docs to:
1. Register a user (POST /auth/register)
2. Login (POST /auth/login)
3. Create emergency profile (POST /profile)
4. Add emergency contact (POST /profile/contacts)
5. Generate QR code (GET /profile/qr-code)

### 3. Test the Emergency Card
- Get your public URL from the QR code endpoint
- Open it in a browser to see your emergency card
- Try it on your phone!

### 4. Download the PDF Card
- Add `/pdf` to your emergency URL
- Print it and keep in your wallet

---

## Development Tips

### Run with Auto-Reload (Development Mode)

The application already runs in development mode with auto-reload enabled. Any changes you make to the code will automatically restart the server.

### View Logs

All logs appear in the terminal where you ran the server.

### Reset Database

If you want to start fresh:
```bash
# Stop the server (Ctrl+C)
# Delete the database file
rm emergency_card.db         # Mac/Linux
del emergency_card.db        # Windows

# Restart the server
python main.py
```

The database will be recreated automatically.

### Change Database to PostgreSQL

Edit `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost/emergency_card
```

Install PostgreSQL driver:
```bash
pip install psycopg2-binary
```

---

## Deployment Guide (After Development)

### Deploy to Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set SECRET_KEY=your-new-secret-key
heroku config:set ENCRYPTION_KEY=your-new-encryption-key

# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### Deploy to Railway

1. Push to GitHub
2. Connect Railway to your repo
3. Set environment variables in Railway dashboard
4. Deploy automatically

---

## Getting Help

### Check These First:
1. README.md - Complete documentation
2. QUICKSTART.md - Beginner guide
3. http://localhost:8000/docs - API documentation

### Still Stuck?
- Check if server is running (terminal should show logs)
- Verify virtual environment is activated `(venv)`
- Try deleting `venv` folder and reinstalling
- Make sure Python 3.9+ is installed

---

## Next Steps

Once everything is running:

1. **Read the QUICKSTART.md** for a 5-minute tutorial
2. **Check PRESENTATION_GUIDE.md** for your project presentation
3. **Explore the API** at http://localhost:8000/docs
4. **Customize the code** to add your own features
5. **Deploy to production** using the deployment guide

---

## Important Notes

⚠️ **For Development Only:**
The included `.env` file has development keys. These are NOT secure for production use.

✅ **Before Production:**
1. Generate new SECRET_KEY and ENCRYPTION_KEY
2. Use PostgreSQL instead of SQLite
3. Set DEBUG=False
4. Use HTTPS
5. Configure proper CORS

---

**You're all set! Have fun building with the Emergency Info Card System! 🚨**

If you encounter any issues, don't hesitate to review the README.md or check the code comments for guidance.
