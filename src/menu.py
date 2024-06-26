import streamlit as st

def get_menu():

    st.sidebar.title("💸 Expendi")
    
    if "role" not in st.session_state:
        st.session_state.role = None

    if st.session_state.role is None:
        st.sidebar.write("Please login to access the dashboard.")
        st.sidebar.page_link("app.py", label="🏠 Home")
        st.sidebar.page_link("pages/Login.py", label="🔑 Log in")
        st.sidebar.page_link("pages/Signup.py", label="✉️ Sign up")
    #elif st.session_state.role == 'admin':
    #    st.sidebar.page_link("Admin Dashboard", label="Dashboard")
    #    st.sidebar.page_link("User Management", label="Manage Users")
    elif st.session_state.role == 'user':
        st.sidebar.write("Welcome, " + st.session_state.user)
        st.sidebar.page_link("app.py", label="🏠 Home")
        st.sidebar.page_link("pages/Profile.py", label="Profile", disabled=True)
        st.sidebar.page_link("pages/Settings.py", label="Settings", disabled=True)
        if st.sidebar.button("Log Out"):
            st.session_state.clear()
            st.switch_page("app.py")

    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/About.py", label="❔ About")