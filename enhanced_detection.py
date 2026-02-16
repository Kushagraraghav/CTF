"""
Enhanced Detection Module with Advanced Pattern Matching and Behavioral Analysis
"""

import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta
import json

class CheatDetectionEngine:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def __del__(self):
        self.conn.close()
    
    def get_user_submissions(self, user_id):
        """Get all submissions for a user"""
        self.cursor.execute("""
            SELECT s.*, c.difficulty, c.points
            FROM submissions s
            JOIN challenges c ON s.challenge_id = c.id
            WHERE s.user_id = ?
            ORDER BY s.time
        """, (user_id,))
        return self.cursor.fetchall()
    
    def detect_multi_account(self):
        """Detect multiple accounts from same IP"""
        print("[*] Detecting multi-account abuse...")
        
        # Get all IPs with multiple users
        self.cursor.execute("""
            SELECT ip, GROUP_CONCAT(DISTINCT id) as user_ids, COUNT(DISTINCT id) as count
            FROM users
            WHERE ip IS NOT NULL
            GROUP BY ip
            HAVING count > 1
        """)
        
        suspicious_ips = self.cursor.fetchall()
        
        for ip, user_ids, count in suspicious_ips:
            users = user_ids.split(',')
            for user_id in users:
                # Check if alert already exists
                self.cursor.execute("""
                    SELECT * FROM alerts 
                    WHERE user_id=? AND reason LIKE '%Multiple accounts%'
                """, (user_id,))
                
                if not self.cursor.fetchone():
                    self.cursor.execute("""
                        INSERT INTO alerts (user_id, reason, risk_score)
                        VALUES (?, ?, ?)
                    """, (user_id, f"Multiple accounts from same IP ({count} accounts)", 50))
        
        self.conn.commit()
        print(f"[+] Found {len(suspicious_ips)} suspicious IPs")
    
    def detect_flag_sharing(self):
        """Detect flag sharing (same flag submitted by multiple users within short time)"""
        print("[*] Detecting flag sharing...")
        
        # Get all submissions grouped by challenge
        self.cursor.execute("""
            SELECT challenge_id, user_id, time
            FROM submissions
            ORDER BY challenge_id, time
        """)
        
        submissions = self.cursor.fetchall()
        
        # Group by challenge
        by_challenge = defaultdict(list)
        for challenge_id, user_id, time in submissions:
            by_challenge[challenge_id].append((user_id, time))
        
        # Check for suspicious patterns
        for challenge_id, user_times in by_challenge.items():
            for i in range(len(user_times)):
                for j in range(i + 1, len(user_times)):
                    user1, time1 = user_times[i]
                    user2, time2 = user_times[j]
                    
                    # Convert to datetime
                    dt1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
                    dt2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
                    
                    # If submitted within 30 seconds
                    if abs((dt2 - dt1).total_seconds()) < 30:
                        # Log alert for both users
                        for user in [user1, user2]:
                            self.cursor.execute("""
                                INSERT INTO alerts (user_id, reason, risk_score)
                                VALUES (?, ?, ?)
                            """, (user, f"Potential flag sharing detected (Challenge {challenge_id})", 65))
        
        self.conn.commit()
        print("[+] Flag sharing detection complete")
    
    def detect_speed_anomaly(self):
        """Detect unusually fast solving patterns"""
        print("[*] Detecting speed anomalies...")
        
        # Get all users
        self.cursor.execute("SELECT DISTINCT user_id FROM submissions")
        users = [row[0] for row in self.cursor.fetchall()]
        
        for user_id in users:
            submissions = self.get_user_submissions(user_id)
            
            if len(submissions) < 2:
                continue
            
            # Calculate average time between submissions
            times = []
            for i in range(1, len(submissions)):
                prev_time = datetime.strptime(submissions[i-1][3], "%Y-%m-%d %H:%M:%S")
                curr_time = datetime.strptime(submissions[i][3], "%Y-%m-%d %H:%M:%S")
                diff = (curr_time - prev_time).total_seconds()
                times.append(diff)
            
            avg_time = sum(times) / len(times)
            
            # Check for consistently fast submissions (possible automated solving)
            if avg_time < 60:  # Less than 1 minute average
                self.cursor.execute("""
                    INSERT INTO alerts (user_id, reason, risk_score)
                    VALUES (?, ?, ?)
                """, (user_id, f"Unusually fast solving pattern (avg {avg_time:.1f}s)", 70))
        
        self.conn.commit()
        print("[+] Speed anomaly detection complete")
    
    def detect_impossible_solving(self):
        """Detect solving hard challenges without attempting easier ones"""
        print("[*] Detecting impossible solving patterns...")
        
        self.cursor.execute("SELECT DISTINCT user_id FROM submissions")
        users = [row[0] for row in self.cursor.fetchall()]
        
        for user_id in users:
            # Get user's first submission
            self.cursor.execute("""
                SELECT c.difficulty, c.points, s.time
                FROM submissions s
                JOIN challenges c ON s.challenge_id = c.id
                WHERE s.user_id = ?
                ORDER BY s.time
                LIMIT 1
            """, (user_id,))
            
            first_submission = self.cursor.fetchone()
            
            if first_submission and first_submission[0] == 'Hard':
                # User's first solve was a hard challenge - suspicious
                self.cursor.execute("""
                    INSERT INTO alerts (user_id, reason, risk_score)
                    VALUES (?, ?, ?)
                """, (user_id, "First submission was a Hard challenge (suspicious progression)", 55))
        
        self.conn.commit()
        print("[+] Impossible solving detection complete")
    
    def detect_device_switching(self):
        """Detect users switching devices excessively"""
        print("[*] Detecting device switching...")
        
        self.cursor.execute("""
            SELECT user_id, COUNT(DISTINCT device) as device_count, 
                   GROUP_CONCAT(DISTINCT device) as devices
            FROM submissions
            GROUP BY user_id
            HAVING device_count > 2
        """)
        
        suspicious_users = self.cursor.fetchall()
        
        for user_id, device_count, devices in suspicious_users:
            self.cursor.execute("""
                INSERT INTO alerts (user_id, reason, risk_score)
                VALUES (?, ?, ?)
            """, (user_id, f"Multiple devices detected ({device_count} devices)", 35))
        
        self.conn.commit()
        print(f"[+] Found {len(suspicious_users)} users with device switching")
    
    def detect_burst_submissions(self):
        """Detect burst submission patterns (many submissions in short time)"""
        print("[*] Detecting burst submissions...")
        
        self.cursor.execute("SELECT DISTINCT user_id FROM submissions")
        users = [row[0] for row in self.cursor.fetchall()]
        
        for user_id in users:
            # Get all submission times
            self.cursor.execute("""
                SELECT time FROM submissions
                WHERE user_id = ?
                ORDER BY time
            """, (user_id,))
            
            times = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") 
                    for row in self.cursor.fetchall()]
            
            if len(times) < 3:
                continue
            
            # Check for 3+ submissions within 5 minutes
            for i in range(len(times) - 2):
                window = times[i:i+3]
                time_span = (window[-1] - window[0]).total_seconds()
                
                if time_span < 300:  # 5 minutes
                    self.cursor.execute("""
                        INSERT INTO alerts (user_id, reason, risk_score)
                        VALUES (?, ?, ?)
                    """, (user_id, f"Burst submission detected (3 solves in {time_span:.0f}s)", 45))
                    break
        
        self.conn.commit()
        print("[+] Burst submission detection complete")
    
    def detect_same_device_fingerprint(self):
        """Detect multiple users with identical device fingerprints"""
        print("[*] Detecting device fingerprint collisions...")
        
        # This would require storing fingerprint data in database
        # Placeholder for advanced implementation
        self.cursor.execute("""
            SELECT device, COUNT(DISTINCT user_id) as user_count
            FROM submissions
            GROUP BY device
            HAVING user_count > 1
        """)
        
        collisions = self.cursor.fetchall()
        
        for device, user_count in collisions:
            # Get affected users
            self.cursor.execute("""
                SELECT DISTINCT user_id FROM submissions
                WHERE device = ?
            """, (device,))
            
            users = [row[0] for row in self.cursor.fetchall()]
            
            for user_id in users:
                self.cursor.execute("""
                    INSERT INTO alerts (user_id, reason, risk_score)
                    VALUES (?, ?, ?)
                """, (user_id, f"Device fingerprint collision with {user_count} users", 40))
        
        self.conn.commit()
        print(f"[+] Found {len(collisions)} device fingerprint collisions")
    
    def calculate_user_risk_score(self, user_id):
        """Calculate overall risk score for a user"""
        self.cursor.execute("""
            SELECT SUM(risk_score) FROM alerts
            WHERE user_id = ?
        """, (user_id,))
        
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0
    
    def get_high_risk_users(self, threshold=80):
        """Get users with risk score above threshold"""
        self.cursor.execute("""
            SELECT user_id, SUM(risk_score) as total_risk
            FROM alerts
            GROUP BY user_id
            HAVING total_risk >= ?
            ORDER BY total_risk DESC
        """, (threshold,))
        
        return self.cursor.fetchall()
    
    def run_all_detections(self):
        """Run all detection algorithms"""
        print("\n" + "="*60)
        print(" CTF CHEAT DETECTION ENGINE - FULL SCAN")
        print("="*60 + "\n")
        
        self.detect_multi_account()
        self.detect_flag_sharing()
        self.detect_speed_anomaly()
        self.detect_impossible_solving()
        self.detect_device_switching()
        self.detect_burst_submissions()
        self.detect_same_device_fingerprint()
        
        print("\n" + "="*60)
        print(" HIGH RISK USERS")
        print("="*60)
        
        high_risk = self.get_high_risk_users()
        if high_risk:
            for user_id, total_risk in high_risk:
                print(f"User {user_id}: Risk Score = {total_risk}")
        else:
            print("No high-risk users detected")
        
        print("\n[✓] Detection engine completed successfully\n")


if __name__ == "__main__":
    engine = CheatDetectionEngine()
    engine.run_all_detections()
