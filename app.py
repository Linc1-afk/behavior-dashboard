import streamlit as st
import requests
import time

# =========================
# CONFIG
# =========================
BACKEND_URL =  "https://behavior-backend-gihn.onrender.com"

st.set_page_config(
    page_title="Behavior Monitoring Dashboard",
    layout="wide"
)

# =========================
# TITLE
# =========================
st.title("📊 Behavior Monitoring Dashboard")
st.caption("Live system connected to backend")

# =========================
# BACKEND HEALTH CHECK
# =========================
st.subheader("🔌 Backend Connection Status")

try:
    response = requests.get(f"{BACKEND_URL}/health", timeout=5)

    if response.status_code == 200:
        st.success("✅ Backend connected successfully")
        st.json(response.json())
    else:
        st.error(f"❌ Backend returned error: {response.status_code}")

except Exception as e:
    st.error("❌ Backend not reachable")
    st.write(e)

st.divider()

# =========================
# EVENT SUMMARY
# =========================
st.subheader("📥 Event Summary")

if st.button("🔄 Fetch Latest Events"):
    try:
        events_response = requests.get(f"{BACKEND_URL}/events", timeout=5)

        if events_response.status_code == 200:
            events = events_response.json()

            if len(events) == 0:
                st.warning("No events received yet")
            else:
                st.success(f"Total events received: {len(events)}")
                st.dataframe(events)

        else:
            st.error("Failed to fetch events")

    except Exception as e:
        st.error("Error connecting to backend")
        st.write(e)

st.divider()

# =========================
# SEND TEST EVENT
# =========================
st.subheader("🧪 Send Test Event")

with st.form("send_event"):
    event_type = st.text_input("Event type", value="test_event")
    description = st.text_input("Description", value="This is a test event")
    submit = st.form_submit_button("Send Event")

    if submit:
        payload = {
            "event_type": event_type,
            "description": description
        }

        try:
            send_response = requests.post(
                f"{BACKEND_URL}/event",
                json=payload,
                timeout=5
            )

            if send_response.status_code == 200:
                st.success("✅ Event sent successfully")
                st.json(send_response.json())
            else:
                st.error("❌ Failed to send event")

        except Exception as e:
            st.error("Backend not reachable")
            st.write(e)

st.divider()

# =========================
# AUTO REFRESH OPTION
# =========================
st.subheader("⏱ Auto Refresh")

auto_refresh = st.checkbox("Auto refresh every 10 seconds")

if auto_refresh:
    time.sleep(10)
    st.experimental_rerun()