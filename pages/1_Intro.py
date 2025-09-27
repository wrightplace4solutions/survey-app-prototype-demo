"""Intro/landing page visuals and instructions for the survey app."""
# pylint: disable=invalid-name

import os
import streamlit as st

# ----- Styling -----
st.markdown(
    """
    <style>
        body { color:#2F1B14; background-color:#FAF7F0; }
        .stApp { color:#2F1B14; background-color:#FEFCF7; }
        h1,h2,h3 { color:#8B2635; }
        .demographics-form{
            background-color:#f8f9fa; padding:20px; border-radius:10px;
            margin:20px 0; border:2px solid #8B2635;
        }
        .required-field{ color:#8B2635; font-weight:700; }
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stTextArea > div > div > textarea { background:#fff !important; color:#2F1B14 !important; }
        
        /* Fix warning box text visibility */
        .stAlert > div { color:#2F1B14 !important; }
        .stWarning > div { color:#2F1B14 !important; font-weight:600; }
        .stSuccess > div { color:#2F1B14 !important; font-weight:600; }
        
        /* QR Code section styling */
        .qr-section { text-align: center; margin: 20px 0; }
        .qr-text { color:#8B2635; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to the Training Feedback Survey")

# ----- HeyGen greeting (prefer secrets → env → local mp4) -----
heygen_embed = st.secrets.get("heygen_embed_url") if "secrets" in dir(st) else os.getenv("HEYGEN_EMBED_URL")
heygen_mp4   = st.secrets.get("heygen_mp4_url")   if "secrets" in dir(st) else os.getenv("HEYGEN_MP4_URL")

if heygen_embed:
    st.components.v1.html(
        f"""<div style="display:flex;justify-content:center">
               <iframe src="{heygen_embed}" width="720" height="405" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
            </div>""",
        height=430
    )
elif heygen_mp4:
    st.video(heygen_mp4)
elif os.path.exists("assets/avatar_intro.mp4"):
    st.video("assets/avatar_intro.mp4")
else:
    st.info("Tap **Take Survey** in the sidebar to get started. (Greeting video not configured.)")

st.write("""
### Instructions
- This survey should take about 10 minutes.
- Please complete the demographics below to unlock the survey.
- If you’d like a copy of your responses, enter your email.
""")

# Optional QR (kept for convenience)
if os.path.exists("assets/survey_qr.png"):
    st.markdown('<div class="qr-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/survey_qr.png", width=280)
        st.markdown('<p class="qr-text">👆 Scan QR Code</p>', unsafe_allow_html=True)
        st.markdown('<p class="qr-text"><strong>or visit:</strong> https://survey.soulwaresystems.com</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Demographics (CSC required) -----
st.markdown("---")
st.markdown('<div class="demographics-form">', unsafe_allow_html=True)
st.header("📝 Demographics")
st.markdown('<p class="required-field">Select your CSC location to proceed.</p>', unsafe_allow_html=True)

if "demographics_completed" not in st.session_state:
    st.session_state.demographics_completed = False

with st.form("demographics_form"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Name** (Optional)")
        name = st.text_input("Name", value=st.session_state.get("user_name",""), label_visibility="collapsed")
        st.markdown("**Role/Title** (Optional)")
        role = st.text_input("Role/Title", value=st.session_state.get("user_role",""), label_visibility="collapsed")
    with col2:
        st.markdown("**CSC Location** (Required)")
        csc = st.selectbox("CSC", [
            "", "Ashland","Chester","Chesterfield","East Henrico","Emporia","Ft Gregg Adams","Hopewell",
            "Kilmarnock","Petersburg","Richmond Center (HQ)","Tappahannock","West Henrico","Williamsburg",
            "Other (please specify in email field)"], index=0, label_visibility="collapsed")
        st.markdown("**Email** (Optional)")
        email = st.text_input("Email", value=st.session_state.get("user_email",""), label_visibility="collapsed",
                              placeholder="your.email@domain.com")
    submitted = st.form_submit_button("💾 Save Demographics & Continue", type="primary", use_container_width=True)

    if submitted:
        if not csc:
            st.error("❌ Please select your CSC location.")
        else:
            st.session_state.user_name  = name.strip() or "Anonymous"
            st.session_state.user_role  = role.strip() or "Not Specified"
            st.session_state.user_csc   = csc
            st.session_state.user_email = email.strip()
            st.session_state.demographics_completed = True
            st.success("✅ Saved! Use the sidebar to open **Survey**.")
            st.balloons()

if st.session_state.get("demographics_completed"):
    st.success("✅ Demographics complete — open **Survey** from the sidebar.")
else:
    st.warning("⚠️ Select your CSC to unlock the survey.")
st.markdown('</div>', unsafe_allow_html=True)
