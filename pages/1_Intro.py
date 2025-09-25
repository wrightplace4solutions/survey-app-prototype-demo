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
    </style>
    """, unsafe_allow_html=True
)

st.title("Welcome to the Training Feedback Survey")

# Placeholder for avatar video embed
try:
    st.video("assets/avatar_intro.mp4")
except Exception:
    st.info("Introduction video not available - you can still proceed with the survey!")

st.write("""
### Instructions
- This survey should take about 10 minutes.
- Answer all sections honestly.
- Complete the demographics section below to proceed to the survey.
- Results can be emailed to you if you enter your email.

👉 Scan the QR code below or go to survey.soulwaresystems.com
""")

# Try to display QR image, handle gracefully if not found
try:
    st.image("assets/survey_qr.png", width=200)
except Exception:
    st.info("QR code image not available - you can still proceed with the survey!")

# Demographics Section - Required before accessing survey
st.markdown("---")
st.markdown('<div class="demographics-form">', unsafe_allow_html=True)
st.header("📝 Demographics (Required)")
st.markdown('<p class="required-field">Please complete all required fields before proceeding to the survey.</p>', unsafe_allow_html=True)

# Initialize session state for demographics
if 'demographics_completed' not in st.session_state:
    st.session_state.demographics_completed = False

# Demographics form
with st.form("demographics_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name *", value=st.session_state.get('user_name', ''))
        role = st.text_input("Your Role/Title *", value=st.session_state.get('user_role', ''))
    
    with col2:
        csc = st.selectbox(
            "Select your CSC *",
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
                "Other (please list)",
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
                    "Other (please list)",
                ].index(st.session_state.get('user_csc', ''))
            )
        )
        email = st.text_input("Your Email (optional)", value=st.session_state.get('user_email', ''))
    
    submitted = st.form_submit_button("Save Demographics & Proceed to Survey")
    
    if submitted:
        # Validation
        if not name.strip():
            st.error("Name is required!")
        elif not role.strip():
            st.error("Role/Title is required!")
        elif not csc or csc == "":
            st.error("Please select your CSC!")
        else:
            # Save to session state
            st.session_state.user_name = name.strip()
            st.session_state.user_role = role.strip() 
            st.session_state.user_csc = csc
            st.session_state.user_email = email.strip()
            st.session_state.demographics_completed = True
            
            st.success("✅ Demographics saved! You can now proceed to the Survey page.")
            st.balloons()

# Show status
if st.session_state.get('demographics_completed', False):
    st.success("✅ Demographics completed! You can proceed to the Survey page.")
    st.info(f"**Name:** {st.session_state.get('user_name', '')}\n\n**Role:** {st.session_state.get('user_role', '')}\n\n**CSC:** {st.session_state.get('user_csc', '')}")
else:
    st.warning("⚠️ Please complete the demographics section above before accessing the survey.")

st.markdown('</div>', unsafe_allow_html=True)
