import streamlit as st
from database import Session, BehaviorHistory

def run_dashboard():
    st.title("Behavior Dashboard")

    activity = st.text_input("Activity")
    score = st.number_input("Score", min_value=0, max_value=100, value=0)
    state = st.text_input("State")

    if st.button("Log Behavior"):
        session = Session()
        try:
            record = BehaviorHistory(activity=activity, score=score, state=state)
            session.add(record)
            session.commit()
            st.success("Behavior logged successfully!")
        except Exception as e:
            session.rollback()
            st.error(f"Error logging behavior: {e}")
        finally:
            session.close()