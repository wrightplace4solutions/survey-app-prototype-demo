"""
Training Feedback Survey Application.

This Streamlit application collects feedback on training programs
including Title Class, FDR1 & DLID, Driver Examiners, Compliance, and Advanced training.
"""

# Note: Streamlit apps commonly use a PascalCase filename like "Home.py" so we
# suppress the Pylint module naming warning for this file only, and allow long
# lines for inline HTML/CSS strings used by Streamlit.
# pylint: disable=invalid-name,line-too-long

import os
from datetime import datetime

import pandas as pd
import streamlit as st

from utils import export_to_excel

st.set_page_config(page_title="Training Feedback Survey", layout="wide")

# Company Branding - Updated with all questions and CSC locations
# st.image("assets/company_logo.png", width=120)  # Add your company logo here
st.markdown(
    "<h3 style='text-align: center; color: #8B2635;'>Excellence Through Training</h3>",
    unsafe_allow_html=True
)

# Set the color scheme with improved styling for better visibility
st.markdown(
    """
    <style>
        body { 
            color: #2F1B14; 
            background-color: #FAF7F0; 
        }
        .stApp { 
            color: #2F1B14; 
            background-color: #FEFCF7; 
        }
        h1, h2, h3 { 
            color: #8B2635; 
            margin-bottom: 1rem;
            margin-top: 1.5rem;
        }
        .stSelectbox > div > div { 
            background-color: #FEFCF7; 
        }
        .stTextInput > div > div > input { 
            background-color: #FEFCF7;
            padding: 0.5rem;
        }
        .stTextArea > div > div > textarea { 
            background-color: #FEFCF7;
            padding: 0.5rem;
            min-height: 80px;
        }
        .rank-warning { 
            color: #8B2635; 
            font-weight: 600; 
        }
        /* Reduce spacing between elements */
        .element-container {
            margin-bottom: 0.5rem;
        }
        /* Improve slider styling */
        .stSlider > div > div {
            padding: 0.25rem 0;
        }
        /* Make rating labels more compact */
        .slider-label {
            font-size: 0.9rem;
            margin-bottom: 0.25rem;
        }
        /* Compact form sections */
        .survey-section {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #8B2635;
        }
        /* Access denied message */
        .access-denied {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True
)

# ----- Helpers -----
def rating_slider(label: str) -> int:
    """Create a rating slider with a 1-5 scale.
    
    Args:
        label: The label text for the slider
        
    Returns:
        int: The selected rating value (1-5)
    """
    st.markdown(f'<div class="slider-label">{label}</div>', unsafe_allow_html=True)
    val = st.slider("", min_value=1, max_value=5, value=3, step=1, label_visibility="collapsed")
    st.caption("👉 5 = Excellent | 1 = Poor")
    return val

def skill_select_with_ranking(prompt: str, options: list[str]) -> tuple[str, dict[str, int]]:
    """Render a selectbox with options plus 'All of the above'.
    If 'All of the above' is selected, show per-item ranking number_inputs.
    Returns (selected_option, rankings_dict). rankings_dict is empty unless All of the above is chosen.
    """
    base_opts = [o for o in options if o != "All of the above"]
    # Ensure All of the above at end
    opts = base_opts + (["All of the above"] if "All of the above" not in options else [])
    chosen = st.selectbox(prompt, opts, index=0)
    rankings: dict[str, int] = {}
    if chosen == "All of the above":
        st.write(
            "Please rank these skills in order of importance "
            f"(1 = most important, {len(base_opts)} = least important):"
        )
        cols = st.columns(min(4, len(base_opts)))
        # Create a unique key based on the prompt
        section_key = prompt.replace(" ", "_").replace("?", "").replace(".", "")[:20]
        for i, skill in enumerate(base_opts):
            with cols[i % len(cols)]:
                rankings[skill] = st.number_input(
                    f"Rank – {skill}",
                    min_value=1, max_value=len(base_opts), step=1,
                    key=f"rank_{section_key}_{i}_{skill}"
                )
        # Soft validation
        vals = list(rankings.values())
        if len(vals) != len(base_opts):
            st.caption("Fill a rank for each skill.")
        elif len(set(vals)) != len(vals):
            st.markdown(
                "<div class='rank-warning'>⚠️ Each rank must be unique (no ties). "
                "Please adjust.</div>",
                unsafe_allow_html=True
            )
    return chosen, rankings

st.title("📋 Training Feedback Survey")

# Check if demographics are completed
if not st.session_state.get('demographics_completed', False):
    st.markdown(
        '<div class="access-denied">'
        '<h3>⚠️ Demographics Required</h3>'
        '<p>Please complete the demographics section in the <strong>Intro</strong> page before accessing this survey.</p>'
        '<p>👈 Use the sidebar navigation to go to the Intro page first.</p>'
        '</div>', 
        unsafe_allow_html=True
    )
    st.stop()

# Welcome message with user info
st.success(f"Welcome back, **{st.session_state.get('user_name', 'User')}**!")
st.write(
    "Thank you for completing the demographics. "
    "Please provide your feedback on how our training programs are preparing your team."
)

# Get demographics from session state
responses = {
    "name": st.session_state.get('user_name', ''),
    "role": st.session_state.get('user_role', ''),
    "csc": st.session_state.get('user_csc', ''),
    "email": st.session_state.get('user_email', ''),
}

# --- Title Class Section ---
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.subheader("📚 Title Class")
responses["title_overall"] = str(rating_slider("Overall effectiveness of Title Class training"))

_title_choice, _title_ranks = skill_select_with_ranking(
    "1. What skills do you find most important for agents coming out of the Title class?",
    [
        "Accuracy in data entry",
        "Understanding title documentation",
        "Customer communication",
        "Problem-solving with difficult cases",
        "All of the above",
    ],
)
responses["title_skill_choice"] = _title_choice
responses.update({f"title_rank_{k}": str(v) for k, v in _title_ranks.items()})

responses["title_challenges"] = st.text_input(
    "2. What specific challenges do they usually face when they return to their roles?",
    key="title_challenges"
)
responses["title_comments"] = st.text_area(
    "Additional comments on Title training",
    key="title_comments",
    height=100
)
st.markdown('</div>', unsafe_allow_html=True)

# --- FDR1 & DLID Section ---
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.subheader("🆔 FDR1 and DLID (Driver's License & ID)")
responses["fdr_overall"] = str(rating_slider("How confident are agents after FDR1/DLID training?"))

_fdr_choice, _fdr_ranks = skill_select_with_ranking(
    "1. Which skills are most important post-FDR1/DLID?",
    [
        "ID & document verification accuracy",
        "System navigation speed",
        "Fraud detection basics",
        "Customer communication",
        "All of the above",
    ],
)
responses["fdr_skill_choice"] = _fdr_choice
responses.update({f"fdr_rank_{k}": str(v) for k, v in _fdr_ranks.items()})

responses["fdr_expectations"] = st.text_input(
    "2. After completing the FDR1 and DLID courses, what improvements do you expect to see in agents' performance?",
    key="fdr_expectations"
)
responses["fdr_tasks_mastery"] = st.text_input(
    "3. Are there any particular document or ID verification tasks you want them to master?",
    key="fdr_tasks"
)
responses["fdr_comments"] = st.text_area(
    "Additional comments on FDR1/DLID training",
    key="fdr_comments",
    height=100
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Driver Examiner Section ---
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.subheader("🚗 Driver Examiners Course")
responses["de_overall"] = str(rating_slider("Readiness after Driver Examiner training"))

_de_choice, _de_ranks = skill_select_with_ranking(
    "1. What skills matter most for Driver Examiners?",
    [
        "Road test protocol adherence",
        "Safety & vehicle inspection",
        "Customer instruction & communication",
        "Documentation accuracy",
        "All of the above",
    ],
)
responses["de_skill_choice"] = _de_choice
responses.update({f"de_rank_{k}": str(v) for k, v in _de_ranks.items()})

responses["de_responsibilities"] = st.text_input(
    "2. For the Driver Examiners course, what additional responsibilities should they be prepared to take on?",
    key="de_responsibilities"
)
responses["de_comments"] = st.text_area(
    "Additional comments on Driver Examiner training",
    key="de_comments", 
    height=100
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Compliance Section ---
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.subheader("📋 Compliance Course")
responses["compliance_overall"] = str(rating_slider("Compliance readiness after training"))

_comp_choice, _comp_ranks = skill_select_with_ranking(
    "1. Which compliance-related skills are most important?",
    [
        "Regulation & policy knowledge",
        "Exception handling & escalation",
        "Audit trail documentation",
        "Data privacy & confidentiality",
        "All of the above",
    ],
)
responses["compliance_skill_choice"] = _comp_choice
responses.update({f"compliance_rank_{k}": str(v) for k, v in _comp_ranks.items()})

responses["compliance_needed"] = st.text_input(
    "2. After the Compliance course, what compliance-related skills do you need them to have?",
    key="compliance_needed"
)
responses["compliance_comments"] = st.text_area(
    "Additional comments on Compliance training",
    key="compliance_comments",
    height=100
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Advanced Section ---
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.subheader("🎯 Advanced Training (VDH, FDR II)")
responses["advanced_overall"] = str(rating_slider("Advanced training effectiveness"))

_adv_choice, _adv_ranks = skill_select_with_ranking(
    "1. Which advanced skills are most important?",
    [
        "Complex case resolution",
        "Inter-agency coordination",
        "Data analysis & reporting",
        "Mentoring & leadership",
        "All of the above",
    ],
)
responses["advanced_skill_choice"] = _adv_choice
responses.update({f"advanced_rank_{k}": str(v) for k, v in _adv_ranks.items()})

responses["advanced_responsibilities"] = st.text_input(
    "2. For those who've completed VDH and FDR II, what advanced responsibilities are you looking for them to handle?",
    key="advanced_responsibilities"
)
responses["advanced_focus"] = st.text_area(
    "3. Any other suggestions or focus areas for these advanced levels?",
    key="advanced_focus",
    height=100
)
responses["advanced_comments"] = st.text_area(
    "Additional comments on Advanced training",
    key="advanced_comments",
    height=100
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Onboarding Questions ---
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.subheader("🚀 Onboarding Process")

responses["onboard_desc"] = st.text_area(
    "Describe how a new hire is onboarded in your CSC from Day 1 until their first class.",
    key="onboard_desc",
    height=120
)
responses["onboard_support"] = st.radio(
    "Are they assigned a dedicated coach/senior/work leader for new hires?", 
    ["Yes", "No"],
    key="onboard_support"
)
responses["onboard_support_desc"] = st.text_area(
    "If yes, describe how they support new hires.",
    key="onboard_support_desc",
    height=100
)
st.markdown('</div>', unsafe_allow_html=True)

# --- Feedback on Survey Experience ---
st.markdown('<div class="survey-section">', unsafe_allow_html=True)
st.subheader("💭 Feedback on Survey Experience")

responses["ai_feedback"] = str(st.slider(
    "How did you like the hybrid AI guided survey structure?", 
    min_value=1, max_value=5, value=3, step=1,
    key="ai_feedback"
))
st.caption("👉 5 = Loved it | 1 = Didn't like at all")

responses["ai_comments"] = st.text_area(
    "Comments on the AI survey experience",
    key="ai_comments",
    height=100
)
responses["recommend"] = st.radio(
    "Would you recommend this survey app for colleagues/departments?", 
    ["Yes", "No", "Maybe"],
    key="recommend"
)
responses["recommend_comments"] = st.text_area(
    "Why or why not?",
    key="recommend_comments",
    height=100
)
st.markdown('</div>', unsafe_allow_html=True)

def _handle_submission(responses_map: dict[str, str]) -> None:
    """Persist the submission to Excel and CSV, then notify the user."""
    # Timestamped copy for persistence
    responses_copy = {
        **responses_map,
        "submitted_at": datetime.now().isoformat(timespec="seconds"),
    }

    # Persist to Excel via helper (one-row per submission)
    try:
        export_to_excel(responses_copy)
        excel_ok = True
    except (IOError, OSError, PermissionError) as exc:
        excel_ok = False
        st.error(f"Excel export failed: {exc}")

    # Persist to CSV (append; create headers if file doesn't exist)
    try:
        csv_path = "survey_data.csv"
        df = pd.DataFrame([responses_copy])
        df.to_csv(
            csv_path,
            mode="a",
            header=not os.path.exists(csv_path),
            index=False,
            encoding="utf-8",
        )
        csv_ok = True
    except (IOError, OSError, PermissionError) as exc:
        csv_ok = False
        st.error(f"CSV save failed: {exc}")

    if excel_ok or csv_ok:
        st.success("✅ Your responses have been submitted and saved! 🎉")
        st.balloons()
    else:
        st.warning(
            "Your response was received but could not be saved. "
            "Please try again or contact support."
        )


# --- Submission ---
st.markdown("---")
st.subheader("📤 Submit Your Responses")
st.write("Please review your responses above before submitting.")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🚀 Submit Survey", type="primary", use_container_width=True):
        # Validate required fields - name is optional, but role and csc are required
        if not all([responses["role"], responses["csc"]]):
            st.error("Please ensure Role/Title and CSC are filled in the demographics!")
        else:
            _handle_submission(responses)
