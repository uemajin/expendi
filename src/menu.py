import streamlit as st
from src.transactions import edit_profile, login, create_profile

def generate_unlogged_menu():

    st.logo(f"assets/images/logo.png")
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.write("Please log in or sign up to access the dashboard.")
    if st.sidebar.button("Log In"):
        login()
    if st.sidebar.button("Sign Up"):
        create_profile()
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/About.py", label="❔ About")

    if st.secrets['current_env'] == 'prod':
# Set an alarm that the app won't save the data
        st.sidebar.warning("This is a test environment. Data is transient and will not be saved.")
    # Any changes made here will not be saved permanently. Please use the development environment for testing and saving data.")

def generate_user_menu():

    user = st.session_state.get('user')

    with st.sidebar:
        c1, c2 = st.columns([1, 3])
        c1.image(user.photo)
        c2.markdown("#### Welcome, " + user.fullname + "!")
    st.sidebar.page_link("app.py", label="🏠 Home")

    if st.sidebar.button("Edit Profile"):
        edit_profile(user)
        
    if st.sidebar.button("Log Out"):
        st.session_state.clear()
        st.rerun()
    
    st.sidebar.markdown("---")
    
    st.sidebar.page_link("pages/About.py", label="❔ About")

    if st.secrets['current_env'] == 'prod':
    # Set an alarm that the app won't save the data
        st.sidebar.warning("This is the production environment")
        st.sidebar.warning("This is a read-only environment.")
        st.sidebar.warning("You can view the data, but you cannot modify it.")
        st.sidebar.warning("If you want to test the app, please use the development environment.")
        # Any changes made here will not be saved permanently. Please use the development environment for testing and saving data.")


def get_menu():

    st.sidebar.title("Expendi")

    if "user" not in st.session_state:
        generate_unlogged_menu()
    else:
        generate_user_menu()
