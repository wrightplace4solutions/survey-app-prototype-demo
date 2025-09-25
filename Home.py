"""
Training Feedback Survey Application - Home Page.

This is the main landing page that directs users to the survey.
"""

import streamlit as st

st.set_page_config(page_title="Training Feedback Survey", layout="wide")

# Company Branding
st.markdown(
    "<h1 style='text-align: center; color: #8B2635;'>Training Feedback Survey</h1>",
    unsafe_allow_html=True
)
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

# Welcome message
st.write("""
### Welcome to the Training Feedback Survey System

This application helps us gather valuable feedback about our training programs to continuously improve the quality and effectiveness of our training offerings.

#### How to Use This System:

1. **📋 Introduction** - Start here to learn about the survey and watch the introduction video
2. **📝 Survey** - Complete the comprehensive training feedback survey  
3. **📊 Results** - View aggregated results and analytics (for administrators)

### Getting Started

Use the sidebar navigation to move between pages. We recommend starting with the **Introduction** page to understand the purpose and scope of this survey.

Thank you for taking the time to provide your valuable feedback!
""")

# Quick navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📋 Introduction")
    st.write("Learn about the survey and watch the intro video")
    
with col2:
    st.markdown("### 📝 Take Survey")  
    st.write("Complete the training feedback questionnaire")
    
with col3:
    st.markdown("### 📊 View Results")
    st.write("Analyze survey results and trends")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #8B2635; font-style: italic;'>Select a page from the sidebar to continue</p>",
    unsafe_allow_html=True
)
