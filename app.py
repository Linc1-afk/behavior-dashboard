import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="Behavior Tracker", layout="wide")

# Create data folder if not exist
if not os.path.exists("data"):
    os.makedirs("data")

DATA_FILE = "data/activities.csv"
USERS_FILE = "data/users.csv"
EMAIL_TRACK_FILE = "data/weekly_email_tracker.csv"
TARGET_SCORE = 70  # Default target score

# ----------------------------
# EMAIL CONFIG
# ----------------------------
EMAIL_ADDRESS = "lincolngithii@gmail.com"
EMAIL_PASSWORD = "dzxarfditwbvrens"

# ----------------------------
# INITIALIZE FILES
# ----------------------------
for file, columns in [
    (DATA_FILE, ["User", "Activity", "Score", "Timestamp"]),
    (USERS_FILE, ["Email", "Password"]),
    (EMAIL_TRACK_FILE, ["User", "LastSent"])
]:
    if not os.path.exists(file):
        pd.DataFrame(columns=columns).to_csv(file, index=False)

# ----------------------------
# LOAD & SAVE FUNCTIONS
# ----------------------------
def load_data(): return pd.read_csv(DATA_FILE)
def save_data(df): df.to_csv(DATA_FILE, index=False)
def load_users(): return pd.read_csv(USERS_FILE)
def save_users(df): df.to_csv(USERS_FILE, index=False)
def load_tracker(): return pd.read_csv(EMAIL_TRACK_FILE)
def save_tracker(df): df.to_csv(EMAIL_TRACK_FILE, index=False)

# ----------------------------
# SEND EMAIL
# ----------------------------
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        html = f"""
        <html>
        <body>
        <h2>🧠 Behavior Tracking System</h2>
        <p>{body}</p>
        <hr>
        <small>Automated Notification</small>
        </body>
        </html>
        """
        msg.attach(MIMEText(html, "html"))
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        st.error(f"Email error: {e}")

# ----------------------------
# WEEKLY SUMMARY
# ----------------------------
def send_weekly_summary(user_email):
    df = load_data()
    tracker = load_tracker()
    df_user = df[df["User"] == user_email]
    if df_user.empty: return
    df_user["Timestamp"] = pd.to_datetime(df_user["Timestamp"], errors="coerce")
    last_week = datetime.now() - timedelta(days=7)
    df_week = df_user[df_user["Timestamp"] >= last_week]
    if df_week.empty: return
    row = tracker[tracker["User"] == user_email]
    if not row.empty:
        last_sent = pd.to_datetime(row["LastSent"].values[0], errors="coerce")
        if (datetime.now() - last_sent).days < 7: return
    avg_score = df_week["Score"].mean()
    total = df_week.shape[0]
    below = df_week[df_week["Score"] < TARGET_SCORE].shape[0]
    body = f"""
Weekly Summary

Total Activities: {total}
Average Score: {avg_score:.1f}
Below Target: {below}

Keep improving!
"""
    send_email(user_email, "Weekly Behavior Summary", body)
    if row.empty:
        tracker = pd.concat([tracker, pd.DataFrame([[user_email, datetime.now()]], columns=["User", "LastSent"])])
    else:
        tracker.loc[tracker["User"] == user_email, "LastSent"] = datetime.now()
    save_tracker(tracker)

# ----------------------------
# SESSION INIT
# ----------------------------
if "user" not in st.session_state: st.session_state.user = None

