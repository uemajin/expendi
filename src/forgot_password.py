import streamlit as st
from .firebase_auth import *
import time

auth = getFirebaseAuth()

@st.experimental_dialog("Forgot Password")
def forgot_password():
    st.write("Input your password to reset your password.")
    email = st.text_input("E-mail")
    if st.button("Submit"):
        auth.send_password_reset_email(email)
        st.success("Password reset email sent successfully!")
        time.sleep(2)