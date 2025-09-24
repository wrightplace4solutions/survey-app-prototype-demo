"""Minimal test app to verify Streamlit is working."""

import streamlit as st

st.title("🧪 Test App")
st.write("If you can see this, Streamlit is working!")

name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}!")

age = st.slider("Select your age:", 0, 100, 25)
st.write(f"You are {age} years old.")

color = st.selectbox("Choose a color:", ["Red", "Green", "Blue"])
st.write(f"You chose: {color}")

if st.button("Click me!"):
    st.success("Button clicked! ✅")
    st.balloons()