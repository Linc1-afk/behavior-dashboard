import streamlit as st
import time

# --------------------------------------------------
# Page configuration (must be first Streamlit call)
# --------------------------------------------------
st.set_page_config(
    page_title="Behavior Insight App",
    page_icon="🧠",
    layout="centered"
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🧠 Behavior Insight Engine")
st.caption("Streamlit app successfully deployed on Render")

st.divider()

# --------------------------------------------------
# App state example
# --------------------------------------------------
if "counter" not in st.session_state:
    st.session_state.counter = 0

# --------------------------------------------------
# Main content
# --------------------------------------------------
st.subheader("Interactive Demo")

st.write(
    "This is a working Streamlit app. "
    "If you can see this page, your deployment is **successful** ✅"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Increase counter"):
        st.session_state.counter += 1

with col2:
    if st.button("🔄 Reset counter"):
        st.session_state.counter = 0

st.success(f"Current counter value: **{st.session_state.counter}**")

# --------------------------------------------------
# Simulated processing section
# --------------------------------------------------
st.subheader("Processing Example")

if st.button("Run analysis"):
    with st.spinner("Analyzing behavior patterns..."):
        time.sleep(2)
    st.success("Analysis complete 🎉")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()
st.caption("Deployed with Streamlit • Hosted on Render")