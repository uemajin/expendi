import streamlit as st
from requests.exceptions import HTTPError
from src import get_config
import time

auth, db = get_config()

with st.form(key='login_form'):
    username = st.text_input("email")
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

                time.sleep(2)

                st.switch_page("app.py")

            

            
            #user_data = db.child("users").child(user['localId']).get().val()
            #st.success("Welcome, " + user_data['fullname'])

        except HTTPError:
            st.error("Invalid username or password")