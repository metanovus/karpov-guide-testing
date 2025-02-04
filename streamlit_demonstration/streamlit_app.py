import streamlit as st

if "my_text" not in st.session_state:
    st.session_state.my_text = ""

def submit():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""

st.text_input("Enter text here", key="widget", on_change=submit)

my_text = st.session_state.my_text

st.write(my_text)
