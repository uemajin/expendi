import streamlit as st

def generate_unlogged_menu():

    st.logo(f"assets/images/logo.png")
    st.sidebar.page_link("app.py", label="🏠 Home")
    st.sidebar.write("Please select a profile to access the dashboard.")
    st.sidebar.page_link("pages/Profiles.py", label="👤 Profiles")
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/About.py", label="❔ About")

def generate_user_menu():

    with st.sidebar:
        c1, c2 = st.columns([1, 3])
        c1.image(st.session_state.user_photo)
        c2.markdown("#### Welcome, " + st.session_state.full_name + "!")
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
