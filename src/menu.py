from src.helper import load_user_profile_image
import streamlit as st

def generate_unlogged_menu():
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.write("Please login to access the dashboard.")
    st.sidebar.page_link("pages/Login.py", label="🔑 Log in")
    st.sidebar.page_link("pages/Signup.py", label="✉️ Sign up")
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/About.py", label="❔ About")
    st.sidebar.page_link("pages/News.py", label="📰 News")

def generate_user_menu():

    st.sidebar.write("Welcome, " + st.session_state.user)
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/Profile.py", label="Profile")
    if st.sidebar.button("Log Out"):
        st.session_state.clear()
        st.switch_page("app.py")
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/About.py", label="❔ About")
    st.sidebar.page_link("pages/News.py", label="📰 News")

def generate_admin_menu():

    c1, c2 = st.sidebar.columns([1, 1])

    load_user_profile_image(c1, st.session_state.img_link)
    c2.write("Welcome! \n" + st.session_state.user)

    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.page_link("pages/Profile.py", label="Profile")
    st.sidebar.markdown("---")
    st.sidebar.write("Admin Stuff")
    st.sidebar.page_link("pages/AdminDashboard.py", label="Admin Dashboard", disabled=True)
    st.sidebar.page_link("pages/UserManagement.py", label="Manage Users", disabled=True)
    if st.sidebar.button("Log Out"):
        st.session_state.clear()
        st.switch_page("app.py")
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/About.py", label="❔ About")
    st.sidebar.page_link("pages/News.py", label="📰 News")

def get_menu():

    st.sidebar.title("💸 Expendi")
    
    if "role" not in st.session_state:
        generate_unlogged_menu()
    elif st.session_state.role == 'user':
        generate_user_menu()
    elif st.session_state.role == 'admin':
        generate_admin_menu()