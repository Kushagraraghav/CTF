from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, session
import sqlite3
import datetime
from user_agents import parse
from flask import jsonify

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = get_db()
        c = conn.cursor()

        c.execute("""
        INSERT INTO users 
        (first_name, last_name, email, phone, username, password, role)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, email, phone, username, password, "user"))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------
# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()

        if user and check_password_hash(user[6], password):

            session["user_id"] = user[0]
            session["role"] = user[7]

            # ---------------- STEP 3.2: SAVE USER IP ----------------
            ip = request.remote_addr

            c.execute("UPDATE users SET ip=? WHERE id=?", (ip, user[0]))
            conn.commit()

            # ---------------- STEP 3.3: SAME IP DETECTION ----------------
            c.execute("SELECT COUNT(*) FROM users WHERE ip=?", (ip,))
            count = c.fetchone()[0]

            if count > 1:
                c.execute("""
                    INSERT INTO alerts (user_id, reason, risk_score)
                    VALUES (?, ?, ?)
                """, (
                    user[0],
                    "Multiple accounts detected from same IP",
                    40
                ))
                conn.commit()

            conn.close()
            return redirect("/challenges")

        else:
            conn.close()
            return "Invalid login"

    return render_template("login.html")


# ---------------- CHALLENGES ----------------
@app.route("/challenges", methods=["GET", "POST"])
def challenges():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    c = conn.cursor()
    result = ""

    if request.method == "POST":
        flag = request.form["flag"]
        challenge_id = request.form["challenge_id"]

        # Check if already solved
        c.execute("""
        SELECT * FROM submissions
        WHERE user_id=? AND challenge_id=?
        """, (session["user_id"], challenge_id))

        already_solved = c.fetchone()

        if already_solved:
            result = "You already solved this challenge!"

        else:
            # Get correct flag
            c.execute("SELECT flag FROM challenges WHERE id=?", (challenge_id,))
            real_flag = c.fetchone()[0]

            if flag == real_flag:
                result = "Correct Flag! Points Added."

                # Log submission
                time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ip = request.remote_addr
                ua = parse(request.headers.get("User-Agent"))
                device = ua.browser.family

                c.execute("""
                    INSERT INTO submissions (user_id, challenge_id, time, ip, device)
                    VALUES (?, ?, ?, ?, ?)
                """, (session["user_id"], challenge_id, time_now, ip, device))

                conn.commit()

                # -------- FAST SOLVING DETECTION --------
                c.execute("""
                SELECT time FROM submissions
                WHERE user_id=?
                ORDER BY id DESC LIMIT 2
                """, (session["user_id"],))

                last_times = c.fetchall()

                if len(last_times) == 2:
                    t1 = datetime.datetime.strptime(last_times[0][0], "%Y-%m-%d %H:%M:%S")
                    t2 = datetime.datetime.strptime(last_times[1][0], "%Y-%m-%d %H:%M:%S")

                    diff = (t1 - t2).seconds

                    if diff < 10:
                        c.execute("""
                        INSERT INTO alerts (user_id, reason, risk_score)
                        VALUES (?, ?, ?)
                        """, (session["user_id"], "Very fast solving detected", 25))
                        conn.commit()

                # -------- ACTIVITY RISK SCORE --------
                c.execute("SELECT COUNT(*) FROM submissions WHERE user_id=?", (session["user_id"],))
                submission_count = c.fetchone()[0]

                risk_score = 0
                if submission_count > 5:
                    risk_score += 20
                if submission_count > 10:
                    risk_score += 30

                if risk_score > 0:
                    c.execute("""
                    INSERT INTO alerts (user_id, reason, risk_score)
                    VALUES (?, ?, ?)
                    """, (session["user_id"], "High submission activity detected", risk_score))
                    conn.commit()

            else:
                result = "Wrong Flag!"

    c.execute("SELECT * FROM challenges")
    all_challenges = c.fetchall()
    conn.close()

    return render_template("challenges.html", challenges=all_challenges, result=result)

# ---------------- LEADERBOARD ----------------
@app.route("/leaderboard")
def leaderboard():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
    SELECT users.username, SUM(challenges.points) as total_points
    FROM submissions
    JOIN users ON submissions.user_id = users.id
    JOIN challenges ON submissions.challenge_id = challenges.id
    GROUP BY users.username
    ORDER BY total_points DESC
    """)

    board = c.fetchall()
    conn.close()

    return render_template("leaderboard.html", board=board)

# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    c = conn.cursor()

    c.execute("""
    SELECT first_name, last_name, username
    FROM users WHERE id=?
    """, (session["user_id"],))
    user = c.fetchone()

    first_name, last_name, username = user
    full_name = first_name + " " + last_name

    # Total score
    c.execute("""
    SELECT SUM(challenges.points)
    FROM submissions
    JOIN challenges ON submissions.challenge_id = challenges.id
    WHERE submissions.user_id=?
    """, (session["user_id"],))
    total_score = c.fetchone()[0]
    if total_score is None:
        total_score = 0

    # Challenges solved
    c.execute("SELECT COUNT(*) FROM submissions WHERE user_id=?", (session["user_id"],))
    solved = c.fetchone()[0]

    # Rank
    c.execute("""
    SELECT users.username, SUM(challenges.points) as total_points
    FROM submissions
    JOIN users ON submissions.user_id = users.id
    JOIN challenges ON submissions.challenge_id = challenges.id
    GROUP BY users.username
    ORDER BY total_points DESC
    """)
    ranking = c.fetchall()

    rank = 0
    for i, row in enumerate(ranking, start=1):
        if row[0] == username:
            rank = i
            break

    conn.close()

    return render_template(
        "profile.html",
        full_name=full_name,
        total_score=total_score,
        solved=solved,
        rank=rank
    )

# ---------------- ADMIN ----------------
@app.route("/dashboard")
def dashboard():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM alerts")
    alerts = c.fetchall()
    conn.close()
    return render_template("admin.html", alerts=alerts)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- RUN ----------------


@app.route("/log_violation", methods=["POST"])
def log_violation():
    if "user_id" not in session:
        return jsonify({"status": "not_logged_in"}), 401

    data = request.get_json()
    vtype = data.get("type")
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr

    conn = get_db()
    c = conn.cursor()

    # Store as alert entry
    c.execute("""
        INSERT INTO alerts (user_id, reason, risk_score)
        VALUES (?, ?, ?)
    """, (session["user_id"], f"Exam violation: {vtype}", 15))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
