import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import smtplib
from email.mime.text import MIMEText

def send_alert_email(to_email, subject, body):
    """
    Send an email alert to the user
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "youremail@example.com"  # replace with your email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("youremail@example.com", "yourpassword")  # replace with your credentials
        server.send_message(msg)

def dashboard():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Add Activity", "Export Data"])

    st.title("📊 Behavior Insight Engine")

    # ---------------------------
    # Logout
    # ---------------------------
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.markdown("---")

    # ---------------------------
    # Add Activity
    # ---------------------------
    st.subheader("➕ Add Activity")
    col1, col2 = st.columns(2)
    with col1:
        activity = st.text_input("Activity")
        state = st.text_input("State")
    with col2:
        score = st.number_input("Score", min_value=0, max_value=100)

    if st.button("Save Activity"):
        if activity.strip() == "":
            st.error("Activity name cannot be empty.")
        else:
            new_entry = BehaviorHistory(
                user_email=st.session_state.user,
                timestamp=datetime.now(),
                activity=activity,
                score=score,
                state=state
            )
            db.add(new_entry)
            db.commit()

            # ---------------------------
            # Alerts & Email Notifications
            # ---------------------------
            if score < st.session_state.target_score:
                st.warning(f"⚠️ Score {score} is below your target of {st.session_state.target_score}!")
                send_alert_email(
                    to_email=st.session_state.user,
                    subject="Behavior Engine Alert: Score Below Target",
                    body=f"Your activity '{activity}' scored {score}, below your target of {st.session_state.target_score}."
                )
            else:
                st.success(f"✅ Score {score} meets your target!")

            st.rerun()

    st.markdown("---")

    # ---------------------------
    # Fetch Records
    # ---------------------------
    records = db.query(BehaviorHistory).filter(
        BehaviorHistory.user_email == st.session_state.user
    ).order_by(BehaviorHistory.timestamp.asc()).all()

    # ---------------------------
    # Target Goal
    # ---------------------------
    st.subheader("🎯 Set Your Target Average Score")
    target = st.number_input(
        "Target Score",
        min_value=0,
        max_value=100,
        value=st.session_state.target_score
    )
    st.session_state.target_score = target
    st.markdown("---")

    # ---------------------------
    # History + Analytics
    # ---------------------------
    if records:
        df = pd.DataFrame([{
            "Timestamp": r.timestamp,
            "Activity": r.activity,
            "Score": r.score,
            "State": r.state
        } for r in records])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df = df.sort_values("Timestamp").set_index("Timestamp")

        # ---------------------------
        # Metrics Cards
        # ---------------------------
        avg_score = round(df["Score"].mean(), 2)
        streak = 0
        max_streak = 0
        last_day = None

        df["MeetsTarget"] = df["Score"] >= st.session_state.target_score
        df = df.sort_index()

        for date, meets in df["MeetsTarget"].items():
            day = date.date()
            if meets:
                if last_day and (day - last_day).days == 1:
                    streak += 1
                else:
                    streak = 1
                max_streak = max(max_streak, streak)
            else:
                streak = 0
            last_day = day

        col1, col2, col3 = st.columns(3)
        col1.metric("Average Score", avg_score)
        col2.metric("Total Activities", len(df))
        col3.metric("Longest Streak (days)", max_streak)

        # ---------------------------
        # Progress Bar
        # ---------------------------
        st.subheader("🎯 Target Progress")
        progress = min(avg_score / st.session_state.target_score, 1.0)
        st.progress(progress)
        st.caption(f"Average Score: {avg_score} / Target: {st.session_state.target_score}")

        # ---------------------------
        # Current Streak
        # ---------------------------
        st.subheader("🔥 Current Streak")
        st.metric("Current Streak (days)", streak)

        # ---------------------------
        # Line Chart (Score Trend)
        # ---------------------------
        st.subheader("📈 Score Trend")
        fig_line = px.line(df, x=df.index, y="Score", title="Score Trend Over Time")
        st.plotly_chart(fig_line, use_container_width=True)
        st.download_button(
            label="📥 Download Line Chart (PNG)",
            data=fig_line.to_image(format="png"),
            file_name="score_trend.png",
            mime="image/png"
        )

        # ---------------------------
        # Weekly Bar Chart
        # ---------------------------
        st.subheader("📅 Weekly Average")
        weekly_avg = df["Score"].resample("W").mean()
        fig_bar = px.bar(weekly_avg.reset_index(), x="Timestamp", y="Score", title="Weekly Average Score")
        st.plotly_chart(fig_bar, use_container_width=True)
        st.download_button(
            label="📥 Download Weekly Bar Chart (PNG)",
            data=fig_bar.to_image(format="png"),
            file_name="weekly_avg.png",
            mime="image/png"
        )

        # ---------------------------
        # Pie Chart (Activity Distribution)
        # ---------------------------
        st.subheader("🥧 Activity Distribution")
        activity_counts = df["Activity"].value_counts().reset_index()
        activity_counts.columns = ["Activity", "Count"]
        fig_pie = px.pie(activity_counts, names="Activity", values="Count", title="Activity Distribution", hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.download_button(
            label="📥 Download Pie Chart (PNG)",
            data=fig_pie.to_image(format="png"),
            file_name="activity_distribution.png",
            mime="image/png"
        )

        # ---------------------------
        # Enhanced CSV Export
        # ---------------------------
        st.subheader("⬇ Export Data (Enhanced)")
        df_export = df.copy()
        df_export["Week"] = df_export.index.isocalendar().week
        weekly_avg_df = df_export.groupby("Week")["Score"].mean().reset_index()
        weekly_avg_df.rename(columns={"Score": "Weekly_Average"}, inplace=True)
        activity_counts_df = df_export["Activity"].value_counts().reset_index()
        activity_counts_df.columns = ["Activity", "Activity_Count"]
        df_export = df_export.merge(weekly_avg_df, on="Week", how="left")
        df_export = df_export.merge(activity_counts_df, on="Activity", how="left")
        csv = df_export.reset_index().to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV with Analytics",
            data=csv,
            file_name="behavior_data_enhanced.csv",
            mime="text/csv",
        )

    else:
        st.info("Add activities to start tracking your behavior.")