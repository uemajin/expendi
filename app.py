import pandas as pd
import plotly.express as px
from datetime import datetime as dt

import plotly.graph_objects as go
import streamlit.components.v1 as components
import json, base64, random

from src import *

db = Database()

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="wide"
    )

get_menu()

user = st.session_state.get('user', None)

if not user:

    with st.container(border=True):
        with open("assets/homepage.md", "rb") as f:
            data = f.read()

        st.markdown(data.decode(), unsafe_allow_html=True)

    all_users = db.load_user_photos()

    if len(all_users) == 0:
        pass

    else:
        st.subheader("Here are some users managing their finances with Expendi.")

        df = pd.DataFrame(all_users, columns=['Image'])

        # Convert each image to base64 string
        users_for_js = []
        for _, row in df.iterrows():
            b64_img = base64.b64encode(row['Image']).decode('utf-8')
            users_for_js.append({
                'id': f'{_}',
                'image': f"data:image/png;base64,{b64_img}",
                'size': random.randint(10, 100)  # random size
            })

        js_data = json.dumps({"children": users_for_js})

        # HTML + D3 with images
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                }}
                svg {{
                    display: block;
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

                const svg = d3.select("#viz")
                    .append("svg")
                    .attr("width", width)
                    .attr("height", height);

                // Define global clip paths in <defs>
                const defs = svg.append("defs");

                data.children.forEach(d => {{
                    defs.append("clipPath")
                        .attr("id", "clip-" + d.id)
                    .append("circle")
                        .attr("r", d.size)
                        .attr("cx", 0)
                        .attr("cy", 0);
                }});

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

                node.append("image")
                    .attr("href", d => d.image)
                    .attr("x", d => -d.size)
                    .attr("y", d => -d.size)
                    .attr("width", d => d.size * 2)
                    .attr("height", d => d.size * 2)
                    .attr("clip-path", d => "url(#clip-" + d.id + ")")
                    .attr("preserveAspectRatio", "xMidYMid slice");

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
                        d.vx = dx / dt * 20;
                        d.vy = dy / dt * 20;
                    }}
                    d.fx = null;
                    d.fy = null;
                    lastEvent = null;
                }}
            </script>
        </body>
        </html>
