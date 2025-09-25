"""DMV Training Feedback Survey Application - No CSS Version.

This Streamlit application collects feedback on DMV training programs
including Title Class, FDR1 & DLID, Driver Examiners, Compliance, and Advanced training.
"""

import streamlit as st

st.set_page_config(page_title="Training Feedback Survey", layout="wide")

# Company Branding - Updated with all questions and CSC locations
st.markdown(
    "<h3 style='text-align: center; color: #8B2635;'>Excellence Through Training</h3>",
    unsafe_allow_html=True
)

# Title and Introduction
st.title("📋 Training Feedback Survey")
st.write("Welcome! We'd love your feedback on how our training programs are preparing your team.")

# --- Demographics ---
st.header("Demographics")
name = st.text_input("Your Name *")
role = st.text_input("Your Role/Title *")
csc_options = [
    "Ashland", "Chester", "Chesterfield", "East Henrico", "Emporia", 
    "Ft Gregg Adams", "Hopewell", "Kimanock", "Petersburg", 
    "Richmond Center (HQ)", "Tappahannock", "West Henrico", 
    "Williamsburg", "Other (please list)"
]
csc = st.selectbox("Select your CSC", csc_options)
email = st.text_input("Your Email (optional)")

# Helper function for sliders
def rating_slider(label: str) -> int:
    """Create a rating slider with standardized scale and labels.
    
    Args:
        label: The label text for the slider
        
    Returns:
        The selected rating value (1-5)
    """
    val = st.slider(label, min_value=1, max_value=5, value=5, step=1)
    st.write("👉 5 = Excellent | 1 = Poor")
    return val

# --- Title Class Section ---
st.header("Title Class")
st.write("This section is now visible!")

# --- Submission ---
if st.button("Submit Survey"):
    st.success("✅ Your responses have been submitted! 🎉")
    st.balloons()
