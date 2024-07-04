import time
import streamlit as st
import pandas as pd
import numpy as np

from src.helper import *
from .database import *

db = Database()

@st.experimental_dialog("Create Profile")
def create_profile():
    with st.form(key="create_profile_form"):
        username = st.text_input("Username:")
        fullname = st.text_input("Full Name:")
        profile_img = st.file_uploader("Profile Image", type=["png", "jpg", "jpeg", "gif"])

        if profile_img:
            process_image(profile_img, username)

        else:
            process_image("assets/images/default.png", username)

        if st.form_submit_button("Create Profile"):
            db.create_user_profile(username, fullname)
            st.success("Profile created successfully!")
            time.sleep(2)
            st.rerun()

@st.experimental_dialog("Edit Profile")
def edit_profile(user):
    with st.form(key="edit_profile_form"):

        c1, c2 = st.columns([1, 1.8])
        username = c2.text_input("Username:", value=user[1])
        fullname = c2.text_input("Full Name:", value=user[2])
        profile_img = c1.image(load_user_profile_image_local(username), use_column_width=True)

        new_profile_img = st.file_uploader("Profile Image", type=["png", "jpg", "jpeg", "gif"])

        enable_delete = st.checkbox("Enable Profile Delete", value=st.session_state.get("delete_enabled_" + username, False))

        st.session_state["delete_enabled_" + username] = True if enable_delete else False

        if new_profile_img:
            process_image(new_profile_img, username)

        c1, c2, c3 = st.columns([1, 2.9, 1])

        if st.form_submit_button("Update"):
            st.write("Updating profile...")
            db.update_user_profile(user[0], username, fullname)
            st.success("Profile updated successfully!")
            time.sleep(2)
            st.rerun()

@st.experimental_dialog("Delete Profile")
def delete_profile(user):
    st.write("Are you sure you want to delete your profile?")

    c1, c2, c3 = st.columns([1, 5.5, 1])
    if c1.button("Yes"):
        db.delete_user_profile(user[0])
        st.success("Profile deleted successfully!")
        time.sleep(2)
        st.rerun()

    if c3.button("No"):
        st.rerun()

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

        db.insert_transaction(st.session_state.user_id, transaction_name, amount, date, category, transaction_type)

        st.success("Transaction inserted successfully!")
        time.sleep(2)
        st.rerun()

@st.experimental_dialog("Remove Transaction")
def remove_transaction():

    transactions = db.load_transactions(st.session_state.user_id)
    selectedTransactionsDict = st.dataframe(transactions, column_order=('date', 'name', 'category', 'type', 'amount'), on_select="rerun", selection_mode="multi-row", hide_index=True)

    transactionsList = selectedTransactionsDict.selection.rows
    filtered_df = transactions.iloc[transactionsList]

    st.write("You selected {} rows".format(len(filtered_df)))

    if st.button("Submit"):

        for index, row in filtered_df.iterrows():

            db.delete_transaction(row['transaction_id'])

        st.success("Transaction(s) removed successfully!")
        time.sleep(2)
        st.rerun()

@st.experimental_dialog("Edit Transaction")
def edit_transaction():
    transactions = db.load_transactions(st.session_state.user_id)
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

            db.update_transaction(st.session_state.user_id, row_dict['transaction_id'], row_dict['name'], row_dict['amount'], row_dict['date'], row_dict['category'], row_dict['type'])

        st.success("Transaction(s) edited successfully!")
        time.sleep(2)
        st.rerun()