"""


        components.html(html_code, height=2048, scrolling=False)

    

else:
    tabMainDashboard, tabAllTransactions= st.tabs(["Main Dashboard", "All Transactions"])

    data = db.load_transactions(user.user_id)

    with tabMainDashboard:

        if data.empty:
            st.write("No transactions found. Please insert a new transaction.")

            c1, c2, c3 = st.columns([3, 1, 1])

            with c3:
                if st.button("Insert new Transaction", key='insert_transaction_p1'):
                    insert_transaction()

        else:
            
            data['amount'] = data.apply(
                lambda row: row['amount'] * get_exchange_rate(
                    row['currency'],
                    user.preferred_currency,
                    row['date'].strftime('%Y-%m-%d') if isinstance(row['date'], pd.Timestamp) else str(row['date'])
                ),
                axis=1
            )

            data['amount'] = data['amount'].astype(float).apply(lambda x: '{:.2f}'.format(x))
            dataf = (data.head(10)
                    .sort_values(by='date', ascending=False)
                    .style
                    .apply(lambda row: [bgcolor_positive_or_negative(cell) for cell in row], subset=['amount'])
)


            col1, col2 = st.columns([2.5, 1.25])

            with col1:
                # Group by category and sum the amounts
                #data['amount'] = data['amount'].astype(float)
                category_group = data.copy()
                category_group['amount'] = category_group['amount'].astype(float).abs()
                category_group = category_group.groupby(['category', 'type', 'name'])['amount'].sum().reset_index()

                # Calculate percentage values
                #category_group['percentage'] = category_group.groupby('type')['amount'].apply(lambda x: 100 * x / x.sum())
                category_group['percentage'] = category_group.groupby('type')['amount'].transform(lambda x: 100 * x / x.sum())

                data['date'] = pd.to_datetime(data['date'])
                data['month'] = data['date'].dt.to_period('M').astype(str)

                # Convert amount to float
                data['amount'] = data['amount'].astype(float)

                # Optional: invert expenses to be negative (if not already)
                #data.loc[data['transaction_type'] == 'Expense', 'amount'] *= -1

                # Group by month and type
                monthly_summary = (
                    data.groupby(['month', 'type'])['amount']
                    .sum()
                    .reset_index()
                )
                
                monthly_summary['month'] = pd.to_datetime(monthly_summary['month'], format='%Y-%m')
                six_months_ago = pd.to_datetime(datetime.today()).replace(day=1) - pd.DateOffset(months=5)
                monthly_summary = monthly_summary[monthly_summary['month'] >= six_months_ago]
                monthly_summary['month'] = monthly_summary['month'].dt.strftime('%Y-%m')

                monthly_summary['amount_label'] = monthly_summary['amount'].map(lambda x: currency_format(x, user.preferred_currency))

                # Plot with Plotly
                fig = px.bar(
                    monthly_summary,
                    x='month',
                    y='amount',
                    color='type',
                    color_discrete_map={
                        'Income': '#90EE90',   # Soft green
                        'Expense': '#F08080'   # Soft red
                    },
                    barmode='relative',
                    text='amount_label'
                )

                fig.update_layout(
                    title='Monthly Cash Flow',
                    xaxis_title='Month',
                    yaxis_title='Net Amount',
                    legend_title='Transaction Type',
                    height=400,
                    bargap=0.25,
                    font=dict(size=12),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )

                st.plotly_chart(fig, theme='streamlit', use_container_width=True)


            with col2:
                st.write("Last Transactions")
                st.dataframe(dataf,
                            column_order=('name', 'amount'),
                            column_config={
                                        "name": st.column_config.TextColumn(
                                        "Transaction",
                                        help="The name of the transaction"
                                        ),
                                        "amount": st.column_config.NumberColumn(
                                        "Amount",
                                        help="The price of the transaction",
                                        format="%.2f",
                                        )
                                    },
                            hide_index=True)

    with tabAllTransactions:

        colTransactions, colKPIs, colFilters = st.columns([3, 1, 1])

        if data.empty:
            st.write("No transactions found. Please insert a new transaction.")

            c1, c2, c3 = st.columns([3, 1, 1])

            with c3:
                if st.button("Insert new Transaction", key='insert_transaction_p2'):
                    insert_transaction()

        else:

            # Filter Transactions

            if colFilters.button("Insert new Transaction"):
                insert_transaction()

            if colFilters.button("Edit Transaction"):
                edit_transaction()

            if colFilters.button("Remove Transaction"):
                remove_transaction()

            colFilters.write("Filter Transactions")
            date_filter = colFilters.date_input("Select your date range", value=(data['date'].max()- timedelta(7), data['date'].max()), key='start_date')
            category_filter = colFilters.multiselect("Select the category of transaction", data['category'].unique(), key='category_filter')

            # Convert date_filter to datetime objects
            start_date = dt.combine(date_filter[0], dt.min.time())
            try:
                end_date = dt.combine(date_filter[1], dt.min.time())
            except IndexError:
                end_date = dt.combine(date_filter[0], dt.max.time())

            start_date_previous_peiod = start_date - pd.DateOffset(months=1)
            end_date_previous_peiod = end_date - pd.DateOffset(months=1)

            data['date'] = pd.to_datetime(data['date'])

            # Filter data DataFrame based on date range
            filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

            # Filter data DataFrame based on category
            if category_filter:
                filtered_data = filtered_data[filtered_data['category'].isin(category_filter)]

            filtered_data = filtered_data.copy()
            filtered_data['amount'] = filtered_data['amount'].astype(float).apply(lambda x: '{:.2f}'.format(x))

            filtered_data = filtered_data[['name', 'amount', 'category', 'date', 'type']]
            filtered_data = filtered_data.set_index('date')

            filtered_data_previous_period = data[(data['date'] >= start_date_previous_peiod) & (data['date'] <= end_date_previous_peiod)]

            colTransactions.dataframe(filtered_data.sort_index(ascending=False),
                                    hide_index=False,
                                    column_order=('date', 'name', 'category', 'type', 'amount'),
                                    column_config={
                                        "date": st.column_config.DateColumn(
                                        "Date",
                                        help="The date of the transaction",
                                        format="YYYY-MM-DD",
                                        step=1
                                        ),
                                        "name": st.column_config.TextColumn(
                                        "Transaction",
                                        help="The name of the transaction"
                                        ),
                                        "amount": st.column_config.NumberColumn(
                                        "Amount",
                                        help="The price of the transaction",
                                        format="%.2f",
                                        ),
                                        "category": st.column_config.TextColumn(
                                        "Category",
                                        help="The category of the transaction"
                                        ),
                                        "type": st.column_config.TextColumn(
                                        "Type",
                                        help="The type of the transaction"
                                        )
                                        }
                                    , use_container_width=True

                                    )

            # KPIs

            totalIncome = filtered_data[filtered_data['type'] == 'Income']['amount'].astype(float).sum()
            totalIncomeLastPeriod = filtered_data_previous_period[filtered_data_previous_period['type'] == 'Income']['amount'].astype(float).sum()
            colKPIs.metric("Total Income", currency_format(totalIncome, user.preferred_currency), str(currency_format(totalIncome - totalIncomeLastPeriod, user.preferred_currency)) + ' vs last period')

            totalExpense = filtered_data[filtered_data['type'] == 'Expense']['amount'].astype(float).sum()
            totalExpenseLastPeriod = filtered_data_previous_period[filtered_data_previous_period['type'] == 'Expense']['amount'].astype(float).sum()
            colKPIs.metric("Total Expense", currency_format(totalExpense, user.preferred_currency), str(currency_format(totalExpense - totalExpenseLastPeriod, user.preferred_currency)) + ' vs last period')

            totalAmount = filtered_data['amount'].astype(float).sum()
            totalAmountLastPeriod = filtered_data_previous_period['amount'].astype(float).sum()
            colKPIs.metric("Total Amount", currency_format(totalAmount, user.preferred_currency), str(currency_format(totalAmount - totalAmountLastPeriod, user.preferred_currency)) + ' vs last period')
