import streamlit as st

st.title("Welcome to the DMV Training Feedback Survey")

# Placeholder for avatar video embed
st.video("assets/avatar_intro.mp4")

st.write("""
### Instructions
- This survey should take about 10 minutes.
- Answer all sections honestly.
- You can preview responses before submitting.
- Results can be emailed to you if you enter your email.

👉 Scan the QR code below or go to survey.soulwaresystems.com
""")

st.image("assets/survey_qr.png", width=200)
