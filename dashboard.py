import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://localhost:8000"  # later this becomes your deployed backend URL

# ---------------- LOGIN ----------------
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "analyst": {"password": "analyst123", "role": "Analyst"}
}

def login():
    st.title("🔐 Behavior Intelligence Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["role"] = USERS[username]["role"]
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

# ---------------- DASHBOARD ----------------
def dashboard():
    st.title("🧠 Behavior Intelligence Dashboard")
    st.write("Monitoring user behavior in real time")

    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    try:
        events = requests.get(f"{BACKEND_URL}/events_summary").json()["events"]
        df = pd.DataFrame(events)
    except:
        st.error("Backend not reachable")
        return

    st.metric("Total Events", len(df))

    if not df.empty:
        st.subheader("🚨 Active Alerts")
        alerts = df[df["risk_level"] == "HIGH"]
        if not alerts.empty:
            st.dataframe(alerts)
        else:
            st.success("No high-risk alerts")

        st.subheader("📡 Live Event Feed")
        st.dataframe(df.sort_values("timestamp", ascending=False))

        st.subheader("📊 Risk Level Distribution")
        st.bar_chart(df["risk_level"].value_counts())

# ---------------- MAIN ----------------
if "logged_in" not in st.session_state:
    login()
else:
    dashboard()