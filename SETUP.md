# 🚀 Quick Setup Guide - CTF Integrity System

## Prerequisites
- Python 3.8+
- pip package manager
- Modern web browser

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python db_setup.py
```

This creates the database with 5 sample challenges:
- Web Exploitation (Medium, 70 points)
- Password Cracking (Easy, 40 points)
- Cryptography (Hard, 90 points)
- Network Analysis (Medium, 60 points)
- OSINT Investigation (Easy, 50 points)

### 3. Run the Application
```bash
python app.py
```

Access at: `http://localhost:5000`

## Default Accounts

### Create Admin Account
1. Register normally at `/register`
2. Manually update database:
```bash
sqlite3 database.db
UPDATE users SET role='admin' WHERE username='your_username';
.quit
```

## Testing the System

### Test 1: Multi-Account Detection
1. Register 2 accounts from same browser
2. Login with both
3. Check `/dashboard` for alerts

### Test 2: Speed Detection
1. Login to an account
2. Quickly submit multiple flags (< 10 seconds apart)
3. Check dashboard for speed alerts

### Test 3: Run Detection Engine
```bash
python enhanced_detection.py
```

This will scan all activities and generate alerts.

## Project Structure
```
/home/user/webapp/
├── app.py                    # Main Flask application
├── db_setup.py              # Database initialization
├── enhanced_detection.py    # Advanced detection engine
├── ai_detect.py             # AI-based anomaly detection
├── detect.py                # Basic detection script
├── requirements.txt         # Python dependencies
├── database.db              # SQLite database
├── DOCUMENTATION.md         # Full documentation
├── templates/               # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── challenges.html
│   ├── leaderboard.html
│   ├── profile.html
│   └── admin.html
└── static/                  # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── monitoring.js
```

## Common Commands

### Start Server
```bash
python app.py
```

### Run Detection
```bash
python enhanced_detection.py
```

### Run AI Detection
```bash
python ai_detect.py
```

### View Database
```bash
sqlite3 database.db
.tables
SELECT * FROM alerts;
.quit
```

## Troubleshooting

### Issue: Port already in use
```bash
# Change port in app.py:
app.run(debug=True, port=5001)
```

### Issue: Module not found
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Database error
```bash
rm database.db
python db_setup.py
```

## Key Features to Demo

1. **User Registration & Login** - Show security notice
2. **Challenges Page** - Show monitoring alert banner
3. **Real-time Monitoring** - Open browser console to see monitoring logs
4. **Admin Dashboard** - Show alert filtering and risk levels
5. **Detection Engine** - Run and show terminal output

## Production Deployment

### Option 1: Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 2: Docker (coming soon)
```bash
docker build -t ctf-integrity .
docker run -p 5000:5000 ctf-integrity
```

## Security Notes

⚠️ **Before Production:**
- Change `app.secret_key` in `app.py`
- Enable HTTPS
- Use PostgreSQL instead of SQLite
- Add rate limiting
- Implement CAPTCHA
- Add email verification

## Support

For issues or questions, refer to `DOCUMENTATION.md`

---

**Ready to start? Run `python app.py` and visit http://localhost:5000**
