import streamlit as st

from src import *

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="centered",
        initial_sidebar_state="collapsed"
    )

get_menu()

st.title("Profile")