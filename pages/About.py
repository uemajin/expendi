import streamlit as st
from src import *

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="centered"
    )

get_menu()

st.title("About")

load_about()