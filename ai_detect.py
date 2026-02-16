import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest

conn = sqlite3.connect("database.db")

# Get submission count per user
df = pd.read_sql_query("""
SELECT user_id, COUNT(*) as submissions
FROM submissions
GROUP BY user_id
""", conn)

# Train AI model
model = IsolationForest(contamination=0.2)
df['anomaly'] = model.fit_predict(df[['submissions']])

# Calculate risk score
df['risk_score'] = 0

for i, row in df.iterrows():
    risk = 0
    
    if row['submissions'] > 10:
        risk += 20
        
    if row['anomaly'] == -1:
        risk += 40
        
    df.at[i, 'risk_score'] = risk

# Save alerts to DB
c = conn.cursor()

for i, row in df.iterrows():
    if row['risk_score'] > 0:
        c.execute("""
        INSERT INTO alerts (user_id, reason, risk_score)
        VALUES (?, ?, ?)
        """, (row['user_id'], "AI Suspicious Behaviour", row['risk_score']))

conn.commit()
conn.close()

print("AI Risk Analysis Completed")
