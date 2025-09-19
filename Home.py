import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import send_email, export_to_excel

st.set_page_config(page_title="Training Feedback Survey", layout="wide")


# Title
st.title("Training Feedback Survey")

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
title_rating = rating_slider("How prepared are agents after Title training?")
title_comments = st.text_area("Comments on Title training")

# --- FDR1 & DLID Section ---
st.header("FDR1 and DLID")
fdr_rating = rating_slider("How confident are agents after FDR1/DLID?")
fdr_comments = st.text_area("Comments on FDR1/DLID training")

# --- Driver Examiner Section ---
st.header("Driver Examiner")
de_rating = rating_slider("Readiness after Driver Examiner training?")
de_comments = st.text_area("Comments on Driver Examiner training")

# --- Compliance Section ---
st.header("Compliance")
compliance_rating = rating_slider("Compliance readiness after training?")
compliance_comments = st.text_area("Comments on Compliance training")

# --- Advanced Section ---
st.header("Advanced Training (VDH, FDR II)")
adv_rating = rating_slider("Advanced training effectiveness?")
adv_comments = st.text_area("Comments on Advanced training")

# --- Onboarding Questions ---
st.header("Onboarding Process")
onboard_desc = st.text_area("Describe how a new hire is onboarded from Day 1 until their first class.")
onboard_support = st.radio("Do you assign a dedicated coach/senior/work leader for new hires?", ["Yes", "No"])
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
