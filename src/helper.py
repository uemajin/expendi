import requests, os, io
import streamlit as st
from PIL import Image, ImageDraw, ImageOps
from st_social_media_links import SocialMediaIcons

def bgcolor_positive_or_negative(value):
    if isinstance(value, str):
        value = float(value.replace(',', ''))

    bgcolor = "lightcoral" if value < 0 else "lightgreen"
    return f"background-color: {bgcolor};"

def read_query(query_name):
    query_path = os.path.join(os.getcwd(), "db", "queries", query_name + ".sql")
    with open(query_path, "r") as file:
        return file.read()

def process_image(img):

    img = Image.open(img)

    width, height = img.size

    if width > height:
        left = (width - height) // 2
        top = 0
        right = left + height
        bottom = height
    else:
        left = 0
        top = (height - width) // 2
        right = width
        bottom = top + width

    img = img.crop((left, top, right, bottom))
    img = img.resize((348, 348), Image.LANCZOS)

    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)

    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result.paste(img, mask=mask)

    # Save the image to a BytesIO object
    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    return buffer.getvalue()

def open_image(img):
    return Image.open(img)

def save_image(img, path):
    return img.save(path)

def load_user_profile_image(col, image_link):
    image = requests.get(image_link).content
    return col.image(image, use_container_width=True)

@st.cache_data(show_spinner=False)
def load_news(_db):

    news = _db.child("news").get().val()

    for key, value in reversed(list(news.items())):

        c1, c2 = st.columns([6, 1])

        c1.markdown(f"## {value['title']}")
        c1.markdown(f"###### Posted on: {value['date'].split(' ')[0]} by {value['author']}")

        load_user_profile_image(c2, value['author_img'])

        st.markdown(f"{value['content']}")

        st.markdown("---")

st.cache_data(show_spinner=False)
def load_about():

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
        load_user_profile_image(c1, "https://uemajin.com/static/images/profile.png")
        social_media_icons.render()

    c2.write("""Hello my name is Jin and I am a Data scientist and software developer. I am currently enrolled in a MBA of Data Science and Analytics at the University of São Paulo (USP) and I am passionate about technology, specially things that can make my life easier 😅.
                I am currently working on a project called Expendi, which is a personal finance management application.
                This project was developed using Python, Streamlit, SQLite and Plotly. I hope you enjoy it!""")


    st.markdown("---")

    st.markdown("## Why Expendi?")

    st.write("""For the past few years I have been trying to find a way to manage my finances in a simple and intuitive way.
            I have tried several applications, but none of them had the features that I was looking for.
            There are a few good apps in the market but unfortunately most of them are paid (which is counterintuitive). """)

    c1, c2, c3 = st.columns([1, 1, 1])

    c2.image("https://media4.giphy.com/media/HPLBdanIEmUVsajae2/giphy.gif?cid=6c09b952yplfwy6pw265vlc0a734zg041suj35bkz1b13xjd&ep=v1_gifs_search&rid=giphy.gif&ct=g", use_container_width=True, caption="Me trying to find a good finance management app")

    st.write("""Expendi was created to help people manage their finances in a simple and intuitive way.
            With Expendi you can insert your transactions, categorize them and visualize them in a simple and interactive way, and the most important feature: **it's free!**""")

    c1, c2, c3 = st.columns([1, 1, 1])

    c2.image("https://media.makeameme.org/created/if-i-dont-5cc72d.jpg", caption="Julius was right", use_container_width=True)
