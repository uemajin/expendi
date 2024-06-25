from src import *

import pandas as pd
import plotly.express as px
from datetime import datetime as dt

get_menu()

if not st.session_state.get('role'):
    with open("assets/homepage.md", "rb") as f:
        data = f.read()

    st.markdown(data.decode(), unsafe_allow_html=True)

else:
    if st.session_state.role == 'user':

        tabMainDashboard, tabAllTransactions= st.tabs(["Main Dashboard", "All Transactions"])

        with tabMainDashboard:
            data = pd.DataFrame(get_transactions_data()).transpose().reset_index(drop=True)

            if data.empty:
                st.write("No transactions found. Please insert a new transaction.")
            
            else:
                data['amount'] = data['amount'].astype(float).apply(lambda x: '{:.2f}'.format(x))
                dataf = data.head(10).sort_values(by='date', ascending=False).style.applymap(bgcolor_positive_or_negative, subset=['amount'])
                
                col1, col2 = st.columns([2.5, 1.25])

                with col1: 
                    # Group by category and sum the amounts
                    #data['amount'] = data['amount'].astype(float)
                    category_group = data.copy()
                    category_group['amount'] = category_group['amount'].astype(float).abs()
                    category_group = category_group.groupby(['category', 'type', 'name'])['amount'].sum().reset_index()

                    # Calculate percentage values
                    category_group['percentage'] = category_group.groupby('type')['amount'].apply(lambda x: 100 * x / x.sum())

                    colors = {'income': 'green', 'expense': 'red'}

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
            
            else:
                
                colFilters.write("Filter Transactions")
                date_filter = colFilters.date_input("Select your date range", value=(dt.strptime(data['date'].min(),'%Y-%m-%d'), dt.strptime(data['date'].max(),'%Y-%m-%d')), key='start_date')
                
                # Convert date_filter to datetime objects
                start_date = dt.combine(date_filter[0], dt.min.time())
                try:
                    end_date = dt.combine(date_filter[1], dt.min.time())
                except IndexError:
                    end_date = dt.combine(date_filter[0], dt.max.time()) 

                data['date'] = pd.to_datetime(data['date'])

                # Filter data DataFrame based on date range
                filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

                filtered_data['amount'] = filtered_data['amount'].astype(float).apply(lambda x: '{:.2f}'.format(x))
                dataf = filtered_data.sort_values(by='date', ascending=False).style.applymap(bgcolor_positive_or_negative, subset=['amount'])
                colTransactions.dataframe(dataf, hide_index=True)

                # KPIs

                totalIncome = filtered_data[filtered_data['type'] == 'income']['amount'].astype(float).sum()
                colKPIs.metric("Total Income", totalIncome)

                totalExpense = filtered_data[filtered_data['type'] == 'expense']['amount'].astype(float).sum()
                colKPIs.metric("Total Expense", totalExpense)

                totalAmount = filtered_data['amount'].astype(float).sum()
                colKPIs.metric("Total Amount", totalAmount)

        # Transactions Menu

        t1, t2, t3, t4, t5, t6 = st.columns(6)

        if t1.button("Insert new Transaction"):
            insert_transaction()

        if t2.button("Remove Transaction"):
            remove_transaction()


        
        #transactions = db.child("transactions").child(st.session_state.uid).get().val()
