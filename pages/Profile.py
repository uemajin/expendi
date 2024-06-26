import streamlit as st

from src import *

storage = getFirebaseStorage()

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="centered",
    )

get_menu()

st.title("Profile")

user = db.child("users").child(st.session_state.uid).get().val()

c1, c2 = st.columns([5, 1])
c1.write(f"Full Name: {user['fullname']}")
c1.write(f"Email: {user['email']}")
c1.write(f"Role: {user['role']}")
c1.write(f"Verified: {user['verified']}")

load_user_profile_image(c2, user['profile_img'])

st.write("")

with st.expander('Update Profile', expanded=False):

    update_lock = False

    st.write("Update your profile")
    col1, col2 = st.columns([1, 1])
    fullname = col1.text_input("Full Name", value=user['fullname'])
    email = col1.text_input("New E-mail", value=user['email'])
    email_confirmation = col1.text_input("Confirm your E-mail", value=user['email'])

    if email != email_confirmation:
        st.error("E-mails do not match!")
        update_lock = True

    password = col1.text_input("New Password", type='password')
    password_validation = col1.text_input("Confirm your Password", type='password')

    if password != password_validation:
        st.error("Passwords do not match!")
        update_lock = True

    submit_button = col1.button(label='Update', disabled=update_lock)
    new_user_img = col2.file_uploader("Upload a new profile picture", type=['png', 'jpg', 'jpeg'])

    if submit_button:

        if new_user_img:

            filename = f"{st.session_state.uid}_p.png"
            save_image(process_image(new_user_img), '.temp/' + filename)

            storage.child("images/profiles").child(filename).put('.temp/' + filename)
            img_url = storage.child("images/profiles").child(filename).get_url(None)

        if password:
            auth.update_user(user['idToken'], {'password': password})

        user_data = {
                "fullname": fullname,
                "email": email,
                "role": user['role'],
                "verified": user['verified'],
                "profile_img": img_url
            }

        db.child("users").child(st.session_state.uid).update(user_data)

        st.success("Profile updated successfully!")
        time.sleep(2)
        st.rerun()
