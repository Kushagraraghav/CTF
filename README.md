# 🔐 CTF Integrity & Cheat Detection System

> A comprehensive platform to ensure fairness, authenticity, and security in Capture The Flag (CTF) competitions through real-time monitoring and intelligent cheat detection.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

This system acts as a **"digital invigilator"** for CTF competitions, monitoring user activities, detecting suspicious patterns, and maintaining competition integrity.

### Key Problems Solved
✅ Flag sharing between participants  
✅ Multiple account usage  
✅ Automated tool exploitation  
✅ Unnatural solving patterns  
✅ Device and IP manipulation  

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Real-time Monitoring** | Track user activities, IP addresses, device fingerprints |
| 🚨 **Alert System** | Automatic flagging of suspicious behaviors |
| 📊 **Admin Dashboard** | Comprehensive view of all security alerts |
| 🤖 **AI Detection** | Machine learning-based anomaly detection |
| 🛡️ **Multi-layer Security** | Browser fingerprinting, behavioral analysis |
| 📈 **Risk Scoring** | Calculate and classify user risk levels |

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python db_setup.py

# Run application
python app.py
```

Visit: `http://localhost:5000`

### First Steps
1. Register an account at `/register`
2. Login at `/login`
3. Solve challenges at `/challenges`
4. View leaderboard at `/leaderboard`
5. Check admin dashboard at `/dashboard` (admin role required)

## 📸 Screenshots

### User Interface
- **Modern, responsive design** with gradient themes
- **Intuitive navigation** with icon-based menu
- **Real-time security notifications**

### Admin Dashboard
- **Alert filtering** by risk level (Critical, Medium, Low)
- **User action controls** (Warn, Ban)
- **Export functionality** for reports

## 🧠 Detection Algorithms

Our system implements 7 advanced detection algorithms:

1. **Multi-Account Detection** (Risk: 50) - Same IP, multiple accounts
2. **Flag Sharing Detection** (Risk: 65) - Simultaneous submissions
3. **Speed Anomaly Detection** (Risk: 70) - Impossibly fast solving
4. **Impossible Solving** (Risk: 55) - Hard challenges first
5. **Device Switching** (Risk: 35) - Multiple devices per user
6. **Burst Submissions** (Risk: 45) - Rapid consecutive solves
7. **Fingerprint Collision** (Risk: 40) - Same device, multiple users

## 🏗️ Architecture

```
User → Flask App → Monitoring Layer → Detection Engine → Admin Dashboard
```

**Tech Stack:**
- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- ML: scikit-learn, pandas

## 📚 Documentation

- [📖 Full Documentation](DOCUMENTATION.md) - Complete system guide
- [🚀 Setup Guide](SETUP.md) - Quick installation instructions
- [🧪 Testing Guide](#testing) - How to test detection features

## 🔒 Security Features

### Client-Side Monitoring
- Tab switching detection
- Copy-paste tracking
- DevTools usage monitoring
- Browser fingerprinting (Canvas, WebGL)
- Mouse movement analysis

### Server-Side Protection
- Password hashing (Werkzeug)
- Session management
- SQL injection prevention
- IP logging and analysis

## 📊 Database Schema

```sql
users:        User accounts and profiles
challenges:   CTF challenges with flags
submissions:  User solutions and timestamps
alerts:       Security violations and risk scores
```

## 🧪 Testing

### Manual Test Scenarios
```bash
# Test 1: Create multiple accounts from same browser
# Expected: Multi-account alert

# Test 2: Submit flags rapidly (< 30 seconds)
# Expected: Speed anomaly alert

# Test 3: Switch tabs during challenge
# Expected: Tab switch violation logged
```

### Run Detection Engine
```bash
python enhanced_detection.py
```

### Run AI Detection
```bash
python ai_detect.py
```

## 🎓 Project Explanation

**One-Line Summary:**
> A smart monitoring system that protects CTF competition integrity by detecting cheating through behavior analysis and activity tracking.

**30-Second Pitch:**
> Our project is a security layer for CTF competitions that monitors user behavior, tracks submissions, and detects cheating using pattern analysis, IP tracking, and timestamp comparison. It helps admins identify suspicious participants and maintain fairness.

## 🎯 Unique Selling Points

✅ Real-time cheat detection  
✅ Behavior-based analysis (not just rule-based)  
✅ Admin visibility & control  
✅ Scalable for large CTF events  
✅ Open source and customizable  

## 🚀 Future Improvements

- [ ] Machine learning-based prediction models
- [ ] Advanced browser fingerprinting (audio, fonts)
- [ ] Screen monitoring integration
- [ ] Blockchain-based submission verification
- [ ] Mobile app for administrators
- [ ] Multi-language support

## 📦 Project Structure

```
webapp/
├── app.py                    # Main Flask application
├── enhanced_detection.py     # Advanced detection engine
├── ai_detect.py              # ML-based detection
├── db_setup.py              # Database initialization
├── requirements.txt         # Dependencies
├── templates/               # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── challenges.html
│   └── admin.html
└── static/                  # CSS, JS, images
    ├── css/style.css
    └── js/monitoring.js
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👥 Team

Built with ❤️ for secure and fair CTF competitions

## 📞 Support

- 📖 [Read Documentation](DOCUMENTATION.md)
- 🐛 [Report Issues](https://github.com/yourusername/ctf-integrity/issues)
- 💬 [Discussions](https://github.com/yourusername/ctf-integrity/discussions)

## 🌟 Acknowledgments

Special thanks to the CTF and cybersecurity community for inspiration and feedback.

---

**⚡ Quick Commands:**
```bash
python app.py              # Start server
python enhanced_detection.py  # Run detection
python ai_detect.py        # AI analysis
```

**Made for educational purposes and fair competition** 🎯
