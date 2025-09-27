"""
Training Feedback Survey Page

Collects survey responses for Title Class, FDR1 & DLID, Driver Examiners,
Compliance, and Advanced training. Saves results to the master CSV + Excel.
"""

import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Master files (everything writes here)
CSV_FILE = "Updated_Training_Feedback_Survey_Template.csv"
EXCEL_FILE = "Updated_Training_Feedback_Survey_Template.xlsx"

# Page settings
st.set_page_config(page_title="Training Feedback Survey", layout="wide")

# Unified header
st.markdown(
    """
    <h1 style='text-align: center; color: #2F1B14;'>Training Feedback Survey</h1>
    <h3 style='text-align: center; color: #8B2635;'>Excellence Through Training</h3>
    """,
    unsafe_allow_html=True,
)

# Check demographics
if not st.session_state.get("demographics_completed"):
    st.warning("⚠️ No demographics found. Please complete the Intro page first.")
    st.stop()

# Show demographics at the top
st.header("Demographics")
st.info(
    f"**Name:** {st.session_state.get('user_name', '')}\n\n"
    f"**Role/Title:** {st.session_state.get('user_role', '')}\n\n"
    f"**CSC:** {st.session_state.get('user_csc', '')}\n\n"
    f"**Email:** {st.session_state.get('user_email', '')}"
)

# --- Skills options for each section ---
SECTION_SKILLS = {
    "Title_Class_Skills_Important": [
        "Accuracy in data entry",
        "Understanding title documentation",
        "Customer communication",
        "Problem-solving with difficult cases",
        "All of the above",
    ],
    "FDR1_and_DLID_Skills_Important": [
        "ID & document verification accuracy",
        "System navigation speed",
        "Fraud detection basics",
        "Customer communication",
        "All of the above",
    ],
    "Driver_Examiner_Skills_Important": [
        "Road test protocol adherence",
        "Safety & vehicle inspection",
        "Customer instruction & communication",
        "Documentation accuracy",
        "All of the above",
    ],
    "Compliance_Skills_Important": [
        "Regulation & policy knowledge",
        "Exception handling & escalation",
        "Audit trail documentation",
        "Data privacy & confidentiality",
        "All of the above",
    ],
    "Advanced_VDH and FDR_II_Skills_Important": [
        "Complex case resolution",
        "Document verification",
        "Data analysis & reporting",
        "Mentoring & leadership",
        "All of the above",
    ],
}

# ---------------- Collect Survey Responses ----------------
responses = {}

for section_key, skills in SECTION_SKILLS.items():
    section_name = section_key.replace("_Skills_Important", "").replace("_", " ")
    st.header(f"{section_name} Section")

    # 1. Skills (multiple choice)
    responses[section_key] = st.radio(
        f"1. What skills do you find most important for agents coming out of {section_name} training?",
        skills,
        key=f"{section_key}_skills",
    )

    # 2. Challenges (open text)
    responses[section_name + "_Challenges"] = st.text_area(
        f"2. What specific challenges do they usually face when they return to their roles?",
        key=f"{section_key}_challenges",
    )

    # 3. Confidence (slider)
    responses[section_name + "_Confidence"] = st.slider(
        f"3. How confident are agents after completing the {section_name} class?",
        1, 10, 5,
        key=f"{section_key}_confidence",
    )

    # 4. Expected Improvements (open text)
    responses[section_name + "_Expected_Improvements"] = st.text_area(
        f"4. After completing the {section_name} training, what improvements do you expect to see in agents’ performance?",
        key=f"{section_key}_improvements",
    )

    # 5. Audit Issues (Yes/No + details)
    audit = st.radio(
        f"5. Do agents in your center experience a high number of audit issues/errors from {section_name} transactions?",
        ["Yes", "No"],
        key=f"{section_key}_audit",
    )
    audit_details = ""
    if audit == "Yes":
        audit_details = st.text_area(
            "If yes: Please describe the most common errors.",
            key=f"{section_key}_audit_details",
        )
    responses[section_name + "_Audit_Issues"] = f"{audit} - {audit_details}"

# ---------------- Onboarding ----------------
st.header("Onboarding")
onboarding_desc = st.text_area(
    "1. Describe how a new hire is onboarded in your CSC."
)
onboarding_coach = st.radio(
    "2. Are they assigned a dedicated coach/senior/work leader for shadowing, coaching and development?",
    ["Yes", "No"],
)
onboarding_support = ""
if onboarding_coach == "Yes":
    onboarding_support = st.text_area("If yes: Please describe how they support new hires.")

# New questions about e-Learning and OJT
elearning_time = st.radio(
    "3. Are new hires provided adequate dedicated time to complete their required e-Learning modules?",
    ["Yes", "No", "Sometimes"],
)
elearning_details = ""
if elearning_time in ["No", "Sometimes"]:
    elearning_details = st.text_area("If no or sometimes: Please explain the challenges or barriers.")

ojt_assessment = st.radio(
    "4. Do new hires successfully complete and pass their Basic Skills OJT guide assessment before being scheduled for Title class?",
    ["Always", "Usually", "Sometimes", "Rarely", "Never"],
)
ojt_details = ""
if ojt_assessment in ["Sometimes", "Rarely", "Never"]:
    ojt_details = st.text_area("If not consistently: What factors prevent successful completion?")

# ---------------- Survey Experience ----------------
st.header("Feedback on Survey Experience")
ai_rating = st.slider("1. How did you like the hybrid AI guided survey structure?", 1, 5, 3)
ai_comments = st.text_area("2. Comments on the AI survey experience")
recommend = st.radio("3. Would you recommend this survey app?", ["Yes", "No", "Maybe"])
recommend_why = st.text_area("4. Why or why not?")

# ---------------- Submit ----------------
if st.button("Submit Survey"):
    record = {
        "SubmissionID": f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{st.session_state.get('user_name', '')}",
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    record.update({
        "User_Name": st.session_state.get('user_name', ''),
        "User_Role": st.session_state.get('user_role', ''),
        "CSC": st.session_state.get('user_csc', ''),
        "User_Email": st.session_state.get('user_email', '')
    })
    record.update(responses)
    record.update({
        "Onboarding_Process_Description": onboarding_desc,
        "Onboarding_Assigned_Coach": onboarding_coach,
        "Onboarding_Coach_Support": onboarding_support,
        "ELearning_Dedicated_Time": elearning_time,
        "ELearning_Time_Details": elearning_details,
        "OJT_Assessment_Success": ojt_assessment,
        "OJT_Assessment_Details": ojt_details,
        "AI_Survey_Experience_Rating": ai_rating,
        "AI_Survey_Experience_Comments": ai_comments,
        "Recommend_Survey_App": recommend,
        "Why_Recommend_or_Not": recommend_why,
    })

    # Save to CSV
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    # Save to Excel
    if os.path.exists(EXCEL_FILE):
        df_excel = pd.read_excel(EXCEL_FILE)
    else:
        df_excel = pd.DataFrame()
    df_excel = pd.concat([df_excel, pd.DataFrame([record])], ignore_index=True)
    df_excel.to_excel(EXCEL_FILE, index=False)

    st.success("✅ Thank you! Your survey response has been submitted.")
    st.balloons()
