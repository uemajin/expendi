import streamlit as st
from src import *
import time

auth = getFirebaseAuth()
db = getFirebaseDB()

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="centered",
        initial_sidebar_state="collapsed"
    )

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
        
        temp_img = open_image("https://firebasestorage.googleapis.com/v0/b/finance-dash-8e11a.appspot.com/o/images%2Fprofiles%2Fdefault.png?alt=media&token=abb6e91f-1e78-4e84-bbc7-3317fc0ef9f8")

        db.child("users").child(user['localId']).set(user_data)
        storage.child("images").child("profiles").child(f"{user['localId']}_p.png").put(temp_img)

        auth.send_email_verification(user['idToken'])
        st.success("Signup successful!")
        st.success("Please check your email to verify your account.")

        st.write("You will be redirected to the login page in 5 seconds.")
        time.sleep(5)
        st.switch_page("pages/Login.py")
    



