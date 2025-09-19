import streamlit as st

# Set consistent styling with main app
st.markdown(
    """
    <style>
        body {
            color: #2F1B14;
            background-color: #FAF7F0; /* cream background */
        }
        .stApp {
            color: #2F1B14;
            background-color: #FEFCF7; /* cream white content background */
        }
        h1, h2, h3 {
            color: #8B2635; /* burgundy for headers */
        }
    </style>
    """, unsafe_allow_html=True
)

st.title("Welcome to the Training Feedback Survey")

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
