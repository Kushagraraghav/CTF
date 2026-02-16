import sqlite3
from collections import defaultdict

def detect_cheating():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT user_id, challenge_id, time, ip FROM submissions")
    rows = c.fetchall()

    ip_users = defaultdict(set)

    for user_id, ch_id, time, ip in rows:
        ip_users[ip].add(user_id)

    for ip, users in ip_users.items():
        if len(users) > 1:
            for u in users:
                c.execute("INSERT INTO alerts (user_id, reason, risk_score) VALUES (?, ?, ?)",
                          (u, "Multiple accounts from same IP", 30))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    detect_cheating()
    print("Cheating detection complete")
