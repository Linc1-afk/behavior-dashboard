import streamlit as st
from datetime import datetime
from database import SessionLocal
from models import User, BehaviorHistory

# -----------------------------
# Initialize session_state
# -----------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# -----------------------------
# Signup
# -----------------------------
def signup():
    st.subheader("Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pass")

    if st.button("Create Account"):
        db = SessionLocal()
        existing_user = db.query(User).filter_by(email=email).first()
        if existing_user:
            st.error("Email already exists.")
        else:
            new_user = User(email=email, password=password)
            db.add(new_user)
            db.commit()
            st.session_state["user"] = email  # auto-login
            st.success("Account created successfully!")
            st.rerun()

# -----------------------------
# Login
# -----------------------------
def login():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        db = SessionLocal()
        user = db.query(User).filter_by(email=email, password=password).first()
        if user:
            st.session_state["user"] = email
            st.success(f"Welcome {email}!")
            st.experimental_rerun()
        else:
            st.error("Invalid password or email")

# -----------------------------
# Dashboard
# -----------------------------
def dashboard():
    st.subheader(f"Welcome {st.session_state['user']}")
    st.write("Here you can add activity, score, and state.")

    db = SessionLocal()

    # Add new activity
    st.markdown("### Add New Activity")
    activity = st.text_input("Activity", key="act")
    score = st.number_input("Score", min_value=0, max_value=100, key="score")
    state = st.text_input("State", key="state")

    if st.button("Save Activity"):
        if activity.strip() == "":
            st.error("Activity cannot be empty.")
        else:
            new_entry = BehaviorHistory(
                user_email=st.session_state["user"],
                timestamp=datetime.now(),
                activity=activity,
                score=score,
                state=state
            )
            db.add(new_entry)
            db.commit()
            st.success("Activity saved successfully!")
            st.rerun()

    # Display history
    st.markdown("### Your History")
    records = db.query(BehaviorHistory).filter(
        BehaviorHistory.user_email == st.session_state["user"]
    ).order_by(BehaviorHistory.timestamp.desc()).all()

    if records:
        for r in records:
            st.write(f"{r.timestamp} | {r.activity} | Score: {r.score} | State: {r.state}")
    else:
        st.info("No behavior history found yet.")

# -----------------------------
# Main App
# -----------------------------
def main():
    st.title("Behavior Tracker App")

    if st.session_state["user"]:
        dashboard()
    else:
        st.write("Please sign up or log in.")
        signup()
        st.markdown("---")
        login()

# -----------------------------
# Run the app
# -----------------------------
if __name__ == "__main__":
    main()