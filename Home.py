"""
Training Feedback Survey Application - Home Page.

This is the main landing page featuring the AI introduction and navigation.
"""

import os
import streamlit as st

st.set_page_config(page_title="Training Feedback Survey", layout="wide")

# Enhanced styling with tan clipboard design
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
        
        /* Header styling with gradient glowing effect */
        .main-header {
            background: linear-gradient(135deg, #2F1B14 0%, #8B2635 50%, #2F1B14 100%);
            background-size: 200% 200%;
            animation: gradientShift 4s ease infinite;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 1rem;
            box-shadow: 
                0 0 20px rgba(139, 38, 53, 0.4),
                0 0 40px rgba(47, 27, 20, 0.3),
                0 0 60px rgba(139, 38, 53, 0.2),
                0 8px 32px rgba(0,0,0,0.2);
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
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5em;
            text-shadow: 
                0 0 10px rgba(255,255,255,0.5),
                2px 2px 4px rgba(0,0,0,0.7);
            position: relative;
            z-index: 2;
        }
        
        .main-header h3 {
            color: rgba(255,255,255,0.95);
            margin: 10px 0 0 0;
            font-weight: 300;
            text-shadow: 
                1px 1px 2px rgba(0,0,0,0.5);
            position: relative;
            z-index: 2;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Content containers with Results page color scheme */
        .content-container {
            background: linear-gradient(135deg, #FFFEF7 0%, #F8F6F0 100%);
            padding: 2rem;
            border-radius: 8px;
            margin: 1.5rem;
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
        
        /* Enhanced text visibility */
        .content-container h3 {
            color: #2F1B14 !important;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        }
        
        .content-container p, .content-container div {
            color: #1A1A1A !important;
            line-height: 1.6;
            font-weight: 500;
        }
        
        /* Navigation buttons with Results page style */
        .stButton > button {
            background: linear-gradient(135deg, #2F1B14 0%, #8B2635 100%);
            color: white !important;
            border: 2px solid #8B2635;
            border-radius: 8px;
            padding: 1rem 2rem;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 
                0 4px 15px rgba(139, 38, 53, 0.3),
                inset 0 1px 0 rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            width: 100%;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 6px 20px rgba(139, 38, 53, 0.4),
                inset 0 1px 0 rgba(255,255,255,0.3);
            background: linear-gradient(135deg, #8B2635 0%, #2F1B14 100%);
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

# AI Introduction Video Section
st.markdown('<div class="content-container">', unsafe_allow_html=True)
st.markdown("### 🤖 Meet Your AI Survey Assistant")

# Check if video file exists
video_file = "assets/avatar_intro.mp4"
if os.path.exists(video_file):
    st.video(video_file)
else:
    st.info("🎬 AI Introduction Video will be displayed here")
    st.markdown("*Video file: assets/avatar_intro.mp4*")

st.markdown("### 📋 Survey System")
st.write("""
This application helps us gather valuable feedback about our training programs to continuously improve the quality and effectiveness of our training offerings.
""")
st.markdown('</div>', unsafe_allow_html=True)

# How to Use This System
st.markdown('<div class="content-container">', unsafe_allow_html=True)
st.markdown("### 🚀 How to Use This System:")

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Take Survey", key="survey_nav", help="Complete the comprehensive training feedback survey"):
        st.switch_page("pages/2_Survey.py")

with col2:
    if st.button("📊 View Results", key="results_nav", help="Analyze survey results and trends (for administrators)"):
        st.switch_page("pages/3_Results.py")

st.markdown('</div>', unsafe_allow_html=True)

# Getting Started Section
st.markdown('<div class="content-container">', unsafe_allow_html=True)
st.markdown("### 🎯 Getting Started")
st.write("""
In case you missed the instructions from our AI Assistant, please scan the QR Code or visit:
**https://survey.soulwaresystems.com**
""")

# QR Code placeholder
if os.path.exists("assets/survey_qr.png"):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("assets/survey_qr.png", width=200, caption="Scan for Quick Access")
else:
    st.info("� QR Code will be displayed here (assets/survey_qr.png)")

st.markdown('</div>', unsafe_allow_html=True)
