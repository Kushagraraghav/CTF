# 🔐 CTF Integrity & Cheat Detection System

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Detection Algorithms](#detection-algorithms)
- [API Documentation](#api-documentation)
- [Security Features](#security-features)
- [Contributing](#contributing)

---

## 🎯 Overview

The **CTF Integrity & Cheat Detection System** is a comprehensive platform designed to ensure fairness, authenticity, and security in Capture The Flag (CTF) competitions. It monitors user activities in real-time, detects suspicious patterns, and maintains the integrity of the contest.

### Why This Project?

In many CTFs, participants may:
- Share flags between accounts
- Use multiple accounts to gain unfair advantages
- Copy writeups or solutions from others
- Exploit platform loopholes
- Use automated tools to solve challenges

Our system acts as a **"digital invigilator"** that automatically detects and flags these behaviors.

---

## ✨ Features

### 1️⃣ User Activity Monitoring
- **Real-time tracking** of login times, IP addresses, and submission timestamps
- **Device fingerprinting** for browser and device identification
- **Session monitoring** with tab-switching detection
- **Navigation behavior** analysis

### 2️⃣ Flag Submission Analysis
- **Timing analysis** for flag submissions
- **Pattern matching** to detect flag sharing
- **Burst detection** for rapid submissions
- **Difficulty progression** tracking

### 3️⃣ Multi-Account Detection
- **IP address clustering** to identify same-network users
- **Device fingerprint comparison** across accounts
- **Behavior pattern matching** between suspicious accounts
- **Submission timeline correlation**

### 4️⃣ Suspicious Behavior Detection
- **Speed anomaly detection** for impossibly fast solving
- **Automated tool detection** through behavioral analysis
- **Copy-paste monitoring** during challenge solving
- **DevTools usage tracking**

### 5️⃣ Real-Time Alerts
- **Automatic flagging** of suspicious users
- **Risk score calculation** based on multiple factors
- **Admin notifications** for critical alerts
- **Detailed activity logs** for investigation

### 6️⃣ Admin Dashboard
- **Comprehensive overview** of all alerts
- **User risk profiling** with visual indicators
- **Filtering and sorting** capabilities
- **Action buttons** for warnings and bans
- **Export functionality** for reports

---

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       v
┌─────────────────────┐
│  CTF Platform       │
│  (Flask Web App)    │
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│  Activity Logger    │
│  (monitoring.js)    │
└──────┬──────────────┘
       │
       v
┌─────────────────────────┐
│  Detection Engine       │
│  (enhanced_detection.py)│
└──────┬──────────────────┘
       │
       v
┌─────────────────────┐
│  SQLite Database    │
│  (database.db)      │
└──────┬──────────────┘
       │
       v
┌─────────────────────┐
│  Admin Dashboard    │
│  (Real-time View)   │
└─────────────────────┘
```

### Components

1. **CTF Platform** (`app.py`)
   - Flask web application serving challenges
   - User authentication and session management
   - Submission handling and scoring

2. **Activity Logger** (`static/js/monitoring.js`)
   - Client-side monitoring script
   - Browser fingerprinting
   - Event tracking (tab switches, copy-paste, etc.)

3. **Detection Engine** (`enhanced_detection.py`)
   - Advanced pattern matching algorithms
   - Behavioral analysis
   - Risk score calculation

4. **Database** (`database.db`)
   - SQLite database storing users, challenges, submissions, and alerts
   - Efficient querying for real-time analysis

5. **Admin Dashboard** (`templates/admin.html`)
   - Visual interface for monitoring
   - Alert management
   - User action controls

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Modern web browser

### Step 1: Clone the Repository
```bash
cd /home/user/webapp
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
python db_setup.py
```

This will create the database with sample challenges.

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

---

## 📖 Usage

### For Participants

1. **Register an Account**
   - Navigate to `/register`
   - Fill in your details (first name, last name, email, phone, username, password)
   - Submit to create your account

2. **Login**
   - Go to `/login`
   - Enter your credentials
   - **Note:** Your activity is monitored from this point

3. **Solve Challenges**
   - Browse available challenges at `/challenges`
   - Read challenge descriptions
   - Submit flags in format: `flag{...}`
   - Earn points for correct submissions

4. **View Leaderboard**
   - Check your ranking at `/leaderboard`
   - See top performers

5. **Check Profile**
   - View your stats at `/profile`
   - See total points, challenges solved, and rank

### For Administrators

1. **Access Dashboard**
   - Login with admin credentials
   - Navigate to `/dashboard`

2. **Monitor Alerts**
   - View all security alerts
   - Filter by risk level (Critical, Medium, Low)
   - Review user activities

3. **Take Action**
   - **Warn User:** Send warning notification
   - **Ban User:** Permanently ban suspicious accounts
   - **Export Report:** Download CSV of all alerts

4. **Run Detection Engine**
   ```bash
   python enhanced_detection.py
   ```
   This runs a comprehensive scan of all user activities.

---

## 🧠 Detection Algorithms

### 1. Multi-Account Detection
**Purpose:** Identify users operating multiple accounts

**Algorithm:**
- Groups users by IP address
- Identifies IPs with 2+ distinct user accounts
- Risk Score: **50 points**

**Code:**
```python
def detect_multi_account(self):
    # Get all IPs with multiple users
    query = """
        SELECT ip, COUNT(DISTINCT id) as count
        FROM users
        WHERE ip IS NOT NULL
        GROUP BY ip
        HAVING count > 1
    """
```

### 2. Flag Sharing Detection
**Purpose:** Detect users sharing flags

**Algorithm:**
- Tracks submission timestamps per challenge
- Flags submissions within 30 seconds of each other
- Risk Score: **65 points**

**Indicators:**
- Same flag submitted by different users within seconds
- Identical solving patterns

### 3. Speed Anomaly Detection
**Purpose:** Identify impossibly fast solving

**Algorithm:**
- Calculates average time between submissions
- Flags users with avg < 60 seconds
- Risk Score: **70 points**

**Formula:**
```
avg_time = Σ(time_differences) / count
if avg_time < 60s: FLAG as suspicious
```

### 4. Impossible Solving Detection
**Purpose:** Detect unnatural difficulty progression

**Algorithm:**
- Checks if first submission is a Hard challenge
- Expects users to solve Easy/Medium first
- Risk Score: **55 points**

### 5. Device Switching Detection
**Purpose:** Identify excessive device changes

**Algorithm:**
- Counts distinct devices per user
- Flags users with 3+ different devices
- Risk Score: **35 points**

### 6. Burst Submission Detection
**Purpose:** Detect automated solving tools

**Algorithm:**
- Identifies 3+ submissions within 5 minutes
- Indicates possible bot usage
- Risk Score: **45 points**

### 7. Device Fingerprint Collision
**Purpose:** Detect multiple accounts on same device

**Algorithm:**
- Compares browser fingerprints
- Flags identical fingerprints across users
- Risk Score: **40 points**

### Risk Score Calculation

```
Total Risk = Σ(Individual Alert Scores)

Classification:
- 0-29:   Low Risk (Green)
- 30-59:  Medium Risk (Yellow)
- 60-79:  High Risk (Orange)
- 80+:    Critical Risk (Red)
```

---

## 🔌 API Documentation

### User Registration
```
POST /register
Content-Type: application/x-www-form-urlencoded

Parameters:
  - first_name: string
  - last_name: string
  - email: string
  - phone: string
  - username: string
  - password: string

Response:
  - Redirect to /login on success
```

### User Login
```
POST /login
Content-Type: application/x-www-form-urlencoded

Parameters:
  - username: string
  - password: string

Response:
  - Redirect to /challenges on success
  - Sets session cookie
  - Logs IP address
```

### Submit Flag
```
POST /challenges
Content-Type: application/x-www-form-urlencoded

Parameters:
  - challenge_id: integer
  - flag: string

Response:
  - Success message with points
  - Triggers detection algorithms
```

### Log Violation
```
POST /log_violation
Content-Type: application/json

Body:
{
  "type": "violation_type",
  "data": {
    "timestamp": "ISO-8601",
    ...additional data
  },
  "fingerprint": {
    "userAgent": "...",
    "canvas": "...",
    ...fingerprint data
  }
}

Response:
{
  "status": "ok"
}
```

---

## 🔒 Security Features

### Client-Side Monitoring

1. **Tab Switching Detection**
   - Tracks `visibilitychange` events
   - Flags excessive tab switches (> 3)

2. **Copy-Paste Monitoring**
   - Monitors clipboard events
   - Alerts on excessive copy (> 5) or paste (> 3)

3. **DevTools Detection**
   - Keyboard shortcut tracking (F12, Ctrl+Shift+I, etc.)
   - Window size monitoring for DevTools panel

4. **Browser Fingerprinting**
   - Canvas fingerprinting
   - WebGL fingerprinting
   - User agent, language, platform
   - Screen resolution and color depth

5. **Mouse Movement Analysis**
   - Detects bot-like uniform movements
   - Tracks click speed patterns

### Server-Side Security

1. **Password Hashing**
   - Uses Werkzeug's `generate_password_hash`
   - Secure password storage

2. **Session Management**
   - Flask session with secret key
   - Automatic session expiration

3. **SQL Injection Prevention**
   - Parameterized queries
   - No raw SQL concatenation

4. **IP Logging**
   - Tracks user IP addresses
   - Enables network-based detection

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  phone TEXT,
  username TEXT,
  password TEXT,
  role TEXT,
  ip TEXT
);
```

### Challenges Table
```sql
CREATE TABLE challenges (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  description TEXT,
  difficulty TEXT,
  flag TEXT,
  points INTEGER
);
```

### Submissions Table
```sql
CREATE TABLE submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  challenge_id INTEGER,
  time TEXT,
  ip TEXT,
  device TEXT
);
```

### Alerts Table
```sql
CREATE TABLE alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  reason TEXT,
  risk_score INTEGER
);
```

---

## 🧪 Testing

### Manual Testing

1. **Create Multiple Accounts**
   ```bash
   # Register 2+ accounts from same browser
   # Expected: Multi-account alert triggered
   ```

2. **Rapid Submissions**
   ```bash
   # Submit flags quickly (< 30s apart)
   # Expected: Speed anomaly alert
   ```

3. **Tab Switching**
   ```bash
   # Switch tabs repeatedly during challenges
   # Expected: Tab switch violation logged
   ```

### Automated Testing

Run the detection engine:
```bash
python enhanced_detection.py
```

View output for detected anomalies and risk scores.

---

## 🎓 How to Explain to Your Team

**30-Second Elevator Pitch:**
> "Our project is a security layer for CTF competitions that monitors user behavior, tracks submissions, and detects cheating using pattern analysis, IP tracking, and timestamp comparison. It helps admins identify suspicious participants and maintain fairness in competitions."

**Real-Life Example:**
> If 3 users submit the same flag within 5 seconds from the same IP, the system will mark them as suspicious and send an alert to the admin.

---

## 🚀 Future Improvements

- [ ] **Machine Learning Integration**
  - Train ML models on historical cheat patterns
  - Predictive risk scoring

- [ ] **Advanced Fingerprinting**
  - Audio fingerprinting
  - Font enumeration
  - Battery API tracking

- [ ] **Screen Monitoring**
  - Screenshot capture (with consent)
  - Eye-tracking integration

- [ ] **Blockchain Verification**
  - Immutable submission records
  - Cryptographic proof of solving

- [ ] **AI-Based Prediction**
  - Neural networks for behavior analysis
  - Anomaly detection using autoencoders

---

## 📝 License

MIT License - Free to use for educational purposes

---

## 👥 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

---

## 📧 Contact

For questions or support, please contact the development team.

---

## 🎯 Unique Selling Points (USP)

✅ **Real-time cheat detection**  
✅ **Behavior-based analysis** (not just rule-based)  
✅ **Admin visibility & control**  
✅ **Scalable for large CTF events**  
✅ **Open source and customizable**

---

**Made with ❤️ for fair and secure CTF competitions**
