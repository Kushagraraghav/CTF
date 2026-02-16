import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# ---------------- USERS TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT,
last_name TEXT,
email TEXT,
phone TEXT,
username TEXT,
password TEXT,
role TEXT,
ip TEXT
)
""")



# ---------------- CHALLENGES TABLE (UPDATED WITH POINTS) ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS challenges(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
description TEXT,
difficulty TEXT,
flag TEXT,
points INTEGER
)
""")


# ---------------- SUBMISSIONS TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS submissions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
challenge_id INTEGER,
time TEXT,
ip TEXT,
device TEXT
)
""")

# ---------------- ALERTS TABLE ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS alerts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
reason TEXT,
risk_score INTEGER
)
""")

# ---------------- INSERT SAMPLE CHALLENGES ----------------
# Challenge 1
c.execute("""
INSERT INTO challenges (name, description, difficulty, flag, points)
VALUES (?, ?, ?, ?, ?)
""", (
"Web Exploitation",
"Find SQL injection vulnerability in the login form",
"Medium",
"flag{sql}",
70
))

# Challenge 2
c.execute("""
INSERT INTO challenges (name, description, difficulty, flag, points)
VALUES (?, ?, ?, ?, ?)
""", (
"Password Cracking",
"Guess the weak password used by the admin",
"Easy",
"flag{password123}",
40
))

# Challenge 3
c.execute("""
INSERT INTO challenges (name, description, difficulty, flag, points)
VALUES (?, ?, ?, ?, ?)
""", (
"Cryptography",
"Decode the encrypted message to find the hidden flag",
"Hard",
"flag{decrypt}",
90
))

# Challenge 4
c.execute("""
INSERT INTO challenges (name, description, difficulty, flag, points)
VALUES (?, ?, ?, ?, ?)
""", (
"Network Analysis",
"Analyze packet data to find suspicious activity",
"Medium",
"flag{packet}",
60
))

# Challenge 5
c.execute("""
INSERT INTO challenges (name, description, difficulty, flag, points)
VALUES (?, ?, ?, ?, ?)
""", (
"OSINT Investigation",
"Search online information to find the hidden clue",
"Easy",
"flag{osint}",
50
))

conn.commit()
conn.close()

print("Database created successfully with challenges and points")
