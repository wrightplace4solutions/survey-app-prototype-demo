"""
Training Survey App
Built with Streamlit for Training Survey (prototype demo)
"""
import streamlit as st

st.title("Survey Prototype Demo")
st.caption("Powered by Soulware Systems | WrightPlace4Solutions")

# Set the color scheme using a bit of custom styling
st.markdown(
    """
    <style>
        body {
            color: black;
            background-color: #f0f2f6; /* light grey background */
        }
        .stApp {
            color: black;
            background-color: white; /* white content background */
        }
        h1, h2, h3 {
            color: #0366d6; /* DMV blue for headers */
        }
    </style>
    """, unsafe_allow_html=True
)

# Title and Introduction
st.title("Training Feedback Survey")
st.write("Welcome! We’d love your feedback on how our training programs are preparing your team.")

# Section 1: Title Class
st.subheader("Title Class")
st.text_input("1. What skills do you find most important for agents coming out of the Title class?")
st.text_input("2. What specific challenges do they usually face when they return to their roles?")

# Section 2: Combined FDR1 and DLID
st.subheader("FDR1 and DLID (Driver’s License & ID)")
st.text_input("3. After completing the FDR1 and DLID courses, what improvements do you expect to see in agents’ performance?")
st.text_input("4. Are there any particular document or ID verification tasks you want them to master?")

# Section 3: Driver Examiners
st.subheader("Driver Examiners Course")
st.text_input("5. For the Driver Examiners course, what additional responsibilities should they be prepared to take on?")

# Section 4: Compliance
st.subheader("Compliance Course")
st.text_input("6. After the Compliance course, what compliance-related skills do you need them to have?")

# Section 5: Advanced Courses (VDH and FDR II)
st.subheader("Advanced Courses (VDH, FDR II)")
st.text_input("7. For those who’ve completed VDH and FDR II, what advanced responsibilities are you looking for them to handle?")
st.text_area("8. Any other suggestions or focus areas for these advanced levels?")

# Placeholder for animation
st.write("[Animation will appear here]")

# Now you can run the app and see all the updated sections!
