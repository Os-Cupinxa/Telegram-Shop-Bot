import streamlit as st


def show_sidebar():
    st.sidebar.selectbox("Menu", ["Home", "About", "Contact"])
