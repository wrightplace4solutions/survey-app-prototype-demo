"""
Training Feedback Survey Page

Collects survey responses for Title Class, FDRI/DLID, Driver examiners,
Compliance, and Advanced VDH FDRII training. Saves results to the master CSV + Excel.
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

# Enhanced styling for engaging yet professional background
st.markdown(
    """
    <style>
        /* Main background with Results page color scheme */
        .stApp {
            background: linear-gradient(135deg, #2F1B14 0%, #8B2635 50%, #2F1B14 100%);
            min-height: 100vh;
            position: relative;
        }
        
        .stApp::before {
            content: '';
            position: fixed;
            top: 20px;
            left: 20px;
            right: 20px;
            bottom: 20px;
            background: 
                linear-gradient(90deg, #8B2635 0px, #8B2635 2px, transparent 2px, transparent 100%),
                linear-gradient(180deg, #8B2635 0px, #8B2635 2px, transparent 2px, transparent 100%);
            border: 3px solid #8B2635;
            border-radius: 8px;
            box-shadow: 
                inset 0 0 20px rgba(139, 38, 53, 0.1),
                0 8px 32px rgba(0,0,0,0.2);
            pointer-events: none;
            z-index: 0;
        }
        
        .stApp > div {
            position: relative;
            z-index: 1;
        }
        
        /* Header styling with granulated glowing effect */
        .main-header {
            background: linear-gradient(135deg, #2F1B14 0%, #8B2635 50%, #2F1B14 100%);
            background-size: 200% 200%;
            animation: gradientShift 4s ease infinite;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 
                0 0 20px rgba(139, 38, 53, 0.4),
                0 0 40px rgba(47, 27, 20, 0.3),
                0 0 60px rgba(139, 38, 53, 0.2),
                0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.3);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 8s linear infinite;
            pointer-events: none;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5em;
            text-shadow: 
                0 0 10px rgba(255,255,255,0.5),
                0 0 20px rgba(255,255,255,0.3),
                0 0 30px rgba(139, 38, 53, 0.4),
                2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 2;
        }
        
        .main-header h3 {
            color: rgba(255,255,255,0.95);
            margin: 10px 0 0 0;
            font-weight: 300;
            text-shadow: 
                0 0 8px rgba(255,255,255,0.3),
                0 0 15px rgba(139, 38, 53, 0.3),
                1px 1px 2px rgba(0,0,0,0.2);
            position: relative;
            z-index: 2;
        }
        
        /* Section containers with colorful backgrounds */
        .section-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .section-title {
            color: white;
            font-size: 1.5em;
            margin-bottom: 1rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        /* Demographics section with Results page theme */
        .demographics-container {
            background: linear-gradient(135deg, #FFFEF7 0%, #F8F6F0 100%);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem;
            box-shadow: 
                0 4px 15px rgba(139, 38, 53, 0.2),
                inset 0 1px 0 rgba(255,255,255,0.8);
            border: 1px solid #8B2635;
            position: relative;
        }
        
        .demographics-container::before {
            content: '';
            position: absolute;
            left: 2rem;
            top: 0;
            bottom: 0;
            width: 1px;
            background: #D8C4C8;
            opacity: 0.7;
        }
        
        .demographics-container h3 {
            color: #2F1B14 !important;
            font-weight: 700;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        }
        
        .demographics-container p, .demographics-container div {
            color: #1A1A1A !important;
            line-height: 1.6;
            font-weight: 600;
        }
        
        /* Content containers with Results page appearance */
        .content-container {
            background: linear-gradient(135deg, #FFFEF7 0%, #F8F6F0 100%);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem;
            box-shadow: 
                0 4px 15px rgba(139, 38, 53, 0.2),
                inset 0 1px 0 rgba(255,255,255,0.8);
            border: 1px solid #8B2635;
            position: relative;
        }
        
        .content-container::before {
            content: '';
            position: absolute;
            left: 2rem;
            top: 0;
            bottom: 0;
            width: 1px;
            background: #D8C4C8;
            opacity: 0.7;
        }
        
        /* Enhanced text visibility with darker colors */
        .content-container h3 {
            color: #2F1B14 !important;
            font-weight: 700;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        }
        
        .content-container p, .content-container div {
            color: #1A1A1A !important;
            line-height: 1.6;
            font-weight: 600;
        }
        
        /* Question containers with varied colors */
        .question-container-1 {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #ff8a65;
        }
        
        .question-container-2 {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #4db6ac;
        }
        
        .question-container-3 {
            background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid #ba68c8;
        }
        
        /* Submit button with clipboard style */
        .stButton > button {
            background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
            color: white !important;
            border: 2px solid #654321;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 
                0 4px 15px rgba(139, 69, 19, 0.3),
                inset 0 1px 0 rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 6px 20px rgba(139, 69, 19, 0.4),
                inset 0 1px 0 rgba(255,255,255,0.3);
            background: linear-gradient(135deg, #A0522D 0%, #8B4513 100%);
        }
        
        /* Custom warning alert styling - comprehensive targeting */
        .stAlert > div {
            border-radius: 10px !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }
        
        /* Target warning alerts specifically */
        .stAlert[data-baseweb="notification"] {
            background: linear-gradient(135deg, #e8f5e8 0%, #f0f4ff 100%) !important;
            border-left: 4px solid #4caf50 !important;
            color: #2e7d32 !important;
        }
        
        .stAlert[data-baseweb="notification"] > div {
            background: transparent !important;
            color: #2e7d32 !important;
        }
        
        /* Alternative targeting for different Streamlit versions */
        div[data-testid="stAlert"] {
            background: linear-gradient(135deg, #e8f5e8 0%, #f0f4ff 100%) !important;
            border-left: 4px solid #4caf50 !important;
            border-radius: 10px !important;
        }
        
        div[data-testid="stAlert"] > div {
            color: #2e7d32 !important;
            background: transparent !important;
        }
        
        /* Target warning text content */
        div[data-testid="stAlert"] div[data-testid="stMarkdownContainer"] p {
            color: #2e7d32 !important;
        }
        
        /* Override any yellow warning styling */
        .stWarning, .st-warning {
            background: linear-gradient(135deg, #e8f5e8 0%, #f0f4ff 100%) !important;
            border-left: 4px solid #4caf50 !important;
            color: #2e7d32 !important;
        }
        
        /* Gradient burgundy section header banners */
        .gradient-header {
            background: linear-gradient(135deg, #8B2635 0%, #2F1B14 50%, #8B2635 100%);
            background-size: 200% 200%;
            animation: gradientText 3s ease infinite;
            color: white;
            text-align: center;
            font-weight: 700;
            font-size: 1.3em;
            margin: 2rem 1.5rem 1rem 1.5rem;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            box-shadow: 
                0 0 15px rgba(139, 38, 53, 0.3),
                0 0 30px rgba(47, 27, 20, 0.2),
                0 4px 15px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.2);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        @keyframes gradientText {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* General text styling for better visibility on burgundy background */
        p, div:not(.stButton) {
            color: #FFFFFF !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        /* Left-align bullet points flush with banner container */
        .aligned-content {
            margin: 0 1.5rem;
            padding: 0;
        }
        
        .aligned-content ul {
            margin: 0;
            padding-left: 1.2rem;
            list-style-position: outside;
        }
        
        .aligned-content li {
            margin-bottom: 0.5rem;
            color: #FFFFFF !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        /* Aligned demographics title */
        .aligned-demographics-title {
            margin: 1rem 1.5rem 0.5rem 1.5rem;
            color: #FFFFFF !important;
            font-size: 1.2em;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        /* Aligned demographics info container */
        .aligned-demographics-info {
            background: rgba(255,255,255,0.7);
            padding: 1rem;
            border-radius: 8px;
            margin: 0 1.5rem 0.5rem 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Survey content alignment */
        .survey-section-content {
            margin: 0 1.5rem 2rem 1.5rem;
            padding: 0;
        }
        
        /* Align all survey form elements */
        .survey-section-content .stRadio,
        .survey-section-content .stTextArea,
        .survey-section-content .stSlider,
        .survey-section-content .stSelectbox {
            margin-bottom: 1.5rem;
        }
        
        /* Survey question text styling */
        .survey-section-content > div > label {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }
        
        /* Radio button and option styling */
        .survey-section-content .stRadio > div > div > div {
            color: #FFFFFF !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Enhanced banner header  
st.markdown(
    """
    <div class="main-header">
        <h1>📊 Training Feedback Survey</h1>
        <h3>Excellence Through Training!</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# Instructions section
st.markdown('<div class="gradient-header">📋 Instructions</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="aligned-content">
        <ul>
            <li>This survey should take about 10 minutes</li>
            <li>Please complete your demographics below to begin the survey</li>
            <li>All responses are confidential and will help improve our training programs</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# Demographics Collection (expandable after CSC selection)
st.markdown('<div class="gradient-header">👤 Demographics</div>', unsafe_allow_html=True)

# Initialize session state
if "demographics_completed" not in st.session_state:
    st.session_state.demographics_completed = False

if not st.session_state.get("demographics_completed"):
    st.markdown('<div class="survey-section-content">', unsafe_allow_html=True)
    st.markdown('<p style="color: #FFFFFF; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">Please select your CSC location to proceed with the survey.</p>', unsafe_allow_html=True)
    
    with st.form("demographics_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p style="color: #FFFFFF; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);"><strong>Name</strong> (Optional)</p>', unsafe_allow_html=True)
            name = st.text_input("Name", value=st.session_state.get("user_name", ""), label_visibility="collapsed")
            st.markdown('<p style="color: #FFFFFF; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);"><strong>Role/Title</strong> (Optional)</p>', unsafe_allow_html=True)
            role = st.text_input("Role/Title", value=st.session_state.get("user_role", ""), label_visibility="collapsed")
        
        with col2:
            st.markdown('<p style="color: #FFFFFF; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);"><strong>CSC Location</strong> (Required)</p>', unsafe_allow_html=True)
            csc = st.selectbox("CSC", [
                "", "Ashland", "Chester", "Chesterfield", "East Henrico", "Emporia", "Ft Gregg Adams", "Hopewell",
                "Kilmarnock", "Petersburg", "Richmond Center (HQ)", "Tappahannock", "West Henrico", "Williamsburg",
                "Other (please specify in email field)"
            ], index=0, label_visibility="collapsed")
            st.markdown('<p style="color: #FFFFFF; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);"><strong>Email</strong> (Optional)</p>', unsafe_allow_html=True)
            email = st.text_input("Email", value=st.session_state.get("user_email", ""), 
                                 label_visibility="collapsed", placeholder="your.email@domain.com")
        
        submitted = st.form_submit_button("💾 Save Demographics & Continue", type="primary", use_container_width=True)
        
        if submitted:
            if not csc:
                st.error("❌ Please select your CSC location.")
            else:
                st.session_state.user_name = name.strip() or "Anonymous"
                st.session_state.user_role = role.strip() or "Not Specified"
                st.session_state.user_csc = csc
                st.session_state.user_email = email.strip()
                st.session_state.demographics_completed = True
                st.success("✅ Demographics saved! Survey unlocked below.")
                st.balloons()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Show saved demographics with proper alignment
    st.markdown('<div class="aligned-demographics-title">✅ Your Information</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="aligned-demographics-info">
            <strong>📛 Name:</strong> {st.session_state.get('user_name', '')}<br>
            <strong>👔 Role/Title:</strong> {st.session_state.get('user_role', '')}<br>
            <strong>🏢 CSC:</strong> {st.session_state.get('user_csc', '')}<br>
            <strong>📧 Email:</strong> {st.session_state.get('user_email', '')}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create aligned button container
    st.markdown('<div style="margin: 0.5rem 1.5rem;">', unsafe_allow_html=True)
    if st.button("🔄 Edit Demographics", key="edit_demographics"):
        st.session_state.demographics_completed = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Only show survey if demographics completed
if not st.session_state.get("demographics_completed"):
    st.stop()

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
    "Advanced_VDH_FDR_II_Skills_Important": [
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
    
    # Create gradient banner for section header
    st.markdown(f'<div class="gradient-header">{section_name} Section</div>', unsafe_allow_html=True)

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
st.markdown('<div class="gradient-header">Onboarding</div>', unsafe_allow_html=True)
st.markdown('<div class="survey-section-content">', unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Survey Experience ----------------
st.markdown('<div class="gradient-header">Feedback on Survey Experience</div>', unsafe_allow_html=True)
st.markdown('<div class="survey-section-content">', unsafe_allow_html=True)

ai_rating = st.slider("1. How did you like the hybrid AI guided survey structure?", 1, 5, 3)
ai_comments = st.text_area("2. Comments on the AI survey experience")
recommend = st.radio("3. Would you recommend this survey app?", ["Yes", "No", "Maybe"])
recommend_why = st.text_area("4. Why or why not?")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Submit ----------------
st.markdown('<div class="survey-section-content">', unsafe_allow_html=True)
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
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown("### 💝 Thank You! From Stephanie & Morgan")
    st.write("Thank you for taking the time to provide your valuable feedback to help us continuously improve our training programs!")
    st.markdown('</div>', unsafe_allow_html=True)
    st.balloons()

st.markdown('</div>', unsafe_allow_html=True)
