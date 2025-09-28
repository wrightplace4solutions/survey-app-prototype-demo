"""
Training Feedback Survey Application - Home Page.

This is the main landing page featuring the AI introduction and navigation.
"""

import os
import streamlit as st

st.set_page_config(page_title="Training Feedback Survey", layout="wide")

# Enhanced styling similar to survey page
st.markdown(
    """
    <style>
        /* Main background with subtle gradient */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        /* Header styling with granulated glowing effect */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
            background-size: 200% 200%;
            animation: gradientShift 4s ease infinite;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 
                0 0 20px rgba(102, 126, 234, 0.4),
                0 0 40px rgba(118, 75, 162, 0.3),
                0 0 60px rgba(102, 126, 234, 0.2),
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
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5em;
            text-shadow: 
                0 0 10px rgba(255,255,255,0.5),
                0 0 20px rgba(255,255,255,0.3),
                0 0 30px rgba(102, 126, 234, 0.4),
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
                0 0 15px rgba(118, 75, 162, 0.3),
                1px 1px 2px rgba(0,0,0,0.2);
            position: relative;
            z-index: 2;
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
        
        /* Content containers */
        .content-container {
            background: rgba(255,255,255,0.9);
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        /* Navigation buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 1rem 2rem;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
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

st.markdown("### Survey System")
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

st.markdown("### � Thank You!")
st.write("Thank you for taking the time to provide your valuable feedback!")
st.markdown('</div>', unsafe_allow_html=True)
