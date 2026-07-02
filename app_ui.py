import streamlit as st

st.title("AI Agent Test")

user_input = st.text_input("Say something")

if user_input:
    st.write("You typed:", user_input)