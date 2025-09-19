import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import send_email, export_to_excel

st.set_page_config(page_title="Training Feedback Survey", layout="wide")

# Company Branding
# st.image("assets/company_logo.png", width=120)  # Add your company logo here
st.markdown("<h3 style='text-align: center; color: #8B2635;'>Excellence Through Training</h3>", unsafe_allow_html=True)

# Set the color scheme using a bit of custom styling
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
        .stSelectbox > div > div {
            background-color: #FEFCF7;
        }
        .stTextInput > div > div > input {
            background-color: #FEFCF7;
        }
        .stTextArea > div > div > textarea {
            background-color: #FEFCF7;
        }
    </style>
    """, unsafe_allow_html=True
)

# Title and Introduction
st.title("📋 Training Feedback Survey")
st.write("Welcome! We'd love your feedback on how our training programs are preparing your team.")

# --- Demographics ---
st.header("Demographics")
name = st.text_input("Your Name *")
role = st.text_input("Your Role/Title *")
csc = st.selectbox("Select your CSC", [
    "Ashland", "Chester", "Chesterfield", "East Henrico", "Emporia", "Ft Gregg Adams",
    "Hopewell", "Kimanock", "Petersburg", "Richmond Center (HQ)", "Tappahannock",
    "West Henrico", "Williamsburg", "Other (please list)"
])
email = st.text_input("Your Email (optional)")

# Helper function for sliders
def rating_slider(label):
    val = st.slider(label, min_value=1, max_value=5, value=5, step=1)
    st.write("👉 5 = Excellent | 1 = Poor")
    return val

# --- Title Class Section ---
st.header("Title Class")
title_rating = rating_slider("Overall effectiveness of Title Class training")
st.text_input("What skills do you find most important for agents coming out of the Title class?")
st.text_input("What specific challenges do they usually face when they return to their roles?")
title_comments = st.text_area("Additional comments on Title training")

# --- FDR1 & DLID Section ---
st.header("FDR1 and DLID (Driver's License & ID)")
fdr_rating = rating_slider("How confident are agents after FDR1/DLID training?")
st.text_input("After completing the FDR1 and DLID courses, what improvements do you expect to see in agents' performance?")
st.text_input("Are there any particular document or ID verification tasks you want them to master?")
fdr_comments = st.text_area("Additional comments on FDR1/DLID training")

# --- Driver Examiner Section ---
st.header("Driver Examiners Course")
de_rating = rating_slider("Readiness after Driver Examiner training")
st.text_input("For the Driver Examiners course, what additional responsibilities should they be prepared to take on?")
de_comments = st.text_area("Additional comments on Driver Examiner training")

# --- Compliance Section ---
st.header("Compliance Course")
compliance_rating = rating_slider("Compliance readiness after training")
st.text_input("After the Compliance course, what compliance-related skills do you need them to have?")
compliance_comments = st.text_area("Additional comments on Compliance training")

# --- Advanced Section ---
st.header("Advanced Training (VDH, FDR II)")
adv_rating = rating_slider("Advanced training effectiveness")
st.text_input("For those who've completed VDH and FDR II, what advanced responsibilities are you looking for them to handle?")
st.text_area("Any other suggestions or focus areas for these advanced levels?")
adv_comments = st.text_area("Additional comments on Advanced training")

# --- Onboarding Questions ---
st.header("Onboarding Process")
onboard_desc = st.text_area("Describe how a new hire is onboarded in your CSC  from Day 1 until their first class.")
onboard_support = st.radio("Are they assigned a dedicated coach/senior/work leader for new hires?", ["Yes", "No"])
onboard_support_desc = st.text_area("If yes, describe how they support new hires.")

# --- Research/AI Feedback ---
st.header("Feedback on Survey Experience")
ai_feedback = st.slider("How did you like the hybrid AI guided survey structure?", min_value=1, max_value=5, value=5, step=1)
st.write("👉 5 = Loved it | 1 = Didn't like at all")
ai_comments = st.text_area("Comments on the AI survey experience")
recommend = st.radio("Would you recommend this survey app for colleagues/departments?", ["Yes", "No", "Maybe"])
recommend_comments = st.text_area("Why or why not?")

# --- Submission ---
if st.button("Submit Survey"):
    st.success("✅ Your responses have been submitted! 🎉")
    st.balloons()
