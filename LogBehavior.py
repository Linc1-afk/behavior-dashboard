import streamlit as st
from database import Session, BehaviorHistory

st.title("Log New Behavior")

activity = st.text_input("Activity")
score = st.number_input("Score", min_value=0, max_value=100)
state = st.text_input("State")

if st.button("Log Behavior"):
    session = Session()
    try:
        new_record = BehaviorHistory(activity=activity, score=score, state=state)
        session.add(new_record)
        session.commit()
        st.success("Behavior logged successfully!")
    except Exception as e:
        session.rollback()
        st.error(f"Error: {e}")
    finally:
        session.close()