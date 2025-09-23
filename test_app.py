"""Simple test to verify Streamlit is working."""

import streamlit as st

st.title("Test App")
st.write("If you can see this, Streamlit is working!")

name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}!")

choice = st.selectbox("Pick a color:", ["Red", "Green", "Blue"])
st.write(f"You chose: {choice}")

rating = st.slider("Rate this test:", 1, 5, 3)
st.write(f"Your rating: {rating}")