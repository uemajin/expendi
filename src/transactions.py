import streamlit as st
from .firebase_auth import *
import time

auth, db = get_config()
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
        transaction_type = 'income'
    else:
        category = st.selectbox("Category:", ["Food", "Transport", "Entertainment", "Rent", "Credit Card", "Others"])
        transaction_type = 'expense'

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