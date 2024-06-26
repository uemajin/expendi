import streamlit as st
import pandas as pd
import numpy as np
from .firebase_auth import *
import time

auth = getFirebaseAuth()
db = getFirebaseDB()
storage = getFirebaseStorage()

def get_transactions_data():
    transactions = db.child("transactions").child(st.session_state.uid).get().val()
    return transactions

@st.experimental_dialog("Insert Transaction")
def insert_transaction():

    transaction_name = st.text_input("Name of the transaction:")
    amount = st.number_input("Amount:", format="%.2f")
    date = st.date_input("Date:")
    if amount > 0:
        category = st.selectbox("Category:", ["Payment", "Salary", "Investment", "Others"])
        transaction_type = 'Income'
    else:
        category = st.selectbox("Category:", ["Food", "Transport", "Entertainment", "Rent", "Credit Card", "Health", "Education", "Others"])
        transaction_type = 'Expense'

    if st.button("Submit"):

        db.child("transactions").child(st.session_state.uid).push({
            "name": transaction_name,
            "amount": amount,
            "date": str(date),
            "category": category,
            "type": transaction_type
        })

        st.success("Transaction inserted successfully!")
        time.sleep(2)
        st.rerun()

@st.experimental_dialog("Remove Transaction")
def remove_transaction():

    transactions = pd.DataFrame(get_transactions_data()).transpose()

    selectedTransactionsDict = st.dataframe(transactions, on_select="rerun", selection_mode="multi-row", hide_index=True)

    transactionsList = selectedTransactionsDict.selection.rows
    filtered_df = transactions.iloc[transactionsList]

    st.write("You selected {} rows".format(len(filtered_df)))

    if st.button("Submit"):

        for index, row in filtered_df.iterrows():
            db.child("transactions").child(st.session_state.uid).child(index).remove()

        st.success("Transaction(s) removed successfully!")
        time.sleep(2)
        st.rerun()

@st.experimental_dialog("Edit Transaction")
def edit_transaction():
    transactions = pd.DataFrame(get_transactions_data()).transpose()
    transactions['date'] = pd.to_datetime(transactions['date'])

    st.write("Edit transactions")
    updated_data = st.data_editor(
        transactions,
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
            "category": st.column_config.SelectboxColumn(
                "Category",
                help="The category of the transaction",
                options=transactions['category'].unique()
            ),
            "date": st.column_config.DateColumn(
                "Date",
                help="The date of the transaction"
            ),
            "type": st.column_config.TextColumn(
                "Type",
                help="The type of the transaction"
            )
        }
    )

    changes_mask = np.any(transactions.values != updated_data.values, axis=1)
    df = updated_data[changes_mask]

    st.write("Changes made")
    changes_report = []
    for row_num, (index, row) in enumerate(df.iterrows()):
        original_row = transactions.loc[index]
        updated_row = updated_data.loc[index]
        changes = []
        for col in transactions.columns:
            if original_row[col] != updated_row[col]:
                changes.append(f"- **Updated {col}** from `{original_row[col]}` to `{updated_row[col]}`")
        if changes:
            changes_report.append(f"### Row {row_num + 1}")
            changes_report.extend(changes)
            changes_report.append("")  # Add a newline for separation

    st.markdown("\n".join(changes_report))

    if st.button("Submit"):
        for index, row in updated_data.iterrows():
            row_dict = row.to_dict()
            row_dict['date'] = row_dict['date'].strftime('%Y-%m-%d')  # Convert Timestamp to string
            db.child("transactions").child(st.session_state.uid).child(index).update(row_dict)

        st.success("Transaction(s) edited successfully!")
        time.sleep(2)
        st.rerun()