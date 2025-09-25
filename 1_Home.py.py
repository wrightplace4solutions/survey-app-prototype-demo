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

# Set the color scheme using safer custom styling
st.markdown(
    """
    <style>
        body { color: #2F1B14; background-color: #FAF7F0; }
        .stApp { color: #2F1B14; background-color: #FEFCF7; }
        h1, h2, h3 { color: #8B2635; }
        .stSelectbox > div > div { background-color: #FEFCF7; }
        .stTextInput > div > div > input { background-color: #FEFCF7; }
        .stTextArea > div > div > textarea { background-color: #FEFCF7; }
        .rank-warning { color: #8B2635; font-weight: 600; }
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
    val = st.slider(label, min_value=1, max_value=5, value=5, step=1)
    st.write("👉 5 = Excellent | 1 = Poor")
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
        # Create a section-specific key so widgets remain unique
        section_key = st.session_state.get('section_key', 'section')
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
st.write(
    "Thank you for taking the time to complete this survey. "
    "We'd love your feedback on how our training programs are preparing your team."
)

# --- Demographics ---
st.header("Demographics")
name = st.text_input("Your Name *")
role = st.text_input("Your Role/Title *")
csc = st.selectbox(
    "Select your CSC",
    [
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
)
email = st.text_input("Your Email (optional)")

# Prepare a container to accumulate responses (kept in-memory; integrate with persistence as needed)
responses = {
    "name": name,
    "role": role,
    "csc": csc,
    "email": email,
}

# --- Title Class Section ---
st.header("Title Class")
st.session_state["section_key"] = "title"
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
responses["title_challenges"] = st.text_input("2. What specific challenges do they usually face when they return to their roles?")
responses["title_comments"] = st.text_area("Additional comments on Title training")

# --- FDR1 & DLID Section ---
st.header("FDR1 and DLID (Driver's License & ID)")
st.session_state["section_key"] = "fdr1_dlid"
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
responses["fdr_expectations"] = st.text_input("2. After completing the FDR1 and DLID courses, what improvements do you expect to see in agents' performance?")
responses["fdr_tasks_mastery"] = st.text_input("3. Are there any particular document or ID verification tasks you want them to master?")
responses["fdr_comments"] = st.text_area("Additional comments on FDR1/DLID training")

# --- Driver Examiner Section ---
st.header("Driver Examiners Course")
st.session_state["section_key"] = "de"
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
responses["de_responsibilities"] = st.text_input("2. For the Driver Examiners course, what additional responsibilities should they be prepared to take on?")
responses["de_comments"] = st.text_area("Additional comments on Driver Examiner training")

# --- Compliance Section ---
st.header("Compliance Course")
st.session_state["section_key"] = "compliance"
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
responses["compliance_needed"] = st.text_input("2. After the Compliance course, what compliance-related skills do you need them to have?")
responses["compliance_comments"] = st.text_area("Additional comments on Compliance training")

# --- Advanced Section ---
st.header("Advanced Training (VDH, FDR II)")
st.session_state["section_key"] = "advanced"
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
responses["advanced_responsibilities"] = st.text_input("2. For those who've completed VDH and FDR II, what advanced responsibilities are you looking for them to handle?")
responses["advanced_focus"] = st.text_area("3. Any other suggestions or focus areas for these advanced levels?")
responses["advanced_comments"] = st.text_area("Additional comments on Advanced training")

# --- Onboarding Questions ---
st.header("Onboarding Process")
responses["onboard_desc"] = st.text_area("Describe how a new hire is onboarded in your CSC  from Day 1 until their first class.")
responses["onboard_support"] = st.radio("Are they assigned a dedicated coach/senior/work leader for new hires?", ["Yes", "No"])
responses["onboard_support_desc"] = st.text_area("If yes, describe how they support new hires.")

# --- Feedback on Survey Experience ---
st.header("Feedback on Survey Experience")
responses["ai_feedback"] = str(st.slider("How did you like the hybrid AI guided survey structure?", min_value=1, max_value=5, value=5, step=1))
st.write("👉 5 = Loved it | 1 = Didn't like at all")
responses["ai_comments"] = st.text_area("Comments on the AI survey experience")
responses["recommend"] = st.radio("Would you recommend this survey app for colleagues/departments?", ["Yes", "No", "Maybe"])
responses["recommend_comments"] = st.text_area("Why or why not?")

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
if st.button("Submit Survey"):
    _handle_submission(responses)
