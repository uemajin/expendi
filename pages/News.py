import streamlit as st
from datetime import datetime

from src import *

auth = getFirebaseAuth()
db = getFirebaseDB()

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="centered",
    )

get_menu()

st.title("News")

if 'role' in st.session_state:

    if st.session_state.role == "admin":

        with st.form(key='news_form'):
            title = st.text_input("Title")
            content = st.text_area("Content")
            submit_button = st.form_submit_button(label='Post News')

            if submit_button:
                news_data = {
                        "title": title,
                        "content": content,
                        "author": st.session_state.user,
                        "author_img": st.session_state.img_link,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                db.child("news").push(news_data)
                st.success("News posted successfully!")

    st.write("")
    
load_news(db)