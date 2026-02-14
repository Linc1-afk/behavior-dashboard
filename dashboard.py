def dashboard():
    import pandas as pd
    from datetime import datetime
    from database import SessionLocal
    from models import BehaviorHistory

    st.subheader(f"Welcome {st.session_state['user']}")

    db = SessionLocal()

    # Add Activity
    st.markdown("### ➕ Add Activity")

    activity = st.text_input("Activity", key="activity_input")
    score = st.number_input("Score", min_value=0, max_value=100, key="score_input")
    state = st.text_input("State", key="state_input")

    if st.button("Save Activity"):
        if activity.strip() != "":
            new_entry = BehaviorHistory(
                user_email=st.session_state["user"],
                timestamp=datetime.now(),
                activity=activity,
                score=score,
                state=state
            )
            db.add(new_entry)
            db.commit()
            st.success("Saved successfully!")

    # Fetch records ONCE
    records = db.query(BehaviorHistory).filter(
        BehaviorHistory.user_email == st.session_state["user"]
    ).order_by(BehaviorHistory.timestamp.asc()).all()

    # Show History
    st.markdown("### 📜 History")

    if records:
        for r in records:
            st.write(f"{r.timestamp} | {r.activity} | {r.score} | {r.state}")
    else:
        st.info("No history yet.")

    # Graph
    st.markdown("### 📊 Score Trend")

    if len(records) >= 1:
        scores = [r.score for r in records]
        st.line_chart(scores)
    else:
        st.info("No data for graph.")