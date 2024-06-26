import streamlit as st
from requests.exceptions import HTTPError
from src import *
import time


auth = getFirebaseAuth()
db = getFirebaseDB()
storage = getFirebaseStorage()

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="centered",
        initial_sidebar_state="collapsed"
    )

get_menu()

st.title("Login")

with st.form(key='login_form'):
    username = st.text_input("Email")   
    password = st.text_input("Password", type='password')
    submit_button = st.form_submit_button(label='Login')

    if submit_button:
        try:
            user = auth.sign_in_with_email_and_password(username, password)
            user_data = auth.get_account_info(user['idToken'])['users'][0]['emailVerified']
            if user_data == False:
                st.error("Please verify your email first.")
            
            else:
                user_data = db.child("users").child(user['localId']).get().val()
                st.success("Login successful!, Welcome, " + user_data['fullname'])

                st.session_state.role = user_data['role']
                st.session_state.user = user_data['fullname']
                st.session_state.uid = user['localId']
                st.session_state.img_link = user_data['profile_img']

                time.sleep(2)
                st.switch_page("app.py")

        except HTTPError:
            st.error("Invalid username or password")

col1, col2= st.columns([1, 1])

with col1:
    with st.form(key='signup_form'):
        st.write("Don't have an account? Sign up now!")
        if st.form_submit_button("Sign Up"):
            st.switch_page("pages/Signup.py")

with col2:
    with st.form(key='reset_password_form'):
        st.write("Forgot your password? Reset now!")
        if st.form_submit_button("Reset Password"):
            forgot_password()