import streamlit as st
from st_social_media_links import SocialMediaIcons

from src import *

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="centered"
    )

get_menu()

st.title("About")

social_media_icons = SocialMediaIcons(
    [
        "https://www.linkedin.com/in/jin-uema/",
        "https://github.com/uemajin"
    ],
    [
        "grey",
        "grey"
    ]
)

c1, c2 = st.columns([1, 9]) 

with c1:
    c1.image("https://i.ibb.co/c3cPDm4/Captura-de-Tela-2024-06-25-a-s-14-48-27-modified-1.png", use_column_width=True)
    social_media_icons.render()

c2.write("""Hello my name is Jin and I am a Data scientist and software developer. I am currently enrolled in a MBA of Data Science and Analytics at the University of São Paulo (USP) and I am passionate about technology, specially things that can make my life easier 😅.
             I am currently working on a project called Expendi, which is a personal finance management application.
             This project was developed using Python, Streamlit, Firebase and Plotly. I hope you enjoy it!""")


st.markdown("---")

st.markdown("## Why Expendi?")

st.write("""For the past few years I have been trying to find a way to manage my finances in a simple and intuitive way. 
         I have tried several applications, but none of them had the features that I was looking for.
         There are a few good apps in the market but unfortunately most of them are paid (which is counterintuitive). """)

c1, c2, c3 = st.columns([1, 1, 1])

c2.image("https://media4.giphy.com/media/HPLBdanIEmUVsajae2/giphy.gif?cid=6c09b952yplfwy6pw265vlc0a734zg041suj35bkz1b13xjd&ep=v1_gifs_search&rid=giphy.gif&ct=g", width=300, caption="Me trying to find a good finance management app")
         
st.write("""Expendi was created to help people manage their finances in a simple and intuitive way. 
         With Expendi you can insert your transactions, categorize them and visualize them in a simple and interactive way, and the most important feature: **it's free!**""")

c1, c2, c3 = st.columns([1, 1, 1])

c2.image("https://media.makeameme.org/created/if-i-dont-5cc72d.jpg", width=300, caption="Julius was right")