import io
import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_plotly_events import plotly_events

import plotly.graph_objects as go
from io import BytesIO
import base64

import random

from packcircles import pack

import streamlit.components.v1 as components

import json

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
    
    else:

        st.subheader("Here are some users managing their finances with Expendi.")

        df = pd.DataFrame(all_users, columns=['ID', 'Username', 'Full Name', 'Password Hash', 'Salt', 'Image'])
                          
        if len(df) > 100:
            df = df.sample(100)  # Sample 100 users if more than 100 exist

        # Convert each image to base64 string
        users_for_js = []
        for _, row in df.iterrows():
            try:
                b64_img = base64.b64encode(row['Image']).decode('utf-8')
                users_for_js.append({
                    'name': row['Username'],
                    'image': f"data:image/png;base64,{b64_img}",
                    'size': random.randint(10, 100)  # random size
                })
            except Exception as e:
                st.warning(f"Error encoding image for {row['Username']}: {e}")

        js_data = json.dumps({"children": users_for_js})

        # HTML + D3 with images
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                .node {{
                    text-anchor: middle;
                    font: 10px sans-serif;
                }}
                .user-img {{
                    clip-path: circle(50%);
                }}
            </style>
        </head>
        <body>
            <div id="viz"></div>

            <script src="https://d3js.org/d3.v7.min.js"></script>
            <script>
                const data = {js_data};

                const width = 600;
                const height = 600;

                const svg = d3.select("#viz").append("svg")
                    .attr("width", width)
                    .attr("height", height)
                    .style("font", "10px sans-serif");

                const simulation = d3.forceSimulation(data.children)
                    .force("charge", d3.forceManyBody().strength(5))
                    .force("center", d3.forceCenter(width / 2, height / 2))
                    .force("x", d3.forceX(width / 2).strength(0.1))
                    .force("y", d3.forceY(height / 2).strength(0.1))
                    .force("collision", d3.forceCollide().radius(d => d.size + 2))
                    .on("tick", ticked);

                const node = svg.selectAll("g")
                    .data(data.children)
                    .join("g")
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));

                node.append("clipPath")
                    .attr("id", d => "clip-" + d.name)
                    .append("circle")
                    .attr("r", d => d.size);

                node.append("image")
                    .attr("href", d => d.image)
                    .attr("x", d => -d.size)
                    .attr("y", d => -d.size)
                    .attr("width", d => d.size * 2)
                    .attr("height", d => d.size * 2)
                    .attr("clip-path", d => "url(#clip-" + d.name + ")");

                function ticked() {{
                    node.attr("transform", d => `translate(${{d.x}}, ${{d.y}})`);
                }}

                let lastEvent = null;

                function dragstarted(event, d) {{
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                    lastEvent = event;
                }}

                function dragged(event, d) {{
                    d.fx = event.x;
                    d.fy = event.y;
                    lastEvent = event;
                }}

                function dragended(event, d) {{
                    if (!event.active) simulation.alphaTarget(0);

                    if (lastEvent) {{
                        const dt = event.sourceEvent.timeStamp - lastEvent.sourceEvent.timeStamp + 1;
                        const dx = event.x - lastEvent.x;
                        const dy = event.y - lastEvent.y;

                        // Set velocity (adjust multiplier as needed)
                        d.vx = dx / dt * 20;
                        d.vy = dy / dt * 20;
                    }}

                    // Let simulation take over again
                    d.fx = null;
                    d.fy = null;
                    lastEvent = null;
                }}
            </script>


        </body>
        </html>
        """

        components.html(html_code, height=650, scrolling=False)

    # # Number of columns in the grid
    # num_columns = 2
    # columns = st.columns(num_columns)

    # for i, user in enumerate(all_users):
    #     col = columns[i % num_columns]  # Select the column in a round-robin fashion

    #     with col:
    #         container = st.container(border=True)

    #         c1, c2 = container.columns([3, 6])

    #         c1.image(user[5], use_container_width=True)
    #         c2.markdown("### " + user[1])

    #         c1, c2, c3 = container.columns([1, 1, 1])
    #         if c1.button("Log in here", key=user[1]):
    #             login(user)

    #         if c2.button("Edit Profile", key='edit_profile_' + user[1]):
    #             edit_profile(user)

    #         if c3.button("Delete Profile", key='delete_profile_' + user[1], disabled = not st.session_state.get('delete_enabled_' + user[1], False)):
    #             delete_profile(user)


container = st.container(border=True)
c1, c2 = container.columns([5, 5])

with c1:
    with st.form(key='signup_column'):
        st.write("Don't have a profile? Create one now!")
        submit_button = st.form_submit_button("Sign Up")
        if submit_button:
            create_profile()

with c2:
    with st.form(key='login_column'):
        st.write("Already have a profile? Log in here!")
        login_button = st.form_submit_button("Log In")
        if login_button:
            login()
