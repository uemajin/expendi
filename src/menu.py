import streamlit as st

from src.helper import load_user_profile_image_local

def generate_unlogged_menu():
    st.logo("assets/images/logo.png")
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.write("Please select a profile to access the dashboard.")
    st.sidebar.page_link("pages/Profiles.py", label="👤 Profiles")
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/About.py", label="❔ About")

def generate_user_menu():

    with st.sidebar:
        c1, c2 = st.columns([1, 3])
        c1.image(load_user_profile_image_local(st.session_state.user))
        c2.markdown("#### Welcome, " + st.session_state.user)
    st.sidebar.page_link("app.py", label="🏠 Home")
    if st.sidebar.button("Log Out"):
        st.session_state.clear()
        st.switch_page("pages/Profiles.py")
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/About.py", label="❔ About")

def get_menu():

    st.sidebar.title("Expendi")

    if "user_id" not in st.session_state:
        generate_unlogged_menu()
    else:
        generate_user_menu()