# ----------------------------
# LOGIN / REGISTER
# ----------------------------
if not st.session_state.user:
    st.title("🧠 Behavior Tracking System")
    st.subheader("Login or Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            users = load_users()
            user_row = users[(users["Email"] == email) & (users["Password"] == password)]
            if not user_row.empty:
                st.session_state.user = email
                st.success("Login successful")
                st.rerun()
            else: st.error("Invalid credentials")
    with col2:
        if st.button("Register"):
            users = load_users()
            if email and password:
                if email in users["Email"].values:
                    st.warning("User already exists")
                else:
                    new_user = pd.DataFrame([[email, password]], columns=["Email", "Password"])
                    users = pd.concat([users, new_user], ignore_index=True)
                    save_users(users)
                    st.success("Account created. You can now login.")

# ----------------------------
# DASHBOARD
# ----------------------------
else:
    user = st.session_state.user
    st.title(f"👨‍💼 Admin Dashboard - {user}")

    df = load_data()
    st.subheader("All Users Data")
    st.dataframe(df)

    # ----------------------------
    # SIDEBAR NAVIGATION
    # ----------------------------
    section = st.sidebar.radio("Navigation", ["Dashboard", "Add Activity", "Metrics"])
    df_user = df[df["User"] == user]
    if not df_user.empty:
        df_user["Timestamp"] = pd.to_datetime(df_user["Timestamp"], errors="coerce")
        df_user = df_user.sort_values("Timestamp")

    # ----------------------------
    # DASHBOARD VIEW
    # ----------------------------
    if section == "Dashboard" and not df_user.empty:
        st.subheader("📊 Performance Overview")
        avg = df_user["Score"].mean()
        best = df_user["Score"].max()
        total_activities = df_user.shape[0]
        above_target = df_user[df_user["Score"] >= TARGET_SCORE].shape[0]
        below_target = df_user[df_user["Score"] < TARGET_SCORE].shape[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Average Score", f"{avg:.1f}")
        col2.metric("Best Score", best)
        col3.metric("Total Activities", total_activities)
        col4.metric("Above Target", above_target)

        # Progress bar for above-target ratio
        st.progress(min(1.0, above_target/total_activities))
        st.write(f"Streak Above Target: {above_target}")

        # Line Chart
        st.line_chart(df_user.set_index("Timestamp")["Score"])

        # Pie Chart
        fig2, ax2 = plt.subplots()
        ax2.pie([above_target, below_target],
                labels=["Above Target","Below Target"],
                autopct="%1.1f%%",
                colors=["#4CAF50","#F44336"])
        ax2.set_title("Performance Distribution")
        st.pyplot(fig2)

        # Download charts
        st.subheader("Download Charts")
        fig1, ax1 = plt.subplots()
        ax1.plot(df_user["Timestamp"], df_user["Score"])
        ax1.set_title("Score Trend")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Score")
        buf1 = BytesIO(); fig1.savefig(buf1, format="png"); buf1.seek(0)
        st.download_button("Download Line Chart (PNG)", buf1, "line_chart.png", "image/png")
        plt.close(fig1)
        buf2 = BytesIO(); fig2.savefig(buf2, format="png"); buf2.seek(0)
        st.download_button("Download Pie Chart (PNG)", buf2, "pie_chart.png", "image/png")
        plt.close(fig2)

        # Download enhanced weekly summary CSV
        st.subheader("Download Weekly Summary CSV")
        weekly_summary = df_user.groupby(pd.Grouper(key="Timestamp", freq="W")).agg(
            total_activities=("Activity","count"),
            avg_score=("Score","mean"),
            below_target=("Score", lambda x: (x<TARGET_SCORE).sum())
        )
        st.download_button("Download Weekly CSV", weekly_summary.to_csv(index=True),
                           "weekly_summary.csv", "text/csv")

    # ----------------------------
    # ADD ACTIVITY VIEW
    # ----------------------------
    elif section == "Add Activity":
        st.subheader("➕ Add Activity")
        activity = st.text_input("Activity Name")
        score = st.number_input("Score", 0, 100)
        if st.button("Save Activity"):
            new_row = pd.DataFrame([[user, activity, score, datetime.now()]],
                                   columns=["User","Activity","Score","Timestamp"])
            df = pd.concat([df,new_row], ignore_index=True)
            save_data(df)
            if score < TARGET_SCORE:
                send_email(user, "Low Score Alert", f"You scored {score}, which is below target ({TARGET_SCORE}).")
            st.success("Activity saved!"); st.rerun()

    # ----------------------------
    # METRICS VIEW
    # ----------------------------
    elif section == "Metrics" and not df_user.empty:
        st.subheader("📈 Metrics & Table")
        # Conditional coloring for scores below target (fixed)
        st.dataframe(
            df_user.style.apply(
                lambda col: ['background-color: #FFCCCC' if v < TARGET_SCORE else '' for v in col],
                subset=['Score'], axis=0
            )
        )

    # Weekly summary
    send_weekly_summary(user)

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()