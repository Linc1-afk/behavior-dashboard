import streamlit as st
from database import Session, BehaviorHistory

def run_history():
    st.title("Behavior History")

    session = Session()
    try:
        records = session.query(BehaviorHistory).order_by(BehaviorHistory.timestamp.desc()).all()
        for r in records:
            st.write(f"Time: {r.timestamp} | Activity: {r.activity} | Score: {r.score} | State: {r.state}")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    finally:
        session.close()