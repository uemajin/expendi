from src import *

import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Finance Dashboard", page_icon="💰")
st.title("Finance Dashboard")

get_menu()

if 'role' in st.session_state:
    if st.session_state.role == 'user':
        st.write("Welcome, ", st.session_state.user)

        data = pd.DataFrame(get_transactions_data()).transpose().reset_index(drop=True)

        if data.empty:
            st.write("No transactions found. Please insert a new transaction.")
        
        else:
            data['amount'] = data['amount'].astype(float).apply(lambda x: '{:.2f}'.format(x))
            dataf = data.sort_values(by='date', ascending=False).style.applymap(bgcolor_positive_or_negative, subset=['amount'])
            
            col1, col2 = st.columns([2.5, 1.25])

            with col1: 
                # Group by category and sum the amounts
                #data['amount'] = data['amount'].astype(float)
                category_group = data.copy()
                category_group['amount'] = category_group['amount'].astype(float).abs()
                category_group = category_group.groupby(['category', 'type'])['amount'].sum().reset_index()

                # Calculate percentage values
                category_group['percentage'] = category_group.groupby('type')['amount'].apply(lambda x: 100 * x / x.sum())

                colors = {'income': 'green', 'expense': 'red'}

                fig = px.sunburst(category_group,
                                path=['type', 'category'],
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

        if st.button("Insert new Transaction"):
            insert_transaction()



        
        #transactions = db.child("transactions").child(st.session_state.uid).get().val()
