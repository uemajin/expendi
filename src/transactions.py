import time
import streamlit as st
import pandas as pd
import numpy as np

import bcrypt

from src.helper import *
from .database import *
from .user import User

db = Database()

@st.dialog("Create Profile")
def create_profile():
    with st.form(key="create_profile_form"):
        username = st.text_input("Username:")
        fullname = st.text_input("Full Name:")
        password = st.text_input("Password:", type="password")
        password_confirm = st.text_input("Confirm Password:", type="password")
        profile_img = st.file_uploader("Profile Image", type=["png", "jpg", "jpeg", "gif"])

        submit_button = st.form_submit_button("Create Profile")
        if submit_button:

            if not username:
                st.warning("Username is required.")
                return
            if not fullname:
                st.warning("Full Name is required.")
                return
            if not password:
                st.warning("Password is required.")
                return
            if password != password_confirm:
                st.warning("Passwords do not match.")
                return
            
            if db.check_user_exists(username):
                st.warning("Username already exists. Please choose a different username.")
                return
            
            if not profile_img:
                profile_img = "assets/images/default.png"

            db.create_user_profile(username, fullname, password, profile_img, preferred_currency="USD")
            st.success("Profile created successfully!")
            time.sleep(2)
            st.rerun()

@st.dialog("Log In")
def login():
    with st.form(key="login_form"):

        st.write("Welcome back! Please log in to continue.")
        
        username = st.text_input("Username:", value=st.session_state.get("username", ""))
        password = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button("Log In")

        if submit_button:
            
            if not password:
                st.warning("Password is required.")
                return
            
            user_check = db.get_user_data(username)
          
            if username == user_check['username'] and bcrypt.hashpw(password.encode('utf-8'), user_check['salt']) == user_check["password_hash"]:

                session_user = User(
                    user_id=user_check['user_id'],
                    username=user_check['username'],
                    fullname=user_check['fullname'],
                    photo=user_check['photo'],
                    password_hash=user_check['password_hash'],
                    salt=user_check['salt'],
                    preferred_currency=user_check['preferred_currency']
                )

                st.session_state.user_logged_in = True
                st.session_state.user = session_user

                st.success("Logged in successfully!")
                time.sleep(2)
                st.switch_page("app.py")

            else:
                st.error("Invalid username or password.")


@st.dialog("Edit Profile")
def edit_profile(user):
    with st.form(key="edit_profile_form"):

        c1, c2 = st.columns([1, 1.8])
        username = c2.text_input("Username:", value=user.username, disabled=True)
        fullname = c2.text_input("Full Name:", value=user.fullname)
        profile_img = c1.image(user.photo, use_container_width=True)

        new_profile_img = st.file_uploader("Profile Image", type=["png", "jpg", "jpeg", "gif"])

        if new_profile_img:
            profile_img = process_image(new_profile_img)
        else:
            profile_img = user.photo

        update_password = st.text_input("New Password:", type="password")
        confirm_password = st.text_input("Confirm New Password:", type="password")

        preferred_currency = st.selectbox(
            "Preferred Currency:",
            options=["USD", "EUR", "GBP", "JPY", "AUD", "BRL"],
            index=["USD", "EUR", "GBP", "JPY", "AUD", "BRL"].index(st.session_state.user.preferred_currency)
        )

        c1, c2, c3 = st.columns([1, 2.9, 1])

        if st.form_submit_button("Update"):

            if update_password:

                if len(update_password) < 8:
                    st.error("Password must be at least 8 characters long.")
                    return

                if update_password != confirm_password:
                    st.error("Passwords do not match.")
                    return
                
                salt = bcrypt.gensalt()
                new_password = bcrypt.hashpw(update_password.encode('utf-8'), salt)

            else:
                new_password = user.password_hash
                salt = user.salt

            st.write("Updating profile...")

            db.update_user_profile(user.user_id, username, fullname, profile_img, new_password, salt, preferred_currency)
            st.success("Profile updated successfully!")

            st.session_state.user = User(
                user_id=user.user_id,
                username=username,
                fullname=fullname,
                photo=profile_img,
                password_hash=new_password,
                salt=salt,
                preferred_currency=preferred_currency
            )

            time.sleep(2)
            st.rerun()

@st.dialog("Delete Profile")
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

@st.dialog("Insert Transaction")
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

    currency = st.selectbox(
        "Currency:",
        options=["USD", "EUR", "GBP", "JPY", "AUD", "BRL"],
        index=["USD", "EUR", "GBP", "JPY", "AUD", "BRL"].index(st.session_state.user.preferred_currency)
    )

    if st.button("Submit"):

        db.insert_transaction(st.session_state.user.user_id, transaction_name, amount, date, category, transaction_type, currency)

        st.success("Transaction inserted successfully!")
        time.sleep(2)
        st.rerun()

@st.dialog("Remove Transaction")
def remove_transaction():

    transactions = db.load_transactions(st.session_state.user.user_id)
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

@st.dialog("Edit Transaction", width="large")
def edit_transaction():
    transactions = db.load_transactions(st.session_state.user.user_id)
    transactions['date'] = pd.to_datetime(transactions['date'])

    st.write("Edit transactions")
    updated_data = st.data_editor(
        transactions,
        hide_index=True,
        column_order=('date', 'name', 'category', 'type', 'amount', 'currency'),
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
            ),
            "currency": st.column_config.SelectboxColumn(
                "Currency",
                help="The currency of the transaction",
                options=["USD", "EUR", "GBP", "JPY", "AUD", "BRL"]
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

            db.update_transaction(st.session_state.user.user_id, row_dict['transaction_id'], row_dict['name'], row_dict['amount'], row_dict['date'], row_dict['category'], row_dict['type'], row_dict['currency'])

        st.success("Transaction(s) edited successfully!")
        time.sleep(2)
        st.rerun()
