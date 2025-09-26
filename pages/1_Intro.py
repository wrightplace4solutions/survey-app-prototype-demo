"""Intro/landing page visuals and instructions for the survey app."""
# pylint: disable=invalid-name

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
        .demographics-form {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border: 2px solid #8B2635;
        }
        .required-field {
            color: #8B2635;
            font-weight: bold;
        }
        /* Fix form field visibility */
        .stTextInput > div > div > input {
            background-color: white !important;
            color: #2F1B14 !important;
            border: 1px solid #ccc !important;
        }
        .stSelectbox > div > div {
            background-color: white !important;
            color: #2F1B14 !important;
        }
        .stSelectbox label {
            color: #2F1B14 !important;
            font-weight: 500;
        }
        .stTextInput label {
            color: #2F1B14 !important;
            font-weight: 500;
        }
        /* Ensure dropdown options are visible */
        .stSelectbox [data-baseweb="select"] {
            background-color: white !important;
        }
        .stSelectbox [data-baseweb="select"] > div {
            background-color: white !important;
            color: #2F1B14 !important;
        }
        /* Fix message box text visibility */
        .stAlert {
            color: #2F1B14 !important;
        }
        .stAlert > div {
            color: #2F1B14 !important;
        }
        .stSuccess {
            background-color: #d4edda !important;
            color: #155724 !important;
        }
        .stWarning {
            background-color: #fff3cd !important;
            color: #856404 !important;
        }
        .stInfo {
            background-color: #d1ecf1 !important;
            color: #0c5460 !important;
        }
        .stError {
            background-color: #f8d7da !important;
            color: #721c24 !important;
        }
    </style>
    """, unsafe_allow_html=True
)

st.title("Welcome to the Training Feedback Survey")

# Only show video section if file exists
import os
if os.path.exists("assets/avatar_intro.mp4"):
    try:
        st.video("assets/avatar_intro.mp4")
    except Exception:
        pass  # Don't show anything if video fails to load

st.write("""
### Instructions
- This survey should take about 10 minutes.
- Answer all sections honestly.
- Complete the demographics section below to proceed to the survey.
- Results can be emailed to you if you enter your email.

👉 Scan the QR code below or go to survey.soulwaresystems.com
""")

# Only show QR code if file exists
if os.path.exists("assets/survey_qr.png"):
    try:
        st.image("assets/survey_qr.png", width=200)
    except Exception:
        pass  # Don't show anything if image fails to load

# Demographics Section - Required before accessing survey
st.markdown("---")
st.markdown('<div class="demographics-form">', unsafe_allow_html=True)
st.header("📝 Demographics")
st.markdown('<p class="required-field">Please select your CSC location below to proceed to the survey.</p>', unsafe_allow_html=True)

# Initialize session state for demographics
if 'demographics_completed' not in st.session_state:
    st.session_state.demographics_completed = False

# Demographics form
with st.form("demographics_form"):
    st.markdown("### Please fill out all required information:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Name** (Optional)")
        name = st.text_input("Enter your full name", value=st.session_state.get('user_name', ''), label_visibility="collapsed", placeholder="Your Name (Optional)")
        
        st.markdown("**Role/Title** (Optional)")
        role = st.text_input("Enter your role or job title", value=st.session_state.get('user_role', ''), label_visibility="collapsed", placeholder="Your Role/Title (Optional)")
    
    with col2:
        st.markdown("**CSC Location** (Required)")
        csc = st.selectbox(
            "Select your Customer Service Center",
            [
                "",  # Empty default option
                "Ashland",
                "Chester", 
                "Chesterfield",
                "East Henrico",
                "Emporia",
                "Ft Gregg Adams",
                "Hopewell",
                "Kilmarnock",
                "Petersburg",
                "Richmond Center (HQ)",
                "Tappahannock",
                "West Henrico",
                "Williamsburg",
                "Other (please specify in email field)",
            ],
            index=0 if 'user_csc' not in st.session_state else (
                [
                    "",
                    "Ashland",
                    "Chester", 
                    "Chesterfield",
                    "East Henrico",
                    "Emporia",
                    "Ft Gregg Adams",
                    "Hopewell",
                    "Kilmarnock",
                    "Petersburg",
                    "Richmond Center (HQ)",
                    "Tappahannock",
                    "West Henrico",
                    "Williamsburg",
                    "Other (please specify in email field)",
                ].index(st.session_state.get('user_csc', '')) if st.session_state.get('user_csc', '') in [
                    "",
                    "Ashland",
                    "Chester", 
                    "Chesterfield",
                    "East Henrico",
                    "Emporia",
                    "Ft Gregg Adams",
                    "Hopewell",
                    "Kilmarnock",
                    "Petersburg",
                    "Richmond Center (HQ)",
                    "Tappahannock",
                    "West Henrico",
                    "Williamsburg",
                    "Other (please specify in email field)",
                ] else 0
            ),
            label_visibility="collapsed"
        )
        
        st.markdown("**Email** (Optional)")
        email = st.text_input("Enter your email address", value=st.session_state.get('user_email', ''), label_visibility="collapsed", placeholder="your.email@domain.com")
    
    st.markdown("---")
    submitted = st.form_submit_button("💾 Save Demographics & Continue", type="primary", use_container_width=True)
    
    if submitted:
        # Validation - Only CSC is required now
        if not csc or csc == "":
            st.error("❌ Please select your CSC location from the dropdown!")
        else:
            # Save to session state - use defaults if fields not provided
            st.session_state.user_name = name.strip() if name.strip() else "Anonymous"
            st.session_state.user_role = role.strip() if role.strip() else "Not Specified"
            st.session_state.user_csc = csc
            st.session_state.user_email = email.strip()
            st.session_state.demographics_completed = True
            
            st.success("✅ Demographics saved successfully! You can now proceed to the Survey page.")
            st.balloons()
            st.info("👈 Use the sidebar navigation to go to the **Survey** page.")

# Show status
if st.session_state.get('demographics_completed', False):
    st.success("✅ Demographics completed! You can proceed to the Survey page.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Name:** {st.session_state.get('user_name', '')}")
    with col2:
        st.info(f"**Role:** {st.session_state.get('user_role', '')}")
    with col3:
        st.info(f"**CSC:** {st.session_state.get('user_csc', '')}")
    
    if st.session_state.get('user_email', ''):
        st.info(f"**Email:** {st.session_state.get('user_email', '')}")
        
    st.markdown("👈 **Next Step:** Use the sidebar to navigate to the **Survey** page to begin!")
else:
    st.warning("⚠️ Please select your CSC location above before accessing the survey.")
    st.info("💡 **Tip:** Only CSC selection is required. Name, Role/Title and Email are optional.")

st.markdown('</div>', unsafe_allow_html=True)
