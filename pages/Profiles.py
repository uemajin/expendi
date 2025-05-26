import io
import streamlit as st

from src import *

db = Database()

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="centered",
    )

get_menu()

st.title("👤 Profiles")

if 'user_id' not in st.session_state:

    all_users = db.load_all_users()

    if len(all_users) == 0:
        st.write("No users found")

    # Number of columns in the grid
    num_columns = 2
    columns = st.columns(num_columns)

    for i, user in enumerate(all_users):
        col = columns[i % num_columns]  # Select the column in a round-robin fashion

        with col:
            container = st.container(border=True)

            c1, c2 = container.columns([3, 6])

            c1.image(user[5], use_container_width=True)
            c2.markdown("### " + user[1])

            c1, c2, c3 = container.columns([1, 1, 1])
            if c1.button("Log in here", key=user[1]):
                login(user)

            if c2.button("Edit Profile", key='edit_profile_' + user[1]):
                edit_profile(user)

            if c3.button("Delete Profile", key='delete_profile_' + user[1], disabled = not st.session_state.get('delete_enabled_' + user[1], False)):
                delete_profile(user)


with st.form(key='signup_form'):
    st.write("Don't have a profile? Create one now!")
    if st.form_submit_button("Create New Profile"):
        create_profile()
