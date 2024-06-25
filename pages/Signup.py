import streamlit as st
from src import get_config, get_menu
import time

auth, db = get_config()

get_menu()

st.title("Sign Up") 

with st.form(key='signup_form'):
    fullname = st.text_input("Full Name")
    email = st.text_input("E-mail")
    password = st.text_input("Password", type='password')
    submit_button = st.form_submit_button(label='Sign Up')

    if submit_button:
        user = auth.create_user_with_email_and_password(email, password)

        user_data = {
                "fullname": fullname,
                "email": email,
                "role": "user",
                "verified": False 
            }

        db.child("users").child(user['localId']).set(user_data)

        auth.send_email_verification(user['idToken'])
        st.success("Signup successful!")
        st.success("Please check your email to verify your account.")

        st.write("You will be redirected to the login page in 5 seconds.")
        time.sleep(5)
        st.switch_page("pages/Login.py")
    



