from src import *

import pandas as pd
import plotly.express as px
from datetime import datetime as dt

st.set_page_config(
        page_title="Expendi",
        page_icon='💸',
        layout="wide"
    )

get_menu()

if not st.session_state.get('role'):
    with open("assets/homepage.md", "rb") as f:
        data = f.read()

    st.markdown(data.decode(), unsafe_allow_html=True)

else:
    if st.session_state.role == 'user' or st.session_state.role == 'admin':

        tabMainDashboard, tabAllTransactions= st.tabs(["Main Dashboard", "All Transactions"])

        with tabMainDashboard:
            data = pd.DataFrame(get_transactions_data()).transpose().reset_index(drop=True)

            if data.empty:
                st.write("No transactions found. Please insert a new transaction.")

                c1, c2, c3 = st.columns([3, 1, 1])

                with c3:
                    if st.button("Insert new Transaction", key='insert_transaction_p1'):
                        insert_transaction()
                    

            
            else:
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


                    colors = {'Income': 'green', 'Expense': 'red'}

                    fig = px.sunburst(category_group,
                                    title='Expenses by Category',
                                    path=['type', 'category', 'name'],
                                    values='amount', color='type',
                                    color_discrete_map=colors,
                                    custom_data=['percentage'],)
                    
                    # Update hover template to show percentage
                    fig.update_traces(hovertemplate='<b>%{label}</b><br>%{parent}: %{value} (%{customdata[0]:.2f}%)')

                    st.plotly_chart(fig, theme=None)
                    

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
            data = pd.DataFrame(get_transactions_data()).transpose().reset_index(drop=True)

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
                date_filter = colFilters.date_input("Select your date range", value=(dt.strptime(data['date'].min(),'%Y-%m-%d'), dt.strptime(data['date'].max(),'%Y-%m-%d')), key='start_date')
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

                filtered_data['amount'] = filtered_data['amount'].astype(float).apply(lambda x: '{:.2f}'.format(x))

                filtered_data = filtered_data[['name', 'amount', 'category', 'date', 'type']]
                filtered_data = filtered_data.set_index('date')

                filtered_data_previous_period = data[(data['date'] >= start_date_previous_peiod) & (data['date'] <= end_date_previous_peiod)]

                colTransactions.dataframe(filtered_data.sort_index(ascending=False),
                                        hide_index=True,
                                        column_order=('date', 'name', 'category', 'type', 'amount'),
                                        column_config={
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
                                            "date": st.column_config.DateColumn(
                                            "Date",
                                            help="The date of the transaction",
                                            format="YYYY-MM-DD",
                                            step=1
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
                colKPIs.metric("Total Income", str(round(totalIncome, 2)) + '$', str(round(totalIncome - totalIncomeLastPeriod, 2)) + '$ vs last period')

                totalExpense = filtered_data[filtered_data['type'] == 'Expense']['amount'].astype(float).sum()
                totalExpenseLastPeriod = filtered_data_previous_period[filtered_data_previous_period['type'] == 'Expense']['amount'].astype(float).sum()
                colKPIs.metric("Total Expense", str(round(totalExpense, 2)) + '$',str(round(totalExpense - totalExpenseLastPeriod, 2)) + '$ vs last period')

                totalAmount = filtered_data['amount'].astype(float).sum()
                totalAmountLastPeriod = filtered_data_previous_period['amount'].astype(float).sum()
                colKPIs.metric("Total Amount", str(round(totalAmount, 2)) + '$', str(round(totalAmount - totalAmountLastPeriod, 2)) + '$ vs last period')
